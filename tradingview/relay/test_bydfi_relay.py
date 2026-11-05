import json
import unittest
from decimal import Decimal as D

from bydfi_relay import Broker, PlannedOrder, create_app, parse_target, plan_orders

SECRET = "x" * 20


class FakeExchange:
    def __init__(self, position_btc="0", contract_size=0.001, min_contracts=1):
        self.pos = D(position_btc)
        self.cs = D(str(contract_size))
        self.min_contracts = min_contracts
        self.orders = []

    def load_markets(self):
        pass

    def set_margin_mode(self, mode, symbol):
        self.margin_mode = mode

    def set_leverage(self, leverage, symbol):
        self.leverage = leverage

    def market(self, symbol):
        return {"contractSize": float(self.cs), "limits": {"amount": {"min": self.min_contracts}}}

    def fetch_positions(self, symbols):
        if self.pos == 0:
            return []
        return [{"symbol": symbols[0], "contracts": float(abs(self.pos) / self.cs),
                 "side": "long" if self.pos > 0 else "short", "entryPrice": 99950.0}]

    def fetch_ticker(self, symbol):
        return {"last": 100000.0}

    def cancel_all_orders(self, symbol):
        self.cancelled = getattr(self, "cancelled", 0) + 1
        self.orders = [o for o in self.orders if "stopLossPrice" not in o[2] and "takeProfitPrice" not in o[2]]

    def price_to_precision(self, symbol, price):
        return str(round(price, 1))

    def amount_to_precision(self, symbol, amount):
        return str(int(amount))

    def create_order(self, symbol, type_, side, amount, price, params):
        if "stopLossPrice" in params or "takeProfitPrice" in params:
            self.orders.append((side, amount, params))
            return {"id": str(len(self.orders))}
        btc = D(str(amount)) * self.cs
        self.pos += btc if side == "buy" else -btc
        self.orders.append((side, amount, params))
        return {"id": str(len(self.orders))}


class PlanTests(unittest.TestCase):
    def test_open_long(self):
        self.assertEqual(plan_orders(D(0), D("0.01"), D("0.001")),
                         [PlannedOrder("buy", D("0.01"), False)])

    def test_close_long(self):
        self.assertEqual(plan_orders(D("0.01"), D(0), D("0.001")),
                         [PlannedOrder("sell", D("0.01"), True)])

    def test_reduce_long(self):
        self.assertEqual(plan_orders(D("0.01"), D("0.004"), D("0.001")),
                         [PlannedOrder("sell", D("0.006"), True)])

    def test_reverse(self):
        self.assertEqual(plan_orders(D("0.01"), D("-0.02"), D("0.001")),
                         [PlannedOrder("sell", D("0.01"), True), PlannedOrder("sell", D("0.02"), False)])

    def test_already_in_sync(self):
        self.assertEqual(plan_orders(D("0.01"), D("0.01"), D("0.001")), [])


class TargetTests(unittest.TestCase):
    def test_long_capped(self):
        t = parse_target({"market_position": "long", "position_size": "5"}, False, D("0.05"))
        self.assertEqual(t, D("0.05"))

    def test_short_disabled_goes_flat(self):
        t = parse_target({"market_position": "short", "position_size": "0.01"}, False, D("1"))
        self.assertEqual(t, D(0))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            parse_target({"market_position": "buy"}, False, D("1"))


class AppTests(unittest.TestCase):
    def make(self, dry_run=False, pos="0"):
        ex = FakeExchange(pos)
        broker = Broker(ex, "BTC/USDT:USDT", dry_run)
        broker.setup(1, "isolated")
        app = create_app(broker, SECRET, False, D("0.05")).test_client()
        return ex, app

    def post(self, app, body):
        return app.post("/webhook", data=json.dumps(body), content_type="text/plain")

    def test_wrong_secret(self):
        ex, app = self.make()
        r = self.post(app, {"secret": "bad", "market_position": "long", "position_size": "0.01"})
        self.assertEqual(r.status_code, 401)
        self.assertEqual(ex.orders, [])

    def test_entry_then_duplicate_then_exit(self):
        ex, app = self.make()
        body = {"secret": SECRET, "market_position": "long", "position_size": "0.0123"}
        self.assertEqual(self.post(app, body).status_code, 200)
        self.assertEqual(ex.orders, [("buy", 12, {})])
        self.post(app, body)  # alerta duplicada: no hace nada
        self.assertEqual(len(ex.orders), 1)
        self.post(app, {"secret": SECRET, "market_position": "flat", "position_size": "0"})
        self.assertEqual(ex.orders[-1], ("sell", 12, {"reduceOnly": True}))
        self.assertEqual(ex.pos, 0)

    def test_entry_places_exchange_sl_tp(self):
        ex, app = self.make()
        r = self.post(app, {"secret": SECRET, "market_position": "short", "position_size": "0.01",
                            "sl": "100500", "tp": "99000"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(ex.pos, 0)  # cortos desactivados en make(): objetivo = plano
        ex2 = FakeExchange()
        broker = Broker(ex2, "BTC/USDT:USDT", False)
        broker.setup(1, "isolated")
        app2 = create_app(broker, SECRET, True, D("0.05")).test_client()
        self.post(app2, {"secret": SECRET, "market_position": "short", "position_size": "0.01",
                         "sl": "100500", "tp": "99000"})
        self.assertEqual(ex2.pos, D("-0.01"))
        kinds = [list(o[2].keys())[0] for o in ex2.orders[1:]]
        self.assertEqual(kinds, ["stopLossPrice", "takeProfitPrice"])
        self.assertTrue(all(o[0] == "buy" and o[2]["reduceOnly"] for o in ex2.orders[1:]))
        self.post(app2, {"secret": SECRET, "market_position": "flat", "position_size": "0", "sl": "", "tp": ""})
        self.assertEqual(ex2.pos, 0)
        self.assertFalse(any("stopLossPrice" in o[2] for o in ex2.orders))

    def test_wrong_side_sl_is_rejected(self):
        ex = FakeExchange()
        broker = Broker(ex, "BTC/USDT:USDT", False)
        broker.setup(1, "isolated")
        app = create_app(broker, SECRET, False, D("0.05")).test_client()
        r = self.post(app, {"secret": SECRET, "market_position": "long", "position_size": "0.01",
                            "sl": "101000", "tp": "102000"})
        self.assertIn("skipped", r.get_json()["protection"][0])
        self.assertEqual(ex.pos, D("0.01"))

    def test_distances_measured_from_real_entry(self):
        ex = FakeExchange()
        broker = Broker(ex, "BTC/USDT:USDT", False)
        broker.setup(5, "isolated")
        app = create_app(broker, SECRET, True, D("0.05")).test_client()
        r = self.post(app, {"secret": SECRET, "market_position": "long", "position_size": "0.01",
                            "sl_dist": "80", "tp_dist": "120"})
        prices = {p["type"]: p["price"] for p in r.get_json()["protection"]}
        self.assertEqual(prices, {"stopLossPrice": "99870.0", "takeProfitPrice": "100070.0"})

    def test_dry_run_sends_nothing(self):
        ex, app = self.make(dry_run=True)
        r = self.post(app, {"secret": SECRET, "market_position": "long", "position_size": "0.01"})
        self.assertEqual(r.get_json()["orders"][0]["skipped"], "DRY_RUN")
        self.assertEqual(ex.orders, [])


if __name__ == "__main__":
    unittest.main()
