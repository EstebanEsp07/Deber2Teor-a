# Ficha C2 · Recorrido que visita cada centro una vez

> **Plan breve.** (1) Fijar una lectura única del correo y declarar las ambigüedades como supuestos. (2) Separar la versión de **decisión** (la que se pide) de la de **optimización**. (3) Sustentar la NP-completitud: pertenencia a NP mediante certificado y verificador, más la reducción Ciclo Hamiltoniano ≤ₚ TSP-D. (4) Implementar el verificador, la búsqueda exacta, la reducción y una heurística de contraste, con pruebas normales, límite e inválidas. (5) Ejecutar y pegar la **salida real**.
>
> **Supuestos de trabajo** (detalle en §1.2): S1, se pide un **ciclo** que regresa al punto de salida. S2, se usa la matriz `[[0,4,8],[4,0,3],[8,3,0]]` en km, tomada del código fuente del simulador. S3, índices 0 = Planta, 1 = Quito y 2 = Guayaquil. S4, el punto de salida es la Planta. S5, «cumplir el límite» significa costo ≤ L, sin desigualdad estricta. S6, las distancias son números finitos ≥ 0 y la diagonal vale 0.

| Campo | Valor |
|---|---|
| Grupo de análisis | C·NP-completo |
| Correo | «¿Existe una ruta hamiltoniana dentro del presupuesto?», de Jorge Tapia (Ruteo) |
| Responsable / revisor | Joshua / *pendiente de asignar* |
| Código | `src/tsp_decision.py` |
| Pruebas | `tests/test_tsp_decision.py` |
| Estado | Borrador (pendiente de revisión por un compañero) |

---

## 1. Identificador y resumen (sin cambiar condiciones)

### 1.1 Resumen fiel del correo
Para la entrega especial de mañana hay que **visitar todos los centros del manifiesto y regresar al punto de salida**. La gerencia fijó un **presupuesto máximo de L km**. La pregunta operativa es **si existe al menos un recorrido** que cumpla ese límite. Se pide usar la matriz del expediente y devolver un recorrido válido cuando exista, junto con su costo y una verificación ejecutable. La ficha debe tratar la **pregunta de decisión** y distinguirla de la búsqueda del recorrido de menor costo. También se piden el código y un comentario sobre cómo crece la búsqueda al agregar centros.

Datos del expediente (tabla del portal): Centros = *Planta, Quito, Guayaquil* (n = 3); Distancias = *matriz simétrica, km*; Límite = **20 km**.

### 1.2 Ambigüedades y contradicciones detectadas (y lectura adoptada)
| # | Observación | Lectura adoptada (supuesto) |
|---|---|---|
| A1 | El **asunto** habla de «ruta **hamiltoniana**» (un camino que no vuelve), pero el **cuerpo** pide «regresar al punto de salida» (un ciclo). La ficha del portal dice «visite cada centro exactamente una vez, costo ≤ L (versión de decisión de TSP)», y el código del HTML cierra el ciclo (`camino = (0,) + ruta + (0,)`). | **S1: ciclo hamiltoniano (tour de TSP).** Manda el cuerpo del correo y concuerda con el portal y el código. La variante de *camino* sigue disponible con `--modo camino` y se reporta aparte (§7). Ambas variantes son NP-completas. |
| A2 | La tabla visible solo dice «matriz simétrica, km». **Los números de la matriz solo aparecen en el código fuente del HTML** (`d = [[0,4,8],[4,0,3],[8,3,0]]`, `ruta_dentro(d, 20)`). | **S2:** se usa esa matriz. Conviene confirmarla con Jorge Tapia porque no figura en la tabla del expediente. |
| A3 | No se dice qué fila corresponde a cada centro. | **S3:** se sigue el orden en que la tabla lista los centros: 0 = Planta, 1 = Quito, 2 = Guayaquil. |
| A4 | El «punto de salida» no tiene nombre. | **S4:** Planta. En un **ciclo**, la elección del inicio no cambia la respuesta Sí/No porque cualquier rotación del ciclo cuesta lo mismo. |
| A5 | «Cumpla ese límite» no aclara si la desigualdad es estricta. | **S5:** costo ≤ L, como dice la ficha del portal. |
| A6 | La matriz del caso es simétrica, pero el problema general podría no serlo (vías de un sentido). | El código acepta matrices **asimétricas** e informa si la matriz es simétrica. La NP-completitud se cumple incluso en el caso simétrico y métrico (§3). |
| A7 | La plantilla cita `fichas/N1_isomorfismo_grafos.md` y el enunciado del equipo menciona `NP1_…`. Ese archivo no llegó adjunto. | Se siguió solo `docs/PLANTILLA_FICHA.md`. Hay que revisar el nombre real del archivo de ejemplo en el repositorio. |

