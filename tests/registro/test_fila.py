"""La fila que se escribe en la hoja de registro.

Una fila por pedido. Es el instrumento de medición de la fase 1: con esto se
cuenta cuántos pedidos entran, cuántos se caen y cuánto se tarda en contestar.

Dos cosas que no se pueden romper y por eso están probadas:
  - el orden y el nombre de las columnas, porque la hoja los tiene fijos
  - una consulta derivada por salud no deja ni un dato del cliente en la hoja
"""
import copy

import pytest

import casa
import flujo
import registro

PEDIDO = {
    "origen": "buzon",
    "entrado_en": "2026-09-08T09:12:00",
    "hilo": {
        "id": "hilo-301",
        "asunto": "Masaje",
        "mensajes": [{
            "de": "marta.vidal@ejemplo.com",
            "nombre": "Marta Vidal",
            "texto": "Estamos en la habitación 9 y queremos un masaje de 60 "
                     "minutos para dos el 12 de septiembre por la tarde.",
        }],
    },
    "lectura": {
        "idioma": "es",
        "intencion": "reserva",
        "senales_salud": False,
        "pide_recomendacion": False,
        "cliente": {
            "nombre": {"valor": "Marta Vidal", "origen": "dicho"},
            "correo": {"valor": "marta.vidal@ejemplo.com", "origen": "dicho"},
            "habitacion": {"valor": "9", "origen": "dicho"},
        },
        "peticion": {
            "duracion": {"valor": 60, "origen": "dicho"},
            "fecha": {"valor": "2026-09-12", "origen": "dicho"},
            "franja": {"valor": "tarde", "origen": "dicho"},
            "personas": {"valor": 2, "origen": "dicho"},
            "preferencia_terapeuta": {"valor": "mujer", "origen": "dicho"},
        },
    },
}


@pytest.fixture(scope="module")
def config():
    return casa.cargar()


def fila_de(pedido, config, agenda=None):
    return registro.fila(pedido, flujo.procesar(pedido, config, agenda_del_dia=agenda))


def test_la_fila_trae_todas_las_columnas_y_en_orden(config):
    fila = fila_de(PEDIDO, config)

    assert list(fila) == list(registro.COLUMNAS)


def test_un_pedido_completo_deja_escrito_lo_que_pidio_el_cliente(config):
    fila = fila_de(PEDIDO, config)

    assert fila["pedido"] == "hilo-301"
    assert fila["entrado_en"] == "2026-09-08T09:12:00"
    assert fila["canal"] == "buzon"
    assert fila["idioma"] == "es"
    assert fila["cliente"] == "Marta Vidal"
    assert fila["habitacion"] == "9"
    assert fila["duracion"] == 60
    assert fila["fecha"] == "2026-09-12"
    assert fila["franja"] == "tarde"
    assert fila["personas"] == 2
    assert fila["preferencia"] == "mujer"
    assert fila["lectura"] == "completo"
    assert fila["falta"] == ""
    assert fila["a_confirmar"] == ""
    assert fila["accion"] == "falta_agenda"
    assert fila["estado"] == "SOLICITADA"


def test_la_hoja_no_guarda_el_correo_del_cliente(config):
    fila = fila_de(PEDIDO, config)

    assert "marta.vidal@ejemplo.com" not in " ".join(str(v) for v in fila.values())


def test_lo_que_llena_una_persona_sale_vacio(config):
    fila = fila_de(PEDIDO, config)

    assert fila["respondido_en"] == ""
    assert fila["desenlace"] == ""
    assert fila["nota"] == ""


def test_lo_que_falta_y_lo_que_hay_que_confirmar_van_separados(config):
    pedido = copy.deepcopy(PEDIDO)
    pedido["lectura"]["peticion"]["duracion"] = {"valor": None, "origen": "dicho"}
    pedido["lectura"]["peticion"]["fecha"] = {"valor": "2026-09-12",
                                              "origen": "deducido"}

    fila = fila_de(pedido, config)

    assert fila["lectura"] == "incompleto"
    assert fila["falta"] == "duracion"
    assert fila["a_confirmar"] == "fecha"
    assert fila["accion"] == "borrador"


def test_una_consulta_con_salud_no_deja_ni_un_dato_del_cliente(config):
    pedido = copy.deepcopy(PEDIDO)
    pedido["lectura"]["senales_salud"] = True

    fila = fila_de(pedido, config)

    assert fila["pedido"] == "hilo-301"
    assert fila["canal"] == "buzon"
    assert fila["accion"] == "derivar"
    assert fila["motivo"] == "salud"
    # Ni el nombre, ni la habitación, ni qué pidió, ni el idioma en que escribe.
    for columna in ("cliente", "habitacion", "duracion", "fecha", "franja",
                    "personas", "preferencia", "idioma", "lectura", "estado"):
        assert fila[columna] == "", f"la columna '{columna}' no puede llevar nada"


def test_una_pregunta_suelta_no_arranca_como_reserva_solicitada(config):
    pedido = copy.deepcopy(PEDIDO)
    pedido["lectura"]["intencion"] = "pregunta"

    fila = fila_de(pedido, config)

    assert fila["estado"] == ""
