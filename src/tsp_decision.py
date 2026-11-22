"""C2 · TSP de decisión (LOGISTPULSE).

Pregunta (versión de decisión): dada una matriz de distancias D (n x n, no
negativa) y un presupuesto L, ¿existe un recorrido que visite cada centro
exactamente una vez y regrese al punto de salida con costo total <= L?

Estructura del módulo (separación pedida por la plantilla):
  1. LECTURA / VALIDACIÓN   -> leer_instancia, validar_matriz, validar_limite
  2. PROCESAMIENTO          -> verificar, buscar_exacto, optimo_held_karp,
                               vecino_mas_cercano, reducir_ciclo_hamiltoniano
  3. PRESENTACIÓN           -> formatear_resultado, main

Solo biblioteca estándar. Compatible con Python 3.8+.
"""

import argparse
import json
import math
import sys
from itertools import combinations
from numbers import Real
from typing import List, Optional, Sequence, Tuple

# Instancia tal como aparece en el código fuente del simulador (caso c2):
#   d = [[0,4,8],[4,0,3],[8,3,0]] ; print(ruta_dentro(d, 20))
# y en la tabla del caso: Centros = "Planta, Quito, Guayaquil", Límite = 20 km.
INSTANCIA_CORREO = {
    "centros": ["Planta", "Quito", "Guayaquil"],
    "distancias": [[0, 4, 8], [4, 0, 3], [8, 3, 0]],
    "limite": 20,
}


class EntradaInvalida(ValueError):
    """La instancia (matriz, límite o nombres) no cumple el formato."""


# ======================================================================
# 1. LECTURA Y VALIDACIÓN
# ======================================================================

def _es_numero(x) -> bool:
    return isinstance(x, Real) and not isinstance(x, bool)


def validar_matriz(dist) -> List[List[float]]:
    """Valida que dist sea cuadrada, no vacía, finita, no negativa y con
    diagonal 0. Devuelve una copia (lista de listas)."""
    if not isinstance(dist, (list, tuple)) or len(dist) == 0:
        raise EntradaInvalida("la matriz debe ser una lista no vacía de filas")
    n = len(dist)
    copia = []
    for i, fila in enumerate(dist):
        if not isinstance(fila, (list, tuple)) or len(fila) != n:
            raise EntradaInvalida(
                "matriz no cuadrada: la fila %d no tiene %d valores" % (i, n))
        for j, x in enumerate(fila):
            if not _es_numero(x):
                raise EntradaInvalida("D[%d][%d] no es numérico: %r" % (i, j, x))
            if not math.isfinite(x) or x < 0:
                raise EntradaInvalida(
                    "D[%d][%d] debe ser finito y >= 0 (vale %r)" % (i, j, x))
        if fila[i] != 0:
            raise EntradaInvalida("la diagonal debe ser 0 (D[%d][%d] = %r)"
                                  % (i, i, fila[i]))
        copia.append(list(fila))
    return copia


def validar_limite(limite) -> float:
    if not _es_numero(limite):
        raise EntradaInvalida("el límite L debe ser numérico: %r" % (limite,))
    if not math.isfinite(limite) or limite < 0:
        raise EntradaInvalida("el límite L debe ser finito y >= 0: %r" % (limite,))
    return limite


def es_simetrica(dist: Sequence[Sequence[float]]) -> bool:
    n = len(dist)
    return all(dist[i][j] == dist[j][i] for i in range(n) for j in range(i + 1, n))


