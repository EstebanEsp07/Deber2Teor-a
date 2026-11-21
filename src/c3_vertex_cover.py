"""
C3 · ¿Bastan k almacenes para cubrir todas las zonas?  (Carla Núñez · Red logística)

Problema de decisión (VERTEX COVER, cobertura de vértices):
    Entrada : un grafo G no dirigido y simple (zonas = vértices, corredores =
              aristas) y un entero k >= 0.
    Pregunta: ¿existe un conjunto S de a lo sumo k vértices tal que TODA arista
              tenga al menos un extremo en S?  (Sí / No)

Supuesto declarado (ver fichas/C3_vertex_cover.md):
    El texto corto del correo habla de «zona cubierta por un almacén propio o
    vecino» (eso sería CONJUNTO DOMINANTE), pero el cuerpo del correo («cada
    corredor debe tener un equipo en al menos uno de sus extremos»), la pregunta
    de datos («¿Cubre toda arista?»), el título y el código del simulador
    hablan de cubrir ARISTAS. Se analiza VERTEX COVER y se mantiene en toda la ficha.

Certificado "Sí": el conjunto S (lista de vértices). Se verifica en O(V + E).
Búsqueda exacta : ramificación por aristas (si una arista (u, v) no está cubierta,
                  u o v tienen que estar en S).  Referencia: enumerar subconjuntos.

Representación del grafo (igual que el simulador): diccionario de adyacencia
    {'A': ['B'], 'B': ['A', 'C'], 'C': ['B']}      (listas o tuplas de vecinos)

Separación de responsabilidades:
    validar_grafo()                   -> lectura/validación
    verificar_cobertura()             -> VERIFICADOR del certificado (polinomial)
    buscar_cobertura(), buscar_fuerza_bruta(), cobertura_minima() -> búsqueda exacta
    reduccion_3sat_a_vertex_cover()   -> la reducción de la ficha (3-SAT ≤p VC)
    main()                            -> presentación
"""
from itertools import combinations


# ------------------------------------------------------------ validación
def _validar_k(k):
    if isinstance(k, bool) or not isinstance(k, int):
        raise TypeError("k debe ser un entero")
    if k < 0:
        raise ValueError("k no puede ser negativo")


def validar_grafo(grafo):
    """Comprueba el grafo y devuelve su lista de aristas [(u, v), ...], cada una una sola vez.

    Exige: diccionario; vecinos en lista o tupla (así el orden es reproducible);
    vecinos que sean vértices del grafo; sin lazos; sin vecinos repetidos; simétrico
    (no dirigido). Lanza TypeError/ValueError. Tiempo O(V + E), espacio O(V + E).
    """
    if not isinstance(grafo, dict):
        raise TypeError("el grafo debe ser un diccionario de adyacencia")
    for u, vecinos in grafo.items():
        if not isinstance(vecinos, (list, tuple)):
            raise TypeError(f"los vecinos de {u!r} deben ser una lista o tupla")
    conjuntos = {u: set(vecinos) for u, vecinos in grafo.items()}   # para consultar en O(1)
    for u, vecinos in grafo.items():
        if len(conjuntos[u]) != len(vecinos):
            raise ValueError(f"vecinos repetidos en {u!r}")
        for v in vecinos:
            if v not in grafo:
                raise ValueError(f"{v!r} es vecino de {u!r} pero no es un vértice")
            if v == u:
                raise ValueError(f"lazo en {u!r}")
            if u not in conjuntos[v]:
                raise ValueError(f"el grafo no es simétrico: falta {v!r} -> {u!r}")
    posicion = {u: i for i, u in enumerate(grafo)}
    return [(u, v) for u in grafo for v in grafo[u] if posicion[u] < posicion[v]]


