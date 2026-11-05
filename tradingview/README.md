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

## Advertencias

- Los resultados pasados no garantizan los futuros. Esto no es asesoría financiera.
- El filtro diario usa la vela diaria **ya cerrada**, así que el backtest no mira al futuro. Aun así, el resultado real
  tendrá algo más de deslizamiento que el backtest.
- En mercados laterales largos (por ejemplo, 2019 o mediados de 2024) los sistemas de tendencia acumulan pequeñas pérdidas. Es normal y es el precio de no perderse las tendencias grandes.