def leer_instancia(texto_json: str):
    """Lee {"distancias": [[...]], "limite": L, "centros": [...] (opcional)}.
    Devuelve (dist, limite, nombres)."""
    try:
        datos = json.loads(texto_json)
    except json.JSONDecodeError as exc:
        raise EntradaInvalida("JSON mal formado: %s" % exc)
    if not isinstance(datos, dict):
        raise EntradaInvalida("se esperaba un objeto JSON")
    for clave in ("distancias", "limite"):
        if clave not in datos:
            raise EntradaInvalida("falta la clave obligatoria '%s'" % clave)
    dist = validar_matriz(datos["distancias"])
    limite = validar_limite(datos["limite"])
    n = len(dist)
    nombres = datos.get("centros", [str(i) for i in range(n)])
    if (not isinstance(nombres, list) or len(nombres) != n
            or not all(isinstance(s, str) and s for s in nombres)
            or len(set(nombres)) != n):
        raise EntradaInvalida("'centros' debe tener %d nombres distintos no vacíos" % n)
    return dist, limite, nombres


# ======================================================================
# 2. PROCESAMIENTO
# ======================================================================

def costo_recorrido(dist, orden: Sequence[int], cerrar_ciclo: bool = True):
    """Suma de D sobre aristas consecutivas (+ regreso al inicio si ciclo)."""
    total = sum(dist[orden[k]][orden[k + 1]] for k in range(len(orden) - 1))
    if cerrar_ciclo and len(orden) > 1:
        total += dist[orden[-1]][orden[0]]
    return total


def verificar(dist, limite, certificado, cerrar_ciclo: bool = True) -> bool:
    """VERIFICADOR polinómico, independiente de la búsqueda.

    certificado: orden de los n centros (cada índice 0..n-1 exactamente una
    vez). En modo ciclo el regreso al primer centro es implícito.
    Acepta  <=>  es permutación válida  y  costo <= L.   Tiempo O(n).
    Una instancia inválida lanza EntradaInvalida; un certificado mal formado
    simplemente se rechaza (False)."""
    dist = validar_matriz(dist)
    limite = validar_limite(limite)
    n = len(dist)
    if not isinstance(certificado, (list, tuple)) or len(certificado) != n:
        return False
    if not all(isinstance(v, int) and not isinstance(v, bool) for v in certificado):
        return False
    vistos = set()
    for v in certificado:
        if v < 0 or v >= n or v in vistos:
            return False
        vistos.add(v)
    return costo_recorrido(dist, certificado, cerrar_ciclo) <= limite


class Resultado:
    def __init__(self, existe: bool, recorrido=None, costo=None, nodos: int = 0):
        self.existe = existe
        self.recorrido = recorrido
        self.costo = costo
        self.nodos = nodos  # nodos del árbol de búsqueda explorados

    def __repr__(self):
        return "Resultado(existe=%r, recorrido=%r, costo=%r, nodos=%r)" % (
            self.existe, self.recorrido, self.costo, self.nodos)


def buscar_exacto(dist, limite, cerrar_ciclo: bool = True) -> Resultado:
    """ALGORITMO EXACTO de decisión: backtracking sobre permutaciones con el
    centro 0 (punto de salida) fijo y poda por presupuesto.

    La poda 'costo parcial > L' es segura porque todos los pesos son >= 0
    (ninguna extensión puede bajar el costo). Termina porque el árbol tiene
    a lo sumo (n-1)! hojas y cada rama agrega un vértice no visitado."""
    dist = validar_matriz(dist)
    limite = validar_limite(limite)
    n = len(dist)
    camino = [0]
    visitado = [False] * n
    visitado[0] = True
    nodos = [0]

    def extender(parcial):
        nodos[0] += 1
        if parcial > limite:          # poda segura (pesos no negativos)
            return None
        if len(camino) == n:
            total = parcial + (dist[camino[-1]][0] if cerrar_ciclo and n > 1 else 0)
            return (list(camino), total) if total <= limite else None
        u = camino[-1]
        for v in range(n):
            if not visitado[v]:
                visitado[v] = True
                camino.append(v)
                hallado = extender(parcial + dist[u][v])
                if hallado:
                    return hallado
                camino.pop()
                visitado[v] = False
        return None

    hallado = extender(0)
    if hallado:
        return Resultado(True, hallado[0], hallado[1], nodos[0])
    return Resultado(False, None, None, nodos[0])


