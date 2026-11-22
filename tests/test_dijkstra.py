import os, random, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from dijkstra import (INF, leer_grafo, bloquear, dijkstra, ruta_minima,
                      existe_ruta_con_costo_max, _dijkstra_nucleo,
                      PASILLOS_PLANTA, TRAMOS_P2)

PLANTA = leer_grafo(PASILLOS_PLANTA, dirigido=False)
P2 = leer_grafo(TRAMOS_P2, dirigido=True)


def costo_de(grafo, ruta):
    """Suma los pesos de una ruta y comprueba que cada tramo existe."""
    total = 0
    for u, v in zip(ruta, ruta[1:]):
        pesos = [w for x, w in grafo[u] if x == v]
        assert pesos, f"el tramo {u}->{v} no existe"
        total += min(pesos)
    return total


def bellman_ford(grafo, origen):
    """Referencia independiente (admite pesos negativos sin ciclos negativos)."""
    vertices = set(grafo)
    for suc in grafo.values():
        vertices.update(v for v, _ in suc)
    dist = {v: INF for v in vertices}
    dist[origen] = 0
    for _ in range(len(vertices) - 1):
        for u, suc in grafo.items():
            for v, w in suc:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
    return dist


class PruebasNormales(unittest.TestCase):
    def test_planta_R_a_D(self):
        costo, ruta = ruta_minima(PLANTA, "R", "D")
        self.assertEqual(costo, 11)
        # Empate: hay DOS rutas óptimas de 11 m. Con '<' estricto el
        # predecesor de E queda en A (llegó primero con 8).
        self.assertEqual(ruta, ["R", "B", "A", "E", "D"])
        self.assertEqual(costo_de(PLANTA, ruta), 11)
        # La ruta resaltada en la Figura 5 también cuesta 11 (es la otra óptima)
        self.assertEqual(costo_de(PLANTA, ["R", "B", "A", "P", "E", "D"]), 11)

    def test_planta_todas_las_distancias(self):
        dist, _ = dijkstra(PLANTA, "R")
        self.assertEqual(dist, {"R": 0, "B": 2, "A": 3, "C": 5,
                                "P": 6, "E": 8, "D": 11})

    def test_planta_con_bloqueos(self):
        self.assertEqual(ruta_minima(bloquear(PLANTA, ["P"]), "R", "D"),
                         (11, ["R", "B", "A", "E", "D"]))
        self.assertEqual(ruta_minima(bloquear(PLANTA, ["A", "P"]), "R", "D"),
                         (12, ["R", "B", "C", "E", "D"]))

    def test_correo_p2(self):
        dist, _ = dijkstra(P2, "Quito")
        self.assertEqual(dist, {"Quito": 0, "Latacunga": 2,
                                "Ambato": 5, "Guayaquil": 8})
        costo, ruta = ruta_minima(P2, "Quito", "Guayaquil")
        self.assertEqual((costo, ruta), (8, ["Quito", "Latacunga", "Guayaquil"]))
        # La alternativa por Ambato empata en 8
        self.assertEqual(costo_de(P2, ["Quito", "Ambato", "Guayaquil"]), 8)

    def test_version_decision(self):
        self.assertTrue(existe_ruta_con_costo_max(PLANTA, "R", "D", 11))
        self.assertFalse(existe_ruta_con_costo_max(PLANTA, "R", "D", 10))

    def test_coincide_con_bellman_ford_en_grafos_aleatorios(self):
        rnd = random.Random(2026)
        for _ in range(200):
            n = rnd.randint(1, 9)
            aristas = [(rnd.randrange(n), rnd.randrange(n), rnd.randint(0, 9))
                       for _ in range(rnd.randint(0, 20))]
            g = leer_grafo(aristas, dirigido=rnd.random() < 0.5)
            g.setdefault(0, [])
            dist, pred = dijkstra(g, 0)
            self.assertEqual(dist, bellman_ford(g, 0))
            for v in dist:                       # cada ruta reconstruida
                if dist[v] < INF:                # cuesta lo que dice dist
                    _, ruta = ruta_minima(g, 0, v)
                    self.assertEqual(costo_de(g, ruta), dist[v])


