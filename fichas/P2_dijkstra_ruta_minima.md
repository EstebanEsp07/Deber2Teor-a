# Ficha P2 · Ruta mínima entre centros de distribución

| Campo | Valor |
|---|---|
| Grupo de análisis | A·P |
| Correo | «Ruta mínima entre centros de distribución» — Marco Cedeño · Transporte |
| Responsable / revisor | Joshua / Elias |
| Código | `src/dijkstra.py` (compartido con la Fase B, B-03) |
| Pruebas | `tests/test_dijkstra_p2.py` |
| Estado | Revisado |

## 1. Identificador y resumen (sin cambiar condiciones)

**P2 · Ruta de menor tiempo.** El proveedor cambió los tiempos estimados por obras en la vía. Transporte necesita, antes del corte de asignación de vehículos de las 09:00, el **tiempo mínimo desde CD Quito hasta cada nodo** y la **ruta reconstruida a CD Guayaquil**, con su costo total, indicando qué información debe conservar el sistema para reconstruir la ruta. Los tiempos son **no negativos** y algunas conexiones no son directas. Se pide código, una prueba pequeña y, si se considera otra técnica, justificar que sus supuestos aplican.

Datos del expediente (tramos dirigidos, como muestran las flechas del mapa del simulador; tiempos en **unidades del expediente**, porque el correo no indica una unidad):

| Origen | Destino | Tiempo |
|---|---|---|
| Quito | Latacunga | 2 |
| Quito | Ambato | 5 |
| Latacunga | Guayaquil | 6 |
| Ambato | Guayaquil | 3 |

**Respuesta operativa:** el tiempo mínimo de CD Quito a CD Guayaquil es **8 unidades del expediente**. Hay **dos rutas óptimas empatadas**:

- Quito → Latacunga → Guayaquil: 2 + 6 = **8**
- Quito → Ambato → Guayaquil: 5 + 3 = **8**

El programa devuelve **Quito → Latacunga → Guayaquil** (ver §5, «Empate»). Las dos rutas tienen el mismo tiempo. El correo no da un criterio para desempatar, así que la elección entre ellas le corresponde a Transporte.

## 2. Entrada, salida y restricciones

**Lo que pide el correo es un problema de optimización** (camino mínimo de origen único):

- **Entrada:** grafo dirigido G = (V, E, w) con w(u, v) ≥ 0, origen s = CD Quito y destino t = CD Guayaquil.
- **Salida:** `dist[v]` = costo mínimo de s a v para todo v ∈ V (∞ si v no es alcanzable), y la ruta s → t reconstruida con el diccionario de predecesores (o «sin ruta»).
- **Restricciones:** pesos reales, finitos y no negativos; s y t deben pertenecer a V.
- **Información que debe conservar el sistema** (lo que pide el correo): para cada vértice v, su **predecesor** en la ruta mínima (`predecesor[v]`). Con eso, la ruta se reconstruye hacia atrás desde t en O(V). `dist[v]` da el costo.

**Versión de decisión asociada** (es la que se clasifica en P, porque P es una clase de problemas de decisión):

> RUTA-CORTA = { ⟨G, s, t, L⟩ : existe una ruta de s a t con costo ≤ L }

Se responde Sí/No con `existe_ruta_con_costo_max(grafo, s, t, L)`: se calcula `dist[t]` con Dijkstra y se compara con L. En el expediente, con L = 8 la respuesta es Sí y con L = 7 es No.

## 3. Clasificación y evidencia (Grupo A: algoritmo polinómico conocido)

**Clasificación: P** (para la versión de decisión RUTA-CORTA).

**Evidencia:** existe un algoritmo determinista que decide RUTA-CORTA en tiempo polinómico en el tamaño de la entrada. Se ejecuta Dijkstra desde s, en O((V + E) log V) operaciones, y luego una comparación `dist[t] ≤ L`.

- El número de operaciones depende de **V y E** y **no del valor numérico de los pesos ni de L**. A diferencia de N2 o N3, ningún bucle recorre un rango del tamaño de un número. Por eso la cota también es polinómica en bits (ver §6).
- La versión de optimización no está en P en sentido estricto, porque no es un problema de decisión. Pero se resuelve con el mismo algoritmo polinómico, y a partir de ella la versión de decisión es inmediata. Por eso se dice que «el problema es tratable».
- Nota: como P ⊆ NP, RUTA-CORTA también está en NP (el certificado sería la ruta). Pero esa no es la evidencia de este grupo: aquí la evidencia es el algoritmo polinómico. Por la misma razón, el problema **no** es NP-completo, salvo que P = NP.

## 4. Decidibilidad y computabilidad

