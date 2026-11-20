# Ficha P2 · Ruta mínima entre centros de distribución

| Campo | Valor |
|---|---|
| **Grupo de análisis** | A · P |
| **Correo** | «Ruta mínima entre centros de distribución» — Marco Cedeño · Transporte |
| **Responsable / revisor** | Joshua (@joshdavr) / Elias (@elorgus) |
| **Sprint** | 2 |
| **Rama sugerida** | `feature/joshua-p2` |
| **Código** | `src/dijkstra.py (compartido con B-03)` |
| **Pruebas** | `tests/test_dijkstra.py` |
| **Estado** | Pendiente — cabecera y datos del correo cargados; el resto lo completa el responsable |

> Referencia de formato y profundidad: `fichas/P1_alcanzabilidad_bfs.md` y `fichas/N1_isomorfismo_grafos.md`. Al terminar, pasar la lista de verificación de `docs/PLANTILLA_FICHA.md`.

## Notas específicas de este correo (guía, no sustituye a la ficha)
- Tipo: **optimización** (camino mínimo). La clasificación en P se hace sobre su **versión de decisión**: «¿existe una ruta con tiempo ≤ L?». Debe quedar escrito.
- Evidencia de grupo A: algoritmo polinómico conocido (Dijkstra), Big-O `O((V+E) log V)` con cola de prioridad; definir V y E.
- Mostrar un **contraejemplo con arista negativa** donde Dijkstra falla y explicar qué invariante se rompe (un vértice «fijado» ya no es definitivo).
- Reconstruir la ruta a CD Guayaquil con el arreglo de predecesores.

## 1. Identificador y resumen (sin cambiar condiciones)
**Texto del correo (literal):** Con tiempos de viaje no negativos, encuentra el tiempo mínimo desde CD Quito hasta cada nodo y reconstruye la ruta a CD Guayaquil.

**Tarea pedida en el simulador:** Codifica Dijkstra. Explica por qué no sirve si hay pesos negativos.

**Datos del correo:**

| Origen | Destino | Tiempo |
|---|---|---|
| Quito | Latacunga | 2 |
| Quito | Ambato | 5 |
| Latacunga | Guayaquil | 6 |
| Ambato | Guayaquil | 3 |

_(Pendiente: resumen propio sin cambiar condiciones.)_

## 2. Entrada, salida y restricciones
_(Pendiente. Indicar si es decisión u optimización y los supuestos.)_

## 3. Clasificación y evidencia
_(Pendiente. Evidencia del grupo A · P.)_

## 4. Decidibilidad y computabilidad
_(Pendiente. Nombrar el modelo de cómputo.)_

## 5. Algoritmo seleccionado y justificación
_(Pendiente. Pseudocódigo, terminación y si es exacto, aproximado o heurístico.)_

## 6. Complejidad Big-O temporal y espacial
_(Pendiente. Definir las variables; distinguir valor vs. tamaño en bits donde aplique.)_

## 7. Código, casos de prueba y salida observada
_(Pendiente. Casos normales, límite e inválidos. La salida debe ser la real, ejecutada por el responsable.)_

## 8. Conclusión
_(Pendiente.)_
