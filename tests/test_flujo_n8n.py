"""El flujo exportado de n8n, mirado por dentro.

Hay errores del flujo que no rompen nada a la vista: n8n da la corrida por buena y
simplemente no sigue. Estas pruebas miran la copia en `flows/` para que no vuelvan.
"""
import json
import re
from pathlib import Path

FLUJO = Path(__file__).parent.parent / "flows" / "del-correo-a-la-ficha.json"


def _pasos():
    datos = json.loads(FLUJO.read_text(encoding="utf-8"))
    if isinstance(datos, list):
        datos = datos[0]
    return datos["nodes"]


def test_una_agenda_vacia_no_corta_el_recorrido():
    # Una sala sin nada ese día devuelve cero eventos, y n8n se frena ahí sin
    # avisar. Justo el día con huecos quedaba sin decisión y sin fila.
    agendas = [p for p in _pasos() if p["type"] == "n8n-nodes-base.googleCalendar"]
    assert agendas
    for paso in agendas:
        assert paso.get("alwaysOutputData") is True, paso["name"]


def test_se_leen_las_agendas_de_todas_las_salas_antes_de_seguir():
    # Con las salas en ramas paralelas, n8n termina el recorrido entero por la
    # primera antes de mirar la segunda: la decisión salía sin la sala 2, y la
    # segunda volvía a disparar el resto. Las agendas van en fila, una detrás de otra.
    datos = json.loads(FLUJO.read_text(encoding="utf-8"))
    if isinstance(datos, list):
        datos = datos[0]
    agendas = {p["name"] for p in datos["nodes"]
               if p["type"] == "n8n-nodes-base.googleCalendar"}
    salidas_afuera = [
        (origen, destino["node"])
        for origen in agendas
        for rama in datos["connections"].get(origen, {}).get("main", [])
        for destino in rama
        if destino["node"] not in agendas
    ]
    assert len(salidas_afuera) == 1, salidas_afuera


PROBADOR = FLUJO.parent / "probador-lectura.json"


def test_el_probador_lee_igual_que_el_recorrido_del_buzon():
    # El probador mide cuánto acierta la lectura del buzón. Si sus instrucciones
    # o su modelo se separan de las del recorrido, mide otra cosa y nadie se entera.
    buzon = {p["name"]: p for p in _pasos()}
    probador = {p["name"]: p for p in json.loads(PROBADOR.read_text(encoding="utf-8"))["nodes"]}
    for nombre in ("Leer el correo", "Modelo Gemini", "Armar el pedido"):
        assert probador[nombre]["parameters"] == buzon[nombre]["parameters"], nombre
        assert probador[nombre]["type"] == buzon[nombre]["type"], nombre

    # Lo que «Armar el hilo» le deja a la lectura también tiene que ser lo mismo.
    for linea in ('duraciones: "40, 60, 90"',
                  'texto_hilo: mensajes.map(m => `De: ${m.de}\\n${m.texto}`).join("\\n\\n---\\n\\n")'):
        de_probador = linea.replace("mensajes.map", "hilo.mensajes.map")
        assert linea in buzon["Armar el hilo"]["parameters"]["jsCode"]
        assert de_probador in probador["Armar el hilo"]["parameters"]["jsCode"]


def test_la_ia_contesta_siempre_igual_al_mismo_correo():
    # Sin esto el mismo pedido salía bien en una pasada y mal en la siguiente, y
    # la medición no decía nada. La copia del probador la cubre la prueba de arriba.
    modelo = {p["name"]: p for p in _pasos()}["Modelo Gemini"]
    assert modelo["parameters"]["options"].get("temperature") == 0


# --- La puerta de prueba del recorrido entero ---------------------------------
#
# Los pedidos de `tests/fixtures/` pueden recorrer el camino completo —IA,
# agendas y hoja— sin mandar un correo. Entran por una puerta propia justo antes
# de «Armar el hilo», así que todo lo que viene después es exactamente lo mismo.

import shutil
import subprocess

PROBADOR_RECORRIDO = FLUJO.parent / "probador-recorrido.json"


def _flujo():
    datos = json.loads(FLUJO.read_text(encoding="utf-8"))
    return datos[0] if isinstance(datos, list) else datos


