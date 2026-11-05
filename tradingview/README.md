# BTC Trend Bot para TradingView

Archivo: `btc_trend_bot.pine` (Pine Script v6, tipo `strategy`).

## Qué hace

Es una estrategia de **seguimiento de tendencia**, el enfoque que más se usa
en BTC porque el precio pasa meses en tendencias fuertes y luego cae mucho
(-75 % en 2018 y en 2022). La idea es entrar en tendencias alcistas, quedarse
fuera en mercados bajistas y cortar las pérdidas pronto.

| Pieza | Por defecto | Para qué sirve |
|---|---|---|
| Filtro de régimen | Precio > EMA 200 **diaria** (vela cerrada, sin repintado) | No compra en mercado bajista |
| Señal de entrada | Supertrend (10, 3.0) cambia a alcista | Entrada en tendencia |
| Alternativas | Cruce EMA 21/55 · Ruptura Donchian 20/10 | Para comparar en el Strategy Tester |
| Filtro ADX | Apagado (opcional, ADX ≥ 20) | Evita mercados laterales |
| Stop inicial | 2.5 × ATR(14) | Limita la pérdida por operación |
| Trailing stop | 3.5 × ATR, solo sube | Deja correr las ganancias |
| Take profit | Apagado | En tendencia es mejor no cortar ganancias |
| Tamaño | 2 % de riesgo por operación, máximo 100 % del capital | Spot sin apalancamiento |
| Costes del backtest | Comisión 0.1 % + 2 ticks de deslizamiento | Resultados más realistas |
| Dirección | Solo largos | Spot no permite cortos; actívalos solo con futuros |

## 1. Cargarlo en TradingView

1. Abre un gráfico de **BTCUSDT** del exchange donde vayas a operar (con BYDFi: `BYDFI:BTCUSDT.P`; en otros exchanges, por ejemplo `BINANCE:BTCUSDT`).
   Usa el mismo par que vas a operar de verdad.
2. Temporalidad recomendada: **4 h** (también puedes probar 1 D).
3. Abre el **Editor de Pine**, pega el contenido de `btc_trend_bot.pine`, haz clic en **Guardar** y luego en **Añadir al gráfico**.
4. Abre el **Probador de estrategias** y revisa: beneficio neto, drawdown máximo,
   factor de beneficio, número de operaciones y la comparación con *comprar y mantener*.

## 2. Elegir la mejor configuración (hazlo tú en el Probador)

Prueba cada combinación en 4 h y en 1 D y anota los resultados:

1. `Tipo de señal` = Supertrend / Cruce EMAs / Ruptura Donchian.
2. Filtro ADX encendido o apagado.
3. Trailing stop 3.0 / 3.5 / 4.5 × ATR.

Cómo elegir sin engañarte:

- Prioriza el **drawdown máximo** y el **factor de beneficio** (> 1.5) por encima del beneficio total.
- Exige **al menos 30 operaciones**. Con menos, el resultado puede ser suerte.
- Si una configuración solo funciona con un valor exacto (por ejemplo, funciona con 3.5 y falla con 3.0 y 4.0), está **sobreajustada**: descártala.
- Haz una validación fuera de muestra: optimiza con `Desde/Hasta` = 2018–2023 y comprueba sin tocar nada el periodo 2024–hoy.

## 3. Conectarlo a BYDFi (automatizarlo)

TradingView **no ejecuta la estrategia por sí solo** en tu cuenta. Cada orden de la estrategia
dispara una **alerta con webhook**, y alguien tiene que recibirla y enviar la orden al exchange.

BYDFi no tiene un bot de señales que reciba los webhooks de TradingView (a diferencia de OKX o Bybit).
Por eso se incluye un **servidor puente** propio en `relay/`. Recibe la alerta y opera en BYDFi por API.

```
TradingView (estrategia) ──webhook──▶ relay/bydfi_relay.py (tu servidor) ──API──▶ BYDFi
```

### Puntos importantes de BYDFi

