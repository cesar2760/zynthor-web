# Glosario de trading: Smart Money / ICT

Términos que el usuario usa al operar. Usarlos al analizar gráficos y
explicar el significado si hace falta. Horas en hora de Nueva York (ET).

## Gestión de la operación

| Sigla | Término | Significado |
|---|---|---|
| **SL** | Stop Loss | Nivel fijado de antemano donde se sale para limitar la pérdida. |
| **TP** | Take Profit | Nivel fijado de antemano donde se cierra para asegurar beneficio. |
| **BE** | Break Even | Mover el stop al precio de entrada: la operación ya no puede perder. Normalmente tras alcanzar el TP1 o 1R. |
| **KZ** | Killzone | Ventanas horarias con más volumen y movimientos institucionales. Asia 20:00–00:00, Londres 02:00–05:00, Nueva York AM 07:00–10:00 (apertura de cash 09:30), Nueva York PM 13:30–16:00. Para el Nasdaq las mejores son Londres y NY AM. |

## Estructura de mercado

| Sigla | Término | Significado |
|---|---|---|
| **BOS** | Break of Structure | El precio supera el máximo (alcista) o mínimo (bajista) anterior **a favor** de la tendencia → continuación. |
| **CHoCH** | Change of Character | Primera ruptura **en contra** de la tendencia (p. ej. en bajista, romper el último máximo inferior) → primera señal de posible cambio de tendencia. |
| **EQH** | Equal Highs | Máximos a la misma altura: acumulan stops encima (liquidez compradora). |
| **EQL** | Equal Lows | Mínimos a la misma altura: acumulan stops debajo (liquidez vendedora). |
| **PDH** | Previous Day High | Máximo del día anterior; nivel de liquidez/resistencia clave. |
| **PDL** | Previous Day Low | Mínimo del día anterior; nivel de liquidez/soporte clave. |

## Liquidez

| Sigla | Término | Significado |
|---|---|---|
| **LQ** | Liquidity | Zonas donde se acumulan stops y órdenes pendientes, normalmente sobre máximos y bajo mínimos (swing highs/lows). |
| **BSL** | Buyside Liquidity | Liquidez **encima** de máximos (stops de los cortos, órdenes buy stop). |
| **SSL** | Sellside Liquidity | Liquidez **debajo** de mínimos (stops de los largos, órdenes sell stop). |
| **LS** | Liquidity Sweep | El precio barre un máximo/mínimo (caza los stops) y se gira. Suele preceder al movimiento real. |
| **LRLR** | Low Resistance Liquidity Run | Serie de máximos o mínimos poco defendidos que el precio recorre con facilidad, uno tras otro. |
| **IRL** | Internal Range Liquidity | Liquidez **dentro** del rango: FVGs, imbalances. |
| **ERL** | External Range Liquidity | Liquidez **fuera** del rango: swing highs/lows, PDH/PDL. El precio suele ir de IRL → ERL → IRL. |
| **SMT** | Smart Money Technique (divergencia SMT) | Divergencia entre activos correlacionados (NQ vs ES, o NQ vs YM): uno hace nuevo mínimo/máximo y el otro no → señal de giro. |

## Zonas de entrada (PD arrays)

| Sigla | Término | Significado |
|---|---|---|
| **FVG** | Fair Value Gap | Desequilibrio de 3 velas: hueco entre la mecha de la vela 1 y la de la vela 3, sin solapamiento. El precio suele volver a rellenarlo. |
| **IFVG** | Inversion Fair Value Gap | FVG que el precio atraviesa con cierre y que pasa a actuar en sentido contrario (un FVG alcista roto se vuelve resistencia). |
| **C.E.** | Consequent Encroachment | El 50 % de un FVG (o de una mecha). Nivel preciso de reacción/entrada. |
| **VI** | Volume Imbalance | Hueco entre los **cuerpos** de dos velas consecutivas, aunque las mechas se solapen. |
| **LV** | Liquidity Void | Movimiento rápido en un solo sentido con muy poco solapamiento (varios FVG seguidos); el precio suele volver a rellenarlo. |
| **OB** | Order Block | Última vela de color contrario antes de un movimiento fuerte que rompe estructura. Zona de soporte (OB alcista: última vela roja antes de la subida) o resistencia (OB bajista). |
| **MT** | Mean Threshold | El 50 % del cuerpo de un order block. Si el precio cierra más allá, el OB pierde validez. |
| **BB** | Breaker Block | OB que barrió liquidez y luego fue roto; cambia de papel (soporte ↔ resistencia). |
| **MB** | Mitigation Block | Como el breaker, pero el OB roto **no** había barrido liquidez (no hizo nuevo máximo/mínimo). |
| **RB** | Rejection Block | Zona de mechas largas en un máximo/mínimo; se entra cuando el precio vuelve a la zona entre el cuerpo y la punta de la mecha. |

## Ciclo de la sesión / de la vela

| Sigla | Término | Significado |
|---|---|---|
| **OHLC** | Open-High-Low-Close | Perfil de vela/día **bajista**: abre, primero hace el máximo, luego el mínimo y cierra abajo. |
| **OLHC** | Open-Low-High-Close | Perfil de vela/día **alcista**: abre, primero hace el mínimo (manipulación), luego el máximo y cierra arriba. |
| **PO3** | Power of Three | Toda vela (diaria, de 4 h…) tiene tres fases: acumulación, manipulación y distribución. |
| **AMD** | Accumulation, Manipulation, Distribution | **A**: rango cerca de la apertura (a menudo Asia). **M**: falso movimiento contra la dirección real que barre liquidez ("Judas swing", a menudo Londres/apertura NY). **D**: el movimiento real (expansión). |

## Modelo de entrada que combina todo

1. **Sesgo** en temporalidad alta (diario/4 h): estructura (BOS/CHoCH) y
   hacia qué liquidez va el precio (PDH/PDL, EQH/EQL, ERL).
2. **Esperar la killzone** (Londres o NY AM).
3. **Barrido de liquidez** (LS) contra el sesgo: la fase de manipulación.
4. **CHoCH** en temporalidad baja (1–15 min) a favor del sesgo, dejando un
   FVG u OB.
5. **Entrada** en el retroceso a ese FVG (su C.E.) u OB (hasta su MT), con
   vela de confirmación (ver `supply-demand-confirmations.md`).
6. **SL** detrás del barrido; **TP** en la liquidez opuesta (ERL, PDH/PDL);
   pasar a **BE** al llegar a 1R o al TP1.
