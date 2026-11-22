# LOGISTPULSE · Decisiones, algoritmos y límites computacionales

Deber de **Teoría de la Computación** · Universidad San Francisco de Quito · Colegio Politécnico.  
Equipo de 4 personas. Este repositorio contiene los modelos formales (autómatas en JFLAP y grafo ponderado de planta), los algoritmos operativos (rutas mínimas, selección FEFO y regla de reposición), las diez fichas de análisis de los correos del simulador, el código ejecutable con pruebas reproducibles y el registro de gestión por sprints.

---

## Equipo y contribuciones
Repositorio: <https://github.com/EstebanEsp07/Deber2Teor-a>

| Integrante | GitHub | Rol de coordinación | Responsabilidades principales |
|---|---|---|---|
| **Esteban** | [@EstebanEsp07](https://github.com/EstebanEsp07) | Líder · Coordinación y backlog | Gestión del repositorio, backlog, sprints, retrospectiva, Fase F, tabla resumen, informe PDF, release final y exposición; fichas `P1` y `N1` |
| **Elias** | [@elorgus](https://github.com/elorgus) | Formalización | Fase A (3 autómatas en JFLAP `.jff`, tablas y secuencias); verificador de certificado (Fase E); fichas `N2` y `N3` |
| **Joshua** | [@joshdavr](https://github.com/joshdavr) | Algoritmos y análisis | Fase B (grafo de planta y Dijkstra con implementación); fichas `P2`, `P3` y `C2` |
| **Richard** | [@RichJ-100](https://github.com/RichJ-100) | Implementación y validación | Fase C (FEFO y reposición con implementación); fichas `N4`, `C1` y `C3` |

_La contribución real de cada integrante se respalda con el historial de commits, revisiones cruzadas y Pull Requests en este repositorio._

---

## Plazo y planificación de sprints
Entrega: **martes 24 de noviembre de 2026**.  
Debido a la ventana de trabajo disponible desde el inicio del proyecto, los tres sprints se organizaron en ciclos cortos de 2 días (detalle, evidencias y retrospectivas en `docs/SPRINTS.md`):

- **Sprint 1 (19–20 nov 2026):** Modelado formal de autómatas (Fase A), grafo de planta (Fase B) y reglas de FEFO/reposición (Fase C).
- **Sprint 2 (21–22 nov 2026):** Implementación de algoritmos, pruebas unitarias, verificadores de certificado (Fase E), fichas `P1–P3` y `N1–N4`, y revisión cruzada por pares.
- **Sprint 3 (23–24 nov 2026):** Fichas NP-completas `C1–C3`, consolidación de `TABLA_RESUMEN.md`, nota de límites computacionales (Fase F), ensamblado del informe PDF y publicación del release `v1.0-entrega`.

---

## Estructura del repositorio

```text
.
├── README.md
├── .gitignore
├── docs/
│   ├── BACKLOG.md                           # Historias, responsables, revisores y dependencias
│   ├── SPRINTS.md                           # Registro de los 3 sprints, revisiones y retrospectivas
│   ├── PLANTILLA_FICHA.md                   # Estructura estándar de las fichas de análisis
│   ├── TABLA_RESUMEN.md                     # Consolidado comparativo de los 10 correos
│   ├── FASE_A_automatas.md                  # Definición formal y pruebas de autómatas
│   ├── FASE_B_grafo_planta_dijkstra.md      # Grafo ponderado de planta y análisis de Dijkstra
│   ├── FASE_C_fefo_reposicion.md            # Reglas operativas FEFO y punto de pedido
│   └── FASE_F_decidibilidad_y_limites.md    # Nota sobre decidibilidad, computabilidad y parada
├── fichas/
│   ├── P1_alcanzabilidad_bfs.md             # Grupo P · Alcanzabilidad en planta (BFS)
│   ├── P2_dijkstra_ruta_minima.md           # Grupo P · Ruta de costo mínimo (Dijkstra)
│   ├── P3_flujo_maximo_edmonds_karp.md      # Grupo P · Flujo máximo en red (Edmonds–Karp)
│   ├── N1_isomorfismo_grafos.md             # Grupo NP · Isomorfismo de subredes
│   ├── N2_factor_entero.md                  # Grupo NP · Factorización acotada
│   ├── N3_logaritmo_discreto.md             # Grupo NP · Logaritmo discreto acotado
│   ├── N4_automorfismo.md                   # Grupo NP · Automorfismo no trivial
│   ├── C1_sat_3cnf.md                       # Grupo NP-completo · Satisfacibilidad 3-CNF
│   ├── C2_tsp_decision.md                   # Grupo NP-completo · Ruta de reparto (TSP decisión)
│   └── C3_vertex_cover.md                   # Grupo NP-completo · Cobertura de zonas (Vertex Cover)
├── modelos/
│   ├── pedido.jff                           # Autómata ciclo de vida del pedido (JFLAP)
│   ├── reserva.jff                          # Autómata ciclo de vida de la reserva (JFLAP)
│   └── orden_compra.jff                     # Autómata ciclo de vida de orden de compra (JFLAP)
├── src/
│   ├── fase_a_automatas.py                  # Simulación y validación de transiciones (Fase A)
│   ├── dijkstra.py                          # Ruta mínima en planta (Fase B y P2)
│   ├── fefo.py                              # Asignación de inventario FEFO (Fase C)
│   ├── reposicion.py                        # Cálculo de punto de pedido y sugerencia (Fase C)
│   ├── p1_bfs.py                            # Correo P1 · BFS
│   ├── flujo_maximo.py                      # Correo P3 · Edmonds–Karp
│   ├── n1_isomorfismo.py                    # Correo N1 · Verificador y búsqueda de isomorfismo
│   ├── n2_factor.py                         # Correo N2 · Verificador y búsqueda de factor
│   ├── n3_logaritmo_discreto.py             # Correo N3 · Verificador y búsqueda de logaritmo discreto
│   ├── n4_automorfismo.py                   # Correo N4 · Verificador y búsqueda de automorfismo
│   ├── c1_sat.py                            # Correo C1 · Verificador y solver DPLL para 3-CNF
│   ├── tsp_decision.py                      # Correo C2 · Verificador y búsqueda para TSP decisión
│   └── c3_vertex_cover.py                   # Correo C3 · Verificador y búsqueda para Vertex Cover
├── tests/
│   ├── test_fase_a_automatas.py
│   ├── test_dijkstra.py
│   ├── test_dijkstra_p2.py
│   ├── test_fefo.py
│   ├── test_reposicion.py
│   ├── test_p1_bfs.py
│   ├── test_flujo_maximo.py
│   ├── test_n1_isomorfismo.py
│   ├── test_n2_factor.py
│   ├── test_n3_logaritmo_discreto.py
│   ├── test_n4_automorfismo.py
│   ├── test_c1_sat.py
│   ├── test_tsp_decision.py
│   └── test_c3_vertex_cover.py
└── informe/                                 # Carpeta destinada al informe PDF final de entrega
```

---

## Requisitos y ejecución

### Requisitos
- **Python 3.8 o superior** (utiliza únicamente la biblioteca estándar de Python, sin dependencias externas).
- **JFLAP** (para abrir y verificar los archivos `.jff` ubicados en `modelos/`).

### Ejecutar toda la suite de pruebas
Desde la raíz del repositorio:
```bash
python3 -m unittest discover -s tests -v
```

### Ejecutar módulos individuales
Cada archivo en `src/` separa **lectura/validación de entrada**, **procesamiento algorítmico** y **presentación** (`main()`). Puedes ejecutar cualquiera de ellos directamente:
```bash
python3 src/dijkstra.py
python3 src/fefo.py
python3 src/reposicion.py
python3 src/p1_bfs.py
python3 src/flujo_maximo.py
python3 src/n1_isomorfismo.py
python3 src/n2_factor.py
python3 src/n3_logaritmo_discreto.py
python3 src/n4_automorfismo.py
python3 src/c1_sat.py
python3 src/tsp_decision.py
python3 src/c3_vertex_cover.py
```

---

## Flujo de trabajo en Git y versión final
- **Rama principal:** `main` (integrada mediante Pull Requests con revisión cruzada por pares y revisión final de coordinación).
- **Ramas de desarrollo:** `feature/<integrante>-<tema>`.
- **Convención de commits:** `feat:`, `fix:`, `docs:`, `test:`, `chore:`.
- **Etiqueta de entrega final:**
```bash
git tag -a v1.0-entrega -m "Entrega Deber 2 · LOGISTPULSE"
git push origin v1.0-entrega
```
