# Ficha N3 · ¿Existe un exponente x que produzca h?

| Campo | Valor |
|---|---|
| **Grupo de análisis** | B · NP (pertenencia a NP por certificado) |
| **Correo** | «¿Existe exponente x que produzca h?» — Paola León · Seguridad TI |
| **Responsable / revisor** | Elias (@elorgus) / Richard (@RichJ-100) |
| **Sprint** | 2 |
| **Código** | `src/n3_logaritmo_discreto.py` (incluye el **verificador de la Fase E**, `verificar_dlog`) |
| **Pruebas** | `tests/test_n3_logaritmo_discreto.py` (26 pruebas) |
| **Estado** | Borrador v0.1 — pendiente de revisión por pares |

## 1. Identificador y resumen (sin cambiar condiciones)
**Texto del correo (literal):** «Dados p primo, g, h y B, decide si existe x entre 0 y B tal que g^x ≡ h (mod p). El certificado es x y la exponenciación modular lo verifica eficientemente.» Tarea del simulador: implementar búsqueda y verificador **separados** e indicar el costo de ambos.

**Datos del correo:** p = 23 (primo), g = 5, h = 8, B = 10.

**Convenciones que el correo no fija, y la que se adopta (declaradas):**
1. **g y h se toman módulo p.** La congruencia `g^x ≡ h (mod p)` tiene sentido para cualquier entero, así que se acepta cualquier entero y se compara contra `h mod p`. (El código del correo compara `valor == h` sin reducir h; para h ≥ p fallaría aunque la congruencia se cumpla. Con los datos del correo, h = 8 < 23, ambos coinciden.)
2. **`g^0 = 1`** también cuando g ≡ 0 (mod p) (convención de `pow`). Así x = 0 es certificado exactamente cuando h ≡ 1.
3. **p debe ser primo** (precondición del enunciado). Se **comprueba** con Miller–Rabin determinista, válido para p < 3,3·10²⁴; para p mayores se rechaza la entrada en vez de aceptar un «primo» sin garantía. Es una limitación del programa, no del problema.
4. **B ≥ 0** entero; con B = 0 solo se prueba x = 0.

## 2. Entrada, salida y restricciones
- **Entrada:** `p` primo, enteros `g`, `h`, y `B ≥ 0`. Tamaño `n = n_p + n_g + n_h + n_B` bits (`n_v = ⌊log₂ |v|⌋ + 1`).
- **Salida:** Sí/No. (Extra del código: el menor x, que es el certificado.)
- **Versión analizada:** **decisión**. `DLOG-ACOT = { ⟨p, g, h, B⟩ : p primo y existe x ∈ [0, B] con g^x ≡ h (mod p) }`. (Calcular el menor x es un problema de búsqueda; no se analiza como optimización.)

## 3. Clasificación y evidencia
**DLOG-ACOT ∈ NP** (evidencia tipo B: certificado + verificador polinómico).
- **Certificado «Sí»:** el exponente `x`. Ocupa a lo sumo `n_B` bits (x ≤ B).
- **Verificador (`verificar_dlog`):** (1) comprobar que `x` es entero y `0 ≤ x ≤ B`: `O(n_B)`; (2) calcular `g^x mod p` con **exponenciación rápida** (cuadrados y multiplicaciones): a lo sumo `2·n_B` multiplicaciones módulo p de `n_p` bits; (3) comparar con `h mod p`. Total **`O(n_B · M(n_p))` tiempo, `O(n_p + n_B)` espacio**, es decir, polinómico en `log p + log B` (no en B). La precondición «p primo» se comprueba aparte en tiempo polinómico en `n_p` (Miller–Rabin con 13 bases fijas en el rango soportado; en general, AKS).
- **Qué demuestra y qué no:** el certificado corto verificable en tiempo polinómico demuestra `DLOG-ACOT ∈ NP`. **No** demuestra que esté fuera de P (todo problema de P tiene verificador), **ni** que sea NP-completo.
- **Qué se sabe sobre su dificultad (sin afirmar de más):** no se conoce un algoritmo polinómico en `n` para el logaritmo discreto en general, y por eso se usa como base de criptosistemas (p. ej. Diffie–Hellman); es una **suposición de dificultad**, no un teorema, y tampoco se conoce una prueba de NP-completitud. Observación útil: la parte «difícil» viene solo de que **B sea grande en valor**: si B está acotado por un polinomio en `n` (p. ej. B dado en unario), la búsqueda es polinómica. _(Citar referencias en el informe.)_

