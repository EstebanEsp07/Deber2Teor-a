# Ficha C3 · ¿Bastan k almacenes para cubrir todas las zonas? (Vertex Cover)

| Campo | Valor |
|---|---|
| **Grupo de análisis** | C · NP-completo (pertenencia a NP + origen + reducción + consecuencia práctica) |
| **Correo** | «¿Bastan k almacenes para cubrir todas las zonas?» — Carla Núñez · Red logística |
| **Responsable / revisor** | Richard (@RichJ-100) / Elias |
| **Código** | `src/c3_vertex_cover.py` (verificador separado, búsqueda por ramificación, referencia por subconjuntos y la reducción desde 3-SAT) |
| **Pruebas** | `tests/test_c3_vertex_cover.py` (43 pruebas) |
| **Estado** | Revisado |

## 1. Identificador, resumen y supuesto de lectura
**Texto del correo (literal):** «Dado un grafo de cobertura y k, decide si existe un conjunto de a lo sumo k almacenes tal que toda zona esté cubierta por un almacén propio o vecino (Vertex Cover).»

**Resumen sin cambiar condiciones:** dado un mapa de zonas conectadas por corredores y un entero `k`, decidir si se puede escoger a lo sumo `k` zonas de modo que **cada corredor** tenga una zona elegida en al menos uno de sus extremos. Si existe, la selección es el certificado, con un verificador separado de la búsqueda. Datos del correo: aristas A-B y B-C, `k = 1`, pregunta «¿Cubre toda arista?».

**Ambigüedad y lectura elegida (supuesto S1).** El enunciado se contradice: la frase «zona cubierta por un almacén propio o vecino» describe un **conjunto dominante** (cada vértice está en el conjunto o tiene un vecino en él), pero el resto del expediente habla de **cubrir aristas**. Se analiza **Vertex Cover (cobertura de vértices)** y se mantiene en toda la ficha, por estas razones:
- el propio texto cierra con «(Vertex Cover)»;
- el cuerpo del correo pide que «cada corredor» tenga un equipo «en al menos uno de sus extremos» y una selección de no más de `k` zonas «que cubra todos los corredores»;
- la pregunta de datos es «¿Cubre toda arista?» y el mapa del portal se titula «Corredores entre zonas · cobertura de inspección»;
- el código del simulador comprueba `u in elegidos or v in elegidos` para cada arista.

Con los datos del correo la respuesta es la misma en ambas lecturas (`{B}` cubre las dos aristas y además domina A y C), así que esta instancia no las distingue. Si Carla o el profesor prefirieran conjunto dominante, cambiaría el verificador (cada vértice en `S` o con un vecino en `S`) y la reducción de §3.

| ID | Otros supuestos | Por qué |
|---|---|---|
| S2 | El grafo es **simple y no dirigido** (sin lazos, sin aristas repetidas, simétrico). | Un corredor une dos zonas distintas y es el mismo en ambos sentidos. |
| S3 | «A lo sumo `k`» se lee como `≤ k`. | Es lo que dice el texto («a lo sumo k», «no más de k»). |

## 2. Entrada, salida y restricciones
- **Entrada:** el grafo como diccionario de adyacencia (el mismo formato del simulador, con vecinos en lista o tupla, por ejemplo `{'A': ['B'], 'B': ['A', 'C'], 'C': ['B']}`) y `k` entero, `k ≥ 0`.
- **Salida:** Sí/No. (Extra del código: una cobertura de a lo sumo `k` vértices.)
- **Versión analizada:** **decisión**. `VC = { ⟨G, k⟩ : G tiene un conjunto S con |S| ≤ k que toca todas las aristas }`.
- **Versión de optimización (separada):** «¿cuál es el menor `k`?». Se implementa aparte (`cobertura_minima`, probando `k = 0, 1, 2…`); es NP-difícil. La clasificación de esta ficha es la de la versión de decisión.
- **Casos particulares:** sin aristas, `k = 0` ya es Sí (cobertura vacía); si `k ≥ |V|`, siempre es Sí (se eligen todos los vértices). Con los datos del correo: **Sí**, con `S = {B}`.

