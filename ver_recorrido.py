"""Corre el recorrido entero delante tuyo y cuenta qué va pasando.

    python ver_recorrido.py

No manda nada, no toca ningún calendario y no se conecta a ningún lado. Los
correos y la agenda son inventados, y la parte que entiende el correo viene
grabada, así que esto da siempre lo mismo.

Sirve para ver el camino completo: entra un pedido y sale una petición lista
para pegar en el grupo.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import casa      # noqa: E402
import flujo     # noqa: E402
import peticion  # noqa: E402

# Un día con dos reservas puestas. Solo horas y salas.
AGENDA = [
    {"sala": "sala_1", "desde": "10:00", "hasta": "11:30"},
    {"sala": "sala_2", "desde": "12:45", "hasta": "14:15"},
]

# Un día lleno de punta a punta: el 8 de septiembre real.
AGENDA_LLENA = [
    {"sala": s, "desde": d, "hasta": h}
    for s, franjas in (
        ("sala_1", [("11:00", "12:30"), ("12:45", "14:15"),
                    ("14:30", "15:30"), ("16:00", "17:30")]),
        ("sala_2", [("11:00", "12:30"), ("12:45", "13:45"),
                    ("14:30", "15:30"), ("16:00", "17:30")]))
    for d, h in franjas
]


def pedido(texto, **peticion_leida):
    """Un pedido con la lectura ya hecha, como la devolvería la IA."""
    campos = {"duracion": 90, "fecha": "2026-09-09", "franja": "mañana",
              "personas": 1, "preferencia_terapeuta": None}
    campos.update(peticion_leida)
    return {
        "origen": "buzon",
        "hilo": {"id": "hilo-demo", "asunto": "Massage",
                 "mensajes": [{"de": "i.sorbo@ejemplo.com",
                               "nombre": "Ingrid Sorbo", "texto": texto}]},
        "lectura": {
            "idioma": "en", "intencion": "reserva",
            "senales_salud": "injury" in texto or "pregnant" in texto,
            "pide_recomendacion": False,
            "cliente": {
                "nombre": {"valor": "Ingrid Sorbo", "origen": "dicho"},
                "correo": {"valor": "i.sorbo@ejemplo.com", "origen": "dicho"},
                "habitacion": {"valor": None, "origen": "dicho"},
            },
            "peticion": {campo: {"valor": valor, "origen": "dicho"}
                         for campo, valor in campos.items()},
        },
    }


def _nombre_de_sala(sala_id, config):
    return next(s["nombre"] for s in config["salas"] if s["id"] == sala_id)


def contar(titulo, resultado, config):
    print(f"\n{'=' * 72}\n{titulo}\n{'=' * 72}")

    if resultado["accion"] == "derivar":
        print("\n  → Lo mira una persona.")
        print(f"    {resultado['ficha']['nota']}")
        print("    De este correo no se guardó ni el nombre.")
        return

    if resultado["accion"] == "borrador":
        falta = ", ".join(resultado["ficha"]["falta"])
        print(f"\n  → Falta saber: {falta}. Hay un borrador esperando visto bueno:\n")
        print("    " + resultado["borrador"]["cuerpo"].replace("\n", "\n    "))
        return

    if resultado["accion"] == "sin_hueco":
        minutos = resultado["ficha"]["peticion"]["duracion"]["valor"]
        print(f"\n  → Un {minutos} no entra ese día.")
        if not resultado["alternativas"]:
            print("    Y ninguna otra duración tampoco.")
        for otra in resultado["alternativas"]:
            hueco = otra["huecos"][0]
            print(f"    Un {otra['minutos']} sí: desde las {hueco['desde']}.")
        return

    print("\n  → Está todo. Horas libres ese día:\n")
    for hueco in resultado["huecos"]:
        salas = " y ".join(_nombre_de_sala(sala, config) for sala in hueco["salas"])
        print(f"    de {hueco['desde']} a {hueco['hasta']}   ({salas})")

    hueco = resultado["huecos"][0]
    elegida = hueco["desde"]
    print(f"\n    Una persona elige las {elegida}. La petición queda así:\n")
    for una in peticion.armar(resultado["ficha"], elegida, hueco["salas"], config):
        print("    " + una["texto"].replace("\n", "\n    "))
        print()


def main():
    config = casa.cargar()

    casos = [
        ("1. Un pedido completo, en un día con dos reservas puestas",
         pedido("I would like a 90 minute massage on 9 September, morning."),
         AGENDA),
        ("2. El mismo pedido, pero para dos personas",
         pedido("A 90 minute massage for two, on 9 September, morning.",
                personas=2),
         AGENDA),
        ("3. Un pedido al que le falta la duración",
         pedido("I would like a massage on 9 September in the morning.",
                duracion=None),
         AGENDA),
        ("4. Un 90 en un día lleno de punta a punta",
         pedido("A 90 minute massage on 9 September, afternoon.",
                franja="tarde"),
         AGENDA_LLENA),
        ("5. Un correo que menciona una lesión",
         pedido("I have a shoulder injury, would a massage help?"),
         AGENDA),
    ]

    print("\nRECORRIDO DEL PEDIDO — de un correo a una petición")
    print("Nada de esto se manda. El sistema redacta y espera.")
    for titulo, uno, agenda_del_dia in casos:
        contar(titulo, flujo.procesar(uno, config, agenda_del_dia=agenda_del_dia), config)
    print()


if __name__ == "__main__":
    main()