## 2. Entrada, salida y restricciones

**Versión pedida: DECISIÓN.** La versión de optimización solo se usa como referencia y queda separada.

- **Entrada:** el número de centros `n ≥ 1`, una matriz `D ∈ ℝ≥0^{n×n}` con `D[i][i] = 0` (km) y un presupuesto `L ≥ 0`. Codificación: `n²` números de hasta `b` bits cada uno, más `L`, de modo que el tamaño en bits es **N = Θ(n²·b + log L)**.
- **Pregunta (TSP-D):** ¿existe una permutación `π` de los `n` centros tal que `Σₖ D[π(k)][π(k+1)] + D[π(n)][π(1)] ≤ L`?
- **Salida:** **SÍ** junto con un recorrido (certificado) y su costo, o **NO** cuando se agota el espacio de búsqueda.
- **Restricciones validadas:** la matriz debe ser cuadrada y no vacía, con valores numéricos finitos ≥ 0 y diagonal 0 (los `bool` se rechazan). L debe ser numérico, finito y ≥ 0. Los nombres de los centros deben ser distintos y su cantidad debe ser `n`.
- **Optimización (no pedida):** hallar `min_π costo(π)`. Si los pesos son enteros, la optimización se reduce a la decisión mediante **búsqueda binaria sobre L**, con `O(log(n·W_max))` llamadas a TSP-D.

## 3. Clasificación y evidencia: **NP-completo**

### 3.1 TSP-D ∈ NP (certificado + verificador polinómico)
- **Certificado:** el orden de los `n` centros, de tamaño `O(n log n)` bits, que es polinómico en N.
- **Verificador** (`verificar`): (i) comprueba que el certificado sea una permutación de `0..n-1` usando un conjunto, en O(n); (ii) suma las `n` aristas del ciclo, en O(n) operaciones aritméticas, es decir, `O(n·(b + log n))` operaciones de bits; (iii) compara el resultado con L. **El tiempo total es polinómico en N.**
- **Aclaración:** NP **no** significa «no polinómico». NP es la clase de problemas de decisión cuyas respuestas *Sí* tienen certificados **verificables en tiempo polinómico** (o, de forma equivalente, que una MT **no determinista** decide en tiempo polinómico). P ⊆ NP. Nada de lo anterior supone P ≠ NP.

### 3.2 Problema NP-completo de origen: **Ciclo Hamiltoniano (HC)**
HC pregunta si un grafo no dirigido `G = (V, E)` tiene un ciclo simple que pase por todos los vértices. Es NP-completo (Karp, 1972, por reducción desde Vertex Cover / 3-SAT).

