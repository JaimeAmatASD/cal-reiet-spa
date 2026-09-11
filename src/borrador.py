"""Redacta la respuesta al cliente. NO la envía: queda para que la revise una persona.

Reglas, todas del pedido de James:
  - en el idioma en que escribió el cliente
  - todo lo que falta se pregunta en un solo correo, nunca de a una cosa por vez
  - al preguntar la duración se ofrecen las tres opciones con su precio, porque
    el cliente no sabe qué elegir si no se lo pones delante
  - si dio una fecha, se le dice qué hay libre ese día
  - se le saluda por su nombre

Los textos no están acá: están en casa.yaml, para poder cambiarlos sin tocar
código. Este archivo solo decide qué bloques entran y en qué orden.
"""
import casa


def redactar(ficha: dict, config: dict, asunto_original: str) -> dict | None:
    """Devuelve el borrador, o None si esto lo tiene que escribir una persona."""
    idioma = ficha["idioma"]
    if idioma not in config["idiomas"]:
        return None

    nombre = ficha["cliente"]["nombre"]["valor"]
    if not nombre:
        return None

    textos = config["textos"]["borrador"][idioma]
    peticion = ficha["peticion"]
    falta = ficha["falta"]

    lineas = [textos["saludo"].format(nombre=nombre), ""]

    if falta:
        lineas += [textos["intro"], ""]
    elif not ficha["a_confirmar"]:
        # No falta nada y nada que confirmar. Si hay algo que confirmar, el
        # correo arranca directamente por ahí y no hace falta otra entrada.
        lineas += [textos["intro_completo"], ""]

    if "duracion" in falta:
        lineas.append(textos["pregunta_duracion"])
        lineas += _opciones_de_duracion(config, textos)
        lineas.append("")
    for campo in ("fecha", "franja", "personas"):
        if campo in falta:
            lineas += [textos[f"pregunta_{campo}"], ""]

    if ficha["a_confirmar"]:
        lineas.append(textos["intro_confirmar"] if falta else textos["intro_confirmar_solo"])
        lineas += [
            textos["linea_confirmar"].format(
                etiqueta=textos["etiquetas"][campo],
                valor=_legible(campo, peticion[campo]["valor"], textos))
            for campo in ficha["a_confirmar"]
        ]
        lineas.append("")

    fecha = peticion["fecha"]["valor"]
    if fecha:
        fecha = _fecha_legible(fecha, textos)
        # Los huecos reales los pone la fase 4. Hasta entonces el borrador deja
        # el sitio marcado para que lo complete a mano quien revisa, en vez de
        # mandar un correo que pregunta sin ofrecer nada.
        lineas += [
            textos["disponibilidad"].format(fecha=fecha),
            textos["disponibilidad_pendiente"].format(fecha=fecha),
            "",
        ]

    lineas += [textos["despedida"], textos["firma"]]

    return {
        "asunto": textos["asunto"].format(asunto=asunto_original),
        "cuerpo": "\n".join(lineas),
    }


def _legible(campo: str, valor, textos: dict):
    return _fecha_legible(valor, textos) if campo == "fecha" else valor


def _fecha_legible(fecha: str, textos: dict) -> str:
    """Convierte 2026-09-12 en «12 de septiembre».

    Un correo a un cliente no lleva fechas escritas como las escribe una
    máquina. Los nombres de los meses y el orden están en casa.yaml, porque
    cambian con el idioma.
    """
    anio, mes, dia = fecha.split("-")
    return textos["formato_fecha"].format(dia=int(dia), mes=textos["meses"][int(mes) - 1])


def _opciones_de_duracion(config: dict, textos: dict) -> list[str]:
    """Las duraciones del catálogo, con precio si lo tiene y sin precio si no.

    Mientras Egi no cargue los precios en tratamientos.yaml salen sin cifra.
    No se inventa ninguna.
    """
    opciones = []
    for duracion in casa.duraciones(config):
        precio = duracion.get("precio_eur")
        plantilla = textos["opcion_duracion" + ("_precio" if precio is not None else "")]
        opciones.append(plantilla.format(minutos=duracion["minutos"], precio=precio))
    return opciones
