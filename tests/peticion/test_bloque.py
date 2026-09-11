"""El bloque que sale al grupo de terapeutas.

El formato está copiado de los mensajes reales y se comprueba letra por letra a
propósito: el equipo lee estos bloques de un vistazo y cambiarles la forma
cuesta más de lo que vale. Ver docs/convenciones.md.

Los nombres son inventados.
"""
import copy

import pytest

import casa
import ficha
import peticion

LECTURA = {
    "idioma": "es",
    "intencion": "reserva",
    "senales_salud": False,
    "pide_recomendacion": False,
    "cliente": {
        "nombre": {"valor": "Laura Prats", "origen": "dicho"},
        "correo": {"valor": "l.prats@ejemplo.com", "origen": "dicho"},
        "habitacion": {"valor": None, "origen": "dicho"},
    },
    "peticion": {
        "duracion": {"valor": 60, "origen": "dicho"},
        "fecha": {"valor": "2026-09-09", "origen": "dicho"},
        "franja": {"valor": "mañana", "origen": "dicho"},
        "personas": {"valor": 1, "origen": "dicho"},
        "preferencia_terapeuta": {"valor": "mujer", "origen": "dicho"},
    },
}

HILO = {"id": "hilo-p1", "asunto": "Masaje", "mensajes": [
    {"de": "l.prats@ejemplo.com", "nombre": "Laura Prats",
     "texto": "Hola, quería un masaje."}]}


@pytest.fixture(scope="module")
def config():
    return casa.cargar()


def armar_ficha(config, **cambios):
    lectura = copy.deepcopy(LECTURA)
    for bloque, campos in cambios.items():
        lectura[bloque].update(campos)
    return ficha.armar(HILO, lectura, config)


def test_la_peticion_sale_con_las_cinco_lineas(config):
    peticiones = peticion.armar(armar_ficha(config), "12:15", ["sala_1"], config)

    assert [p["texto"] for p in peticiones] == ["\n".join([
        "PETICIÓN A Espera de pago",
        "Terapeuta Mujer",
        "Massage 60`",
        "Laura Prats (Ext)",
        "Wednesday, 9 September⋅12:15 – 13:15",
    ])]


def test_sin_preferencia_esa_linea_no_existe(config):
    ficha_sin = armar_ficha(config, peticion={
        "preferencia_terapeuta": {"valor": None, "origen": "dicho"}})

    texto = peticion.armar(ficha_sin, "12:15", ["sala_1"], config)[0]["texto"]

    assert texto.splitlines() == [
        "PETICIÓN A Espera de pago",
        "Massage 60`",
        "Laura Prats (Ext)",
        "Wednesday, 9 September⋅12:15 – 13:15",
    ]


def test_una_preferencia_deducida_no_sale_en_la_peticion(config):
    """Un dato deducido no cuenta como dato. Vale también para esto."""
    ficha_deducida = armar_ficha(config, peticion={
        "preferencia_terapeuta": {"valor": "mujer", "origen": "deducido"}})

    texto = peticion.armar(ficha_deducida, "12:15", ["sala_1"], config)[0]["texto"]

    assert "Terapeuta Mujer" not in texto


def test_un_cliente_alojado_lleva_habitacion_en_vez_de_ext(config):
    alojada = armar_ficha(config, cliente={
        "habitacion": {"valor": "9", "origen": "dicho"}})

    texto = peticion.armar(alojada, "12:15", ["sala_1"], config)[0]["texto"]

    assert "Laura Prats #9" in texto
    assert "(Ext)" not in texto


def test_la_hora_de_fin_sale_de_la_duracion(config):
    noventa = armar_ficha(config, peticion={
        "duracion": {"valor": 90, "origen": "dicho"}})

    texto = peticion.armar(noventa, "10:00", ["sala_1"], config)[0]["texto"]

    assert "Wednesday, 9 September⋅10:00 – 11:30" in texto


def test_un_pedido_para_dos_personas_son_dos_peticiones_iguales(config):
    dos = armar_ficha(config, peticion={"personas": {"valor": 2, "origen": "dicho"}})

    peticiones = peticion.armar(dos, "17:45", ["sala_1", "sala_2"], config)

    assert len(peticiones) == 2
    assert peticiones[0]["texto"] == peticiones[1]["texto"]
    assert [p["sala"] for p in peticiones] == ["sala_1", "sala_2"]


def test_hacen_falta_tantas_salas_como_personas(config):
    dos = armar_ficha(config, peticion={"personas": {"valor": 2, "origen": "dicho"}})

    with pytest.raises(peticion.NoSePuedeArmar, match="dos personas|2 personas|salas"):
        peticion.armar(dos, "17:45", ["sala_1"], config)
