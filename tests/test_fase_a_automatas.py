import os
import sys
import tempfile
import unittest
from dataclasses import replace

AQUI = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(AQUI, "..", "src"))
from fase_a_automatas import (ACEPTADA, AUTOMATAS, CASOS, ORDEN_COMPRA,
                              PEDIDO, RECHAZADA_NO_FINAL,
                              RECHAZADA_TRANSICION, RESERVA, a_jff,
                              a_letras, alcanzables, coalcanzables,
                              ejecutar, escribir_jff, leer_jff, sumideros,
                              validar_automata)

MODELOS = os.path.join(AQUI, "..", "modelos")


def veredicto(a, seq):
    return ejecutar(a, seq).veredicto


# ------------------------------------------------------------ normales
class PruebasNormales(unittest.TestCase):
    def test_cuatro_pruebas_minimas_del_deber(self):
        # 1) pedido válido
        self.assertEqual(veredicto(PEDIDO, [
            "confirmar", "reservar", "iniciar_picking", "empacar",
            "despachar", "entregar"]), ACEPTADA)
        # 2) pedido inválido: Borrador -> Despachado
        self.assertEqual(veredicto(PEDIDO, ["despachar"]),
                         RECHAZADA_TRANSICION)
        # 3) reserva válida
        self.assertEqual(veredicto(RESERVA, [
            "validar", "confirmar", "picking"]), ACEPTADA)
        # 4) compra inválida: Rechazada -> Enviada
        self.assertEqual(veredicto(ORDEN_COMPRA, [
            "solicitar_aprobacion", "rechazar", "emitir_orden"]),
            RECHAZADA_TRANSICION)

    def test_todos_los_casos_documentados(self):
        for nombre, casos in CASOS.items():
            a = AUTOMATAS[nombre]
            for id_, _desc, seq, esperado, bloqueo in casos:
                with self.subTest(caso=id_):
                    r = ejecutar(a, seq)
                    self.assertEqual(r.veredicto, esperado)
                    self.assertEqual(r.bloqueo, bloqueo)

    def test_minimo_dos_validas_y_dos_invalidas_por_automata(self):
        for nombre, casos in CASOS.items():
            validas = [c for c in casos if c[3] == ACEPTADA]
            invalidas = [c for c in casos if c[3] == RECHAZADA_TRANSICION]
            self.assertGreaterEqual(len(validas), 2, nombre)
            self.assertGreaterEqual(len(invalidas), 2, nombre)

    def test_traza_de_la_reserva_valida(self):
        r = ejecutar(RESERVA, ["validar", "confirmar", "picking"])
        self.assertEqual(r.traza, ["Solicitada", "Validada", "Reservada",
                                   "Consumida"])

    def test_cancelar_el_pedido_antes_del_picking(self):
        for previo in ([], ["confirmar"], ["confirmar", "reservar"]):
            self.assertEqual(veredicto(PEDIDO, previo + ["cancelar"]),
                             ACEPTADA)


# -------------------------------------------------------------- límite
class PruebasLimite(unittest.TestCase):
    def test_secuencia_vacia_se_rechaza_por_no_final(self):
        # q0 no es final en ningún modelo: un ciclo sin eventos no está cerrado
        for a in AUTOMATAS.values():
            self.assertNotIn(a.inicial, a.finales)
            self.assertEqual(veredicto(a, []), RECHAZADA_NO_FINAL)

    def test_bucle_de_recepciones_parciales_largo(self):
        seq = ["solicitar_aprobacion", "aprobar", "emitir_orden"]
        seq += ["recibir_parte"] * 10_000 + ["completar_recepcion"]
        r = ejecutar(ORDEN_COMPRA, seq)
        self.assertEqual(r.veredicto, ACEPTADA)
        self.assertEqual(r.traza[-1], "Recibida")

    def test_bucle_sin_cierre_no_es_aceptado(self):
        seq = ["solicitar_aprobacion", "aprobar", "emitir_orden"]
        seq += ["recibir_parte"] * 50
        self.assertEqual(veredicto(ORDEN_COMPRA, seq), RECHAZADA_NO_FINAL)

    def test_el_rechazo_ocurre_en_el_primer_evento_imposible(self):
        # el sufijo posterior al bloqueo no se evalúa
        r = ejecutar(PEDIDO, ["despachar", "entregar", "entregar"])
        self.assertEqual(r.bloqueo, ("Borrador", "despachar"))
        self.assertEqual(r.traza, ["Borrador"])

    def test_estados_finales_son_sumideros(self):
        # un estado final cierra el ciclo: ningún evento posterior es válido
        for a in AUTOMATAS.values():
            for f in a.finales:
                for ev in a.eventos:
                    self.assertNotIn((f, ev), a.delta, (a.nombre, f, ev))

    def test_tamanos(self):
        self.assertEqual((len(PEDIDO.estados), len(PEDIDO.delta)), (8, 9))
        self.assertEqual((len(RESERVA.estados), len(RESERVA.delta)), (7, 6))
        self.assertEqual((len(ORDEN_COMPRA.estados), len(ORDEN_COMPRA.delta)),
                         (7, 8))