## 3. Clasificación y evidencia
**Vertex Cover es NP-completo.**

1. **Pertenencia a NP (certificado + verificador).**
   - **Certificado:** el conjunto `S` de a lo sumo `k` vértices.
   - **Verificador** (`verificar_cobertura`, función separada de la búsqueda): comprobar que `S` son vértices distintos del grafo y que `|S| ≤ k`, y que cada arista `(u, v)` cumple `u ∈ S` o `v ∈ S`. Con conjuntos hash cada comprobación es `O(1)`; el total es **`O(V + E)`**, lineal en la entrada.
2. **Problema NP-completo de origen:** **3-SAT** (ficha C1; NP-completo por Cook–Levin más la reducción SAT ≤ₚ 3-SAT). La reducción 3-SAT ≤ₚ Vertex Cover es la clásica de Sipser (cap. 7) y de Karp (1972).
3. **Reducción polinómica `3-SAT ≤ₚ VC`.** Dada una fórmula con `n` variables y `m` cláusulas de exactamente 3 literales (las de menos literales se rellenan repitiendo uno, como en C1), se construye un grafo `G` y `k = n + 2m`:
   - por cada variable `xi`: dos vértices `xi` y `¬xi` unidos por una arista (el «selector» de la variable);
   - por cada cláusula: un triángulo de 3 vértices, y cada vértice del triángulo se une al vértice de variable de su literal.
   - **Tamaño:** `2n + 3m` vértices y `n + 6m` aristas; se construye en tiempo `O(n + m)`: polinómica.
   - **(⇒) satisfacible ⇒ hay cobertura de tamaño `n + 2m`:** de cada selector se elige el vértice del literal verdadero (`n` vértices); en cada triángulo hay un literal verdadero: se deja fuera su vértice y se eligen los otros dos (`2m` vértices). Las aristas de selector, las del triángulo (dos de sus tres vértices están elegidos) y las que salen de los vértices elegidos quedan cubiertas; la arista del vértice dejado fuera va a un vértice de variable verdadero, que sí está elegido.
   - **(⇐) cobertura de tamaño `n + 2m` ⇒ satisfacible:** los `n` selectores y los `m` triángulos son disjuntos y cubrir un selector exige 1 vértice y cubrir un triángulo exige 2; como `n + 2m` es justo el mínimo, la cobertura toma **exactamente** 1 por selector y 2 por triángulo. Se hace `xi = verdadero` si el elegido del selector es `xi`. En cada triángulo queda fuera un vértice; su arista al selector solo se cubre si el vértice de variable de ese literal está elegido, es decir, si el literal es verdadero: la cláusula se cumple.
   - **Verificado en el código:** `reduccion_3sat_a_vertex_cover` implementa la construcción, y las pruebas comprueban «satisfacible ⇔ hay cobertura de tamaño `k`» contra una fuerza bruta propia de la prueba en las 4 096 fórmulas de 2 cláusulas sobre 2 variables y en 40 fórmulas aleatorias de 3 variables.
4. **Consecuencia práctica.** Hasta donde se sabe **no hay un algoritmo polinómico** y **no está demostrado que no pueda haberlo** (P vs NP abierto; esta ficha no afirma P ≠ NP). Operativamente: *comprobar* un despliegue propuesto es barato (`O(V + E)`), pero *encontrar* el menor despliegue puede costar tiempo exponencial. Hay un matiz útil: con `k` pequeño el esfuerzo crece casi linealmente con el tamaño del mapa y explota con `k` (§6), así que desplegar «pocos equipos» en mapas grandes es manejable y exigir una cobertura grande no lo es.

**Qué demuestra y qué no:** NP + reducción desde un NP-completo prueba NP-completitud. «En NP» por sí solo **no** significaría «no polinómico» (P ⊆ NP).

