import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from reposicion import calcular_posicion, sugerir_reposicion, sugerir_catalogo


class PruebasNormales(unittest.TestCase):
    def test_ejemplo_del_deber(self):
        self.assertEqual(sugerir_reposicion(18, 10, 5, 30, 50), (23, 27))

    def test_posicion_comoda_no_sugiere(self):
        self.assertEqual(sugerir_reposicion(80, 0, 10, 30, 50), (70, 0))

    def test_calcular_posicion(self):
        self.assertEqual(calcular_posicion(18, 10, 5), 23)

    def test_catalogo_conserva_el_orden(self):
        filas = [("A", 18, 10, 5, 30, 50), ("B", 80, 0, 10, 30, 50)]
        self.assertEqual(sugerir_catalogo(filas), [("A", 23, 27), ("B", 70, 0)])


class PruebasAntiDuplicacion(unittest.TestCase):
    def test_tras_emitir_la_orden_ya_no_sugiere(self):
        pos, sug = sugerir_reposicion(18, 10, 5, 30, 50)
        pos2, sug2 = sugerir_reposicion(18, 10 + sug, 5, 30, 50)
        self.assertEqual((pos2, sug2), (50, 0))

    def test_orden_previa_resta_a_la_sugerencia_sin_pasarse_del_objetivo(self):
        _, sin_orden = sugerir_reposicion(18, 0, 5, 30, 50)       # pediría 37
        _, con_orden = sugerir_reposicion(18, 10, 5, 30, 50)      # pide 27
        self.assertEqual(sin_orden, 37)
        self.assertEqual(10 + con_orden, sin_orden)

    def test_orden_abierta_suficiente_evita_la_sugerencia(self):
        self.assertEqual(sugerir_reposicion(18, 20, 5, 30, 50)[1], 0)   # posición 33 > 30


class PruebasLimite(unittest.TestCase):
    def test_posicion_igual_al_minimo_si_sugiere(self):
        self.assertEqual(sugerir_reposicion(30, 0, 0, 30, 50), (30, 20))

    def test_posicion_un_punto_sobre_el_minimo_no_sugiere(self):
        self.assertEqual(sugerir_reposicion(31, 0, 0, 30, 50), (31, 0))

    def test_posicion_negativa(self):
        self.assertEqual(sugerir_reposicion(5, 0, 20, 30, 50), (-15, 65))

    def test_todo_en_cero(self):
        self.assertEqual(sugerir_reposicion(0, 0, 0, 0, 0), (0, 0))

    def test_minimo_cero_y_objetivo_positivo(self):
        self.assertEqual(sugerir_reposicion(0, 0, 0, 0, 10), (0, 10))

    def test_objetivo_igual_al_minimo(self):
        self.assertEqual(sugerir_reposicion(10, 0, 0, 30, 30), (10, 20))

    def test_catalogo_vacio(self):
        self.assertEqual(sugerir_catalogo([]), [])


class PruebasInvalidas(unittest.TestCase):
    def test_negativos(self):
        with self.assertRaises(ValueError):
            sugerir_reposicion(-1, 0, 0, 30, 50)
        with self.assertRaises(ValueError):
            sugerir_reposicion(1, -2, 0, 30, 50)
        with self.assertRaises(ValueError):
            sugerir_reposicion(1, 0, -3, 30, 50)
        with self.assertRaises(ValueError):
            sugerir_reposicion(1, 0, 0, -30, 50)

    def test_tipos(self):
        for malo in (1.5, "3", None, True):
            with self.assertRaises(TypeError):
                sugerir_reposicion(malo, 0, 0, 30, 50)

    def test_objetivo_menor_que_minimo(self):
        with self.assertRaises(ValueError):
            sugerir_reposicion(10, 0, 0, 50, 30)

    def test_fila_mal_formada(self):
        with self.assertRaises(ValueError):
            sugerir_catalogo([("A", 1, 2)])
        with self.assertRaises(TypeError):
            sugerir_catalogo("A")


if __name__ == "__main__":
    unittest.main(verbosity=2)