# ------------------------------------------------------------ verificador
def verificar_cobertura(grafo, k, seleccion):
    """VERIFICADOR del certificado, independiente de la búsqueda. Tiempo O(V + E).

    Acepta si `seleccion` es un conjunto de vértices distintos del grafo, con a lo
    sumo k elementos, y toda arista tiene un extremo en él. Un certificado mal
    formado se rechaza (False); un grafo o k inválidos lanzan excepción.
    """
    aristas = validar_grafo(grafo)
    _validar_k(k)
    if not isinstance(seleccion, (list, tuple, set, frozenset)):
        return False
    try:
        conjunto = set(seleccion)
    except TypeError:                      # algún elemento no es hashable
        return False
    if len(conjunto) != len(seleccion):    # repetidos: no es un conjunto
        return False
    if len(conjunto) > k:
        return False
    if any(v not in grafo for v in conjunto):
        return False
    return all(u in conjunto or v in conjunto for u, v in aristas)


# --------------------------------------------- búsqueda: ramificación por aristas
def _ramificar(aristas, k, elegidos):
    """Devuelve una lista de a lo sumo k vértices que cubre `aristas`, o None.

    Idea: si queda una arista (u, v) sin cubrir, TODA cobertura contiene a u o a v.
    Se prueba u y, si falla, v; cada elección cubre las aristas que tocan ese vértice
    y gasta 1 de presupuesto. Terminación: k baja en 1 en cada llamada y con k = 0 se
    para, así que la profundidad es <= k; además cada elección es un vértice nuevo
    (todas sus aristas ya se quitaron), así que la profundidad es <= V.
    """
    if not aristas:
        return list(elegidos)              # todas cubiertas
    if k == 0:
        return None                        # quedan aristas y no queda presupuesto
    u, v = aristas[0]
    for w in (u, v):
        restantes = [e for e in aristas if w not in e]
        resultado = _ramificar(restantes, k - 1, elegidos + [w])
        if resultado is not None:
            return resultado
    return None


def buscar_cobertura(grafo, k):
    """Devuelve una cobertura de a lo sumo k vértices o None. Exacto.

    OJO: si el grafo no tiene aristas devuelve [] (lista vacía, falsa en Python);
    comparar siempre con 'is not None'.

    Tiempo O(V + E + 2^min(k,V) * E): el árbol tiene <= 2^(min(k,V)+1) - 1 nodos y
    cada nodo filtra las aristas en O(E). Espacio O(min(k,V) * E) (cada nivel guarda
    la lista de aristas restantes).
    """
    aristas = validar_grafo(grafo)
    _validar_k(k)
    return _ramificar(aristas, k, [])


def es_coberturable(grafo, k):
    """Versión de decisión (Sí/No)."""
    return buscar_cobertura(grafo, k) is not None


# --------------------------------------------- referencia: enumerar subconjuntos
def buscar_fuerza_bruta(grafo, k):
    """Prueba todos los subconjuntos de tamaño 0..min(k, V). Exacto.

    Tiempo O(sum_{i<=min(k,V)} C(V, i) * E) <= O(2^V * (V + E)); espacio O(V).
    Sirve para contrastar la ramificación en las pruebas.
    """
    aristas = validar_grafo(grafo)
    _validar_k(k)
    vertices = list(grafo)
    for tam in range(min(k, len(vertices)) + 1):
        for candidato in combinations(vertices, tam):
            conjunto = set(candidato)
            if all(u in conjunto or v in conjunto for u, v in aristas):
                return list(candidato)
    return None


# --------------------------------------------- versión de optimización
def cobertura_minima(grafo):
    """Versión de OPTIMIZACIÓN: una cobertura de tamaño mínimo (se busca con k = 0, 1, 2...).

    Siempre termina: con k = V basta con elegir todos los vértices. Es NP-difícil
    como problema de optimización. Tiempo O(V * (V + E + 2^V * E)) en el peor caso.
    """
    validar_grafo(grafo)
    for k in range(len(grafo) + 1):
        cobertura = buscar_cobertura(grafo, k)
        if cobertura is not None:
            return cobertura


