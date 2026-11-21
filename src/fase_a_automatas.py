"""
Fase A · Autómatas finitos de LOGISTPULSE: pedido, reserva y orden de compra.

Cada proceso se modela como un AUTÓMATA FINITO DETERMINISTA PARCIAL
    M = (Q, Σ, q0, F, δ),   δ : Q × Σ ⇀ Q   (función parcial)
- Σ son EVENTOS de negocio (confirmar, reservar, ...), no letras sueltas.
- δ es parcial a propósito: si (q, e) no está en δ, el evento NO es posible en
  ese estado (p. ej. consumir una reserva que nunca fue confirmada). Equivale
  a un estado trampa implícito que no dibujamos; JFLAP lo trata igual.
- F = estados donde el ciclo de vida queda CERRADO (sumideros: no tienen
  transiciones salientes). Un estado final no significa "éxito": Rechazada,
  Liberada o Cancelado son finales que cierran el ciclo sin éxito.

Veredictos de ejecutar():
    ACEPTADA              todos los eventos tenían transición y se termina en F
    RECHAZADA_TRANSICION  algún evento no tiene δ definida (secuencia inválida)
    RECHAZADA_NO_FINAL    todas las transiciones existen pero se termina en un
                          estado ∉ F (secuencia válida pero INCOMPLETA)

Separación de responsabilidades:
    AUTOMATAS / CASOS            -> datos (definición y secuencias de prueba)
    validar_automata()           -> validación de la definición
    ejecutar(), analisis (*)     -> procesamiento
    a_jff(), leer_jff()          -> exportación / lectura de JFLAP
    main()                       -> presentación

Uso:
    python3 src/fase_a_automatas.py                 # imprime modelos y pruebas
    python3 src/fase_a_automatas.py --jff modelos   # además escribe los .jff
"""
import argparse
import os
import sys
import xml.etree.ElementTree as ET
from collections import namedtuple
from dataclasses import dataclass
from xml.sax.saxutils import escape

ACEPTADA = "ACEPTADA"
RECHAZADA_TRANSICION = "RECHAZADA_TRANSICION"
RECHAZADA_NO_FINAL = "RECHAZADA_NO_FINAL"

Resultado = namedtuple("Resultado", "veredicto traza bloqueo")
# traza   : lista de estados visitados (empieza en q0)
# bloqueo : (estado, evento) donde δ no está definida, o None


# =====================================================================
#  DATOS · definición de los tres autómatas
# =====================================================================
@dataclass(frozen=True)
class Automata:
    nombre: str
    estados: tuple          # Q (en orden de dibujo)
    eventos: dict           # Σ: nombre del evento -> letra de JFLAP (1 carácter)
    inicial: str            # q0
    finales: frozenset      # F
    delta: dict             # (estado, evento) -> estado
    posiciones: dict        # estado -> (x, y) solo para el dibujo en JFLAP


def _t(*filas):
    """Construye δ a partir de filas (origen, evento, destino)."""
    return {(o, e): d for o, e, d in filas}


PEDIDO = Automata(
    nombre="pedido",
    estados=("Borrador", "Confirmado", "Reservado", "Preparación",
             "Empacado", "Despachado", "Entregado", "Cancelado"),
    eventos={"confirmar": "c", "reservar": "r", "iniciar_picking": "p",
             "empacar": "e", "despachar": "d", "entregar": "t",
             "cancelar": "x"},
    inicial="Borrador",
    finales=frozenset({"Entregado", "Cancelado"}),
    delta=_t(
        ("Borrador", "confirmar", "Confirmado"),
        ("Confirmado", "reservar", "Reservado"),
        ("Reservado", "iniciar_picking", "Preparación"),
        ("Preparación", "empacar", "Empacado"),
        ("Empacado", "despachar", "Despachado"),
        ("Despachado", "entregar", "Entregado"),
        # cancelar: solo antes de iniciar el picking (después la reserva ya
        # fue consumida y no hay nada que liberar)
        ("Borrador", "cancelar", "Cancelado"),
        ("Confirmado", "cancelar", "Cancelado"),
        ("Reservado", "cancelar", "Cancelado"),
    ),
    posiciones={"Borrador": (60, 200), "Confirmado": (200, 200),
                "Reservado": (340, 200), "Preparación": (480, 200),
                "Empacado": (620, 200), "Despachado": (760, 200),
                "Entregado": (900, 200), "Cancelado": (200, 360)},
)