def optimo_held_karp(dist, cerrar_ciclo: bool = True) -> Tuple[List[int], float]:
    """VERSIÓN DE OPTIMIZACIÓN (no es lo que pide el correo; se usa para
    contrastar): costo mínimo exacto por programación dinámica de Held–Karp.
    Tiempo O(n^2 * 2^n), espacio O(n * 2^n). Salida desde el centro 0."""
    dist = validar_matriz(dist)
    n = len(dist)
    if n == 1:
        return [0], 0
    INF = float("inf")
    # dp[(S, j)] = costo mínimo de salir de 0, visitar exactamente S (sin 0) y terminar en j
    dp = {}
    padre = {}
    for j in range(1, n):
        dp[(1 << j, j)] = dist[0][j]
        padre[(1 << j, j)] = 0
    for tam in range(2, n):
        for sub in combinations(range(1, n), tam):
            S = 0
            for x in sub:
                S |= 1 << x
            for j in sub:
                prev = S & ~(1 << j)
                mejor, arg = INF, None
                for k in sub:
                    if k != j and (prev, k) in dp:
                        c = dp[(prev, k)] + dist[k][j]
                        if c < mejor:
                            mejor, arg = c, k
                dp[(S, j)] = mejor
                padre[(S, j)] = arg
    completo = (1 << n) - 2
    mejor, fin = INF, None
    for j in range(1, n):
        c = dp[(completo, j)] + (dist[j][0] if cerrar_ciclo else 0)
        if c < mejor:
            mejor, fin = c, j
    orden, S, j = [], completo, fin
    while j != 0:
        orden.append(j)
        S, j = S & ~(1 << j), padre[(S, j)]
    orden.append(0)
    orden.reverse()
    return orden, mejor


def vecino_mas_cercano(dist, cerrar_ciclo: bool = True) -> Tuple[List[int], float]:
    """HEURÍSTICA voraz O(n^2): desde 0, ir siempre al no visitado más
    cercano. Devuelve SIEMPRE un recorrido válido, pero SIN garantía de que
    sea óptimo ni de que encuentre uno <= L cuando existe."""
    dist = validar_matriz(dist)
    n = len(dist)
    orden, visitado = [0], {0}
    while len(orden) < n:
        u = orden[-1]
        v = min((w for w in range(n) if w not in visitado), key=lambda w: (dist[u][w], w))
        orden.append(v)
        visitado.add(v)
    return orden, costo_recorrido(dist, orden, cerrar_ciclo)


def decidir_heuristico(dist, limite, cerrar_ciclo: bool = True):
    """'SI' (con certificado verificado) o 'NO CONCLUYENTE'. Nunca dice 'NO'."""
    orden, costo = vecino_mas_cercano(dist, cerrar_ciclo)
    if verificar(dist, limite, orden, cerrar_ciclo):
        return "SI", orden, costo
    return "NO CONCLUYENTE", orden, costo


# ---------------- Reducción  Ciclo Hamiltoniano  <=p  TSP-decisión ----------

def _validar_grafo(n, aristas):
    if not isinstance(n, int) or isinstance(n, bool) or n < 3:
        raise EntradaInvalida("n debe ser un entero >= 3 (grafo simple)")
    if not isinstance(aristas, (list, tuple)):
        raise EntradaInvalida("las aristas deben ser una lista de pares")
    E = set()
    for a in aristas:
        if (not isinstance(a, (list, tuple)) or len(a) != 2
                or not all(isinstance(x, int) and not isinstance(x, bool) for x in a)):
            raise EntradaInvalida("arista mal formada: %r" % (a,))
        u, v = a
        if not (0 <= u < n and 0 <= v < n):
            raise EntradaInvalida("vértice fuera de rango en %r" % (a,))
        if u == v:
            raise EntradaInvalida("lazo no permitido en grafo simple: %r" % (a,))
        E.add(frozenset((u, v)))
    return E


