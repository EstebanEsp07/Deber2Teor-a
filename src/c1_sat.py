"""
C1 · ¿Hay una asignación que cumpla todas las reglas?  (Mónica Ruiz · Planificación)

Problema de decisión (SAT con cláusulas de a lo sumo 3 literales, "3-CNF"):
    Entrada : n variables x1..xn y m cláusulas. Una cláusula es una lista de
              a lo sumo 3 literales; el literal  k  significa xk  y  -k  significa ¬xk.
              Ejemplo del correo: [[1, -2], [2, 3]]  =  (x1 ∨ ¬x2) ∧ (x2 ∨ x3).
    Pregunta: ¿existe una asignación de verdadero/falso a las n variables que
              haga verdaderas TODAS las cláusulas?  (Sí / No)

Certificado "Sí": la asignación {1: bool, ..., n: bool}.  Se verifica en O(n + m).
Búsqueda exacta : DPLL (propagación unitaria + ramificación). Peor caso exponencial.
Referencia      : enumeración de las 2^n asignaciones (se usa para contrastar).

Supuestos declarados (ver fichas/C1_sat_3cnf.md):
    S1. "3-CNF" = cada cláusula tiene a lo sumo 3 literales (el correo trae
        cláusulas de 2 literales). Es equivalente a exactamente 3 por relleno.
    S2. La cláusula vacía es falsa (fórmula insatisfacible); sin cláusulas la
        fórmula es verdadera (satisfacible).
    S3. Las n variables existen aunque no aparezcan en ninguna cláusula; la
        asignación devuelta las incluye todas.

Separación de responsabilidades:
    validar_formula()               -> lectura/validación
    verificar_asignacion()          -> VERIFICADOR del certificado (polinomial)
    resolver_fuerza_bruta(), resolver_dpll() -> búsqueda exacta
    main()                          -> presentación
"""
from itertools import product


