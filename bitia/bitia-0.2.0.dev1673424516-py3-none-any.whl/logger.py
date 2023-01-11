import logging

from rich.logging import RichHandler
from rich.console import Console

FORMAT = "%(message)s"

logging.basicConfig(
    level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

logger = logging.getLogger("bitia")
console = Console()


def set_logger_level(level_name: str):
    """Set the global logging level"""
    assert level_name.upper() in ["INFO", "DEBUG", "WARNING"]
    lvl = logging.getLevelName(level_name.upper())
    logger.setLevel(lvl)
    for handler in logger.handlers:
        handler.setLevel(lvl)


def cprint(*args, **kwargs):
    """Forward to rich.console.print"""
    console.print(*args, **kwargs)