RESERVA = Automata(
    nombre="reserva",
    estados=("Solicitada", "Validada", "Rechazada", "Reservada",
             "Consumida", "Liberada", "Expirada"),
    eventos={"validar": "v", "sin_stock": "s", "confirmar": "c",
             "picking": "p", "cancelar": "x", "vence_plazo": "e"},
    inicial="Solicitada",
    finales=frozenset({"Rechazada", "Consumida", "Liberada", "Expirada"}),
    delta=_t(
        ("Solicitada", "validar", "Validada"),
        ("Solicitada", "sin_stock", "Rechazada"),
        ("Validada", "confirmar", "Reservada"),
        # solo una reserva CONFIRMADA (Reservada) puede consumirse,
        # liberarse o vencer
        ("Reservada", "picking", "Consumida"),
        ("Reservada", "cancelar", "Liberada"),
        ("Reservada", "vence_plazo", "Expirada"),
    ),
    posiciones={"Solicitada": (60, 200), "Validada": (220, 120),
                "Rechazada": (220, 300), "Reservada": (380, 120),
                "Consumida": (540, 40), "Liberada": (540, 120),
                "Expirada": (540, 200)},
)

ORDEN_COMPRA = Automata(
    nombre="orden_compra",
    estados=("Borrador", "En aprobación", "Aprobada", "Rechazada",
             "Enviada", "Recepción parcial", "Recibida"),
    eventos={"solicitar_aprobacion": "s", "aprobar": "a", "rechazar": "r",
             "emitir_orden": "e", "recibir_parte": "p",
             "completar_recepcion": "c", "recibir_completa": "t"},
    inicial="Borrador",
    finales=frozenset({"Rechazada", "Recibida"}),
    delta=_t(
        ("Borrador", "solicitar_aprobacion", "En aprobación"),
        ("En aprobación", "aprobar", "Aprobada"),
        ("En aprobación", "rechazar", "Rechazada"),
        ("Aprobada", "emitir_orden", "Enviada"),
        ("Enviada", "recibir_parte", "Recepción parcial"),
        ("Enviada", "recibir_completa", "Recibida"),
        ("Recepción parcial", "completar_recepcion", "Recibida"),
        # AÑADIDA (no está en la Figura 4): varias entregas parciales
        ("Recepción parcial", "recibir_parte", "Recepción parcial"),
    ),
    posiciones={"Borrador": (60, 160), "En aprobación": (220, 160),
                "Aprobada": (380, 80), "Rechazada": (380, 240),
                "Enviada": (540, 80), "Recepción parcial": (700, 30),
                "Recibida": (860, 80)},
)

AUTOMATAS = {a.nombre: a for a in (PEDIDO, RESERVA, ORDEN_COMPRA)}

