"""
N3 · ¿Existe exponente x que produzca h?  (Paola León · Seguridad TI)
Incluye el VERIFICADOR DE CERTIFICADO de la Fase E (E-01): verificar_dlog().

Problema de decisión (logaritmo discreto acotado):
    Entrada : p primo, enteros g, h y B >= 0.
    Pregunta: ¿existe x con 0 <= x <= B tal que g^x ≡ h (mod p)?   (Sí / No)

Convenciones (declaradas en la ficha): g y h se toman módulo p (cualquier
entero es válido) y g^0 = 1 aunque g ≡ 0 (mod p).

Certificado "Sí": el exponente x. Se verifica con exponenciación modular
rápida (cuadrados y multiplicaciones): O(log B) multiplicaciones modulares.
Búsqueda exacta: se prueban x = 0, 1, ..., B.

Valor vs. tamaño: B ocupa log2(B) bits. La búsqueda hace B + 1 pasos: lineal
en el VALOR de B, exponencial en su tamaño en bits. El verificador es
polinómico en log p + log B.

Separación de responsabilidades:
    leer_instancia()     -> lectura (texto -> enteros)
    es_primo()           -> primalidad determinista (precondición de p)
    validar_instancia()  -> validación
    verificar_dlog()     -> VERIFICADOR del certificado (polinómico)
    buscar_dlog()        -> búsqueda exhaustiva (exacta)
    main()               -> presentación

Uso:
    python3 src/n3_logaritmo_discreto.py            # demo del correo
    python3 src/n3_logaritmo_discreto.py --medir    # tiempos (dependen de la máquina)
"""
import argparse
import sys
import time

# Miller-Rabin DETERMINISTA: con estas 13 bases (los primeros 13 primos) el
# test es exacto para todo n < 3 317 044 064 679 887 385 961 981 (≈ 3,3·10^24)
# (resultado de Sorenson y Webster, 2015). Más allá no garantizamos nada y
# preferimos rechazar la entrada antes que aceptar un "primo" dudoso.
_BASES_MR = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)
_LIMITE_MR = 3_317_044_064_679_887_385_961_981


# ------------------------------------------------------ lectura / validación
def leer_instancia(texto_p, texto_g, texto_h, texto_B):
    """Convierte cuatro textos en enteros (decimal o con prefijo 0b/0x)."""
    textos = (texto_p, texto_g, texto_h, texto_B)
    if not all(isinstance(t, str) for t in textos):
        raise TypeError("p, g, h y B deben darse como texto")
    try:
        return tuple(int(t, 0) for t in textos)
    except ValueError:
        raise ValueError(f"no son enteros válidos: {textos!r}")


def _es_entero(x):
    return isinstance(x, int) and not isinstance(x, bool)


def es_primo(n):
    """Primalidad determinista (Miller-Rabin) para n < ~3,3·10^24.

    Tiempo polinómico en log n: O(k · log n) multiplicaciones modulares con
    k = 13 bases fijas. Lanza ValueError si n supera el límite garantizado.
    """
    if not _es_entero(n):
        raise TypeError("n debe ser entero")
    if n < 2:
        return False
    for q in _BASES_MR:                       # divisores pequeños
        if n % q == 0:
            return n == q
    if n >= _LIMITE_MR:
        raise ValueError("p supera 3,3e24: no hay garantía determinista de "
                         "primalidad con las bases fijas de este programa")
    d, s = n - 1, 0
    while d % 2 == 0:                         # n - 1 = d * 2^s con d impar
        d //= 2
        s += 1
    for a in _BASES_MR:
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False                      # a es testigo de que n es compuesto
    return True


def validar_instancia(p, g, h, B):
    """Comprueba tipos, B >= 0 y que p sea primo. Devuelve (p, g, h, B)."""
    if not all(_es_entero(v) for v in (p, g, h, B)):
        raise TypeError("p, g, h y B deben ser enteros")
    if B < 0:
        raise ValueError("B debe ser >= 0")
    if not es_primo(p):
        raise ValueError(f"p = {p} no es primo")
    return p, g, h, B


