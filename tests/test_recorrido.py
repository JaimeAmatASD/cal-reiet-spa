"""El recorrido entero: entra un pedido y sale una petición.

Estas pruebas no miran una pieza sino el camino completo. Si una falla, algo
del circuito se desconectó aunque las piezas sueltas sigan verdes.

Los nombres y los correos son inventados. La agenda del 8 de septiembre es la
real: un día lleno.
"""
import copy

import pytest

import casa
import flujo
import peticion

DIA_LLENO = [
    {"sala": "sala_1", "desde": "11:00", "hasta": "12:30"},
    {"sala": "sala_1", "desde": "12:45", "hasta": "14:15"},
    {"sala": "sala_1", "desde": "14:30", "hasta": "15:30"},
    {"sala": "sala_1", "desde": "16:00", "hasta": "17:30"},
    {"sala": "sala_2", "desde": "11:00", "hasta": "12:30"},
    {"sala": "sala_2", "desde": "12:45", "hasta": "13:45"},
    {"sala": "sala_2", "desde": "14:30", "hasta": "15:30"},
    {"sala": "sala_2", "desde": "16:00", "hasta": "17:30"},
]

PEDIDO = {
    "origen": "buzon",
    "hilo": {
        "id": "hilo-201",
        "asunto": "Massage booking",
        "mensajes": [{
            "de": "i.sorbo@ejemplo.com",
            "nombre": "Ingrid Sorbo",
            "texto": "Hello, I would like to book a 90 minute massage on "
                     "9 September, in the morning. Just for me. Thank you.",
        }],
    },
    "lectura": {
        "idioma": "en",
        "intencion": "reserva",
        "senales_salud": False,
        "pide_recomendacion": False,
        "cliente": {
            "nombre": {"valor": "Ingrid Sorbo", "origen": "dicho"},
            "correo": {"valor": "i.sorbo@ejemplo.com", "origen": "dicho"},
            "habitacion": {"valor": None, "origen": "dicho"},
        },
        "peticion": {
            "duracion": {"valor": 90, "origen": "dicho"},
            "fecha": {"valor": "2026-09-09", "origen": "dicho"},
            "franja": {"valor": "mañana", "origen": "dicho"},
            "personas": {"valor": 1, "origen": "dicho"},
            "preferencia_terapeuta": {"valor": None, "origen": "dicho"},
        },
    },
}


@pytest.fixture(scope="module")
def config():
    return casa.cargar()


def pedido_con(**cambios):
    pedido = copy.deepcopy(PEDIDO)
    for campo, valor in cambios.items():
        pedido["lectura"]["peticion"][campo] = valor
    return pedido


def test_una_consulta_con_salud_se_deriva_sin_mirar_la_agenda(config):
    pedido = copy.deepcopy(PEDIDO)
    pedido["lectura"]["senales_salud"] = True

    resultado = flujo.procesar(pedido, config, agenda_del_dia=DIA_LLENO)

    assert resultado["accion"] == "derivar"
    assert resultado["huecos"] is None


def test_un_pedido_incompleto_sale_como_borrador_sin_mirar_la_agenda(config):
    incompleto = pedido_con(duracion={"valor": None, "origen": "dicho"})

    resultado = flujo.procesar(incompleto, config, agenda_del_dia=DIA_LLENO)

    assert resultado["accion"] == "borrador"
    assert resultado["huecos"] is None
    assert "How long" in resultado["borrador"]["cuerpo"]


def test_un_pedido_completo_sin_agenda_pide_la_agenda_de_ese_dia(config):
    resultado = flujo.procesar(PEDIDO, config)

    assert resultado["accion"] == "falta_agenda"
    assert resultado["fecha"] == "2026-09-09"


def test_un_pedido_completo_con_la_agenda_devuelve_las_horas_libres(config):
    # Ese día ya está puesta una reserva de 10:00 a 11:30 en la sala 1. La
    # sala 2 sigue libre toda la mañana, y la 1 vuelve a estarlo a las 11:45,
    # cuando terminan los quince minutos de margen.
    ocupado = [{"sala": "sala_1", "desde": "10:00", "hasta": "11:30"}]

    resultado = flujo.procesar(PEDIDO, config, agenda_del_dia=ocupado)

    assert resultado["accion"] == "elegir_hora"
    assert resultado["huecos"] == [
        {"desde": "10:00", "hasta": "14:00", "salas": ["sala_2"]},
        {"desde": "11:45", "hasta": "14:00", "salas": ["sala_1"]},
    ]


def test_un_dia_lleno_dice_que_no_entra_y_ofrece_lo_que_si(config):
    tarde = pedido_con(franja={"valor": "tarde", "origen": "dicho"})

    resultado = flujo.procesar(tarde, config, agenda_del_dia=DIA_LLENO)

    assert resultado["accion"] == "sin_hueco"
    assert resultado["huecos"] == []
    # Un 90 no entra, pero un 60 sí, al final del día.
    assert [a["minutos"] for a in resultado["alternativas"]] == [40, 60]
    assert resultado["alternativas"][1]["huecos"][0]["desde"] == "17:45"


def test_el_recorrido_entero_termina_en_una_peticion(config):
    """De un correo a un bloque listo para pegar en el grupo."""
    ocupado = [{"sala": "sala_1", "desde": "10:00", "hasta": "11:30"}]

    resultado = flujo.procesar(PEDIDO, config, agenda_del_dia=ocupado)
    hueco = resultado["huecos"][0]

    # Elegir la hora dentro del hueco es de una persona: el sistema no elige.
    peticiones = peticion.armar(resultado["ficha"], "12:15", hueco["salas"], config)

    assert peticiones[0]["texto"] == "\n".join([
        "PETICIÓN A Espera de pago",
        "Massage 90`",
        "Ingrid Sorbo (Ext)",
        "Wednesday, 9 September⋅12:15 – 13:45",
    ])
    assert peticiones[0]["sala"] == "sala_2"
