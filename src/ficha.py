"""La ficha: lo que sale de leer un correo, y el contrato con el resto del sistema.

Entra un hilo de correo y la lectura de la IA, y sale un diccionario que se
guarda como JSON. Esta pieza no busca huecos, no toca el calendario y no manda
nada: solo entiende el pedido y deja constancia.

Tres salidas posibles:
  - completo    los cuatro datos están y los dijo el cliente
  - incompleto  falta alguno, o alguno lo dedujimos y hay que confirmarlo
  - derivar     hay datos de salud, o pide que le recomendemos

Un campo deducido NO cuenta como resuelto. La ficha sale incompleta y el
borrador se lo pregunta, porque agendar sobre una suposición es peor que
preguntar una vez más.

Si el motivo es salud, la ficha sale vacía: número de hilo y nada más. El texto
del correo no se copia a ningún lado. Son datos de categoría especial y el sitio
donde tienen que quedarse es el buzón, no nuestros registros.
"""
from datetime import datetime

import borrador
import clasificador
from extraccion import CAMPOS_PETICION, LecturaInvalida, extraer

__all__ = ["armar", "LecturaInvalida"]


def armar(hilo: dict, lectura: dict, config: dict, ahora: datetime | None = None) -> dict:
    """Devuelve la ficha del hilo."""
    leido_en = (ahora or datetime.now()).isoformat(timespec="seconds")
    intencion, motivo = clasificador.clasificar(hilo, lectura, config)

    if motivo == "salud":
        return {
            "salida": "derivar",
            "motivo": "salud",
            "hilo_id": hilo["id"],
            "leido_en": leido_en,
            "nota": config["textos"]["aviso_salud"],
        }

    cliente, peticion = extraer(lectura, config)
    falta = [c for c in CAMPOS_PETICION if peticion[c]["valor"] is None]
    a_confirmar = [c for c in CAMPOS_PETICION
                   if peticion[c]["valor"] is not None and peticion[c]["origen"] == "deducido"]

    ficha = {
        "salida": _salida(intencion, falta, a_confirmar),
        "motivo": motivo,
        "intencion": intencion,
        "hilo_id": hilo["id"],
        "leido_en": leido_en,
        "idioma": lectura.get("idioma"),
        "cliente": cliente,
        "peticion": peticion,
        "falta": falta,
        "a_confirmar": a_confirmar,
        "borrador": None,
    }

    # Solo se redacta para un pedido de reserva. Una pregunta suelta o algo que
    # va a una persona lo contesta esa persona, que sabe qué le preguntaron.
    if intencion == "reserva":
        ficha["borrador"] = borrador.redactar(ficha, config, hilo["asunto"])

    return ficha


def _salida(intencion: str, falta: list, a_confirmar: list) -> str:
    if intencion == "derivar":
        return "derivar"
    if falta or a_confirmar:
        return "incompleto"
    return "completo"
