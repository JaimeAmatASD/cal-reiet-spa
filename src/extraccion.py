"""Saca los campos del hilo y los contrasta contra la configuración de la casa.

Lo que la IA leyó entra acá y sale limpio. Un valor que no existe en la casa
—una duración que no está en el catálogo, una franja que no se ofrece— no se
da por bueno: se descarta y el campo pasa a la lista de lo que falta, para
volver a preguntárselo al cliente.

Cada campo lleva de dónde salió: 'dicho', 'deducido' o 'historial'. No es
opcional. Si un campo llega sin origen es un error de la lectura, no un campo
vacío, y hay que verlo.
"""
import casa

CAMPOS_PETICION = ("duracion", "fecha", "franja", "personas")
# La preferencia de terapeuta se guarda si el cliente la dice, pero no
# frena la ficha: la mayoría no tiene preferencia y no vale una vuelta de
# correo de más para todos. Ver docs/decisions.md.
CAMPOS_OPCIONALES = ("preferencia_terapeuta",)
CAMPOS_CLIENTE = ("nombre", "correo", "habitacion")
ORIGENES = ("dicho", "deducido", "historial")


class LecturaInvalida(Exception):
    """Lo que devolvió la IA no tiene la forma acordada."""


def extraer(lectura: dict, config: dict) -> tuple[dict, dict]:
    """Devuelve los datos del cliente y los de la petición, con su origen."""
    cliente = {campo: _campo(lectura, "cliente", campo) for campo in CAMPOS_CLIENTE}
    peticion = {campo: _campo(lectura, "peticion", campo)
                for campo in CAMPOS_PETICION + CAMPOS_OPCIONALES}

    minutos_validos = [d["minutos"] for d in casa.duraciones(config)]
    _descartar_si(peticion["duracion"], lambda v: v not in minutos_validos)
    _descartar_si(peticion["franja"], lambda v: v not in config["franjas"])
    _descartar_si(peticion["personas"], lambda v: not isinstance(v, int) or v < 1)
    _descartar_si(peticion["fecha"], lambda v: not isinstance(v, str))
    _descartar_si(peticion["preferencia_terapeuta"],
                  lambda v: v not in casa.preferencias(config))

    return cliente, peticion


def _campo(lectura: dict, bloque: str, campo: str) -> dict:
    leido = lectura.get(bloque, {}).get(campo)
    if leido is None:
        return {"valor": None, "origen": None}

    origen = leido.get("origen")
    if origen not in ORIGENES:
        raise LecturaInvalida(
            f"el campo '{campo}' vino con origen {origen!r}. Tiene que ser uno de "
            f"{', '.join(ORIGENES)}: sin eso no se sabe si el dato lo dijo el "
            f"cliente o lo dedujimos nosotros.")

    return {"valor": leido.get("valor"), "origen": origen}


def _descartar_si(campo: dict, no_sirve) -> None:
    if campo["valor"] is not None and no_sirve(campo["valor"]):
        campo["valor"] = None
