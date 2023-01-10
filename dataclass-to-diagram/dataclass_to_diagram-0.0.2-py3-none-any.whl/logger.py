"""Настройка логгирования."""

import logging

from rich.logging import RichHandler

FORMAT: str = "%(message)s"


def logger_setup() -> None:
    """Настройка логгирования."""
    logging.basicConfig(
        level=logging.INFO,
        format=FORMAT,
        datefmt="[%X]",
        handlers=[RichHandler()],
    )
    logging.getLogger("asyncio").setLevel(logging.WARNING)