### 3.3 Reducción polinómica HC ≤ₚ TSP-D (`reducir_ciclo_hamiltoniano`)
Dado `G = (V, E)` con `|V| = n ≥ 3`, se construye `f(G) = (D, L)` así:
`D[u][v] = 1` si `{u,v} ∈ E`; `D[u][v] = 2` si `{u,v} ∉ E`; `D[u][u] = 0`; **`L = n`**.
- **Tiempo de construcción:** O(n²), y la salida mide O(n²) entradas de 2 bits. Es **polinómica**.
- **(⇒)** Si G tiene un ciclo hamiltoniano, ese ciclo usa `n` aristas de E con peso 1 cada una, así que su costo es `n ≤ L`.
- **(⇐)** Todo tour tiene exactamente `n` aristas de peso ≥ 1, de modo que su costo es ≥ n. Si el costo es ≤ n, todas las aristas pesan 1, todas pertenecen a E, y el tour es un ciclo hamiltoniano de G.
- **Observación:** con pesos de 1 y 2 la matriz es **simétrica y cumple la desigualdad triangular**, porque 1 + 1 ≥ 2. Por eso el problema sigue siendo NP-completo **incluso restringido a instancias como la del correo**, simétricas y métricas. La simetría no lo vuelve fácil en general.
- **Validación empírica:** las pruebas recorren **todos** los grafos de 4 vértices (64) y de 5 vértices (1024) y confirman que `HC(G) = TSP-D(f(G))`. También comprueban que el grafo de Petersen, que no es hamiltoniano, da NO (§7).

**Conclusión:** TSP-D ∈ NP y HC ≤ₚ TSP-D, por lo tanto **TSP-D es NP-completo**. La variante del asunto (camino hamiltoniano con presupuesto) también es NP-completa, por la misma vía desde Camino Hamiltoniano.

### 3.4 Consecuencia práctica
Que TSP-D sea NP-completo **no demuestra** que no exista un algoritmo polinómico. Lo que implica es que encontrar uno probaría **P = NP**. En la práctica no se conoce ningún algoritmo exacto con peor caso polinómico, de modo que hay dos opciones: (a) métodos **exactos exponenciales** para `n` pequeño; (b) **heurísticas o aproximaciones** para `n` grande, con la advertencia de que solo pueden afirmar **SÍ** cuando encuentran un certificado, y nunca **NO**. Medición real en este equipo (Python 3.13, peor caso sin poda efectiva):

| n | (n−1)! | nodos explorados | tiempo (s) |
|---|---|---|---|
| 9 | 40 320 | 109 601 | 0,06 |
| 10 | 362 880 | 986 410 | 0,53 |
| 11 | 3 628 800 | 9 864 101 | 4,65 |

El costo se multiplica por **≈ ×10 con cada centro adicional**. Extrapolando, n = 12 tomaría del orden de un minuto y n = 13 unos diez minutos. **Con los 3 centros del correo el método exacto es instantáneo**, pero para una red de 20 o más centros haría falta Held–Karp, programación entera (ILP) o heurísticas.

## 4. Decidibilidad y computabilidad
- **Modelo de cómputo:** **Máquina de Turing determinista**. Para contar operaciones se usa una RAM con costo uniforme, y en §6 se indica el costo en bits cuando importa.
- **Decidible:** el espacio de candidatos es **finito**, con `(n−1)!` ciclos al fijar el inicio. Cada candidato se evalúa en tiempo finito (el verificador), así que enumerarlos todos **siempre termina** y responde SÍ o NO para toda entrada válida. Las entradas inválidas se rechazan con un error explícito y también terminan.
- **Computable ≠ eficiente:** hay un procedimiento efectivo, pero su tiempo de peor caso es superpolinómico en N.
- **Diferencia con un problema numérico (p. ej., N2):** aquí la explosión depende de la **estructura** (`n`), no del **valor** de L ni de los pesos. Los valores solo afectan el costo en bits de las sumas.

## 5. Algoritmo seleccionado y justificación

