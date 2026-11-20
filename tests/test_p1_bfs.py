import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from p1_bfs import leer_red, camino_bfs, alcanzable

RED = leer_red([("Durán", "Quito"), ("Durán", "Guayaquil"),
                ("Quito", "Norte"), ("Guayaquil", "Sur")])


class PruebasNormales(unittest.TestCase):
    def test_alcanzable_con_ruta(self):
        self.assertTrue(alcanzable(RED, "Durán", "Norte"))
        self.assertEqual(camino_bfs(RED, "Durán", "Norte"),
                         ["Durán", "Quito", "Norte"])

    def test_no_alcanzable(self):
        self.assertFalse(alcanzable(RED, "Quito", "Sur"))

    def test_direccion_importa(self):
        self.assertTrue(alcanzable(RED, "Durán", "Norte"))
        self.assertFalse(alcanzable(RED, "Norte", "Durán"))

    def test_menos_aristas(self):
        g = leer_red([("A", "B"), ("B", "C"), ("C", "D"), ("A", "D")])
        self.assertEqual(camino_bfs(g, "A", "D"), ["A", "D"])


class PruebasLimite(unittest.TestCase):
    def test_origen_igual_destino(self):
        self.assertEqual(camino_bfs(RED, "Norte", "Norte"), ["Norte"])

    def test_ciclo_termina(self):
        g = leer_red([("A", "B"), ("B", "A"), ("C", "C")])
        self.assertFalse(alcanzable(g, "A", "C"))

    def test_destino_solo_como_valor(self):
        # formato del simulador: 'Norte' no es clave del diccionario
        g = {"Durán": ["Quito"], "Quito": ["Norte"]}
        self.assertTrue(alcanzable(g, "Durán", "Norte"))

    def test_cadena_larga_sin_recursion(self):
        n = 50_000
        g = leer_red([(i, i + 1) for i in range(n)])
        self.assertEqual(len(camino_bfs(g, 0, n)), n + 1)


class PruebasInvalidas(unittest.TestCase):
    def test_nodo_inexistente(self):
        with self.assertRaises(ValueError):
            alcanzable(RED, "Durán", "Cuenca")
        with self.assertRaises(ValueError):
            alcanzable(RED, "Cuenca", "Norte")

    def test_red_vacia(self):
        with self.assertRaises(ValueError):
            alcanzable({}, "A", "A")

    def test_tipo_de_grafo(self):
        with self.assertRaises(TypeError):
            alcanzable([("A", "B")], "A", "B")

    def test_arista_mal_formada(self):
        with self.assertRaises(ValueError):
            leer_red([("A", "B", 3)])
        with self.assertRaises(TypeError):
            leer_red("AB")


if __name__ == "__main__":
    unittest.main(verbosity=2)
