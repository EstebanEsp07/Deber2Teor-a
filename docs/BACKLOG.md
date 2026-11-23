# Backlog · LOGISTPULSE

**Plazo:** martes 24 de noviembre de 2026 · Sprint 1: 19–20 nov · Sprint 2: 21–22 nov · Sprint 3: 23–24 nov.
Estados: `Pendiente` · `En curso` · `Borrador` (hecho, falta revisión) · `Revisado` · `Final`.
Cada correo es una historia vinculada a **ficha + código + pruebas** (ver `PLANTILLA_FICHA.md`; fichas creadas en `fichas/`).

## Equipo
| Integrante | GitHub | Rol |
|---|---|---|
| Esteban | @EstebanEsp07 | Líder · Coordinación y backlog |
| Elias | @elorgus | Formalización |
| Joshua | @joshdavr | Algoritmos y análisis |
| Richard | @RichJ-100 | Implementación y validación |

## Gestión y entrega (Esteban)
| ID | Entregable | Sprint | Depende de | Estado |
|---|---|---|---|---|
| G-01 | Repositorio, README, ramas y convenciones | 1 | — | Revisado (base `19 nov` + limpieza `22 nov`) |
| G-02 | Backlog (este archivo) | 1 | — | Revisado |
| G-03 | Plantillas de ficha y de Pull Request | 1 | — | Revisado |
| G-04 | Registro de sprints (`SPRINTS.md`) | 1–3 | — | Revisado |
| G-05 | Retrospectiva real de cada sprint | 1–3 | Cierre de cada sprint | Borrador (notas de S1–S3 completadas; el equipo debe confirmarlas) |
| G-06 | Tabla resumen de los 10 casos (`docs/TABLA_RESUMEN.md`) | 3 | Las 10 fichas | Borrador (10 de 10 casos; actualizada) |
| G-07 | Informe PDF (`informe/Informe_LOGISTPULSE.pdf`) | 3 | A, B, C, D, F | Borrador (regenerado con `SPRINTS.md` y `BACKLOG.md` actualizados) |
| G-08 | Release etiquetado `v1.0-entrega` | 3 | Todo revisado | Pendiente |
| G-09 | Guion y ensayo de la exposición (8–10 min, ~2 min/persona) | 3 | A, B, C y un caso de complejidad | Pendiente |

## Fases del núcleo obligatorio
| ID | Entregable | Responsable | Sprint | Depende de | Estado |
|---|---|---|---|---|---|
| A-01 | Autómata de **pedido** (Q, Σ, q₀, F, δ) + .jff | Elias | 1 | — | Revisado (PR `#6`) |
| A-02 | Autómata de **reserva** + .jff | Elias | 1 | — | Revisado (PR `#6`) |
| A-03 | Autómata de **orden de compra** + .jff | Elias | 1 | — | Revisado (PR `#6`) |
| A-04 | ≥2 secuencias válidas y ≥2 inválidas por autómata, con la transición que acepta/rechaza | Elias | 2 | A-01…03 | Revisado (PR `#6`) |
| B-01 | Grafo ponderado de la planta (dirigido/no, bloqueos, origen/destino AMR) | Joshua | 1 | — | Revisado (PR `#7`) |
| B-02 | Pseudocódigo de Dijkstra, terminación y Big-O | Joshua | 2 | B-01 | Revisado (PR `#7`) |
| B-03 | Implementación de Dijkstra + pruebas (`src/dijkstra.py`, `tests/test_dijkstra.py`) | Joshua | 2 | B-02 | Revisado (PR `#7`) |
| C-01 | Formalización FEFO y reposición (restricciones, desempate, política de faltantes, anti-duplicación) | Richard | 1 | — | Revisado (PR `#1`) |
| C-02 | Pseudocódigo final FEFO y reposición, terminación y Big-O | Richard | 2 | C-01 | Revisado (PR `#1`) |
| C-03 | Código y pruebas de FEFO y reposición | Richard | 2 | C-02 | Revisado (PR `#1`) |
| E-01 | Verificador de certificado (sobre N2 o N3) | Elias | 2 | ficha del caso | Revisado (PR `#6`) |
| F-01 | Nota de 1 página: decidibilidad y límites | Esteban | 2–3 | — | Revisado (`22 nov`) |

## Fase D · diez correos (ficha + código + pruebas)
| ID | Correo (remitente) | Grupo | Responsable | Revisor | Sprint | Estado |
|---|---|---|---|---|---|---|
| P1 | Alcanzabilidad a la Zona Norte (Daniela Paredes) | A·P | Esteban | Equipo (reunión) | 1–2 | Revisado (`19 nov` / `22 nov`) |
| P2 | Ruta mínima entre centros (Marco Cedeño) | A·P | Joshua | Elias / Esteban | 2 | Revisado (PR `#7`) |
| P3 | Máximo de camiones a clientes (Luis Vaca) | A·P | Joshua | Elias / Esteban | 2 | Revisado (PR `#7`) |
| N1 | Isomorfismo de redes (Elena Ruiz) | B·NP | Esteban | Equipo (reunión) | 1–2 | Revisado (`19 nov` / `22 nov`) |
| N2 | ¿N tiene un factor en [2, B]? (Andrés Molina) | B·NP | Elias | Richard | 2 | Revisado (`22 nov`) |
| N3 | Logaritmo discreto acotado (Paola León) | B·NP | Elias | Richard | 2 | Revisado (`22 nov`) |
| N4 | Automorfismo no trivial (Santiago Jaramillo) | B·NP | Richard | Elias | 2 | Revisado (PR `#3`) |
| C1 | SAT 3-CNF (Mónica Ruiz) | C·NPC | Richard | Joshua | 3 | Revisado (PR `#4`) |
| C2 | TSP de decisión (Jorge Tapia) | C·NPC | Joshua | Elias / Esteban | 3 | Revisado (PR `#7`) |
| C3 | Cobertura de zonas / Vertex Cover (Carla Núñez) | C·NPC | Richard | Elias | 3 | Revisado (PR `#5`, trabajado como Vertex Cover) |

## Revisión por pares (ejecutada)
| Revisor | Revisó a | Qué revisó |
|---|---|---|
| Elias | Joshua | Grafo, Dijkstra, P2, P3, C2 (con apoyo de Esteban) |
| Elias | Richard | N4 (PR `#3`) y C3 (PR `#5`) |
| Joshua | Richard | FEFO y reposición (PR `#1`) y C1 (PR `#4`) |
| Richard | Elias | Autómatas, verificador (PR `#6`), N2 y N3 |
| Equipo (reunión) | Esteban | P1, N1, archivos base (G-01…G-04) y nota de la Fase F |
| Esteban | Todos | Migración a `unittest`, limpieza de repo y revisión final pre-release |