| Componente | Función | Tipo | Garantía |
|---|---|---|---|
| Verificador | `verificar` | exacto | acepta ⇔ el certificado es una permutación válida con costo ≤ L |
| **Decisión (seleccionado)** | `buscar_exacto`, backtracking con poda | **exacto** | SÍ/NO siempre correcto |
| Optimización (referencia) | `optimo_held_karp`, programación dinámica | exacto | costo mínimo; **no es lo que pide el correo** |
| Heurística (contraste) | `vecino_mas_cercano` / `decidir_heuristico` | **heurístico** | si dice SÍ, es correcto porque el certificado está verificado; **nunca puede decir NO**; sin garantía de optimalidad ni de razón de aproximación en general |
| Reducción | `reducir_ciclo_hamiltoniano` | transformación | HC(G) ⇔ TSP-D(f(G)) |

**Justificación:** el correo pide una respuesta segura («¿existe?») sobre 3 centros. El backtracking exacto es correcto y, a ese tamaño, inmediato. La poda «costo parcial > L» es **segura** porque los pesos son ≥ 0: una extensión nunca reduce el costo. La heurística se incluye para mostrar qué se pierde al usarla: en la instancia `D_TRAMPA` el óptimo es 17 y el vecino más cercano da 23, así que con L = 17 la heurística responde «no concluyente» aunque la respuesta correcta es SÍ.

**Pseudocódigo (decisión exacta):**
```
BUSCAR(D, L):
  camino ← [0]; visitado ← {0}
  EXTENDER(parcial):
    si parcial > L: retornar FALLO                    # poda (pesos ≥ 0)
    si |camino| = n:
        total ← parcial + D[último][0]
        retornar (camino, total) si total ≤ L, si no FALLO
    para v ∉ visitado:
        agregar v; r ← EXTENDER(parcial + D[último][v])
        si r ≠ FALLO: retornar r
        quitar v
    retornar FALLO
  r ← EXTENDER(0); retornar SÍ(r) si r ≠ FALLO, si no NO
```
**Terminación:** cada llamada recursiva agrega un vértice **no visitado**, de modo que la medida «vértices sin visitar» decrece estrictamente y la profundidad es ≤ n. El factor de ramificación es ≤ n − 1. El árbol es finito: tiene a lo sumo `Σₖ (n−1)!/(n−1−k)! ≤ e·(n−1)!` nodos. Con n = 11 se contaron **9 864 101 nodos ≈ e·10!**, lo que coincide con la cota.

## 6. Complejidad Big-O temporal y espacial
Variables: `n` = número de centros; `b` = bits por peso; `N = Θ(n²·b + log L)` = tamaño de la entrada; `W_max` = peso máximo.

| Rutina | Tiempo | Espacio extra |
|---|---|---|
| Validación de la entrada | O(n²) | O(n²) (copia) |
| **Verificador** | **O(n)** operaciones, es decir O(n·(b + log n)) bits; **polinómico en N** | O(n) |
| **Búsqueda exacta (decisión)** | **O(n·(n−1)!) = O(n!)** en el peor caso (≤ e·(n−1)! nodos, O(1) por nodo y O(n) por hoja); superpolinómico en N | O(n) (camino, visitados, pila) |
| Held–Karp (optimización) | O(n²·2ⁿ) | O(n·2ⁿ) |
| Vecino más cercano | O(n²) | O(n) |
| Reducción HC → TSP-D | O(n²) | O(n²) |

*Tamaño del valor frente a tamaño en bits:* L y los pesos solo entran en las sumas y comparaciones, con un costo de O(b + log n) bits cada una. A diferencia de un algoritmo pseudo-polinómico O(L), aquí la explosión **no** depende de la magnitud de L sino de `n`.

## 7. Código, casos de prueba y salida observada
- **Código:** `src/tsp_decision.py` (Python 3.8+, solo biblioteca estándar). Está dividido en **1. Lectura/validación** (`leer_instancia`, `validar_matriz`, `validar_limite`), **2. Procesamiento** (`verificar`, `buscar_exacto`, `optimo_held_karp`, `vecino_mas_cercano`, `reducir_ciclo_hamiltoniano`) y **3. Presentación** (`formatear_resultado`, `main`). Ante una entrada inválida, `main` devuelve el código de salida 2 con un mensaje en stderr.
- **Uso:** `python src/tsp_decision.py [--archivo instancia.json] [--modo ciclo|camino]`

