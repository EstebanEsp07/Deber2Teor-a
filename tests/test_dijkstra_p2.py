"""Pruebas del correo P2 (Marco Cedeño · Transporte) sobre src/dijkstra.py.

Ejecutar desde la raíz del repo:
    python -m unittest tests/test_dijkstra_p2.py -v
"""
import math
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from dijkstra import (TRAMOS_P2, _dijkstra_nucleo, dijkstra,  # noqa: E402
                      existe_ruta_con_costo_max, leer_grafo, ruta_minima)


def costo_de(grafo, ruta):
    """Verificador independiente: suma los pesos de una ruta dada."""
    total = 0
    for u, v in zip(ruta, ruta[1:]):
        pesos = [w for x, w in grafo[u] if x == v]
        if not pesos:
            raise AssertionError(f"no existe el tramo {u} -> {v}")
        total += min(pesos)
    return total


class TestDijkstraP2(unittest.TestCase):
    def setUp(self):
        self.red = leer_grafo(TRAMOS_P2, dirigido=True)

    # ----------------------------------------------------------- casos normales
    def test_distancias_desde_quito(self):
        dist, _ = dijkstra(self.red, "Quito")
        self.assertEqual(
            dist, {"Quito": 0, "Latacunga": 2, "Ambato": 5, "Guayaquil": 8}
        )

    def test_ruta_reportada_a_guayaquil(self):
        self.assertEqual(
            ruta_minima(self.red, "Quito", "Guayaquil"),
            (8, ["Quito", "Latacunga", "Guayaquil"]),
        )

    def test_empate_de_costo_8(self):
        # Las dos rutas del expediente cuestan lo mismo: ambas son óptimas.
        self.assertEqual(costo_de(self.red, ["Quito", "Latacunga", "Guayaquil"]), 8)
        self.assertEqual(costo_de(self.red, ["Quito", "Ambato", "Guayaquil"]), 8)

    def test_desempate_no_depende_del_orden_de_entrada(self):
        # Aunque Ambato se lea primero, Latacunga (dist 2) sale antes de la cola,
        # fija dist[Guayaquil] = 8 y, por el '<' estricto, Ambato no lo reemplaza.
        red_inv = leer_grafo(list(reversed(TRAMOS_P2)), dirigido=True)
        self.assertEqual(
            ruta_minima(red_inv, "Quito", "Guayaquil"),
            (8, ["Quito", "Latacunga", "Guayaquil"]),
        )

    def test_version_de_decision(self):
        self.assertIs(existe_ruta_con_costo_max(self.red, "Quito", "Guayaquil", 8), True)
        self.assertIs(existe_ruta_con_costo_max(self.red, "Quito", "Guayaquil", 7), False)

    # -------------------------------------------------------------- casos límite
    def test_origen_igual_a_destino(self):
        self.assertEqual(ruta_minima(self.red, "Quito", "Quito"), (0, ["Quito"]))

    def test_sin_ruta_en_sentido_contrario(self):
        # Los tramos son dirigidos: no hay ruta de Guayaquil hacia Quito.
        self.assertEqual(ruta_minima(self.red, "Guayaquil", "Quito"), (math.inf, None))
        self.assertIs(existe_ruta_con_costo_max(self.red, "Guayaquil", "Quito", 10**9), False)

    def test_peso_cero_permitido():
        pass

    def test_peso_cero_permitido(self):
        g = leer_grafo(
            [("Quito", "Latacunga", 0), ("Latacunga", "Guayaquil", 6)], dirigido=True
        )
        self.assertEqual(
            ruta_minima(g, "Quito", "Guayaquil"), (6, ["Quito", "Latacunga", "Guayaquil"])
        )

    # ----------------------------------------------------------- casos inválidos
    def test_rechaza_peso_negativo(self):
        with self.assertRaisesRegex(ValueError, "peso negativo"):
            leer_grafo([("Quito", "Ambato", -1)], dirigido=True)

    def test_rechaza_pesos_no_validos(self):
        casos = [
            ("5", TypeError),
            (True, TypeError),
            (math.nan, ValueError),
            (math.inf, ValueError),
        ]
        for peso, error in casos:
            with self.subTest(peso=peso, error=error):
                with self.assertRaises(error):
                    leer_grafo([("Quito", "Ambato", peso)], dirigido=True)

    def test_rechaza_nodo_inexistente(self):
        with self.assertRaisesRegex(ValueError, "no pertenece"):
            ruta_minima(self.red, "Quito", "Cuenca")

    def test_rechaza_limite_no_numerico(self):
        with self.assertRaises(TypeError):
            existe_ruta_con_costo_max(self.red, "Quito", "Guayaquil", "8")

    # ------------------------------------- contraejemplo con peso negativo (§5)
    def test_contraejemplo_peso_negativo_sin_validar(self):
        # Quito->A (1), Quito->B (2), B->A (-2): la ruta real Quito->B->A cuesta 0,
        # pero el núcleo sin validación finaliza A con 1 y ya no lo corrige.
        g = {"Quito": [("A", 1), ("B", 2)], "B": [("A", -2)], "A": []}
        dist, _ = _dijkstra_nucleo(g, "Quito")
        self.assertEqual(dist["A"], 1)  # respuesta incorrecta (la correcta es 0)


if __name__ == "__main__":
    unittest.main()
