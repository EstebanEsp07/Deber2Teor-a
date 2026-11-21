# Ficha P3 · Capacidad máxima de despacho

## Plan breve y supuestos

**Plan.** (1) Modelar el correo como una red de flujo dirigida con capacidades enteras. (2) Separar el problema de **optimización** (valor del flujo máximo) de su **versión de decisión** (¿existe un flujo de valor ≥ K?), que es la que se clasifica en P. (3) Resolver con Edmonds–Karp, registrar cada camino aumentante y la actualización del residual, y comprobar el resultado con el corte mínimo. (4) Justificar la terminación y la cota O(V·E²), sin depender del valor numérico de las capacidades. (5) Implementar en Python con `unittest` y pegar la salida observada real.

**Supuestos (no cambian datos ni condiciones del correo):**

- S1. Las capacidades de la tabla del portal son las **capacidades actuales**, es decir, ya reflejan la falla temporal del CD Quito («Revisa las capacidades actuales en la red del portal»). No se reduce ni se modifica ningún valor.
- S2. El nodo `Planta` del portal es la Planta Durán (origen `s`) y `Clientes` es la zona de clientes (destino `t`).
- S3. Los tramos son **dirigidos**, como indican las flechas del mapa. Existe `Quito → Guayaquil` (2), pero no `Guayaquil → Quito`.
- S4. Las capacidades son enteras y no negativas, en camiones/día.

| Campo | Valor |
|---|---|
| Grupo de análisis | A·P |
| Correo | «Máximo de camiones hacia clientes» — Luis Vaca · Distribución |
| Responsable / revisor | Paula Altamirano / *(por asignar: otro integrante del equipo)* |
| Código | `src/flujo_maximo.py` |
| Pruebas | `tests/test_flujo_maximo.py` |
| Estado | Borrador (pendiente de revisión por otro integrante) |

## 1. Identificador y resumen (sin cambiar condiciones)

**P3 · Capacidad máxima de despacho.** Una falla temporal redujo la operación del CD Quito. Servicio al Cliente pide saber **cuántos camiones por día todavía pueden llegar desde la Planta Durán hasta la zona de clientes sin exceder la capacidad de ningún tramo**. El correo pide tres cosas: el máximo que puede despacharse con esas restricciones, un **registro reproducible** de cómo se actualizan los tramos usados y disponibles, y el algoritmo en código con un análisis de cómo crece su trabajo al aumentar nodos y conexiones. Además advierte que **no debe suponerse que la suma de capacidades de salida equivale al flujo que realmente llega**.

Datos del expediente (tabla del portal, sin modificar):

| Origen | Destino | Capacidad (camiones/día) |
|---|---|---|
| Planta | Quito | 7 |
| Planta | Guayaquil | 5 |
| Quito | Clientes | 4 |
| Guayaquil | Clientes | 6 |
| Quito | Guayaquil | 2 |

## 2. Entrada, salida y restricciones

**Entrada:** una red dirigida `G = (V, E)`, una función de capacidad `c: E → ℤ≥0`, un origen `s` y un destino `t` (con `s ≠ t`). En el caso: `V = {Planta, Quito, Guayaquil, Clientes}`, `|V| = 4`, `|E| = 5`, `s = Planta`, `t = Clientes`.

**Salida (optimización):** el valor `|f*|` de un flujo máximo `s → t`, el flujo asignado a cada tramo, la traza de caminos aumentantes y un corte mínimo que certifica la optimalidad.

**Restricciones que debe cumplir un flujo `f`:**
- Capacidad: `0 ≤ f(u,v) ≤ c(u,v)` en cada tramo.
- Conservación: en todo nodo distinto de `s` y `t`, lo que entra es igual a lo que sale.
- Valor: `|f|` = flujo neto que sale de `s`, que es igual al flujo neto que llega a `t`.

**¿Decisión u optimización?** El problema **original del correo es de optimización**: pide el flujo máximo. La clasificación en P se hace sobre su **versión de decisión asociada**:

> **MAX-FLOW-DEC** = { ⟨G, c, s, t, K⟩ : existe un flujo `s → t` en `G` con `|f| ≥ K` }.