## 4. Decidibilidad y computabilidad
- **Modelo supuesto:** máquina de Turing determinista (polinomialmente equivalente a una RAM de costo logarítmico).
- **Función calculada:** `f(p, g, h, B) ∈ {Sí, No}`, total sobre las entradas válidas (p primo, B ≥ 0).
- **Decidible:** sí. Hay `B + 1` exponentes candidatos, un conjunto **finito**; probarlos todos termina siempre. Decidible no implica eficiente (§6).

## 5. Algoritmo seleccionado y justificación
**Búsqueda exhaustiva con actualización incremental** (el algoritmo del correo) y **verificador separado** con `pow(g, x, p)`. Es **exacta** (no aproximada ni heurística): devuelve el *menor* x válido o declara que no existe.

```
BUSCAR-DLOG(p, g, h, B):
  validar tipos, B ≥ 0 y que p sea primo
  objetivo ← h mod p;  base ← g mod p;  valor ← 1        # g^0
  para x ← 0 hasta B:
    si valor = objetivo: devolver (Sí, x)
    valor ← (valor · base) mod p                          # g^(x+1)
  devolver No

VERIFICAR-DLOG(p, g, h, B, x):
  validar p, g, h, B
  si x no es entero o no (0 ≤ x ≤ B): devolver falso
  devolver (g^x mod p = h mod p)          # exponenciación rápida
```
- **Terminación:** el `para` recorre `B + 1` valores y cada paso es una multiplicación modular finita; `VERIFICAR` hace `O(log B)` multiplicaciones.
- **Corrección (invariante):** al comienzo de la vuelta `x`, `valor = g^x mod p`. Si coincide con el objetivo se devuelve el primer x que lo cumple; si el bucle acaba, ningún x de [0, B] lo cumple.
- **Por qué incremental:** una multiplicación por paso en vez de una exponenciación completa. Recalcular `pow(g, x, p)` en cada x daría `O(B · log B · M(n_p))`, **la cota que cita el correo**; el incremental da `O(B · M(n_p))`. No se contradicen: ambas son cotas superiores válidas y la segunda es más ajustada. Una mejora conocida (baby-step giant-step, ≈ √B pasos y memoria) no se implementa: sigue siendo exponencial en los bits.
- **Observación:** si g no es múltiplo de p, las potencias se repiten con período que divide a p − 1, así que B mayor que p no añade exponentes nuevos; no se corta para conservar el algoritmo del correo.

## 6. Complejidad (p, B: valores; n_p, n_B: bits; M(k): costo de multiplicar k bits)
| Operación | Tiempo | Espacio |
|---|---|---|
| Verificar un certificado | `O(n_B · M(n_p))` | `O(n_p + n_B)` |
| Búsqueda exhaustiva (peor caso, incremental) | `O(B · M(n_p))` | `O(n_p + n_B)` |
| Búsqueda recalculando `pow` en cada x (cota del correo) | `O(B · log B · M(n_p))` | `O(n_p + n_B)` |
| Comprobar que p es primo (Miller–Rabin, 13 bases) | `O(n_p · M(n_p))` | `O(n_p)` |

**Valor vs. bits (el punto de la tarea).** La búsqueda es **lineal en el valor de B**, pero `B = 2^(n_B)`: en función del tamaño de la entrada es `O(2^(n_B) · M(n_p))`, **exponencial**; cada bit más en B duplica el trabajo. Verificar depende de `n_B`, no de B: es **polinómico en `log p + log B`**. En el mismo `n_B = 1000` bits, verificar es cuestión de microsegundos y buscar es inviable.

**Medición** (una ejecución en el entorno de pruebas, depende de la máquina; `python3 src/n3_logaritmo_discreto.py --medir`):

```
Búsqueda con p = 2^61-1, g = 3, h = 0 (sin solución: se agotan B+1 pasos):
           B  bits de B   búsqueda (s)
       10000         14         0.0009   -> None
      100000         17         0.0087   -> None
     1000000         20         0.0814   -> None
    10000000         24         1.0548   -> None

Verificar x de 1000 bits con B = 2^1000: True, 206.9 µs por verificación
```

La búsqueda se multiplica por ≈ 10 cada vez que B se multiplica por 10 (≈ 3,3 bits más). La verificación del certificado de 1000 bits tarda microsegundos, y buscarlo con B = 2¹⁰⁰⁰ no terminaría nunca.

