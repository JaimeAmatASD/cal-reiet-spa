"""Qué horas quedan libres en las salas de un día.

Los quince minutos a cada lado de cada reserva son regla de la casa y salen de
la configuración, no de acá.

La agenda del 8 de septiembre que se usa en varios casos es la real: un día
lleno, con las dos salas ocupadas casi de punta a punta. Es el caso que importa,
porque es donde un buscador ingenuo dice que hay hueco y no lo hay.
"""
import pytest

import agenda
import casa

# El día lleno, tal como estaba. Solo horas y salas: ni un nombre.
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


@pytest.fixture(scope="module")
def config():
    return casa.cargar()


def test_un_dia_vacio_deja_libre_todo_el_horario(config):
    assert agenda.huecos([], 60, config) == [
        {"desde": "10:00", "hasta": "19:00", "salas": ["sala_1"]},
        {"desde": "10:00", "hasta": "19:00", "salas": ["sala_2"]},
    ]


def test_una_reserva_deja_quince_minutos_libres_a_cada_lado(config):
    ocupado = [{"sala": "sala_1", "desde": "11:00", "hasta": "12:30"}]

    huecos = agenda.huecos(ocupado, 30, config)

    assert [h for h in huecos if h["salas"] == ["sala_1"]] == [
        {"desde": "10:00", "hasta": "10:45", "salas": ["sala_1"]},
        {"desde": "12:45", "hasta": "19:00", "salas": ["sala_1"]},
    ]


def test_un_hueco_mas_corto_que_el_tratamiento_no_se_ofrece(config):
    ocupado = [{"sala": "sala_1", "desde": "11:00", "hasta": "12:30"}]

    huecos = agenda.huecos(ocupado, 60, config)

    # El rato de 10:00 a 10:45 son cuarenta y cinco minutos: no entra un 60.
    assert [h for h in huecos if h["salas"] == ["sala_1"]] == [
        {"desde": "12:45", "hasta": "19:00", "salas": ["sala_1"]},
    ]


def test_entre_dos_reservas_separadas_por_el_margen_justo_no_queda_nada(config):
    ocupado = [
        {"sala": "sala_1", "desde": "11:00", "hasta": "12:30"},
        {"sala": "sala_1", "desde": "12:45", "hasta": "14:15"},
    ]

    huecos = agenda.huecos(ocupado, 15, config)

    # Los quince minutos entre una y otra son el margen de las dos. No es hueco.
    assert [h for h in huecos if h["salas"] == ["sala_1"]] == [
        {"desde": "10:00", "hasta": "10:45", "salas": ["sala_1"]},
        {"desde": "14:30", "hasta": "19:00", "salas": ["sala_1"]},
    ]


def test_la_franja_recorta_el_hueco(config):
    huecos = agenda.huecos([], 60, config, franja="mañana")

    assert huecos == [
        {"desde": "10:00", "hasta": "14:00", "salas": ["sala_1"]},
        {"desde": "10:00", "hasta": "14:00", "salas": ["sala_2"]},
    ]


def test_en_el_dia_lleno_un_sesenta_solo_entra_al_final(config):
    assert agenda.huecos(DIA_LLENO, 60, config) == [
        {"desde": "17:45", "hasta": "19:00", "salas": ["sala_1"]},
        {"desde": "17:45", "hasta": "19:00", "salas": ["sala_2"]},
    ]


def test_en_el_dia_lleno_un_noventa_no_entra_en_ningun_lado(config):
    assert agenda.huecos(DIA_LLENO, 90, config) == []


def test_para_dos_personas_hacen_falta_dos_salas_a_la_vez(config):
    huecos = agenda.huecos(DIA_LLENO, 60, config, personas=2)

    assert huecos == [
        {"desde": "17:45", "hasta": "19:00", "salas": ["sala_1", "sala_2"]},
    ]


def test_para_dos_personas_no_sirve_un_rato_libre_en_una_sola_sala(config):
    # La sala 2 queda libre de 14:00 a 14:15 y la sala 1 no. Para dos no vale,
    # y para una tampoco porque son quince minutos.
    huecos = agenda.huecos(DIA_LLENO, 15, config, personas=2)

    assert {"desde": "14:00", "hasta": "14:15"} not in [
        {"desde": h["desde"], "hasta": h["hasta"]} for h in huecos
    ]