def _armar_el_hilo(entrada: dict, *otras: dict) -> dict:
    """Corre el código de «Armar el hilo» como lo corre n8n: un ítem por mensaje."""
    codigo = {p["name"]: p for p in _pasos()}["Armar el hilo"]["parameters"]["jsCode"]
    programa = (
        "const $input = { all: () => TODAS.map(json => ({ json })), first: () => ({ json: TODAS[0] }) };\n"
        "const TODAS = " + json.dumps([entrada, *otras]) + ";\n"
        "const salida = (() => {\n" + codigo + "\n})();\n"
        "process.stdout.write(JSON.stringify(salida[0].json));\n"
    )
    node = shutil.which("node")
    assert node, "Hace falta node para correr el código de n8n"
    hecho = subprocess.run([node, "-e", programa], capture_output=True, text=True, check=True)
    return json.loads(hecho.stdout)


def test_la_puerta_de_prueba_entra_por_armar_el_hilo():
    datos = _flujo()
    puertas = [p["name"] for p in datos["nodes"]
               if p["type"] == "n8n-nodes-base.executeWorkflowTrigger"]
    assert len(puertas) == 1, puertas
    destinos = [d["node"] for rama in datos["connections"][puertas[0]]["main"] for d in rama]
    assert destinos == ["Armar el hilo"]


def test_un_pedido_de_prueba_sale_marcado_para_distinguirlo_en_la_hoja():
    # La fila de una prueba va a la misma hoja que las de verdad. Tiene que
    # poder reconocerse de un vistazo para no contarla con los pedidos reales.
    hilo = {"id": "real-01", "asunto": "Reserva masaje",
            "mensajes": [{"de": "n.ferrer@ejemplo.com", "nombre": "Nuria Ferrer",
                          "texto": "Masaje de 60 el jueves por la tarde."}]}
    salida = _armar_el_hilo({"prueba": {"hilo": hilo, "fecha_hoy": "2026-09-14"}})
    assert salida["hilo"]["id"] == "prueba-real-01"
    assert salida["hilo"]["mensajes"] == hilo["mensajes"]
    assert salida["fecha_hoy"] == "2026-09-14"
    assert salida["duraciones"] == "40, 60, 90"
    assert salida["texto_hilo"] == "De: n.ferrer@ejemplo.com\nMasaje de 60 el jueves por la tarde."


def test_un_correo_del_buzon_no_sale_marcado_como_prueba():
    correo = {"id": "m1", "threadId": "1a0c9698894046e9", "Subject": "Masaje",
              "From": "Ana <ana@ejemplo.com>", "snippet": "Hola, un masaje",
              "internalDate": "1790000000000", "payload": {}}
    salida = _armar_el_hilo(correo)
    assert salida["hilo"]["id"] == "1a0c9698894046e9"


def test_el_probador_del_recorrido_llama_al_recorrido_del_buzon():
    probador = json.loads(PROBADOR_RECORRIDO.read_text(encoding="utf-8"))
    if isinstance(probador, list):
        probador = probador[0]
    pasos = {p["type"]: p for p in probador["nodes"]}
    llamada = pasos["n8n-nodes-base.executeWorkflow"]["parameters"]
    assert llamada["workflowId"]["value"] == _flujo()["id"]
    assert pasos["n8n-nodes-base.webhook"]["parameters"]["path"] == "probador-recorrido"


def test_antes_de_agregar_una_fila_se_mira_si_el_pedido_ya_estaba():
    # Un cliente que escribe dos correos aparte por la misma reserva abría dos
    # filas y se contaba dos veces. La fila nueva pasa antes por `repetido`.
    datos = json.loads(FLUJO.read_text(encoding="utf-8"))
    if isinstance(datos, list):
        datos = datos[0]
    pasos = {p["name"]: p for p in datos["nodes"]}
    siguiente = {origen: [d["node"] for rama in salidas.get("main", []) for d in rama]
                 for origen, salidas in datos["connections"].items()}

    camino, paso = [], siguiente["¿Existe la fila?"][-1]
    while paso != "Agregar la fila":
        camino.append(paso)
        paso = siguiente[paso][0]
    comandos = [pasos[p]["parameters"].get("command", "") for p in camino]
    assert any(c.endswith("cli.py repetido") for c in comandos), camino
    assert pasos[camino[0]].get("alwaysOutputData") is True, camino[0]


