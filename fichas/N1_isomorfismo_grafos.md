# Ficha N1 · ¿Existe isomorfismo entre dos redes?

| Campo | Valor |
|---|---|
| **Grupo de análisis** | B · NP (pertenencia a NP por certificado) |
| **Correo** | «Comparar topologías equivalentes» — Elena Ruiz · Arquitectura |
| **Responsable / revisor** | Esteban (@EstebanEsp07) / Elias (@elorgus) |
| **Código** | `src/n1_isomorfismo.py` (incluye el **verificador**) |
| **Pruebas** | `tests/test_n1_isomorfismo.py` (17 pruebas) |
| **Estado** | Borrador v0.1 — pendiente de revisión por pares |

## 1. Identificador y resumen (sin cambiar condiciones)
Dadas dos redes como grafos, decidir si existe una correspondencia uno a uno entre nodos que preserve las aristas (isomorfismo de grafos). Datos del correo: Red A y Red B, cada una con 3 nodos y 2 enlaces; pregunta «¿misma estructura?» (Sí/No).

## 2. Entrada, salida y restricciones
- **Entrada:** dos grafos `G1`, `G2` **simples y no dirigidos** (supuesto explícito), dados como matrices de adyacencia `n × n`, 0/1, simétricas, diagonal en 0.
- **Salida:** Sí/No. (Extra del código: el certificado `p`.)
- **Versión analizada:** **decisión**. `GI = { ⟨G1, G2⟩ : existe una biyección p: V1 → V2 con A[i][j] = B[p[i]][p[j]] ∀ i, j }`.
- **Instancia del correo:** el correo da solo conteos. Como hay exactamente un grafo simple de 3 nodos y 2 aristas salvo isomorfismo (el camino de 3 nodos), **cualquier** par A, B con esos datos es isomorfo. Para probar el código se usó A = camino 0–1–2 y B = estrella centrada en 0.

## 3. Clasificación y evidencia
**GI ∈ NP** (evidencia tipo B: certificado + verificador polinómico).
- **Certificado «Sí»:** la permutación `p` (una lista de `n` enteros: `O(n log n)` bits).
- **Verificador:** (1) comprobar que `p` es una permutación de `{0..n-1}`: `O(n)`; (2) comprobar `A[i][j] = B[p[i]][p[j]]` para todo `i, j`: `O(n²)`. Total **`O(n²)` tiempo, `O(n)` espacio**, lineal en el tamaño de la entrada (`Θ(n²)` bits).
- **Qué demuestra y qué no:** que exista un certificado corto y verificable en tiempo polinómico demuestra `GI ∈ NP`. **No** demuestra que GI no esté en P (todo problema de P también tiene verificador), ni que sea NP-completo. Hasta donde sabemos, no se conoce un algoritmo polinómico para GI ni una prueba de NP-completitud; existe un resultado cuasi-polinómico de Babai (2016), que no usamos y no cambia esta clasificación. _(Citar la referencia exacta en el informe.)_

## 4. Decidibilidad y computabilidad
- **Modelo supuesto:** máquina de Turing determinista.
- **Función calculada:** `GI: (G1, G2) → {Sí, No}`, total.
- **Decidible:** sí. Hay solo `n!` biyecciones posibles; el algoritmo las enumera y termina siempre. Que sea decidible **no** implica que sea eficiente (§6).

## 5. Algoritmo seleccionado y justificación
**Búsqueda exhaustiva de permutaciones** con dos filtros baratos previos (mismo `n`, misma secuencia de grados). Es **exacta** (no heurística): responde Sí/No correctamente; los filtros son condiciones **necesarias**, no suficientes.

```
BUSCAR-ISO(A, B):
  validar A y B;  si n(A) ≠ n(B): devolver No
  si ordenar(grados(A)) ≠ ordenar(grados(B)): devolver No
  para cada permutación p de {0..n-1}:
    si VERIFICAR(A, B, p): devolver (Sí, p)
  devolver No

VERIFICAR(A, B, p):
  si p no es permutación de {0..n-1}: devolver falso
  devolver (∀ i, j: A[i][j] = B[p[i]][p[j]])
```
- **Terminación:** el `para` recorre un conjunto finito de `n!` permutaciones, cada una verificada en `O(n²)` tiempo finito.
- **Corrección:** si existe isomorfismo, es una de las `n!` permutaciones y `VERIFICAR` lo acepta; si ninguna pasa, no existe.
- Por qué no algo más sofisticado: el objetivo del correo es separar «encontrar» de «verificar»; un algoritmo especializado no cambiaría la clasificación pedida.