def reducir_ciclo_hamiltoniano(n, aristas):
    """f(G) = (D, L): D[u][v] = 1 si {u,v} ∈ E, 2 si no (0 en la diagonal);
    L = n.  G tiene ciclo hamiltoniano  <=>  existe tour con costo <= n.
    Construcción O(n^2). Los pesos 1/2 cumplen la desigualdad triangular, así
    que la instancia es simétrica y métrica, como la del correo."""
    E = _validar_grafo(n, aristas)
    D = [[0 if i == j else (1 if frozenset((i, j)) in E else 2) for j in range(n)]
         for i in range(n)]
    return D, n


def tiene_ciclo_hamiltoniano(n, aristas) -> bool:
    """Decisor directo por fuerza bruta (solo para PROBAR la reducción;
    no usa la matriz D)."""
    E = _validar_grafo(n, aristas)
    from itertools import permutations
    for resto in permutations(range(1, n)):
        ciclo = (0,) + resto
        if all(frozenset((ciclo[k], ciclo[(k + 1) % n])) in E for k in range(n)):
            return True
    return False


# ======================================================================
# 3. PRESENTACIÓN
# ======================================================================

def formatear_resultado(dist, limite, nombres, cerrar_ciclo=True) -> str:
    modo = "ciclo (regresa al punto de salida)" if cerrar_ciclo else "camino (no regresa)"
    nom = lambda orden: " -> ".join(nombres[i] for i in (
        list(orden) + ([orden[0]] if cerrar_ciclo and len(orden) > 1 else [])))
    lineas = [
        "=== C2 · TSP de decisión ===",
        "Centros (n=%d): %s" % (len(dist), ", ".join(nombres)),
        "Matriz simétrica: %s | L = %s | modo: %s" % (
            "sí" if es_simetrica(dist) else "no", limite, modo),
    ]
    r = buscar_exacto(dist, limite, cerrar_ciclo)
    if r.existe:
        lineas.append("[Exacto]     Respuesta: SÍ  | recorrido: %s | costo = %s | nodos explorados = %d"
                      % (nom(r.recorrido), r.costo, r.nodos))
        lineas.append("[Verificador] certificado %s aceptado: %s"
                      % (r.recorrido, verificar(dist, limite, r.recorrido, cerrar_ciclo)))
    else:
        lineas.append("[Exacto]     Respuesta: NO  | se agotó el espacio de búsqueda (nodos explorados = %d)"
                      % r.nodos)
    veredicto, orden, costo = decidir_heuristico(dist, limite, cerrar_ciclo)
    lineas.append("[Heurística] vecino más cercano: %s | costo = %s | veredicto: %s"
                  % (nom(orden), costo, veredicto))
    orden_opt, costo_opt = optimo_held_karp(dist, cerrar_ciclo)
    lineas.append("[Optimización, solo referencia] óptimo Held–Karp: %s | costo mínimo = %s"
                  % (nom(orden_opt), costo_opt))
    return "\n".join(lineas)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="C2 · TSP de decisión (LOGISTPULSE)")
    p.add_argument("--archivo", help="JSON con 'distancias', 'limite' y opcional 'centros'")
    p.add_argument("--modo", choices=["ciclo", "camino"], default="ciclo",
                   help="ciclo = regresa al punto de salida (lectura principal)")
    args = p.parse_args(argv)
    try:
        if args.archivo:
            with open(args.archivo, encoding="utf-8") as fh:
                texto = fh.read()
        else:
            texto = json.dumps(INSTANCIA_CORREO)
        dist, limite, nombres = leer_instancia(texto)
    except (EntradaInvalida, OSError) as exc:
        print("Error de entrada: %s" % exc, file=sys.stderr)
        return 2
    print(formatear_resultado(dist, limite, nombres, args.modo == "ciclo"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
