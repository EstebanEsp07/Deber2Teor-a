# Ficha C3 · ¿Bastan k almacenes para cubrir todas las zonas?

| Campo | Valor |
|---|---|
| **Grupo de análisis** | C · NP-completo |
| **Correo** | «¿Bastan k almacenes para cubrir todas las zonas?» — Carla Núñez · Red logística |
| **Responsable / revisor** | Richard (@RichJ-100) / Joshua (@joshdavr) |
| **Sprint** | 3 |
| **Rama sugerida** | `feature/richard-c3` |
| **Código** | `src/c3_vertex_cover.py` |
| **Pruebas** | `tests/test_c3_vertex_cover.py` |
| **Estado** | Pendiente — cabecera y datos del correo cargados; el resto lo completa el responsable |

> Referencia de formato y profundidad: `fichas/P1_alcanzabilidad_bfs.md` y `fichas/N1_isomorfismo_grafos.md`. Al terminar, pasar la lista de verificación de `docs/PLANTILLA_FICHA.md`.

## Notas específicas de este correo (guía, no sustituye a la ficha)
- **Ambigüedad del correo:** el texto habla de «zona cubierta por un almacén propio o vecino» (conjunto dominante), pero la pregunta de datos, el título y el código hablan de **cubrir aristas** (Vertex Cover). **Supuesto sugerido:** Vertex Cover; declararlo explícitamente en la sección 2 y mantenerlo en toda la ficha.
- Evidencia de grupo C: pertenencia a NP (conjunto de ≤ k vértices como certificado, verificación `O(V+E)`) + reducción desde un NP-completo conocido (p. ej. Independent Set/Clique, o 3-SAT) con el argumento de la reducción + consecuencia práctica.
- Verificador **independiente** del algoritmo de búsqueda (función separada); búsqueda por ramificación `O(2ⁿ·(V+E))`.

## 1. Identificador y resumen (sin cambiar condiciones)
**Texto del correo (literal):** Dado un grafo de cobertura y k, decide si existe un conjunto de a lo sumo k almacenes tal que toda zona esté cubierta por un almacén propio o vecino (Vertex Cover).

**Tarea pedida en el simulador:** Incluye un verificador polinomial independiente del algoritmo de búsqueda.

**Datos del correo:**

| Dato | Valor | Nota |
|---|---|---|
| Aristas | A-B, B-C | zonas adyacentes |
| k | 1 | máximo de almacenes |
| Pregunta | ¿Cubre toda arista? | Sí/No |

_(Pendiente: resumen propio sin cambiar condiciones.)_

## 2. Entrada, salida y restricciones
_(Pendiente. Indicar si es decisión u optimización y los supuestos.)_

## 3. Clasificación y evidencia
_(Pendiente. Evidencia del grupo C · NP-completo.)_

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