## 6. Complejidad (n = nodos)
| Operación | Tiempo | Espacio |
|---|---|---|
| Verificar un certificado | `O(n²)` | `O(n)` |
| Búsqueda exhaustiva (peor caso) | `O(n! · n²)` | `O(n)` (las permutaciones se generan de a una) |
| Filtro de grados | `O(n²)` | `O(n)` |

**Medición** (peor caso real para n = 6…9: el ciclo Cₙ contra C₃ ∪ Cₙ₋₃, no isomorfos pero con la **misma** secuencia de grados, así que el filtro no los separa y se agotan las `n!` permutaciones; tiempos de una ejecución en el entorno de pruebas, dependen de la máquina):

| n | n! | Búsqueda | Verificar 1 certificado |
|---|---|---|---|
| 6 | 720 | 0,001 s | ~8 µs |
| 7 | 5 040 | 0,003 s | ~10 µs |
| 8 | 40 320 | 0,024 s | ~12 µs |
| 9 | 362 880 | 0,213 s | ~15 µs |

La búsqueda se multiplica por ~9 cada vez que `n` sube en 1; el verificador crece apenas. Esa es la asimetría **encontrar vs. verificar**.

## 7. Implementación, pruebas y salida observada
Validación (`validar_matriz`: cuadrada, 0/1, simétrica, sin lazos), verificador (`verificar_isomorfismo`), búsqueda (`buscar_isomorfismo`) y presentación (`main`) están separados. Nota: para `n = 0` la búsqueda devuelve `()`, que es falso en Python; por eso siempre se compara con `is not None`.

| Tipo | Caso | Resultado esperado |
|---|---|---|
| Normal | camino 0–1–2 vs. estrella (caso del correo) | Sí; el certificado pasa el verificador |
| Normal | triángulo vs. sí mismo | Sí, identidad `(0,1,2)` |
| Normal | camino vs. triángulo | No (distinto nº de aristas) |
| Normal | grafo de 6 nodos reetiquetado al azar (5 veces, semilla 2026) | Sí y verificado |
| Límite | C₆ vs. C₃ ∪ C₃ (misma secuencia de grados, no isomorfos) | No, tras agotar 720 permutaciones |
| Límite | tamaños distintos; grafo vacío (`n=0`); un nodo; sin aristas | No / `()` / `(0,)` / Sí |
| Verificador | certificado válido `(1,0,2)` | acepta |
| Verificador | repetido `(0,0,2)`, fuera de rango `(0,1,3)`, longitud errónea, no preserva `(0,1,2)` | rechaza |
| Inválido | no cuadrada, valores ≠ 0/1, asimétrica, con lazo | `ValueError` |
| Inválido | entrada que no es lista | `TypeError` |

**Reproducir**
```bash
python3 src/n1_isomorfismo.py
python3 -m unittest discover -s tests -v
```
**Salida observada** (`python3 src/n1_isomorfismo.py`)
```
¿A y B son isomorfas? Sí
Certificado p (i -> p[i]): (1, 0, 2)
Verificador acepta el certificado: True
¿Camino de 3 nodos vs triángulo? False
```
Las 17 pruebas de `test_n1_isomorfismo.py` pasan (`OK`).

## 8. Conclusión
Con los datos del correo, **las redes sí son isomorfas** (certificado `p = (1, 0, 2)`). GI está en **NP** porque el certificado se verifica en `O(n²)`, pero eso **no** prueba que esté fuera de P ni que sea NP-completo. La búsqueda exacta es `O(n!·n²)`: decidible, pero inviable para redes grandes.

## 9. Nota para Richard (correo n4)
`_preserva` y el verificador sirven para el automorfismo no trivial: es el caso `A = B` exigiendo `p ≠ identidad`. Ojo: la primera permutación que genera `itertools.permutations` es la identidad, así que n4 debe saltarla.