# --------------------------------------------- reducción 3-SAT ≤p VERTEX COVER
def reduccion_3sat_a_vertex_cover(clausulas, n):
    """Construye (grafo, k) tal que la fórmula es satisfacible  <=>  el grafo tiene
    una cobertura de a lo sumo k = n + 2m vértices.  (Sipser, cap. 7: VERTEX-COVER.)

    Entrada: n variables y m cláusulas de EXACTAMENTE 3 literales (el literal k es xk
    y -k es ¬xk; se admiten literales repetidos dentro de la cláusula, que es el
    relleno de C1). Construcción:
      - por cada variable xi: dos vértices «xi» y «¬xi» unidos por una arista;
      - por cada cláusula j: un triángulo de 3 vértices «Cj.1», «Cj.2», «Cj.3»,
        y cada vértice del triángulo se une al vértice de variable de su literal.
    Tamaño: 2n + 3m vértices y n + 6m aristas, o sea tiempo y espacio O(n + m).
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n debe ser un entero")
    if n < 0:
        raise ValueError("n no puede ser negativo")
    if not isinstance(clausulas, (list, tuple)):
        raise TypeError("clausulas debe ser una lista")
    for c in clausulas:
        if not isinstance(c, (list, tuple)) or len(c) != 3:
            raise ValueError(f"la cláusula debe tener exactamente 3 literales: {c!r}")
        for lit in c:
            if isinstance(lit, bool) or not isinstance(lit, int):
                raise TypeError(f"literal no entero: {lit!r}")
            if lit == 0 or abs(lit) > n:
                raise ValueError(f"literal fuera de rango (1..{n}): {lit}")

    grafo = {}

    def unir(a, b):
        grafo.setdefault(a, []).append(b)
        grafo.setdefault(b, []).append(a)

    def vertice_de_variable(lit):
        return f"x{lit}" if lit > 0 else f"¬x{-lit}"

    for i in range(1, n + 1):
        unir(f"x{i}", f"¬x{i}")
    for j, c in enumerate(clausulas, start=1):
        a, b, d = (f"C{j}.1", f"C{j}.2", f"C{j}.3")
        unir(a, b)
        unir(a, d)
        unir(b, d)
        for vertice, lit in zip((a, b, d), c):
            unir(vertice, vertice_de_variable(lit))
    return grafo, n + 2 * len(clausulas)


# ------------------------------------------------------------ presentación
def main():
    # Datos del expediente c3 del simulador: aristas A-B y B-C, k = 1
    grafo = {"A": ["B"], "B": ["A", "C"], "C": ["B"]}
    k = 1
    cobertura = buscar_cobertura(grafo, k)
    print(f"¿Bastan {k} equipo(s) para cubrir A-B y B-C?", "Sí" if cobertura is not None else "No")
    print("Cobertura encontrada:", cobertura)
    print("Verificador acepta ['B']:", verificar_cobertura(grafo, k, ["B"]))
    print("Verificador acepta ['A'] (B-C queda sin cubrir):", verificar_cobertura(grafo, k, ["A"]))
    print("Verificador acepta ['A', 'C'] con k = 1 (son 2 > k):", verificar_cobertura(grafo, k, ["A", "C"]))
    print("Verificador acepta ['A', 'C'] con k = 2:", verificar_cobertura(grafo, 2, ["A", "C"]))
    print("Con k = 0:", buscar_cobertura(grafo, 0))
    print("Cobertura mínima (optimización):", cobertura_minima(grafo))

    # La reducción de la ficha, sobre la fórmula de C1 (x1 ∨ ¬x2) ∧ (x2 ∨ x3), rellenada a 3 literales
    formula = [[1, -2, -2], [2, 3, 3]]
    g, kk = reduccion_3sat_a_vertex_cover(formula, 3)
    print(f"Reducción de C1: grafo de {len(g)} vértices, k = {kk} ->",
          "Sí" if es_coberturable(g, kk) else "No", "(la fórmula es satisfacible)")
    insat = [[1, 2, 2], [-1, 2, 2], [1, -2, -2], [-1, -2, -2]]
    g2, k2 = reduccion_3sat_a_vertex_cover(insat, 2)
    print(f"Reducción de una fórmula insatisfacible: {len(g2)} vértices, k = {k2} ->",
          "Sí" if es_coberturable(g2, k2) else "No")


if __name__ == "__main__":
    main()