# Casos documentados: (id, descripción, [eventos], veredicto, bloqueo)
# bloqueo = (estado, evento) donde falla δ, solo para RECHAZADA_TRANSICION.
CASOS = {
    "pedido": [
        ("P-V1", "ciclo completo (prueba del deber)",
         ["confirmar", "reservar", "iniciar_picking", "empacar",
          "despachar", "entregar"], ACEPTADA, None),
        ("P-V2", "cancelación con reserva activa",
         ["confirmar", "reservar", "cancelar"], ACEPTADA, None),
        ("P-V3", "cancelación inmediata desde Borrador",
         ["cancelar"], ACEPTADA, None),
        ("P-I1", "despachar sin confirmar (prueba del deber)",
         ["despachar"], RECHAZADA_TRANSICION, ("Borrador", "despachar")),
        ("P-I2", "cancelar con el picking ya iniciado",
         ["confirmar", "reservar", "iniciar_picking", "cancelar"],
         RECHAZADA_TRANSICION, ("Preparación", "cancelar")),
        ("P-I3", "cancelar un pedido ya entregado",
         ["confirmar", "reservar", "iniciar_picking", "empacar",
          "despachar", "entregar", "cancelar"],
         RECHAZADA_TRANSICION, ("Entregado", "cancelar")),
        ("P-I4", "empacar sin reservar ni hacer picking",
         ["confirmar", "empacar"],
         RECHAZADA_TRANSICION, ("Confirmado", "empacar")),
        ("P-N1", "válida pero incompleta: termina en Empacado",
         ["confirmar", "reservar", "iniciar_picking", "empacar"],
         RECHAZADA_NO_FINAL, None),
    ],
    "reserva": [
        ("R-V1", "ciclo completo (prueba del deber)",
         ["validar", "confirmar", "picking"], ACEPTADA, None),
        ("R-V2", "reserva liberada por cancelación",
         ["validar", "confirmar", "cancelar"], ACEPTADA, None),
        ("R-V3", "reserva expirada",
         ["validar", "confirmar", "vence_plazo"], ACEPTADA, None),
        ("R-V4", "solicitud rechazada por falta de stock",
         ["sin_stock"], ACEPTADA, None),
        ("R-I1", "consumir una reserva sin confirmarla",
         ["validar", "picking"],
         RECHAZADA_TRANSICION, ("Validada", "picking")),
        ("R-I2", "consumir sin validar ni confirmar",
         ["picking"], RECHAZADA_TRANSICION, ("Solicitada", "picking")),
        ("R-I3", "validar una solicitud ya rechazada",
         ["sin_stock", "validar"],
         RECHAZADA_TRANSICION, ("Rechazada", "validar")),
        ("R-I4", "cancelar una reserva ya consumida",
         ["validar", "confirmar", "picking", "cancelar"],
         RECHAZADA_TRANSICION, ("Consumida", "cancelar")),
        ("R-N1", "válida pero incompleta: queda en Reservada",
         ["validar", "confirmar"], RECHAZADA_NO_FINAL, None),
    ],
    "orden_compra": [
        ("O-V1", "recepción completa en un solo envío",
         ["solicitar_aprobacion", "aprobar", "emitir_orden",
          "recibir_completa"], ACEPTADA, None),
        ("O-V2", "una recepción parcial y luego completar",
         ["solicitar_aprobacion", "aprobar", "emitir_orden",
          "recibir_parte", "completar_recepcion"], ACEPTADA, None),
        ("O-V3", "dos recepciones parciales (usa el bucle añadido)",
         ["solicitar_aprobacion", "aprobar", "emitir_orden",
          "recibir_parte", "recibir_parte", "completar_recepcion"],
         ACEPTADA, None),
        ("O-V4", "orden rechazada en aprobación",
         ["solicitar_aprobacion", "rechazar"], ACEPTADA, None),
        ("O-I1", "emitir una orden rechazada (prueba del deber)",
         ["solicitar_aprobacion", "rechazar", "emitir_orden"],
         RECHAZADA_TRANSICION, ("Rechazada", "emitir_orden")),
        ("O-I2", "emitir sin pedir aprobación",
         ["emitir_orden"], RECHAZADA_TRANSICION, ("Borrador", "emitir_orden")),
        ("O-I3", "emitir antes de que termine la aprobación",
         ["solicitar_aprobacion", "emitir_orden"],
         RECHAZADA_TRANSICION, ("En aprobación", "emitir_orden")),
        ("O-I4", "recibir otra parte después de Recibida",
         ["solicitar_aprobacion", "aprobar", "emitir_orden",
          "recibir_completa", "recibir_parte"],
         RECHAZADA_TRANSICION, ("Recibida", "recibir_parte")),
        ("O-N1", "válida pero incompleta: queda en Recepción parcial",
         ["solicitar_aprobacion", "aprobar", "emitir_orden",
          "recibir_parte"], RECHAZADA_NO_FINAL, None),
    ],
}


