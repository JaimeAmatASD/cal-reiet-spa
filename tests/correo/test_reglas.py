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


def test_si_no_sabemos_el_nombre_se_le_pregunta_en_vez_de_no_contestar(config):
    # El cliente que no firma también recibe respuesta: se le saluda sin nombre
    # y el nombre va con el resto de lo que falta.
    sin_nombre = copy.deepcopy(LECTURA["cliente"])
    del sin_nombre["nombre"]
    textos = config["textos"]["borrador"]["es"]

    resultado = ficha.armar(HILO, lectura_con(cliente=sin_nombre), config)

    cuerpo = resultado["borrador"]["cuerpo"]
    assert cuerpo.startswith(textos["saludo_sin_nombre"])
    assert textos["intro"] in cuerpo
    assert textos["pregunta_nombre"] in cuerpo


def test_un_idioma_que_la_casa_no_habla_deja_la_ficha_sin_borrador(config):
    resultado = ficha.armar(HILO, lectura_con(idioma="de"), config)

    assert resultado["salida"] == "completo"
    assert resultado["borrador"] is None


# --- NUEVO:{nombre} en el asunto -------------------------------------------
# Atajo del laboratorio: desde un mismo buzón se simulan clientes distintos
# poniendo en el asunto quién escribe, sin tener que cambiar de correo. Hace de
# correo del cliente, no de nombre: el nombre se le sigue preguntando.

def sin_nombre_leido():
    cliente = copy.deepcopy(LECTURA["cliente"])
    del cliente["nombre"]
    return lectura_con(cliente=cliente)


@pytest.mark.parametrize("asunto", ["NUEVO:Juan23", "NUEVO: Juan23", "Re: NUEVO:Juan23"])
def test_nuevo_en_el_asunto_hace_de_correo_del_cliente(config, asunto):
    hilo = {**HILO, "asunto": asunto}

    resultado = ficha.armar(hilo, lectura_con(), config)

    assert resultado["cliente"]["correo"] == {"valor": "juan23@ejemplo.com", "origen": "dicho"}


def test_nuevo_en_el_asunto_no_da_el_nombre_y_se_sigue_preguntando(config):
    hilo = {**HILO, "asunto": "NUEVO:Juan23"}

    resultado = ficha.armar(hilo, sin_nombre_leido(), config)

    assert resultado["cliente"]["nombre"]["valor"] is None
    textos = config["textos"]["borrador"]["es"]
    assert textos["pregunta_nombre"] in resultado["borrador"]["cuerpo"]


@pytest.mark.parametrize("asunto", ["Masaje", "NUEVO:", "Quiero algo NUEVO:Juan23"])
def test_sin_nuevo_al_principio_del_asunto_el_correo_no_cambia(config, asunto):
    hilo = {**HILO, "asunto": asunto}

    resultado = ficha.armar(hilo, lectura_con(), config)

    assert resultado["cliente"]["correo"]["valor"] == "a.molins@ejemplo.com"