**Modelo de cómputo supuesto:** máquina RAM determinista con **costo uniforme**. Cada suma, comparación y operación del montículo sobre números de O(log(V·W)) bits cuesta O(1), donde W es el peso máximo. Este modelo se simula con una máquina de Turing determinista con sobrecosto polinómico, así que las conclusiones de decidibilidad y de pertenencia a P valen también en ese modelo.

- **Decidible:** sí. Dijkstra + comparación con L es un algoritmo que **termina para toda entrada válida** y responde correctamente Sí/No. Las entradas inválidas (peso negativo, NaN, ∞, nodo inexistente, L no numérico) se **rechazan con una excepción** y no producen una respuesta falsa.
- **Computable:** sí. La función v ↦ dist(s, v) se calcula con un procedimiento efectivo y finito: los pasos de §5.
- **Terminación:**
  1. Cada vértice se marca como `finalizado` **una sola vez** y no vuelve a relajarse.
  2. Cada iteración del `while` saca una entrada del montículo.
  3. Solo hay inserciones al montículo cuando una relajación mejora `dist[v]`. Cada arco (u, v) se examina una vez, cuando u se finaliza, así que hay a lo sumo **E + 1 inserciones**.
  4. Por tanto, el bucle hace a lo sumo E + 1 iteraciones y termina.
  5. `reconstruir_ruta` también termina, porque cada predecesor tiene una distancia final menor o igual y la cadena acaba en s en a lo sumo V pasos.

## 5. Algoritmo seleccionado y justificación

**Algoritmo: Dijkstra con cola de prioridad (montículo binario).** Es **exacto**, no aproximado ni heurístico: con pesos ≥ 0 devuelve el óptimo verdadero, y lo garantiza el invariante de abajo.

**Por qué Dijkstra y no otra técnica:**

| Técnica | Supuestos | ¿Aplica a P2? |
|---|---|---|
| **Dijkstra** | pesos ≥ 0, origen único | **Sí:** el correo garantiza tiempos no negativos y pide origen único (Quito) |
| Bellman–Ford | admite pesos negativos | Aplica, pero es O(V·E), más lento sin necesidad |
| Floyd–Warshall | todos los pares | Calcula de más: O(V³) cuando el correo solo pide desde Quito |
| BFS | todos los pesos iguales | No aplica: los tiempos son distintos (2, 5, 6, 3) |

**Implementación reutilizada:** `src/dijkstra.py` (Fase B).

- `leer_grafo(TRAMOS_P2, dirigido=True)` lee y valida los datos.
- `dijkstra()` / `ruta_minima()` hacen el procesamiento.
- `existe_ruta_con_costo_max()` resuelve la versión de decisión.
- `main()` presenta los resultados.

**Pseudocódigo:**

```
DIJKSTRA(G, s):
    para todo v en V: dist[v] ← ∞
    dist[s] ← 0 ;  Q ← {(0, s)} ;  F ← ∅          # F = finalizados
    mientras Q ≠ ∅:
        (d, u) ← EXTRAER-MÍNIMO(Q)
        si u ∈ F: continuar                         # entrada obsoleta
        F ← F ∪ {u}
        para cada (v, w) en Adj[u] con v ∉ F:
            si d + w < dist[v]:                     # '<' estricto
                dist[v] ← d + w ;  pred[v] ← u
                INSERTAR(Q, (dist[v], v))
    devolver dist, pred

RUTA-CORTA(G, s, t, L):  devolver DIJKSTRA(G, s).dist[t] ≤ L
```

**Invariante (corrección):** cuando u sale de la cola por primera vez, `dist[u]` es su costo mínimo real. Cualquier otro camino de s a u tiene que pasar por algún vértice x que todavía está en la cola, con `dist[x] ≥ dist[u]`. Como los arcos que quedan pesan ≥ 0, ese camino no puede costar menos que `dist[u]`.

**Por qué falla con pesos negativos:** el invariante usa justamente «los arcos que quedan pesan ≥ 0». Con un arco negativo, un vértice ya finalizado podría mejorar después, y Dijkstra no lo vuelve a procesar.

*Contraejemplo* (`test_contraejemplo_peso_negativo_sin_validar`): arcos Quito→A (1), Quito→B (2), B→A (−2).

- El núcleo sin validar finaliza A con dist = 1.
- La ruta real Quito→B→A cuesta 2 − 2 = **0**.
- Salida observada del núcleo: `{'B': 2, 'A': 1, 'Quito': 0}`, que es incorrecta para A.

Por eso `src/dijkstra.py` **rechaza** cualquier peso negativo en vez de devolver un resultado falso. Si Transporte llegara a tener pesos negativos, habría que usar Bellman–Ford. Este caso no ocurre en P2, porque el correo garantiza tiempos no negativos.

**Empate de costo 8 a Guayaquil, paso a paso:**

