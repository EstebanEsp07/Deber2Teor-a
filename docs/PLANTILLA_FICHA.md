# Plantilla de ficha de análisis (copiar a `fichas/<ID>_<tema>.md`)

Ficha obligatoria del deber (Fase D). **Una ficha por correo**, con su código y pruebas en el mismo Pull Request.
Ejemplos completos: `fichas/P1_alcanzabilidad_bfs.md` y `fichas/N1_isomorfismo_grafos.md`.

```markdown
# Ficha <ID> · <título del correo>

| Campo | Valor |
|---|---|
| Grupo de análisis | A·P / B·NP / C·NP-completo |
| Correo | «<asunto>» — <remitente> |
| Responsable / revisor | <nombre> / <nombre> |
| Código | `src/<archivo>.py` |
| Pruebas | `tests/test_<archivo>.py` |
| Estado | Borrador / Revisada / Final |

## 1. Identificador y resumen (sin cambiar condiciones)
## 2. Entrada, salida y restricciones   (indicar: ¿versión de decisión u optimización?)
## 3. Clasificación y evidencia
   A: algoritmo polinómico conocido.
   B: certificado + verificador polinómico (y por qué NO prueba que no esté en P ni que sea NP-completo).
   C: pertenencia a NP + problema NP-completo de origen + argumento de reducción polinómica + consecuencia práctica.
## 4. Decidibilidad y computabilidad   (modelo de cómputo supuesto explícito)
## 5. Algoritmo seleccionado y justificación   (¿exacto, aproximado o heurístico?)  + pseudocódigo + terminación
## 6. Complejidad Big-O temporal y espacial   (definir n, V, E, k…)
## 7. Código, casos de prueba y salida observada   (normales, límite, inválidos)
## 8. Conclusión
```

## Lista de verificación antes de pedir revisión
- [ ] El resumen **no cambia** las condiciones del correo (datos, límites, preguntas).
- [ ] Se dice explícitamente si es **decisión** u **optimización**.
- [ ] La etiqueta P / NP / NP-completo está **sostenida con la evidencia que corresponde** al grupo.
- [ ] No se escribe «NP = no polinómico»: NP es *verificable* en tiempo polinómico.
- [ ] Hay **modelo de cómputo** nombrado y se justifica la **terminación**.
- [ ] Las variables de Big-O están definidas, y se distingue tamaño del valor vs. tamaño en bits (p. ej. `B` vs. `log B`).
- [ ] El código valida entradas y separa lectura / procesamiento / presentación.
- [ ] Hay pruebas normales, límite e inválidas, y la **salida observada** es la real (se pegó tras ejecutar).
- [ ] Alguien distinto al autor la revisó (nombre en el campo «revisor»).
