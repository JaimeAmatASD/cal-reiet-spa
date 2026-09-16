"""La puerta por la que n8n le habla a nuestro código.

n8n corre en JavaScript y esto es Python. Se hablan por línea de comandos: entra
un JSON por la entrada estándar y sale otro por la salida. Sin servidor, sin
puerto abierto y sin una dependencia más que se pueda caer.

Se usa así, y así es como lo llama el nodo «Execute Command» de n8n:

    echo '{"pedido": {...}, "agenda": [...]}' | python src/cli.py procesar
    echo '{"ficha": {...}, "inicio": "12:15", "salas": ["sala_2"]}' | python src/cli.py peticion

`procesar` dice qué hacer con un pedido. Si la agenda del día no viene, la
respuesta es `falta_agenda` con la fecha: n8n va a buscarla al calendario y
vuelve a llamar. Es en dos pasos porque hasta que no se lee el correo no se
sabe de qué día hay que traer la agenda.

`procesar` devuelve además `fila`: la línea que se escribe en la hoja de
registro, con las columnas ya en orden. Y `fila_actualizar`: lo que se
escribe si ese pedido ya tiene fila, sin el estado ni lo que llena una persona.

`peticion` escribe el bloque para el grupo, con la hora que eligió una persona
entre las libres. El sistema no elige la hora.

Siempre sale un JSON, también cuando algo falla: ahí sale `{"error": ...}` y el
programa termina con código distinto de cero, para que n8n se entere de las dos
maneras y no siga adelante con una respuesta a medias.
"""
import json
import sys

import casa
import flujo
import peticion
import registro


def procesar(entrada: dict, config: dict) -> dict:
    pedido = entrada["pedido"]
    resultado = flujo.procesar(pedido, config, agenda_del_dia=entrada.get("agenda"))
    # La fila de la hoja va en la misma respuesta: n8n llama una vez y con lo
    # que sale escribe en la hoja, sin tener que mandarnos todo de vuelta.
    fila = registro.fila(pedido, resultado)
    return resultado | {"fila": fila, "fila_actualizar": registro.actualizacion(fila)}


def armar_peticion(entrada: dict, config: dict) -> dict:
    return {"peticiones": peticion.armar(
        entrada["ficha"], entrada["inicio"], entrada["salas"], config)}


COMANDOS = {"procesar": procesar, "peticion": armar_peticion}


def main(argv: list) -> int:
    comando = argv[1] if len(argv) > 1 else ""
    if comando not in COMANDOS:
        return _fallar(f"no sé hacer '{comando}'. Los comandos son: "
                       f"{', '.join(COMANDOS)}")

    try:
        entrada = json.load(sys.stdin)
    except json.JSONDecodeError as error:
        return _fallar(f"lo que entró no es un JSON válido: {error}")

    try:
        salida = COMANDOS[comando](entrada, casa.cargar())
    except (KeyError, TypeError) as error:
        return _fallar(f"falta algo en lo que entró: {error}")
    except Exception as error:
        return _fallar(str(error), type(error).__name__)

    print(json.dumps(salida, ensure_ascii=False))
    return 0


def _fallar(mensaje: str, tipo: str = "EntradaInvalida") -> int:
    print(json.dumps({"error": mensaje, "tipo": tipo}, ensure_ascii=False))
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
