---
name: chart-patterns
description: Guía de patrones chartistas y de velas (chart patterns + candlestick patterns) para analizar un gráfico y plantear una operación. Cubre patrones alcistas (doble suelo, HCH invertido, triángulo ascendente, bull flag, taza con asa, cuña descendente), bajistas (doble techo, HCH, triángulo descendente, bear flag, cuña ascendente, taza con asa invertida), de continuación (triángulo simétrico, rectángulo, banderín, canal), de reversión (suelo/techo redondeado, triple suelo/techo) y velas (envolvente, martillo, doji, estrella de la mañana/tarde, shooting star, hanging man), con zona de entrada, stop loss y objetivo para cada uno. Usar cuando el usuario diga "analiza este gráfico", "qué patrón ves", "usa los patrones", "dónde entro", "zonas de entrada", "chart patterns", "patrones de velas", o pida mejorar un trade o una estrategia de trading.
---

# Patrones chartistas y de velas

Referencia para identificar el patrón en un gráfico y convertirlo en un plan:
**entrada, stop loss, objetivo**. Aplica a cualquier mercado y temporalidad
(cripto, futuros, acciones). Esto es una herramienta de análisis, no una
recomendación de inversión.

## Cómo usarlo (4 pasos)

1. **Tendencia**: identificar la tendencia previa (alcista / bajista / rango).
   Un patrón de continuación necesita una tendencia que continuar; uno de
   reversión necesita una tendencia que revertir.
2. **Patrón**: localizar el patrón y marcar su línea clave (neckline,
   resistencia, soporte o línea de tendencia).
3. **Confirmación de ruptura**: esperar el **cierre de vela** más allá de la
   línea clave, idealmente con aumento de volumen. Sin cierre no hay patrón.
4. **Plan**: entrada, stop y objetivo con las reglas de abajo, y tamaño de
   posición según el riesgo (p. ej. 1 % de la cuenta por operación).

### Reglas generales de entrada / stop / objetivo

- **Entrada**: en el cierre que rompe la línea clave, o en el *pullback*
  (retesteo) de esa línea, que da mejor precio y stop más corto.
- **Stop loss**: al otro lado de la estructura — debajo del último mínimo
  del patrón en largos, encima del último máximo en cortos.
- **Objetivo (movimiento medido)**: altura del patrón proyectada desde el
  punto de ruptura. En banderas, la longitud del mástil.
- **Filtro**: descartar si la relación beneficio/riesgo es menor de 1,5–2.

## Patrones alcistas (precio sube) → COMPRA

| Patrón | Forma | Línea clave / entrada | Stop | Objetivo |
|---|---|---|---|---|
| **Doble suelo** (W) | Dos mínimos a nivel similar tras caída | Ruptura al alza del neckline (máximo entre los suelos) | Debajo de los suelos | Altura suelo→neckline sobre el neckline |
| **Hombro-cabeza-hombro invertido** | Mínimo, mínimo más bajo (cabeza), mínimo más alto | Ruptura del neckline (une los máximos) | Debajo del hombro derecho | Distancia cabeza→neckline |
| **Triángulo ascendente** | Resistencia horizontal + mínimos crecientes | Cierre sobre la resistencia | Debajo del último mínimo creciente | Altura de la base del triángulo |
| **Bull flag** | Subida fuerte (mástil) + canal corto bajista | Ruptura del techo de la bandera | Debajo de la bandera | Longitud del mástil |
| **Taza con asa** | Suelo redondeado (U) + pequeño retroceso (asa) | Ruptura del máximo del asa / borde de la taza | Debajo del asa | Profundidad de la taza |
| **Cuña descendente** | Dos líneas bajistas que convergen | Ruptura de la línea superior | Debajo del último mínimo | Altura de la parte ancha de la cuña |

## Patrones bajistas (precio baja) → VENTA

| Patrón | Forma | Línea clave / entrada | Stop | Objetivo |
|---|---|---|---|---|
| **Doble techo** (M) | Dos máximos a nivel similar tras subida | Ruptura a la baja del neckline | Encima de los techos | Altura techo→neckline bajo el neckline |
| **Hombro-cabeza-hombro** | Máximo, máximo más alto (cabeza), máximo más bajo | Ruptura del neckline | Encima del hombro derecho | Distancia cabeza→neckline |
| **Triángulo descendente** | Soporte horizontal + máximos decrecientes | Cierre bajo el soporte | Encima del último máximo decreciente | Altura de la base |
| **Bear flag** | Caída fuerte (mástil) + canal corto alcista | Ruptura del suelo de la bandera | Encima de la bandera | Longitud del mástil |
| **Cuña ascendente** | Dos líneas alcistas que convergen | Ruptura de la línea inferior | Encima del último máximo | Altura de la parte ancha |
| **Taza con asa invertida** | Techo redondeado (∩) + pequeño rebote (asa) | Ruptura del mínimo del asa | Encima del asa | Profundidad de la taza |

