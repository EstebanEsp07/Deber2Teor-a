# Ficha C1 · ¿Hay una asignación que cumpla todas las reglas? (SAT 3-CNF)

| Campo | Valor |
|---|---|
| **Grupo de análisis** | C · NP-completo (pertenencia a NP + origen + reducción + consecuencia práctica) |
| **Correo** | «¿Hay una asignación que cumpla todas las reglas?» — Mónica Ruiz · Planificación |
| **Responsable / revisor** | Richard (@RichJ-100) / Joshua (@joshdavr) |
| **Código** | `src/c1_sat.py` (verificador, fuerza bruta y DPLL) |
| **Pruebas** | `tests/test_c1_sat.py` (31 pruebas) |
| **Estado** | Revisado |

## 1. Identificador, resumen y supuestos
Decidir si una fórmula booleana en forma normal conjuntiva con cláusulas de a lo sumo 3 literales (3-CNF) se puede hacer verdadera con alguna asignación de verdadero/falso a sus variables. Datos del correo: variables `x1, x2, x3` y cláusulas `(x1 ∨ ¬x2)` y `(x2 ∨ x3)`; tarea: codificar un solucionador pequeño y explicar cómo se verifica una asignación candidata.

| ID | Supuesto | Por qué |
|---|---|---|
| S1 | «3-CNF» se lee como **a lo sumo 3 literales por cláusula**. | Las cláusulas del correo tienen **2** literales, no 3. Es equivalente a «exactamente 3» (se rellena repitiendo un literal), así que no cambia la clasificación (§3). |
| S2 | La cláusula **vacía** es falsa; una fórmula **sin cláusulas** es verdadera. | Convención estándar (la disyunción vacía es falsa, la conjunción vacía es verdadera). |
| S3 | Las `n` variables existen aunque no aparezcan en ninguna cláusula; la asignación las incluye todas. | El certificado debe dar valor a cada variable declarada. |

## 2. Entrada, salida y restricciones
- **Entrada:** `n` (número de variables) y una lista de `m` cláusulas; cada cláusula es una lista de a lo sumo 3 literales; el entero `k` significa `xk` y `-k` significa `¬xk` (`0` no es un literal válido). El correo se escribe `n = 3`, `[[1, -2], [2, 3]]`.
- **Salida:** Sí/No. (Extra del código: la asignación que lo demuestra.)
- **Versión analizada:** **decisión**. `SAT3 = { ⟨φ⟩ : existe una asignación que hace verdaderas todas las cláusulas de φ }`.
- **Tamaño de la entrada:** `n + m` (hay a lo sumo `3m` literales). Las cantidades son números pequeños (índices de variable), sin enteros enormes.
- **Nota sobre el dato del correo:** la fórmula del correo es una instancia con solo cláusulas de 2 literales (2-CNF), que sola se resolvería en tiempo polinómico; la etiqueta NP-completo es del **problema general** con cláusulas de hasta 3 literales, no de esa instancia aislada.

## 3. Clasificación y evidencia
**SAT3 es NP-completo.**

1. **Pertenencia a NP (certificado + verificador).**
   - **Certificado:** la asignación `{1: v1, …, n: vn}`; ocupa `n` bits.
   - **Verificador:** comprobar que cada variable `1..n` tiene un booleano (`O(n)`) y que toda cláusula tiene al menos un literal verdadero (como mucho 3 literales por cláusula: `O(m)`). Total **`O(n + m)`**, lineal en la entrada.
