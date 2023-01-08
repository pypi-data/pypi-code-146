import logging
import os
from pathlib import Path
from typing import Any, Dict

CURRENT_DIR = Path(__file__).parent.resolve()

DEBUG = bool(os.getenv("SPOOR_DEBUG", default=""))
DEFAULT_LOGGER_LEVEL = logging.DEBUG if DEBUG else logging.ERROR

LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            # https://docs.python.org/3/library/logging.html#logrecord-attributes
            "format": "%(levelname)s::%(module)s::%(message)s",
            "style": "%",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "spoor": {
            "handlers": ["default"],
            "level": DEFAULT_LOGGER_LEVEL,
            "propagate": False,
        },
    },
}
