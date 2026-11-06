# Niveles de opciones (gamma) en los niveles del usuario

El usuario añade a sus niveles datos de opciones de QQQ/NDX (→ NQ) y GLD
(→ GC). **No tratarlos como soportes/resistencias técnicos normales**:
cada tipo cambia cómo se mueve el precio. Leerlos así:

| Nivel | Qué significa | Cómo operarlo |
|---|---|---|
| **Gamma flip** | Frontera del régimen de los dealers | **Encima = gamma positiva**: los dealers compran caídas y venden subidas → rango, reversión a la media, movimientos frenados. **Debajo = gamma negativa**: los dealers venden caídas y compran subidas → movimientos rápidos, tendencia, rupturas que corren. |
| **Muro de calls** | Strike con más gamma de calls | Techo del día en gamma positiva. Vender rechazos ahí; no comprar debajo de él esperando que lo rompa. |
| **Muro de puts** | Strike con más gamma de puts | Suelo del día. Comprar rechazos; si se rompe en gamma negativa, la caída acelera. |
| **Imán / max pain / pin** | Nivel que atrae al precio (sobre todo cerca del cierre y vencimientos) | **Objetivo**, no zona para operar en contra. No vender en un imán por estar arriba ni comprar por estar abajo: el precio tiende a ir hacia él. |
| **Acelerador** | Strike donde, al cruzarlo, la cobertura de los dealers acelera el movimiento | Ruptura = movimiento rápido hasta el siguiente nivel; no operar reversión ahí. |
| **Vanna peligro** | Zona donde la cobertura por cambios de volatilidad puede acelerar | Debajo (soporte) o encima (resistencia), riesgo de aceleración; stops fuera de ella. |
| **DEX** (delta exposure, ±millones) | Exposición delta de los dealers en ese strike | Cifra grande = nivel fuerte donde el precio suele reaccionar; actúa como objetivo en el sentido del movimiento. |

## Reglas para armar las entradas

1. **Primero el régimen**: ¿el precio está encima o debajo del gamma flip?
   - Encima (gamma positiva): comprar retrocesos hacia imanes y VWAP,
     vender solo en el muro de calls; TP1 cercano (los movimientos se
     frenan).
   - Debajo (gamma negativa): operar a favor de la ruptura (ventas en
     retesteo del flip o del acelerador), objetivos en los niveles DEX y en
     el muro de puts; dejar correr el trailing.
2. Los **imanes son TPs**, nunca entradas en contra.
3. Los **stops van fuera de los muros y del gamma flip** (con un margen),
   no justo en el nivel.
4. Mantener el riesgo dentro de los límites de la estrategia
   (`vwap.md`).

Pendiente de confirmar con el usuario: qué significa "QW" (¿fuente de los
datos o vencimiento semanal?) y el criterio exacto de "acelerador" y
"vanna peligro" en sus informes.
