# Backlog · LOGISTPULSE

**Plazo:** martes 24 de noviembre de 2026 · Sprint 1: 19–20 nov · Sprint 2: 21–22 nov · Sprint 3: 23–24 nov.
Estados: `Pendiente` · `En curso` · `Borrador` (hecho, falta revisión) · `Revisado` · `Final`.
Cada correo es una historia vinculada a **ficha + código + pruebas** (ver `PLANTILLA_FICHA.md`; fichas pendientes ya creadas con su cabecera en `fichas/`).

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
| G-01 | Repositorio, README, ramas y convenciones | 1 | — | Borrador |
| G-02 | Backlog (este archivo) | 1 | — | Borrador |
| G-03 | Plantillas de ficha y de Pull Request | 1 | — | Borrador |
| G-04 | Registro de sprints (`SPRINTS.md`) | 1–3 | — | Borrador (fechas fijadas) |
| G-05 | Retrospectiva real de cada sprint | 1–3 | Cierre de cada sprint | Pendiente |
| G-06 | Tabla resumen de los 10 casos | 3 | Las 10 fichas | Borrador (2 de 10 completos) |
| G-07 | Informe PDF (ensamblado) | 3 | A, B, C, D, F | Pendiente |
| G-08 | Release etiquetado `v1.0-entrega` | 3 | Todo revisado | Pendiente |
| G-09 | Guion y ensayo de la exposición (8–10 min) | 3 | A, B, C y un caso de complejidad | Pendiente |

## Fases del núcleo obligatorio
| ID | Entregable | Responsable | Sprint | Depende de | Estado |
|---|---|---|---|---|---|
| A-01 | Autómata de **pedido** (Q, Σ, q₀, F, δ) + .jff | Elias | 1 | — | Pendiente |
| A-02 | Autómata de **reserva** + .jff | Elias | 1 | — | Pendiente |
| A-03 | Autómata de **orden de compra** + .jff | Elias | 1 | — | Pendiente |
| A-04 | ≥2 secuencias válidas y ≥2 inválidas por autómata, con la transición que acepta/rechaza | Elias | 2 | A-01…03 | Pendiente |
| B-01 | Grafo ponderado de la planta (dirigido/no, bloqueos, origen/destino AMR) | Joshua | 1 | — | Pendiente |
| B-02 | Pseudocódigo de Dijkstra, terminación y Big-O | Joshua | 2 | B-01 | Pendiente |
| B-03 | Implementación de Dijkstra + pruebas (`src/dijkstra.py`, `tests/test_dijkstra.py`) | Joshua | 2 | B-02 | Pendiente |
| C-01 | Formalización FEFO y reposición (restricciones, desempate, política de faltantes, anti-duplicación) | Richard | 1 | — | Pendiente |
| C-02 | Pseudocódigo final FEFO y reposición, terminación y Big-O | Richard | 2 | C-01 | Pendiente |
| C-03 | Código y pruebas de FEFO y reposición | Richard | 2 | C-02 | Pendiente |
| E-01 | Verificador de certificado (sobre N2 o N3) | Elias | 2 | ficha del caso | Pendiente |
| F-01 | Nota de 1 página: decidibilidad y límites | Esteban | 2–3 | — | Borrador v0.2 |

## Fase D · diez correos (ficha + código + pruebas)
| ID | Correo (remitente) | Grupo | Responsable | Revisor | Sprint | Estado |
|---|---|---|---|---|---|---|
| P1 | Alcanzabilidad a la Zona Norte (Daniela Paredes) | A·P | Esteban | Joshua | 1–2 | **Borrador** (código y 12 pruebas OK) |
| P2 | Ruta mínima entre centros (Marco Cedeño) | A·P | Joshua | Elias | 2 | Pendiente (ficha creada) |
| P3 | Máximo de camiones a clientes (Luis Vaca) | A·P | Joshua | Elias | 2 | Pendiente (ficha creada) |
| N1 | Isomorfismo de redes (Elena Ruiz) | B·NP | Esteban | Elias | 1–2 | **Borrador** (código, verificador y 17 pruebas OK) |
| N2 | ¿N tiene un factor en [2, B]? (Andrés Molina) | B·NP | Elias | Richard | 2 | Pendiente (ficha creada) |
| N3 | Logaritmo discreto acotado (Paola León) | B·NP | Elias | Richard | 2 | Pendiente (ficha creada) |
| N4 | Automorfismo no trivial (Santiago Jaramillo) | B·NP | Richard | Joshua | 2 | Pendiente (ficha creada; reutilizar `_preserva`, saltar la identidad) |
| C1 | SAT 3-CNF (Mónica Ruiz) | C·NPC | Richard | Joshua | 3 | Pendiente (ficha creada) |
| C2 | TSP de decisión (Jorge Tapia) | C·NPC | Joshua | Elias | 3 | Pendiente (ficha creada) |
| C3 | Cobertura de zonas / Vertex Cover (Carla Núñez) | C·NPC | Richard | Joshua | 3 | Pendiente (ficha creada). **Decisión sugerida:** trabajar como Vertex Cover (el título, la pregunta, los datos y el código del correo hablan de cubrir aristas) y declarar el supuesto |

## Revisión por pares
| Revisor | Revisa a | Qué revisa |
|---|---|---|
| Elias | Joshua | Grafo, Dijkstra, P2, P3, C2 |
| Joshua | Richard | FEFO y reposición, N4, C1, C3 y la ficha P1 |
| Richard | Elias | Autómatas, verificador, N2, N3 y la nota de la Fase F |
| Elias | Esteban | Ficha N1 |
| Esteban | Todos | Revisión final antes del release |
