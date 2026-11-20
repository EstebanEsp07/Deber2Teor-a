# Ficha C1 · ¿Hay una asignación que cumpla todas las reglas?

| Campo | Valor |
|---|---|
| **Grupo de análisis** | C · NP-completo |
| **Correo** | «¿Hay una asignación que cumpla todas las reglas?» — Mónica Ruiz · Planificación |
| **Responsable / revisor** | Richard (@RichJ-100) / Joshua (@joshdavr) |
| **Sprint** | 3 |
| **Rama sugerida** | `feature/richard-c1` |
| **Código** | `src/c1_sat.py` |
| **Pruebas** | `tests/test_c1_sat.py` |
| **Estado** | Pendiente — cabecera y datos del correo cargados; el resto lo completa el responsable |

> Referencia de formato y profundidad: `fichas/P1_alcanzabilidad_bfs.md` y `fichas/N1_isomorfismo_grafos.md`. Al terminar, pasar la lista de verificación de `docs/PLANTILLA_FICHA.md`.

## Notas específicas de este correo (guía, no sustituye a la ficha)
- Evidencia de grupo C: pertenencia a NP (asignación como certificado, verificación `O(m)`) + problema NP-completo de origen (SAT por **Cook–Levin**, y la reducción SAT → 3-SAT para la forma 3-CNF) + consecuencia práctica.
- Solucionador exacto: retroceso/DPLL con poda; enumeración directa `O(2ⁿ·m)`.
- Pruebas: fórmula satisfacible, insatisfacible, cláusula vacía, sin cláusulas, variables que no aparecen.

## 1. Identificador y resumen (sin cambiar condiciones)
**Texto del correo (literal):** Modelo SAT: asigna valores verdadero/falso a variables de decisión para satisfacer simultáneamente las restricciones de despacho (fórmula 3-CNF).

**Tarea pedida en el simulador:** Codifica un solucionador pequeño y explica cómo se verifica una asignación candidata.

**Datos del correo:**

| Dato | Valor | Nota |
|---|---|---|
| Variables | x1, x2, x3 | decisiones |
| Cláusulas | (x1∨¬x2) | (x2∨x3) |
| Pregunta | ¿Hay asignación? | SAT |

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
