"""Decide de qué tipo es un correo: reserva, pregunta o derivar.

La parte de IA ya viene con su lectura del hilo. Acá no se vuelve a leer el
correo: se decide, que es distinto. Lo que decide esto es determinista y se
puede probar sin llamar a ningún modelo.
"""

INTENCIONES = ("reserva", "pregunta", "derivar")


def clasificar(hilo: dict, lectura: dict, config: dict) -> tuple[str, str | None]:
    """Devuelve la intención del correo y, si hay que derivarlo, por qué.

    El motivo 'salud' manda sobre todo lo demás: si aparece, la ficha se vacía.
    """
    if lectura.get("senales_salud") or _hay_palabra_de_salud(hilo, config):
        return "derivar", "salud"

    if lectura.get("pide_recomendacion"):
        return "derivar", "recomendacion"

    intencion = lectura.get("intencion")
    if intencion not in INTENCIONES:
        return "derivar", "otro"

    return intencion, "otro" if intencion == "derivar" else None


def _hay_palabra_de_salud(hilo: dict, config: dict) -> bool:
    """Red de seguridad por si la IA no vio la señal.

    Se miran las listas de todos los idiomas, no solo la del idioma detectado:
    un correo en inglés puede traer una palabra en castellano y al revés.
    """
    texto = " ".join(m["texto"] for m in hilo["mensajes"]).lower()
    for palabras in config["senales_salud"].values():
        if any(palabra.lower() in texto for palabra in palabras):
            return True
    return False
