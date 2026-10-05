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


def test_si_lo_ultimo_lo_escribio_el_spa_no_se_vuelve_a_leer(config):
    # Cuando el spa contesta, su respuesta entra en la misma conversación y el
    # buzón la ve como correo nuevo. Leerla otra vez volvería a contestar al
    # cliente, y así sin fin. Se lee cuando el que escribe es el cliente.
    conversacion = {"id": "h", "asunto": "Masaje", "mensajes": [
        {"de": "cliente@gmail.com", "texto": "Quiero un masaje"},
        {"de": "spa@gmail.com", "texto": "¿De cuántos minutos?", "propio": True}]}
    assert not flujo.hay_que_leer(conversacion, config)

    conversacion["mensajes"].append({"de": "cliente@gmail.com", "texto": "60"})
    assert flujo.hay_que_leer(conversacion, config)
