"""
BYDFi relay: recibe las alertas webhook de TradingView y opera en BYDFi.

Funciona por "posición objetivo": cada alerta trae la posición que la estrategia
tiene DESPUÉS de la orden ({{strategy.market_position}} y
{{strategy.market_position_size}}). El relay compara con la posición real en
BYDFi y envía solo la diferencia. Así, si una alerta se pierde o llega dos
veces, la siguiente deja la cuenta sincronizada igualmente.

BYDFi a través de CCXT solo ofrece futuros perpetuos (BTC/USDT:USDT). Con
apalancamiento 1x y solo largos, el resultado es parecido a operar spot
(más/menos el funding).

Variables de entorno (ver .env.example):
  BYDFI_API_KEY, BYDFI_API_SECRET   claves de la API (sin permiso de retiro)
  WEBHOOK_SECRET                    debe coincidir con "secret" en la alerta
  SYMBOL            BTC/USDT:USDT
  LEVERAGE          1
  MARGIN_MODE       isolated | cross
  MAX_POSITION_BTC  0.01   tope de seguridad del tamaño absoluto
  ALLOW_SHORT       false
  DRY_RUN           true   (true = solo registra, no envía órdenes)
  ALLOWED_IPS       opcional, lista separada por comas
  PORT              8080
"""
from __future__ import annotations

import hmac
import json
import logging
import os
import threading
from dataclasses import dataclass
from decimal import Decimal, ROUND_DOWN

log = logging.getLogger("bydfi_relay")


# ───────────────────────── lógica pura (testeable) ─────────────────────────

@dataclass(frozen=True)
class PlannedOrder:
    side: str          # "buy" | "sell"
    btc: Decimal       # cantidad en BTC (siempre > 0)
    reduce_only: bool


def parse_target(payload: dict, allow_short: bool, max_btc: Decimal) -> Decimal:
    """Convierte la alerta en una posición objetivo con signo, en BTC."""
    mp = str(payload.get("market_position", "")).strip().lower()
    if mp not in ("long", "short", "flat"):
        raise ValueError(f"market_position inválido: {mp!r}")
    if mp == "flat":
        return Decimal("0")
    try:
        size = abs(Decimal(str(payload.get("position_size", "0"))))
    except Exception as exc:  # noqa: BLE001
        raise ValueError("position_size no es un número") from exc
    if mp == "short":
        if not allow_short:
            return Decimal("0")
        size = -size
    if abs(size) > max_btc:
        size = max_btc if size > 0 else -max_btc
    return size


def plan_orders(current: Decimal, target: Decimal, min_btc: Decimal) -> list[PlannedOrder]:
    """Órdenes de mercado necesarias para pasar de `current` a `target` (BTC con signo)."""
    orders: list[PlannedOrder] = []
    if abs(target - current) < min_btc:
        return orders
    # Cambio de lado: primero cerrar, luego abrir.
    if current != 0 and (target == 0 or (current > 0) != (target > 0)):
        orders.append(PlannedOrder("sell" if current > 0 else "buy", abs(current), True))
        current = Decimal("0")
    delta = target - current
    if abs(delta) < min_btc:
        return orders
    reducing = current != 0 and abs(target) < abs(current)
    orders.append(PlannedOrder("buy" if delta > 0 else "sell", abs(delta), reducing))
    return orders


def parse_protection(payload: dict) -> tuple[Decimal | None, Decimal | None]:
    """SL y TP opcionales enviados por la estrategia (vacíos o ausentes = None)."""
    out = []
    for key in ("sl", "tp"):
        raw = str(payload.get(key, "") or "").strip()
        try:
            val = Decimal(raw) if raw else None
        except Exception:  # noqa: BLE001
            val = None
        out.append(val if val is not None and val > 0 else None)
    return out[0], out[1]


def protection_valid(target: Decimal, ref_price: Decimal, sl: Decimal | None, tp: Decimal | None) -> bool:
    """El SL debe quedar del lado de la pérdida y el TP del lado de la ganancia."""
    if target > 0:
        return (sl is None or sl < ref_price) and (tp is None or tp > ref_price)
    if target < 0:
        return (sl is None or sl > ref_price) and (tp is None or tp < ref_price)
    return False


def check_secret(payload: dict, expected: str) -> bool:
    got = str(payload.get("secret", ""))
    return bool(expected) and hmac.compare_digest(got.encode(), expected.encode())


# ───────────────────────────── exchange ─────────────────────────────

