# Registro de sprints

**Plazo de entrega:** martes **24 de noviembre de 2026** (confirmar la hora límite en el espacio del curso).
**Equipo:** Esteban (@EstebanEsp07, líder) · Elias (@elorgus) · Joshua (@joshdavr) · Richard (@RichJ-100).

> **Nota de planificación.** El deber pide tres sprints semanales, pero el plazo real desde el arranque (jueves 19) hasta la entrega (martes 24) son 6 días. Se ejecutan **tres sprints cortos de ~2 días**, conservando los objetivos y la evidencia que el deber fija para cada uno. Si el docente lo pide, se aclara en la exposición.

| Sprint | Fechas | Objetivo (del deber) |
|---|---|---|
| **1** | Jue 19 – Vie 20 nov | Modelar pedidos, reservas y compras con autómatas; definir el grafo de planta y casos de ruta |
| **2** | Sáb 21 – Dom 22 nov | Desarrollar Dijkstra, pseudocódigo FEFO y regla de reposición; analizar terminación y Big-O |
| **3** | Lun 23 – Mar 24 nov | Analizar los diez correos, conectar decidibilidad/computabilidad/P-NP y presentar resultados |

La exposición (8–10 min) se agenda según indique el docente.

## Ceremonias (15 min cada una, por llamada o presencial)
| Cuándo | Qué | Quién |
|---|---|---|
| Jue 19 (hoy) | **Planificación Sprint 1**: confirmar clones, identidad de Git, ramas y reparto | Todos |
| Vie 20 (noche) | **Revisión + retrospectiva Sprint 1** y planificación Sprint 2 | Todos |
| Dom 22 (noche) | **Revisión + retrospectiva Sprint 2** y planificación Sprint 3 | Todos |
| Lun 23 (noche) | **Congelar contenido**: todo en `main`, revisado | Todos |
| Mar 24 (mañana) | **Entrega**: PDF, release `v1.0-entrega`, enlace subido al curso | Esteban |

Evidencia de cada sprint = enlaces a commits/PR + nombre del revisor.

---
## Sprint 1 · Jue 19 – Vie 20 nov
**Evidencia esperada (deber):** diagramas de estados y grafo con entradas, eventos y supuestos.

| Historia | Responsable | Resultado esperado al cierre (Vie 20) | Estado |
|---|---|---|---|
| G-01…G-04 Repo, backlog, plantillas, registro | Esteban | Repo publicado con la estructura base | Borrador listo |
| P1, N1 (adelantados) | Esteban | Ficha + código + pruebas (29 pruebas OK) | Borrador listo |
| A-01…A-03 Autómatas en JFLAP | Elias | 3 .jff + tablas de δ | Pendiente |
| B-01 Grafo de planta y casos de ruta | Joshua | Diagrama del grafo con supuestos | Pendiente |
| C-01 Formalización FEFO/reposición | Richard | Restricciones, desempate y política de faltantes definidos | Pendiente |

**Impedimentos:** _(completar el vie 20)_
**Retrospectiva Sprint 1** _(completar el vie 20)_
- Qué funcionó: _
- Qué mejorar: _
- Acuerdos para el Sprint 2: _

---
## Sprint 2 · Sáb 21 – Dom 22 nov
**Evidencia esperada (deber):** pruebas, pseudocódigo y complejidades **revisados por pares**.

| Historia | Responsable | Revisor | Resultado esperado al cierre (Dom 22) | Estado |
|---|---|---|---|---|
| A-04 Secuencias válidas/inválidas | Elias | Richard | ≥2 válidas y ≥2 inválidas por autómata | Pendiente |
| E-01 Verificador de certificado | Elias | Richard | Función separada + pruebas | Pendiente |
| B-02, B-03 Dijkstra | Joshua | Elias | Pseudocódigo, Big-O, código y pruebas | Pendiente |
| C-02, C-03 FEFO y reposición | Richard | Joshua | Pseudocódigo final, código y pruebas | Pendiente |
| Fichas N2, N3 | Elias | Richard | Ficha + código + pruebas | Pendiente |
| Fichas P2, P3 | Joshua | Elias | Ficha + código + pruebas | Pendiente |
| Ficha N4 | Richard | Joshua | Ficha + código + pruebas | Pendiente |
| F-01 Nota de decidibilidad (v0.3) | Esteban | Richard | Revisada | Borrador v0.2 |
| Revisión de P1 y N1 | Esteban | Joshua (P1), Elias (N1) | Fichas revisadas | Pendiente |

**Impedimentos:** _
**Retrospectiva Sprint 2**
- Qué funcionó: _
- Qué mejorar: _
- Acuerdos para el Sprint 3: _

---
## Sprint 3 · Lun 23 – Mar 24 nov (entrega)
**Evidencia esperada (deber):** release del informe, código, modelos JFLAP y retrospectiva.

| Historia | Responsable | Revisor | Resultado esperado | Estado |
|---|---|---|---|---|
| Fichas C1, C3 | Richard | Joshua | Ficha + código + pruebas | Pendiente |
| Ficha C2 | Joshua | Elias | Ficha + código + pruebas | Pendiente |
| G-06 Tabla resumen final | Esteban | Todos | 10 casos completos | Borrador |
| G-07 Informe PDF | Esteban | Todos | PDF ensamblado | Pendiente |
| G-08 Release `v1.0-entrega` | Esteban | Todos | Tag publicado | Pendiente |
| G-09 Guion y ensayo de la exposición | Todos | — | ~2 min por persona | Pendiente |
| Subida al espacio del curso | Esteban | — | Enlace al repo + PDF + .jff + diagramas + código + datos de prueba | Pendiente |

**Impedimentos:** _
**Retrospectiva final**
- Qué funcionó: _
- Qué mejorar: _
- Qué haríamos distinto: _
