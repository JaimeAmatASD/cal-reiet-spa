"""La fila que se escribe en la hoja de registro. Una fila por pedido.

Es el instrumento de medición de la fase 1: el sistema lee el buzón y anota,
sin tocar la operación. De acá salen los números con los que se decide si el
proyecto sigue —cuántos pedidos entran, cuántos se caen, cuánto se tarda en
contestar—, así que las columnas no se cambian a la ligera: la hoja las tiene
fijas y el reporte semanal las lee por nombre.

Hay dos clases de columnas. Las que llena el sistema, con lo que entendió del
correo, y las cuatro últimas, que las llena una persona a mano mientras la
reserva avanza. El sistema las deja vacías y no las vuelve a tocar.

Lo que NO se escribe acá, a propósito:
  - el correo y el teléfono del cliente. Para contestarle está el buzón; para
    contar pedidos no hacen falta, y una hoja que se comparte es un sitio peor
    para guardarlos que el buzón del que salieron.
  - nada de una consulta derivada por salud. Esa fila lleva el número de hilo,
    cuándo entró y que se derivó. Ni el nombre. Ver docs/contrato-lectura.md.
"""
__all__ = ["COLUMNAS", "fila"]

COLUMNAS = (
    # --- lo que escribe el sistema ---
    "pedido",          # número del hilo de correo. Es la llave: no se repite
    "entrado_en",      # cuándo llegó el pedido
    "leido_en",        # cuándo lo leyó el sistema
    "canal",           # por dónde entró: buzón, formulario, telegram
    "idioma",
    "cliente",
    "habitacion",      # vacío si no se aloja
    "duracion",        # minutos
    "fecha",           # el día que pidió
    "franja",          # mañana o tarde
    "personas",
    "preferencia",     # de sexo del terapeuta, si la dijo
    "lectura",         # completo, incompleto o derivar
    "falta",           # qué datos no dio
    "a_confirmar",     # qué datos dedujimos nosotros y hay que confirmarle
    "accion",          # qué hizo el sistema con el pedido
    "motivo",          # por qué se derivó, cuando se derivó
    "estado",          # arranca en SOLICITADA y de ahí lo mueve una persona
    # --- lo que llena una persona ---
    "respondido_en",   # cuándo salió la respuesta al cliente
    "desenlace",       # REALIZADA, CAÍDA, CANCELADA, SIN COBERTURA
    "nota",
)

A_MANO = ("respondido_en", "desenlace", "nota")


def fila(pedido: dict, resultado: dict) -> dict:
    """Devuelve la fila del registro para un pedido ya procesado."""
    ficha = resultado["ficha"]
    base = dict.fromkeys(COLUMNAS, "")
    base |= {
        "pedido": ficha["hilo_id"],
        "entrado_en": pedido.get("entrado_en", ""),
        "leido_en": ficha["leido_en"],
        "canal": pedido.get("origen", ""),
        "accion": resultado["accion"],
        "motivo": ficha.get("motivo") or "",
    }

    # Una consulta con datos de salud llega hasta acá y no más. La ficha ya
    # viene vacía; esto es el segundo cerrojo, para que un cambio de allá no
    # abra una puerta acá sin que nadie lo note.
    if ficha["motivo"] == "salud":
        return base

    pide = ficha["peticion"]
    return base | {
        "idioma": ficha.get("idioma") or "",
        "cliente": _valor(ficha["cliente"]["nombre"]),
        "habitacion": _valor(ficha["cliente"]["habitacion"]),
        "duracion": _valor(pide["duracion"]),
        "fecha": _valor(pide["fecha"]),
        "franja": _valor(pide["franja"]),
        "personas": _valor(pide["personas"]),
        "preferencia": _valor(pide["preferencia_terapeuta"]),
        "lectura": ficha["salida"],
        "falta": ", ".join(ficha["falta"]),
        "a_confirmar": ", ".join(ficha["a_confirmar"]),
        "estado": "SOLICITADA" if ficha["intencion"] == "reserva" else "",
    }


def _valor(campo: dict):
    """Un campo sin valor va como celda vacía, no como la palabra 'None'."""
    return campo["valor"] if campo["valor"] is not None else ""
