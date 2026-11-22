"""
B-03 · Dijkstra para el grafo de planta (Fase B)  ·  compartido con el correo P2
(Marco Cedeño · Transporte: «Ruta mínima entre centros de distribución»).

Problema (optimización): camino mínimo desde un origen s en un grafo con
pesos NO NEGATIVOS.
    Entrada : G = (V, E, w) con w(u, v) >= 0, origen s y (opcional) destino t.
    Salida  : dist[v] = menor costo de s a v para todo v, y la ruta s -> t
              reconstruida con predecesores (o "sin ruta" si dist[t] = inf).
Versión de decisión asociada (la que se clasifica en P):
    RUTA-CORTA = { <G, s, t, L> : existe una ruta de s a t con costo <= L }.

Separación de responsabilidades:
    leer_grafo(), bloquear()       -> lectura y validación de la entrada
    dijkstra(), ruta_minima()      -> procesamiento
    existe_ruta_con_costo_max()    -> versión de decisión (Sí/No)
    main()                         -> presentación
"""
import heapq
import math
from numbers import Real

INF = math.inf


# ---------------------------------------------------------------- lectura
def _validar_peso(peso, u, v):
    """Precondición de Dijkstra: peso real, finito y >= 0."""
    if isinstance(peso, bool) or not isinstance(peso, Real):
        raise TypeError(f"el peso de ({u!r}, {v!r}) debe ser numérico: {peso!r}")
    if math.isnan(peso) or math.isinf(peso):
        raise ValueError(f"el peso de ({u!r}, {v!r}) debe ser finito: {peso!r}")
    if peso < 0:
        # Decisión de diseño: rechazar en vez de devolver un resultado falso.
        # Con un peso negativo, un vértice ya "finalizado" podría mejorar
        # después, y Dijkstra no lo vuelve a procesar (ver ficha P2, §5).
        raise ValueError(f"peso negativo en ({u!r}, {v!r}) = {peso}: Dijkstra "
                         "exige pesos >= 0 (usar Bellman–Ford en ese caso)")


def leer_grafo(aristas, dirigido=False):
    """Convierte una lista de triples (u, v, peso) en lista de adyacencia.

    Si dirigido=False, cada pasillo se recorre en ambos sentidos y se guardan
    dos arcos (u->v y v->u); por eso en el análisis E cuenta arcos (2·pasillos).
    Todo vértice queda como clave del diccionario, aunque no tenga sucesores.
    """
    if not isinstance(aristas, (list, tuple)):
        raise TypeError("aristas debe ser una lista de triples (u, v, peso)")
    grafo = {}
    for tramo in aristas:
        if not isinstance(tramo, (list, tuple)) or len(tramo) != 3:
            raise ValueError(f"arista inválida (se espera (u, v, peso)): {tramo!r}")
        u, v, peso = tramo
        _validar_peso(peso, u, v)
        grafo.setdefault(u, [])
        grafo.setdefault(v, [])
        grafo[u].append((v, peso))
        if not dirigido:
            grafo[v].append((u, peso))
    return grafo


def bloquear(grafo, bloqueados):
    """Devuelve una copia del grafo SIN las zonas bloqueadas ni sus pasillos.

    Modelo: una zona bloqueada no se puede atravesar ni usar como origen o
    destino. Tiempo O(V + E).
    """
    vertices = _validar_grafo(grafo)
    bloqueados = set(bloqueados)
    faltan = bloqueados - vertices
    if faltan:
        raise ValueError(f"zonas bloqueadas que no existen: {sorted(map(str, faltan))}")
    return {u: [(v, w) for v, w in sucesores if v not in bloqueados]
            for u, sucesores in grafo.items() if u not in bloqueados}


def _validar_grafo(grafo):
    """Comprueba la estructura {u: [(v, peso), ...]} y devuelve V. O(V + E)."""
    if not isinstance(grafo, dict):
        raise TypeError("grafo debe ser un dict {vértice: [(vecino, peso), ...]}")
    vertices = set(grafo)
    for u, sucesores in grafo.items():
        if not isinstance(sucesores, (list, tuple)):
            raise TypeError(f"los sucesores de {u!r} deben ser una lista")
        for par in sucesores:
            if not isinstance(par, (list, tuple)) or len(par) != 2:
                raise ValueError(f"sucesor inválido de {u!r}: {par!r}")
            v, peso = par
            _validar_peso(peso, u, v)
            vertices.add(v)
    return vertices


