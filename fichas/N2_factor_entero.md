# Ficha N2 · ¿Tiene N un factor en este intervalo?

| Campo | Valor |
|---|---|
| **Grupo de análisis** | B · NP (pertenencia a NP por certificado) |
| **Correo** | «¿Tiene N un factor en este intervalo?» — Andrés Molina · Seguridad |
| **Responsable / revisor** | Elias (@elorgus) / Richard (@RichJ-100) |
| **Sprint** | 2 |
| **Código** | `src/n2_factor.py` (incluye el **verificador** `verificar_factor`) |
| **Pruebas** | `tests/test_n2_factor.py` (19 pruebas) |
| **Estado** | Revisado |

## 1. Identificador y resumen (sin cambiar condiciones)
**Texto del correo (literal):** «Dados enteros N y B en binario, decide si N tiene un divisor d con 2 ≤ d ≤ B. Un certificado "sí" es d; se comprueba dividiendo N por d.» Tarea del simulador: diferenciar el tiempo de **encontrar** un certificado del de **verificarlo**.

**Datos del correo:** N = 91 (en binario `1011011`), B = 10, certificado d con d | N y 2 ≤ d ≤ B.

**Lecturas que el correo deja abiertas, y la que se adopta (declaradas, no silenciosas):**
1. **«factor» (asunto) vs. «divisor» (texto).** Se sigue el texto, que es la definición precisa: *cualquier* divisor d con 2 ≤ d ≤ B. Consecuencia: si B ≥ N, d = N también es certificado, y todo N ≥ 2 responde Sí. Quien quiera «factor propio» (d < N) debe pedirlo; aquí no se cambia la condición.
2. **«N y B en binario».** Se interpreta como la **codificación de la entrada** (de ahí que su tamaño sea `log N` y `log B` bits), no como que «10» sea el número dos. B = 10 es **diez**: el código del propio correo usa `N, B = 91, 10` y devuelve 7; con B = 2 la respuesta sería No y contradiría su código. El programa acepta además texto con prefijo `0b…` (`0b1011011` = 91).
3. **Dominio:** N ≥ 1 y B ≥ 0 enteros. N = 0 se rechaza (todo d divide a 0). Si B < 2 el intervalo [2, B] está vacío y la respuesta es No.

## 2. Entrada, salida y restricciones
- **Entrada:** enteros `N ≥ 1` y `B ≥ 0`. Tamaño de la entrada `n = n_N + n_B` bits, con `n_N = ⌊log₂ N⌋ + 1` y `n_B = ⌊log₂ B⌋ + 1`.
- **Salida:** Sí/No. (Extra del código: el menor divisor d encontrado, que es el certificado.)
- **Versión analizada:** **decisión**. `DIV-ACOT = { ⟨N, B⟩ : existe d ∈ ℤ con 2 ≤ d ≤ B y d | N }`. (La variante «encontrar d» es de búsqueda; no se analiza como optimización.)

## 3. Clasificación y evidencia
**DIV-ACOT ∈ NP** (evidencia tipo B: certificado + verificador polinómico).
- **Certificado «Sí»:** el entero `d`. Ocupa a lo sumo `n_B` bits (porque d ≤ B): longitud polinómica en el tamaño de la entrada.
- **Verificador:** (1) comprobar `2 ≤ d ≤ B`: `O(n_B)`; (2) comprobar `N mod d = 0`: **una división**, `O(M(n_N))`, donde `M(k)` es el costo de multiplicar/dividir números de `k` bits. Total **`O(M(n_N) + n_B)` tiempo, `O(n_N + n_B)` espacio**: polinómico (cuasi-lineal con multiplicación rápida) en el tamaño de la entrada.
- **Qué demuestra y qué no:** que exista un certificado corto verificable en tiempo polinómico demuestra `DIV-ACOT ∈ NP`. **No** demuestra que esté fuera de P (todo problema de P también tiene verificador: basta ignorar el certificado y resolverlo), **ni** que sea NP-completo.
- **Qué se sabe sobre su dificultad (sin afirmar de más):** no se conoce un algoritmo polinómico en `n` para este problema, y de tenerlo se obtendría uno para **factorizar enteros** (bastaría una búsqueda binaria sobre B para hallar el menor divisor ≥ 2, que es el menor primo de N). Por eso importa en seguridad. Pero «no se conoce» no es «no existe»: no se ha demostrado que esté fuera de P. Tampoco se sabe de una prueba de NP-completitud; además el problema complementario también tiene certificado corto (la factorización completa de N con pruebas de primalidad), y un problema NP-completo en NP ∩ coNP implicaría NP = coNP, que se cree falso pero no está demostrado. Esto último es contexto, no parte de la evidencia del grupo B. _(Citar referencias en el informe.)_

## 4. Decidibilidad y computabilidad
- **Modelo supuesto:** máquina de Turing determinista (polinomialmente equivalente a una RAM de costo logarítmico).
- **Función calculada:** `f(N, B) ∈ {Sí, No}`, total sobre las entradas válidas.
- **Decidible:** sí. Los candidatos son los `B − 1` enteros de [2, B]: un conjunto **finito**; probarlos todos termina siempre y responde correctamente. Decidible no implica eficiente (§6).

## 5. Algoritmo seleccionado y justificación
**Búsqueda exhaustiva por división** (el algoritmo del correo), con el verificador como función **separada**. Es **exacta** (no aproximada ni heurística): devuelve el *menor* d válido o declara que no existe.