2. **Problema NP-completo de origen:** **SAT** (satisfacibilidad de fórmulas en CNF sin límite de literales por cláusula), NP-completo por el **teorema de Cook–Levin** (Cook 1971; Levin 1973). Cook–Levin prueba SAT; la completitud de 3-SAT se obtiene de ahí con la reducción siguiente (Karp 1972).
3. **Reducción polinómica `SAT ≤ₚ SAT3`.** Dada una fórmula `φ`, se construye `φ'` reemplazando cada cláusula `(l₁ ∨ … ∨ lₖ)`:
   - `k ≤ 3`: se deja igual (para «exactamente 3» se rellena repitiendo un literal, `(l₁ ∨ l₁ ∨ l₂)`).
   - `k ≥ 4`: se sustituye por la cadena `(l₁ ∨ l₂ ∨ y₁) ∧ (¬y₁ ∨ l₃ ∨ y₂) ∧ … ∧ (¬y_{k−3} ∨ l_{k−1} ∨ lₖ)`, con variables nuevas `y₁…y_{k−3}` propias de esa cláusula.
   - **Tamaño:** una cláusula de `k` literales produce `k − 2` cláusulas de 3 literales y `k − 3` variables nuevas, así que `|φ'| = O(|φ|)`: la transformación es lineal, por tanto polinómica.
   - **Equisatisfacible (⇒):** si una asignación hace verdadero algún `lᵢ` de la cláusula original, se ponen `y_j = verdadero` para `j ≤ i − 2` y `y_j = falso` para el resto; todas las cláusulas de la cadena se cumplen (la que contiene `lᵢ` por `lᵢ`; las anteriores por su `y` verdadero; las posteriores por su `¬y` verdadero).
   - **Equisatisfacible (⇐):** si todos los `lᵢ` fueran falsos, la 1.ª cláusula obliga `y₁ = verdadero`, la 2.ª obliga `y₂ = verdadero`, y así hasta que la última `(¬y_{k−3} ∨ l_{k−1} ∨ lₖ)` queda falsa: contradicción. Luego si la cadena se cumple, algún `lᵢ` es verdadero.
4. **Consecuencia práctica.** Hasta donde se sabe **no existe un algoritmo polinómico** para SAT3, y **no está demostrado que no pueda existir** (es el problema abierto P vs NP; esta ficha no afirma P ≠ NP). Si alguien lo encontrara, todo NP estaría en P. En términos operativos: *comprobar* un plan propuesto es rápido (`O(n + m)`), pero *encontrar* uno que cumpla todas las reglas puede ser exponencialmente caro en el peor caso; si Planificación codifica sus reglas como SAT, conviene usar un solucionador con tiempo límite y simplificar reglas, sin prometer respuesta rápida en todos los casos.

**Qué demuestra y qué no:** NP + reducción desde un NP-completo prueba NP-completitud. «En NP» por sí solo **no** significaría «no polinómico» (P ⊆ NP).

## 4. Decidibilidad y computabilidad
- **Modelo supuesto:** máquina de Turing determinista.
- **Función calculada:** `SAT3: φ → {Sí, No}`, total: definida para toda fórmula válida.
- **Decidible:** sí. Hay solo `2ⁿ` asignaciones; enumerarlas y verificar cada una siempre termina. Que sea decidible **no** implica que sea eficiente: es un problema **decidible, pero sin algoritmo polinómico conocido** (hasta donde se sabe).

## 5. Algoritmo seleccionado y justificación
**DPLL** (Davis–Putnam–Logemann–Loveland), búsqueda **exacta**: no es heurística ni aproximada, responde Sí/No correctamente. Se implementa en su versión básica: **propagación unitaria + ramificación** (sin eliminación de literales puros ni heurísticas de elección). También se incluye la **enumeración de las `2ⁿ` asignaciones** como referencia.

