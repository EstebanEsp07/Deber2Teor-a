# LOGISTPULSE · Decisiones, algoritmos y límites computacionales

Deber de **Teoría de la Computación** · Universidad San Francisco de Quito · Colegio Politécnico.
Equipo de 4 personas. Este repositorio contiene los modelos (autómatas JFLAP, grafo de planta), los algoritmos (rutas, FEFO, reposición), las diez fichas de análisis de los correos del simulador, el código con pruebas reproducibles y el registro de sprints.

## Equipo y contribuciones
Repositorio: <https://github.com/EstebanEsp07/Deber2Teor-a>

| Integrante | GitHub | Rol de coordinación | Responsabilidades principales |
|---|---|---|---|
| **Esteban** | [@EstebanEsp07](https://github.com/EstebanEsp07) | Líder · Coordinación y backlog | Repo, backlog, sprints, retrospectiva, Fase F, tabla resumen, informe PDF, release; fichas P1 y N1 |
| **Elias** | [@elorgus](https://github.com/elorgus) | Formalización | Fase A (3 autómatas JFLAP); verificador de certificado (Fase E); fichas N2 y N3 |
| **Joshua** | [@joshdavr](https://github.com/joshdavr) | Algoritmos y análisis | Fase B (grafo y Dijkstra, con implementación); fichas P2, P3 y C2 |
| **Richard** | [@RichJ-100](https://github.com/RichJ-100) | Implementación y validación | Fase C (FEFO y reposición, con código); fichas N4, C1 y C3 |

_La contribución real de cada integrante se respalda con el historial de commits y Pull Requests del repositorio._

## Plazo y sprints
Entrega: **martes 24 de noviembre de 2026**. Por la fecha, los tres sprints son cortos (detalle en `docs/SPRINTS.md`):
Sprint 1 · 19–20 nov · Sprint 2 · 21–22 nov · Sprint 3 · 23–24 nov.

## Configuración inicial de cada integrante (obligatorio)
Los commits deben salir con la identidad de **tu propia cuenta de GitHub**; así el historial prueba tu contribución.
```bash
git clone https://github.com/EstebanEsp07/Deber2Teor-a.git
cd Deber2Teor-a
git config user.name  "Tu Nombre Apellido"
git config user.email "correo-de-tu-cuenta-de-GitHub"   # o tu correo noreply de GitHub
git checkout -b feature/<tunombre>-<tema>               # p. ej. feature/elias-automatas
# ... trabajas, luego:
git add . && git commit -m "feat: autómata de pedido"
git push -u origin feature/<tunombre>-<tema>            # y abres un Pull Request a main
```
Si el repositorio es privado, GitHub pedirá iniciar sesión (o un token personal) al clonar o hacer push.

## Estructura
```
.
├── README.md
├── src/                     código fuente (un archivo por algoritmo/correo)
├── tests/                   pruebas reproducibles (unittest)
├── fichas/                  una ficha por correo (P1, P2, P3, N1…N4, C1…C3)
├── docs/
│   ├── BACKLOG.md           historias, responsables, dependencias, estado
│   ├── SPRINTS.md           registro de los 3 sprints + retrospectiva
│   ├── PLANTILLA_FICHA.md   plantilla de la ficha obligatoria
│   ├── TABLA_RESUMEN.md     tabla resumen de los 10 casos
│   └── FASE_F_decidibilidad_y_limites.md
├── modelos/                 (pendiente) .jff de JFLAP, diagramas y grafo de planta
└── informe/                 (pendiente) informe PDF final
```

## Cómo ejecutar
Requisitos: Python 3.8 o superior. Sin dependencias externas.
```bash
python3 src/p1_bfs.py                 # demo del correo P1
python3 src/n1_isomorfismo.py         # demo del correo N1 (con verificador)
python3 -m unittest discover -s tests -v   # todas las pruebas
```
Convención: cada algoritmo separa **lectura/validación**, **procesamiento** y **presentación** (`main()`), y se acompaña de pruebas normales, límite e inválidas.

## Flujo de trabajo en Git
- Rama principal: `main` (solo se integra por Pull Request con **al menos una revisión** de otra persona).
- Ramas: `feature/<nombre>-<tema>` (p. ej. `feature/elias-automatas`).
- Commits en presente y con prefijo: `feat:`, `fix:`, `docs:`, `test:` (p. ej. `docs: ficha P1`).
- Cada correo es una unidad de trabajo: **ficha + código + pruebas** en el mismo PR.
- Versión final etiquetada:
```bash
git tag -a v1.0-entrega -m "Entrega Deber 2 · LOGISTPULSE"
git push origin v1.0-entrega
```

## Primer arranque (solo Esteban, una vez)
Descomprimir el ZIP del repo base y, dentro de la carpeta `logistpulse/`:
```bash
git init
git add .
git commit -m "docs: estructura inicial del repositorio"
git branch -M main
git remote add origin https://github.com/EstebanEsp07/Deber2Teor-a.git
git pull origin main --allow-unrelated-histories   # solo si el repo ya tenía un README; resolver conflicto conservando el nuestro
git push -u origin main
```
