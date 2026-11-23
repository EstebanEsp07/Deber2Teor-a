# Fase C · Selección FEFO y regla de reposición

| Campo | Valor |
|---|---|
| **Fase / historias** | C-01, C-02, C-03 (Sprint 1–2) |
| **Responsable / revisor** | Richard (@RichJ-100) / Joshua (@joshdavr) |
| **Código** | `src/fefo.py`, `src/reposicion.py` |
| **Pruebas** | `tests/test_fefo.py` (27), `tests/test_reposicion.py` (18) |
| **Estado** | Borrador v0.1 — pendiente de revisión por pares |

## 1. Supuestos declarados (el enunciado no los fija)
| ID | Supuesto | Por qué |
|---|---|---|
| S1 | Un lote que vence **hoy** sigue siendo utilizable; vencido = vence **antes** de `hoy`. | El enunciado dice «no vencidos» sin definir el día límite. Cambiarlo es una sola comparación (`>=` por `>`). |
| S2 | Los códigos de lote son **únicos**; si hay repetidos se lanza `ValueError`. | Con códigos repetidos el desempate no sería reproducible. |
| S3 | El código se compara como **texto** (`"L10" < "L2"`). | Es lo que hace el orden `(vencimiento, código)` del enunciado; se recomienda ancho fijo (`L-002`). |
| S4 | Cantidades **enteras**; `disponible` del lote ya descuenta lo reservado. | Las unidades son discretas. |
| S5 | `hoy` se **recibe como parámetro**. | Sin `date.today()` dentro, las pruebas son reproducibles. |
| R1 | En reposición, cantidades enteras ≥ 0; `reservado` puede superar a `disponible + en_órdenes` (posición negativa). | Hay pedidos pendientes sin stock; es un caso real. |
| R2 | `objetivo ≥ mínimo`; si no, `ValueError`. | Un objetivo menor que el mínimo es una configuración incoherente. |
| R3 | La orden emitida se registra como **abierta** antes de la siguiente consulta. | La regla es una función pura; no recuerda lo que sugirió. |

## 2. Selección FEFO

### 2.1 Entrada, salida, tipo
- **Entrada:** lotes `(código, vencimiento, disponible)` de un SKU; `pedido` entero ≥ 1; `hoy`.
- **Salida:** `(aceptado, plan, faltante)` con `plan = [(código, cantidad), …]`.
- **Tipo:** regla de decisión operativa determinista (no es un problema de optimización: FEFO no minimiza nada, aplica un orden fijo).
- **Pedido 0 o negativo → `ValueError`**: reservar 0 unidades no es una reserva válida (el autómata de reserva parte de una solicitud con cantidad positiva).

### 2.2 Política si no alcanza el stock: **rechazar el pedido completo**
Se elige *rechazar* (todo o nada) entre las tres opciones del enunciado:
- **Atomicidad:** una reserva parcial dejaría un pedido a medias frente al autómata de reserva (Solicitada → Validada → Reservada); rechazar evita estados intermedios.
- **No se compromete stock inútil:** con parcial, ese stock queda inmovilizado para un pedido que no se puede completar.
- **No se pierde información:** se devuelve `faltante` y el `plan` parcial **solo como dato**; Planificación puede decidir entonces reservar parcial a mano o esperar reposición (el faltante alimenta la regla de la sección 3).
- El código **no modifica** el inventario (solo devuelve el plan), así que rechazar no requiere deshacer nada.

### 2.3 Pseudocódigo
```
FEFO(lotes, pedido, hoy):
  validar pedido (entero ≥ 1), hoy (fecha) y lotes (códigos únicos, disponible entero ≥ 0)
  candidatos ← [l ∈ lotes : l.vencimiento ≥ hoy  y  l.disponible > 0]
  ordenar candidatos por (l.vencimiento ascendente, l.código ascendente)
  plan ← [];  pendiente ← pedido
  para cada l en candidatos:
    si pendiente = 0: salir
    tomar ← min(pendiente, l.disponible)
    agregar (l.código, tomar) a plan;  pendiente ← pendiente − tomar
  devolver (aceptado = (pendiente = 0), plan, faltante = pendiente)
```

### 2.4 Terminación y corrección
- **Terminación:** el único ciclo recorre `candidatos`, una lista finita de a lo sumo `L` elementos; cada vuelta avanza un elemento. El ordenamiento también termina (Timsort sobre lista finita).
- **Invariante:** al inicio de cada vuelta, `suma(plan) + pendiente = pedido` y `0 ≤ pendiente ≤ pedido`. Se mantiene porque `tomar ≤ pendiente` y `tomar ≤ disponible`. Al salir: `pendiente = 0` ⇒ el plan cubre exactamente el pedido; `pendiente > 0` ⇒ se agotaron **todos** los candidatos, o sea que el stock elegible no alcanza.
- **Reproducible:** como los códigos son únicos, `(vencimiento, código)` es un **orden total**; el plan no depende del orden en que lleguen los lotes (hay una prueba que lo baraja 20 veces).
- **Exacta** respecto de la regla: no es heurística ni aproximación; es la política FEFO definida.

### 2.5 Complejidad (`L` = lotes del SKU)
| Paso | Tiempo | Espacio |
|---|---|---|
| Validar y filtrar candidatos | `O(L)` | `O(L)` |
| Ordenar candidatos | `O(L log L)` | `O(L)` |
| Recorrido voraz | `O(L)` | `O(plan) ⊆ O(L)` |
| **Total** | **`O(L log L)`** | **`O(L)`** |

