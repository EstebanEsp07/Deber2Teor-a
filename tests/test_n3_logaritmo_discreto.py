import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from n3_logaritmo_discreto import (buscar_dlog, es_primo, existe_dlog,
                                   leer_instancia, validar_instancia,
                                   verificar_dlog)


def primos_hasta(n):
    """Criba de Eratóstenes, referencia independiente para es_primo."""
    es = [True] * (n + 1)
    es[0:2] = [False, False]
    for i in range(2, int(n ** 0.5) + 1):
        if es[i]:
            for j in range(i * i, n + 1, i):
                es[j] = False
    return [i for i, v in enumerate(es) if v]


# ------------------------------------------------------------ normales
class PruebasNormales(unittest.TestCase):
    def test_caso_del_correo(self):
        x = buscar_dlog(23, 5, 8, 10)      # 5^6 = 15625 ≡ 8 (mod 23)
        self.assertEqual(x, 6)
        self.assertTrue(verificar_dlog(23, 5, 8, 10, x))

    def test_verificador_rechaza_exponentes_incorrectos(self):
        for x in (0, 1, 2, 3, 4, 5, 7, 8, 9, 10):
            self.assertFalse(verificar_dlog(23, 5, 8, 10, x), x)

    def test_solucion_fuera_de_la_cota(self):
        # la solución x = 6 existe pero B = 5 no la deja entrar
        self.assertIsNone(buscar_dlog(23, 5, 8, 5))
        self.assertFalse(existe_dlog(23, 5, 8, 5))
        self.assertFalse(verificar_dlog(23, 5, 8, 5, 6))   # pow coincide, x > B

    def test_g_y_h_se_toman_modulo_p(self):
        self.assertEqual(buscar_dlog(23, 5 + 23, 8 + 2 * 23, 10), 6)
        self.assertEqual(buscar_dlog(23, 5 - 23, 8 - 23, 10), 6)   # negativos
        self.assertTrue(verificar_dlog(23, 5 + 23, 8 + 23, 10, 6))

    def test_sin_solucion(self):
        # las potencias de 2 mod 7 son {1, 2, 4}: h = 3 nunca aparece
        self.assertIsNone(buscar_dlog(7, 2, 3, 100))


# -------------------------------------------------------------- límite
class PruebasLimite(unittest.TestCase):
    def test_x_igual_a_0(self):
        self.assertEqual(buscar_dlog(23, 5, 1, 10), 0)
        self.assertTrue(existe_dlog(23, 5, 1, 10))     # 0 es certificado válido
        self.assertTrue(verificar_dlog(23, 5, 1, 10, 0))

    def test_x_igual_a_B(self):
        self.assertEqual(buscar_dlog(23, 5, 8, 6), 6)
        self.assertTrue(verificar_dlog(23, 5, 8, 6, 6))

    def test_B_igual_a_0(self):
        self.assertEqual(buscar_dlog(23, 5, 1, 0), 0)
        self.assertIsNone(buscar_dlog(23, 5, 8, 0))

    def test_g_multiplo_de_p(self):
        # g ≡ 0: la sucesión es 1, 0, 0, 0, ... (convención g^0 = 1)
        self.assertEqual(buscar_dlog(7, 7, 0, 3), 1)
        self.assertEqual(buscar_dlog(7, 7, 1, 3), 0)
        self.assertIsNone(buscar_dlog(7, 7, 2, 3))
        self.assertTrue(verificar_dlog(7, 14, 0, 3, 1))

    def test_h_cero_con_g_coprimo_no_tiene_solucion(self):
        self.assertIsNone(buscar_dlog(23, 5, 0, 50))

    def test_p_igual_a_2(self):
        self.assertEqual(buscar_dlog(2, 1, 1, 5), 0)
        self.assertIsNone(buscar_dlog(2, 1, 0, 5))

    def test_periodicidad_B_mayor_que_p(self):
        # la solución mínima nunca supera p - 1 cuando g no es múltiplo de p
        self.assertEqual(buscar_dlog(23, 5, 8, 10 ** 4), 6)

    def test_verificador_con_B_enorme_es_inmediato(self):
        p, g = 2 ** 61 - 1, 3
        B, x0 = 2 ** 1000, 2 ** 999 + 12345
        h = pow(g, x0, p)
        self.assertTrue(verificar_dlog(p, g, h, B, x0))
        self.assertFalse(verificar_dlog(p, g, h, B, x0 + 1))
        self.assertFalse(verificar_dlog(p, g, h, B, B + 1))   # fuera de la cota

    def test_certificado_mal_formado_se_rechaza_sin_excepcion(self):
        for malo in ("6", 6.0, None, True, [6], -1, 11):
            self.assertFalse(verificar_dlog(23, 5, 8, 10, malo), repr(malo))

    def test_lectura_decimal_y_hexadecimal(self):
        self.assertEqual(leer_instancia("23", "5", "8", "10"), (23, 5, 8, 10))
        self.assertEqual(leer_instancia("0x17", "0b101", "8", "0xa"),
                         (23, 5, 8, 10))

    def test_consistencia_exhaustiva_busqueda_vs_verificador(self):
        # para todo primo p < 50, g y h en [0, p) y B en {0, 3, 10}:
        # la búsqueda devuelve el MENOR certificado válido, o None
        for p in primos_hasta(49):
            for g in range(p):
                for h in range(p):
                    for B in (0, 3, 10):
                        validos = [x for x in range(B + 1)
                                   if verificar_dlog(p, g, h, B, x)]
                        esperado = validos[0] if validos else None
                        self.assertEqual(buscar_dlog(p, g, h, B), esperado,
                                         (p, g, h, B))