## 4. Decidibilidad y computabilidad
- **Modelo supuesto:** máquina de Turing determinista.
- **Función calculada:** `VC: ⟨G, k⟩ → {Sí, No}`, total: definida para todo grafo válido y todo `k ≥ 0`.
- **Decidible:** sí. Hay solo `2^|V|` subconjuntos de vértices; el algoritmo termina siempre. Que sea decidible **no** implica que sea eficiente: no se conoce algoritmo polinómico.

## 5. Algoritmo seleccionado y justificación
**Ramificación por aristas** (búsqueda exhaustiva con poda por presupuesto): **exacta**, no heurística ni aproximada. Se elige porque cualquier cobertura debe tocar la arista `(u, v)` por `u` o por `v`, lo que reduce el espacio de búsqueda a un árbol binario de profundidad `≤ k` en vez de `2^|V|` subconjuntos.

```
COBERTURA(aristas, k, elegidos):
  si no quedan aristas: devolver elegidos
  si k = 0: devolver No                      # quedan aristas y no hay presupuesto
  (u, v) ← primera arista
  para w en (u, v):
    restantes ← las aristas que NO tocan a w
    r ← COBERTURA(restantes, k − 1, elegidos ∪ {w})
    si r ≠ No: devolver r
  devolver No
```
- **Terminación:** `k` baja en 1 en cada llamada y con `k = 0` se detiene, así que la profundidad es `≤ k`. Además cada `w` elegido es un vértice nuevo (todas sus aristas ya se quitaron), así que la profundidad es `≤ |V|`.
- **Corrección** (por inducción en `k`): si devuelve algo, todas las aristas quitadas tocan un vértice elegido y solo se eligen `≤ k` vértices (*solidez*). Si existe una cobertura `C` de las aristas restantes con `≤ k` vértices y hay alguna arista `(u, v)`, `C` contiene a `u` o a `v`; la rama de ese vértice recibe `C` menos ese vértice, que cubre lo que queda con `≤ k − 1`, y por inducción tiene éxito (*completitud*).
- **Referencia:** `buscar_fuerza_bruta` prueba todos los subconjuntos de tamaño `0..min(k, V)` (`itertools.combinations`) y se usa para contrastar. El código del simulador usa `int.bit_count()`, que solo existe desde Python 3.10; se evitó para respetar la regla de Python 3.8+.
- **Límite del algoritmo:** la ramificación no explota la estructura del grafo; aun en un camino (que tiene estructura sencilla) explora hasta `2^k` ramas (§6, tabla d).

## 6. Complejidad (V = vértices, E = aristas, k = presupuesto)
| Operación | Tiempo | Espacio |
|---|---|---|
| Verificar un certificado | `O(V + E)` | `O(V + E)` (la validación construye conjuntos) |
| Ramificación | `O(V + E + 2^min(k,V) · E)` | `O(min(k,V) · E)` |
| Enumerar subconjuntos (referencia y cota del correo) | `O(2^V · (V + E))` | `O(V)` |

- **Ramificación:** el árbol tiene `≤ 2^(min(k,V)+1) − 1` nodos y cada nodo filtra las aristas en `O(E)`. El espacio es por la lista de aristas restantes que guarda cada nivel (con una pila de deshacer bajaría). La cota `O(2ⁿ·(V+E))` del correo, con `n = V`, también es válida pero más gruesa.
- **Valor vs. tamaño:** la entrada ocupa `Θ(V + E)` más `log k` bits para `k`. El costo depende de `min(k, V)`, no del valor de `k`: un `k = 10⁹` no hace explotar nada porque la profundidad nunca pasa de `V`. En función del tamaño de la entrada, el peor caso (`k ≈ V/2`) es exponencial.

**Medición** (Python 3.12.3, una ejecución en mi entorno; los tiempos dependen de la máquina; grafos aleatorios de `n` vértices y `m = round(1,5 · n)` aristas distintas, semillas 0, 1 y 2, promedio de 3):