- La API de BYDFi (y la librería CCXT que usa el relay) trabaja con **futuros perpetuos** USDT-M, no con spot.
  El relay opera `BTC/USDT:USDT` con **apalancamiento 1x, margen aislado y solo largos**, lo que se parece
  mucho a tener BTC en spot. La diferencia es que se paga o se cobra **funding** cada pocas horas.
- Usa el gráfico de BYDFi en TradingView: **`BYDFI:BTCUSDT.P`**, en 4 h. Así las señales salen con los mismos precios con los que vas a operar.
- En **Propiedades** de la estrategia, pon el **capital inicial** igual al dinero que vas a dedicar al bot.
  El relay copia la cantidad de BTC que calcula la estrategia, limitada por `MAX_POSITION_BTC`.

### Cómo funciona el relay

Cada alerta envía la posición que la estrategia **debe tener** después de la orden
(`{{strategy.market_position}}` y `{{strategy.market_position_size}}`). El relay la compara con tu
posición real en BYDFi y envía solo la diferencia como orden de mercado (las salidas van con `reduceOnly`).
Si una alerta llega dos veces, no pasa nada. Si se pierde una, la siguiente vuelve a sincronizar la cuenta.

Protecciones:
- Comprueba un secreto (`WEBHOOK_SECRET`) en cada alerta.
- Aplica un tope de tamaño (`MAX_POSITION_BTC`).
- Bloquea los cortos salvo que actives `ALLOW_SHORT`.
- Arranca en `DRY_RUN=true`, que solo registra lo que haría y no envía órdenes.
- Guarda un registro en `relay.log`.

### Pasos

1. **API key en BYDFi:** Perfil → Gestión de API → crear clave con permiso de **trading de perpetuos**.
   Nunca actives el permiso de **transferencia ni de retiro**. Vincúlala a la IP de tu servidor.
2. **Servidor:** un VPS pequeño con IP fija (TradingView solo envía webhooks a los puertos 80/443 y por HTTPS).
   ```bash
   cd tradingview/relay
   python3 -m venv venv && ./venv/bin/pip install -r requirements.txt
   cp .env.example .env    # rellena las claves y un WEBHOOK_SECRET largo
   set -a && . ./.env && set +a
   ./venv/bin/python -m unittest test_bydfi_relay   # tests locales
   ./venv/bin/python bydfi_relay.py                 # escucha en el puerto 8080
   ```
   Pon delante un proxy con HTTPS, por ejemplo Caddy con `tudominio.com { reverse_proxy localhost:8080 }`,
   y déjalo funcionando como servicio (systemd) para que se reinicie solo.
   Comprueba que responde en `https://tudominio.com/health`.
3. **Estrategia:** en *5) Mensajes de alerta*, cambia `CAMBIA_ESTE_SECRETO` por tu `WEBHOOK_SECRET` en los 4 campos.
4. **Alerta:** Alertas → Crear alerta.
   - Condición: `BTC Trend Bot (Zynthor)` → *Solo ejecuciones de órdenes* (*Order fills only*).
   - Mensaje: exactamente `{{strategy.order.alert_message}}`
   - Notificaciones: **Webhook URL** = `https://tudominio.com/webhook`
   - Caducidad: abierta.
   Necesitas un plan de TradingView con webhooks (Essential o superior) y la verificación en dos pasos activada.
5. **Prueba en seco:** deja `DRY_RUN=true` unos días y comprueba en `relay.log` que cada señal llega con el tamaño correcto.
6. **En real:** pon `DRY_RUN=false` con un `MAX_POSITION_BTC` pequeño y sube el tope poco a poco.

Si cambias cualquier parámetro de la estrategia, **borra y vuelve a crear la alerta**. La alerta guarda la configuración del momento en que se creó.

## 4. Scalping en futuros (5 min / 1 min): `btc_scalper.pine`

Es una estrategia aparte, pensada para hacer **muchas operaciones** en `BYDFI:BTCUSDT.P` y aprovechar el reembolso de comisiones.