Las dos versiones son equivalentes en costo polinómico. Con el valor óptimo se responde la decisión comparando `|f*| ≥ K`. A la inversa, el óptimo se obtiene con búsqueda binaria sobre `K ∈ [0, Σc]`, que hace O(log Σc) llamadas, una cantidad polinómica en el tamaño en bits. En el código, la decisión es `existe_flujo_al_menos(red, s, t, K)`.

## 3. Clasificación y evidencia (Grupo A · P)

**Clasificación:** MAX-FLOW-DEC ∈ **P**.

**Evidencia (algoritmo polinómico conocido):** Edmonds–Karp calcula un flujo máximo exacto en **O(V·E²)** operaciones aritméticas. Esa cota no depende de los valores de las capacidades (ver §5–6). Para decidir MAX-FLOW-DEC basta con ejecutarlo y comparar con `K`, así que hay un decisor determinista en tiempo polinómico.

Observaciones:
- MAX-FLOW-DEC también está en NP, como todo problema en P (P ⊆ NP). El certificado sería un flujo `f`, que se verifica en O(V+E) revisando capacidad, conservación y `|f| ≥ K`. Esa pertenencia es más débil que lo que ya sabemos: el problema se **resuelve**, no solo se verifica, en tiempo polinómico.
- No es NP-completo, salvo que P = NP.
- El teorema **flujo máximo = corte mínimo** da un certificado también para la respuesta «no». Si un corte `(S, V\S)` tiene capacidad `< K`, ningún flujo puede alcanzar `K`.

## 4. Decidibilidad y computabilidad

**Modelo de cómputo supuesto:** máquina **RAM de palabra** (word-RAM) determinista. Cada palabra tiene O(log(E·C)) bits, donde `C = max c(e)`, y las sumas, restas y comparaciones cuestan O(1). Una máquina de Turing determinista la simula con sobrecosto polinómico, así que la clasificación en P vale también en el modelo de Turing.

- **Decidible:** sí. Para toda entrada válida, el procedimiento termina (§5) y responde Sí/No a MAX-FLOW-DEC. Las entradas inválidas (capacidades negativas o no enteras, nodos inexistentes, `s = t`, CSV mal formado) se rechazan con un error explícito, y ese rechazo también termina.
- **Computable:** la función `⟨G, c, s, t⟩ ↦ |f*|` es computable con un procedimiento efectivo y finito. Además es **eficientemente** computable (tiempo polinómico), algo que no ocurre con todos los problemas computables.

## 5. Algoritmo seleccionado y justificación

**Algoritmo:** Edmonds–Karp, es decir, Ford–Fulkerson donde el camino aumentante se elige con **BFS** (el camino con menos aristas en el grafo residual).

**Carácter:** **exacto**. No es aproximado ni heurístico. Al terminar no queda ningún camino aumentante, y entonces el flujo es máximo (teorema de flujo máximo y corte mínimo). Con capacidades enteras el resultado es entero (teorema de integralidad), lo que tiene sentido para contar camiones.

**¿Por qué no otro algoritmo?**
- Ford–Fulkerson con DFS arbitrario es pseudopolinómico: O(E·|f*|), que depende del valor de las capacidades.
- BFS solo (P1) responde alcanzabilidad, no capacidad.
- Dijkstra (P2) optimiza costo de camino, no flujo.
- Edmonds–Karp es simple, exacto y tiene cota polinómica fuerte. Algoritmos como Dinic (O(V²E)) o push-relabel son más rápidos en teoría, pero innecesarios para este tamaño.

**Pseudocódigo:**

```
EDMONDS-KARP(G, c, s, t):
  validar entrada (capacidades enteras ≥ 0, s ≠ t, s y t ∈ V)
  r(u,v) ← c(u,v) para cada (u,v) ∈ E ;  r(v,u) ← 0 si no existe   ▷ residual con inversas
  |f| ← 0
  repetir:
     padre ← BFS(s) usando solo aristas con r(u,v) > 0
     si t ∉ padre: salir                                          ▷ no hay camino aumentante
     P ← camino s→t reconstruido con padre                        ▷ el más corto en nº de aristas
     δ ← min { r(u,v) : (u,v) ∈ P }                               ▷ cuello de botella
     para cada (u,v) ∈ P:  r(u,v) ← r(u,v) − δ ;  r(v,u) ← r(v,u) + δ
     |f| ← |f| + δ ;  registrar (P, δ, actualizaciones)
  S ← nodos alcanzables desde s en el residual                    ▷ corte mínimo
  devolver |f|, f(u,v) = c(u,v) − r(u,v) (acotado a [0, c]), (S, V\S)
```

