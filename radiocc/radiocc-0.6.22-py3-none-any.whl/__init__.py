#!/usr/bin/env python3

"""
radiocc
"""

import logging
import os
import string
from pathlib import Path
from typing import Optional

from pkg_resources import get_distribution

from radiocc import config, download_data, interface, process_descriptor
from radiocc.core import enable_gui, run

from .model import Bands, Layers

__all__ = [
    "Bands",
    "Layers",
    "run",
    "enable_gui",
]

__version__ = get_distribution("radiocc").version

# Logging settings.
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "%(asctime)s %(name)s[%(levelname)s]: %(message)s"
LOG_DATEFMT = "%m/%d/%Y %I:%M:%S %p"

# Runtime variables.
SRC_PATH = Path(os.path.realpath(__file__)).parent
ASSETS_PATH = SRC_PATH / "assets"
CFG_PATH = Path("radiocc.yaml")
LOG_PATH = Path("radiocc.log")
INFORMATION_PATH = ASSETS_PATH / "information"
DESCRIPTOR_FILENAME = "descriptor.yaml"

# Start logging.
logging.basicConfig(
    filename=LOG_PATH,
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    datefmt=LOG_DATEFMT,
)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
LOGGER = logging.getLogger("radiocc")
LOGGER.info("Logging enabled.")

# Configurable parameters definition.
cfg = config.Cfg()
gui: Optional[interface.Interface] = None
quick_trace_to_process_and_time: Optional[dict[str, str]] = None

# General Constants.
SPICE_MAVEN_DIRECTORY = Path("spice-maven/mk")
TEMPORARY_DOWNLOAD_DIRECTORY = Path("temporary-download-location")
MAVEN_DIRNAME_TEMPLATE = string.Template("maven $DATE")
DATE_FMT_FOLDER = "YYYY-MMM-DD HH:mm:ss"
