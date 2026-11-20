# Ficha N3 · ¿Existe exponente x que produzca h?

| Campo | Valor |
|---|---|
| **Grupo de análisis** | B · NP |
| **Correo** | «¿Existe exponente x que produzca h?» — Paola León · Seguridad TI |
| **Responsable / revisor** | Elias (@elorgus) / Richard (@RichJ-100) |
| **Sprint** | 2 |
| **Rama sugerida** | `feature/elias-n3` |
| **Código** | `src/n3_logaritmo_discreto.py` |
| **Pruebas** | `tests/test_n3_logaritmo_discreto.py` |
| **Estado** | Pendiente — cabecera y datos del correo cargados; el resto lo completa el responsable |

> Referencia de formato y profundidad: `fichas/P1_alcanzabilidad_bfs.md` y `fichas/N1_isomorfismo_grafos.md`. Al terminar, pasar la lista de verificación de `docs/PLANTILLA_FICHA.md`.

## Notas específicas de este correo (guía, no sustituye a la ficha)
- Evidencia de grupo B: certificado `x`, verificación con exponenciación rápida en tiempo polinómico en `log p + log B`.
- Costo de la búsqueda `O(B·log B·M(log p))` vs. costo de verificar; explicar por qué `B` en valor ≠ `log B` en bits.
- Búsqueda y verificador en **funciones separadas**, con pruebas normales, límite (x = 0, x = B) e inválidas (p no primo, B negativo).

## 1. Identificador y resumen (sin cambiar condiciones)
**Texto del correo (literal):** Dados p primo, g, h y B, decide si existe x entre 0 y B tal que g^x ≡ h (mod p). El certificado es x y la exponenciación modular lo verifica eficientemente.

**Tarea pedida en el simulador:** Implementa búsqueda y verificador separado; indica el costo de ambos.

**Datos del correo:**

| Dato | Valor | Nota |
|---|---|---|
| p | 23 | primo |
| g | 5 | base |
| h | 8 | objetivo |
| B | 10 | exponente máximo |

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