1. Se finaliza Quito (0). Se relajan Latacunga = 2 y Ambato = 5.
2. Sale Latacunga (2), que es menor que 5. Se relaja Guayaquil = 2 + 6 = 8, con `pred[Guayaquil] = Latacunga`.
3. Sale Ambato (5). Se prueba 5 + 3 = 8, pero como `8 < 8` es falso, **no se reemplaza** el predecesor.
4. Sale Guayaquil (8) y se finaliza.

El resultado es Quito → Latacunga → Guayaquil. Este desempate **no depende del orden en que se escriben los tramos**, porque Latacunga siempre sale de la cola antes que Ambato (2 < 5). Lo comprueba `test_desempate_no_depende_del_orden_de_entrada`. Si se usara `≤`, el programa reportaría la ruta por Ambato. **El costo mínimo, 8, es el mismo con cualquiera de las dos reglas.** Ambas rutas son óptimas y el algoritmo es exacto en el costo, no en la elección entre rutas empatadas.

## 6. Complejidad Big-O temporal y espacial

**Variables:**

- V = número de vértices (centros); en el expediente, V = 4.
- E = número de arcos dirigidos; en el expediente, E = 4. Si el grafo no fuera dirigido, cada tramo contaría como 2 arcos.
- W = peso máximo.
- n = tamaño de la entrada en bits: n = Θ((V + E)·(log V + log W)), porque cada arco codifica dos vértices y un peso.

**Tiempo**, en el modelo RAM de costo uniforme:

- Validación (`_validar_grafo` / `leer_grafo`): O(V + E).
- Inicialización de `dist`: O(V).
- Montículo: a lo sumo E + 1 inserciones y extracciones, cada una en O(log E) = O(log V), porque E ≤ V² ⇒ log E ≤ 2 log V.
- Recorrido de las listas de adyacencia: O(E) en total.
- Reconstrucción de la ruta: O(V).
- **Total: O((V + E) log V)**. La versión de decisión solo agrega una comparación O(1).

**Tamaño en bits:** el número de operaciones **no depende de W ni de L**. Cada distancia es ≤ (V − 1)·W, así que ocupa O(log V + log W) bits. En el modelo de costo por bit, cada operación aritmética cuesta O(log V + log W), y el total es O((V + E) log V · (log V + log W)). Eso es **polinómico en n**. Este es el punto que distingue a P2 de N2/N3: allí el bucle recorre un rango de B valores, y B es exponencial en log B, su tamaño en bits.

**Espacio:**

- Grafo: O(V + E).
- `dist`, `predecesor`, `finalizado`: O(V).
- Montículo con borrado perezoso: O(E) entradas como máximo.
- **Total: O(V + E).**

## 7. Código, casos de prueba y salida observada

Código: `src/dijkstra.py` (sin cambios respecto a la Fase B). Pruebas nuevas para P2: `tests/test_dijkstra_p2.py`.

| Tipo | Prueba | Entrada | Esperado |
|---|---|---|---|
| Normal | `test_distancias_desde_quito` | TRAMOS_P2, s = Quito | Quito 0, Latacunga 2, Ambato 5, Guayaquil 8 |
| Normal | `test_ruta_reportada_a_guayaquil` | s = Quito, t = Guayaquil | (8, Quito→Latacunga→Guayaquil) |
| Normal | `test_empate_de_costo_8` | ambas rutas, con un verificador independiente | las dos cuestan 8 |
| Normal | `test_desempate_no_depende_del_orden_de_entrada` | tramos en orden inverso | misma ruta por Latacunga |
| Normal | `test_version_de_decision` | L = 8 / L = 7 | True / False |
| Límite | `test_origen_igual_a_destino` | Quito → Quito | (0, [Quito]) |
| Límite | `test_sin_ruta_en_sentido_contrario` | Guayaquil → Quito (arcos dirigidos) | (inf, None); decisión False incluso con L = 10⁹ |
| Límite | `test_peso_cero_permitido` | un tramo con peso 0 | se acepta y el costo es 6 |
| Inválido | `test_rechaza_peso_negativo` | peso −1 | `ValueError` |
| Inválido | `test_rechaza_pesos_no_validos` | `"5"`, `True`, NaN, ∞ | `TypeError` / `ValueError` |
| Inválido | `test_rechaza_nodo_inexistente` | destino «Cuenca» | `ValueError` |
| Inválido | `test_rechaza_limite_no_numerico` | L = `"8"` | `TypeError` |
| §5 | `test_contraejemplo_peso_negativo_sin_validar` | Quito→A 1, Quito→B 2, B→A −2 | el núcleo da dist[A] = 1 (la respuesta real es 0) |

**Salida observada**, ejecutada con Python 3.13.18 y pytest 9.1.1 el 20-11-2026.

`python src/dijkstra.py` (sección P2 de `main()`):

