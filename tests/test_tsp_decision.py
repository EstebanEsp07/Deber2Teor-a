"""Pruebas de C2 · TSP de decisión. Ejecutar desde la raíz del repo:
    python -m unittest -v tests/test_tsp_decision.py
"""
import contextlib
import io
import json
import os
import random
import sys
import tempfile
import unittest
from itertools import permutations

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from tsp_decision import (  # noqa: E402
    INSTANCIA_CORREO, EntradaInvalida, buscar_exacto, costo_recorrido,
    decidir_heuristico, es_simetrica, leer_instancia, main, optimo_held_karp,
    reducir_ciclo_hamiltoniano, tiene_ciclo_hamiltoniano, verificar,
    vecino_mas_cercano,
)

D_CORREO = INSTANCIA_CORREO["distancias"]
L_CORREO = INSTANCIA_CORREO["limite"]

# Instancia donde la heurística falla: óptimo = 17, vecino más cercano = 23.
D_TRAMPA = [[0, 7, 6, 8], [7, 0, 1, 8], [6, 1, 0, 1], [8, 8, 1, 0]]


def fuerza_bruta(D, L, ciclo=True):
    """Oráculo independiente: enumera todas las permutaciones."""
    n = len(D)
    return any(costo_recorrido(D, (0,) + p, ciclo) <= L for p in permutations(range(1, n)))


class CasosNormales(unittest.TestCase):
    def test_correo_ciclo_responde_si(self):
        r = buscar_exacto(D_CORREO, L_CORREO)
        self.assertTrue(r.existe)
        self.assertEqual(r.costo, 15)
        self.assertTrue(verificar(D_CORREO, L_CORREO, r.recorrido))

    def test_correo_lectura_camino_responde_si(self):
        r = buscar_exacto(D_CORREO, L_CORREO, cerrar_ciclo=False)
        self.assertTrue(r.existe)
        self.assertEqual(r.costo, 7)

    def test_matriz_del_correo_es_simetrica(self):
        self.assertTrue(es_simetrica(D_CORREO))

    def test_optimizacion_separada_de_decision(self):
        orden, c = optimo_held_karp(D_CORREO)
        self.assertEqual(c, 15)
        self.assertTrue(verificar(D_CORREO, c, orden))

    def test_aleatorio_exacto_coincide_con_oraculos(self):
        rnd = random.Random(2026)
        for _ in range(150):
            n = rnd.randint(2, 7)
            D = [[0 if i == j else rnd.randint(1, 20) for j in range(n)] for i in range(n)]
            L = rnd.randint(0, 20 * n)
            for ciclo in (True, False):
                r = buscar_exacto(D, L, ciclo)
                self.assertEqual(r.existe, fuerza_bruta(D, L, ciclo))
                self.assertEqual(r.existe, optimo_held_karp(D, ciclo)[1] <= L)
                if r.existe:
                    self.assertTrue(verificar(D, L, r.recorrido, ciclo))

    def test_heuristica_es_correcta_cuando_dice_si(self):
        rnd = random.Random(7)
        for _ in range(150):
            n = rnd.randint(2, 7)
            D = [[0 if i == j else rnd.randint(1, 20) for j in range(n)] for i in range(n)]
            L = rnd.randint(0, 20 * n)
            veredicto, orden, _ = decidir_heuristico(D, L)
            if veredicto == "SI":
                self.assertTrue(buscar_exacto(D, L).existe)
                self.assertTrue(verificar(D, L, orden))

    def test_heuristica_no_garantiza_encontrar(self):
        self.assertEqual(vecino_mas_cercano(D_TRAMPA)[1], 23)
        self.assertEqual(optimo_held_karp(D_TRAMPA)[1], 17)
        veredicto, _, _ = decidir_heuristico(D_TRAMPA, 17)
        self.assertEqual(veredicto, "NO CONCLUYENTE")
        self.assertTrue(buscar_exacto(D_TRAMPA, 17).existe)


class CasosLimite(unittest.TestCase):
    def test_L_igual_al_optimo_es_si(self):           # "costo <= L" no estricto
        self.assertTrue(buscar_exacto(D_CORREO, 15).existe)

    def test_L_justo_bajo_el_optimo_es_no(self):
        r = buscar_exacto(D_CORREO, 14)
        self.assertFalse(r.existe)
        self.assertIsNone(r.recorrido)

    def test_L_cero(self):
        self.assertFalse(buscar_exacto(D_CORREO, 0).existe)
        self.assertTrue(buscar_exacto([[0, 0], [0, 0]], 0).existe)

    def test_un_solo_centro(self):
        r = buscar_exacto([[0]], 0)
        self.assertTrue(r.existe)
        self.assertEqual((r.recorrido, r.costo), ([0], 0))

    def test_dos_centros(self):
        self.assertTrue(buscar_exacto([[0, 5], [5, 0]], 10).existe)
        self.assertFalse(buscar_exacto([[0, 5], [5, 0]], 9).existe)

    def test_matriz_asimetrica_sentido_importa(self):
        D = [[0, 1, 9], [9, 0, 1], [1, 9, 0]]
        self.assertFalse(es_simetrica(D))
        self.assertTrue(verificar(D, 3, [0, 1, 2]))
        self.assertFalse(verificar(D, 3, [0, 2, 1]))

    def test_pesos_reales(self):
        self.assertTrue(buscar_exacto([[0, 1.5], [1.5, 0]], 3.0).existe)


