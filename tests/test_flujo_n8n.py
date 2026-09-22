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
