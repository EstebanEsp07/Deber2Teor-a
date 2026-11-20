"""
Fase C · Regla de reposición (punto de pedido)  — responsable: Richard

Regla (del enunciado), para cada SKU:
    posición   = disponible + en_órdenes_abiertas − reservado
    si posición <= mínimo:  sugerencia = max(0, objetivo − posición)
    si no:                  sugerencia = 0

Anti-duplicación: las unidades de las órdenes abiertas YA suman a la posición.
Cuando se emite una orden por `sugerencia`, la siguiente consulta ve
posición = objetivo y devuelve 0. Por eso no se vuelve a pedir lo ya pedido.

Supuestos declarados (ver docs/FASE_C_fefo_reposicion.md):
    R1. Las cantidades son enteros >= 0.  `reservado` puede superar a
        disponible + en_órdenes: la posición queda negativa (pedido pendiente).
    R2. objetivo >= mínimo (una configuración con objetivo < mínimo es incoherente).
    R3. La orden emitida se registra como abierta antes de la siguiente consulta;
        si no, la regla (que es una función pura) repetiría la sugerencia.

Separación de responsabilidades:
    validar / calcular_posicion / sugerir_reposicion -> procesamiento (O(1))
    sugerir_catalogo()  -> recorrido de P productos (O(P))
    main()              -> presentación
"""


# ---------------------------------------------------------------- lectura
def _validar_entero(valor, nombre):
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise TypeError(f"{nombre} debe ser un entero")
    if valor < 0:
        raise ValueError(f"{nombre} no puede ser negativo")


# ----------------------------------------------------------- procesamiento
def calcular_posicion(disponible, en_ordenes_abiertas, reservado):
    """posición = disponible + en_órdenes_abiertas − reservado. Tiempo y espacio O(1)."""
    _validar_entero(disponible, "disponible")
    _validar_entero(en_ordenes_abiertas, "en_ordenes_abiertas")
    _validar_entero(reservado, "reservado")
    return disponible + en_ordenes_abiertas - reservado


def sugerir_reposicion(disponible, en_ordenes_abiertas, reservado, minimo, objetivo):
    """Devuelve (posición, sugerencia). Sin ciclos: termina siempre. Tiempo y espacio O(1)."""
    _validar_entero(minimo, "minimo")
    _validar_entero(objetivo, "objetivo")
    if objetivo < minimo:                                  # R2
        raise ValueError("objetivo no puede ser menor que minimo")
    posicion = calcular_posicion(disponible, en_ordenes_abiertas, reservado)
    if posicion <= minimo:                                 # incluye la igualdad (<=)
        return posicion, max(0, objetivo - posicion)
    return posicion, 0


def sugerir_catalogo(filas):
    """filas: lista de (sku, disponible, en_ordenes, reservado, minimo, objetivo).

    Devuelve [(sku, posición, sugerencia)] en el mismo orden. Tiempo O(P);
    espacio O(1) adicional por producto, O(P) por la lista de salida.
    """
    if not isinstance(filas, (list, tuple)):
        raise TypeError("filas debe ser una lista de tuplas")
    salida = []
    for fila in filas:
        if not isinstance(fila, (list, tuple)) or len(fila) != 6:
            raise ValueError(f"fila mal formada: {fila!r}")
        sku, disponible, en_ordenes, reservado, minimo, objetivo = fila
        posicion, sugerencia = sugerir_reposicion(disponible, en_ordenes, reservado,
                                                  minimo, objetivo)
        salida.append((sku, posicion, sugerencia))
    return salida


# ------------------------------------------------------------ presentación
def main():
    # Ejemplo del enunciado: 18, 10, 5, mínimo 30, objetivo 50
    pos, sug = sugerir_reposicion(18, 10, 5, 30, 50)
    print(f"Ejemplo del deber: posición = {pos}, sugerencia = {sug}")

    # Anti-duplicación: se emite la orden y se vuelve a consultar
    pos2, sug2 = sugerir_reposicion(18, 10 + sug, 5, 30, 50)
    print(f"Tras emitir la orden de {sug}: posición = {pos2}, sugerencia = {sug2}")

    # Catálogo de ejemplo (datos ilustrativos propios)
    filas = [("SKU-A", 18, 10, 5, 30, 50),     # bajo el mínimo
             ("SKU-B", 80, 0, 10, 30, 50),     # cómodo
             ("SKU-C", 25, 0, 0, 30, 50),      # bajo el mínimo (25 < 30)
             ("SKU-D", 30, 0, 0, 30, 50),      # posición == mínimo -> sí sugiere
             ("SKU-E", 5, 0, 20, 30, 50)]      # reservado > disponible: posición negativa
    for sku, posicion, sugerencia in sugerir_catalogo(filas):
        print(f"{sku}: posición = {posicion}, sugerencia = {sugerencia}")


if __name__ == "__main__":
    main()
