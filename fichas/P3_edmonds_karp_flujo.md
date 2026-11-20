# Ficha P3 · Máximo de camiones hacia clientes

| Campo | Valor |
|---|---|
| **Grupo de análisis** | A · P |
| **Correo** | «Máximo de camiones hacia clientes» — Luis Vaca · Distribución |
| **Responsable / revisor** | Joshua (@joshdavr) / Elias (@elorgus) |
| **Sprint** | 2 |
| **Rama sugerida** | `feature/joshua-p3` |
| **Código** | `src/p3_edmonds_karp.py` |
| **Pruebas** | `tests/test_p3_edmonds_karp.py` |
| **Estado** | Pendiente — cabecera y datos del correo cargados; el resto lo completa el responsable |

> Referencia de formato y profundidad: `fichas/P1_alcanzabilidad_bfs.md` y `fichas/N1_isomorfismo_grafos.md`. Al terminar, pasar la lista de verificación de `docs/PLANTILLA_FICHA.md`.

## Notas específicas de este correo (guía, no sustituye a la ficha)
- Tipo: **optimización** (flujo máximo). Versión de decisión asociada: «¿flujo ≥ k?».
- Justificar la terminación con la **cota de Edmonds–Karp `O(V·E²)`**, que no depende del valor de las capacidades. No usar el argumento de Ford–Fulkerson («aumenta ≥ 1 unidad»): depende del valor numérico (ver `TABLA_RESUMEN.md`, observación 3).
- Mostrar los caminos aumentantes que encuentra el algoritmo y el valor final del flujo; comprobar con el corte mínimo.

## 1. Identificador y resumen (sin cambiar condiciones)
**Texto del correo (literal):** Calcula el máximo flujo de camiones por día desde la planta hasta los clientes respetando las capacidades de cada tramo.

**Tarea pedida en el simulador:** Completa/explica el código Edmonds–Karp y calcula el flujo máximo.

**Datos del correo:**

| Origen | Destino | Capacidad |
|---|---|---|
| Planta | Quito | 7 |
| Planta | Guayaquil | 5 |
| Quito | Clientes | 4 |
| Guayaquil | Clientes | 6 |
| Quito | Guayaquil | 2 |

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