```
BUSCAR-FACTOR(N, B):
  validar N ≥ 1, B ≥ 0 enteros
  para d ← 2 hasta B:
    si N mod d = 0: devolver (Sí, d)
  devolver No

VERIFICAR-FACTOR(N, B, d):
  validar N, B
  si d no es entero: devolver falso
  si no (2 ≤ d ≤ B): devolver falso      # evita también d = 0
  devolver (N mod d = 0)
```
- **Terminación:** el `para` recorre a lo sumo `B − 1` valores y cada división termina; `VERIFICAR` hace un número constante de operaciones.
- **Corrección:** si existe un divisor en [2, B], el primero que encuentra el bucle (el menor) cumple `d | N`; si el bucle termina sin éxito, ningún entero de [2, B] divide a N.
- **Por qué no cortar en √N:** es una mejora exacta conocida (si N no tiene divisor ≤ √N, es primo y su único divisor es N), pero cambia el algoritmo del correo y **no** cambia la conclusión: `√N = 2^(n_N / 2)` sigue siendo exponencial en los bits.

## 6. Complejidad (N, B: valores; n_N, n_B: bits; M(k): costo de multiplicar k bits)
| Operación | Tiempo | Espacio |
|---|---|---|
| Verificar un certificado | `O(M(n_N) + n_B)` | `O(n_N + n_B)` |
| Búsqueda exhaustiva (peor caso) | `O(B · M(n_N))` | `O(n_N + n_B)` |

**Valor vs. bits (el punto de la tarea).** La búsqueda hace hasta `B − 1` divisiones: es **lineal en el valor de B**, pero `B = 2^(n_B)`, así que en función del **tamaño** `n_B` de la entrada es `O(2^(n_B) · M(n_N))`: **exponencial**. Cada bit más en B **duplica** el trabajo en el peor caso. El verificador, en cambio, hace **una división**: crece como un polinomio en `n_N`. «Lineal en B» y «polinómico en la entrada» no son lo mismo.

**Medición** (peor caso real: N = 2³¹−1 es primo, no hay divisor propio y se agotan los `B − 1` casos; una ejecución en el entorno de pruebas, depende de la máquina; `python3 src/n2_factor.py --medir`):

```
Búsqueda sobre N = 2^31-1 (primo), sin factor en [2, B]:
           B  bits de B   búsqueda (s)
       10000         14         0.0006   -> None
      100000         17         0.0064   -> None
     1000000         20         0.0516   -> None
    10000000         24         0.3496   -> None

Verificar d = 2^31-1 para N de 92 bits: 0.31 µs por verificación
```

Cada vez que B se multiplica por 10 (≈ 3,3 bits más) el tiempo se multiplica por ≈ 10. **Extrapolación (no medida):** con la misma velocidad (≈ 3,6·10⁻⁸ s por división), B ≈ 2³¹ tomaría ≈ 76 s y B ≈ 2⁶¹ unos 8·10¹⁰ s (≈ 2600 años). El verificador sigue en fracciones de microsegundo.

## 7. Código, casos de prueba y salida observada
Lectura (`leer_instancia`), validación (`validar_instancia`), verificador (`verificar_factor`), búsqueda (`buscar_factor`) y presentación (`main`) están separados. El verificador **no llama** a la búsqueda. Instancia inválida → excepción; certificado mal formado → `False` (no excepción).

| Tipo | Caso | Resultado esperado |
|---|---|---|
| Normal | N = 91, B = 10 (caso del correo) | Sí, d = 7; el verificador lo acepta |
| Normal | N = 97 (primo), B = 10 | No |
| Normal | N = 100, B = 50 | d = 2 |
| Normal | d = 13 con N = 91, B = 10 | rechaza (13 > B); con B = 13 acepta |
| Normal | d = 5 con N = 91 | rechaza (no divide) |
| Límite | B = 0 y B = 1 (intervalo vacío); N = 1 | No |
| Límite | N = B = 97 (primo) | d = 97 (lectura literal: d = N cuenta); con B = 96 → No |
| Límite | extremos d = B y d = 2; d = 1 y d = B + 1 | acepta / rechaza |
| Límite | d = 0 o negativo | rechaza, sin `ZeroDivisionError` |
| Límite | N de 92 bits (producto de dos primos de Mersenne), d = 2³¹−1 | acepta de inmediato |
| Límite | certificado `"7"`, `7.0`, `None`, `True`, `[7]` | rechaza sin excepción |
| Límite | lectura `0b1011011` y `0b1010` | (91, 10) |
| Límite | N en 1..120 × B en 0..40: la búsqueda devuelve el **menor** certificado que acepta el verificador, o None si ninguno | coincide en las 4 920 instancias |
| Inválido | N = 0 o N < 0; B < 0 | `ValueError` |
| Inválido | N o B decimales, texto, `None` o `bool` | `TypeError` |
| Inválido | texto no numérico, vacío o `"1.5"` | `ValueError` |

**Reproducir**
```bash
python3 src/n2_factor.py
python3 src/n2_factor.py --medir
python3 -m unittest discover -s tests -v
```
**Salida observada** (`python3 src/n2_factor.py`)
```
¿91 tiene un divisor en [2, 10]? Sí
Certificado d: 7
Verificador acepta el certificado: True
¿d = 13 sirve como certificado (13 > B)? False
¿97 (primo) tiene divisor en [2, 10]? False
```
Las 19 pruebas de `test_n2_factor.py` pasan (`OK`); las 333 del repo se ejecutaron juntas en 0,8 s.

## 8. Conclusión
Con los datos del correo, **N = 91 sí tiene un divisor en [2, 10]**: d = 7 (91 = 7 · 13); el otro factor, 13, queda fuera del intervalo. El problema está en **NP**: el certificado d se verifica con una división, pero eso **no** prueba que esté fuera de P ni que sea NP-completo. La búsqueda exacta es `O(B · M(log N))`: lineal en el valor de B y **exponencial en su tamaño en bits**; verificar es polinómico. Esa es la asimetría **encontrar vs. verificar** que pide la tarea.
