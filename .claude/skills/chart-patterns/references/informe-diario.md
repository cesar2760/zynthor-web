# Informe diario "Informe NQ y Oro" (formato que espera el usuario)

El usuario recibe por email (a sí mismo, asunto "Informe NQ y Oro – <día>
dd/mm") un informe antes de la apertura de NY, con datos de opciones de
**QuantWheel ("QW")** para QQQ/NDX → NQ y GLD → GC. El usuario está en
Argentina (ET + 2 h). Cuando pida "el informe", "las señales" o "los
niveles", entregarlo **exactamente con esta estructura**:

```
<Titular de una línea: qué mueve al NQ y al oro hoy y el sesgo>
Datos de las HH:MM ET (HH:MM Argentina).

PARA PEGAR EN TRADINGVIEW
Oro · MGCZ2026:
precio|tipo|texto;precio|tipo|texto;...   (de mayor a menor)
Nasdaq · MNQZ2026:
precio|tipo|texto;...
Entradas (solo calificación A):
MGCZ2026 | VENTA n | entrada X | stop X | TP1 X | TP2 X
Nasdaq: sin entradas A hoy        (si no hay)
Opcionales (B, medio tamaño):
MNQZ2026 | VENTA n | entrada X | stop X | TP1 X | TP2 X
...

ESTADÍSTICA REAL: N registradas, N resueltas (G ganadoras / P perdedoras),
N sin activar, N pendientes. Resumen de cómo salieron las de ayer.

FILTRO DEL DÍA: NQ sobre/bajo el VWAP (precio): solo compras/ventas.
Oro: ídem.

NOTICIAS: drivers del día + datos macro con hora ET y la pausa
correspondiente (p. ej. 8:30 ET → no operar 8:25-8:40).

Planes condicionales para análisis propio, no son recomendación de
inversión. Confirmá precios en tu plataforma antes de operar.
```

## Cómo se construyen los niveles
Mezclar en una sola lista por instrumento (texto corto, sin tildes
problemáticas no es requisito, pero sin `|` ni `;`):
- **Precio**: máximo/mínimo de ayer, Asia, Londres, NY y semana pasada;
  máximos sin barrer; VWAP de sesión, VWAP anclado, bandas ±1/±2; POC.
- **Opciones (QuantWheel)**: muro de calls, muro de puts, gamma flip, max
  pain, imanes por strike (GLD 375, QQQ 690…), vanna, DEX. Ver
  `opciones-gamma.md` para cómo operarlos.
- Varios motivos en el mismo precio se juntan: "Maximo Asia y QQQ 693".

## Cómo se construyen las entradas
- **Filtro del día** manda: NQ bajo el VWAP → solo ventas (las compras, como
  mucho B). Entradas contra el VWAP → B, medio tamaño.
- **A**: a favor del filtro, en un nivel fuerte (muro, imán, nivel de
  precio + opciones coincidentes), TP1 ≥ 1,5R. **B**: el resto que valga la
  pena, medio tamaño.
- Numerar las entradas del día (VENTA 1, COMPRA 3…), stop detrás del
  nivel, TP1/TP2 en los siguientes niveles de la lista.
- Riesgo dentro de la estrategia (`vwap.md`): MNQ ≤ 60 pts.

## Estadística real
Llevar el registro de todas las entradas publicadas: activada o no,
ganadora/perdedora (TP1 = ganadora, stop antes de TP1 = perdedora).
Señalar cuando hay pocos datos.

## Datos que hacen falta (pedirlos si no están)
Desde esta sesión no hay datos de mercado en vivo ni acceso a QuantWheel.
Pedir al usuario: capturas de MNQ y MGC (5 min y 15 min / diario, con los
VWAP) y los niveles de QuantWheel (muros, gamma flip, max pain, imanes,
DEX/vanna) de QQQ y GLD, o el informe del día. Sin eso, no inventar
precios.