# =====================================================================
#  VALIDACIÓN de la definición
# =====================================================================
def validar_automata(a):
    """Comprueba que M = (Q, Σ, q0, F, δ) está bien formado.
    Lanza TypeError/ValueError si no. Devuelve el propio autómata."""
    if not isinstance(a, Automata):
        raise TypeError("se esperaba un Automata")
    Q = set(a.estados)
    if len(Q) != len(a.estados):
        raise ValueError("estados repetidos en Q")
    if a.inicial not in Q:
        raise ValueError(f"q0 = {a.inicial!r} no pertenece a Q")
    if not set(a.finales) <= Q:
        raise ValueError("F no está contenido en Q")
    letras = list(a.eventos.values())
    if any(not isinstance(l, str) or len(l) != 1 for l in letras):
        raise ValueError("cada evento necesita una letra JFLAP de 1 carácter")
    if len(set(letras)) != len(letras):
        raise ValueError("dos eventos comparten la misma letra JFLAP")
    for (q, e), d in a.delta.items():
        if q not in Q or d not in Q:
            raise ValueError(f"δ({q}, {e}) usa un estado fuera de Q")
        if e not in a.eventos:
            raise ValueError(f"δ({q}, {e}) usa un evento fuera de Σ")
    return a


# =====================================================================
#  PROCESAMIENTO
# =====================================================================
def ejecutar(a, secuencia):
    """Ejecuta una secuencia de EVENTOS (lista/tupla de nombres) sobre a.

    Tiempo O(|w|), espacio O(|w|) por la traza (O(1) si no se guarda).
    Entrada inválida -> TypeError/ValueError (no es un rechazo del modelo).
    Un evento sin transición definida SÍ es un rechazo del modelo.
    """
    if isinstance(secuencia, str) or not isinstance(secuencia, (list, tuple)):
        raise TypeError("la secuencia debe ser lista/tupla de eventos "
                        "(una cadena se confundiría con letras)")
    q = a.inicial
    traza = [q]
    for ev in secuencia:
        if not isinstance(ev, str):
            raise TypeError(f"evento no textual: {ev!r}")
        if ev not in a.eventos:
            raise ValueError(f"el evento {ev!r} no pertenece a Σ de "
                             f"{a.nombre}")
        siguiente = a.delta.get((q, ev))
        if siguiente is None:                 # transición imposible
            return Resultado(RECHAZADA_TRANSICION, traza, (q, ev))
        q = siguiente
        traza.append(q)
    if q in a.finales:
        return Resultado(ACEPTADA, traza, None)
    return Resultado(RECHAZADA_NO_FINAL, traza, None)


def a_letras(a, secuencia):
    """Traduce eventos a la cadena de letras que se teclea en JFLAP."""
    return "".join(a.eventos[e] for e in secuencia)


def sumideros(a):
    """Estados sin transiciones salientes."""
    con_salida = {q for (q, _e) in a.delta}
    return set(a.estados) - con_salida


def alcanzables(a):
    """Estados alcanzables desde q0 (BFS sobre δ)."""
    vistos, pila = {a.inicial}, [a.inicial]
    while pila:
        u = pila.pop()
        for (q, _e), d in a.delta.items():
            if q == u and d not in vistos:
                vistos.add(d)
                pila.append(d)
    return vistos


def coalcanzables(a):
    """Estados desde los que se puede llegar a F (ninguno queda atrapado)."""
    buenos = set(a.finales)
    cambio = True
    while cambio:
        cambio = False
        for (q, _e), d in a.delta.items():
            if d in buenos and q not in buenos:
                buenos.add(q)
                cambio = True
    return buenos


