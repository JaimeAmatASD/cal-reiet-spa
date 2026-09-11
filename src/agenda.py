"""Qué horas quedan libres en las salas de un día.

Recibe lo que ya está ocupado y devuelve los ratos en los que cabe un
tratamiento. No sabe de Google Calendar ni de nada que se conecte: la agenda
entra como un dato y se va como otro. Quien la lea del calendario es n8n.

Dos cosas que hace y una que NO hace.

Hace: dejar los quince minutos libres a cada lado de cada reserva —el margen de
la casa, que sale de la configuración— y buscar tantas salas libres a la vez
como personas tenga el pedido. Un masaje para dos son dos salas a la misma
hora, no dos horas seguidas.

NO hace: decidir cuál de los huecos conviene. Ese criterio —pegar el
tratamiento a una reserva existente antes que abrir una cita suelta— es de Egi
y es lo que cierra la fase 4. Acá salen todos los que caben y elige una persona.

Las horas entran y salen como texto, "10:00". Por dentro son minutos desde la
medianoche, porque restar horas escritas es una fuente de errores y contar
minutos no.
"""
from itertools import combinations

__all__ = ["huecos"]


def huecos(ocupado: list, minutos: int, config: dict,
           franja: str | None = None, personas: int = 1) -> list[dict]:
    """Los ratos libres donde entra un tratamiento de `minutos`.

    `ocupado` son las reservas del día: sala, hora de inicio y hora de fin.
    `franja` recorta el día a la mañana o a la tarde, si el cliente la pidió.

    Cada hueco dice de cuándo a cuándo está libre y en qué salas. El
    tratamiento puede empezar en cualquier momento del hueco que le deje
    terminar dentro: un hueco de 12:45 a 19:00 admite un 90 hasta las 17:30.
    """
    abre, cierra = _ventana(config, franja)
    margen = config["margen_minutos"]
    salas = [sala["id"] for sala in config["salas"]]
    libre = {sala: _libre(_bloqueado(ocupado, sala, margen), abre, cierra)
             for sala in salas}

    encontrados = [
        {"desde": _hhmm(desde), "hasta": _hhmm(hasta), "salas": list(grupo)}
        for grupo in combinations(salas, personas)
        for desde, hasta in _comun([libre[sala] for sala in grupo])
        if hasta - desde >= minutos
    ]
    return sorted(encontrados, key=lambda hueco: (hueco["desde"], hueco["salas"]))


def _ventana(config: dict, franja: str | None) -> tuple[int, int]:
    """De cuándo a cuándo se puede buscar. Una franja nunca pasa del horario."""
    abre = _min(config["horario"]["abre"])
    cierra = _min(config["horario"]["cierra"])
    if franja is None:
        return abre, cierra
    rango = config["franjas"][franja]
    return max(abre, _min(rango["desde"])), min(cierra, _min(rango["hasta"]))


def _bloqueado(ocupado: list, sala: str, margen: int) -> list[tuple[int, int]]:
    """Las reservas de una sala, estiradas el margen a cada lado y unidas.

    Se unen porque dos reservas separadas por el margen justo no dejan hueco
    entre ellas: esos quince minutos son el margen de las dos a la vez.
    """
    tramos = sorted((_min(r["desde"]) - margen, _min(r["hasta"]) + margen)
                    for r in ocupado if r["sala"] == sala)
    unidos: list[tuple[int, int]] = []
    for desde, hasta in tramos:
        if unidos and desde <= unidos[-1][1]:
            unidos[-1] = (unidos[-1][0], max(unidos[-1][1], hasta))
        else:
            unidos.append((desde, hasta))
    return unidos


def _libre(bloqueado: list, abre: int, cierra: int) -> list[tuple[int, int]]:
    """Lo que queda del día una vez quitado lo bloqueado."""
    libres = []
    borde = abre
    for desde, hasta in bloqueado:
        if desde > borde:
            libres.append((borde, min(desde, cierra)))
        borde = max(borde, hasta)
        if borde >= cierra:
            break
    if borde < cierra:
        libres.append((borde, cierra))
    return [(desde, hasta) for desde, hasta in libres if hasta > desde]


def _comun(ratos_por_sala: list) -> list[tuple[int, int]]:
    """Los ratos en que TODAS esas salas están libres a la vez."""
    comun = ratos_por_sala[0]
    for otra in ratos_por_sala[1:]:
        comun = [(max(a, c), min(b, d))
                 for a, b in comun for c, d in otra
                 if max(a, c) < min(b, d)]
    return sorted(comun)


def _min(hora: str) -> int:
    horas, minutos = hora.split(":")
    return int(horas) * 60 + int(minutos)


def _hhmm(minutos: int) -> str:
    return f"{minutos // 60:02d}:{minutos % 60:02d}"
