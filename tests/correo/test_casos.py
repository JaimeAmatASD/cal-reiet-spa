"""Recorre los correos de tests/correo/casos/ y comprueba la ficha que sale.

Para sumar un caso no hay que tocar este archivo: se agrega un .yaml en la
carpeta con el correo, la lectura grabada de la IA y lo que se espera, y esta
batería lo levanta sola.

No se llama al modelo. Cada caso trae grabada la respuesta de la IA para ese
hilo, así la prueba es rápida y da siempre lo mismo.
"""
import json
from pathlib import Path

import pytest
import yaml

import casa
import ficha

CASOS = sorted((Path(__file__).parent / "casos").glob("*.yaml"))


@pytest.fixture(scope="module")
def config():
    return casa.cargar()


@pytest.mark.parametrize("ruta", CASOS, ids=lambda ruta: ruta.stem)
def test_el_correo_produce_la_ficha_esperada(ruta, config):
    caso = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    espera = caso["espera"]

    resultado = ficha.armar(caso["hilo"], caso["lectura"], config)

    assert resultado["salida"] == espera["salida"]

    if "motivo" in espera:
        assert resultado["motivo"] == espera["motivo"]
    if "idioma" in espera:
        assert resultado["idioma"] == espera["idioma"]
    if "falta" in espera:
        assert resultado["falta"] == espera["falta"]
    if "a_confirmar" in espera:
        assert resultado["a_confirmar"] == espera["a_confirmar"]

    if espera.get("sin_borrador"):
        assert resultado.get("borrador") is None, "esta consulta la contesta una persona"
    else:
        cuerpo = resultado["borrador"]["cuerpo"]
        for texto in espera.get("borrador_contiene", []):
            assert texto in cuerpo, f"el borrador no dice: {texto!r}\n---\n{cuerpo}"
        for texto in espera.get("borrador_no_contiene", []):
            assert texto not in cuerpo, f"el borrador no debería decir: {texto!r}\n---\n{cuerpo}"

    if espera.get("cliente_guardado"):
        assert resultado["cliente"]["nombre"]["valor"] is not None

    if espera.get("motivo") == "salud":
        _comprobar_que_no_guarda_nada(resultado, caso["hilo"])


def _comprobar_que_no_guarda_nada(resultado, hilo):
    """Una consulta con datos de salud deja constancia y nada más.

    Ni el texto del correo, ni el nombre, ni la dirección. Solo el número de
    hilo, para que una persona pueda ir a buscarlo al buzón.
    """
    assert set(resultado) == {"salida", "motivo", "hilo_id", "leido_en", "nota"}

    guardado = json.dumps(resultado, ensure_ascii=False)
    for mensaje in hilo["mensajes"]:
        assert mensaje["nombre"] not in guardado
        assert mensaje["de"] not in guardado
        for palabra in mensaje["texto"].split():
            if len(palabra) > 6:
                assert palabra not in guardado, f"quedó guardado del correo: {palabra!r}"