| Pieza | Por defecto |
|---|---|
| Tendencia | Precio sobre/bajo la EMA 200 de **15 min** (pendiente de la EMA 21 opcional) |
| Entrada | **Todas**: cualquiera de estas señales vale: RSI(7) cruza 40/60, toque a la EMA 21 o cruce EMA 9/21 |
| Salidas | TP 1.5 × ATR, SL 1.0 × ATR **medidos desde el precio real de entrada**, cierre a las 12 velas |
| TP mínimo | 0.10 %: si el mercado está tranquilo se amplían TP y SL en vez de no operar |
| Diagnóstico | Tabla en el gráfico: señales, qué filtro las bloquea y entradas por día |
| Riesgo | 0.5 % del capital por operación, máximo 5x de exposición |
| Protecciones | Para el día al perder un 3 %, máximo 30 operaciones al día |
| Comisión del backtest | 0.018 % por lado (0.06 % taker × 30 % que pagas tras el reembolso del 70 %) |

### Las cuentas de las comisiones (lo más importante)

Las cifras suponen una comisión taker del 0.06 %. Confirma tu comisión real en BYDFi y pon la neta en
**Propiedades → Comisión**.

| | Sin reembolso | Con 70 % de reembolso |
|---|---|---|
| Coste de ida y vuelta | 0.12 % | **0.036 %** |
| Ganancia neta si llega al TP (ATR = 0.08 % → TP 0.12 %) | 0.00 % | 0.084 % |
| Pérdida neta si salta el SL (0.08 %) | 0.20 % | 0.116 % |
| % de aciertos necesario para no perder | imposible | **~58 %** |

Sin el reembolso, este scalping no puede ganar. Con el reembolso es posible, pero necesitas acertar
más de la mitad de las veces, y antes de eso hay que comprobarlo en el Probador.

### Cómo probarlo

1. Gráfico `BYDFI:BTCUSDT.P` en **5 min** (si usas 15 min, pon el marco de tendencia en 60). En 1 min hay más ruido y el retraso del webhook (1 a 5 s) pesa más; empieza por 5 min.
2. En Propiedades: capital inicial = tu capital real, comisión = tu comisión neta, deslizamiento ≥ 1 tick.
3. Con menos de ~200 operaciones el resultado no dice nada. Mira el **% de aciertos**, el **factor de beneficio** (> 1.2 en scalping ya es bueno), el drawdown y que haya cientos de operaciones.
4. Prueba las dos entradas y TP/SL de 1.0–2.0 × ATR. Si solo gana con un valor exacto, está sobreajustado.

### Relay para scalping

- En `.env`: `ALLOW_SHORT=true`, `LEVERAGE=5` (igual o mayor que el apalancamiento máximo de la estrategia) y `MARGIN_MODE=isolated`.
- La entrada envía el SL y el TP, y el relay los deja **puestos en BYDFi** como órdenes `reduceOnly`.
  Así la posición sigue protegida aunque TradingView, el webhook o tu servidor fallen. Cuando la posición
  se cierra, el relay cancela las órdenes que queden abiertas.
- Pon el servidor cerca de BYDFi (VPS en Asia o Europa) para reducir el retraso.

### Antes de ir en real

- **El 70 % de comisión:** si es una comisión de **afiliado** (referidos), revisa los términos de BYDFi.
  Muchos exchanges prohíben cobrar comisiones de afiliado por operaciones de tu propia cuenta y pueden retirarlas o bloquear la cuenta.
- Hay **liquidación** con apalancamiento y el backtest de TradingView no la simula. Mantén el apalancamiento bajo y el margen aislado.
- Empieza con `DRY_RUN=true`, luego con el mínimo, y compara cada día el resultado real con el del Probador.

## 5. Scalper de HYPE: `hype_scalper.pine`

Usa la misma lógica que el scalper de BTC, con ajustes para un activo mucho más volátil. Gráfico: **`BYDFI:HYPEUSDT.P`** en 5 min.