## 7. Código, casos de prueba y salida observada
Lectura (`leer_instancia`), primalidad (`es_primo`), validación (`validar_instancia`), verificador (`verificar_dlog`), búsqueda (`buscar_dlog`) y presentación (`main`) están separados. El verificador **no llama** a la búsqueda. Nota: x = 0 es un certificado válido y es falso en Python; por eso la decisión compara con `is not None`. Instancia inválida → excepción; certificado mal formado o incorrecto → `False`.

| Tipo | Caso | Resultado esperado |
|---|---|---|
| Normal | p = 23, g = 5, h = 8, B = 10 (caso del correo) | Sí, x = 6 (5⁶ = 15625 ≡ 8); el verificador lo acepta |
| Normal | x ∈ {0, 1, 2, 3, 4, 5, 7, 8, 9, 10} | el verificador rechaza todos |
| Normal | B = 5 (la solución x = 6 queda fuera) | No; y x = 6 se rechaza por x > B |
| Normal | g, h mayores que p o negativos (28, 54; −18, −15) | misma respuesta que reducidos |
| Normal | p = 7, g = 2, h = 3 (no está en {1, 2, 4}) | No |
| Límite | h = 1 | x = 0 (Sí) |
| Límite | solución justo en B (B = 6) y B = 0 | x = 6 / x = 0 o No |
| Límite | g múltiplo de p (sucesión 1, 0, 0, …) | h = 0 → x = 1; h = 1 → x = 0; otro h → No |
| Límite | h = 0 con g coprimo con p; p = 2 | No / casos correctos |
| Límite | B = 10 000 ≫ p | x = 6 (el período de las potencias lo acota) |
| Límite | p = 2⁶¹−1, B = 2¹⁰⁰⁰, certificado de 1000 bits | acepta de inmediato; x + 1 y B + 1 se rechazan |
| Límite | certificado `"6"`, `6.0`, `None`, `True`, `[6]`, `−1`, `11` | rechaza sin excepción |
| Límite | primos p < 50 × todos g, h × B ∈ {0, 3, 10}: la búsqueda devuelve el **menor** certificado que acepta el verificador, o None | coincide en todas las instancias |
| Primalidad | `es_primo` vs. criba de Eratóstenes de −5 a 10 000 | coincide en todos |
| Primalidad | Carmichael (561, 1105, 1729, …) y pseudoprimos fuertes (3 215 031 751, 3 825 123 056 546 413 051) | compuestos |
| Primalidad | 2³¹−1, 2⁶¹−1, 10¹⁸+9; 2⁸⁹−1 (fuera del límite) | primos / `ValueError` |
| Inválido | p = 15, 1, 0, −7, 561 | `ValueError` |
| Inválido | B < 0; p ≥ 3,3·10²⁴ | `ValueError` |
| Inválido | tipos no enteros, `bool`, texto en lugar de número | `TypeError` / `ValueError` |

**Reproducir**
```bash
python3 src/n3_logaritmo_discreto.py
python3 src/n3_logaritmo_discreto.py --medir
python3 -m unittest discover -s tests -v
```
**Salida observada** (`python3 src/n3_logaritmo_discreto.py`)
```
¿Existe x en [0, 10] con 5^x ≡ 8 (mod 23)? Sí
Certificado x: 6 (pow(5, 6, 23) = 8)
Verificador acepta el certificado: True
¿x = 7 sirve como certificado? False
¿Existe x en [0, 5]? (la solución x = 6 queda fuera) No
```
Las 26 pruebas de `test_n3_logaritmo_discreto.py` pasan (`OK`); las 104 del repo se ejecutaron juntas en 0,8 s.

## 8. Conclusión
Con los datos del correo, **sí existe x**: x = 6 (5⁶ = 15 625 = 679·23 + 8). DLOG-ACOT está en **NP**: el certificado x se verifica con exponenciación modular en tiempo polinómico en `log p + log B`, pero eso **no** prueba que esté fuera de P ni que sea NP-completo. La búsqueda exacta es `O(B · M(log p))`: lineal en el valor de B y **exponencial en su tamaño en bits**. `verificar_dlog` es además el **verificador de certificado de la Fase E (E-01)**: función separada de la búsqueda, con pruebas normales, límite e inválidas.
