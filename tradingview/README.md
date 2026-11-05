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

1. Abre un gráfico de **BTCUSDT** del exchange donde vayas a operar (por ejemplo `BINANCE:BTCUSDT`,
   `OKX:BTCUSDT` o `BITGET:BTCUSDT`). Usa el mismo par que vas a operar de verdad.
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

## 3. Conectarlo a un exchange (automatizarlo)

TradingView **no ejecuta estrategias por sí solo** en tu cuenta. El panel de trading de
TradingView sirve para operar a mano. Para automatizar, cada orden de la estrategia
dispara una **alerta con webhook** que recibe el bot de señales de tu exchange.

Requisitos: un plan de TradingView con webhooks (Essential o superior) y la verificación en dos pasos activada.

Opciones habituales:
- **Bots de señales del propio exchange** que aceptan webhooks de TradingView (OKX Signal Bot, Bitget y otros).
- **Intermediarios** como 3Commas, WunderTrading o similares, conectados a tu exchange por API.

Pasos:

1. En tu exchange o intermediario, crea un bot de señales de TradingView para BTCUSDT spot. Te dará una
   **URL de webhook** y una **plantilla de mensaje** (JSON), normalmente con un token secreto.
2. En la configuración de la estrategia (sección *5) Mensajes de alerta*) pega esa plantilla en los
   campos de entrada y salida. Puedes usar variables de TradingView como `{{ticker}}`, `{{close}}`,
   `{{strategy.order.contracts}}` o `{{strategy.order.action}}`.
3. En el gráfico: **Alertas → Crear alerta**.
   - Condición: `BTC Trend Bot (Zynthor)` → *Solo ejecuciones de órdenes* (*Order fills only*).
   - Mensaje: escribe exactamente `{{strategy.order.alert_message}}`
   - Notificaciones: activa **Webhook URL** y pega la URL del exchange.
   - Caducidad: *abierta* (sin fecha de fin).
4. Prueba primero con **cuenta demo o un importe muy pequeño** y comprueba que cada señal llega bien.

Importante:
- Si cambias cualquier parámetro de la estrategia, **borra y vuelve a crear la alerta**. La alerta guarda la configuración del momento en que se creó.
- Usa la **misma temporalidad y el mismo par** en el gráfico que en el bot del exchange.
- La API key del exchange debe tener solo permiso de **trading**, nunca de retiro.
- Si quieres que el exchange gestione el tamaño (por ejemplo, un % fijo del saldo), configura eso en el bot y no envíes la cantidad en el mensaje.

## Advertencias

- Los resultados pasados no garantizan los futuros. Esto no es asesoría financiera.
- El filtro diario usa la vela diaria **ya cerrada**, así que el backtest no mira al futuro. Aun así, el resultado real
  tendrá algo más de deslizamiento que el backtest.
- En mercados laterales largos (por ejemplo, 2019 o mediados de 2024) los sistemas de tendencia acumulan pequeñas pérdidas. Es normal y es el precio de no perderse las tendencias grandes.
