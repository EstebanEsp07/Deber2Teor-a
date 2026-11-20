import os, random, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from n1_isomorfismo import (validar_matriz, verificar_isomorfismo,
                            buscar_isomorfismo, son_isomorfos)

CAMINO = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
ESTRELLA = [[0, 1, 1], [1, 0, 0], [1, 0, 0]]
TRIANGULO = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]


def ciclo(n):
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        a, b = i, (i + 1) % n
        M[a][b] = M[b][a] = 1
    return M


def union_ciclos(n1, n2):
    n = n1 + n2
    M = [[0] * n for _ in range(n)]
    for m, off in ((n1, 0), (n2, n1)):
        for i in range(m):
            a, b = off + i, off + (i + 1) % m
            M[a][b] = M[b][a] = 1
    return M


def permutar(A, p):
    n = len(A)
    B = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            B[p[i]][p[j]] = A[i][j]
    return B


class PruebasNormales(unittest.TestCase):
    def test_caso_simulador(self):
        p = buscar_isomorfismo(CAMINO, ESTRELLA)
        self.assertIsNotNone(p)
        self.assertTrue(verificar_isomorfismo(CAMINO, ESTRELLA, p))

    def test_identidad(self):
        self.assertEqual(buscar_isomorfismo(TRIANGULO, TRIANGULO), (0, 1, 2))

    def test_no_isomorfos_distinto_numero_de_aristas(self):
        self.assertFalse(son_isomorfos(CAMINO, TRIANGULO))

    def test_reetiquetado_aleatorio(self):
        rng = random.Random(2026)
        A = [[0, 1, 1, 0, 0, 0], [1, 0, 0, 1, 0, 0], [1, 0, 0, 0, 1, 0],
             [0, 1, 0, 0, 0, 1], [0, 0, 1, 0, 0, 1], [0, 0, 0, 1, 1, 0]]
        for _ in range(5):
            q = list(range(6)); rng.shuffle(q)
            B = permutar(A, q)
            p = buscar_isomorfismo(A, B)
            self.assertIsNotNone(p)
            self.assertTrue(verificar_isomorfismo(A, B, p))


class PruebasLimite(unittest.TestCase):
    def test_misma_secuencia_de_grados_no_isomorfos(self):
        # C6 vs C3+C3: ambos 2-regulares con 6 nodos; el filtro de grados
        # NO los separa y hay que agotar las 720 permutaciones.
        self.assertFalse(son_isomorfos(ciclo(6), union_ciclos(3, 3)))

    def test_tamanos_distintos(self):
        self.assertIsNone(buscar_isomorfismo(CAMINO, [[0]]))

    def test_grafo_vacio_y_un_nodo(self):
        self.assertEqual(buscar_isomorfismo([], []), ())
        self.assertTrue(son_isomorfos([], []))
        self.assertEqual(buscar_isomorfismo([[0]], [[0]]), (0,))

    def test_sin_aristas(self):
        Z = [[0] * 4 for _ in range(4)]
        self.assertTrue(son_isomorfos(Z, Z))


class PruebasVerificador(unittest.TestCase):
    def test_certificado_valido(self):
        self.assertTrue(verificar_isomorfismo(CAMINO, ESTRELLA, (1, 0, 2)))

    def test_no_es_permutacion(self):
        self.assertFalse(verificar_isomorfismo(CAMINO, ESTRELLA, (0, 0, 2)))
        self.assertFalse(verificar_isomorfismo(CAMINO, ESTRELLA, (0, 1, 3)))

    def test_longitud_incorrecta(self):
        self.assertFalse(verificar_isomorfismo(CAMINO, ESTRELLA, (0, 1)))

    def test_permutacion_que_no_preserva(self):
        self.assertFalse(verificar_isomorfismo(CAMINO, ESTRELLA, (0, 1, 2)))


class PruebasInvalidas(unittest.TestCase):
    def test_no_cuadrada(self):
        with self.assertRaises(ValueError):
            validar_matriz([[0, 1], [1]])

    def test_valores_no_binarios(self):
        with self.assertRaises(ValueError):
            validar_matriz([[0, 2], [2, 0]])

    def test_asimetrica(self):
        with self.assertRaises(ValueError):
            validar_matriz([[0, 1], [0, 0]])

    def test_lazo(self):
        with self.assertRaises(ValueError):
            validar_matriz([[1, 0], [0, 0]])

    def test_tipo(self):
        with self.assertRaises(TypeError):
            buscar_isomorfismo("abc", CAMINO)


if __name__ == "__main__":
    unittest.main(verbosity=2)