**BFS completada (fragmento real de `src/flujo_maximo.py`).** La versión base del simulador recorre `residual[u]` sin inicializar todos los nodos, y lanzaría `KeyError` si un nodo intermedio no aparece como clave. Aquí el residual se inicializa con **todos** los nodos y sus aristas inversas en 0 antes de empezar:

```python
def _bfs_camino(res, s, t):
    padre = {s: None}
    cola = deque([s])
    while cola:
        u = cola.popleft()
        for v, c in res[u].items():
            if c > 0 and v not in padre:   # solo tramos con capacidad disponible
                padre[v] = u
                if v == t:
                    return padre
                cola.append(v)
    return None
```

### Terminación y cota O(V·E²): por qué no depende de las capacidades

Sea `δ_f(s,v)` la distancia, en número de aristas, de `s` a `v` en el residual `G_f`.

1. **Monotonía.** Al aumentar por un camino más corto, `δ_f(s,v)` nunca disminuye para ningún `v`. Las aristas que aparecen en el residual son inversas `(v,u)` de aristas del camino, y van «hacia atrás» en distancia. Por eso no pueden acortar ningún camino desde `s`.
2. **Arista crítica.** En cada aumento, al menos una arista del camino es crítica: su capacidad residual es igual a `δ` y se satura. Si `(u,v)` es crítica, entonces `δ(s,v) = δ(s,u) + 1` y desaparece del residual. Solo puede volver si luego se usa `(v,u)` en un camino más corto, lo que exige `δ'(s,u) = δ'(s,v) + 1 ≥ δ(s,u) + 2`. Por tanto, entre dos veces consecutivas en que `(u,v)` es crítica, `δ(s,u)` crece al menos en 2. Como `δ(s,u) ≤ V − 1`, **cada arista es crítica a lo sumo O(V/2) veces**.
3. **Conteo.** El residual tiene a lo sumo `2E` aristas, así que hay **O(V·E) aumentos**. Cada aumento cuesta una BFS más la actualización del camino, O(V + E) = O(E) cuando `E ≥ V − 1`. Total: **O(V·E²)**.

En ese argumento **nunca aparece el valor de las capacidades**: solo se cuentan distancias y aristas. Por eso la cota es **fuertemente polinómica**. Con capacidades `10¹⁸` o de cualquier magnitud, el número de iteraciones sigue acotado por O(V·E). La prueba `test_capacidades_enormes_no_afectan_iteraciones` lo muestra: con capacidades `10¹⁸`, Edmonds–Karp hace **2** aumentos, mientras que Ford–Fulkerson con una mala elección de caminos podría necesitar del orden de `2·10¹⁸`. Además, como las capacidades son enteras, cada aumento sube `|f|` en al menos 1, lo que da un segundo argumento de terminación. Ese segundo argumento es pseudopolinómico y no es el que da la cota.

### Traza del caso P3 (tomada de la salida observada, §7)

| # | Camino aumentante (BFS) | Cuello δ | Actualización del residual | \|f\| acumulado |
|---|---|---|---|---|
| 1 | Planta → Quito → Clientes | 4 | Planta→Quito 7→3; Quito→Clientes 4→0 (inversas +4) | 4 |
| 2 | Planta → Guayaquil → Clientes | 5 | Planta→Guayaquil 5→0; Guayaquil→Clientes 6→1 (inversas +5) | 9 |
| 3 | Planta → Quito → Guayaquil → Clientes | 1 | Planta→Quito 3→2; Quito→Guayaquil 2→1; Guayaquil→Clientes 1→0 | **10** |
| — | BFS final: desde Planta se alcanzan Quito y Guayaquil, pero no Clientes | — | termina | **10** |

