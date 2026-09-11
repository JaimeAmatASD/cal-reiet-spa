"""Lee la configuración de la casa. El único punto del sistema que toca esos archivos.

Todo lo propio de Cal Reiet entra por acá. Si algún día aparece un tratamiento
o una duración escrita dentro del código, es un error: va en config/.

Son dos archivos y se juntan al cargar: casa.yaml (la casa) y tratamientos.yaml
(el catálogo, que es lo que más se toca y lo mantiene Egi).

Se valida al cargar y no después. El formato YAML es cómodo de editar a mano
pero adivina tipos, y adivina mal justo acá: en una lista de idiomas lee `no`
(noruego) como "falso", y una hora suelta como 10:30 la lee como el número 630.
Por eso reventamos al arrancar con un mensaje que diga qué mirar, en vez de
fallar tres pasos más adelante sin que se note.
"""
import re
from pathlib import Path

import yaml

CONFIG = Path(__file__).resolve().parent.parent / "config"
# Una hora escrita a mano: "10:00". Las comillas no son decoración, ver abajo.
HORA = re.compile(r"^\d{1,2}:\d{2}$")
RUTA_CASA = CONFIG / "casa.yaml"
RUTA_TRATAMIENTOS = CONFIG / "tratamientos.yaml"


class ConfiguracionInvalida(Exception):
    """La configuración de la casa no se puede usar. El mensaje dice qué mirar."""


def cargar(ruta_casa: Path = RUTA_CASA, ruta_tratamientos: Path = RUTA_TRATAMIENTOS) -> dict:
    """Devuelve la configuración de la casa, ya validada, como diccionario."""
    config = _leer(ruta_casa)
    config["tratamientos"] = _leer(ruta_tratamientos).get("tratamientos")
    _validar(config)
    return config


def _leer(ruta: Path) -> dict:
    with open(ruta, encoding="utf-8") as f:
        contenido = yaml.safe_load(f)
    if not isinstance(contenido, dict):
        raise ConfiguracionInvalida(f"{ruta.name} está vacío o mal formado")
    return contenido


def _validar(config: dict) -> None:
    for clave in ("casa", "margen_minutos", "aviso_sin_pago_horas", "salas",
                  "tratamientos", "idiomas", "horario", "franjas", "senales_salud",
                  "textos"):
        if config.get(clave) is None:
            raise ConfiguracionInvalida(f"falta '{clave}' en config/casa.yaml")

    for clave in ("margen_minutos", "aviso_sin_pago_horas"):
        if not isinstance(config[clave], int):
            raise ConfiguracionInvalida(
                f"'{clave}' tiene que ser un número de minutos u horas, "
                f"y vino: {config[clave]!r}")

    _validar_horario(config)

    for idioma in config["idiomas"]:
        # Acá es donde YAML muerde: `no` sin comillas se lee como falso.
        if not isinstance(idioma, str):
            raise ConfiguracionInvalida(
                f"el idioma {idioma!r} de casa.yaml no se leyó como texto. "
                f"Escribilo entre comillas: - \"no\"")
        if idioma not in config["textos"].get("borrador", {}):
            raise ConfiguracionInvalida(
                f"el idioma '{idioma}' está en la lista pero no tiene su bloque "
                f"en textos.borrador de casa.yaml")

    if not config["tratamientos"]:
        raise ConfiguracionInvalida("config/tratamientos.yaml no tiene ningún tratamiento")

    for tratamiento in config["tratamientos"]:
        for duracion in tratamiento["duraciones"]:
            if not isinstance(duracion["minutos"], int):
                raise ConfiguracionInvalida(
                    f"la duración {duracion['minutos']!r} del tratamiento "
                    f"'{tratamiento['id']}' no es un número de minutos")
            precio = duracion.get("precio_eur")
            if precio is not None and not isinstance(precio, (int, float)):
                raise ConfiguracionInvalida(
                    f"el precio {precio!r} de los {duracion['minutos']} minutos "
                    f"de '{tratamiento['id']}' no es una cifra")


def tratamiento(config: dict, tratamiento_id: str = "masaje") -> dict:
    """Un tratamiento del catálogo.

    Por ahora todo entra como 'masaje': el catálogo real lo tiene que mandar
    Egi y hasta entonces el sistema no distingue tipos.
    """
    for candidato in config["tratamientos"]:
        if candidato["id"] == tratamiento_id:
            return candidato
    raise ConfiguracionInvalida(f"no existe el tratamiento '{tratamiento_id}'")


def duraciones(config: dict, tratamiento_id: str = "masaje") -> list[dict]:
    """Las duraciones reservables de un tratamiento, con su precio si lo tiene."""
    return tratamiento(config, tratamiento_id)["duraciones"]


def preferencias(config: dict) -> list[str]:
    """Las preferencias de terapeuta que la casa reconoce.

    Son las que sabe escribir en la petición, y nada más. Lo que llegue fuera
    de esta lista se descarta.
    """
    return list(config["textos"]["peticion"]["preferencia"])


def _validar_horario(config: dict) -> None:
    """Que las horas sean horas y que ninguna franja termine antes de empezar."""
    abre = _hora(config["horario"].get("abre"), "apertura de las salas")
    cierra = _hora(config["horario"].get("cierra"), "cierre de las salas")
    if cierra <= abre:
        raise ConfiguracionInvalida(
            f"las salas cierran ({config['horario'].get('cierra')}) antes de "
            f"abrir ({config['horario'].get('abre')}) en config/casa.yaml")

    if not isinstance(config["franjas"], dict):
        raise ConfiguracionInvalida(
            "'franjas' tiene que ser una lista con nombre, y cada franja con su "
            "'desde' y su 'hasta'. Vino: "
            f"{config['franjas']!r}")

    for nombre, rango in config["franjas"].items():
        desde = _hora(rango.get("desde"), f"principio de la franja '{nombre}'")
        hasta = _hora(rango.get("hasta"), f"final de la franja '{nombre}'")
        if hasta <= desde:
            raise ConfiguracionInvalida(
                f"la franja '{nombre}' termina antes de empezar, en config/casa.yaml")


def _hora(valor, donde: str) -> int:
    """Una hora del archivo, en minutos desde la medianoche.

    Acá es donde YAML muerde por segunda vez: 10:00 sin comillas se lee como el
    número 600, no como una hora, y el error aparecería mucho más adelante.
    """
    if not isinstance(valor, str) or not HORA.match(valor):
        raise ConfiguracionInvalida(
            f"la hora de {donde} no se leyó como texto y vino: {valor!r}. "
            f"Escribila entre comillas en config/casa.yaml: \"10:00\"")

    horas, minutos = (int(parte) for parte in valor.split(":"))
    if horas > 23 or minutos > 59:
        raise ConfiguracionInvalida(f"la hora de {donde} no existe: {valor!r}")
    return horas * 60 + minutos