**a) Instancias «No» con `k` = mínimo − 1 (se agota la búsqueda): ramificación vs. subconjuntos**

| n | m | cobertura mínima | Ramificación | Subconjuntos |
|---|---|---|---|---|
| 10 | 15 | 6, 5, 5 | < 0,0001 s | 0,0002 s |
| 14 | 21 | 6, 8, 6 | 0,0001 s | 0,0028 s |
| 18 | 27 | 8, 9, 8 | 0,0002 s | 0,0547 s |
| 22 | 33 | 10, 10, 11 | 0,0009 s | 0,683 s |

**b) «Cómo varía el esfuerzo cuando crece el mapa» con `k = 8` fijo** (instancias «No»)

| n | m | Ramificación |
|---|---|---|
| 100 | 150 | 0,0021 s |
| 200 | 300 | 0,0041 s |
| 400 | 600 | 0,0081 s |
| 800 | 1 200 | 0,0165 s |
| 1 600 | 2 400 | 0,0330 s |

Se duplica al duplicar el mapa (crecimiento lineal en `V + E` con `k` fijo).

**c) `n = 60`, `m = 90` fijos y `k` creciente** (instancias «No»)

| k | Ramificación |
|---|---|
| 8 | 0,0011 s |
| 12 | 0,0143 s |
| 16 | 0,2089 s |
| 20 | 2,4856 s |

Cada +4 en `k` multiplica el tiempo por ~12 a 15 (la poda queda por debajo del máximo teórico de ×16): crecimiento exponencial en `k`.

**d) Peor caso estructurado: camino de `2k` vértices con `k` justo** (instancias «Sí»)

| k | n | Ramificación |
|---|---|---|
| 8 | 16 | 0,0002 s |
| 12 | 24 | 0,0017 s |
| 14 | 28 | 0,0071 s |
| 16 | 32 | 0,0302 s |

Es ×4 por cada +2 en `k`, es decir ×2 por vértice de presupuesto: la ramificación básica no ve que un camino tiene una solución trivial.

**e) Verificador** (ciclo de `n` vértices con la mitad de los vértices como cobertura válida)

| n | Verificar |
|---|---|
| 1 000 | 0,7 ms |
| 10 000 | 8,8 ms |
| 100 000 | 129 ms |
| 1 000 000 | 1 731 ms |

En esta medición crece algo por encima de lo lineal (≈×13 por cada ×10 en `n`, probablemente por efectos de memoria con grafos grandes); la cota teórica es `O(V + E)`. Aun así, verificar un millón de zonas tarda menos de 2 s, mientras que buscar con `k = 20` en solo 60 zonas ya tarda ~2,5 s: esa es la asimetría **encontrar vs. verificar**.

Las tablas son pocos puntos y pocas semillas: muestran la tendencia, no demuestran la tasa de crecimiento.

## 7. Implementación, pruebas y salida observada
Validación (`validar_grafo`), verificador (`verificar_cobertura`), búsquedas (`buscar_cobertura`, `buscar_fuerza_bruta`, `cobertura_minima`), reducción (`reduccion_3sat_a_vertex_cover`) y presentación (`main`) están separados. Si el grafo no tiene aristas, la búsqueda devuelve `[]` (lista vacía, que Python trata como falsa), así que el código y las pruebas comparan siempre con `is not None`.

