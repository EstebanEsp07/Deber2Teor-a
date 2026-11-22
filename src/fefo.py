"""
Fase C · Selección FEFO (First Expired, First Out)  — responsable: Richard

Problema (reserva de inventario):
    Entrada : lotes de un SKU (código, fecha de vencimiento, cantidad disponible),
              la cantidad pedida y la fecha de referencia `hoy`.
    Salida  : plan de reserva [(código_lote, cantidad)], cuánto falta y si se
              acepta o se rechaza el pedido.

Reglas (del enunciado):
    1. Candidatos = lotes NO vencidos con disponible > 0.
    2. Orden: (fecha de vencimiento ascendente, código de lote ascendente).
    3. De cada lote se toma min(pendiente, disponible).

Supuestos declarados (ver docs/FASE_C_fefo_reposicion.md):
    S1. Un lote que vence EXACTAMENTE `hoy` todavía es utilizable (vencido = vence antes de hoy).
    S2. Los códigos de lote son únicos (si no, el desempate no sería reproducible).
    S3. El código se compara como texto (orden lexicográfico: "L10" < "L2").
    S4. Las cantidades son enteros; `disponible` ya descuenta lo reservado.
    S5. Política si no alcanza el stock: RECHAZAR el pedido completo (no se reserva
        nada); el plan parcial se devuelve solo como información.

Separación de responsabilidades:
    leer_lotes()   -> lectura y validación
    plan_fefo()    -> procesamiento
    main()         -> presentación
"""
from collections import namedtuple
from datetime import date

Lote = namedtuple("Lote", "codigo vencimiento disponible")
ResultadoFefo = namedtuple("ResultadoFefo", "aceptado plan faltante")


# ---------------------------------------------------------------- lectura
def _validar_entero(valor, nombre, minimo):
    """bool es subclase de int en Python, por eso se rechaza de forma explícita."""
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise TypeError(f"{nombre} debe ser un entero")
    if valor < minimo:
        raise ValueError(f"{nombre} debe ser >= {minimo}")


def _validar_fecha(valor, nombre):
    """Acepta date o texto 'AAAA-MM-DD'. Rechaza datetime (no se puede comparar con date)."""
    if isinstance(valor, str):
        try:
            return date.fromisoformat(valor)
        except ValueError:
            raise ValueError(f"{nombre} no es una fecha AAAA-MM-DD válida: {valor!r}")
    if type(valor) is not date:
        raise TypeError(f"{nombre} debe ser date o texto AAAA-MM-DD")
    return valor


def leer_lotes(registros):
    """Convierte [(código, vencimiento, disponible), ...] en una lista de Lote validados.

    Una lista vacía es válida (SKU sin lotes). Tiempo O(L), espacio O(L).
    """
    if not isinstance(registros, (list, tuple)):
        raise TypeError("registros debe ser una lista de (código, vencimiento, disponible)")
    lotes = []
    codigos = set()
    for reg in registros:
        if not isinstance(reg, (list, tuple)) or len(reg) != 3:
            raise ValueError(f"lote mal formado: {reg!r}")
        codigo, venc, disp = reg
        if not isinstance(codigo, str) or codigo == "":
            raise ValueError(f"el código de lote debe ser un texto no vacío: {codigo!r}")
        if codigo in codigos:
            raise ValueError(f"código de lote repetido: {codigo!r}")
        codigos.add(codigo)
        _validar_entero(disp, f"disponible del lote {codigo}", 0)
        lotes.append(Lote(codigo, _validar_fecha(venc, f"vencimiento del lote {codigo}"), disp))
    return lotes


# ----------------------------------------------------------- procesamiento
def plan_fefo(registros, pedido, hoy):
    """Calcula el plan FEFO. No modifica el inventario (solo devuelve el plan).

    Decisión algorítmica: se ordena una sola vez por (vencimiento, código). Como los
    códigos son únicos, esa clave es un orden total: el resultado no depende del orden
    en que lleguen los lotes. Luego un recorrido voraz toma min(pendiente, disponible).

    Invariante del ciclo: suma(plan) + pendiente == pedido y 0 <= pendiente <= pedido.
    Terminación: el `for` recorre una lista finita de <= L candidatos.
    Tiempo O(L log L) (el orden domina); espacio O(L). L = número de lotes del SKU.
    """
    _validar_entero(pedido, "pedido", 1)          # S: pedir 0 o negativo no es una reserva
    hoy = _validar_fecha(hoy, "hoy")
    lotes = leer_lotes(registros)

    candidatos = [l for l in lotes if l.vencimiento >= hoy and l.disponible > 0]  # S1
    candidatos.sort(key=lambda l: (l.vencimiento, l.codigo))

    plan = []
    pendiente = pedido
    for lote in candidatos:
        if pendiente == 0:
            break
        tomar = min(pendiente, lote.disponible)
        plan.append((lote.codigo, tomar))
        pendiente -= tomar
    # S5: si pendiente > 0 se RECHAZA; `plan` queda solo como información del parcial.
    return ResultadoFefo(pendiente == 0, plan, pendiente)


# ------------------------------------------------------------ presentación
def _mostrar(titulo, resultado):
    estado = "ACEPTADO" if resultado.aceptado else "RECHAZADO (stock insuficiente)"
    print(f"{titulo}: {estado}")
    print(f"  plan = {resultado.plan}   faltante = {resultado.faltante}")


def main():
    # Datos ilustrativos propios (el simulador no trae un correo de FEFO).
    hoy = date(2026, 11, 19)
    lotes = [("L-003", "2026-12-10", 40),   # empata con L-001 en fecha
             ("L-001", "2026-12-10", 25),
             ("L-002", "2026-11-30", 30),   # vence primero
             ("L-000", "2026-11-10", 50),   # vencido: se excluye
             ("L-004", "2027-01-15", 0)]    # sin disponible: se excluye
    _mostrar("Pedido de 70", plan_fefo(lotes, 70, hoy))
    _mostrar("Pedido de 200", plan_fefo(lotes, 200, hoy))
    _mostrar("SKU sin lotes, pedido de 5", plan_fefo([], 5, hoy))


if __name__ == "__main__":
    main()
