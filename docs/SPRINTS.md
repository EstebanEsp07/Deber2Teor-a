# Registro de sprints

**Plazo de entrega:** martes **24 de noviembre de 2026** (confirmar la hora límite en el espacio del curso).  
**Equipo:** Esteban (@EstebanEsp07, líder) · Elias (@elorgus) · Joshua (@joshdavr) · Richard (@RichJ-100).

> **Nota de planificación.** El deber pide tres sprints semanales, pero el plazo real desde el arranque (jueves 19) hasta la entrega (martes 24) son 6 días. Se ejecutan **tres sprints cortos de ~2 días**, conservando los objetivos y la evidencia que el deber fija para cada uno. Si el docente lo pide, se aclara en la exposición.

| Sprint | Fechas | Objetivo (del deber) |
|---|---|---|
| **1** | Jue 19 – Vie 20 nov | Modelar pedidos, reservas y compras con autómatas; definir el grafo de planta y casos de ruta |
| **2** | Sáb 21 – Dom 22 nov | Desarrollar Dijkstra, pseudocódigo FEFO y regla de reposición; analizar terminación y Big-O |
| **3** | Dom 22 – Mar 24 nov | Analizar los diez correos, conectar decidibilidad/computabilidad/P-NP y presentar resultados |

La exposición (8–10 min) se agenda según indique el docente.

## Ceremonias (15 min cada una, por llamada o presencial)
| Cuándo | Qué | Quién |
|---|---|---|
| Jue 19 | **Planificación Sprint 1**: confirmar clones, identidad de Git, ramas y reparto | Todos |
| Vie 20 (noche) | **Revisión + retrospectiva Sprint 1** y planificación Sprint 2 | Todos |
| Dom 22 (noche) | **Revisión + retrospectiva Sprint 2** y integración de PRs (`#1`, `#3`–`#7`) | Todos |
| Lun 23 (noche) | **Congelar contenido**: todo en `main`, revisado | Todos |
| Mar 24 (mañana) | **Entrega**: PDF, release `v1.0-entrega`, enlace subido al curso | Esteban |

Evidencia de cada sprint = enlaces a commits/PR + nombre del revisor (o revisión en reunión cuando aplique a archivos base).

---
## Sprint 1 · Jue 19 – Vie 20 nov
**Evidencia esperada (deber):** diagramas de estados y grafo con entradas, eventos y supuestos.

| Historia | Responsable | Revisor / Evidencia | Resultado esperado al cierre | Estado |
|---|---|---|---|---|
| G-01…G-04 Repo, backlog, plantillas, registro | Esteban | Equipo (commit inicial `19 nov`) | Repo publicado con la estructura base | Revisado |
| P1, N1 (adelantados) | Esteban | Revisión en reunión de equipo (base `19 nov`, sin PR) | Ficha + código + pruebas | Revisado |
| A-01…A-03 Autómatas en JFLAP | Elias | Richard (integrado en PR `#6`, `22 nov`) | 3 .jff + tablas de δ | Revisado |
| B-01 Grafo de planta y casos de ruta | Joshua | Elias (commits `21 nov` y PR `#7`, `22 nov`) | Diagrama del grafo con supuestos | Revisado |
| C-01 Formalización FEFO/reposición | Richard | Joshua (integrado en PR `#1`, `22 nov`) | Restricciones, desempate y política de faltantes definidos | Revisado |

**Impedimentos:** el plazo real (6 días) no alcanza para tres sprints semanales, por lo que se acortaron a ~2 días (nota de planificación). Las figuras del deber dejaron dos ambigüedades de modelado (`Cancelado` dibujado sin doble círculo en la Figura 2; `Recepción parcial` limitada a una sola entrega), declaradas como supuestos y diferidas a confirmación en el Sprint 2.  
**Retrospectiva Sprint 1**  
- Qué funcionó: adelantar P1 y N1 dio dos fichas completas que sirvieron de ejemplo para la plantilla; declarar los supuestos de las Fases A–C por escrito evitó decidir a ciegas.  
- Qué mejorar: la revisión de los archivos base y de P1/N1 se hizo en reunión, sin PR ni rastro; `SPRINTS.md` y `BACKLOG.md` no se actualizaron al ritmo del trabajo.  
- Acuerdos para el Sprint 2: integrar por Pull Request con revisor nombrado (PR `#1`, `#3`–`#7`) y confirmar las decisiones pendientes de la Fase A.  

---
## Sprint 2 · Sáb 21 – Dom 22 nov
**Evidencia esperada (deber):** pruebas, pseudocódigo y complejidades **revisados por pares**.