# ------------------------------------------------------------ verificador
def verificar_dlog(p, g, h, B, x):
    """VERIFICADOR del certificado x (Fase E, E-01).

    Acepta si x es entero, 0 <= x <= B y g^x ≡ h (mod p).
    Tiempo: O(log B) multiplicaciones modulares de log p bits, es decir
    O(log B · M(log p)), más la comprobación de primalidad de p (polinómica
    en log p); espacio O(log p + log B). Es INDEPENDIENTE de buscar_dlog().
    Instancia inválida -> excepción; certificado mal formado o incorrecto
    -> False.
    """
    validar_instancia(p, g, h, B)
    if not _es_entero(x) or not 0 <= x <= B:
        return False
    return pow(g, x, p) == h % p              # pow usa cuadrados y multiplicaciones


# ---------------------------------------------------------------- búsqueda
def buscar_dlog(p, g, h, B):
    """Devuelve el menor x en [0, B] con g^x ≡ h (mod p), o None. Exacto.

    Se mantiene g^x de forma INCREMENTAL (valor ← valor·g mod p): una
    multiplicación modular por paso, O(B · M(log p)) tiempo y O(log p) espacio
    (es el código del correo). Recalcular pow(g, x, p) en cada paso daría
    O(B · log B · M(log p)), la cota que cita el correo; ambas son cotas
    superiores válidas y la incremental es la más ajustada.
    Observación (no usada): si g no es múltiplo de p, g^x se repite con
    período que divide a p - 1, así que valores de B mayores que p no añaden
    exponentes nuevos; no se corta para mantener el algoritmo del correo.
    """
    validar_instancia(p, g, h, B)
    objetivo = h % p
    base = g % p
    valor = 1                                  # g^0 (p >= 2, así que 1 % p = 1)
    for x in range(B + 1):
        if valor == objetivo:
            return x
        valor = valor * base % p
    return None


def existe_dlog(p, g, h, B):
    """Versión de decisión (Sí/No). Ojo: x = 0 es certificado válido, por
    eso se compara con 'is not None' y no con la veracidad de x."""
    return buscar_dlog(p, g, h, B) is not None


# ------------------------------------------------------------ presentación
def _medir():
    p, g = 2 ** 61 - 1, 3                      # p primo de Mersenne
    h = 0                                      # inalcanzable (g no es múltiplo de p)
    print(f"Búsqueda con p = 2^61-1, g = 3, h = 0 (sin solución: se agotan B+1 pasos):")
    print(f"{'B':>12} {'bits de B':>10} {'búsqueda (s)':>14}")
    for k in (4, 5, 6, 7):
        B = 10 ** k
        t0 = time.perf_counter()
        r = buscar_dlog(p, g, h, B)
        dt = time.perf_counter() - t0
        print(f"{B:>12} {B.bit_length():>10} {dt:>14.4f}   -> {r}")
    # Verificación con B enorme: la búsqueda sería imposible, verificar es instantáneo
    B = 2 ** 1000
    x0 = 2 ** 999 + 12345
    h = pow(g, x0, p)
    reps = 2000
    t0 = time.perf_counter()
    for _ in range(reps):
        ok = verificar_dlog(p, g, h, B, x0)
    dt = (time.perf_counter() - t0) / reps
    print(f"\nVerificar x de {x0.bit_length()} bits con B = 2^1000: {ok}, "
          f"{dt * 1e6:.1f} µs por verificación")


def main(argv=None):
    ap = argparse.ArgumentParser(description="N3 · logaritmo discreto acotado")
    ap.add_argument("--medir", action="store_true",
                    help="imprime la tabla de tiempos búsqueda vs. verificación")
    args = ap.parse_args(argv)

    # Datos del correo n3 del simulador: p = 23, g = 5, h = 8, B = 10
    p, g, h, B = leer_instancia("23", "5", "8", "10")
    x = buscar_dlog(p, g, h, B)
    print(f"¿Existe x en [0, {B}] con {g}^x ≡ {h} (mod {p})?",
          "Sí" if x is not None else "No")
    if x is not None:
        print("Certificado x:", x, f"(pow({g}, {x}, {p}) = {pow(g, x, p)})")
        print("Verificador acepta el certificado:", verificar_dlog(p, g, h, B, x))
    print("¿x = 7 sirve como certificado?", verificar_dlog(p, g, h, B, 7))
    print("¿Existe x en [0, 5]? (la solución x = 6 queda fuera)",
          "Sí" if existe_dlog(p, g, h, 5) else "No")
    if args.medir:
        print()
        _medir()
    return 0


if __name__ == "__main__":
    sys.exit(main())
