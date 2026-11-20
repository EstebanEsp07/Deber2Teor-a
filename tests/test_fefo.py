import os, random, sys, unittest
from datetime import date, datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from fefo import leer_lotes, plan_fefo

HOY = date(2026, 11, 19)


class PruebasNormales(unittest.TestCase):
    def test_toma_primero_el_que_vence_antes(self):
        lotes = [("B", "2026-12-20", 10), ("A", "2026-12-01", 10)]
        r = plan_fefo(lotes, 5, HOY)
        self.assertEqual(r.plan, [("A", 5)])
        self.assertTrue(r.aceptado)
        self.assertEqual(r.faltante, 0)

    def test_pedido_que_abarca_varios_lotes(self):
        lotes = [("A", "2026-12-01", 30), ("B", "2026-12-10", 25), ("C", "2027-01-01", 40)]
        r = plan_fefo(lotes, 70, HOY)
        self.assertEqual(r.plan, [("A", 30), ("B", 25), ("C", 15)])
        self.assertEqual(sum(c for _, c in r.plan), 70)

    def test_no_modifica_la_entrada(self):
        lotes = [("B", "2026-12-20", 10), ("A", "2026-12-01", 10)]
        copia = list(lotes)
        plan_fefo(lotes, 15, HOY)
        self.assertEqual(lotes, copia)

    def test_acepta_fechas_date_y_texto(self):
        r = plan_fefo([("A", date(2026, 12, 1), 5)], 5, HOY)
        self.assertEqual(r.plan, [("A", 5)])


class PruebasLimite(unittest.TestCase):
    def test_lote_vencido_se_excluye(self):
        r = plan_fefo([("V", "2026-11-18", 100), ("A", "2026-12-01", 10)], 10, HOY)
        self.assertEqual(r.plan, [("A", 10)])

    def test_lote_que_vence_hoy_si_sirve(self):          # supuesto S1
        r = plan_fefo([("H", "2026-11-19", 10)], 10, HOY)
        self.assertTrue(r.aceptado)

    def test_todos_vencidos(self):
        r = plan_fefo([("V", "2026-01-01", 100)], 1, HOY)
        self.assertFalse(r.aceptado)
        self.assertEqual((r.plan, r.faltante), ([], 1))

    def test_lote_sin_disponible_se_excluye(self):
        r = plan_fefo([("Z", "2026-11-25", 0), ("A", "2026-12-01", 10)], 4, HOY)
        self.assertEqual(r.plan, [("A", 4)])

    def test_empate_de_fecha_se_resuelve_por_codigo(self):
        lotes = [("L-3", "2026-12-10", 10), ("L-1", "2026-12-10", 10), ("L-2", "2026-12-10", 10)]
        r = plan_fefo(lotes, 15, HOY)
        self.assertEqual(r.plan, [("L-1", 10), ("L-2", 5)])

    def test_resultado_no_depende_del_orden_de_entrada(self):
        base = [("L-3", "2026-12-10", 10), ("L-1", "2026-12-10", 7),
                ("L-2", "2026-12-05", 4), ("L-4", "2027-02-01", 9)]
        esperado = plan_fefo(base, 20, HOY)
        rng = random.Random(2026)
        for _ in range(20):
            mezcla = base[:]
            rng.shuffle(mezcla)
            self.assertEqual(plan_fefo(mezcla, 20, HOY), esperado)

    def test_orden_lexicografico_del_codigo(self):       # supuesto S3
        lotes = [("L2", "2026-12-10", 5), ("L10", "2026-12-10", 5)]
        self.assertEqual(plan_fefo(lotes, 5, HOY).plan, [("L10", 5)])

    def test_pedido_igual_al_stock(self):
        r = plan_fefo([("A", "2026-12-01", 6), ("B", "2026-12-02", 4)], 10, HOY)
        self.assertTrue(r.aceptado)
        self.assertEqual(r.faltante, 0)

    def test_pedido_mayor_al_stock_se_rechaza_con_plan_parcial(self):   # supuesto S5
        r = plan_fefo([("A", "2026-12-01", 6), ("B", "2026-12-02", 4)], 25, HOY)
        self.assertFalse(r.aceptado)
        self.assertEqual(r.plan, [("A", 6), ("B", 4)])
        self.assertEqual(r.faltante, 15)

    def test_vencidos_no_cuentan_como_stock(self):
        r = plan_fefo([("V", "2026-01-01", 100), ("A", "2026-12-01", 3)], 5, HOY)
        self.assertFalse(r.aceptado)
        self.assertEqual(r.faltante, 2)

    def test_sku_sin_lotes(self):
        r = plan_fefo([], 5, HOY)
        self.assertEqual((r.aceptado, r.plan, r.faltante), (False, [], 5))

    def test_pedido_minimo_de_una_unidad(self):
        self.assertEqual(plan_fefo([("A", "2026-12-01", 1)], 1, HOY).plan, [("A", 1)])

    def test_muchos_lotes(self):
        lotes = [(f"L{i:06d}", "2027-01-01", 1) for i in range(50_000)]
        r = plan_fefo(lotes, 50_000, HOY)
        self.assertTrue(r.aceptado)
        self.assertEqual(len(r.plan), 50_000)


class PruebasInvalidas(unittest.TestCase):
    LOTES = [("A", "2026-12-01", 10)]

    def test_pedido_cero_o_negativo(self):
        for malo in (0, -1, -50):
            with self.assertRaises(ValueError):
                plan_fefo(self.LOTES, malo, HOY)

    def test_pedido_de_tipo_incorrecto(self):
        for malo in (2.5, "10", None, True):
            with self.assertRaises(TypeError):
                plan_fefo(self.LOTES, malo, HOY)

    def test_disponible_negativo(self):
        with self.assertRaises(ValueError):
            plan_fefo([("A", "2026-12-01", -1)], 1, HOY)

    def test_disponible_no_entero(self):
        with self.assertRaises(TypeError):
            plan_fefo([("A", "2026-12-01", 1.5)], 1, HOY)

    def test_codigo_repetido(self):
        with self.assertRaises(ValueError):
            plan_fefo([("A", "2026-12-01", 1), ("A", "2026-12-02", 1)], 1, HOY)

    def test_codigo_vacio(self):
        with self.assertRaises(ValueError):
            leer_lotes([("", "2026-12-01", 1)])

    def test_fecha_mal_formada(self):
        with self.assertRaises(ValueError):
            plan_fefo([("A", "01/12/2026", 1)], 1, HOY)
        with self.assertRaises(ValueError):
            plan_fefo([("A", "2026-02-30", 1)], 1, HOY)

    def test_fecha_de_tipo_incorrecto(self):
        with self.assertRaises(TypeError):
            plan_fefo([("A", 20261201, 1)], 1, HOY)
        with self.assertRaises(TypeError):
            plan_fefo([("A", datetime(2026, 12, 1, 8, 0), 1)], 1, HOY)

    def test_lote_mal_formado_y_entrada_no_lista(self):
        with self.assertRaises(ValueError):
            leer_lotes([("A", "2026-12-01")])
        with self.assertRaises(TypeError):
            leer_lotes("A")

    def test_hoy_invalido(self):
        with self.assertRaises(TypeError):
            plan_fefo(self.LOTES, 1, None)


if __name__ == "__main__":
    unittest.main(verbosity=2)
