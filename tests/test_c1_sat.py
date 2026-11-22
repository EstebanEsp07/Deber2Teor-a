import os, random, sys, unittest
from itertools import combinations, product
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from c1_sat import (validar_formula, verificar_asignacion, resolver_fuerza_bruta,
                    resolver_dpll, es_satisfacible, formatear)

CORREO = [[1, -2], [2, 3]]          # (x1 ∨ ¬x2) ∧ (x2 ∨ x3), n = 3
OCHO_SIGNOS = [[s1 * 1, s2 * 2, s3 * 3]
               for s1 in (1, -1) for s2 in (1, -1) for s3 in (1, -1)]   # insatisfacible


def formula_aleatoria(n, m, semilla):
    """m cláusulas de 3 variables distintas con signo al azar (reproducible)."""
    rng = random.Random(semilla)
    return [[v * rng.choice((1, -1)) for v in rng.sample(range(1, n + 1), 3)]
            for _ in range(m)]


def palomar(palomas, nidos):
    """Principio del palomar: p(i,j) = la paloma i va al nido j. Insatisfacible si palomas > nidos."""
    var = lambda i, j: i * nidos + j + 1
    cls = [[var(i, j) for j in range(nidos)] for i in range(palomas)]
    for j in range(nidos):
        for i1, i2 in combinations(range(palomas), 2):
            cls.append([-var(i1, j), -var(i2, j)])
    return cls, palomas * nidos


def cumple_por_definicion(clausulas, asignacion):
    """Referencia independiente del módulo."""
    return all(any(asignacion[abs(l)] == (l > 0) for l in c) for c in clausulas)


class PruebasNormales(unittest.TestCase):
    def test_caso_del_correo(self):
        a = resolver_dpll(CORREO, 3)
        self.assertIsNotNone(a)
        self.assertTrue(verificar_asignacion(CORREO, 3, a))

    def test_fuerza_bruta_devuelve_la_primera_en_orden_F_T(self):
        self.assertEqual(resolver_fuerza_bruta(CORREO, 3), {1: False, 2: False, 3: True})

    def test_formula_satisfacible_de_tres_literales(self):
        f = [[1, 2, -3], [-1, 2, 3], [1, -2, 3]]
        a = resolver_dpll(f, 3)
        self.assertTrue(verificar_asignacion(f, 3, a))

    def test_formula_insatisfacible(self):
        self.assertIsNone(resolver_dpll(OCHO_SIGNOS, 3))
        self.assertIsNone(resolver_fuerza_bruta(OCHO_SIGNOS, 3))
        self.assertFalse(es_satisfacible(OCHO_SIGNOS, 3))

    def test_dpll_y_fuerza_bruta_coinciden_en_formulas_aleatorias(self):
        for semilla in range(60):
            n = 6 + semilla % 5
            f = formula_aleatoria(n, round(4.26 * n), semilla)
            bruta = resolver_fuerza_bruta(f, n)
            dpll = resolver_dpll(f, n)
            self.assertEqual(bruta is not None, dpll is not None, msg=f"semilla {semilla}")
            if dpll is not None:
                self.assertTrue(cumple_por_definicion(f, dpll))

    def test_palomar_insatisfacible(self):
        for palomas, nidos in ((2, 1), (3, 2), (4, 3)):
            f, n = palomar(palomas, nidos)
            self.assertIsNone(resolver_dpll(f, n), msg=f"{palomas} palomas, {nidos} nidos")

    def test_palomar_satisfacible_si_caben(self):
        f, n = palomar(3, 3)
        self.assertTrue(verificar_asignacion(f, n, resolver_dpll(f, n)))

    def test_no_modifica_la_entrada(self):
        f = [[1, -2], [2, 3], [-1, 3]]
        copia = [list(c) for c in f]
        resolver_dpll(f, 3)
        self.assertEqual(f, copia)

    def test_formatear(self):
        self.assertEqual(formatear(CORREO), "(x1 ∨ ¬x2) ∧ (x2 ∨ x3)")


