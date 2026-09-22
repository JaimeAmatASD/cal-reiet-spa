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