# ----------------------------------------------------------- inválidas
class PruebasInvalidas(unittest.TestCase):
    def test_evento_fuera_de_sigma(self):
        with self.assertRaises(ValueError):
            ejecutar(PEDIDO, ["confirmar", "sin_stock"])   # evento de reserva

    def test_secuencia_como_cadena(self):
        with self.assertRaises(TypeError):
            ejecutar(PEDIDO, "confirmar")

    def test_secuencia_no_iterable_o_con_tipos_mixtos(self):
        with self.assertRaises(TypeError):
            ejecutar(PEDIDO, None)
        with self.assertRaises(TypeError):
            ejecutar(PEDIDO, ["confirmar", 7])

    def test_definicion_con_q0_fuera_de_Q(self):
        with self.assertRaises(ValueError):
            validar_automata(replace(PEDIDO, inicial="Inexistente"))

    def test_definicion_con_F_fuera_de_Q(self):
        with self.assertRaises(ValueError):
            validar_automata(replace(RESERVA, finales=frozenset({"Nada"})))

    def test_definicion_con_transicion_a_estado_inexistente(self):
        d = dict(ORDEN_COMPRA.delta)
        d[("Borrador", "aprobar")] = "Fantasma"
        with self.assertRaises(ValueError):
            validar_automata(replace(ORDEN_COMPRA, delta=d))

    def test_definicion_con_letras_repetidas(self):
        ev = dict(PEDIDO.eventos)
        ev["entregar"] = ev["despachar"]
        with self.assertRaises(ValueError):
            validar_automata(replace(PEDIDO, eventos=ev))

    def test_no_es_un_automata(self):
        with self.assertRaises(TypeError):
            validar_automata({"estados": []})


# --------------------------------------------------------- estructurales
class PruebasEstructurales(unittest.TestCase):
    def test_todo_estado_es_alcanzable_desde_q0(self):
        for a in AUTOMATAS.values():
            self.assertEqual(alcanzables(a), set(a.estados), a.nombre)

    def test_ningun_estado_queda_atrapado(self):
        # desde cualquier estado se puede llegar a F: no hay callejones
        for a in AUTOMATAS.values():
            self.assertEqual(coalcanzables(a), set(a.estados), a.nombre)

    def test_F_es_exactamente_el_conjunto_de_sumideros(self):
        for a in AUTOMATAS.values():
            self.assertEqual(sumideros(a), set(a.finales), a.nombre)

    def test_pedido_cancelar_solo_antes_del_picking(self):
        con_cancelar = {q for (q, e) in PEDIDO.delta if e == "cancelar"}
        self.assertEqual(con_cancelar, {"Borrador", "Confirmado", "Reservado"})

    def test_solo_reservada_puede_consumir_liberar_o_vencer(self):
        for ev in ("picking", "cancelar", "vence_plazo"):
            origenes = {q for (q, e) in RESERVA.delta if e == ev}
            self.assertEqual(origenes, {"Reservada"}, ev)

    def test_unico_ciclo_es_el_bucle_de_recepcion_parcial(self):
        bucles = [(q, e) for (q, e), d in ORDEN_COMPRA.delta.items() if q == d]
        self.assertEqual(bucles, [("Recepción parcial", "recibir_parte")])
        for a in (PEDIDO, RESERVA):
            self.assertFalse([1 for (q, _e), d in a.delta.items() if q == d])


# --------------------------------------------------------------- JFLAP
class PruebasJFLAP(unittest.TestCase):
    def test_los_jff_entregados_coinciden_con_el_codigo(self):
        for a in AUTOMATAS.values():
            ruta = os.path.join(MODELOS, f"{a.nombre}.jff")
            self.assertTrue(os.path.exists(ruta), ruta)
            j = leer_jff(ruta)
            self.assertEqual(set(j.estados), set(a.estados))
            self.assertEqual(j.inicial, a.inicial)
            self.assertEqual(j.finales, a.finales)
            esperado = {(q, a.eventos[e]): d for (q, e), d in a.delta.items()}
            self.assertEqual(j.delta, esperado)

    def test_los_casos_dan_el_mismo_veredicto_ejecutados_desde_el_jff(self):
        # se simula el archivo .jff leído, tecleando las letras como en JFLAP
        for nombre, casos in CASOS.items():
            a = AUTOMATAS[nombre]
            j = leer_jff(os.path.join(MODELOS, f"{nombre}.jff"))
            for id_, _d, seq, esperado, _b in casos:
                with self.subTest(caso=id_):
                    letras = list(a_letras(a, seq))
                    self.assertEqual(ejecutar(j, letras).veredicto, esperado)

    def test_exportar_y_releer_es_identidad(self):
        with tempfile.TemporaryDirectory() as d:
            for ruta in escribir_jff(d):
                nombre = os.path.basename(ruta)[:-4]
                a = AUTOMATAS[nombre]
                j = leer_jff(ruta)
                self.assertEqual(j.finales, a.finales)
                self.assertEqual(len(j.delta), len(a.delta))

    def test_jff_invalido(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = os.path.join(d, "x.jff")
            with open(ruta, "w", encoding="utf-8") as f:
                f.write("<structure><type>pda</type><automaton/></structure>")
            with self.assertRaises(ValueError):
                leer_jff(ruta)

    def test_xml_exportado_contiene_estructura_esperada(self):
        xml = a_jff(RESERVA)
        self.assertIn("<type>fa</type>", xml)
        self.assertEqual(xml.count("<state "), 7)
        self.assertEqual(xml.count("<final/>"), 4)
        self.assertEqual(xml.count("<initial/>"), 1)
        self.assertEqual(xml.count("<transition>"), 6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
