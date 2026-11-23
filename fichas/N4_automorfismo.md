# Ficha N4 · ¿La topología tiene una simetría?

| Campo | Valor |
|---|---|
| **Grupo de análisis** | B · NP (pertenencia a NP por certificado) |
| **Correo** | «¿La topología tiene una simetría?» — Santiago Jaramillo · Analítica |
| **Responsable / revisor** | Richard (@RichJ-100) / Elias|
| **Código** | `src/n4_automorfismo.py` (incluye el **verificador**; reutiliza `src/n1_isomorfismo.py`) |
| **Pruebas** | `tests/test_n4_automorfismo.py` (21 pruebas) |
| **Estado** | Revisado |

## 1. Identificador y resumen (sin cambiar condiciones)
Decidir si un grafo tiene un automorfismo distinto de la identidad, es decir, una permutación de los vértices que preserve las adyacencias y no sea la identidad. La permutación es el certificado y se verifica comparando pares de vértices. Datos del correo: grafo de 3 vértices (triángulo); tarea: mostrar una permutación no identidad o argumentar que no existe.

## 2. Entrada, salida y restricciones
- **Entrada:** un grafo `G` **simple y no dirigido** (supuesto explícito, el mismo de N1), dado como matriz de adyacencia `n × n`, 0/1, simétrica, diagonal en 0.
- **Salida:** Sí/No. (Extra del código: el certificado `p`.)
- **Versión analizada:** **decisión**. `NTA = { ⟨G⟩ : existe una permutación p de {0..n-1}, p ≠ id, con A[i][j] = A[p[i]][p[j]] ∀ i, j }`.
- **Es el caso `A = B` del isomorfismo (N1)** con la condición extra `p ≠ identidad`. Sin esa condición la respuesta sería siempre Sí (la identidad es automorfismo de todo grafo).
- **Casos pequeños:** para `n = 0` y `n = 1` solo existe la identidad, así que la respuesta es **No**; para `n = 2` siempre es **Sí** (el intercambio `(1, 0)` es automorfismo, haya arista o no).
- **Instancia del correo:** triángulo `K₃`. Tiene `3! = 6` automorfismos, 1 identidad y 5 no triviales, así que la respuesta es **Sí**.

## 3. Clasificación y evidencia
**NTA ∈ NP** (evidencia tipo B: certificado + verificador polinómico).
- **Certificado «Sí»:** la permutación `p` (una lista de `n` enteros: `O(n log n)` bits).
- **Verificador:** (1) comprobar que `p` es una permutación de `{0..n-1}`: `O(n)`; (2) comprobar `A[i][j] = A[p[i]][p[j]]` para todo `i, j`: `O(n²)`; (3) comprobar `p ≠ identidad`: `O(n)`. Total **`O(n²)` tiempo, `O(n)` espacio**, lineal en el tamaño de la entrada (`Θ(n²)` bits).
- **Qué demuestra y qué no:** que exista un certificado corto y verificable en tiempo polinómico demuestra `NTA ∈ NP`. **No** demuestra que NTA no esté en P (todo problema de P también tiene verificador), ni que sea NP-completo.
- **Respuesta «No»:** para afirmar que **no** existe simetría no conocemos un certificado corto; hay que agotar las permutaciones. Por eso la ficha solo afirma pertenencia a NP, no a co-NP.
- **Estado conocido:** hasta donde sabemos, no se conoce un algoritmo polinómico general para este problema ni una prueba de que sea NP-completo; Babai (2016) da un resultado cuasi-polinómico para isomorfismo de grafos, que no usamos y no cambia esta clasificación. Existen variantes con una restricción extra (p. ej., automorfismos sin puntos fijos) que sí se demostraron NP-completas, pero no son el problema del correo. _(Verificar y citar las referencias exactas en el informe.)_

## 4. Decidibilidad y computabilidad
- **Modelo supuesto:** máquina de Turing determinista.
- **Función calculada:** `NTA: G → {Sí, No}`, total: está definida para toda matriz válida.
- **Decidible:** sí. Hay solo `n!` permutaciones posibles; el algoritmo las recorre y termina siempre. Que sea decidible **no** implica que sea eficiente (§6).

## 5. Algoritmo seleccionado y justificación
**Búsqueda exhaustiva de permutaciones** saltando la identidad; cada candidata se comprueba con el **mismo verificador** que valida un certificado (buscar = enumerar + verificar). Es **exacta** (no heurística ni aproximada): responde Sí/No correctamente.

```
BUSCAR-AUTOMORFISMO-NO-TRIVIAL(A):
  validar A;  n ← tamaño de A
  para cada permutación p de {0..n-1}:
    si p = identidad: continuar
    si VERIFICAR(A, p): devolver (Sí, p)
  devolver No

VERIFICAR(A, p):
  si p no es permutación de {0..n-1}: devolver falso
  si no (∀ i, j: A[i][j] = A[p[i]][p[j]]): devolver falso
  devolver (p ≠ identidad)
```
- **Terminación:** el `para` recorre un conjunto finito de `n!` permutaciones, cada una verificada en `O(n²)` tiempo finito.
- **Corrección:** si existe un automorfismo no trivial, es una de las `n!` permutaciones, no es la identidad, y `VERIFICAR` lo acepta; si ninguna candidata pasa, no existe. Para `n ≤ 1` el ciclo no devuelve nada y la respuesta es No, que es correcta.
- **Por qué se salta la identidad comparando:** `itertools.permutations` genera la identidad primero, pero el código la compara en vez de asumir ese orden.
- **Por qué no algo más sofisticado:** el objetivo del correo es separar «encontrar» de «verificar»; una búsqueda con poda por grados u órbitas no cambiaría la clasificación pedida.

