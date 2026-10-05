"""El flujo exportado de n8n, mirado por dentro.

Hay errores del flujo que no rompen nada a la vista: n8n da la corrida por buena y
simplemente no sigue. Estas pruebas miran la copia en `flows/` para que no vuelvan.
"""
import json
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


def _armar_el_hilo(entrada: dict) -> dict:
    """Corre el código de «Armar el hilo» como lo corre n8n, con una sola entrada."""
    codigo = {p["name"]: p for p in _pasos()}["Armar el hilo"]["parameters"]["jsCode"]
    programa = (
        "const $input = { all: () => [{ json: ENTRADA }], first: () => ({ json: ENTRADA }) };\n"
        "const ENTRADA = " + json.dumps(entrada) + ";\n"
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
