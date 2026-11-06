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

Gráfico del usuario: Micro Nasdaq (MNQ), 15 min, estrategia **"Estrategia
VWAP diario + VWAP NY v2"**. El código completo está en
`tradingview/vwap_daily_ny_v2.pine` (leerlo para detalles). Panel inferior:
"Panel RSI de confirmación 14 14 75 25".

| Elemento | Color | Qué es |
|---|---|---|
| VWAP diario | Amarillo | `ta.vwap` reiniciado con el día de futuros (18:00 ET), con bandas ±1 desviación |
| VWAP NY | Azul | VWAP acumulado desde la vela de las 09:30 ET |
| Línea de tendencia | Verde / roja (relleno) | **Supertrend (3 × ATR 10)**: verde = alcista, roja = bajista |
| Cambio a alcista / bajista | Círculo verde / rojo | Giro del Supertrend |
| Banda +1 / Banda −1 | Rojo / verde tenue | Bandas ±1 desviación del VWAP diario |
| Media de tendencia | Naranja | EMA 20 (solo si "días de tendencia" está activo) |
| Stop / Take profit | Rojo / verde | Niveles de la operación abierta |

Reglas de la estrategia (resumen):
- **Quién manda**: precio sobre ambos VWAP = solo compras; bajo ambos = solo
  ventas; entre ambos = operar hacia el VWAP diario (imán).
- **Entrada**: vela que toca el VWAP NY (o el VWAP diario / banda ±1 con
  tendencia) y cierra a favor, con mecha de rechazo ≥ 30 % de la vela.
- **Stop**: detrás de la mecha + 0,3 × ATR; no entra si el riesgo > 60 pts.
- **Salida**: 1/3 en 1R, 1/3 en 2R, último tercio con trailing 1,5 × ATR;
  stop a la entrada al llegar a 1R.
- **Horario**: entradas 09:35–11:45 ET, pausas por datos (08:25–08:40,
  09:55–10:10, 13:55–14:15), cierre total 15:50.
- **Riesgo (prueba de fondeo)**: 2 contratos, pérdida máxima diaria 500 USD,
  máximo 4 operaciones al día.

Temporalidad: el usuario la probó en el Probador de estrategias de
TradingView y le resulta **rentable en 5 minutos** (MNQ). Cifras del
backtest aún no compartidas. Al analizar sus gráficos, priorizar 5 min
para entradas y 15 min / diario para contexto.

### Backtest del usuario (TradingView, exportado 5-nov-2026)

MNQZ2026, 5 min, 15-sep → 5-nov-2026 (32 días operados). Ajuste de
contratos al riesgo activado (252 USD/operación, stop máx. 150 pts),
parciales + trailing 1,75 × ATR, días de tendencia (EMA 20) activado.
- 101 "operaciones" de TradingView = **60 posiciones** (cada parcial cuenta
  como una): 43 ganadoras / 17 perdedoras.
- Beneficio neto +5.494 USD (+11 % de 50k), profit factor 2,75, caída
  máxima 536 USD intrabarra (1,07 %), comprar y mantener −11 %.
- 22 días positivos / 10 negativos; peor día −255 USD. Semanas: todas ≥ 0
  salvo una plana. Sin los 5 mejores días: +1.942 USD (sigue positiva).
- Límites de la muestra: solo ~7 semanas y 60 posiciones; sin Bar Magnifier
  (resultados de parciales/trailing pueden ser optimistas). Validar en demo.

## Niveles para pegar en el indicador (flujo de trabajo del usuario)

El usuario usa la estrategia "VWAP diario + VWAP NY v2" en **MNQZ2026**
(Micro Nasdaq, 2 USD/punto, tick 0,25) y **MGCZ2026** (Micro Oro, 10
USD/punto, tick 0,10). Cuando le doy un análisis o señales, él copia los
niveles en el campo **"Niveles del informe"** del indicador (filtro de
niveles, `useLv`), que bloquea entradas con un nivel contrario antes del TP1.

**Siempre que analice MNQ o MGC, terminar con una línea lista para pegar**,
una por instrumento, con este formato exacto:

```
precio|tipo|texto ; precio|tipo|texto ; ...
```

- `tipo`: **R** = resistencia, **S** = soporte, **I** = imán (objetivo que
  atrae al precio; bloquea en ambos sentidos).
- `precio`: número con punto decimal, sin separador de miles
  (p. ej. `27518.75`, no `27.518,75`).
- `texto`: etiqueta corta sin `|` ni `;` (p. ej. `Fibo 0.5`, `PDH`, `FVG 15m`).

Ejemplo MNQ: `27518.75|R|Fibo 0.5 diario ; 27150|R|Neckline 15m ; 26600|S|Doble suelo ; 26817|I|VWAP diario`

Recordar al usuario que active "Filtro de niveles" para que se usen, y que
los niveles son del día: actualizarlos cada sesión.

Nota MGC: los parámetros por defecto están pensados para MNQ (riesgo máx.
60 pts = 120 USD/contrato en MNQ, pero 60 pts en oro = 600 USD/contrato) y
los textos de alerta dicen "MNQ". Revisar riesgo máximo en puntos y USD al
usarlo en MGC.