# ------------------------------------------------------------ validación
def validar_formula(clausulas, n):
    """Comprueba la fórmula y devuelve las cláusulas sin literales repetidos.

    Lanza TypeError/ValueError si la entrada es inválida. Tiempo O(m), espacio O(m).
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise TypeError("n debe ser un entero")
    if n < 0:
        raise ValueError("n no puede ser negativo")
    if not isinstance(clausulas, (list, tuple)):
        raise TypeError("clausulas debe ser una lista de cláusulas")
    limpias = []
    for c in clausulas:
        if not isinstance(c, (list, tuple)):
            raise ValueError(f"cláusula mal formada: {c!r}")
        if len(c) > 3:
            raise ValueError(f"la cláusula {list(c)!r} tiene más de 3 literales")  # S1
        for lit in c:
            if isinstance(lit, bool) or not isinstance(lit, int):
                raise TypeError(f"literal no entero: {lit!r}")
            if lit == 0 or abs(lit) > n:
                raise ValueError(f"literal fuera de rango (1..{n}): {lit}")
        limpias.append(list(dict.fromkeys(c)))      # quita repetidos, conserva el orden
    return limpias


# ------------------------------------------------------------ verificador
def verificar_asignacion(clausulas, n, asignacion):
    """VERIFICADOR del certificado. Tiempo O(n + m), espacio O(m) (la validación copia las cláusulas).

    Acepta si `asignacion` da un booleano a cada x1..xn y toda cláusula tiene
    al menos un literal verdadero. Una asignación mal formada se rechaza
    (False); una fórmula inválida lanza excepción.
    """
    cls = validar_formula(clausulas, n)
    if not isinstance(asignacion, dict) or set(asignacion) != set(range(1, n + 1)):
        return False
    if any(type(v) is not bool for v in asignacion.values()):
        return False
    # Una cláusula (≤ 3 literales) es verdadera si algún literal lo es.
    return all(any(asignacion[abs(lit)] == (lit > 0) for lit in c) for c in cls)


# ------------------------------------------------- búsqueda: fuerza bruta
def resolver_fuerza_bruta(clausulas, n):
    """Prueba las 2^n asignaciones. Exacto. Tiempo O(2^n * (n + m)), espacio O(n + m).

    Devuelve la primera asignación que cumple (orden False < True) o None.
    OJO: para n = 0 una fórmula satisfacible devuelve {} (dict vacío, falso en
    Python); comparar siempre con 'is not None'.
    """
    validar_formula(clausulas, n)
    for bits in product([False, True], repeat=n):
        asignacion = {i + 1: bits[i] for i in range(n)}
        if verificar_asignacion(clausulas, n, asignacion):
            return asignacion
    return None


# ----------------------------------------------------------------- DPLL
def _simplificar(clausulas, lit):
    """Hace verdadero el literal `lit`: borra las cláusulas que lo contienen y
    quita ¬lit de las demás. Devuelve None si alguna cláusula queda vacía
    (conflicto). No modifica la entrada. Tiempo O(tamaño de la fórmula)."""
    nuevas = []
    for c in clausulas:
        if lit in c:
            continue                       # cláusula satisfecha
        resto = [x for x in c if x != -lit]
        if not resto:
            return None                    # cláusula vacía: conflicto
        nuevas.append(resto)
    return nuevas


def _dpll(clausulas, asignacion):
    """DPLL recursivo. Rellena `asignacion` con las variables decididas y
    devuelve True/False.

    Terminación: cada paso (unitario o ramificación) asigna una variable y
    elimina TODAS sus apariciones de la fórmula, así que el número de variables
    distintas en la fórmula baja en 1 en cada paso. La profundidad es <= n.
    """
    # 1) propagación unitaria: una cláusula de 1 literal obliga ese literal
    while True:
        unitaria = None
        for c in clausulas:
            if len(c) == 1:
                unitaria = c[0]
                break
        if unitaria is None:
            break
        asignacion[abs(unitaria)] = unitaria > 0
        clausulas = _simplificar(clausulas, unitaria)
        if clausulas is None:
            return False
    if not clausulas:
        return True                        # todas las cláusulas satisfechas
    # 2) ramificación: se prueba un literal y, si falla, su negación
    lit = clausulas[0][0]
    for elegido in (lit, -lit):
        nuevas = _simplificar(clausulas, elegido)
        if nuevas is None:
            continue
        copia = dict(asignacion)
        copia[abs(elegido)] = elegido > 0
        if _dpll(nuevas, copia):
            asignacion.update(copia)
            return True
    return False


def resolver_dpll(clausulas, n):
    """Resuelve SAT con DPLL (propagación unitaria + ramificación). Exacto.

    No usa eliminación de literales puros ni heurísticas de elección: es la
    versión básica. Peor caso: árbol de <= 2^(n+1) nodos y O(n*m) por nodo
    => O(2^n * n * m) tiempo. Espacio O(n*m) (cada nivel guarda una copia de la
    fórmula simplificada; la profundidad es <= n).
    Devuelve una asignación completa (variables libres en False) o None.
    OJO: igual que la fuerza bruta, comparar con 'is not None' (n = 0 da {}).
    """
    cls = validar_formula(clausulas, n)
    if any(len(c) == 0 for c in cls):      # S2: cláusula vacía => insatisfacible
        return None
    asignacion = {}
    if not _dpll(cls, asignacion):
        return None
    for i in range(1, n + 1):              # S3: variables que no aparecen
        asignacion.setdefault(i, False)
    return asignacion


def es_satisfacible(clausulas, n):
    """Versión de decisión (Sí/No)."""
    return resolver_dpll(clausulas, n) is not None


# ------------------------------------------------------------ presentación
def formatear(clausulas):
    """(x1 ∨ ¬x2) ∧ (x2 ∨ x3) a partir de [[1, -2], [2, 3]]."""
    def lit(k):
        return ("" if k > 0 else "¬") + f"x{abs(k)}"
    if not clausulas:
        return "(sin cláusulas)"
    return " ∧ ".join("(" + (" ∨ ".join(lit(k) for k in c) if c else "∅") + ")"
                      for c in clausulas)


def main():
    # Datos del expediente c1 del simulador: x1, x2, x3 ; (x1∨¬x2) ∧ (x2∨x3)
    n = 3
    formula = [[1, -2], [2, 3]]
    print("Fórmula:", formatear(formula))

    a = resolver_dpll(formula, n)
    print("¿Satisfacible (DPLL)?", "Sí" if a is not None else "No")
    if a is not None:
        print("Asignación:", a)
        print("Verificador acepta la asignación:", verificar_asignacion(formula, n, a))
    print("Fuerza bruta (primera en el orden F<T):", resolver_fuerza_bruta(formula, n))

    candidata = {1: False, 2: True, 3: False}          # viola (x1 ∨ ¬x2)
    print("Candidata", candidata, "->", verificar_asignacion(formula, n, candidata))

    # Insatisfacible: las 8 combinaciones de signos sobre 3 variables
    ocho = [[s1 * 1, s2 * 2, s3 * 3] for s1 in (1, -1) for s2 in (1, -1) for s3 in (1, -1)]
    print("Las 8 cláusulas de signos sobre x1,x2,x3 ->", resolver_dpll(ocho, 3))


if __name__ == "__main__":
    main()
