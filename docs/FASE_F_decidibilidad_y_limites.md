# Fase F · Decidibilidad y límites  _(v1.0 · autor: Esteban)_

## 1. Cuatro preguntas distintas
- **Decidibilidad:** ¿existe un algoritmo que, para **toda** entrada válida, termine y responda bien Sí/No? «¿Llega el envío a la Zona Norte?» (P1) es decidible: BFS siempre termina.
- **Computabilidad:** ¿qué función queremos calcular y bajo qué modelo? Usamos la **máquina de Turing determinista** (polinomialmente equivalente a una RAM). Responde *qué* se puede calcular, no cuánto cuesta.
- **Complejidad:** dado un algoritmo, ¿qué tiempo y espacio usa según el tamaño de la entrada? BFS: `O(V+E)`; isomorfismo de grafos por fuerza bruta: `O(n!·n²)`.
- **Práctica:** «decidible» solo garantiza que el algoritmo termina *alguna vez*, no en un tiempo útil para el almacén real.

## 2. Caso límite: decidible pero inviable
**TSP de decisión** (C2): con `n` centros, una matriz de distancias y un límite `L`, ¿hay una ruta que visite cada centro una vez con costo ≤ L?
- **Es decidible:** hay un número finito de rutas (con origen fijo, `(n−1)!`); enumerarlas y comparar con `L` siempre termina. Todo espacio de búsqueda finito se decide por enumeración.
- **Es impracticable:** con `n = 25`, `24! ≈ 6,2×10²³` rutas; incluso a `10⁹` rutas por segundo son `≈ 6,2×10¹⁴ s ≈ 2×10⁷ años`.
- **Verificar es barato:** comprobar una ruta propuesta toma `O(n)`, por eso TSP-decisión está en **NP**. Su NP-completitud se sostiene con una reducción polinómica (p. ej. desde Ciclo Hamiltoniano), no con que sea «difícil». Que no exista algoritmo polinómico **no está demostrado** (`P ≠ NP` sigue abierto): solo no conocemos uno.

## 3. Contraste: «¿este programa arbitrario terminará para toda entrada?»
Es el **problema de la parada**: `HALT_TM = {⟨M,w⟩ : M es una MT y M se detiene con entrada w}`. Turing (1936) demostró su indecidibilidad; en la bibliografía del curso corresponde al **Teorema 4.11** (reducido desde $A_{\text{TM}}$, Teorema 4.11, p. 201) de Sipser, *Introduction to the Theory of Computation* (3.ª ed., Cengage Learning, 2013).
*Idea de la prueba:* si `H` decidiera `HALT_TM`, definimos `D(⟨M⟩)`: si `H(⟨M, ⟨M⟩⟩)` dice «se detiene», `D` entra en bucle; si no, `D` se detiene. Entonces `D(⟨D⟩)` se detiene si y solo si no se detiene: contradicción.

| | TSP finito (C2) | Parada (`HALT_TM`) |
|---|---|---|
| ¿Existe algoritmo que siempre termina? | **Sí** (lento) | **No** |
| Naturaleza del obstáculo | Recursos (tiempo) | Imposibilidad lógica |
| ¿Lo arregla un hardware mejor? | Solo en instancias pequeñas | Nunca |

«Indecidible» no es «muy difícil», y «NP-completo» no es indecidible: es decidible y sin algoritmo polinómico conocido. `HALT_TM` es **semidecidible** (Turing-reconocible): simular confirma que se detiene, pero no puede confirmar que no. Para LOGISTPULSE: no habrá una herramienta que garantice la terminación de **cualquier** programa de planificación, pero sí podemos probarla en algoritmos **concretos** (BFS: cada vértice entra una vez a la cola).