| Tipo | Caso | Resultado esperado |
|---|---|---|
| Normal | caso del correo (A-B, B-C, `k = 1`) | Sí, `['B']`; el verificador la acepta |
| Normal | el correo con `k = 0` | No |
| Normal | triángulo; estrella; ciclo de 5; `K₄`; camino de 4 | mínimos 2, 1, 3, 3, 2; con `k` por debajo, No |
| Normal | **todos** los grafos de 1 a 5 vértices (1 + 2 + 8 + 64 + 1 024), todo `k` de 0 a `n` | la ramificación y la referencia coinciden con el mínimo calculado por definición; cada cobertura devuelta cubre todas las aristas y tiene `≤ k` vértices |
| Normal | 40 grafos aleatorios de 6 a 10 vértices | el Sí/No coincide con el mínimo por definición en `k = mínimo − 1` y `k = mínimo` |
| Límite | grafo vacío `{}`; sin aristas; un vértice aislado | Sí con cobertura `[]` |
| Límite | una sola arista, `k = 0` y `k = 1` | No; Sí |
| Límite | `k ≥ V` (incluido `k = 100`) | Sí |
| Límite | ciclo de 5 con `k = 2` y `k = 3` | No; Sí |
| Límite | vértices de distinto tipo (`1` y `'x'`); resultado reproducible; el grafo no se modifica | correcto |
| Límite | camino de 24 vértices con `k = 12` y `k = 11` | Sí; No |
| Verificador | `['B']`, `('B',)` y `{'A', 'C'}` (con `k = 2`) | acepta |
| Verificador | deja una arista sin cubrir (`['A']`, `['C']`); excede `k`; vértice inexistente; repetidos; tipo incorrecto; elemento no hashable; selección vacía en un grafo con aristas | rechaza |
| Verificador | coberturas válidas que la búsqueda no devolvería primero (`[0, 2]`, `[1, 3]`, `[1, 2]` en un camino de 4) | acepta |
| Reducción | tamaño `2n + 3m` vértices, `n + 6m` aristas, `k = n + 2m` | coincide |
| Reducción | fórmula de C1 rellenada; fórmula insatisfacible de 4 cláusulas | Sí; No |
| Reducción | equivalencia con una fuerza bruta propia: 4 096 fórmulas de 2 cláusulas sobre 2 variables; 40 aleatorias sobre 3 | coincide en todas |
| Inválido | no es diccionario; vecinos que no son lista/tupla; vecino que no es vértice; lazo; no simétrico; vecinos repetidos | `TypeError` / `ValueError` |
| Inválido | `k` negativo; `k` no entero (`1.5`, `"1"`, `None`, `True`) | `ValueError` / `TypeError` |
| Inválido | cláusula de la reducción sin exactamente 3 literales; literal `0`, fuera de rango o no entero | `ValueError` / `TypeError` |

**Reproducir**
```bash
python3 src/c3_vertex_cover.py
python3 -m unittest discover -s tests -v
```
**Salida observada** (`python3 src/c3_vertex_cover.py`, ejecutada en Python 3.12.3)
```
¿Bastan 1 equipo(s) para cubrir A-B y B-C? Sí
Cobertura encontrada: ['B']
Verificador acepta ['B']: True
Verificador acepta ['A'] (B-C queda sin cubrir): False
Verificador acepta ['A', 'C'] con k = 1 (son 2 > k): False
Verificador acepta ['A', 'C'] con k = 2: True
Con k = 0: None
Cobertura mínima (optimización): ['B']
Reducción de C1: grafo de 12 vértices, k = 7 -> Sí (la fórmula es satisfacible)
Reducción de una fórmula insatisfacible: 16 vértices, k = 10 -> No
```
Las 43 pruebas de `test_c3_vertex_cover.py` pasan (`OK`).

## 8. Conclusión
Con los datos del correo, **sí bastan 1 equipo**: la zona `B` toca los corredores A-B y B-C, el verificador acepta `['B']` y rechaza `['A']` (deja B-C sin cubrir) y `['A', 'C']` con `k = 1` (son 2 > `k`). Se analizó **Vertex Cover** (S1) porque el cuerpo del correo, los datos y el código hablan de cubrir corredores. Vertex Cover es **NP-completo**: está en NP (certificado verificable en `O(V + E)`), es NP-difícil por la reducción desde 3-SAT (implementada y probada) y su consecuencia práctica es que verificar un despliegue es barato mientras que encontrar el mínimo puede costar tiempo exponencial: con `k` fijo el esfuerzo crece de forma lineal con el mapa, y con `k` crece exponencialmente. No se afirma que P ≠ NP; es un problema abierto.