**Pruebas (`tests/test_tsp_decision.py`, unittest, 28 casos):**

| Tipo | Casos |
|---|---|
| Normales | instancia del correo en modo ciclo (SÍ, 15) y en modo camino (SÍ, 7); simetría de la matriz; Held–Karp separado de la decisión; 150 instancias aleatorias con n entre 2 y 7, comparadas contra fuerza bruta y contra Held–Karp; la heurística es correcta cuando dice SÍ; contraejemplo `D_TRAMPA` donde la heurística falla |
| Límite | L = óptimo (SÍ) y L = óptimo − 1 (NO); L = 0; n = 1; n = 2; matriz asimétrica; pesos reales; rotaciones del ciclo |
| Verificador | rechaza certificados cortos, con repeticiones, fuera de rango, con un vértice repetido al final, de tipo `str`/`bool`/`float`, `None`, o con costo > L |
| Reducción | equivalencia exhaustiva en todos los grafos de n = 4 y n = 5; forma simétrica y métrica de la instancia reducida; Petersen → NO; entradas inválidas (n < 3, lazos, vértices fuera de rango, aristas mal formadas, tipos incorrectos) |
| Inválidos | matrices vacías, no cuadradas, negativas, con NaN o ∞, de tipo `str`/`bool`, o con diagonal ≠ 0; L negativo, `str`, `None`, NaN, ∞ o `bool`; JSON mal formado, sin claves, o con `centros` incorrectos |
| Presentación | `main` con la instancia del correo; archivo inválido o inexistente → código 2 |

**Salida observada** (ejecutada en esta sesión con Python 3.13.18; Python 3.8 no estaba disponible aquí, así que conviene volver a correrla en esa versión):

```
$ python3 src/tsp_decision.py
=== C2 · TSP de decisión ===
Centros (n=3): Planta, Quito, Guayaquil
Matriz simétrica: sí | L = 20 | modo: ciclo (regresa al punto de salida)
[Exacto]     Respuesta: SÍ  | recorrido: Planta -> Quito -> Guayaquil -> Planta | costo = 15 | nodos explorados = 3
[Verificador] certificado [0, 1, 2] aceptado: True
[Heurística] vecino más cercano: Planta -> Quito -> Guayaquil -> Planta | costo = 15 | veredicto: SI
[Optimización, solo referencia] óptimo Held–Karp: Planta -> Guayaquil -> Quito -> Planta | costo mínimo = 15

$ python3 src/tsp_decision.py --modo camino
=== C2 · TSP de decisión ===
Centros (n=3): Planta, Quito, Guayaquil
Matriz simétrica: sí | L = 20 | modo: camino (no regresa)
[Exacto]     Respuesta: SÍ  | recorrido: Planta -> Quito -> Guayaquil | costo = 7 | nodos explorados = 3
[Verificador] certificado [0, 1, 2] aceptado: True
[Heurística] vecino más cercano: Planta -> Quito -> Guayaquil | costo = 7 | veredicto: SI
[Optimización, solo referencia] óptimo Held–Karp: Planta -> Quito -> Guayaquil | costo mínimo = 7

$ python3 -m unittest -v tests/test_tsp_decision.py
... (28 líneas «... ok», una por prueba) ...
----------------------------------------------------------------------
Ran 28 tests in 0.181s

OK
```
*Nota:* con n = 3 y una matriz simétrica solo hay **un** ciclo distinto, recorrido en dos sentidos (4 + 3 + 8 = 15). Por eso el óptimo de Held–Karp aparece en el sentido inverso con el mismo costo.