# ----------------------------------------------------------- procesamiento
def _dijkstra_nucleo(grafo, origen):
    """Dijkstra "de libro" SIN validar pesos. Uso interno.

    Se separa para poder mostrar en las pruebas qué pasa con un peso
    negativo (contraejemplo de la ficha P2). No llamarlo directamente.

    Invariante: al FINALIZAR u (primera vez que sale de la cola),
    dist[u] es el costo mínimo real de origen a u. Vale porque todos los
    pesos son >= 0: cualquier otro camino pasa por un vértice aún en la
    cola, cuyo costo ya es >= dist[u], y los pesos restantes no lo bajan.
    """
    vertices = set(grafo)
    for sucesores in grafo.values():
        vertices.update(v for v, _ in sucesores)
    dist = {v: INF for v in vertices}
    predecesor = {}
    finalizado = set()
    dist[origen] = 0
    orden = 0                          # desempate estable: FIFO entre iguales
    cola = [(0, orden, origen)]        # montículo binario (cola de prioridad)
    while cola:
        d, _, u = heapq.heappop(cola)
        if u in finalizado:            # entrada obsoleta ("lazy deletion")
            continue
        finalizado.add(u)              # cada vértice se finaliza UNA vez
        for v, peso in grafo.get(u, ()):
            if v in finalizado:
                continue
            nueva = d + peso
            if nueva < dist[v]:        # '<' estricto: ante empate se conserva
                dist[v] = nueva        # el predecesor que llegó primero
                predecesor[v] = u
                orden += 1
                heapq.heappush(cola, (nueva, orden, v))
    return dist, predecesor


def dijkstra(grafo, origen):
    """Distancias mínimas desde origen a todo vértice y predecesores.

    Precondiciones (se validan): grafo bien formado, pesos reales finitos
    >= 0, origen en V.  Tiempo O((V + E) log V); espacio O(V + E).
    """
    vertices = _validar_grafo(grafo)
    if origen not in vertices:
        raise ValueError(f"origen {origen!r} no pertenece al grafo")
    return _dijkstra_nucleo(grafo, origen)


def reconstruir_ruta(predecesor, origen, destino):
    """Sigue los predecesores desde destino hasta origen. O(V)."""
    if destino != origen and destino not in predecesor:
        return None
    ruta = [destino]
    while ruta[-1] != origen:
        ruta.append(predecesor[ruta[-1]])
    return ruta[::-1]


def ruta_minima(grafo, origen, destino):
    """Devuelve (costo, ruta). Si no hay ruta: (inf, None)."""
    vertices = _validar_grafo(grafo)
    for nombre, nodo in (("origen", origen), ("destino", destino)):
        if nodo not in vertices:
            raise ValueError(f"{nombre} {nodo!r} no pertenece al grafo")
    dist, predecesor = _dijkstra_nucleo(grafo, origen)
    if dist[destino] == INF:
        return INF, None
    return dist[destino], reconstruir_ruta(predecesor, origen, destino)


def existe_ruta_con_costo_max(grafo, origen, destino, limite):
    """Versión de DECISIÓN: ¿existe ruta origen -> destino con costo <= L?"""
    if isinstance(limite, bool) or not isinstance(limite, Real) or math.isnan(limite):
        raise TypeError("el límite L debe ser un número")
    costo, _ = ruta_minima(grafo, origen, destino)
    return costo <= limite


# ------------------------------------------------------------ presentación
# Fase B: planta del enunciado (Figura 5). Pasillos NO dirigidos, metros.
PASILLOS_PLANTA = [
    ("R", "A", 4), ("R", "B", 2), ("A", "B", 1), ("A", "P", 3),
    ("A", "E", 5), ("B", "P", 7), ("B", "C", 3), ("P", "E", 2),
    ("P", "C", 2), ("C", "E", 4), ("E", "D", 3),
]
# Correo P2: tramos DIRIGIDOS (el mapa del simulador usa flechas).
TRAMOS_P2 = [
    ("Quito", "Latacunga", 2), ("Quito", "Ambato", 5),
    ("Latacunga", "Guayaquil", 6), ("Ambato", "Guayaquil", 3),
]


def _formato(costo, ruta):
    if ruta is None:
        return "sin ruta"
    return f"costo {costo}  [{' -> '.join(ruta)}]"


def main():
    planta = leer_grafo(PASILLOS_PLANTA, dirigido=False)
    print("== Fase B · AMR de R (Recepción) a D (Despacho) ==")
    escenarios = [("sin bloqueos", []), ("P bloqueada", ["P"]),
                  ("A y P bloqueadas", ["A", "P"]), ("E bloqueada", ["E"])]
    for nombre, bloq in escenarios:
        costo, ruta = ruta_minima(bloquear(planta, bloq), "R", "D")
        print(f"{nombre:>17}: {_formato(costo, ruta)}")
    dist, _ = dijkstra(planta, "R")
    print("Distancias desde R:", {v: dist[v] for v in sorted(dist)})
    print("¿Ruta R->D con costo <= 11?", existe_ruta_con_costo_max(planta, "R", "D", 11))
    print("¿Ruta R->D con costo <= 10?", existe_ruta_con_costo_max(planta, "R", "D", 10))

    print("\n== Correo P2 · desde CD Quito ==")
    red = leer_grafo(TRAMOS_P2, dirigido=True)
    dist, _ = dijkstra(red, "Quito")
    for v in ("Quito", "Latacunga", "Ambato", "Guayaquil"):
        print(f"  tiempo mínimo a {v}: {dist[v]}")
    print("  ruta a Guayaquil:", _formato(*ruta_minima(red, "Quito", "Guayaquil")))


if __name__ == "__main__":
    main()