## 6. Complejidad (n = número de vértices)
| Operación | Tiempo | Espacio |
|---|---|---|
| Verificar un certificado | `O(n²)` | `O(n)` |
| Búsqueda exhaustiva (peor caso: grafo sin simetrías) | `O(n! · n²)` | `O(n)` (las permutaciones se generan de a una) |

**Valor vs. tamaño:** aquí `n` es el número de vértices y la entrada ocupa `Θ(n²)` bits, así que `n!` es **superpolinómico en el tamaño de la entrada**. No hay números grandes en juego (las entradas son 0/1), por lo que no aparece la distinción valor/bits de N2 y N3. El código revalida la matriz en cada candidata; eso mantiene `O(n²)` por permutación (solo cambia la constante).

**Medición** (peor caso real: un grafo de `n` vértices **sin** simetrías no triviales, de modo que se agotan las `n! − 1` permutaciones; el de 6 vértices es el de la prueba y los de 7 a 9 lo extienden con una cola de vértices; la búsqueda devuelve `None` en los cuatro, lo que confirma que no tienen simetrías; tiempos de una ejecución en mi entorno con Python 3.12.3, dependen de la máquina):

| n | n! − 1 | Búsqueda | Verificar 1 certificado válido |
|---|---|---|---|
| 6 | 719 | 0,007 s | ~12 µs |
| 7 | 5 039 | 0,064 s | ~14 µs |
| 8 | 40 319 | 0,628 s | ~18 µs |
| 9 | 362 879 | 6,731 s | ~21 µs |

La búsqueda se multiplica por ~10 cada vez que `n` sube en 1; el verificador crece apenas. Para ver `O(n²)` en el verificador: con `n = 100` toma ~1,5 ms y con `n = 200` ~6,3 ms, es decir, ×4 al duplicar `n`. (El certificado válido se midió sobre el grafo sin aristas con la permutación inversa, para que se recorra toda la matriz.) Esa es la asimetría **encontrar vs. verificar**.

## 7. Implementación, pruebas y salida observada
Validación (`validar_matriz`, importada de N1: cuadrada, 0/1, simétrica, sin lazos), verificador (`verificar_automorfismo_no_trivial`), búsqueda (`buscar_automorfismo_no_trivial`) y presentación (`main`) están separados. Nota: para `n = 0` la búsqueda devuelve `None`, porque la única permutación es la identidad (`()`), que se salta.

| Tipo | Caso | Resultado esperado |
|---|---|---|
| Normal | triángulo (caso del correo) | Sí; el certificado no es la identidad y pasa el verificador |
| Normal | camino 0–1–2 | solo el espejo `(2, 1, 0)` (se contrasta con un conteo independiente: 2 automorfismos en total) |
| Normal | ciclo de 5 vértices | Sí |
| Normal | **todos** los grafos de 1 a 5 vértices (1 + 2 + 8 + 64 + 1024) | el resultado coincide con un conteo independiente de automorfismos (`> 1` ⇔ Sí) |
| Límite | grafo de 6 vértices sin simetrías (se agotan 719 candidatas) | No; el conteo independiente da 1 (solo la identidad) |
| Límite | `n = 0`; `n = 1` | No / No |
| Límite | `n = 2`, con y sin arista | Sí, `(1, 0)` |
| Límite | 4 vértices sin aristas; `K₄` | Sí (`K₄` tiene 24 automorfismos) |
| Verificador | certificados válidos `(0, 2, 1)` en el triángulo; `[2, 1, 0]` (lista) en el camino | acepta |
| Verificador | la **identidad** en el triángulo y en el camino (aunque sea automorfismo) | rechaza |
| Verificador | repetido `(0, 0, 2)`, fuera de rango `(0, 1, 3)`, longitud errónea, `(1, 0, 2)` en el camino (no preserva) | rechaza |
| Verificador | las 720 permutaciones sobre el grafo de 6 vértices sin simetrías | rechaza todas |
| Inválido | no cuadrada, valores ≠ 0/1, asimétrica, con lazo | `ValueError` |
| Inválido | entrada que no es lista (`"abc"`, `None`) | `TypeError` |

**Reproducir**
```bash
python3 src/n4_automorfismo.py
python3 -m unittest discover -s tests -v
```
**Salida observada** (`python3 src/n4_automorfismo.py`, ejecutada en Python 3.12.3)
```
¿El triángulo tiene un automorfismo no trivial? Sí
Certificado p (i -> p[i]): (0, 2, 1)
Verificador acepta el certificado: True
La identidad (0, 1, 2) como certificado: False
Camino 0-1-2: (2, 1, 0)
Grafo asimétrico de 6 vértices: None
```
Las 21 pruebas de `test_n4_automorfismo.py` pasan (`OK`).

## 8. Conclusión
Con los datos del correo, **el triángulo sí tiene un automorfismo no trivial**: `p = (0, 2, 1)` (intercambia los vértices 1 y 2 y deja fijo el 0), y el verificador lo acepta. NTA está en **NP** porque el certificado se verifica en `O(n²)`, pero eso **no** prueba que esté fuera de P ni que sea NP-completo. La búsqueda exacta es `O(n!·n²)`: decidible, pero inviable para redes grandes (a `n = 9` ya tarda unos 7 s). Argumentar que **no** existe simetría exige agotar todas las permutaciones o usar otra técnica, porque no tenemos un certificado corto para el «No».