# =====================================================================
#  JFLAP · exportación y lectura de .jff (XML)
# =====================================================================
def a_jff(a):
    """Devuelve el XML de JFLAP (type fa) con eventos de 1 letra."""
    validar_automata(a)
    ids = {q: i for i, q in enumerate(a.estados)}
    L = ['<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
         "<structure>", "\t<type>fa</type>", "\t<automaton>",
         "\t\t<!--The list of states.-->"]
    for q in a.estados:
        x, y = a.posiciones[q]
        L += [f'\t\t<state id="{ids[q]}" name="{escape(q)}">',
              f"\t\t\t<x>{x}.0</x>", f"\t\t\t<y>{y}.0</y>"]
        if q == a.inicial:
            L.append("\t\t\t<initial/>")
        if q in a.finales:
            L.append("\t\t\t<final/>")
        L.append("\t\t</state>")
    L.append("\t\t<!--The list of transitions.-->")
    for (o, e), d in a.delta.items():
        L += ["\t\t<transition>", f"\t\t\t<from>{ids[o]}</from>",
              f"\t\t\t<to>{ids[d]}</to>",
              f"\t\t\t<read>{escape(a.eventos[e])}</read>", "\t\t</transition>"]
    L += ["\t</automaton>", "</structure>", ""]
    return "\n".join(L)


def leer_jff(ruta):
    """Lee un .jff y devuelve un Automata cuyos 'eventos' son las propias
    letras (letra -> letra). Sirve para comprobar que el archivo que se
    entrega coincide con la definición del código."""
    arbol = ET.parse(ruta).getroot()
    if arbol.findtext("type") != "fa":
        raise ValueError(f"{ruta}: se esperaba type 'fa'")
    aut = arbol.find("automaton")
    nombre_de, estados, finales, inicial, pos = {}, [], set(), None, {}
    for s in aut.findall("state"):
        nombre = s.get("name")
        nombre_de[s.get("id")] = nombre
        estados.append(nombre)
        pos[nombre] = (float(s.findtext("x")), float(s.findtext("y")))
        if s.find("initial") is not None:
            inicial = nombre
        if s.find("final") is not None:
            finales.add(nombre)
    delta, letras = {}, {}
    for t in aut.findall("transition"):
        letra = t.findtext("read")
        letras[letra] = letra
        delta[(nombre_de[t.findtext("from")], letra)] = nombre_de[t.findtext("to")]
    return validar_automata(Automata(
        nombre=os.path.basename(ruta), estados=tuple(estados), eventos=letras,
        inicial=inicial, finales=frozenset(finales), delta=delta,
        posiciones=pos))


def escribir_jff(directorio):
    os.makedirs(directorio, exist_ok=True)
    rutas = []
    for a in AUTOMATAS.values():
        ruta = os.path.join(directorio, f"{a.nombre}.jff")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(a_jff(a))
        rutas.append(ruta)
    return rutas


# =====================================================================
#  PRESENTACIÓN
# =====================================================================
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--jff", metavar="DIR",
                    help="escribe los tres .jff en DIR")
    args = ap.parse_args(argv)

    if args.jff:
        for r in escribir_jff(args.jff):
            print("escrito:", r)
        print()

    for a in AUTOMATAS.values():
        validar_automata(a)
        print(f"=== {a.nombre} ===  |Q|={len(a.estados)}  |Σ|={len(a.eventos)}"
              f"  |δ|={len(a.delta)}  q0={a.inicial}  F={sorted(a.finales)}")
        for (q, e), d in a.delta.items():
            print(f"  δ({q}, {e}) = {d}")
        for id_, desc, seq, esperado, _blq in CASOS[a.nombre]:
            r = ejecutar(a, seq)
            marca = "OK " if r.veredicto == esperado else "!! "
            detalle = (f"  bloqueo en δ{r.bloqueo}" if r.bloqueo else "")
            print(f"{marca}{id_}  {a_letras(a, seq) or 'λ':<8} "
                  f"{r.veredicto:<21} {' -> '.join(r.traza)}{detalle}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
