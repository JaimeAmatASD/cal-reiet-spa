"""Pasa los pedidos de prueba por la IA de verdad y cuenta en cuántos acierta.

    python src/probador.py

Cada pedido de `tests/fixtures/` entra a n8n por la puerta de prueba (el flujo
`flows/probador-lectura.json`), que lo lee con la misma IA y las mismas
instrucciones que el recorrido del buzón. Lo que vuelve se pasa por nuestro
código y se compara con lo que habría sacado una persona, que está anotado en
cada pedido bajo `espera`.

No manda correos, no toca la hoja ni las agendas. Cada pedido gasta una
lectura de la IA.
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

import yaml

import casa
import ficha

PEDIDOS = Path(__file__).parent.parent / "tests" / "fixtures"
PUERTA = os.environ.get("PROBADOR_URL", "http://localhost:5678/webhook/probador-lectura")

CAMPOS_PETICION = ("duracion", "fecha", "franja", "personas")


def comparar(caso: dict, lectura: dict, config: dict) -> list[dict]:
    """Lo que la lectura no acertó, campo por campo. Vacío si acertó todo."""
    espera = caso["espera"]
    resultado = ficha.armar(caso["hilo"], lectura, config)

    leido = {"salida": resultado["salida"], "idioma": resultado.get("idioma")}
    if "peticion" in resultado:
        for campo in CAMPOS_PETICION:
            leido[campo] = resultado["peticion"][campo]["valor"]
        habitacion = resultado["cliente"]["habitacion"]["valor"]
        leido["habitacion"] = None if habitacion is None else str(habitacion)

    # Una consulta derivada no tiene ficha que comparar: basta con que se derive.
    if espera["salida"] == "derivar" and resultado["salida"] == "derivar":
        return []

    return [{"campo": campo, "esperado": esperado, "leido": leido.get(campo)}
            for campo, esperado in espera.items()
            if leido.get(campo) != esperado]


def leer_con_la_ia(caso: dict) -> dict:
    cuerpo = json.dumps({"hilo": caso["hilo"], "fecha_hoy": caso.get("recibido")}).encode()
    pedido = urllib.request.Request(PUERTA, data=cuerpo,
                                    headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(pedido, timeout=120) as respuesta:
        return json.load(respuesta)["entrada"]["pedido"]["lectura"]


def main() -> int:
    config = casa.cargar()
    rutas = sorted(PEDIDOS.glob("*.yaml"))
    if not rutas:
        print(f"No hay pedidos de prueba en {PEDIDOS}")
        return 1

    aciertos = 0
    for ruta in rutas:
        caso = yaml.safe_load(ruta.read_text(encoding="utf-8"))
        try:
            fallos = comparar(caso, leer_con_la_ia(caso), config)
        except Exception as error:  # un pedido que se rompe no frena al resto
            print(f"{ruta.stem:12} NO SE PUDO PROBAR  {error}")
            continue
        if not fallos:
            aciertos += 1
            print(f"{ruta.stem:12} bien")
        else:
            detalle = "; ".join(f"{f['campo']}: esperaba {f['esperado']!r}, leyó {f['leido']!r}"
                                for f in fallos)
            print(f"{ruta.stem:12} MAL   {detalle}")

    print(f"\nAcertó {aciertos} de {len(rutas)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
