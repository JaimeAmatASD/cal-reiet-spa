"""El mismo pedido que entra dos veces, en dos correos aparte.

La hoja junta los correos de una misma conversación, pero si el cliente escribe
un correo nuevo por la misma reserva abre otra fila, y el pedido se cuenta dos
veces. El sistema no las junta solo —dos personas de la misma habitación pueden
pedir el mismo día—: marca la fila nueva y decide una persona.
"""
import registro

ANTERIOR = {"pedido": "hilo-1", "cliente": "Marta Vidal", "habitacion": "12",
            "fecha": "2026-11-17", "nota": ""}


def _nueva(**cambios):
    return dict.fromkeys(registro.COLUMNAS, "") | {
        "pedido": "hilo-2", "cliente": "Marta Vidal", "habitacion": "12",
        "fecha": "2026-11-17"} | cambios


def test_mismo_cliente_mismo_dia_misma_habitacion_se_marca():
    fila = registro.marcar_repetido(_nueva(), [ANTERIOR])
    assert fila["nota"] == "posible repetido de hilo-1"


def test_el_nombre_se_compara_sin_mayusculas_ni_espacios_de_mas():
    fila = registro.marcar_repetido(_nueva(cliente=" marta vidal"), [ANTERIOR])
    assert fila["nota"] == "posible repetido de hilo-1"


def test_otro_dia_no_es_repetido():
    assert registro.marcar_repetido(_nueva(fecha="2026-11-18"), [ANTERIOR])["nota"] == ""


def test_otra_habitacion_no_es_repetido():
    assert registro.marcar_repetido(_nueva(habitacion="9"), [ANTERIOR])["nota"] == ""


def test_otro_cliente_no_es_repetido():
    assert registro.marcar_repetido(_nueva(cliente="Jordi Pons"), [ANTERIOR])["nota"] == ""


def test_sin_nombre_o_sin_fecha_no_se_compara():
    # Dos consultas sin nombre del mismo día no dicen que sean la misma persona.
    sin_nombre = ANTERIOR | {"cliente": ""}
    assert registro.marcar_repetido(_nueva(cliente=""), [sin_nombre])["nota"] == ""
    sin_fecha = ANTERIOR | {"fecha": ""}
    assert registro.marcar_repetido(_nueva(fecha=""), [sin_fecha])["nota"] == ""


def test_la_misma_fila_no_es_repetida_de_si_misma():
    assert registro.marcar_repetido(_nueva(pedido="hilo-1"), [ANTERIOR])["nota"] == ""


def test_la_hoja_vacia_no_rompe():
    # Con la hoja vacía, la lectura de n8n devuelve una fila sin nada.
    assert registro.marcar_repetido(_nueva(), [{}])["nota"] == ""
    assert registro.marcar_repetido(_nueva(), [])["nota"] == ""


def test_no_toca_el_resto_de_la_fila():
    nueva = _nueva(lectura="completo", estado="SOLICITADA")
    fila = registro.marcar_repetido(nueva, [ANTERIOR])
    assert {c: v for c, v in fila.items() if c != "nota"} == \
           {c: v for c, v in nueva.items() if c != "nota"}


def test_la_hoja_devuelve_la_habitacion_como_numero():
    # Google Sheets lee «12» como el número 12; la fila nueva lo trae como texto.
    fila = registro.marcar_repetido(_nueva(), [ANTERIOR | {"habitacion": 12}])
    assert fila["nota"] == "posible repetido de hilo-1"