```
DPLL(F):                                   # F: lista de cláusulas simplificadas
  repetir:                                 # propagación unitaria
    si hay una cláusula con un solo literal l:
      asignar l a verdadero; F ← SIMPLIFICAR(F, l)
      si F es conflicto: devolver falso
    si no: salir del ciclo
  si F no tiene cláusulas: devolver verdadero
  l ← primer literal de la primera cláusula
  para cada elegido en (l, ¬l):            # ramificar
    F' ← SIMPLIFICAR(F, elegido)
    si F' no es conflicto y DPLL(F'): devolver verdadero
  devolver falso

SIMPLIFICAR(F, l):                         # hacer verdadero el literal l
  borrar las cláusulas que contienen l
  quitar ¬l de las demás;  si alguna queda vacía: conflicto
```
- **Terminación:** cada paso (unitario o ramificación) asigna una variable y **elimina todas sus apariciones** de la fórmula; el número de variables distintas baja en 1 en cada paso, así que la profundidad es `≤ n`. Cada nivel hace como mucho 2 ramas, por lo que hay a lo sumo `2^(n+1) − 1` nodos.
- **Corrección:** `SIMPLIFICAR` conserva la satisfacibilidad bajo la asignación hecha; una cláusula vacía es conflicto (S2); la propagación unitaria no pierde soluciones porque un literal solo en su cláusula **debe** ser verdadero; si se prueban `l` y `¬l` y ambos fallan, no hay solución.
- **Por qué DPLL y no solo enumerar:** poda con la propagación y detecta conflictos temprano (§6, medición); pero **no cambia el peor caso**, que sigue siendo exponencial.

## 6. Complejidad (n = variables, m = cláusulas)
| Operación | Tiempo | Espacio |
|---|---|---|
| Verificar una asignación | `O(n + m)` | `O(m)` (la validación copia las cláusulas) |
| Enumeración de `2ⁿ` asignaciones | `O(2ⁿ · (n + m))` | `O(n + m)` |
| DPLL (peor caso, versión del código) | `O(2ⁿ · n · m)` | `O(n · m)` |

**DPLL en detalle:** el árbol tiene `≤ 2^(n+1)` nodos y cada nodo cuesta `O(n · m)` en el peor caso (hasta `n` rondas de propagación, cada una recorre `O(m)`); es una cota gruesa que con estructuras de datos más finas se puede mejorar en el factor polinómico, pero **no** quita el `2ⁿ`. El espacio es `O(n · m)` porque cada nivel guarda una copia de la fórmula simplificada (con una pila de deshacer bajaría a `O(n + m)`). La recursión llega a profundidad `≤ n`; para `n` de miles habría que subir el límite de recursión de Python.

**Valor vs. tamaño:** las únicas cantidades son `n` y `m`, números pequeños; el tamaño de la entrada es `Θ(n + m)` y `2ⁿ` es exponencial en `n`. No hay enteros grandes en juego (no aparece la distinción valor/bits de N2 y N3).

**Medición** (fórmulas 3-CNF aleatorias, 3 variables distintas por cláusula con signo al azar, `m = round(4,26 · n)` —zona difícil, cerca del umbral—; promedio de 5 semillas fijas; tiempos de una ejecución en mi entorno con Python 3.12.3, dependen de la máquina; ambos métodos coinciden en el Sí/No de cada fórmula):

| n | m | Enumeración | DPLL | Fórmulas satisfacibles |
|---|---|---|---|---|
| 10 | 43 | 0,021 s | 0,0001 s | 4 de 5 |
| 14 | 60 | 0,433 s | 0,0003 s | 4 de 5 |
| 16 | 68 | 2,111 s | 0,0005 s | 3 de 5 |
| 18 | 77 | 6,337 s | 0,0005 s | 3 de 5 |

La enumeración crece del orden de ×4 por cada 2 variables más (coherente con `2ⁿ`). Solo DPLL, en instancias más grandes:

| n | m | DPLL | Fórmulas satisfacibles |
|---|---|---|---|
| 30 | 128 | 0,0016 s | 4 de 5 |
| 50 | 213 | 0,0196 s | 5 de 5 |
| 75 | 320 | 0,629 s | 4 de 5 |
| 100 | 426 | 5,954 s | 2 de 5 |

DPLL es mucho más rápido que enumerar con el mismo `n`, pero también se dispara al crecer `n` (de 0,63 s a 5,95 s entre `n = 75` y `n = 100`): es coherente con un peor caso exponencial, **aunque cuatro puntos no prueban la tasa**. **Verificar** una asignación válida sigue siendo lineal: con `m = n` cláusulas tarda ~0,14 ms (`n = 100`), ~1,3 ms (1 000), ~9,5 ms (10 000) y ~99 ms (100 000). Esa es la asimetría **encontrar vs. verificar**.

