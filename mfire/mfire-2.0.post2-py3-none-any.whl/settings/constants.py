"""constants.py

Module for configuring all the application's global constants
"""

from typing import Union, Sequence, Optional
from pathlib import Path

__all__ = [
    "CUR_DIR",
    "SETTINGS_DIR",
    "RULES_DIR",
    "RULES_NAMES",
    "TEMPLATES_FILENAMES",
    "LOCAL",
    "UNITS_TABLES",
    "ALT_MIN",
    "ALT_MAX",
    "SPACE_DIM",
    "TIME_DIM",
    "N_CUTS",
    "GAIN_THRESHOLD",
    "Dimension",
]

# Paths
CUR_DIR = Path(".")
SETTINGS_DIR = Path(__file__).absolute().parent

# Rules
RULES_DIR = SETTINGS_DIR / "rules"
RULES_NAMES = tuple(
    d.name for d in RULES_DIR.iterdir() if d.is_dir() and not d.name.startswith("__")
)

# Text
_text_dir = SETTINGS_DIR / "text"
TEMPLATES_FILENAMES = {
    "fr": {
        "language": _text_dir / "fr" / "language.json",
        "date": _text_dir / "fr" / "date.json",
        "synonyms": _text_dir / "fr" / "synonyms.json",
        "period": {
            "short": _text_dir / "period" / "short_term.csv",
            "long": _text_dir / "period" / "alertes_vh_time.ini",
        },
        "multizone": {
            "generic": _text_dir / "comment" / "multizone.json",
            "snow": _text_dir / "comment" / "multizone_snow.json",
            "precip": _text_dir / "comment" / "multizone_precip.json",
            "rep_val_FFRaf": _text_dir / "comment" / "multizone_rep_value_FFRaf.json",
            "rep_val": _text_dir / "comment" / "multizone_rep_value.json",
            "rep_val_snow_bertrand": _text_dir
            / "comment"
            / "multizone_rep_value_snow_bertrand.json",
        },
        "monozone": {
            "precip": _text_dir / "comment" / "monozone_precip.json",
        },
        "synthesis": {
            "period": {"short": _text_dir / "period" / "weather_short_term.csv"},
            "temperature": _text_dir / "synthesis" / "temperature.json",
        },
        "situation_generale": _text_dir / "fr" / "sit_gen_templates.json",
        "directions": _text_dir / "fr" / "directions.json",
        "compass": _text_dir / "fr" / "compass.json",
    },
    "en": {
        "date": _text_dir / "en" / "date.json",
        "compass": _text_dir / "fr" / "compass.json",
    },
}

MONOZONE = _text_dir / "comment" / "monozone.csv"

SIT_GEN = {
    "zones": {
        "front": SETTINGS_DIR / "geos/marine/zones_SG_anticyc_front.geojson",
        "anticyclone": SETTINGS_DIR / "geos/marine/zones_SG_anticyc_front.geojson",
        "depression": SETTINGS_DIR / "geos/marine/zones_SG_depression.geojson",
    },
    "depression": {
        "fast": (8, 16),
        "slow": (4, 8),
        "evol": (2, 4),
        "move": (200, 400),
    },
    "anticyclone": {
        "evol": (8, 16),
        "move": (400, 800),
    },
}

# Data conf
LOCAL = {
    "gridpoint": "[date:stdvortex]/[model]/[geometry:area]/[term:fmth].[format]",
    "promethee_gridpoint": (
        "[date:stdvortex]/[model]/[geometry:area]/"
        "[param].[begintime:fmth]_[endtime:fmth]_[step:fmth].[format]"
    ),
}

# Units
_units_dir = SETTINGS_DIR / "units"
UNITS_TABLES = {
    "pint_extension": _units_dir / "pint_extension.txt",
    "wwmf_w1": _units_dir / "wwmf_w1_correspondence.csv",
}

# Default altitudes min and max
ALT_MIN = -500
ALT_MAX = 10000
EARTH_RADIUS_KM = 6378.137

# Default dimensions used
Dimension = Optional[Union[str, Sequence[str]]]
SPACE_DIM = ("latitude", "longitude")
TIME_DIM = ("valid_time",)

# Localisation default values
N_CUTS = 2
GAIN_THRESHOLD = 0.001
