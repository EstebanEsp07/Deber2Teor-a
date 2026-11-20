"""
N1 · ¿Existe isomorfismo entre dos redes?  (Elena Ruiz · Arquitectura)

Problema de decisión (isomorfismo de grafos, GI):
    Entrada : dos grafos G1, G2 no dirigidos y simples, como matrices de
              adyacencia n x n (0/1, simétricas, diagonal en 0).
    Pregunta: ¿existe una biyección p: V1 -> V2 tal que
              A[i][j] = B[p[i]][p[j]] para todo i, j?  (Sí / No)

Certificado "Sí": la permutación p.  Se verifica en O(n^2).
Búsqueda exacta: se enumeran las n! permutaciones (exponencial).

Separación de responsabilidades:
    validar_matriz()          -> lectura/validación
    verificar_isomorfismo()   -> VERIFICADOR del certificado (polinomial)
    buscar_isomorfismo()      -> búsqueda exhaustiva (exacta)
    main()                    -> presentación
"""
from itertools import permutations


# ------------------------------------------------------------ validación
def validar_matriz(M, nombre="M"):
    """Comprueba que M es matriz de adyacencia de un grafo simple no dirigido.
    Devuelve n. Lanza ValueError/TypeError si la entrada es inválida."""
    if not isinstance(M, (list, tuple)):
        raise TypeError(f"{nombre} debe ser una lista de filas")
    n = len(M)
    for fila in M:
        if not isinstance(fila, (list, tuple)) or len(fila) != n:
            raise ValueError(f"{nombre} no es una matriz cuadrada")
    for i in range(n):
        for j in range(n):
            if M[i][j] not in (0, 1):
                raise ValueError(f"{nombre}[{i}][{j}] debe ser 0 o 1")
        if M[i][i] != 0:
            raise ValueError(f"{nombre} tiene un lazo en el vértice {i}")
        for j in range(i + 1, n):
            if M[i][j] != M[j][i]:
                raise ValueError(f"{nombre} no es simétrica en ({i},{j})")
    return n


def _preserva(A, B, p):
    n = len(A)
    return all(A[i][j] == B[p[i]][p[j]] for i in range(n) for j in range(n))


# ------------------------------------------------------------ verificador
def verificar_isomorfismo(A, B, p):
    """VERIFICADOR del certificado. Tiempo O(n^2), espacio O(n).

    Acepta si p es una permutación de {0..n-1} que preserva adyacencia.
    """
    n = validar_matriz(A, "A")
    if validar_matriz(B, "B") != n or len(p) != n:
        return False
    visto = [False] * n
    for x in p:                       # ¿p es biyección sobre {0..n-1}?
        if not isinstance(x, int) or not 0 <= x < n or visto[x]:
            return False
        visto[x] = True
    return _preserva(A, B, p)


# ---------------------------------------------------------------- búsqueda
def buscar_isomorfismo(A, B):
    """Devuelve una permutación certificado o None. Exacto.

    OJO: para n = 0 devuelve () (tupla vacía, falsa en Python); comparar
    siempre con 'is not None'.

    Filtro previo (condición necesaria, no suficiente): igual tamaño e igual
    secuencia de grados. No cambia el peor caso: sigue siendo O(n! * n^2)
    tiempo y O(n) espacio (las permutaciones se generan de a una).
    """
    n = validar_matriz(A, "A")
    if validar_matriz(B, "B") != n:
        return None
    if sorted(map(sum, A)) != sorted(map(sum, B)):
        return None
    for p in permutations(range(n)):
        if _preserva(A, B, p):
            return p
    return None


def son_isomorfos(A, B):
    """Versión de decisión (Sí/No)."""
    return buscar_isomorfismo(A, B) is not None


# ------------------------------------------------------------ presentación
def main():
    # Datos del expediente n1 del simulador (3 nodos, 2 enlaces cada red)
    A = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]   # camino 0-1-2
    B = [[0, 1, 1], [1, 0, 0], [1, 0, 0]]   # estrella centrada en 0
    p = buscar_isomorfismo(A, B)
    print("¿A y B son isomorfas?", "Sí" if p is not None else "No")
    if p is not None:
        print("Certificado p (i -> p[i]):", p)
        print("Verificador acepta el certificado:", verificar_isomorfismo(A, B, p))

    triangulo = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
    print("¿Camino de 3 nodos vs triángulo?", son_isomorfos(A, triangulo))


if __name__ == "__main__":
    main()
