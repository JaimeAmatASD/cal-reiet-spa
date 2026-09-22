"""El probador compara lo que leyó la IA con lo que habría sacado una persona.

Acá no se llama a la IA: se le da una lectura armada a mano y se mira que el
probador diga bien qué acertó y qué no.
"""
import pytest

import casa
import probador

CASO = {
    "hilo": {
        "id": "real-00",
        "asunto": "Reserva masaje",
        "mensajes": [{"de": "n.ferrer@ejemplo.com", "nombre": "Nuria Ferrer",
                      "texto": "Masaje de 60 el jueves 17 por la tarde, una persona. Hab. 9."}],
    },
    "espera": {"salida": "completo", "idioma": "es", "habitacion": "9", "duracion": 60,
               "fecha": "2026-09-17", "franja": "tarde", "personas": 1},
}


def _lectura(**cambios):
    peticion = {
        "duracion": {"valor": 60, "origen": "dicho"},
        "fecha": {"valor": "2026-09-17", "origen": "dicho"},
        "franja": {"valor": "tarde", "origen": "dicho"},
        "personas": {"valor": 1, "origen": "dicho"},
    }
    peticion.update(cambios)
    return {
        "idioma": "es", "intencion": "reserva", "senales_salud": False,
        "pide_recomendacion": False,
        "cliente": {"nombre": {"valor": "Nuria Ferrer", "origen": "dicho"},
                    "habitacion": {"valor": 9, "origen": "dicho"}},
        "peticion": peticion,
    }


@pytest.fixture(scope="module")
def config():
    return casa.cargar()


def test_una_lectura_igual_a_la_de_una_persona_no_tiene_fallos(config):
    assert probador.comparar(CASO, _lectura(), config) == []


def test_dice_que_campo_fallo_y_que_leyo_en_su_lugar(config):
    fallos = probador.comparar(CASO, _lectura(duracion={"valor": 90, "origen": "dicho"}), config)
    assert fallos == [{"campo": "duracion", "esperado": 60, "leido": 90}]


def test_un_dato_deducido_cuenta_como_fallo_de_la_salida(config):
    # La fecha está bien, pero si la IA la marca como deducida la ficha sale
    # incompleta y se le vuelve a preguntar al cliente algo que ya dijo.
    lectura = _lectura(fecha={"valor": "2026-09-17", "origen": "deducido"})
    fallos = probador.comparar(CASO, lectura, config)
    assert fallos == [{"campo": "salida", "esperado": "completo", "leido": "incompleto"}]


def test_una_consulta_de_salud_derivada_no_se_compara_campo_por_campo(config):
    caso = {"hilo": CASO["hilo"], "espera": {"salida": "derivar"}}
    lectura = _lectura() | {"senales_salud": True}
    assert probador.comparar(caso, lectura, config) == []