class PruebasLimite(unittest.TestCase):
    def test_origen_igual_destino(self):
        self.assertEqual(ruta_minima(PLANTA, "R", "R"), (0, ["R"]))

    def test_sin_ruta_por_bloqueo(self):
        # D solo se conecta con E: bloquear E deja a D aislado
        self.assertEqual(ruta_minima(bloquear(PLANTA, ["E"]), "R", "D"), (INF, None))
        self.assertFalse(existe_ruta_con_costo_max(bloquear(PLANTA, ["E"]), "R", "D", 10**9))

    def test_sin_ruta_por_direccion(self):
        self.assertEqual(ruta_minima(P2, "Guayaquil", "Quito"), (INF, None))

    def test_pesos_cero(self):
        g = leer_grafo([("A", "B", 0), ("B", "C", 0), ("A", "C", 1)], dirigido=True)
        self.assertEqual(ruta_minima(g, "A", "C"), (0, ["A", "B", "C"]))

    def test_vertice_aislado_y_lazo(self):
        g = leer_grafo([("A", "A", 5), ("A", "B", 1)], dirigido=True)
        g["Z"] = []
        self.assertEqual(ruta_minima(g, "A", "Z"), (INF, None))
        self.assertEqual(ruta_minima(g, "A", "B"), (1, ["A", "B"]))

    def test_cadena_larga_sin_recursion(self):
        n = 50_000
        g = leer_grafo([(i, i + 1, 1) for i in range(n)], dirigido=True)
        costo, ruta = ruta_minima(g, 0, n)
        self.assertEqual((costo, len(ruta)), (n, n + 1))


class PruebasInvalidas(unittest.TestCase):
    def test_peso_negativo_rechazado(self):
        with self.assertRaises(ValueError):
            leer_grafo([("A", "B", -1)])
        with self.assertRaises(ValueError):             # también si llega
            dijkstra({"A": [("B", -1)]}, "A")           # como dict directo

    def test_contraejemplo_negativo_explica_el_rechazo(self):
        # Sin la validación, Dijkstra finaliza Latacunga con 2 y no la
        # vuelve a procesar cuando Ambato ofrece 5 + (-4) = 1.
        g = {"Quito": [("Latacunga", 2), ("Ambato", 5)],
             "Ambato": [("Latacunga", -4)],
             "Latacunga": [("Guayaquil", 6)], "Guayaquil": []}
        dist_dijkstra, _ = _dijkstra_nucleo(g, "Quito")
        dist_real = bellman_ford(g, "Quito")
        self.assertEqual(dist_dijkstra["Guayaquil"], 8)   # respuesta incorrecta
        self.assertEqual(dist_real["Guayaquil"], 7)       # Quito-Ambato-Latacunga-Guayaquil

    def test_nodo_inexistente(self):
        with self.assertRaises(ValueError):
            ruta_minima(PLANTA, "R", "Z")
        with self.assertRaises(ValueError):
            dijkstra(PLANTA, "Z")

    def test_origen_bloqueado(self):
        with self.assertRaises(ValueError):
            ruta_minima(bloquear(PLANTA, ["R"]), "R", "D")

    def test_bloquear_zona_inexistente(self):
        with self.assertRaises(ValueError):
            bloquear(PLANTA, ["Z"])

    def test_pesos_no_numericos_o_no_finitos(self):
        for malo in ("3", None, True, float("nan"), float("inf")):
            with self.assertRaises((TypeError, ValueError)):
                leer_grafo([("A", "B", malo)])

    def test_estructura_mal_formada(self):
        with self.assertRaises(TypeError):
            leer_grafo("AB3")
        with self.assertRaises(ValueError):
            leer_grafo([("A", "B")])
        with self.assertRaises(TypeError):
            dijkstra([("A", "B", 1)], "A")
        with self.assertRaises(TypeError):
            existe_ruta_con_costo_max(PLANTA, "R", "D", "11")


if __name__ == "__main__":
    unittest.main(verbosity=2)
