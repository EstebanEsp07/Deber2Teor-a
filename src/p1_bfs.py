"""
P1 · ¿Puede llegar el envío a la zona Norte?  (Daniela Paredes · Planificación)

Problema de decisión (alcanzabilidad dirigida):
    Entrada : red dirigida G = (V, E), origen s, destino t.
    Pregunta: ¿existe un camino dirigido de s a t?  (Sí / No)

Separación de responsabilidades:
    leer_red()     -> lectura y validación de la entrada
    camino_bfs()   -> procesamiento (BFS con predecesores)
    alcanzable()   -> versión de decisión (Sí/No)
    main()         -> presentación de resultados
"""
from collections import deque


# ---------------------------------------------------------------- lectura
def leer_red(aristas):
    """Convierte una lista de pares (u, v) en lista de adyacencia.

    Todo vértice (también los que solo aparecen como destino) queda como
    clave del diccionario, de modo que V = grafo.keys().
    """
    if not isinstance(aristas, (list, tuple)):
        raise TypeError("aristas debe ser una lista de pares (origen, destino)")
    grafo = {}
    for par in aristas:
        if not isinstance(par, (list, tuple)) or len(par) != 2:
            raise ValueError(f"arista inválida: {par!r}")
        u, v = par
        grafo.setdefault(u, [])
        grafo.setdefault(v, [])
        grafo[u].append(v)
    return grafo


def _vertices(grafo):
    if not isinstance(grafo, dict):
        raise TypeError("grafo debe ser un dict {vértice: [sucesores]}")
    vs = set(grafo)
    for sucesores in grafo.values():
        vs.update(sucesores)
    return vs


# ----------------------------------------------------------- procesamiento
def camino_bfs(grafo, origen, destino):
    """Devuelve el camino con MENOS ARISTAS de origen a destino, o None.

    Invariante: 'predecesor' contiene exactamente los vértices descubiertos;
    'cola' contiene los descubiertos aún no expandidos. Cada vértice entra a
    la cola a lo sumo una vez, por lo que el ciclo termina en <= |V| vueltas.
    Si la cola se vacía sin hallar el destino, el conjunto descubierto es
    cerrado bajo sucesores y no contiene a t: no existe camino.
    Tiempo O(V + E); espacio O(V).
    """
    vertices = _vertices(grafo)
    for nombre, nodo in (("origen", origen), ("destino", destino)):
        if nodo not in vertices:
            raise ValueError(f"{nombre} {nodo!r} no pertenece a la red")

    predecesor = {origen: origen}
    cola = deque([origen])
    while cola:
        u = cola.popleft()
        if u == destino:
            ruta, nodo = [], u
            while True:
                ruta.append(nodo)
                if nodo == origen:
                    break
                nodo = predecesor[nodo]
            return ruta[::-1]
        for v in grafo.get(u, []):
            if v not in predecesor:
                predecesor[v] = u
                cola.append(v)
    return None


def alcanzable(grafo, origen, destino):
    """Versión de decisión: True si existe camino dirigido origen -> destino."""
    return camino_bfs(grafo, origen, destino) is not None


# ------------------------------------------------------------ presentación
def main():
    # Datos del expediente p1 del simulador
    aristas = [("Durán", "Quito"), ("Durán", "Guayaquil"),
               ("Quito", "Norte"), ("Guayaquil", "Sur")]
    red = leer_red(aristas)
    consultas = [("Durán", "Norte"), ("Durán", "Sur"),
                 ("Quito", "Sur"), ("Norte", "Durán")]
    for s, t in consultas:
        ruta = camino_bfs(red, s, t)
        veredicto = "Sí" if ruta else "No"
        detalle = " -> ".join(ruta) if ruta else "sin camino"
        print(f"¿{s} alcanza {t}? {veredicto}  [{detalle}]")


if __name__ == "__main__":
    main()