Las cantidades se tratan como enteros de tamaño fijo (modelo RAM de costo unitario): sumar o restar es `O(1)`. Si las cantidades fueran enteros arbitrariamente grandes, cada operación costaría `O(b)` con `b` bits, pero en inventario real caben en 64 bits.

## 3. Regla de reposición

### 3.1 Entrada, salida, tipo
- **Entrada por SKU:** `disponible`, `en_órdenes_abiertas`, `reservado`, `mínimo`, `objetivo` (enteros ≥ 0, `objetivo ≥ mínimo`).
- **Salida:** `(posición, sugerencia)`. **Tipo:** cálculo determinista (no decisión Sí/No ni optimización).

### 3.2 Pseudocódigo
```
REPOSICION(disponible, en_orden, reservado, minimo, objetivo):
  validar entradas
  posicion ← disponible + en_orden − reservado
  si posicion ≤ minimo: sugerencia ← max(0, objetivo − posicion)
  si no:                sugerencia ← 0
  devolver (posicion, sugerencia)
```
**Terminación:** no tiene ciclos; son un número fijo de operaciones. Para `P` SKU, el recorrido hace `P` iteraciones sobre una lista finita.

### 3.3 Verificación con el ejemplo del deber
`posición = 18 + 10 − 5 = 23`; `23 ≤ 30` ⇒ `sugerencia = max(0, 50 − 23) = 27`. El código y las pruebas devuelven `(23, 27)`.

### 3.4 Cómo se evita duplicar sugerencias
Las unidades de las **órdenes abiertas ya suman a la posición**. Si se emite la orden por 27, la siguiente consulta ve `en_orden = 10 + 27 = 37` y `posición = 18 + 37 − 5 = 50 = objetivo`, que es mayor que el mínimo (30) ⇒ sugerencia **0**. Dos propiedades probadas:
1. **Idempotencia tras emitir:** pedir `sugerencia` y volver a consultar da 0.
2. **Sin pasarse del objetivo:** con una orden previa de 10 se sugieren 27; sin ella se sugerirían 37; `10 + 27 = 37`, o sea, el total ordenado es el mismo que sin orden previa.

Límite honesto: esto depende de **R3**. Como la regla es una función pura, si la orden no se registra como abierta antes de la siguiente consulta, repite la sugerencia.

### 3.5 Complejidad
| Caso | Tiempo | Espacio |
|---|---|---|
| Un SKU | `O(1)` | `O(1)` |
| `P` SKU, procesados uno a uno | `O(P)` | `O(1)` adicional |
| `P` SKU guardando todas las sugerencias | `O(P)` | `O(P)` (la salida) |

## 4. Pruebas y salida observada
| Módulo | Tipo | Casos |
|---|---|---|
| FEFO | Normal | toma el que vence antes; pedido que abarca varios lotes; la entrada no se modifica; fechas `date` y texto |
| FEFO | Límite | lote vencido; vence hoy (S1); todos vencidos; `disponible = 0`; **empate de fecha** (desempate por código); orden de entrada barajado; orden lexicográfico (S3); pedido = stock; **pedido > stock** (rechazo con plan parcial); **SKU sin lotes**; pedido de 1; 50 000 lotes |
| FEFO | Inválido | pedido **0 o negativo**; pedido no entero (`2.5`, `"10"`, `None`, `True`); `disponible` negativo o no entero; código repetido o vacío; fecha mal formada o inexistente; `datetime`; lote mal formado; entrada no lista; `hoy` inválido |
| Reposición | Normal / anti-duplicación | ejemplo del deber (23, 27); posición cómoda; orden emitida ⇒ 0; orden previa + sugerencia = total sin orden previa; orden previa suficiente |
| Reposición | Límite | posición = mínimo (sí sugiere); mínimo + 1 (no); posición negativa; todo en 0; objetivo = mínimo; catálogo vacío |
| Reposición | Inválido | negativos; tipos; `objetivo < mínimo`; fila mal formada |

**Reproducir**
```bash
python3 src/fefo.py
python3 src/reposicion.py
python3 -m unittest discover -s tests -v
```
**Salida observada** (ejecutada en Python 3.12.3; falta repetirla en la máquina de Richard)
```
=== python3 src/fefo.py ===
Pedido de 70: ACEPTADO
  plan = [('L-002', 30), ('L-001', 25), ('L-003', 15)]   faltante = 0
Pedido de 200: RECHAZADO (stock insuficiente)
  plan = [('L-002', 30), ('L-001', 25), ('L-003', 40)]   faltante = 105
SKU sin lotes, pedido de 5: RECHAZADO (stock insuficiente)
  plan = []   faltante = 5
=== python3 src/reposicion.py ===
Ejemplo del deber: posición = 23, sugerencia = 27
Tras emitir la orden de 27: posición = 50, sugerencia = 0
SKU-A: posición = 23, sugerencia = 27
SKU-B: posición = 70, sugerencia = 0
SKU-C: posición = 25, sugerencia = 25
SKU-D: posición = 30, sugerencia = 20
SKU-E: posición = -15, sugerencia = 65
```
`test_fefo.py`: 27 pruebas OK · `test_reposicion.py`: 18 pruebas OK · repo completo: 333 pruebas OK.

## 5. Conclusión
FEFO se resuelve en `O(L log L)` tiempo y `O(L)` espacio con un orden total reproducible, y rechaza de forma atómica lo que el stock no cubre. La reposición es `O(1)` por SKU y no duplica órdenes porque las órdenes abiertas ya cuentan en la posición, siempre que se registren antes de volver a consultar.
