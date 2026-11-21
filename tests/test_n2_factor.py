import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from n2_factor import (buscar_factor, leer_instancia, tiene_factor,
                       validar_instancia, verificar_factor)


# ------------------------------------------------------------ normales
class PruebasNormales(unittest.TestCase):
    def test_caso_del_correo(self):
        d = buscar_factor(91, 10)          # 91 = 7 * 13
        self.assertEqual(d, 7)
        self.assertTrue(verificar_factor(91, 10, d))

    def test_primo_sin_factor_en_el_intervalo(self):
        self.assertIsNone(buscar_factor(97, 10))
        self.assertFalse(tiene_factor(97, 10))

    def test_compuesto_par(self):
        self.assertEqual(buscar_factor(100, 50), 2)

    def test_el_otro_factor_queda_fuera_del_intervalo(self):
        # 13 divide a 91 pero 13 > B = 10: no es certificado válido
        self.assertFalse(verificar_factor(91, 10, 13))
        self.assertTrue(verificar_factor(91, 13, 13))

    def test_certificado_que_no_divide(self):
        self.assertFalse(verificar_factor(91, 10, 5))


# -------------------------------------------------------------- límite
class PruebasLimite(unittest.TestCase):
    def test_intervalo_vacio(self):
        for B in (0, 1):
            self.assertIsNone(buscar_factor(91, B))

    def test_N_igual_a_1(self):
        self.assertIsNone(buscar_factor(1, 100))

    def test_N_igual_a_B_cuenta_a_N_como_divisor(self):
        # lectura literal del correo: d = N es divisor con 2 <= d <= B
        self.assertEqual(buscar_factor(97, 97), 97)
        self.assertTrue(verificar_factor(97, 97, 97))

    def test_B_justo_debajo_de_N_primo(self):
        self.assertIsNone(buscar_factor(97, 96))

    def test_extremos_del_intervalo(self):
        self.assertTrue(verificar_factor(15, 5, 5))      # d = B
        self.assertTrue(verificar_factor(14, 7, 2))      # d = 2
        self.assertFalse(verificar_factor(15, 5, 1))     # d = 1 fuera
        self.assertFalse(verificar_factor(15, 5, 6))     # d = B + 1 fuera

    def test_d_cero_o_negativo_no_rompe_con_division_por_cero(self):
        self.assertFalse(verificar_factor(91, 10, 0))
        self.assertFalse(verificar_factor(91, 10, -7))

    def test_N_grande_el_verificador_es_inmediato(self):
        p1, p2 = 2 ** 31 - 1, 2 ** 61 - 1
        self.assertTrue(verificar_factor(p1 * p2, p1, p1))
        self.assertFalse(verificar_factor(p1 * p2, p1 - 1, p1))   # d > B

    def test_certificado_mal_formado_se_rechaza_sin_excepcion(self):
        for malo in ("7", 7.0, None, True, [7]):
            self.assertFalse(verificar_factor(91, 10, malo), repr(malo))

    def test_lectura_decimal_y_binaria(self):
        self.assertEqual(leer_instancia("91", "10"), (91, 10))
        self.assertEqual(leer_instancia("0b1011011", "0b1010"), (91, 10))

    def test_consistencia_exhaustiva_busqueda_vs_verificador(self):
        # para N en 1..120 y B en 0..40: la búsqueda devuelve el MENOR
        # certificado válido, o None si ningún d lo es
        for N in range(1, 121):
            for B in range(0, 41):
                validos = [d for d in range(-2, 50)
                           if verificar_factor(N, B, d)]
                esperado = min(validos) if validos else None
                self.assertEqual(buscar_factor(N, B), esperado, (N, B))


# ----------------------------------------------------------- inválidas
class PruebasInvalidas(unittest.TestCase):
    def test_N_cero_o_negativo(self):
        for N in (0, -91):
            with self.assertRaises(ValueError):
                buscar_factor(N, 10)

    def test_B_negativo(self):
        with self.assertRaises(ValueError):
            buscar_factor(91, -1)
        with self.assertRaises(ValueError):
            verificar_factor(91, -1, 7)

    def test_tipos_incorrectos(self):
        for N, B in ((91.0, 10), (91, 10.5), ("91", 10), (None, 10),
                     (True, 10), (91, False)):
            with self.assertRaises(TypeError, msg=repr((N, B))):
                validar_instancia(N, B)

    def test_lectura_invalida(self):
        for t in ("abc", "", "9 1", "1.5"):
            with self.assertRaises(ValueError, msg=repr(t)):
                leer_instancia(t, "10")
        with self.assertRaises(TypeError):
            leer_instancia(91, "10")


if __name__ == "__main__":
    unittest.main(verbosity=2)
