import os, random, sys, unittest
from itertools import combinations, product
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from c3_vertex_cover import (validar_grafo, verificar_cobertura, buscar_cobertura,
                             buscar_fuerza_bruta, es_coberturable, cobertura_minima,
                             reduccion_3sat_a_vertex_cover)

CORREO = {"A": ["B"], "B": ["A", "C"], "C": ["B"]}      # aristas A-B y B-C


def desde_aristas(vertices, aristas):
    g = {v: [] for v in vertices}
    for u, v in aristas:
        g[u].append(v)
        g[v].append(u)
    return g


def cubre_por_definicion(grafo, conjunto):
    """Referencia independiente del módulo."""
    return all(u in conjunto or v in conjunto for u in grafo for v in grafo[u])


def tamano_minimo_por_definicion(grafo):
    vertices = list(grafo)
    for tam in range(len(vertices) + 1):
        for cand in combinations(vertices, tam):
            if cubre_por_definicion(grafo, set(cand)):
                return tam


def satisfacible_por_definicion(clausulas, n):
    """Fuerza bruta propia de la prueba (no depende de c1_sat.py)."""
    for bits in product([False, True], repeat=n):
        if all(any(bits[abs(l) - 1] == (l > 0) for l in c) for c in clausulas):
            return True
    return False


class PruebasNormales(unittest.TestCase):
    def test_caso_del_correo(self):
        cob = buscar_cobertura(CORREO, 1)
        self.assertEqual(cob, ["B"])
        self.assertTrue(verificar_cobertura(CORREO, 1, cob))

    def test_k_cero_en_el_correo_es_no(self):
        self.assertIsNone(buscar_cobertura(CORREO, 0))
        self.assertFalse(es_coberturable(CORREO, 0))

    def test_triangulo_necesita_dos(self):
        T = desde_aristas("ABC", [("A", "B"), ("B", "C"), ("A", "C")])
        self.assertIsNone(buscar_cobertura(T, 1))
        self.assertEqual(len(buscar_cobertura(T, 2)), 2)

    def test_estrella_se_cubre_con_el_centro(self):
        S = desde_aristas(range(5), [(0, i) for i in range(1, 5)])
        self.assertEqual(buscar_cobertura(S, 1), [0])

    def test_ciclo_de_cinco_necesita_tres(self):
        C5 = desde_aristas(range(5), [(i, (i + 1) % 5) for i in range(5)])
        self.assertIsNone(buscar_cobertura(C5, 2))
        self.assertTrue(verificar_cobertura(C5, 3, buscar_cobertura(C5, 3)))

    def test_cobertura_minima(self):
        K4 = desde_aristas(range(4), list(combinations(range(4), 2)))
        self.assertEqual(len(cobertura_minima(K4)), 3)
        P4 = desde_aristas(range(4), [(0, 1), (1, 2), (2, 3)])
        self.assertEqual(len(cobertura_minima(P4)), 2)
        self.assertEqual(cobertura_minima(CORREO), ["B"])

    def test_ramificacion_coincide_con_la_referencia_en_todos_los_grafos_de_hasta_5_vertices(self):
        # Exhaustivo: 1 + 2 + 8 + 64 + 1024 grafos, todo k de 0 a n.
        for n in range(1, 6):
            vertices = list(range(n))
            pares = list(combinations(vertices, 2))
            for mascara in range(1 << len(pares)):
                g = desde_aristas(vertices, [pares[i] for i in range(len(pares)) if mascara >> i & 1])
                minimo = tamano_minimo_por_definicion(g)
                for k in range(n + 1):
                    cob = buscar_cobertura(g, k)
                    self.assertEqual(cob is not None, k >= minimo, msg=f"{g} k={k}")
                    if cob is not None:
                        self.assertTrue(cubre_por_definicion(g, set(cob)))
                        self.assertLessEqual(len(cob), k)
                    self.assertEqual(buscar_fuerza_bruta(g, k) is not None, k >= minimo)
                self.assertEqual(len(cobertura_minima(g)), minimo)

    def test_grafos_aleatorios_contra_la_referencia(self):
        rng = random.Random(2026)
        for _ in range(40):
            n = rng.randint(6, 10)
            aristas = [p for p in combinations(range(n), 2) if rng.random() < 0.3]
            g = desde_aristas(range(n), aristas)
            minimo = tamano_minimo_por_definicion(g)
            for k in (max(0, minimo - 1), minimo):
                self.assertEqual(es_coberturable(g, k), k >= minimo)


