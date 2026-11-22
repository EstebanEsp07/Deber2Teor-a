"""
P3 · Capacidad máxima de despacho (LOGISTPULSE)
Flujo máximo con Edmonds–Karp (Ford–Fulkerson + BFS).

Estructura:
  1) LECTURA        -> leer_aristas_csv(), construir_red()
  2) PROCESAMIENTO  -> edmonds_karp(), corte_minimo(), existe_flujo_al_menos()
  3) PRESENTACIÓN   -> formatear_resultado()

Compatible con Python 3.8+; solo biblioteca estándar.
"""
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import sys

Red = Dict[str, Dict[str, int]]          # red[u][v] = capacidad u -> v
Arista = Tuple[str, str, int]

# Datos del expediente P3 (tabla del portal). NO se modifican.
DATOS_P3 = """origen,destino,capacidad
Planta,Quito,7
Planta,Guayaquil,5
Quito,Clientes,4
Guayaquil,Clientes,6
Quito,Guayaquil,2
"""


# ---------------------------------------------------------------- 1) LECTURA
def leer_aristas_csv(texto: str) -> List[Arista]:
    """Convierte texto 'origen,destino,capacidad' en una lista de aristas.
    Acepta una cabecera opcional. Lanza ValueError ante filas mal formadas."""
    if not isinstance(texto, str):
        raise TypeError("La entrada debe ser texto CSV.")
    aristas: List[Arista] = []
    for num, linea in enumerate(texto.strip().splitlines(), start=1):
        linea = linea.strip()
        if not linea:
            continue
        partes = [p.strip() for p in linea.split(",")]
        if num == 1 and partes[0].lower() == "origen":
            continue  # cabecera
        if len(partes) != 3:
            raise ValueError(f"Línea {num}: se esperaban 3 campos, hay {len(partes)}.")
        u, v, c = partes
        try:
            cap = int(c)
        except ValueError:
            raise ValueError(f"Línea {num}: capacidad no entera: {c!r}.") from None
        aristas.append((u, v, cap))
    return aristas


def construir_red(aristas: List[Arista]) -> Red:
    """Valida las aristas y construye la red dirigida.
    Aristas repetidas u->v se suman (capacidad total del tramo)."""
    red: Red = {}
    for arista in aristas:
        if not (isinstance(arista, (tuple, list)) and len(arista) == 3):
            raise ValueError(f"Arista mal formada: {arista!r}.")
        u, v, c = arista
        for nombre in (u, v):
            if not isinstance(nombre, str) or not nombre.strip():
                raise ValueError(f"Nombre de nodo inválido: {nombre!r}.")
        if isinstance(c, bool) or not isinstance(c, int):
            raise ValueError(f"Capacidad no entera en {u}->{v}: {c!r}.")
        if c < 0:
            raise ValueError(f"Capacidad negativa en {u}->{v}: {c}.")
        if u == v:
            raise ValueError(f"Lazo no permitido: {u}->{v}.")
        red.setdefault(u, {})
        red.setdefault(v, {})
        red[u][v] = red[u].get(v, 0) + c
    return red


# ---------------------------------------------------------- 2) PROCESAMIENTO
@dataclass
class Aumento:
    camino: List[str]
    cuello: int
    actualizaciones: List[str]          # registro de tramos usados/disponibles


@dataclass
class ResultadoFlujo:
    valor: int
    aumentos: List[Aumento]
    flujo_por_arista: Dict[Tuple[str, str], int]
    lado_s: List[str]                   # nodos alcanzables desde s en el residual final
    corte: List[Arista]                 # aristas originales del corte mínimo
    capacidad_corte: int
    capacidades: Dict[Tuple[str, str], int] = field(default_factory=dict)
    residual: Red = field(repr=False, default_factory=dict)


def _validar_extremos(red: Red, s: str, t: str) -> None:
    if not isinstance(red, dict):
        raise TypeError("La red debe ser un diccionario.")
    if s == t:
        raise ValueError("Origen y destino deben ser distintos.")
    if s not in red:
        raise ValueError(f"El origen {s!r} no está en la red.")
    if t not in red:
        raise ValueError(f"El destino {t!r} no está en la red.")


def _residual_inicial(red: Red) -> Red:
    """Residual con arista inversa (capacidad 0) para cada arista original."""
    res: Red = {u: {} for u in red}
    for u, vecinos in red.items():
        for v, c in vecinos.items():
            res[u][v] = res[u].get(v, 0) + c
            res[v].setdefault(u, 0)
    return res


def _bfs_camino(res: Red, s: str, t: str) -> Optional[Dict[str, Optional[str]]]:
    """BFS sobre aristas con capacidad residual > 0.
    Devuelve el diccionario padre si alcanza t (camino con MENOS aristas), o None."""
    padre: Dict[str, Optional[str]] = {s: None}
    cola = deque([s])
    while cola:
        u = cola.popleft()
        for v, c in res[u].items():
            if c > 0 and v not in padre:   # solo tramos con capacidad disponible
                padre[v] = u
                if v == t:
                    return padre
                cola.append(v)
    return None


