"""Pasa los pedidos de prueba por el recorrido entero, hasta la hoja.

    python src/probador_recorrido.py            # todos los de tests/fixtures/
    python src/probador_recorrido.py real-01    # solo ese

Cada pedido entra a n8n por la puerta de prueba (el flujo
`flows/probador-recorrido.json`), que lo mete en el recorrido del buzón justo
después de traer el correo: lo lee la IA, se miran las agendas de las salas y se
escribe la fila en la hoja del laboratorio. Es lo mismo que pasa con un correo
de verdad, sin tener que mandarlo.

La fila queda en la hoja con el número de pedido empezando por «prueba-», para
no contarla con los pedidos reales. Si el mismo pedido se vuelve a probar, su
fila se pone al día en vez de duplicarse.

No manda correos. Cada pedido gasta una lectura de la IA.
"""
import json
import os
import sys
import urllib.error
import urllib.request

import yaml

from probador import PEDIDOS

PUERTA = os.environ.get("PROBADOR_RECORRIDO_URL",
                        "http://localhost:5678/webhook/probador-recorrido")


def resumir(respuesta: list) -> str:
    """Una línea con cómo terminó el recorrido para un pedido."""
    filas = [item for item in respuesta if "pedido" in item and "accion" in item]
    if filas:
        fila = filas[0]
        return (f"llegó a la hoja como {fila['pedido']}: "
                f"lectura {fila.get('lectura') or '-'}, acción {fila['accion']}")
    return "NO LLEGÓ A LA HOJA  el recorrido terminó antes: " + json.dumps(respuesta)[:200]


def recorrer(caso: dict) -> list:
    cuerpo = json.dumps({"prueba": {"hilo": caso["hilo"],
                                    "fecha_hoy": caso.get("recibido")}}).encode()
    pedido = urllib.request.Request(PUERTA, data=cuerpo,
                                    headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(pedido, timeout=300) as respuesta:
        datos = json.load(respuesta)
    return datos if isinstance(datos, list) else [datos]


def main(nombres: list[str]) -> int:
    rutas = sorted(PEDIDOS.glob("*.yaml"))
    if nombres:
        rutas = [r for r in rutas if r.stem in nombres]
    if not rutas:
        print(f"No hay pedidos de prueba con ese nombre en {PEDIDOS}")
        return 1

    llegaron = 0
    for ruta in rutas:
        caso = yaml.safe_load(ruta.read_text(encoding="utf-8"))
        try:
            linea = resumir(recorrer(caso))
        except urllib.error.HTTPError as error:
            linea = (f"FALLÓ EN n8n  ({error.code}) — el paso donde se cortó está en "
                     "las ejecuciones de «Cal Reiet - del correo a la hoja»")
        except Exception as error:  # un pedido que se rompe no frena al resto
            linea = f"NO SE PUDO PROBAR  {error}"
        if linea.startswith("llegó"):
            llegaron += 1
        print(f"{ruta.stem:12} {linea}")

    print(f"\nLlegaron a la hoja {llegaron} de {len(rutas)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