## Patrones de continuación (siguen la tendencia previa)

Se opera la ruptura **en la dirección de la tendencia previa**; una ruptura
en contra se trata con más cautela.

- **Triángulo simétrico**: máximos decrecientes y mínimos crecientes.
  Ruptura en cualquier sentido; objetivo = altura de la base.
- **Rectángulo**: rango entre soporte y resistencia horizontales.
  Objetivo = altura del rango desde la ruptura.
- **Banderín (pennant)**: mini-triángulo simétrico tras un mástil.
  Objetivo = longitud del mástil.
- **Bull flag / Bear flag**: ver tablas de arriba.
- **Canal**: precio entre dos paralelas. Dentro: comprar en la parte baja y
  vender en la alta a favor de la pendiente. Ruptura del canal = posible
  aceleración o cambio de tendencia.

## Patrones de reversión (cambio de tendencia)

- **Suelo redondeado** (rounding bottom): giro lento en U → compra al romper
  el borde. **Techo redondeado**: giro en ∩ → venta al perder la base.
- **Triple suelo**: tres mínimos al mismo nivel → compra al romper la
  resistencia. **Triple techo**: tres máximos → venta al perder el soporte.
- También: doble suelo/techo y HCH (tablas de arriba).

## Patrones de velas

Las velas sirven como **gatillo o confirmación** en una zona relevante
(soporte, resistencia, neckline, VWAP), no como señal aislada.

| Vela | Sesgo | Cómo es | Dónde importa |
|---|---|---|---|
| **Envolvente alcista** | Alcista ↑ | Vela verde cuyo cuerpo cubre entero el cuerpo rojo anterior | Tras caída / en soporte |
| **Martillo** (hammer) | Alcista ↑ | Cuerpo pequeño arriba, mecha inferior ≥ 2× el cuerpo | Al final de una caída |
| **Estrella de la mañana** | Alcista ↑ | Roja grande, vela pequeña (indecisión), verde que cierra en la mitad de la roja o más | Suelo de una caída |
| **Doji** | Neutral — | Apertura ≈ cierre; indecisión | Avisa de posible giro; esperar la siguiente vela |
| **Envolvente bajista** | Bajista ↓ | Vela roja cuyo cuerpo cubre entero el cuerpo verde anterior | Tras subida / en resistencia |
| **Shooting star** | Bajista ↓ | Cuerpo pequeño abajo, mecha superior larga | Al final de una subida |
| **Estrella de la tarde** | Bajista ↓ | Verde grande, vela pequeña, roja que cierra en la mitad de la verde o más | Techo de una subida |
| **Hanging man** | Bajista ↓ | Forma de martillo pero tras una subida | Techo; necesita confirmación bajista |

Stop típico con vela gatillo: al otro extremo de la vela (o de la
formación de 3 velas en las estrellas).

## Gestión del riesgo y consejos

- Practicar primero en temporalidades pequeñas o en cuenta demo/paper.
- Confirmar con indicadores: **RSI** (divergencias, sobrecompra/sobreventa),
  **medias móviles** (dirección de tendencia), **volumen** en la ruptura.
- Siempre stop loss antes de entrar; arriesgar un % fijo pequeño por trade.
- Paciencia: esperar el cierre de confirmación; no sobreoperar.
- Las rupturas falsas son frecuentes, sobre todo sin volumen o en contra de
  la tendencia mayor. Ningún patrón garantiza el resultado.

## Al analizar un gráfico para el usuario

Responder con este formato:

1. **Tendencia** previa y temporalidad.
2. **Patrón** identificado (o candidatos) y su línea clave con precio.
3. **Estado**: formándose / ruptura confirmada / ruptura fallida.
4. **Plan**: entrada, stop, objetivo y relación beneficio/riesgo.
5. **Qué invalidaría** el escenario.

Leer también `references/smc-terms.md` (glosario Smart Money / ICT: FVG,
OB, BOS, CHoCH, liquidez, killzones, PO3/AMD y modelo de entrada) y
`references/supply-demand-confirmations.md` (velas de confirmación en zonas
de oferta y demanda), y añadir esa lectura cuando aplique: liquidez cercana
(PDH/PDL, EQH/EQL), barridos, FVG y order blocks donde entrar, y si el
momento cae en una killzone.

Si hay datos de velas disponibles (p. ej. la estrategia VWAP + niveles de
este repo o una herramienta de backtest), combinar el patrón con esos
niveles en vez de analizarlo aislado.