class Verificador(unittest.TestCase):
    def test_rechaza_certificados_mal_formados(self):
        for cert in ([0, 1], [0, 1, 1], [0, 1, 3], [0, -1, 2], [0, 1, 2, 0],
                     [0, "1", 2], [0, True, 2], [0, 1.0, 2], None, "012"):
            with self.subTest(cert=cert):
                self.assertFalse(verificar(D_CORREO, L_CORREO, cert))

    def test_rechaza_certificado_caro(self):
        self.assertFalse(verificar(D_CORREO, 14, [0, 1, 2]))

    def test_acepta_cualquier_rotacion_del_ciclo(self):
        for cert in ([0, 1, 2], [1, 2, 0], [2, 0, 1], [0, 2, 1]):
            self.assertTrue(verificar(D_CORREO, 15, cert))


class Reduccion(unittest.TestCase):
    def _todos_los_grafos(self, n):
        pares = [(i, j) for i in range(n) for j in range(i + 1, n)]
        for mask in range(1 << len(pares)):
            yield [pares[k] for k in range(len(pares)) if mask >> k & 1]

    def test_equivalencia_exhaustiva_n4_n5(self):
        for n in (4, 5):
            for E in self._todos_los_grafos(n):
                D, L = reducir_ciclo_hamiltoniano(n, E)
                self.assertEqual(tiene_ciclo_hamiltoniano(n, E),
                                 buscar_exacto(D, L).existe, msg=str(E))

    def test_forma_de_la_instancia_reducida(self):
        D, L = reducir_ciclo_hamiltoniano(4, [(0, 1), (1, 2)])
        self.assertEqual(L, 4)
        self.assertTrue(es_simetrica(D))
        n = len(D)
        for i in range(n):            # desigualdad triangular (instancia métrica)
            for j in range(n):
                for k in range(n):
                    self.assertLessEqual(D[i][j], D[i][k] + D[k][j])

    def test_petersen_no_hamiltoniano(self):
        ext = [(i, (i + 1) % 5) for i in range(5)]
        rad = [(i, i + 5) for i in range(5)]
        inn = [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
        D, L = reducir_ciclo_hamiltoniano(10, ext + rad + inn)
        self.assertFalse(buscar_exacto(D, L).existe)

    def test_entradas_invalidas_de_la_reduccion(self):
        for n, E in ((2, [(0, 1)]), (3, [(0, 0)]), (3, [(0, 3)]), (3, [(0,)]),
                     ("3", []), (3, "01"), (True, [])):
            with self.subTest(n=n, E=E):
                with self.assertRaises(EntradaInvalida):
                    reducir_ciclo_hamiltoniano(n, E)


class CasosInvalidos(unittest.TestCase):
    def test_matrices_invalidas(self):
        malas = [[], None, "matriz", [[0, 1], [1]], [[0, -1], [-1, 0]],
                 [[0, float("nan")], [1, 0]], [[0, float("inf")], [1, 0]],
                 [[0, "4"], [4, 0]], [[0, True], [1, 0]], [[1, 2], [2, 0]],
                 [[0, 1, 2], [1, 0, 2]]]
        for D in malas:
            with self.subTest(D=D):
                with self.assertRaises(EntradaInvalida):
                    buscar_exacto(D, 10)

    def test_limites_invalidos(self):
        for L in (-1, "20", None, float("nan"), float("inf"), True):
            with self.subTest(L=L):
                with self.assertRaises(EntradaInvalida):
                    buscar_exacto(D_CORREO, L)

    def test_json_invalidos(self):
        malos = ["{no es json", "[1,2]", '{"limite": 20}',
                 '{"distancias": [[0]]}',
                 '{"distancias": [[0,1],[1,0]], "limite": 5, "centros": ["A"]}',
                 '{"distancias": [[0,1],[1,0]], "limite": 5, "centros": ["A","A"]}',
                 '{"distancias": [[0,1],[1,0]], "limite": 5, "centros": ["A",""]}']
        for t in malos:
            with self.subTest(t=t):
                with self.assertRaises(EntradaInvalida):
                    leer_instancia(t)

    def test_json_valido(self):
        D, L, nombres = leer_instancia(json.dumps(INSTANCIA_CORREO))
        self.assertEqual((D, L, nombres), (D_CORREO, 20, ["Planta", "Quito", "Guayaquil"]))


class Presentacion(unittest.TestCase):
    def test_main_instancia_del_correo(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(main([]), 0)
        self.assertIn("Respuesta: SÍ", buf.getvalue())

    def test_main_archivo_invalido_devuelve_2(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            fh.write('{"distancias": [[0,-3],[-3,0]], "limite": 5}')
        err = io.StringIO()
        try:
            with contextlib.redirect_stderr(err):
                self.assertEqual(main(["--archivo", fh.name]), 2)
        finally:
            os.unlink(fh.name)
        self.assertIn("Error de entrada", err.getvalue())

    def test_main_archivo_inexistente_devuelve_2(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(["--archivo", "/no/existe.json"]), 2)


if __name__ == "__main__":
    unittest.main()