Observa el orden de la BFS. El camino de 3 aristas (Quito → Guayaquil) solo aparece cuando ya no quedan caminos de 2 aristas, como establece el lema de monotonía.

### Comprobación con el corte mínimo

En el residual final, el conjunto alcanzable desde `s` es `S = {Planta, Quito, Guayaquil}` y `V\S = {Clientes}`.

- Aristas del corte `S → V\S`: Quito→Clientes (4) + Guayaquil→Clientes (6) = **10**.
- No hay aristas de `V\S` hacia `S` con flujo.
- `|f*| = 10 = c(S, V\S)`. Por el teorema de flujo máximo y corte mínimo, **10 es óptimo**: ningún plan puede superar 10 camiones/día.

**Respuesta a la advertencia del correo:** la salida de la planta suma 7 + 5 = 12, pero solo **llegan 10**. El cuello de botella son los tramos de entrada a Clientes (4 + 6). Quedan 2 camiones/día de holgura en Planta→Quito (usado 5 de 7), y Quito→Guayaquil usa 1 de 2.

Flujo por tramo: Planta→Quito 5/7 · Planta→Guayaquil 5/5 · Quito→Clientes 4/4 · Quito→Guayaquil 1/2 · Guayaquil→Clientes 6/6. Hay conservación en Quito (entra 5, sale 4 + 1) y en Guayaquil (entra 5 + 1, sale 6).

## 6. Complejidad Big-O temporal y espacial

**Variables:**
- `V` = número de nodos (centros); `E` = número de tramos dirigidos.
- `C = max c(e)` = la mayor capacidad, como **valor**.
- **Tamaño de entrada en bits:** `n = Θ((V + E)·log V + Σ_e log₂(c(e) + 1))`. Cada capacidad ocupa O(log C) bits, **no** C unidades.

