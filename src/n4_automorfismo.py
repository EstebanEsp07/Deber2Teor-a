"""
N4 · ¿La topología tiene una simetría?  (Santiago Jaramillo · Analítica)

Problema de decisión (automorfismo no trivial de un grafo):
    Entrada : un grafo G no dirigido y simple, como matriz de adyacencia
              n x n (0/1, simétrica, diagonal en 0).
    Pregunta: ¿existe una permutación p de {0..n-1}, DISTINTA de la identidad,
              tal que A[i][j] = A[p[i]][p[j]] para todo i, j?  (Sí / No)

Es el caso A = B del isomorfismo (N1) exigiendo además p != identidad.
Por eso se reutiliza el código de src/n1_isomorfismo.py.

Certificado "Sí": la permutación p.  Se verifica en O(n^2).
Búsqueda exacta: se enumeran las n! permutaciones y se salta la identidad.

Separación de responsabilidades:
    validar_matriz()                      -> lectura/validación (de N1)
    verificar_automorfismo_no_trivial()   -> VERIFICADOR del certificado (polinomial)
    buscar_automorfismo_no_trivial()      -> búsqueda exhaustiva (exacta)
    main()                                -> presentación
"""
from itertools import permutations

from n1_isomorfismo import validar_matriz, verificar_isomorfismo


# ------------------------------------------------------------ verificador
def verificar_automorfismo_no_trivial(A, p):
    """VERIFICADOR del certificado. Tiempo O(n^2), espacio O(n).

    Acepta si p es una permutación de {0..n-1} que preserva la adyacencia
    (es decir, un automorfismo) Y además p no es la identidad.
    """
    n = validar_matriz(A, "A")
    # Reutiliza el verificador de N1 con A = B: comprueba que p es permutación
    # (O(n)) y que A[i][j] = A[p[i]][p[j]] (O(n^2)).
    if not verificar_isomorfismo(A, A, p):
        return False
    return tuple(p) != tuple(range(n))      # la identidad no cuenta (O(n))


# ---------------------------------------------------------------- búsqueda
def buscar_automorfismo_no_trivial(A):
    """Devuelve una permutación certificado o None. Exacto.

    Decisión algorítmica: se prueban todas las permutaciones y se salta la
    identidad (itertools.permutations la genera siempre primero, pero se
    compara en vez de asumir el orden). Cada candidata se comprueba con el
    mismo verificador que usa el certificado: buscar = enumerar + verificar.

    Para n = 0 y n = 1 la única permutación es la identidad, así que se
    devuelve None (no hay automorfismo no trivial). Se compara siempre con
    'is not None'.

    Peor caso (grafo sin simetrías): se agotan las n! - 1 permutaciones no
    triviales. Tiempo O(n! * n^2); espacio O(n) (se generan de a una).
    """
    n = validar_matriz(A, "A")
    identidad = tuple(range(n))
    for p in permutations(range(n)):
        if p == identidad:
            continue
        if verificar_automorfismo_no_trivial(A, p):
            return p
    return None


def tiene_automorfismo_no_trivial(A):
    """Versión de decisión (Sí/No)."""
    return buscar_automorfismo_no_trivial(A) is not None


# ------------------------------------------------------------ presentación
def main():
    # Datos del expediente n4 del simulador: 3 vértices, triángulo
    triangulo = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
    p = buscar_automorfismo_no_trivial(triangulo)
    print("¿El triángulo tiene un automorfismo no trivial?", "Sí" if p is not None else "No")
    if p is not None:
        print("Certificado p (i -> p[i]):", p)
        print("Verificador acepta el certificado:",
              verificar_automorfismo_no_trivial(triangulo, p))
    print("La identidad (0, 1, 2) como certificado:",
          verificar_automorfismo_no_trivial(triangulo, (0, 1, 2)))

    # Camino de 3 nodos: la única simetría no trivial es el espejo
    camino = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
    print("Camino 0-1-2:", buscar_automorfismo_no_trivial(camino))

    # Grafo de 6 vértices sin simetrías no triviales (se agotan las 719 candidatas)
    aristas = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 4), (3, 5)]
    asimetrico = [[0] * 6 for _ in range(6)]
    for u, v in aristas:
        asimetrico[u][v] = asimetrico[v][u] = 1
    print("Grafo asimétrico de 6 vértices:", buscar_automorfismo_no_trivial(asimetrico))


if __name__ == "__main__":
    main()
