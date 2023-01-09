# https://docs.python.org/3/howto/logging.html#library-config
import logging

from rich.logging import RichHandler

logger = logging.getLogger("servicefoundry")


def add_cli_handler(level: int = logging.INFO, show_path=False):
    handler = RichHandler(level=level, show_path=show_path)
    handler.setLevel(level)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