| Historia | Responsable | Revisor | Evidencia / Notas | Resultado esperado al cierre (Dom 22) | Estado |
|---|---|---|---|---|---|
| A-04 Secuencias válidas/inválidas | Elias | Richard | PR `#6` (`22 nov`) | ≥2 válidas y ≥2 inválidas por autómata | Revisado |
| E-01 Verificador de certificado | Elias | Richard | PR `#6` (`22 nov`) / código en repo | Función separada + pruebas | Revisado |
| B-02, B-03 Dijkstra | Joshua | Elias / Esteban | Commits `21 nov`, PR `#7` y ajustes/renombres (`22 nov`) | Pseudocódigo, Big-O, código y pruebas | Revisado |
| C-02, C-03 FEFO y reposición | Richard | Joshua | PR `#1` (`22 nov`) | Pseudocódigo final, código y pruebas | Revisado |
| Fichas N2, N3 | Elias | Richard | Revisado por Richard (`22 nov`) | Ficha + código + pruebas | Revisado |
| Fichas P2, P3 | Joshua | Elias / Esteban | PR `#7` y limpieza/revisión de docs (`22 nov`) | Ficha + código + pruebas | Revisado |
| Ficha N4 | Richard | Elias | PR `#3` (`22 nov`) | Ficha + código + pruebas | Revisado |
| F-01 Nota de decidibilidad | Esteban | Equipo | Revisado y actualizado (`22 nov`) | Revisada | Revisado |
| Revisión de P1 y N1 | Esteban | Reunión de equipo | Revisión conjunta realizada (`22 nov`) | Fichas revisadas | Revisado |

**Impedimentos:** el repositorio mezclaba `pytest` y `unittest` aunque el README prometía solo biblioteca estándar (la salida de P2 mostraba pytest); la integración de los PR se concentró el `22 nov`, lo que dejó poco margen de revisión.  
**Retrospectiva Sprint 2**  
- Qué funcionó: la revisión cruzada entre pares (cada autor fue revisado por otro integrante) y el uso de PR como evidencia.  
- Qué mejorar: repartir las integraciones a lo largo del sprint en lugar de concentrarlas en el último día; nombrar al revisor al crear cada ficha.  
- Acuerdos para el Sprint 3: unificar las pruebas en `unittest`, limpiar el repositorio y congelar el contenido el lunes 23 por la noche.  

---
## Sprint 3 · Dom 22 – Mar 24 nov (entrega)
**Evidencia esperada (deber):** release del informe, código, modelos JFLAP y retrospectiva.

| Historia | Responsable | Revisor | Evidencia / Notas | Resultado esperado | Estado |
|---|---|---|---|---|---|
| Fichas C1, C3 | Richard | Joshua (C1) / Elias (C3) | PR `#4` (C1) y PR `#5` (C3), integrados `22 nov` | Ficha + código + pruebas | Revisado |
| Ficha C2 | Joshua | Elias / Esteban | PR `#7` y revisión de documento (`22 nov`) | Ficha + código + pruebas | Revisado |
| Estándar de pruebas y limpieza | Esteban | Todos | Migración `pytest` → `unittest` y `README` (`22 nov`) | Suite unificada y repo limpio | Revisado |
| G-06 Tabla resumen final | Esteban | Todos | Generada y actualizada (`docs/TABLA_RESUMEN.md`) | 10 casos completos | Borrador |
| G-07 Informe PDF | Esteban | Todos | Generado y regenerado con los registros actualizados (`informe/Informe_LOGISTPULSE.pdf`) | PDF ensamblado | Borrador |
| G-08 Release `v1.0-entrega` | Esteban | Todos | — | Tag publicado | Pendiente |
| G-09 Guion y ensayo de la exposición | Todos | — | — | ~2 min por persona | Pendiente |
| Subida al espacio del curso | Esteban | — | — | Enlace al repo + PDF + .jff + diagramas + código + datos de prueba | Pendiente |

**Impedimentos:** el correo C3 era ambiguo («almacén propio o vecino» describe un conjunto dominante, pero los datos y la pregunta piden cubrir aristas): se trabajó como Vertex Cover y se declaró el supuesto. Al ensamblar el informe se detectaron inconsistencias entre fichas y registros (responsable erróneo en P2/P3, salida de P2 con pytest, conteos de pruebas obsoletos, frases «este chat» y estados sin actualizar), ya corregidas.  
**Retrospectiva final**  
- Qué funcionó: contrastar cada ficha con su código y sus pruebas (333 pruebas OK y salidas idénticas a las documentadas) y la revisión final previa a la entrega.  
- Qué mejorar: mantener `SPRINTS.md` y `BACKLOG.md` al día en cada cierre de sprint y pegar las salidas de ejecución desde el repositorio del equipo.  
- Qué haríamos distinto: fijar desde el inicio un único marco de pruebas (`unittest`), asignar revisor al crear cada ficha y revisar los archivos base por PR en vez de en reunión.