```
== Correo P2 · desde CD Quito ==
  tiempo mínimo a Quito: 0
  tiempo mínimo a Latacunga: 2
  tiempo mínimo a Ambato: 5
  tiempo mínimo a Guayaquil: 8
  ruta a Guayaquil: costo 8  [Quito -> Latacunga -> Guayaquil]
```

Mensaje al rechazar un peso negativo:

```
ValueError: peso negativo en ('Quito', 'Ambato') = -1: Dijkstra exige pesos >= 0 (usar Bellman–Ford en ese caso)
```

`python3 -m unittest tests.test_dijkstra_p2 -v`:

```
test_contraejemplo_peso_negativo_sin_validar (tests.test_dijkstra_p2.TestDijkstraP2.test_contraejemplo_peso_negativo_sin_validar) ... ok
test_desempate_no_depende_del_orden_de_entrada (tests.test_dijkstra_p2.TestDijkstraP2.test_desempate_no_depende_del_orden_de_entrada) ... ok
test_distancias_desde_quito (tests.test_dijkstra_p2.TestDijkstraP2.test_distancias_desde_quito) ... ok
test_empate_de_costo_8 (tests.test_dijkstra_p2.TestDijkstraP2.test_empate_de_costo_8) ... ok
test_origen_igual_a_destino (tests.test_dijkstra_p2.TestDijkstraP2.test_origen_igual_a_destino) ... ok
test_peso_cero_permitido (tests.test_dijkstra_p2.TestDijkstraP2.test_peso_cero_permitido) ... ok
test_rechaza_limite_no_numerico (tests.test_dijkstra_p2.TestDijkstraP2.test_rechaza_limite_no_numerico) ... ok
test_rechaza_nodo_inexistente (tests.test_dijkstra_p2.TestDijkstraP2.test_rechaza_nodo_inexistente) ... ok
test_rechaza_peso_negativo (tests.test_dijkstra_p2.TestDijkstraP2.test_rechaza_peso_negativo) ... ok
test_rechaza_pesos_no_validos (tests.test_dijkstra_p2.TestDijkstraP2.test_rechaza_pesos_no_validos) ... ok
test_ruta_reportada_a_guayaquil (tests.test_dijkstra_p2.TestDijkstraP2.test_ruta_reportada_a_guayaquil) ... ok
test_sin_ruta_en_sentido_contrario (tests.test_dijkstra_p2.TestDijkstraP2.test_sin_ruta_en_sentido_contrario) ... ok
test_version_de_decision (tests.test_dijkstra_p2.TestDijkstraP2.test_version_de_decision) ... ok

----------------------------------------------------------------------
Ran 13 tests in 0.006s

OK
```

## 8. Conclusión

- El tiempo mínimo de CD Quito a CD Guayaquil es **8 unidades del expediente**. Hay dos rutas óptimas empatadas: por Latacunga (2 + 6) y por Ambato (5 + 3). El programa reporta la ruta por Latacunga por su regla de desempate (`<` estricto). Transporte puede asignar el camión refrigerado por cualquiera de las dos sin perder tiempo.
- Desde Quito, los tiempos mínimos son: Latacunga 2, Ambato 5, Guayaquil 8.
- Para reconstruir la ruta, el sistema debe guardar el **predecesor de cada nodo** además de su distancia.
- La versión de decisión RUTA-CORTA está en **P**: Dijkstra la decide en O((V + E) log V), un tiempo polinómico también en bits. El problema es **decidible**, y el algoritmo es **exacto** y siempre termina.
- La garantía depende de que los pesos sean **no negativos**, como asegura el correo. Si hubiera pesos negativos, Dijkstra podría dar un resultado falso (contraejemplo en §5), y por eso el código los rechaza y remite a Bellman–Ford.

---

## Lista de verificación antes de pedir revisión
- [x] El resumen **no cambia** las condiciones del correo (datos, límites, preguntas). Los tiempos están en «unidades del expediente».
- [x] Se dice explícitamente si es **decisión** u **optimización**: el correo pide optimización y P se aplica a RUTA-CORTA.
- [x] La etiqueta P está **sostenida con la evidencia que corresponde** al grupo A: un algoritmo polinómico conocido.
- [x] No se escribe «NP = no polinómico»: NP es *verificable* en tiempo polinómico.
- [x] Hay **modelo de cómputo** nombrado (RAM de costo uniforme, con nota sobre el costo por bit) y se justifica la **terminación**.
- [x] Las variables de Big-O están definidas (V, E, W, n), y se distingue el tamaño del valor del tamaño en bits.
- [x] El código valida entradas y separa lectura / procesamiento / presentación.
- [x] Hay pruebas normales, límite e inválidas, y la **salida observada** es la real. Falta volver a ejecutarla en el repositorio del equipo.
- [ ] Alguien distinto al autor la revisó (falta el nombre en el campo «revisor»).
