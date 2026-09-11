"""La puerta por la que n8n le habla a nuestro código.

n8n corre en JavaScript y esto es Python. Se hablan por línea de comandos: n8n
manda un JSON por la entrada y recibe otro por la salida. Sin servidor, sin
puerto y sin dependencias.

Estas pruebas llaman al programa de verdad, como lo va a llamar n8n. Si pasan,
el enchufe funciona.
"""
import json
import subprocess
import sys
from pathlib import Path

CLI = Path(__file__).resolve().parent.parent / "src" / "cli.py"

PEDIDO = {
    "origen": "buzon",
    "hilo": {"id": "hilo-cli", "asunto": "Massage", "mensajes": [
        {"de": "i.sorbo@ejemplo.com", "nombre": "Ingrid Sorbo",
         "texto": "A 90 minute massage on 9 September, morning please."}]},
    "lectura": {
        "idioma": "en", "intencion": "reserva",
        "senales_salud": False, "pide_recomendacion": False,
        "cliente": {
            "nombre": {"valor": "Ingrid Sorbo", "origen": "dicho"},
            "correo": {"valor": "i.sorbo@ejemplo.com", "origen": "dicho"},
            "habitacion": {"valor": None, "origen": "dicho"}},
        "peticion": {
            "duracion": {"valor": 90, "origen": "dicho"},
            "fecha": {"valor": "2026-09-09", "origen": "dicho"},
            "franja": {"valor": "mañana", "origen": "dicho"},
            "personas": {"valor": 1, "origen": "dicho"},
            "preferencia_terapeuta": {"valor": None, "origen": "dicho"}}},
}


def llamar(comando, entrada):
    hecho = subprocess.run(
        [sys.executable, str(CLI), comando],
        input=json.dumps(entrada), capture_output=True, text=True)
    return hecho.returncode, json.loads(hecho.stdout)


def test_procesar_con_agenda_devuelve_las_horas_libres():
    codigo, salida = llamar("procesar", {
        "pedido": PEDIDO,
        "agenda": [{"sala": "sala_1", "desde": "10:00", "hasta": "11:30"}]})

    assert codigo == 0
    assert salida["accion"] == "elegir_hora"
    assert salida["huecos"][0] == {
        "desde": "10:00", "hasta": "14:00", "salas": ["sala_2"]}


def test_procesar_sin_agenda_pide_la_agenda_de_ese_dia():
    codigo, salida = llamar("procesar", {"pedido": PEDIDO})

    assert codigo == 0
    assert salida["accion"] == "falta_agenda"
    assert salida["fecha"] == "2026-09-09"


def test_peticion_devuelve_el_bloque_para_pegar_en_el_grupo():
    _, procesado = llamar("procesar", {
        "pedido": PEDIDO,
        "agenda": [{"sala": "sala_1", "desde": "10:00", "hasta": "11:30"}]})

    codigo, salida = llamar("peticion", {
        "ficha": procesado["ficha"], "inicio": "12:15", "salas": ["sala_2"]})

    assert codigo == 0
    assert salida["peticiones"][0]["texto"] == "\n".join([
        "PETICIÓN A Espera de pago",
        "Massage 90`",
        "Ingrid Sorbo (Ext)",
        "Wednesday, 9 September⋅12:15 – 13:45",
    ])


def test_una_lectura_mal_formada_sale_como_error_con_codigo_distinto_de_cero():
    roto = json.loads(json.dumps(PEDIDO))
    del roto["lectura"]["peticion"]["fecha"]["origen"]

    codigo, salida = llamar("procesar", {"pedido": roto})

    assert codigo != 0
    assert "origen" in salida["error"]


def test_un_comando_que_no_existe_lo_dice_en_vez_de_reventar():
    codigo, salida = llamar("bailar", {})

    assert codigo != 0
    assert "bailar" in salida["error"]


def test_procesar_devuelve_tambien_la_fila_de_la_hoja_de_registro():
    # n8n llama una sola vez y con lo que sale escribe la fila: si la fila
    # hubiera que pedirla aparte, habría que mandarle todo de vuelta.
    codigo, salida = llamar("procesar", {"pedido": PEDIDO})

    assert codigo == 0
    assert salida["fila"]["pedido"] == "hilo-cli"
    assert salida["fila"]["duracion"] == 90
    assert salida["fila"]["canal"] == "buzon"