class PruebasLimite(unittest.TestCase):
    def test_grafo_vacio(self):
        self.assertEqual(buscar_cobertura({}, 0), [])           # [] es falso: usar 'is not None'
        self.assertTrue(es_coberturable({}, 0))
        self.assertEqual(cobertura_minima({}), [])

    def test_sin_aristas(self):
        g = {"A": [], "B": [], "C": []}
        self.assertEqual(buscar_cobertura(g, 0), [])
        self.assertEqual(cobertura_minima(g), [])

    def test_un_vertice_aislado(self):
        self.assertTrue(es_coberturable({"A": []}, 0))

    def test_una_sola_arista(self):
        g = {"A": ["B"], "B": ["A"]}
        self.assertIsNone(buscar_cobertura(g, 0))
        self.assertEqual(buscar_cobertura(g, 1), ["A"])

    def test_k_mayor_o_igual_que_el_numero_de_vertices(self):
        K4 = desde_aristas(range(4), list(combinations(range(4), 2)))
        self.assertTrue(es_coberturable(K4, 4))
        self.assertTrue(es_coberturable(K4, 100))

    def test_k_exacto_en_el_borde(self):
        C5 = desde_aristas(range(5), [(i, (i + 1) % 5) for i in range(5)])
        self.assertFalse(es_coberturable(C5, 2))
        self.assertTrue(es_coberturable(C5, 3))

    def test_vertices_con_nombres_distintos_tipos(self):
        g = {1: ["x"], "x": [1]}
        self.assertTrue(es_coberturable(g, 1))

    def test_resultado_reproducible(self):
        g = desde_aristas(range(6), [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (0, 5)])
        self.assertEqual(buscar_cobertura(g, 3), buscar_cobertura(g, 3))

    def test_camino_largo_con_k_justo(self):
        # Un camino de 24 vértices se cubre con 12. La ramificación no aprovecha
        # la estructura del camino y explora hasta 2^12 ramas: sigue siendo rápido.
        n = 24
        g = desde_aristas(range(n), [(i, i + 1) for i in range(n - 1)])
        cob = buscar_cobertura(g, n // 2)
        self.assertIsNotNone(cob)
        self.assertTrue(verificar_cobertura(g, n // 2, cob))
        self.assertIsNone(buscar_cobertura(g, n // 2 - 1))

    def test_no_modifica_el_grafo(self):
        g = {"A": ["B", "C"], "B": ["A"], "C": ["A"]}
        copia = {u: list(v) for u, v in g.items()}
        buscar_cobertura(g, 1)
        self.assertEqual(g, copia)


class PruebasVerificador(unittest.TestCase):
    def test_certificados_validos(self):
        self.assertTrue(verificar_cobertura(CORREO, 1, ["B"]))
        self.assertTrue(verificar_cobertura(CORREO, 1, ("B",)))
        self.assertTrue(verificar_cobertura(CORREO, 2, {"A", "C"}))

    def test_deja_una_arista_sin_cubrir(self):
        self.assertFalse(verificar_cobertura(CORREO, 1, ["A"]))      # falta B-C
        self.assertFalse(verificar_cobertura(CORREO, 1, ["C"]))      # falta A-B

    def test_excede_k(self):
        self.assertFalse(verificar_cobertura(CORREO, 1, ["A", "C"]))
        self.assertFalse(verificar_cobertura(CORREO, 0, ["B"]))

    def test_vertice_que_no_existe(self):
        self.assertFalse(verificar_cobertura(CORREO, 2, ["B", "Z"]))

    def test_repetidos_no_son_un_conjunto(self):
        self.assertFalse(verificar_cobertura(CORREO, 2, ["B", "B"]))

    def test_certificado_de_tipo_incorrecto(self):
        self.assertFalse(verificar_cobertura(CORREO, 1, "B"))
        self.assertFalse(verificar_cobertura(CORREO, 1, None))
        self.assertFalse(verificar_cobertura(CORREO, 1, [["B"]]))     # elemento no hashable

    def test_seleccion_vacia(self):
        self.assertFalse(verificar_cobertura(CORREO, 1, []))
        self.assertTrue(verificar_cobertura({"A": []}, 0, []))

    def test_el_verificador_es_independiente_de_la_busqueda(self):
        g = desde_aristas(range(4), [(0, 1), (1, 2), (2, 3)])
        # una cobertura válida que la ramificación no devolvería primero
        self.assertTrue(verificar_cobertura(g, 2, [0, 2]))
        self.assertTrue(verificar_cobertura(g, 2, [1, 3]))
        self.assertTrue(verificar_cobertura(g, 2, [1, 2]))


class PruebasReduccion(unittest.TestCase):
    def test_tamano_de_la_construccion(self):
        formula = [[1, -2, 3], [-1, 2, 2]]
        g, k = reduccion_3sat_a_vertex_cover(formula, 3)
        aristas = validar_grafo(g)
        self.assertEqual((len(g), len(aristas), k), (2 * 3 + 3 * 2, 3 + 6 * 2, 3 + 2 * 2))

    def test_formula_del_correo_c1_es_satisfacible(self):
        g, k = reduccion_3sat_a_vertex_cover([[1, -2, -2], [2, 3, 3]], 3)
        self.assertTrue(es_coberturable(g, k))

    def test_formula_insatisfacible(self):
        f = [[1, 2, 2], [-1, 2, 2], [1, -2, -2], [-1, -2, -2]]
        g, k = reduccion_3sat_a_vertex_cover(f, 2)
        self.assertFalse(es_coberturable(g, k))

    def test_equivalencia_en_todas_las_formulas_de_2_clausulas_sobre_2_variables(self):
        # cláusulas de 3 literales con 4 literales posibles: 4^3 = 64; pares: 64^2 = 4096
        literales = [1, -1, 2, -2]
        clausulas = [list(c) for c in product(literales, repeat=3)]
        for c1, c2 in product(clausulas, repeat=2):
            f = [c1, c2]
            g, k = reduccion_3sat_a_vertex_cover(f, 2)
            self.assertEqual(es_coberturable(g, k), satisfacible_por_definicion(f, 2), msg=str(f))

    def test_equivalencia_en_formulas_aleatorias_de_3_variables(self):
        rng = random.Random(7)
        for _ in range(40):
            m = rng.randint(1, 3)
            f = [[v * rng.choice((1, -1)) for v in rng.sample(range(1, 4), 3)] for _ in range(m)]
            g, k = reduccion_3sat_a_vertex_cover(f, 3)
            self.assertEqual(es_coberturable(g, k), satisfacible_por_definicion(f, 3), msg=str(f))

    def test_sin_variables_ni_clausulas(self):
        g, k = reduccion_3sat_a_vertex_cover([], 0)
        self.assertEqual((g, k), ({}, 0))
        self.assertTrue(es_coberturable(g, k))

    def test_clausula_que_no_tiene_tres_literales(self):
        with self.assertRaises(ValueError):
            reduccion_3sat_a_vertex_cover([[1, 2]], 2)
        with self.assertRaises(ValueError):
            reduccion_3sat_a_vertex_cover([[1, 2, 1, 2]], 2)

    def test_literal_invalido(self):
        with self.assertRaises(ValueError):
            reduccion_3sat_a_vertex_cover([[1, 0, 2]], 2)
        with self.assertRaises(ValueError):
            reduccion_3sat_a_vertex_cover([[1, 2, 3]], 2)
        with self.assertRaises(TypeError):
            reduccion_3sat_a_vertex_cover([[1, 2, 1.5]], 2)
        with self.assertRaises(TypeError):
            reduccion_3sat_a_vertex_cover("x", 2)


class PruebasInvalidas(unittest.TestCase):
    def test_no_es_diccionario(self):
        with self.assertRaises(TypeError):
            buscar_cobertura([("A", "B")], 1)

    def test_vecinos_que_no_son_lista(self):
        with self.assertRaises(TypeError):
            buscar_cobertura({"A": "B", "B": ["A"]}, 1)
        with self.assertRaises(TypeError):
            buscar_cobertura({"A": {"B"}, "B": ["A"]}, 1)

    def test_vecino_que_no_es_vertice(self):
        with self.assertRaises(ValueError):
            buscar_cobertura({"A": ["Z"]}, 1)

    def test_lazo(self):
        with self.assertRaises(ValueError):
            buscar_cobertura({"A": ["A"]}, 1)

    def test_no_simetrico(self):
        with self.assertRaises(ValueError):
            buscar_cobertura({"A": ["B"], "B": []}, 1)

    def test_vecinos_repetidos(self):
        with self.assertRaises(ValueError):
            buscar_cobertura({"A": ["B", "B"], "B": ["A"]}, 1)

    def test_k_negativo(self):
        with self.assertRaises(ValueError):
            buscar_cobertura(CORREO, -1)

    def test_k_de_tipo_incorrecto(self):
        for malo in (1.5, "1", None, True):
            with self.assertRaises(TypeError):
                buscar_cobertura(CORREO, malo)

    def test_el_verificador_valida_el_grafo_y_k(self):
        with self.assertRaises(ValueError):
            verificar_cobertura({"A": ["B"], "B": []}, 1, ["A"])
        with self.assertRaises(ValueError):
            verificar_cobertura(CORREO, -1, ["B"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
