"""Custom logging class and setup function"""

import logging
from typing import Optional


def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """get or create a logger.

    Args:
        name (str)
        level (Optional[int]): Defaults to logging.DEBUG.

    Returns:
        logging.Logger
    """
    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO if level is None else level)
    logger.propagate = False

    log_handler = logging.StreamHandler()
    log_handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
    )
    logger.addHandler(log_handler)

    return logger