## 8. Conclusión
**Respuesta operativa para Jorge Tapia:** **SÍ.** Existe un recorrido **Planta → Quito → Guayaquil → Planta** de **15 km ≤ 20 km**, con 5 km de holgura, y el verificador independiente lo confirma. Si en realidad no hubiera que regresar a la Planta (lectura del asunto), la respuesta también es SÍ, con 7 km. El problema general (TSP de decisión) es **NP-completo**: está en NP porque un recorrido se verifica en O(n), y es NP-difícil por la reducción polinómica desde Ciclo Hamiltoniano. Es decidible, y la búsqueda exacta termina, pero crece como O(n!). Para el manifiesto actual la solución exacta es inmediata. Si la red crece, habrá que pasar a Held–Karp, ILP o heurísticas, sabiendo que una heurística puede confirmar un **SÍ** pero no un **NO**. **Pendiente:** confirmar con Ruteo que la matriz del código fuente (A2) es la oficial.

---

## Lista de verificación antes de pedir revisión
- [x] El resumen **no cambia** las condiciones del correo (datos, límites, preguntas); las ambigüedades se declaran en §1.2.
- [x] Se dice explícitamente que es una pregunta de **decisión**, y la optimización aparece separada (§2, §5).
- [x] La etiqueta NP-completo está sostenida con pertenencia a NP, el problema de origen (HC), la reducción y su consecuencia práctica (§3).
- [x] No se escribe «NP = no polinómico» (§3.1).
- [x] Se nombra el **modelo de cómputo** (MT determinista) y se justifica la **terminación** (§4, §5).
- [x] Las variables de Big-O están definidas y se distingue el tamaño del valor del tamaño en bits (§6).
- [x] El código valida entradas y separa lectura, procesamiento y presentación (§7).
- [x] Hay pruebas normales, límite e inválidas, y la **salida observada** es la real (Python 3.13.18; volver a ejecutar en 3.8 si el curso lo exige).
- [ ] Alguien distinto al autor la revisó (**falta el nombre del revisor**).

---

## Guion de defensa oral (~2 min)
1. **(15 s) Pregunta.** «Jorge Tapia pregunta si existe al menos un recorrido que visite los centros una vez y vuelva a la Planta sin pasar de 20 km. Es una pregunta Sí/No: la versión de **decisión** del TSP, no la de buscar el más corto».
2. **(15 s) Ambigüedad.** «El asunto dice "ruta hamiltoniana", pero el cuerpo pide regresar al punto de salida. Tomamos la lectura de ciclo y verificamos también la de camino. Además, la matriz solo aparece en el código del simulador, así que la declaramos como supuesto».
3. **(30 s) NP.** «Está en NP porque, si alguien responde que sí, entrega el orden de los centros, y nosotros comprobamos en tiempo lineal que es una permutación y que la suma no supera L. NP significa *verificable* en tiempo polinómico, no "no polinómico"».
4. **(30 s) NP-completo.** «Reducimos Ciclo Hamiltoniano: las aristas del grafo pesan 1, las que no existen pesan 2, y L = n. Un tour de costo n solo puede usar aristas de peso 1, es decir, aristas reales. La construcción es O(n²), y las pruebas la confirman en los 1088 grafos de 4 y 5 vértices. Como esa instancia es simétrica y métrica, la simetría del correo no facilita el problema».
5. **(20 s) Algoritmo y costo.** «Usamos backtracking exacto con poda por presupuesto, que termina porque cada paso agrega un centro no visitado. Su costo es O(n!) en tiempo y O(n) en espacio. Medimos que crece unas diez veces por cada centro: 4,6 s con 11 centros».
6. **(10 s) Heurística.** «El vecino más cercano es O(n²), pero solo puede confirmar un sí. Mostramos una instancia donde falla y el método exacto acierta».
7. **(10 s) Respuesta.** «Sí: Planta → Quito → Guayaquil → Planta, 15 km ≤ 20. El verificador lo acepta y las 28 pruebas pasan».