## 7. Implementación, pruebas y salida observada
Validación (`validar_formula`), verificador (`verificar_asignacion`), búsquedas (`resolver_fuerza_bruta`, `resolver_dpll`) y presentación (`main`, `formatear`) están separados. Para `n = 0` una fórmula satisfacible devuelve `{}` (dict vacío, que Python trata como falso), así que el código y las pruebas comparan siempre con `is not None`.

| Tipo | Caso | Resultado esperado |
|---|---|---|
| Normal | caso del correo `[[1, -2], [2, 3]]` | Sí; la asignación pasa el verificador |
| Normal | fuerza bruta en el correo | primera asignación en el orden F<T: `{1: F, 2: F, 3: V}` |
| Normal | las 8 cláusulas de signos sobre 3 variables | No (insatisfacible) con DPLL y con fuerza bruta |
| Normal | 60 fórmulas aleatorias (n entre 6 y 10, `m = round(4,26 n)`) | DPLL y fuerza bruta coinciden; cada asignación de DPLL cumple todas las cláusulas |
| Normal | principio del palomar (2/1, 3/2, 4/3) | No; con 3 palomas y 3 nidos, Sí |
| Límite | sin cláusulas; `n = 0` y sin cláusulas | Sí (`{}` cuando `n = 0`) |
| Límite | cláusula vacía (S2) | No |
| Límite | variables que no aparecen (n = 5, solo `x1`) | Sí; la asignación incluye las 5 variables (S3) |
| Límite | `[[1], [-1]]`; `[[1,1,1]]`; tautología `[[1,-1]]` | No; Sí; Sí |
| Límite | cadena de 300 implicaciones `x1, x1→x2, …` | Sí, resuelta por propagación sin ramificar |
| Límite | **todas** las fórmulas de 2 cláusulas (a lo sumo 2 literales) sobre 3 variables | DPLL coincide con la fuerza bruta |
| Verificador | asignación válida; la que viola la 1.ª cláusula; la que viola la 2.ª | acepta; rechaza; rechaza |
| Verificador | incompleta, con variables de más, `0` como clave, valores `1`/`0`/`"True"` que no son booleanos, no es `dict` | rechaza |
| Verificador | cláusula vacía; sin cláusulas | rechaza; acepta |
| Inválido | más de 3 literales; literal `0` o fuera de rango | `ValueError` |
| Inválido | literal no entero (`1.5`, `"1"`, `None`, `True`); fórmula que no es lista; `n` no entero | `TypeError` |
| Inválido | cláusula mal formada (`5`, `"x1"`); `n` negativo | `ValueError` |

**Reproducir**
```bash
python3 src/c1_sat.py
python3 -m unittest discover -s tests -v
```
**Salida observada** (`python3 src/c1_sat.py`, ejecutada en Python 3.12.3)
```
Fórmula: (x1 ∨ ¬x2) ∧ (x2 ∨ x3)
¿Satisfacible (DPLL)? Sí
Asignación: {1: True, 2: True, 3: False}
Verificador acepta la asignación: True
Fuerza bruta (primera en el orden F<T): {1: False, 2: False, 3: True}
Candidata {1: False, 2: True, 3: False} -> False
Las 8 cláusulas de signos sobre x1,x2,x3 -> None
```
Las 31 pruebas de `test_c1_sat.py` pasan (`OK`).

## 8. Conclusión
Con los datos del correo, **sí existe una asignación**: `x1 = V, x2 = V, x3 = F` (la encuentra DPLL; el verificador la acepta). La candidata `x1 = F, x2 = V, x3 = F` se rechaza porque viola `(x1 ∨ ¬x2)`. SAT 3-CNF es **NP-completo**: está en NP (certificado verificable en `O(n + m)`), es NP-difícil por la reducción `SAT ≤ₚ SAT3` desde el problema NP-completo de Cook–Levin, y su consecuencia práctica es que verificar un plan es barato pero encontrarlo puede costar tiempo exponencial en el peor caso. No se afirma que P ≠ NP; es un problema abierto.