# --------------------------------------------------------- primalidad
class PruebasPrimalidad(unittest.TestCase):
    def test_coincide_con_la_criba_hasta_10000(self):
        primos = set(primos_hasta(10_000))
        for n in range(-5, 10_001):
            self.assertEqual(es_primo(n), n in primos, n)

    def test_numeros_de_carmichael_y_pseudoprimos_fuertes(self):
        # compuestos que engañan a tests débiles (Fermat, o MR con pocas bases)
        for c in (561, 1105, 1729, 2465, 6601, 41041, 3_215_031_751,
                  3_825_123_056_546_413_051):
            self.assertFalse(es_primo(c), c)

    def test_primos_grandes(self):
        for q in (2 ** 31 - 1, 2 ** 61 - 1, 10 ** 18 + 9):
            self.assertTrue(es_primo(q), q)

    def test_mas_alla_del_limite_se_rechaza(self):
        with self.assertRaises(ValueError):
            es_primo(2 ** 89 - 1)          # primo, pero fuera de la garantía

    def test_tipo(self):
        with self.assertRaises(TypeError):
            es_primo(7.0)


# ----------------------------------------------------------- inválidas
class PruebasInvalidas(unittest.TestCase):
    def test_p_no_primo(self):
        for p in (15, 1, 0, -7, 561):
            with self.assertRaises(ValueError, msg=str(p)):
                buscar_dlog(p, 2, 3, 5)
            with self.assertRaises(ValueError, msg=str(p)):
                verificar_dlog(p, 2, 3, 5, 1)

    def test_B_negativo(self):
        with self.assertRaises(ValueError):
            buscar_dlog(23, 5, 8, -1)

    def test_tipos_incorrectos(self):
        for args in ((23.0, 5, 8, 10), (23, 5.5, 8, 10), (23, 5, "8", 10),
                     (23, 5, 8, None), (True, 5, 8, 10), (23, 5, 8, 10.0)):
            with self.assertRaises(TypeError, msg=repr(args)):
                validar_instancia(*args)

    def test_p_fuera_del_limite_de_primalidad(self):
        with self.assertRaises(ValueError):
            buscar_dlog(2 ** 89 - 1, 3, 5, 10)

    def test_lectura_invalida(self):
        with self.assertRaises(ValueError):
            leer_instancia("23", "cinco", "8", "10")
        with self.assertRaises(TypeError):
            leer_instancia(23, "5", "8", "10")


if __name__ == "__main__":
    unittest.main(verbosity=2)