| Recurso | Cota | Justificación |
|---|---|---|
| Tiempo (operaciones aritméticas) | **O(V·E²)** | O(V·E) aumentos × O(E) por BFS y actualización (§5) |
| Tiempo en bits | **O(V·E²·log(E·C))** | todo valor intermedio es ≤ Σc ≤ E·C, así que cada operación cuesta O(log(E·C)) bits, lo que es **polinómico en n** |
| Espacio del algoritmo | **O(V + E)** | residual con ≤ 2E entradas + `padre` y cola O(V) |
| Espacio de la traza (opcional) | O(#aumentos · V) ⊆ O(V²·E) | registro reproducible pedido en el correo; no es necesario para calcular |
| Versión de decisión | O(V·E²) + O(1) | una ejecución + comparar con K |

**Valor vs. bits.** Ford–Fulkerson genérico cuesta O(E·|f*|), con `|f*| ≤ E·C`. Eso es polinómico en el **valor** C pero **exponencial en log C**, es decir, pseudopolinómico. Edmonds–Karp evita esa dependencia.

**Caso P3:** `V = 4`, `E = 5`, así que la cota es `V·E² = 100` (en orden de magnitud). La cota de aumentos `V·E/2 = 10` se cumple: hubo **3** aumentos.

**Crecimiento (lo que pide el correo):** si se duplican los tramos, el peor caso crece ~4×. Si se duplican los centros, crece ~2× en la cota. El valor de las capacidades no afecta el número de iteraciones.

## 7. Código, casos de prueba y salida observada

**Estructura del código (`src/flujo_maximo.py`, Python 3.8+, solo biblioteca estándar):**
- **Lectura:** `leer_aristas_csv(texto)` convierte el CSV `origen,destino,capacidad` en aristas y `construir_red(aristas)` valida y construye la red. Valida capacidades enteras ≥ 0 (rechaza `bool`, `float` y texto), nombres no vacíos, sin lazos y aristas de 3 campos; los tramos repetidos se suman.
- **Procesamiento:** `edmonds_karp(red, s, t)` devuelve el valor, la traza, el flujo por tramo y el corte mínimo. También están `corte_minimo(...)` y `existe_flujo_al_menos(red, s, t, K)` (versión de decisión).
- **Presentación:** `formatear_resultado(...)` y `main()`. `main()` usa los datos del expediente o un CSV pasado como argumento, y devuelve código de salida 1 con un mensaje claro si la entrada es inválida.

**Cómo ejecutar (desde la raíz del repositorio):**

```bash
python src/flujo_maximo.py                       # caso P3
python src/flujo_maximo.py ruta/a/red.csv        # otra red
python -m unittest discover -s tests -v          # pruebas
```

**Casos de prueba (`tests/test_flujo_maximo.py`, 29 pruebas):**

| Tipo | Pruebas |
|---|---|
| Normales (caso P3) | valor = 10; 10 < 12 (no es la suma de salidas); traza exacta de los 3 caminos; corte mínimo `S = {Planta, Quito, Guayaquil}` con capacidad 10; capacidad y conservación en cada nodo; decisión con K = 10 → Sí, K = 11 → No, K = 0 → Sí; CSV equivalente a tuplas |
| Límite | destino inalcanzable → 0; arista de capacidad 0; una sola arista; tramos repetidos sumados; aristas antiparalelas; caso que exige arista inversa; capacidades `10¹⁸` con solo 2 aumentos; cota de aumentos ≤ V·E/2 en red bipartita 6×6; CSV sin cabecera y con líneas vacías |
| Inválidas | capacidad negativa; capacidad `2.5`, `"3"`, `True`, `None`; nombre vacío; lazo; arista de 2 campos; `s = t`; origen o destino inexistente; CSV con campos faltantes o capacidad «siete»; entrada no textual; red que no es diccionario; K negativo, decimal o booleano |

**Salida observada.** Se ejecutó en el entorno de trabajo de este chat (Linux, **Python 3.13.18**) el 21-nov-2026. El texto está pegado tal cual. *El código usa solo construcciones compatibles con 3.8+, pero no se probó en 3.8. El equipo debe volver a correrlo en su máquina y reemplazar este bloque por su propia salida antes de la entrega.*

`python src/flujo_maximo.py`:

```
Flujo máximo Planta -> Clientes: 10 camiones/día

Traza de caminos aumentantes (BFS):
  1. Planta -> Quito -> Clientes  (cuello = 4)
       Planta->Quito: 7->3 | inversa Quito->Planta: 0->4
       Quito->Clientes: 4->0 | inversa Clientes->Quito: 0->4
  2. Planta -> Guayaquil -> Clientes  (cuello = 5)
       Planta->Guayaquil: 5->0 | inversa Guayaquil->Planta: 0->5
       Guayaquil->Clientes: 6->1 | inversa Clientes->Guayaquil: 0->5
  3. Planta -> Quito -> Guayaquil -> Clientes  (cuello = 1)
       Planta->Quito: 3->2 | inversa Quito->Planta: 4->5
       Quito->Guayaquil: 2->1 | inversa Guayaquil->Quito: 0->1
       Guayaquil->Clientes: 1->0 | inversa Clientes->Guayaquil: 5->6
  BFS final: no alcanza Clientes; algoritmo termina.

Flujo por tramo (usado / capacidad):
  Guayaquil->Clientes: 6/6
  Planta->Guayaquil: 5/5
  Planta->Quito: 5/7
  Quito->Clientes: 4/4
  Quito->Guayaquil: 1/2

Corte mínimo: S = {Guayaquil, Planta, Quito}
  Aristas S -> V\S: Quito->Clientes(4), Guayaquil->Clientes(6)
  Capacidad del corte = 10
  ¿Flujo máximo = corte mínimo? Sí
```

`python -m unittest discover -s tests -v` (resumen; las 29 líneas individuales terminan en `... ok`):

```
Ran 29 tests in 0.003s

OK
```

Entrada inválida: `python src/flujo_maximo.py malo.csv`, con la fila `Planta,Quito,-3`:

```
Error de entrada: Capacidad negativa en Planta->Quito: -3.
```

(código de salida 1)

## 8. Conclusión

- **Respuesta operativa:** con las capacidades actuales del portal, **pueden llegar como máximo 10 camiones por día** desde la Planta Durán a la zona de clientes. No son 12: los tramos de entrada a Clientes (Quito→Clientes 4 y Guayaquil→Clientes 6) forman el corte mínimo y limitan el despacho. Hay 2 camiones/día de holgura en Planta→Quito que no pueden aprovecharse sin ampliar esos tramos finales.
- **Teoría:** el problema original es de optimización. Su versión de decisión, MAX-FLOW-DEC, está en **P**: Edmonds–Karp es un algoritmo **exacto**, termina siempre y corre en **O(V·E²)** con una cota independiente del valor de las capacidades, es decir, polinómica en el tamaño en bits. Es decidible y computable en el modelo word-RAM. El corte mínimo certifica la optimalidad.
- **Recomendación:** para comunicar compromisos, usar 10 camiones/día. Si se quiere subir esa cifra, hay que ampliar Quito→Clientes o Guayaquil→Clientes; ampliar las salidas de la planta no sirve.

---

## Lista de verificación antes de pedir revisión

- [x] El resumen **no cambia** las condiciones del correo (datos, límites, preguntas). Las capacidades son las de la tabla y la falla del CD Quito se menciona sin alterar valores (S1).
- [x] Se dice explícitamente si es **decisión** u **optimización**: el original es optimización y se clasifica MAX-FLOW-DEC (§2).
- [x] La etiqueta P está **sostenida con la evidencia que corresponde** al grupo A: un algoritmo polinómico conocido con prueba de cota (§3, §5).
- [x] No se escribe «NP = no polinómico»: se menciona NP como *verificable* en tiempo polinómico (§3).
- [x] Hay **modelo de cómputo** nombrado (word-RAM, simulable por MT) y se justifica la **terminación** (§4, §5).
- [x] Las variables de Big-O están definidas y se distingue el valor `C` del tamaño en bits `log C` (§6).
- [x] El código valida entradas y separa lectura / procesamiento / presentación (§7).
- [x] Hay pruebas normales, límite e inválidas, y la **salida observada** es la real, pegada tras ejecutar (§7). *Pendiente: que el equipo la reemplace por la de su propia ejecución.*
- [ ] Alguien distinto al autor la revisó (nombre en el campo «revisor»).

---

## Anexo · Guion de defensa oral (~2 min)

> **(Problema, 20 s)** El correo P3 pregunta cuántos camiones por día pueden llegar de la Planta Durán a los clientes tras la falla del CD Quito, sin exceder ningún tramo. Lo modelamos como una red de flujo dirigida con las capacidades actuales del portal. Es un problema de **optimización**. Para clasificarlo usamos su versión de decisión: ¿existe un flujo de al menos K?
>
> **(Algoritmo, 35 s)** Usamos Edmonds–Karp: Ford–Fulkerson eligiendo siempre, con BFS, el camino aumentante con menos tramos. En nuestro caso hubo tres aumentos: Planta–Quito–Clientes con 4, Planta–Guayaquil–Clientes con 5, y Planta–Quito–Guayaquil–Clientes con 1. En total, **10 camiones por día**. Cada paso resta el cuello de botella en la arista directa y lo suma en la inversa, y eso queda en la traza que pidió el correo.
>
> **(Optimalidad, 20 s)** ¿Cómo sabemos que 10 es el máximo? Después del último paso, desde la planta solo se alcanzan Quito y Guayaquil. El corte que los separa de Clientes vale 4 + 6 = 10. Flujo máximo igual a corte mínimo: no se puede hacer mejor. Por eso la suma de salidas, 12, engaña.
>
> **(Complejidad y P, 35 s)** El algoritmo siempre termina. Como BFS usa caminos más cortos, las distancias en el residual nunca bajan, y cada arista se satura a lo sumo V/2 veces. Eso da O(V·E) aumentos de costo O(E) cada uno: **O(V·E²)**. Esa cuenta no usa el valor de las capacidades: con capacidades de 10¹⁸ hicimos solo dos aumentos en las pruebas. Es polinómico en el tamaño en bits, así que la versión de decisión está en **P**. Es decidible y exacto, no heurístico.
>
> **(Cierre, 10 s)** El código valida las entradas, separa lectura, cálculo y presentación, y pasa 29 pruebas normales, límite e inválidas. Recomendación: comprometer 10 camiones por día y, si se quiere más, ampliar los tramos que llegan a Clientes.