class Broker:
    def __init__(self, exchange, symbol: str, dry_run: bool):
        self.ex = exchange
        self.symbol = symbol
        self.dry_run = dry_run
        self.lock = threading.Lock()
        self.market = None

    def setup(self, leverage: int, margin_mode: str) -> None:
        self.ex.load_markets()
        self.market = self.ex.market(self.symbol)
        if self.dry_run:
            log.info("DRY_RUN: no se cambia apalancamiento ni modo de margen")
            return
        for fn, args in ((self.ex.set_margin_mode, (margin_mode, self.symbol)),
                         (self.ex.set_leverage, (leverage, self.symbol))):
            try:
                fn(*args)
            except Exception as exc:  # noqa: BLE001
                log.warning("%s falló (puede que ya esté configurado): %s", fn.__name__, exc)

    @property
    def contract_size(self) -> Decimal:
        return Decimal(str(self.market.get("contractSize") or 1))

    @property
    def min_btc(self) -> Decimal:
        min_contracts = (self.market.get("limits", {}).get("amount", {}) or {}).get("min") or 0
        return Decimal(str(min_contracts)) * self.contract_size

    def position_btc(self) -> Decimal:
        total = Decimal("0")
        for p in self.ex.fetch_positions([self.symbol]):
            if p.get("symbol") != self.symbol:
                continue
            contracts = Decimal(str(p.get("contracts") or 0))
            btc = contracts * self.contract_size
            total += -btc if p.get("side") == "short" else btc
        return total

    def to_contracts(self, btc: Decimal) -> str:
        contracts = (btc / self.contract_size).quantize(Decimal("1e-8"), rounding=ROUND_DOWN)
        return self.ex.amount_to_precision(self.symbol, float(contracts))

    def protect(self, target: Decimal, sl: Decimal | None, tp: Decimal | None) -> list[dict]:
        """Coloca SL y TP reduceOnly en BYDFi para la posición abierta."""
        placed: list[dict] = []
        if sl is None and tp is None:
            return placed
        ref = Decimal(str(self.ex.fetch_ticker(self.symbol)["last"]))
        if not protection_valid(target, ref, sl, tp):
            log.warning("SL/TP inválidos para precio %s: sl=%s tp=%s", ref, sl, tp)
            return [{"skipped": "SL/TP del lado equivocado del precio actual"}]
        side = "sell" if target > 0 else "buy"
        amount = self.to_contracts(abs(target))
        for kind, price in (("stopLossPrice", sl), ("takeProfitPrice", tp)):
            if price is None:
                continue
            entry = {"type": kind, "price": str(price), "contracts": amount}
            if self.dry_run:
                entry["skipped"] = "DRY_RUN"
            else:
                params = {kind: float(price), "reduceOnly": True}
                entry["order_id"] = self.ex.create_order(self.symbol, "market", side, float(amount), None, params).get("id")
            placed.append(entry)
        return placed

    def cancel_open_orders(self) -> None:
        if self.dry_run:
            return
        try:
            self.ex.cancel_all_orders(self.symbol)
        except Exception as exc:  # noqa: BLE001
            log.warning("cancel_all_orders falló: %s", exc)

    def sync(self, target: Decimal, sl: Decimal | None = None, tp: Decimal | None = None) -> dict:
        with self.lock:
            current = self.position_btc()
            orders = plan_orders(current, target, self.min_btc)
            result = {"current_btc": str(current), "target_btc": str(target),
                      "dry_run": self.dry_run, "orders": []}
            for o in orders:
                amount = self.to_contracts(o.btc)
                entry = {"side": o.side, "btc": str(o.btc), "contracts": amount,
                         "reduce_only": o.reduce_only}
                if float(amount) <= 0:
                    entry["skipped"] = "cantidad por debajo de la precisión"
                elif self.dry_run:
                    entry["skipped"] = "DRY_RUN"
                else:
                    params = {"reduceOnly": True} if o.reduce_only else {}
                    order = self.ex.create_order(self.symbol, "market", o.side, float(amount), None, params)
                    entry["order_id"] = order.get("id")
                result["orders"].append(entry)
            if orders:
                # La posición cambió: los SL/TP anteriores ya no sirven.
                self.cancel_open_orders()
                if target != 0:
                    result["protection"] = self.protect(target, sl, tp)
            log.info("sync %s", json.dumps(result))
            return result


# ───────────────────────────── servidor web ─────────────────────────────

def env_bool(name: str, default: bool) -> bool:
    return os.getenv(name, str(default)).strip().lower() in ("1", "true", "yes", "si", "sí")


def create_app(broker: Broker, secret: str, allow_short: bool, max_btc: Decimal,
               allowed_ips: set[str] | None = None):
    from flask import Flask, jsonify, request

    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify(ok=True, symbol=broker.symbol, dry_run=broker.dry_run)

    @app.post("/webhook")
    def webhook():
        ip = request.headers.get("X-Forwarded-For", request.remote_addr or "").split(",")[0].strip()
        if allowed_ips and ip not in allowed_ips:
            log.warning("IP rechazada: %s", ip)
            return jsonify(error="forbidden"), 403
        try:
            payload = json.loads(request.get_data(as_text=True) or "{}")
        except json.JSONDecodeError:
            return jsonify(error="el cuerpo no es JSON"), 400
        if not check_secret(payload, secret):
            log.warning("secreto incorrecto desde %s", ip)
            return jsonify(error="unauthorized"), 401
        try:
            target = parse_target(payload, allow_short, max_btc)
        except ValueError as exc:
            return jsonify(error=str(exc)), 400
        try:
            sl, tp = parse_protection(payload)
            return jsonify(broker.sync(target, sl, tp))
        except Exception as exc:  # noqa: BLE001
            log.exception("error al operar")
            return jsonify(error=str(exc)), 502

    return app


def main() -> None:
    import ccxt

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                        handlers=[logging.StreamHandler(), logging.FileHandler("relay.log")])
    secret = os.getenv("WEBHOOK_SECRET", "")
    if len(secret) < 16:
        raise SystemExit("WEBHOOK_SECRET debe tener al menos 16 caracteres")
    dry_run = env_bool("DRY_RUN", True)
    exchange = ccxt.bydfi({
        "apiKey": os.getenv("BYDFI_API_KEY", ""),
        "secret": os.getenv("BYDFI_API_SECRET", ""),
        "enableRateLimit": True,
    })
    broker = Broker(exchange, os.getenv("SYMBOL", "BTC/USDT:USDT"), dry_run)
    broker.setup(int(os.getenv("LEVERAGE", "1")), os.getenv("MARGIN_MODE", "isolated"))
    ips = {x.strip() for x in os.getenv("ALLOWED_IPS", "").split(",") if x.strip()} or None
    app = create_app(broker, secret, env_bool("ALLOW_SHORT", False),
                     Decimal(os.getenv("MAX_POSITION_BTC", "0.01")), ips)
    log.info("relay listo: %s dry_run=%s", broker.symbol, dry_run)
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))


if __name__ == "__main__":
    main()
