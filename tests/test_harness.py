"""Prueba el andamio, no el negocio.

Si esto falla, lo que se rompió es el montaje del proyecto (el entorno, las
rutas, la lectura de la configuración), no la lógica de reservas. Sirve para
saber de entrada de qué lado está el problema.
"""
import casa


def test_se_lee_la_configuracion_de_la_casa():
    config = casa.cargar()

    assert config["casa"] == "Cal Reiet"
    for clave in ("margen_minutos", "salas", "tratamientos"):
        assert clave in config, f"falta '{clave}' en config/casa.yaml"
