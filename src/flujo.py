"""El circuito: entra un pedido y sale lo que hay que hacer con él.

Es la pieza que junta todo. No entiende correos, no busca huecos y no escribe
mensajes: llama a las que sí, y decide qué sigue.

Lo que entra es un **pedido**, no un correo. Hoy la única puerta es el buzón,
pero va a haber otra —el Telegram de la spa manager, que pide tratamientos
sobre la marcha— y de la puerta para adentro el camino es el mismo.

Cinco salidas, y el nombre de cada una dice qué tiene que pasar después:

  derivar        lo mira una persona. Si es por salud, no se guardó nada.
  borrador       falta algún dato: hay una respuesta redactada esperando visto
                 bueno. La agenda no se toca hasta que el pedido esté completo.
  falta_agenda   está todo, pero nadie trajo la agenda de ese día. Hay que ir
                 a buscarla y volver a llamar. Esto es así porque la fecha no
                 se sabe hasta que la IA lee el correo.
  elegir_hora    hay horas libres. Elegir una es de una persona: el sistema no
                 elige. Con esa hora se arma la petición.
  sin_hueco      ese día no entra. Va con lo que sí entraría, porque «no hay»
                 a secas obliga a otra vuelta de correo.
"""
from agenda import huecos as buscar_huecos
from casa import duraciones
from ficha import armar as armar_ficha

__all__ = ["procesar", "hay_que_leer"]


def hay_que_leer(hilo: dict, config: dict) -> bool:
    """Si la conversación pasa por la IA, que cuesta saldo.

    No pasa si todos los que escribieron son remitentes automáticos de la casa:
    avisos que no son pedidos y que meterían filas en la hoja. En cuanto un
    cliente escribe en la conversación, se lee.
    """
    automaticos = config.get("remitentes_automaticos") or []

    def es_automatico(correo: str) -> bool:
        dominio = correo.rpartition("@")[2].lower()
        return any(dominio == d or dominio.endswith("." + d) for d in automaticos)

    return not all(es_automatico(m["de"]) for m in hilo["mensajes"])


def procesar(pedido: dict, config: dict, agenda_del_dia: list | None = None,
             ahora=None) -> dict:
    """Qué hacer con un pedido. Ver las cinco salidas en la cabecera."""
    ficha = armar_ficha(pedido["hilo"], pedido["lectura"], config, ahora)
    resultado = {"accion": None, "ficha": ficha, "borrador": ficha.get("borrador"),
                 "huecos": None}

    if ficha["salida"] == "derivar":
        return resultado | {"accion": "derivar"}

    if ficha["salida"] == "incompleto":
        return resultado | {"accion": "borrador"}

    fecha = ficha["peticion"]["fecha"]["valor"]
    if agenda_del_dia is None:
        return resultado | {"accion": "falta_agenda", "fecha": fecha}

    pide = ficha["peticion"]
    huecos = _buscar(agenda_del_dia, pide["duracion"]["valor"], pide, config)
    if huecos:
        return resultado | {"accion": "elegir_hora", "huecos": huecos}

    return resultado | {"accion": "sin_hueco", "huecos": [],
                        "alternativas": _alternativas(agenda_del_dia, pide, config)}


def _buscar(agenda_del_dia: list, minutos: int, pide: dict, config: dict) -> list:
    return buscar_huecos(agenda_del_dia, minutos, config,
                         franja=pide["franja"]["valor"],
                         personas=pide["personas"]["valor"])


def _alternativas(agenda_del_dia: list, pide: dict, config: dict) -> list:
    """Las otras duraciones del catálogo que sí entran ese día.

    Decirle a un cliente «ese día no hay» y nada más le cuesta otra vuelta de
    correo. Si entra un 60 donde no entraba un 90, se le ofrece.
    """
    pedida = pide["duracion"]["valor"]
    otras = []
    for duracion in duraciones(config):
        minutos = duracion["minutos"]
        if minutos == pedida:
            continue
        huecos = _buscar(agenda_del_dia, minutos, pide, config)
        if huecos:
            otras.append({"minutos": minutos, "huecos": huecos})
    return otras
