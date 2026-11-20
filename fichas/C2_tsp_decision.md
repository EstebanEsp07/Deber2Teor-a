# Ficha C2 · ¿Existe una ruta hamiltoniana dentro del presupuesto?

| Campo | Valor |
|---|---|
| **Grupo de análisis** | C · NP-completo |
| **Correo** | «¿Existe una ruta hamiltoniana dentro del presupuesto?» — Jorge Tapia · Ruteo |
| **Responsable / revisor** | Joshua (@joshdavr) / Elias (@elorgus) |
| **Sprint** | 3 |
| **Rama sugerida** | `feature/joshua-c2` |
| **Código** | `src/c2_tsp.py` |
| **Pruebas** | `tests/test_c2_tsp.py` |
| **Estado** | Pendiente — cabecera y datos del correo cargados; el resto lo completa el responsable |

> Referencia de formato y profundidad: `fichas/P1_alcanzabilidad_bfs.md` y `fichas/N1_isomorfismo_grafos.md`. Al terminar, pasar la lista de verificación de `docs/PLANTILLA_FICHA.md`.

## Notas específicas de este correo (guía, no sustituye a la ficha)
- Evidencia de grupo C: pertenencia a NP (ruta como certificado, verificación `O(n)`) + reducción polinómica desde **Ciclo Hamiltoniano** + consecuencia práctica (ver `docs/FASE_F_decidibilidad_y_limites.md`: `24! ≈ 6,2×10²³`).
- Separar **decisión** («¿existe ruta con costo ≤ L?») de **optimización** («¿cuál es la mejor?»).
- Opcional: comparar búsqueda exacta (instancias pequeñas) con una heurística (p. ej. vecino más cercano) y decir qué garantiza cada una (la heurística no garantiza optimalidad).

## 1. Identificador y resumen (sin cambiar condiciones)
**Texto del correo (literal):** Dada una matriz de distancias y un límite L, decide si existe un orden que visite cada centro exactamente una vez, con costo total ≤ L (versión de decisión de TSP).

**Tarea pedida en el simulador:** Implementa la versión de decisión y separa solución de optimización.

**Datos del correo:**

| Dato | Valor | Nota |
|---|---|---|
| Centros | Planta, Quito, Guayaquil | n = 3 |
| Distancias | matriz simétrica | km |
| Límite | 20 | km |

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
