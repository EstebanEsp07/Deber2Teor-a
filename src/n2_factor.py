"""
N2 · ¿Tiene N un factor en este intervalo?  (Andrés Molina · Seguridad)

Problema de decisión (divisor acotado):
    Entrada : enteros N >= 1 y B >= 0.
    Pregunta: ¿existe un entero d con 2 <= d <= B y d | N?   (Sí / No)

Certificado "Sí": el divisor d.  Se verifica con comprobaciones de rango y una
sola división (N mod d).  Búsqueda exacta: probar d = 2, 3, ..., B.

Lectura literal del correo (decisión declarada en la ficha): se pide un
"divisor d con 2 <= d <= B", así que si B >= N, d = N también cuenta.

Valor vs. tamaño: la entrada ocupa log2(N) + log2(B) BITS. La búsqueda hace
hasta B - 1 divisiones: lineal en el VALOR de B, pero exponencial en su
tamaño en bits (B = 2^(log2 B)). Verificar cuesta una división.

Separación de responsabilidades:
    leer_instancia()     -> lectura (texto -> enteros)
    validar_instancia()  -> validación
    verificar_factor()   -> VERIFICADOR del certificado (polinomial)
    buscar_factor()      -> búsqueda exhaustiva (exacta)
    main()               -> presentación

Uso:
    python3 src/n2_factor.py            # demo del correo
    python3 src/n2_factor.py --medir    # tabla de tiempos (depende de la máquina)
"""
import argparse
import sys
import time


# ------------------------------------------------------ lectura / validación
def leer_instancia(texto_N, texto_B):
    """Convierte dos textos en enteros. Acepta decimal ('91') o con prefijo
    de base ('0b1011011' = 91). Lanza ValueError/TypeError si no se puede."""
    if not isinstance(texto_N, str) or not isinstance(texto_B, str):
        raise TypeError("N y B deben darse como texto")
    try:
        return int(texto_N, 0), int(texto_B, 0)
    except ValueError:
        raise ValueError(f"no son enteros válidos: {texto_N!r}, {texto_B!r}")


def _es_entero(x):
    # bool es subclase de int en Python: True/False no son enteros del problema
    return isinstance(x, int) and not isinstance(x, bool)


def validar_instancia(N, B):
    """Comprueba N >= 1 y B >= 0 enteros. Devuelve (N, B)."""
    if not _es_entero(N) or not _es_entero(B):
        raise TypeError("N y B deben ser enteros")
    if N < 1:
        raise ValueError("N debe ser >= 1 (todo d divide a 0: caso trivial)")
    if B < 0:
        raise ValueError("B debe ser >= 0")
    return N, B


# ------------------------------------------------------------ verificador
def verificar_factor(N, B, d):
    """VERIFICADOR del certificado d.

    Tiempo O(M(log N)) (una división) + O(log B) comparaciones; espacio
    O(log N + log B). Instancia inválida -> excepción; certificado mal
    formado (no entero, fuera de [2, B], no divide) -> False.
    """
    validar_instancia(N, B)
    if not _es_entero(d):
        return False
    if not 2 <= d <= B:          # evita también la división por cero (d = 0)
        return False
    return N % d == 0


# ---------------------------------------------------------------- búsqueda
def buscar_factor(N, B):
    """Devuelve el menor d en [2, B] que divide a N, o None. Exacto.

    Hasta B - 1 divisiones de M(log N) bits cada una: O(B * M(log N)) tiempo,
    O(log N + log B) espacio. Es el algoritmo del correo (fuerza bruta); no
    se corta en sqrt(N) para no cambiar la pregunta: cortar en sqrt(N) sigue
    siendo exponencial en los bits de N (sqrt(N) = 2^(log2(N)/2)).
    """
    validar_instancia(N, B)
    for d in range(2, B + 1):
        if N % d == 0:
            return d
    return None


def tiene_factor(N, B):
    """Versión de decisión (Sí/No)."""
    return buscar_factor(N, B) is not None


# ------------------------------------------------------------ presentación
def _medir():
    # N primo (2^31 - 1): no hay divisor propio, así que se agotan los B - 1 casos.
    N = 2 ** 31 - 1
    print(f"Búsqueda sobre N = 2^31-1 (primo), sin factor en [2, B]:")
    print(f"{'B':>12} {'bits de B':>10} {'búsqueda (s)':>14}")
    for k in (4, 5, 6, 7):
        B = 10 ** k
        t0 = time.perf_counter()
        r = buscar_factor(N, B)
        dt = time.perf_counter() - t0
        print(f"{B:>12} {B.bit_length():>10} {dt:>14.4f}   -> {r}")
    # Verificar un certificado: N = producto de dos primos de Mersenne.
    p1, p2 = 2 ** 31 - 1, 2 ** 61 - 1
    N2, B2 = p1 * p2, p1
    reps = 100_000
    t0 = time.perf_counter()
    for _ in range(reps):
        verificar_factor(N2, B2, p1)
    dt = (time.perf_counter() - t0) / reps
    print(f"\nVerificar d = 2^31-1 para N de {N2.bit_length()} bits: "
          f"{dt * 1e6:.2f} µs por verificación")


def main(argv=None):
    ap = argparse.ArgumentParser(description="N2 · factor de N en [2, B]")
    ap.add_argument("--medir", action="store_true",
                    help="imprime la tabla de tiempos búsqueda vs. verificación")
    args = ap.parse_args(argv)

    # Datos del correo n2 del simulador: N = 91, B = 10
    N, B = leer_instancia("91", "10")
    d = buscar_factor(N, B)
    print(f"¿{N} tiene un divisor en [2, {B}]?", "Sí" if d is not None else "No")
    if d is not None:
        print("Certificado d:", d)
        print("Verificador acepta el certificado:", verificar_factor(N, B, d))
    print("¿d = 13 sirve como certificado (13 > B)?", verificar_factor(N, B, 13))
    print("¿97 (primo) tiene divisor en [2, 10]?", tiene_factor(97, 10))
    if args.medir:
        print()
        _medir()
    return 0


if __name__ == "__main__":
    sys.exit(main())
