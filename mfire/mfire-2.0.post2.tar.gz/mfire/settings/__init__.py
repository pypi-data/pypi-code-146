"""mfire.settings module

This module manages the processing of constants and templates

"""
import json
import collections

from mfire.settings.algorithms import TEXT_ALGO, PREFIX_TO_VAR
from mfire.settings.constants import (
    RULES_DIR,
    RULES_NAMES,
    TEMPLATES_FILENAMES,
    LOCAL,
    UNITS_TABLES,
    SETTINGS_DIR,
    ALT_MIN,
    ALT_MAX,
    SPACE_DIM,
    TIME_DIM,
    N_CUTS,
    GAIN_THRESHOLD,
    Dimension,
    MONOZONE,
    SIT_GEN,
)
from mfire.settings.logger import get_logger
from mfire.settings.settings import Settings

with open(TEMPLATES_FILENAMES[Settings().language]["language"]) as fp:
    _lang_dict = json.load(fp)
_LanguageSettings = collections.namedtuple("LanguageSettings", _lang_dict)

LANGUAGE = _LanguageSettings(**_lang_dict)

__all__ = [
    "TEXT_ALGO",
    "RULES_DIR",
    "RULES_NAMES",
    "TEMPLATES_FILENAMES",
    "PREFIX_TO_VAR",
    "LOCAL",
    "UNITS_TABLES",
    "SETTINGS_DIR",
    "ALT_MIN",
    "ALT_MAX",
    "SPACE_DIM",
    "TIME_DIM",
    "N_CUTS",
    "GAIN_THRESHOLD",
    "LANGUAGE",
    "Settings",
    "Dimension",
    "get_logger",
    "MONOZONE",
    "SIT_GEN",
]
