# Ficha N2 · ¿Tiene N un factor en este intervalo?

| Campo | Valor |
|---|---|
| **Grupo de análisis** | B · NP |
| **Correo** | «¿Tiene N un factor en este intervalo?» — Andrés Molina · Seguridad |
| **Responsable / revisor** | Elias (@elorgus) / Richard (@RichJ-100) |
| **Sprint** | 2 |
| **Rama sugerida** | `feature/elias-n2` |
| **Código** | `src/n2_factor.py` |
| **Pruebas** | `tests/test_n2_factor.py` |
| **Estado** | Pendiente — cabecera y datos del correo cargados; el resto lo completa el responsable |

> Referencia de formato y profundidad: `fichas/P1_alcanzabilidad_bfs.md` y `fichas/N1_isomorfismo_grafos.md`. Al terminar, pasar la lista de verificación de `docs/PLANTILLA_FICHA.md`.

## Notas específicas de este correo (guía, no sustituye a la ficha)
- Evidencia de grupo B: certificado `d`, verificador con una división (`O(M(log N))`), y por qué eso **no** prueba que no esté en P ni que sea NP-completo.
- Dejar claro el **tamaño de la entrada en bits**: `N` y `B` ocupan `log N` y `log B` bits; la búsqueda `O(B·M(log N))` es exponencial en el tamaño binario si `B ≈ √N`.
- Implementar la búsqueda y el **verificador como funciones separadas** (puede ser el verificador de la Fase E).

## 1. Identificador y resumen (sin cambiar condiciones)
**Texto del correo (literal):** Dados enteros N y B en binario, decide si N tiene un divisor d con 2 ≤ d ≤ B. Un certificado «sí» es d; se comprueba dividiendo N por d.

**Tarea pedida en el simulador:** Diferencia el tiempo de encontrar un certificado del tiempo de verificarlo.

**Datos del correo:**

| Dato | Valor | Nota |
|---|---|---|
| N | 91 | representación binaria |
| B | 10 | cota superior |
| Certificado | d | d divide N y 2≤d≤B |

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
