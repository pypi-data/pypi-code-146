# read version from installed package
from importlib.metadata import version
__version__ = version("thatscraper")

from .browser import Crawler
from .browser import Key
from .browser import ATTR_SELECTOR
from . import data
from . import common
from . import extractor

__all__ = [
    "Crawler",
    "Key",
    "ATTR_SELECTOR",
    "common",
    "data",
    "extractor"
]
