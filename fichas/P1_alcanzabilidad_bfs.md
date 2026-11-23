# Ficha P1 · Pedidos alcanzables desde la planta

| Campo | Valor |
|---|---|
| **Grupo de análisis** | A · P (algoritmo polinómico conocido) |
| **Correo** | «¿Puede llegar el envío a la zona Norte?» — Daniela Paredes · Planificación |
| **Responsable / revisor** | Esteban (@EstebanEsp07) / Joshua (@joshdavr) |
| **Código** | `src/p1_bfs.py` |
| **Pruebas** | `tests/test_p1_bfs.py` (12 pruebas) |
| **Estado** | Revisado |

## 1. Identificador y resumen (sin cambiar condiciones)
Dada una red de rutas activas, determinar si existe un camino desde la **Planta Durán** hasta la **Zona Norte**.
Datos del correo (aristas dirigidas): Durán→Quito, Durán→Guayaquil, Quito→Norte, Guayaquil→Sur.

## 2. Entrada, salida y restricciones
- **Entrada:** red dirigida `G = (V, E)` como lista de adyacencia; origen `s ∈ V`; destino `t ∈ V`.
- **Salida:** Sí/No. (Extra del código: el camino con menos aristas, si existe.)
- **Restricciones:** `s` y `t` deben pertenecer a `V`; la red es finita; las aristas no tienen peso en este correo.
- **Versión analizada:** **decisión**. Lenguaje `REACH = { ⟨G, s, t⟩ : existe un camino dirigido de s a t en G }`.
- **Supuesto:** los pasillos son **dirigidos** (como en el correo: Quito→Norte no implica Norte→Quito).

## 3. Clasificación y evidencia
**REACH ∈ P.** Evidencia tipo A: algoritmo polinómico conocido (BFS), con tiempo `O(V + E)`, lineal en el tamaño de la entrada.
(Como P ⊆ NP, también está en NP; la clasificación útil es la más fuerte que podemos demostrar: P.)

## 4. Decidibilidad y computabilidad
- **Modelo supuesto:** máquina de Turing determinista (polinomialmente equivalente a una máquina RAM).
- **Función calculada:** `f(G, s, t) ∈ {Sí, No}`, total: está definida para toda entrada válida.
- **Decidible:** sí. El algoritmo **siempre termina** y responde correctamente (ver §5).

## 5. Algoritmo, justificación y garantías
**Elegido: BFS** con arreglo de predecesores. Se prefiere a DFS porque además entrega el camino con **menos aristas**; se prefiere a Dijkstra porque el correo no tiene pesos (Dijkstra aplica en el correo p2).

```
BFS-ALCANZABLE(G, s, t):
  si s ∉ V o t ∉ V: error de entrada
  pred[s] ← s;  cola ← [s]
  mientras cola ≠ ∅:
    u ← extraer frente de cola
    si u = t: reconstruir camino con pred y devolver (Sí, camino)
    para cada v en Adj[u]:
      si v ∉ pred: pred[v] ← u;  encolar v
  devolver No
```
- **Terminación:** cada vértice entra a la cola a lo sumo una vez (se marca en `pred` al encolarlo), así que el `mientras` hace ≤ |V| vueltas; el `para` interno recorre cada lista de adyacencia una sola vez.
- **Corrección (invariante):** `pred` contiene exactamente los vértices descubiertos desde `s`; la cola, los descubiertos aún no expandidos. Si la cola se vacía sin encontrar `t`, el conjunto descubierto es cerrado bajo sucesores y no contiene a `t` ⇒ no hay camino. Si se encuentra `t`, el orden por niveles de BFS garantiza que el camino tiene el mínimo número de aristas.
- **Exacto**, no heurístico ni aproximado.

## 6. Complejidad (V = |V|, E = |E|)
| Recurso | Cota | Motivo |
|---|---|---|
| Tiempo | `O(V + E)` | cada vértice se encola una vez y cada arista se examina una vez |
| Espacio | `O(V)` | `pred` y la cola; la lista de adyacencia es la entrada |

## 7. Implementación, pruebas y salida observada
Lectura (`leer_red`), procesamiento (`camino_bfs`) y presentación (`main`) están separados; la entrada se valida (tipos, aristas mal formadas, nodos inexistentes).

| Tipo | Caso | Resultado esperado |
|---|---|---|
| Normal | Durán → Norte | Sí, `Durán → Quito → Norte` |
| Normal | Quito → Sur | No |
| Normal | Norte → Durán (el sentido importa) | No |
| Normal | A→D directo vs. A→B→C→D | camino de 1 arista |
| Límite | origen = destino | Sí, camino `[origen]` |
| Límite | red con ciclos (A⇄B) y vértice aislado | termina; No |
| Límite | destino que solo aparece como valor en el dict | Sí |
| Límite | cadena de 50 000 aristas | Sí, sin recursión |
| Inválido | nodo inexistente / red vacía | `ValueError` |
| Inválido | `grafo` que no es dict / arista con 3 elementos / entrada no lista | `TypeError` / `ValueError` |

**Reproducir**
```bash
python3 src/p1_bfs.py
python3 -m unittest discover -s tests -v
```
**Salida observada** (`python3 src/p1_bfs.py`)
```
¿Durán alcanza Norte? Sí  [Durán -> Quito -> Norte]
¿Durán alcanza Sur? Sí  [Durán -> Guayaquil -> Sur]
¿Quito alcanza Sur? No  [sin camino]
¿Norte alcanza Durán? No  [sin camino]
```
Las 12 pruebas de `test_p1_bfs.py` pasan (`OK`; las 333 del repo se ejecutaron juntas en 0,05 s).

## 8. Conclusión
Con los datos del correo, **la Zona Norte sí es alcanzable** desde Durán por `Durán → Quito → Norte`. El problema está en P y BFS lo resuelve en tiempo lineal. Si la red tuviera tiempos de viaje, la pregunta de "menor tiempo" pasa a optimización y se resuelve con Dijkstra (correo p2 / Fase B).