def edmonds_karp(red: Red, s: str, t: str) -> ResultadoFlujo:
    """Flujo máximo exacto de s a t. Tiempo O(V·E²), espacio O(V + E)."""
    _validar_extremos(red, s, t)
    res = _residual_inicial(red)
    valor = 0
    aumentos: List[Aumento] = []

    while True:
        padre = _bfs_camino(res, s, t)
        if padre is None:                       # no hay camino aumentante -> óptimo
            break
        # Reconstruir el camino t -> s
        camino = [t]
        while camino[-1] != s:
            camino.append(padre[camino[-1]])
        camino.reverse()
        # Cuello de botella
        cuello = min(res[camino[i]][camino[i + 1]] for i in range(len(camino) - 1))
        # Actualizar residual (directa -cuello, inversa +cuello) y registrar
        registro = []
        for i in range(len(camino) - 1):
            u, v = camino[i], camino[i + 1]
            antes_d, antes_i = res[u][v], res[v][u]
            res[u][v] -= cuello
            res[v][u] += cuello
            registro.append(f"{u}->{v}: {antes_d}->{res[u][v]} | "
                            f"inversa {v}->{u}: {antes_i}->{res[v][u]}")
        valor += cuello
        aumentos.append(Aumento(camino, cuello, registro))

    # Flujo neto por arista original
    flujo: Dict[Tuple[str, str], int] = {}
    for u, vecinos in red.items():
        for v, c in vecinos.items():
            f = c - res[u][v]
            flujo[(u, v)] = max(0, min(c, f))

    lado_s, corte, cap_corte = corte_minimo(red, res, s)
    capacidades = {(u, v): c for u in red for v, c in red[u].items()}
    return ResultadoFlujo(valor, aumentos, flujo, lado_s, corte, cap_corte,
                          capacidades, res)


def corte_minimo(red: Red, res: Red, s: str) -> Tuple[List[str], List[Arista], int]:
    """S = nodos alcanzables desde s en el residual final; corte = aristas S -> V\\S."""
    S = {s}
    cola = deque([s])
    while cola:
        u = cola.popleft()
        for v, c in res[u].items():
            if c > 0 and v not in S:
                S.add(v)
                cola.append(v)
    corte = [(u, v, c) for u in red for v, c in red[u].items()
             if u in S and v not in S]
    return sorted(S), corte, sum(c for _, _, c in corte)


def existe_flujo_al_menos(red: Red, s: str, t: str, K: int) -> bool:
    """Versión de DECISIÓN: ¿existe un flujo s-t de valor >= K?"""
    if isinstance(K, bool) or not isinstance(K, int) or K < 0:
        raise ValueError("K debe ser un entero no negativo.")
    return edmonds_karp(red, s, t).valor >= K


# ----------------------------------------------------------- 3) PRESENTACIÓN
def formatear_resultado(r: ResultadoFlujo, s: str, t: str) -> str:
    L = [f"Flujo máximo {s} -> {t}: {r.valor} camiones/día", "",
         "Traza de caminos aumentantes (BFS):"]
    for i, a in enumerate(r.aumentos, 1):
        L.append(f"  {i}. {' -> '.join(a.camino)}  (cuello = {a.cuello})")
        for reg in a.actualizaciones:
            L.append(f"       {reg}")
    L.append(f"  BFS final: no alcanza {t}; algoritmo termina.")
    L += ["", "Flujo por tramo (usado / capacidad):"]
    for (u, v), f in sorted(r.flujo_por_arista.items()):
        L.append(f"  {u}->{v}: {f}/{r.capacidades[(u, v)]}")
    L += ["", f"Corte mínimo: S = {{{', '.join(r.lado_s)}}}",
          "  Aristas S -> V\\S: " + ", ".join(f"{u}->{v}({c})" for u, v, c in r.corte),
          f"  Capacidad del corte = {r.capacidad_corte}",
          f"  ¿Flujo máximo = corte mínimo? {'Sí' if r.valor == r.capacidad_corte else 'NO'}"]
    return "\n".join(L)


def main(argv: List[str]) -> int:
    try:
        if len(argv) > 1:                      # archivo CSV opcional
            with open(argv[1], encoding="utf-8") as fh:
                texto = fh.read()
        else:
            texto = DATOS_P3
        red = construir_red(leer_aristas_csv(texto))
        resultado = edmonds_karp(red, "Planta", "Clientes")
    except (OSError, ValueError, TypeError) as e:
        print(f"Error de entrada: {e}", file=sys.stderr)
        return 1
    print(formatear_resultado(resultado, "Planta", "Clientes"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