class PruebasLimite(unittest.TestCase):
    def test_sin_clausulas_es_satisfacible(self):
        self.assertEqual(resolver_dpll([], 3), {1: False, 2: False, 3: False})
        self.assertIsNotNone(resolver_fuerza_bruta([], 2))

    def test_sin_variables_ni_clausulas(self):
        self.assertEqual(resolver_dpll([], 0), {})            # {} es falso: usar 'is not None'
        self.assertTrue(es_satisfacible([], 0))
        self.assertEqual(resolver_fuerza_bruta([], 0), {})

    def test_clausula_vacia_es_insatisfacible(self):
        self.assertIsNone(resolver_dpll([[]], 0))
        self.assertIsNone(resolver_dpll([[1, 2], []], 2))
        self.assertIsNone(resolver_fuerza_bruta([[]], 2))

    def test_variables_que_no_aparecen_quedan_asignadas(self):
        a = resolver_dpll([[1]], 5)
        self.assertEqual(set(a), {1, 2, 3, 4, 5})
        self.assertTrue(a[1])
        self.assertTrue(verificar_asignacion([[1]], 5, a))

    def test_clausulas_unitarias_contradictorias(self):
        self.assertIsNone(resolver_dpll([[1], [-1]], 1))

    def test_literales_repetidos_y_tautologia(self):
        self.assertTrue(es_satisfacible([[1, 1, 1]], 1))
        self.assertTrue(es_satisfacible([[1, -1]], 1))
        self.assertFalse(es_satisfacible([[1, 1, 1], [-1, -1, -1]], 1))

    def test_cadena_de_implicaciones_se_resuelve_por_propagacion(self):
        n = 300
        f = [[1]] + [[-k, k + 1] for k in range(1, n)]
        a = resolver_dpll(f, n)
        self.assertTrue(all(a[k] for k in range(1, n + 1)))

    def test_exhaustivo_todas_las_formulas_de_dos_clausulas_sobre_3_variables(self):
        # todas las cláusulas posibles de a lo sumo 2 literales distintos sobre 3 variables
        literales = [1, -1, 2, -2, 3, -3]
        posibles = [[]] + [[l] for l in literales] + [list(p) for p in combinations(literales, 2)]
        for c1, c2 in product(posibles, repeat=2):
            f = [c1, c2]
            self.assertEqual(es_satisfacible(f, 3), resolver_fuerza_bruta(f, 3) is not None,
                             msg=str(f))


class PruebasVerificador(unittest.TestCase):
    def test_asignacion_valida(self):
        self.assertTrue(verificar_asignacion(CORREO, 3, {1: True, 2: True, 3: False}))

    def test_asignacion_que_viola_una_clausula(self):
        self.assertFalse(verificar_asignacion(CORREO, 3, {1: False, 2: True, 3: False}))  # viola la 1.ª
        self.assertFalse(verificar_asignacion(CORREO, 3, {1: True, 2: False, 3: False}))  # viola la 2.ª

    def test_asignacion_incompleta_o_con_variables_de_mas(self):
        self.assertFalse(verificar_asignacion(CORREO, 3, {1: True, 2: True}))
        self.assertFalse(verificar_asignacion(CORREO, 3, {1: True, 2: True, 3: True, 4: True}))
        self.assertFalse(verificar_asignacion(CORREO, 3, {0: True, 1: True, 2: True}))

    def test_valores_que_no_son_booleanos(self):
        self.assertFalse(verificar_asignacion(CORREO, 3, {1: 1, 2: 1, 3: 0}))
        self.assertFalse(verificar_asignacion(CORREO, 3, {1: "True", 2: True, 3: True}))

    def test_asignacion_que_no_es_dict(self):
        self.assertFalse(verificar_asignacion(CORREO, 3, [True, True, False]))
        self.assertFalse(verificar_asignacion(CORREO, 3, None))

    def test_clausula_vacia_nunca_se_cumple(self):
        self.assertFalse(verificar_asignacion([[]], 1, {1: True}))

    def test_sin_clausulas_se_cumple(self):
        self.assertTrue(verificar_asignacion([], 2, {1: False, 2: False}))


class PruebasInvalidas(unittest.TestCase):
    def test_mas_de_tres_literales(self):
        with self.assertRaises(ValueError):
            resolver_dpll([[1, 2, 3, 4]], 4)

    def test_literal_cero_o_fuera_de_rango(self):
        with self.assertRaises(ValueError):
            validar_formula([[0, 1]], 2)
        with self.assertRaises(ValueError):
            validar_formula([[1, 4]], 3)
        with self.assertRaises(ValueError):
            validar_formula([[-4]], 3)

    def test_tipos_de_literal(self):
        for malo in (1.5, "1", None, True):
            with self.assertRaises(TypeError):
                validar_formula([[malo]], 3)

    def test_clausula_mal_formada(self):
        with self.assertRaises(ValueError):
            validar_formula([5], 3)
        with self.assertRaises(ValueError):
            validar_formula(["x1"], 3)

    def test_formula_que_no_es_lista(self):
        with self.assertRaises(TypeError):
            resolver_dpll("x1", 1)

    def test_n_invalido(self):
        with self.assertRaises(ValueError):
            resolver_dpll([], -1)
        for malo in (2.0, "3", None, True):
            with self.assertRaises(TypeError):
                resolver_dpll([], malo)

    def test_el_verificador_valida_la_formula(self):
        with self.assertRaises(ValueError):
            verificar_asignacion([[1, 2, 3, 4]], 4, {1: True, 2: True, 3: True, 4: True})


if __name__ == "__main__":
    unittest.main(verbosity=2)
