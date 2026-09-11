"""La configuración se valida al arrancar, no tres pasos más adelante.

La edita alguien que no programa, y este formato adivina tipos: una hora suelta
como 10:00 la lee como el número 600. Si eso pasa, el sistema tiene que
reventar en el arranque con un mensaje que diga qué línea mirar.
"""
import pytest

import casa


def cargar_con(tmp_path, viejo, nuevo):
    ruta = tmp_path / "casa.yaml"
    original = casa.RUTA_CASA.read_text(encoding="utf-8")
    assert viejo in original, f"la configuración ya no dice {viejo!r}"
    ruta.write_text(original.replace(viejo, nuevo), encoding="utf-8")
    return casa.cargar(ruta_casa=ruta)


def test_una_hora_sin_comillas_revienta_con_un_mensaje_que_dice_que_hacer(tmp_path):
    with pytest.raises(casa.ConfiguracionInvalida, match="comillas"):
        cargar_con(tmp_path, 'abre: "10:00"', "abre: 10:00")


def test_sin_horario_no_se_puede_buscar_hueco_y_no_arranca(tmp_path):
    with pytest.raises(casa.ConfiguracionInvalida, match="horario"):
        cargar_con(tmp_path, "horario:\n  abre:", "horario_viejo:\n  abre:")


def test_una_franja_a_la_que_le_falta_una_punta_no_arranca(tmp_path):
    with pytest.raises(casa.ConfiguracionInvalida, match="mañana"):
        cargar_con(tmp_path, '  mañana:\n    desde: "10:00"\n    hasta: "14:00"',
                   '  mañana:\n    desde: "10:00"')


def test_una_franja_que_termina_antes_de_empezar_no_arranca(tmp_path):
    with pytest.raises(casa.ConfiguracionInvalida, match="tarde"):
        cargar_con(tmp_path, '  tarde:\n    desde: "14:00"', '  tarde:\n    desde: "20:00"')