def test_al_cliente_se_le_contesta_despues_de_anotar_la_fila():
    # Primero queda medido, después se contesta: si el correo falla, la fila ya está.
    datos = json.loads(FLUJO.read_text(encoding="utf-8"))[0]
    conexiones = datos["connections"]
    for origen in ("Agregar la fila", "Poner al día la fila"):
        assert conexiones[origen]["main"][0][0]["node"] == "¿Hay que contestarle?"
    assert conexiones["¿Hay que contestarle?"]["main"][0][0]["node"] == "Contestar al cliente"
    contestar = {p["name"]: p for p in datos["nodes"]}["Contestar al cliente"]
    assert contestar["parameters"]["operation"] == "reply"
    assert contestar["parameters"]["options"]["appendAttribution"] is False


def test_cada_mensaje_sabe_si_lo_escribio_el_spa():
    # Sin esto, nuestra propia respuesta vuelve a entrar y se contesta sin fin.
    # Gmail, en modo completo, dice las etiquetas en «labels», como en el
    # correo real del 2026-10-06; no en «labelIds».
    cliente = {"id": "m1", "threadId": "t1", "Subject": "Masaje", "From": "cliente@ejemplo.com",
               "labels": [{"id": "INBOX", "name": "INBOX"}], "snippet": "Quiero un masaje"}
    spa = {"id": "m2", "threadId": "t1", "Subject": "Re: Masaje", "From": "spa@ejemplo.com",
           "labels": [{"id": "SENT", "name": "SENT"}], "snippet": "¿De cuántos minutos?"}
    mensajes = _armar_el_hilo(cliente, spa)["hilo"]["mensajes"]
    assert [m["propio"] for m in mensajes] == [False, True]


def _primera_respuesta(fila_existente: dict) -> list:
    """Corre el código de «¿Es la primera respuesta?» como lo corre n8n."""
    codigo = {p["name"]: p for p in _pasos()}["¿Es la primera respuesta?"]["parameters"]["jsCode"]
    pasos = {
        "¿Ya tiene fila?": fila_existente,
        "Leer la respuesta": {"fila": {"pedido": "hilo-1"}},
    }
    programa = (
        "const PASOS = " + json.dumps(pasos) + ";\n"
        "const $ = nombre => ({ first: () => ({ json: PASOS[nombre] }) });\n"
        "const salida = (() => {\n" + codigo + "\n})();\n"
        "process.stdout.write(JSON.stringify(salida.map(i => i.json)));\n"
    )
    hecho = subprocess.run([shutil.which("node"), "-e", programa],
                           capture_output=True, text=True, check=True)
    return json.loads(hecho.stdout)


def test_despues_de_contestar_se_anota_la_hora_en_la_fila():
    # Con «entrado_en» da cuánto se tarda en contestar, que es lo que quiere Petra.
    datos = _flujo()
    conexiones = datos["connections"]
    assert conexiones["Contestar al cliente"]["main"][0][0]["node"] == "¿Es la primera respuesta?"
    assert conexiones["¿Es la primera respuesta?"]["main"][0][0]["node"] == "Anotar la respuesta"
    anotar = {p["name"]: p for p in datos["nodes"]}["Anotar la respuesta"]
    assert anotar["parameters"]["operation"] == "update"
    assert anotar["parameters"]["columns"]["matchingColumns"] == ["pedido"]


def test_la_primera_respuesta_deja_la_hora_en_la_fila():
    salida = _primera_respuesta({})  # fila nueva: el pedido no estaba
    assert len(salida) == 1
    assert salida[0]["pedido"] == "hilo-1"
    assert re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d", salida[0]["respondido_en"])


def test_si_ya_se_le_habia_contestado_la_hora_no_se_pisa():
    # Lo que se mide es cuánto tardó la primera respuesta, no la última.
    salida = _primera_respuesta({"pedido": "hilo-1", "respondido_en": "2026-10-09T11:14:25"})
    assert salida == []
