"""El bloque que sale al grupo de terapeutas. NO lo manda: lo escribe.

Es el mensaje interno que hoy Egi escribe a mano. El formato está copiado de
los mensajes reales del grupo y se respeta letra por letra —el mismo bloque se
repite tres veces, en la petición, en el «puedo» del terapeuta y en la
confirmación, y eso es lo que permite seguir un pedido dentro de un hilo de
cien mensajes. Todo el detalle está en docs/convenciones.md.

Los textos están en casa.yaml. Acá solo se decide qué líneas entran.

Dos reglas del dominio que esta pieza sostiene:

  - **Una petición por persona.** Un masaje para dos son dos peticiones con el
    bloque idéntico, no una que diga «para dos». Cada una se lleva su sala y
    su terapeuta, y las dos van a la misma hora.
  - **Una preferencia deducida no sale.** Si el cliente no la escribió, no se
    pone. Poner «Terapeuta Mujer» porque lo supusimos es peor que no ponerlo.
"""
from datetime import date

import casa

__all__ = ["armar", "NoSePuedeArmar"]


class NoSePuedeArmar(Exception):
    """Falta algo para poder escribir la petición. El mensaje dice qué."""


def armar(ficha: dict, inicio: str, salas: list, config: dict) -> list[dict]:
    """Las peticiones de un pedido: una por persona, todas con el mismo texto.

    `inicio` es la hora que eligió una persona entre los huecos libres, y
    `salas` las salas de ese hueco.
    """
    pedido = ficha["peticion"]
    personas = pedido["personas"]["valor"]
    if len(salas) < personas:
        raise NoSePuedeArmar(
            f"el pedido es para {personas} personas y hacen falta {personas} "
            f"salas libres a la misma hora. Llegaron {len(salas)}.")

    textos = config["textos"]["peticion"]
    minutos = pedido["duracion"]["valor"]
    lineas = [textos["encabezado"]]

    preferencia = pedido["preferencia_terapeuta"]
    if preferencia["valor"] and preferencia["origen"] == "dicho":
        lineas.append(textos["preferencia"][preferencia["valor"]])

    lineas += [
        textos["tratamiento"].format(
            tratamiento=casa.tratamiento(config)["nombre"][textos["idioma"]],
            minutos=minutos),
        _cliente(ficha["cliente"], textos),
        _cuando(pedido["fecha"]["valor"], inicio, minutos, textos),
    ]

    texto = "\n".join(lineas)
    return [{"sala": sala, "texto": texto} for sala in salas[:personas]]


def _cliente(cliente: dict, textos: dict) -> str:
    """El nombre, con la habitación si está alojado y con (Ext) si no.

    Lo único que sabemos hoy es si trajo habitación. Un externo con habitación
    asignada —que existe, está visto— sale como alojado. Ver convenciones.
    """
    habitacion = cliente["habitacion"]["valor"]
    plantilla = "cliente_alojado" if habitacion else "cliente_externo"
    return textos[plantilla].format(
        nombre=cliente["nombre"]["valor"], habitacion=habitacion)


def _cuando(fecha: str, inicio: str, minutos: int, textos: dict) -> str:
    dia = date.fromisoformat(fecha)
    return textos["fecha"].format(
        dia_semana=textos["dias_semana"][dia.weekday()],
        dia=dia.day,
        mes=textos["meses"][dia.month - 1],
        desde=inicio,
        hasta=_fin(inicio, minutos))


def _fin(inicio: str, minutos: int) -> str:
    horas, resto = (int(parte) for parte in inicio.split(":"))
    total = horas * 60 + resto + minutos
    return f"{total // 60:02d}:{total % 60:02d}"
