"""Las reglas que no se ven en un caso de correo suelto."""
import copy

import pytest

import casa
import ficha

HILO = {
    "id": "hilo-x",
    "asunto": "Masaje",
    "mensajes": [{"de": "a.molins@ejemplo.com", "nombre": "Ada Molins",
                  "texto": "Hola, quería un masaje."}],
}

LECTURA = {
    "idioma": "es",
    "intencion": "reserva",
    "senales_salud": False,
    "pide_recomendacion": False,
    "cliente": {
        "nombre": {"valor": "Ada Molins", "origen": "dicho"},
        "correo": {"valor": "a.molins@ejemplo.com", "origen": "dicho"},
        "habitacion": {"valor": None, "origen": "dicho"},
    },
    "peticion": {
        "duracion": {"valor": 60, "origen": "dicho"},
        "fecha": {"valor": "2026-09-12", "origen": "dicho"},
        "franja": {"valor": "tarde", "origen": "dicho"},
        "personas": {"valor": 2, "origen": "dicho"},
    },
}


@pytest.fixture(scope="module")
def config():
    return casa.cargar()


def lectura_con(**cambios):
    lectura = copy.deepcopy(LECTURA)
    for campo, valor in cambios.items():
        lectura[campo] = valor
    return lectura


def test_si_la_ia_ve_salud_se_deriva_aunque_no_haya_ninguna_palabra_de_la_lista(config):
    resultado = ficha.armar(HILO, lectura_con(senales_salud=True), config)

    assert resultado["salida"] == "derivar"
    assert resultado["motivo"] == "salud"


def test_una_duracion_que_no_esta_en_el_catalogo_no_se_da_por_buena(config):
    lectura = lectura_con()
    lectura["peticion"]["duracion"]["valor"] = 75

    resultado = ficha.armar(HILO, lectura, config)

    assert resultado["salida"] == "incompleto"
    assert resultado["falta"] == ["duracion"]


def test_una_franja_que_no_es_de_la_casa_no_se_da_por_buena(config):
    lectura = lectura_con()
    lectura["peticion"]["franja"]["valor"] = "noche"

    resultado = ficha.armar(HILO, lectura, config)

    assert resultado["falta"] == ["franja"]


def test_un_campo_sin_origen_es_un_error_no_un_campo_vacio(config):
    lectura = lectura_con()
    del lectura["peticion"]["fecha"]["origen"]

    with pytest.raises(ficha.LecturaInvalida, match="origen"):
        ficha.armar(HILO, lectura, config)


def test_un_idioma_que_la_casa_no_habla_deja_la_ficha_sin_borrador(config):
    resultado = ficha.armar(HILO, lectura_con(idioma="de"), config)

    assert resultado["salida"] == "completo"
    assert resultado["borrador"] is None
