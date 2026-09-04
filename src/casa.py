"""Lee config/casa.yaml. El único punto del sistema que toca ese archivo.

Todo lo propio de Cal Reiet entra por acá. Si algún día aparece un tratamiento
o una duración escrita dentro del código, es un error: va en casa.yaml.
"""
from pathlib import Path

import yaml

RUTA = Path(__file__).resolve().parent.parent / "config" / "casa.yaml"


def cargar(ruta: Path = RUTA) -> dict:
    """Devuelve la configuración de la casa como diccionario."""
    with open(ruta, encoding="utf-8") as f:
        return yaml.safe_load(f)
