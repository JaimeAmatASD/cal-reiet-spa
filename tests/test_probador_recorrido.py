"""El probador del recorrido dice, por cada pedido de prueba, si llegó a la hoja.

Acá no se llama a n8n: se le da lo que n8n devuelve al final del recorrido y se
mira que lo cuente bien.
"""
import probador_recorrido

FILA = {"pedido": "prueba-real-01", "entrado_en": "", "leido_en": "2026-09-24T10:30:00",
        "canal": "buzon", "lectura": "completo", "accion": "borrador", "estado": "SOLICITADA"}


def test_una_fila_escrita_dice_que_hizo_el_sistema_con_el_pedido():
    assert probador_recorrido.resumir([FILA]) == (
        "llegó a la hoja como prueba-real-01: lectura completo, acción borrador")


def test_si_el_recorrido_termina_sin_fila_lo_dice():
    # Un pedido que el recorrido deja afuera —un aviso automático, por ejemplo—
    # termina antes de la hoja. Eso no es un acierto aunque n8n no dé error.
    fin = [{"stdout": '{"leer": false}', "exitCode": 0}]
    assert probador_recorrido.resumir(fin).startswith("NO LLEGÓ A LA HOJA")


def test_si_n8n_no_devuelve_nada_tampoco_cuenta_como_fila():
    assert probador_recorrido.resumir([]).startswith("NO LLEGÓ A LA HOJA")
