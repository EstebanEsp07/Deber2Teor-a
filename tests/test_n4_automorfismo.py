import os, sys, unittest
from itertools import combinations, permutations
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from n4_automorfismo import (verificar_automorfismo_no_trivial,
                             buscar_automorfismo_no_trivial,
                             tiene_automorfismo_no_trivial)

TRIANGULO = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
CAMINO = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]


def desde_aristas(n, aristas):
    M = [[0] * n for _ in range(n)]
    for u, v in aristas:
        M[u][v] = M[v][u] = 1
    return M


# Grafo de 6 vértices sin automorfismos no triviales (hallado por fuerza bruta)
ASIMETRICO = desde_aristas(6, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 4), (3, 5)])


def contar_automorfismos(A):
    """Referencia independiente del módulo: cuenta TODOS los automorfismos
    (incluida la identidad) comparando directamente la definición."""
    n = len(A)
    return sum(1 for p in permutations(range(n))
               if all(A[i][j] == A[p[i]][p[j]] for i in range(n) for j in range(n)))


class PruebasNormales(unittest.TestCase):
    def test_caso_simulador_triangulo(self):
        p = buscar_automorfismo_no_trivial(TRIANGULO)
        self.assertIsNotNone(p)
        self.assertNotEqual(p, (0, 1, 2))
        self.assertTrue(verificar_automorfismo_no_trivial(TRIANGULO, p))

    def test_camino_solo_tiene_el_espejo(self):
        self.assertEqual(buscar_automorfismo_no_trivial(CAMINO), (2, 1, 0))
        self.assertEqual(contar_automorfismos(CAMINO), 2)   # identidad + espejo

    def test_ciclo_de_cinco(self):
        C5 = desde_aristas(5, [(i, (i + 1) % 5) for i in range(5)])
        self.assertTrue(tiene_automorfismo_no_trivial(C5))

    def test_coincide_con_conteo_independiente_en_todos_los_grafos_de_hasta_5_nodos(self):
        # Exhaustivo: 1 + 2 + 8 + 64 + 1024 grafos (n = 1..5, con n = 0 aparte).
        for n in range(1, 6):
            pares = list(combinations(range(n), 2))
            for mascara in range(1 << len(pares)):
                A = desde_aristas(n, [pares[k] for k in range(len(pares)) if mascara >> k & 1])
                esperado = contar_automorfismos(A) > 1
                self.assertEqual(tiene_automorfismo_no_trivial(A), esperado, msg=str(A))


class PruebasLimite(unittest.TestCase):
    def test_grafo_asimetrico_de_6_nodos_no_tiene(self):
        self.assertIsNone(buscar_automorfismo_no_trivial(ASIMETRICO))
        self.assertEqual(contar_automorfismos(ASIMETRICO), 1)   # solo la identidad

    def test_grafo_vacio_y_un_nodo(self):
        self.assertIsNone(buscar_automorfismo_no_trivial([]))
        self.assertFalse(tiene_automorfismo_no_trivial([]))
        self.assertIsNone(buscar_automorfismo_no_trivial([[0]]))

    def test_dos_nodos_siempre_tienen_el_intercambio(self):
        self.assertEqual(buscar_automorfismo_no_trivial([[0, 1], [1, 0]]), (1, 0))
        self.assertEqual(buscar_automorfismo_no_trivial([[0, 0], [0, 0]]), (1, 0))

    def test_sin_aristas(self):
        Z = [[0] * 4 for _ in range(4)]
        self.assertTrue(tiene_automorfismo_no_trivial(Z))

    def test_completo_de_cuatro(self):
        K4 = [[0 if i == j else 1 for j in range(4)] for i in range(4)]
        self.assertTrue(tiene_automorfismo_no_trivial(K4))
        self.assertEqual(contar_automorfismos(K4), 24)


class PruebasVerificador(unittest.TestCase):
    def test_certificado_valido(self):
        self.assertTrue(verificar_automorfismo_no_trivial(TRIANGULO, (0, 2, 1)))
        self.assertTrue(verificar_automorfismo_no_trivial(CAMINO, [2, 1, 0]))   # lista también

    def test_la_identidad_se_rechaza_aunque_sea_automorfismo(self):
        self.assertTrue(contar_automorfismos(TRIANGULO) > 1)
        self.assertFalse(verificar_automorfismo_no_trivial(TRIANGULO, (0, 1, 2)))
        self.assertFalse(verificar_automorfismo_no_trivial(CAMINO, (0, 1, 2)))

    def test_no_es_permutacion(self):
        self.assertFalse(verificar_automorfismo_no_trivial(TRIANGULO, (0, 0, 2)))
        self.assertFalse(verificar_automorfismo_no_trivial(TRIANGULO, (0, 1, 3)))

    def test_longitud_incorrecta(self):
        self.assertFalse(verificar_automorfismo_no_trivial(TRIANGULO, (0, 1)))
        self.assertFalse(verificar_automorfismo_no_trivial(TRIANGULO, (1, 0, 2, 3)))

    def test_permutacion_que_no_preserva_adyacencia(self):
        # En el camino 0-1-2 el nodo central no puede moverse
        self.assertFalse(verificar_automorfismo_no_trivial(CAMINO, (1, 0, 2)))

    def test_ningun_certificado_sirve_en_el_asimetrico(self):
        for p in permutations(range(6)):
            self.assertFalse(verificar_automorfismo_no_trivial(ASIMETRICO, p))


class PruebasInvalidas(unittest.TestCase):
    def test_no_cuadrada(self):
        with self.assertRaises(ValueError):
            buscar_automorfismo_no_trivial([[0, 1], [1]])

    def test_valores_no_binarios(self):
        with self.assertRaises(ValueError):
            buscar_automorfismo_no_trivial([[0, 2], [2, 0]])

    def test_asimetrica_como_matriz(self):
        with self.assertRaises(ValueError):
            buscar_automorfismo_no_trivial([[0, 1], [0, 0]])

    def test_lazo(self):
        with self.assertRaises(ValueError):
            buscar_automorfismo_no_trivial([[1, 0], [0, 0]])

    def test_tipo(self):
        with self.assertRaises(TypeError):
            buscar_automorfismo_no_trivial("abc")
        with self.assertRaises(TypeError):
            verificar_automorfismo_no_trivial(None, (0, 1))

    def test_verificador_valida_la_matriz(self):
        with self.assertRaises(ValueError):
            verificar_automorfismo_no_trivial([[0, 1], [0, 0]], (1, 0))


if __name__ == "__main__":
    unittest.main(verbosity=2)
