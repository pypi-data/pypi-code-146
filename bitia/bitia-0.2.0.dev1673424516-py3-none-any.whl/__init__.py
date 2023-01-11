"""
BioInformatics Tool for Infrastructure Automation (BiTIA)

"""
from importlib.metadata import version as _version
import os
import logging
from rich.logging import RichHandler
import logging.handlers

log_level = os.environ.get("BITIA_LOGLEVEL", "WARNING").upper()
logging.basicConfig(
    format="%(message)s",
    level=log_level,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

__version__ = _version("bitia")


def version() -> str:
    """version"""
    return __version__
