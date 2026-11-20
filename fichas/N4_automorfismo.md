# Ficha N4 · ¿La topología tiene una simetría?

| Campo | Valor |
|---|---|
| **Grupo de análisis** | B · NP |
| **Correo** | «¿La topología tiene una simetría?» — Santiago Jaramillo · Analítica |
| **Responsable / revisor** | Richard (@RichJ-100) / Joshua (@joshdavr) |
| **Sprint** | 2 |
| **Rama sugerida** | `feature/richard-n4` |
| **Código** | `src/n4_automorfismo.py` |
| **Pruebas** | `tests/test_n4_automorfismo.py` |
| **Estado** | Pendiente — cabecera y datos del correo cargados; el resto lo completa el responsable |

> Referencia de formato y profundidad: `fichas/P1_alcanzabilidad_bfs.md` y `fichas/N1_isomorfismo_grafos.md`. Al terminar, pasar la lista de verificación de `docs/PLANTILLA_FICHA.md`.

## Notas específicas de este correo (guía, no sustituye a la ficha)
- Reutilizar `_preserva` y la validación de `src/n1_isomorfismo.py` (caso `A = B`). **Ojo:** la primera permutación que genera `itertools.permutations` es la identidad; hay que saltarla.
- Casos límite: grafo sin simetrías no triviales (hay que probar que ninguna permutación distinta de la identidad preserva), grafos de 1 y 2 vértices.
- Mismo esquema de la ficha N1: certificado, verificador `O(n²)`, búsqueda `O(n!·n²)`.

## 1. Identificador y resumen (sin cambiar condiciones)
**Texto del correo (literal):** Decide si un grafo tiene un automorfismo distinto de la identidad. La permutación de vértices es un certificado y se verifica preservando adyacencias.

**Tarea pedida en el simulador:** Muestra una permutación no identidad o argumenta que no existe.

**Datos del correo:**

| Dato | Valor | Nota |
|---|---|---|
| Grafo | 3 vértices | triángulo |
| Certificado | permutación | no identidad |
| Verificación | comparar pares | adyacencia preservada |

_(Pendiente: resumen propio sin cambiar condiciones.)_

## 2. Entrada, salida y restricciones
_(Pendiente. Indicar si es decisión u optimización y los supuestos.)_

## 3. Clasificación y evidencia
_(Pendiente. Evidencia del grupo B · NP.)_

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
