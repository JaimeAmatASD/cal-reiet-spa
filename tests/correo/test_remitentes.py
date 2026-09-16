"""Lo que no es un pedido no pasa por la IA.

Al buzón llegan avisos automáticos —de Google, por ejemplo— que gastan saldo al
leerlos y meterían filas en la hoja que no son pedidos. Se dejan afuera por el
remitente, antes de leer. La lista vive en la configuración de la casa.
"""
import pytest

import casa
import flujo


@pytest.fixture(scope="module")
def config():
    return casa.cargar()


def hilo(*remitentes):
    return {"id": "hilo-1", "asunto": "x",
            "mensajes": [{"de": r, "nombre": "", "texto": "x"} for r in remitentes]}


def test_un_aviso_de_google_no_se_lee(config):
    assert not flujo.hay_que_leer(hilo("no-reply@accounts.google.com"), config)


def test_el_dominio_exacto_de_la_lista_tampoco_se_lee(config):
    assert not flujo.hay_que_leer(hilo("CloudPlatform-noreply@google.com"), config)


def test_un_cliente_con_gmail_se_lee(config):
    # gmail.com no es google.com: de ahí escriben muchos clientes.
    assert flujo.hay_que_leer(hilo("marta.vidal@gmail.com"), config)


def test_un_dominio_que_solo_termina_parecido_se_lee(config):
    assert flujo.hay_que_leer(hilo("reservas@notgoogle.com"), config)


def test_si_un_cliente_escribe_en_la_conversacion_se_lee(config):
    assert flujo.hay_que_leer(
        hilo("no-reply@accounts.google.com", "marta.vidal@gmail.com"), config)


def test_una_casa_sin_lista_lo_lee_todo(config):
    sin_lista = {k: v for k, v in config.items() if k != "remitentes_automaticos"}

    assert flujo.hay_que_leer(hilo("no-reply@accounts.google.com"), sin_lista)