| Ajuste | BTC | HYPE | Motivo |
|---|---|---|---|
| TP mínimo | 0.10 % | **0.25 %** | HYPE se mueve más: objetivos más amplios y la comisión pesa menos |
| Apalancamiento máximo | 5x | **3x** | Las mechas violentas pueden liquidar con apalancamiento alto |
| Riesgo por operación | 0.5 % | **0.4 %** | Más deslizamiento real que en BTC |
| Deslizamiento del backtest | 1 tick | **3 ticks** | Menos liquidez que BTC |
| Máx. operaciones/día | 30 | 20 | Evita sobreoperar en días de mucho ruido |
| Decimales de la cantidad | 3 | 1 | Compruébalo con el mínimo del contrato en BYDFi |

Relay para HYPE (`.env`): `SYMBOL=HYPE/USDT:USDT`, `LEVERAGE=3`, `ALLOW_SHORT=true`, y `MAX_POSITION_BTC`
pasa a ser el tope **en HYPE** (por ejemplo `20`). Si el relay no arranca con ese símbolo, BYDFi lo nombra
de otra forma: el error del arranque lo dirá.

Cuidado con HYPE:
- Puede tener un **funding** alto en días de euforia. Revísalo en BYDFi si mantienes posiciones muchas horas.
- Es una moneda con noticias propias (desbloqueos de tokens, Hyperliquid) que pueden moverla un 10–20 % en minutos. El SL puesto en el exchange es imprescindible.
- Con pocos meses de histórico en BYDFi, valida con **cientos de operaciones** y mira si gana tanto en largos como en cortos.

## 6. Sistema VWAP + soportes y resistencias: `vwap_sr_bot.pine`

Sirve para HYPE, BTC o SOL en BYDFi, en 5 o 15 min. Usa el mismo relay que los scalpers.

**Cómo decide:**
1. **Sesgo con el VWAP** (anclado a la sesión de Nueva York por defecto; también diario o semanal):
   - Precio sobre el VWAP y VWAP subiendo → **mandan los compradores**: solo compras.
   - Precio bajo el VWAP y VWAP bajando → **mandan los vendedores**: solo ventas.
   - En cualquier otro caso → neutral, no opera.
2. **Soportes y resistencias:** pivotes confirmados (no repintan), que se unen si están muy cerca;
   máximo y mínimo del día anterior; el VWAP y sus bandas. Se dibujan en el gráfico (verde = soporte, rojo = resistencia).
3. **Entradas:** rechazo en el VWAP, rebote en soporte o resistencia, y ruptura de nivel (esta última apagada por defecto).
4. **Objetivo = el siguiente nivel** (con un máximo de 3 × ATR). Si ese nivel está tan cerca que no compensa el
   riesgo (relación < 1.2) o no cubre la comisión (objetivo < 0.15 %), **no entra**.
5. **Stop** detrás del nivel tocado + 0.3 × ATR. Cierre a las 24 velas si no ha tocado ni stop ni objetivo.
6. Riesgo 0.5 % por operación, máximo 3x, pérdida diaria máxima 3 %, máximo 15 operaciones al día.

El panel de arriba a la derecha muestra el sesgo actual y cuántas señales bloqueó cada filtro
(contra el sesgo, nivel muy cerca, ya en posición, límite diario). Si hay pocas entradas, la tabla dice por qué.

Ajustes que más cambian el número de entradas:
- `Operar solo a favor del sesgo del VWAP`: apagado → muchas más entradas, pero también contra la tendencia.
- `Relación beneficio/riesgo mínima`: 1.0 en lugar de 1.2 → menos bloqueos por "nivel muy cerca".
- `Pivote: velas a la izquierda/derecha`: valores más pequeños (5/3) → más niveles y más rebotes.

## Advertencias

- Los resultados pasados no garantizan los futuros. Esto no es asesoría financiera.
- El filtro diario usa la vela diaria **ya cerrada**, así que el backtest no mira al futuro. Aun así, el resultado real
  tendrá algo más de deslizamiento que el backtest.
- En mercados laterales largos (por ejemplo, 2019 o mediados de 2024) los sistemas de tendencia acumulan pequeñas pérdidas. Es normal y es el precio de no perderse las tendencias grandes.
