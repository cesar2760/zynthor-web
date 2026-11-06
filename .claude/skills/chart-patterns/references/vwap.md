# VWAP: guía completa

El usuario opera con VWAP (también tiene en el repo la estrategia
`tradingview/vwap_sr_bot.pine` y `crypto_vwap_levels_bot.pine`). Usar esta
guía al analizar gráficos intradía.

## 1. Qué es

- **VWAP = Volume Weighted Average Price**: precio medio negociado del día,
  ponderado por volumen.
- Se **reinicia al inicio de cada sesión** (en futuros del Nasdaq, a las
  18:00 ET; en cripto, a las 00:00 UTC salvo que se configure otra cosa).
- Muy usado por traders profesionales e instituciones como referencia de
  "precio justo" del día. Ideal para **intradía**, no para inversión a
  largo plazo.

## 2. Cómo leerlo

- **Precio por encima del VWAP** → sesgo **alcista** (los compradores
  dominan el día).
- **Precio por debajo del VWAP** → sesgo **bajista**.
- El VWAP actúa como **soporte/resistencia dinámico**.
- Las instituciones lo usan como benchmark: compran por debajo y venden por
  encima del VWAP para ejecutar "bien".

## 3. Fórmula

```
VWAP = Σ (Precio típico × Volumen) / Σ Volumen
Precio típico = (Máximo + Mínimo + Cierre) / 3
```

Acumulado desde el inicio de la sesión. El volumen pesa más que el precio
solo. Las plataformas lo calculan automáticamente.

## 4. Soporte y resistencia

- En **tendencia alcista**, el VWAP suele actuar como **soporte**.
- En **tendencia bajista**, suele actuar como **resistencia**.
- La reacción del precio en el VWAP da oportunidades de entrada, pero
  **siempre esperar confirmación** (vela de rechazo).

## 5. Estrategia de pullback (compra)

1. Tendencia alcista clara (precio por encima del VWAP, máximos crecientes).
2. El precio retrocede hasta el VWAP.
3. Vela alcista de confirmación en el VWAP (martillo, envolvente alcista,
   pin bar con mecha inferior).
4. **Entrada** tras la confirmación.
5. **Stop loss** debajo del último mínimo (swing low).
6. **Objetivo**: el máximo anterior o continuación de tendencia.

## 6. Estrategia de breakdown (venta)

1. Tendencia bajista clara (precio por debajo del VWAP).
2. El precio vuelve a testear el VWAP desde abajo.
3. Vela bajista de rechazo (shooting star, envolvente bajista, pin bar con
   mecha superior).
4. **Venta** tras la confirmación.
5. **Stop loss** encima del último máximo (swing high).
6. **Objetivo**: el soporte reciente / último mínimo.

## 7. Cruces del VWAP

- Precio cruza **por encima** del VWAP → señal alcista.
- Precio cruza **por debajo** → señal bajista.
- **No operar cada cruce**: en rango el precio cruza el VWAP muchas veces
  (señales falsas). Confirmar con tendencia y volumen.

## 8. Mejores combinaciones

VWAP + volumen · VWAP + RSI · VWAP + MACD · VWAP + EMA · VWAP + price
action · VWAP + soportes y resistencias (PDH/PDL, order blocks, FVG).

## 9. Errores comunes

- Usar el VWAP para inversión a largo plazo.
- Ignorar la tendencia general.
- Operar cada cruce.
- Ignorar el volumen.
- Entrar sin confirmación.
- Mala gestión del riesgo.

## 10. Resumen

Mejor para intradía · las instituciones lo usan · soporte/resistencia
dinámico · combinarlo con otros indicadores · esperar confirmación ·
gestión del riesgo siempre.

## Aplicación al analizar un gráfico

- Decir si el precio está **sobre o bajo el VWAP** y si lo respeta como
  soporte/resistencia o lo cruza una y otra vez (rango → no operar cruces).
- Buscar el setup de **pullback** (tendencia alcista) o de **breakdown**
  (tendencia bajista) con vela de confirmación.
- Combinar con la liquidez y las zonas de `smc-terms.md` y con los
  patrones de `SKILL.md`: una entrada en el VWAP que coincide con un FVG,
  OB o PDH/PDL es de más calidad.
- El VWAP es menos fiable al principio de la sesión (poco volumen
  acumulado) y gana peso a medida que avanza el día.

## Configuración del usuario (TradingView)

- En el gráfico del usuario (estrategia "Estrateg... 2 2 1 0 0,3 60 260 150
  500 4 Parcial", Micro Nasdaq MNQ), la **línea azul es el VWAP** (confirmado
  por el usuario). El resto de líneas (roja, naranja, amarilla, verdes) aún
  no están identificadas: preguntar si hace falta.
