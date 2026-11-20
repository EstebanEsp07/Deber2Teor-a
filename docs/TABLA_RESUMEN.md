# Tabla resumen de los diez casos

Columnas exigidas por el deber: tipo de problema, decidibilidad, algoritmo, complejidad y estrategia exacta/heurística.

- **Completo** = ficha, código y pruebas hechos (pendiente de revisión por pares).
- **Preliminar** = datos tomados del simulador; **el responsable debe validarlos con su propia ficha** antes de que esta tabla pase a «Final».

| ID | Correo | Grupo | Tipo de problema | Decidibilidad | Algoritmo | Complejidad (tiempo / espacio) | Estrategia | Responsable | Estado |
|---|---|---|---|---|---|---|---|---|---|
| P1 | Alcanzabilidad a la Zona Norte | A·P | Decisión (REACH) | Decidible | BFS | `O(V+E)` / `O(V)` | Exacta | Esteban | **Completo** |
| P2 | Ruta de menor tiempo | A·P | Optimización (camino mínimo; decisión asociada: ¿dist ≤ L?) | Decidible | Dijkstra | `O((V+E) log V)` / `O(V)` | Exacta (pesos ≥ 0) | Joshua | Preliminar |
| P3 | Capacidad máxima de despacho | A·P | Optimización (flujo máximo; decisión asociada: ¿flujo ≥ k?) | Decidible | Edmonds–Karp | `O(V·E²)` | Exacta | Joshua | Preliminar |
| N1 | Isomorfismo de redes | B·NP | Decisión (GI) | Decidible | Permutaciones exhaustivas + **verificador** | Búsqueda `O(n!·n²)` / `O(n)`; verificar `O(n²)` / `O(n)` | Exacta (exhaustiva) | Esteban | **Completo** |
| N2 | Factor de N en [2, B] | B·NP | Decisión | Decidible | División exhaustiva | `O(B·M(log N))`; exponencial en bits si B ≈ √N; verificar con una división | Exacta (exhaustiva) | Elias | Preliminar |
| N3 | Logaritmo discreto acotado | B·NP | Decisión | Decidible | Búsqueda con exponenciación modular | `O(B·log B·M(log p))`; verificar polinómico en `log p + log B` | Exacta (exhaustiva) | Elias | Preliminar |
| N4 | Automorfismo no trivial | B·NP | Decisión | Decidible | Permutaciones + verificación | Búsqueda `O(n!·n²)`; verificar `O(n²)` | Exacta (exhaustiva) | Richard | Preliminar |
| C1 | Satisfacer restricciones (SAT, 3-CNF) | C·NPC | Decisión | Decidible | DPLL / retroceso con poda | `O(2ⁿ·m)` enumeración; DPLL mantiene peor caso exponencial; verificar `O(m)` | Exacta (DPLL) | Richard | Preliminar |
| C2 | Ruta que visita cada centro (TSP-decisión) | C·NPC | Decisión (TSP-D) | Decidible | Backtracking / permutaciones | `O(n!·n)`; verificar `O(n)` | Exacta; heurística opcional (vecino más cercano) en instancias grandes | Joshua | Preliminar |
| C3 | Cobertura de zonas con almacenes | C·NPC | Decisión (Vertex Cover) | Decidible | Backtracking / ramificación | `O(2ⁿ·(V+E))`; verificar `O(V+E)` | Exacta; aproximación 2 posible | Richard | Preliminar |

## Observaciones a resolver antes de pasar a «Final»
1. **C3 tiene dos descripciones distintas en el correo.** El texto habla de «zona cubierta por un almacén propio o vecino» (eso es un **conjunto dominante**), pero el título, la pregunta y el código hablan de cubrir **aristas** (Vertex Cover). Ambos son NP-completos, pero la reducción y el verificador cambian. Richard debe escoger una lectura, declararla como supuesto en su ficha y mantenerla.
2. **N2 y N3: Big-O en bits.** Un `O(B)` no es polinómico si `B` se codifica en binario (su tamaño es `log B` bits); por eso la búsqueda es exponencial en el tamaño de la entrada aunque el verificador sea polinómico. Elias debe decirlo explícitamente.
3. **P3: dos argumentos de terminación distintos.** El texto del simulador mezcla el argumento de Ford–Fulkerson (el flujo aumenta ≥ 1 unidad, depende del valor de las capacidades) con el de Edmonds–Karp (`O(V·E²)`, independiente de las capacidades). Joshua debe justificar con la cota de Edmonds–Karp.
4. **P2 y P3 son de optimización**; la clasificación en P se hace sobre su versión de decisión asociada, y eso debe quedar escrito en cada ficha.
5. **«Heurística» solo cuando corresponda:** si se incluye una heurística (p. ej. en C2), la ficha debe decir qué garantiza (nada sobre optimalidad) y qué no, frente a la búsqueda exacta.
