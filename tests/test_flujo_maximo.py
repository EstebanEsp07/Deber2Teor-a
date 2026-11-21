"""Pruebas unitarias de P3 · flujo máximo con Edmonds–Karp.
Ejecutar desde la raíz del repositorio:
    python -m unittest discover -s tests -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from flujo_maximo import (DATOS_P3, construir_red, corte_minimo, edmonds_karp,  # noqa: E402
                          existe_flujo_al_menos, leer_aristas_csv)


def red_de(aristas):
    return construir_red(aristas)


class PropiedadesDeFlujo:
    """Comprobaciones comunes: capacidad, conservación y corte = flujo."""

    def verificar_flujo_valido(self, red, r, s, t):
        for (u, v), f in r.flujo_por_arista.items():
            self.assertGreaterEqual(f, 0)
            self.assertLessEqual(f, red[u][v])
        for x in red:
            if x in (s, t):
                continue
            entra = sum(f for (u, v), f in r.flujo_por_arista.items() if v == x)
            sale = sum(f for (u, v), f in r.flujo_por_arista.items() if u == x)
            self.assertEqual(entra, sale, f"conservación falla en {x}")
        sale_s = sum(f for (u, v), f in r.flujo_por_arista.items() if u == s)
        entra_s = sum(f for (u, v), f in r.flujo_por_arista.items() if v == s)
        self.assertEqual(sale_s - entra_s, r.valor)
        self.assertEqual(r.valor, r.capacidad_corte)  # teorema flujo máx = corte mín


class TestCasoP3(unittest.TestCase, PropiedadesDeFlujo):
    """Casos normales: los datos del expediente, sin modificar."""

    def setUp(self):
        self.red = construir_red(leer_aristas_csv(DATOS_P3))
        self.r = edmonds_karp(self.red, "Planta", "Clientes")

    def test_valor_flujo_maximo(self):
        self.assertEqual(self.r.valor, 10)

    def test_no_es_la_suma_de_salidas(self):
        # El correo advierte: salida de Planta = 7 + 5 = 12, pero llegan 10.
        self.assertEqual(sum(self.red["Planta"].values()), 12)
        self.assertLess(self.r.valor, 12)

    def test_traza_caminos_aumentantes(self):
        caminos = [(a.camino, a.cuello) for a in self.r.aumentos]
        self.assertEqual(caminos, [
            (["Planta", "Quito", "Clientes"], 4),
            (["Planta", "Guayaquil", "Clientes"], 5),
            (["Planta", "Quito", "Guayaquil", "Clientes"], 1),
        ])

    def test_corte_minimo(self):
        self.assertEqual(self.r.lado_s, ["Guayaquil", "Planta", "Quito"])
        self.assertEqual(sorted(self.r.corte),
                         [("Guayaquil", "Clientes", 6), ("Quito", "Clientes", 4)])
        self.assertEqual(self.r.capacidad_corte, 10)

    def test_flujo_valido(self):
        self.verificar_flujo_valido(self.red, self.r, "Planta", "Clientes")

    def test_version_decision(self):
        self.assertTrue(existe_flujo_al_menos(self.red, "Planta", "Clientes", 10))
        self.assertFalse(existe_flujo_al_menos(self.red, "Planta", "Clientes", 11))
        self.assertTrue(existe_flujo_al_menos(self.red, "Planta", "Clientes", 0))

    def test_lectura_csv_equivale_a_tuplas(self):
        directo = red_de([("Planta", "Quito", 7), ("Planta", "Guayaquil", 5),
                          ("Quito", "Clientes", 4), ("Guayaquil", "Clientes", 6),
                          ("Quito", "Guayaquil", 2)])
        self.assertEqual(directo, self.red)


class TestCasosLimite(unittest.TestCase, PropiedadesDeFlujo):

    def test_destino_inalcanzable_flujo_cero(self):
        red = red_de([("s", "a", 3), ("b", "t", 4)])
        r = edmonds_karp(red, "s", "t")
        self.assertEqual(r.valor, 0)
        self.assertEqual(r.aumentos, [])
        self.assertEqual(r.capacidad_corte, 0)

    def test_arista_capacidad_cero(self):
        red = red_de([("s", "t", 0)])
        self.assertEqual(edmonds_karp(red, "s", "t").valor, 0)

    def test_una_sola_arista(self):
        red = red_de([("s", "t", 9)])
        r = edmonds_karp(red, "s", "t")
        self.assertEqual(r.valor, 9)
        self.assertEqual(len(r.aumentos), 1)

    def test_aristas_repetidas_se_suman(self):
        red = red_de([("s", "t", 2), ("s", "t", 3)])
        self.assertEqual(red["s"]["t"], 5)
        self.assertEqual(edmonds_karp(red, "s", "t").valor, 5)

    def test_aristas_antiparalelas(self):
        red = red_de([("s", "a", 4), ("a", "b", 3), ("b", "a", 2), ("b", "t", 5), ("s", "b", 1)])
        r = edmonds_karp(red, "s", "t")
        self.assertEqual(r.valor, 4)
        self.verificar_flujo_valido(red, r, "s", "t")

    def test_necesita_arista_inversa(self):
        # Ejemplo clásico donde un camino debe "deshacer" flujo por la inversa.
        red = red_de([("s", "a", 1), ("s", "b", 1), ("a", "b", 1),
                      ("a", "t", 1), ("b", "t", 1)])
        r = edmonds_karp(red, "s", "t")
        self.assertEqual(r.valor, 2)
        self.verificar_flujo_valido(red, r, "s", "t")

    def test_capacidades_enormes_no_afectan_iteraciones(self):
        # Ford–Fulkerson con DFS podría necesitar ~2·10^18 aumentos;
        # Edmonds–Karp usa caminos más cortos: 2 aumentos.
        M = 10 ** 18
        red = red_de([("s", "a", M), ("s", "b", M), ("a", "b", 1),
                      ("a", "t", M), ("b", "t", M)])
        r = edmonds_karp(red, "s", "t")
        self.assertEqual(r.valor, 2 * M)
        self.assertEqual(len(r.aumentos), 2)

    def test_cota_de_aumentos(self):
        # Número de aumentos <= V·E / 2 (lema de Edmonds–Karp), red en capas.
        aristas = []
        for i in range(6):
            aristas.append(("s", f"a{i}", 3))
            for j in range(6):
                aristas.append((f"a{i}", f"b{j}", 1))
            aristas.append((f"b{i}", "t", 3))
        red = red_de(aristas)
        r = edmonds_karp(red, "s", "t")
        V, E = len(red), len(aristas)
        self.assertEqual(r.valor, 18)
        self.assertLessEqual(len(r.aumentos), V * E // 2)
        self.verificar_flujo_valido(red, r, "s", "t")

    def test_corte_minimo_funcion_directa(self):
        red = red_de([("s", "a", 2), ("a", "t", 1)])
        r = edmonds_karp(red, "s", "t")
        S, corte, cap = corte_minimo(red, r.residual, "s")
        self.assertEqual(S, ["a", "s"])
        self.assertEqual(corte, [("a", "t", 1)])
        self.assertEqual(cap, 1)

    def test_csv_con_lineas_vacias_y_sin_cabecera(self):
        aristas = leer_aristas_csv("\n s , t , 3 \n\n")
        self.assertEqual(aristas, [("s", "t", 3)])


class TestEntradasInvalidas(unittest.TestCase):

    def test_capacidad_negativa(self):
        with self.assertRaises(ValueError):
            construir_red([("s", "t", -1)])

    def test_capacidad_no_entera(self):
        for c in (2.5, "3", True, None):
            with self.subTest(c=c), self.assertRaises(ValueError):
                construir_red([("s", "t", c)])

    def test_nombre_vacio(self):
        with self.assertRaises(ValueError):
            construir_red([("", "t", 1)])

    def test_lazo(self):
        with self.assertRaises(ValueError):
            construir_red([("s", "s", 1)])

    def test_arista_mal_formada(self):
        with self.assertRaises(ValueError):
            construir_red([("s", "t")])

    def test_origen_igual_destino(self):
        with self.assertRaises(ValueError):
            edmonds_karp(red_de([("s", "t", 1)]), "s", "s")

    def test_extremos_inexistentes(self):
        red = red_de([("s", "t", 1)])
        with self.assertRaises(ValueError):
            edmonds_karp(red, "X", "t")
        with self.assertRaises(ValueError):
            edmonds_karp(red, "s", "Y")

    def test_csv_campos_incorrectos(self):
        with self.assertRaises(ValueError):
            leer_aristas_csv("origen,destino,capacidad\nPlanta,Quito")

    def test_csv_capacidad_texto(self):
        with self.assertRaises(ValueError):
            leer_aristas_csv("Planta,Quito,siete")

    def test_csv_no_texto(self):
        with self.assertRaises(TypeError):
            leer_aristas_csv(None)

    def test_red_no_diccionario(self):
        with self.assertRaises(TypeError):
            edmonds_karp([("s", "t", 1)], "s", "t")

    def test_K_invalido(self):
        red = red_de([("s", "t", 1)])
        for K in (-1, 1.5, True):
            with self.subTest(K=K), self.assertRaises(ValueError):
                existe_flujo_al_menos(red, "s", "t", K)


if __name__ == "__main__":
    unittest.main(verbosity=2)
