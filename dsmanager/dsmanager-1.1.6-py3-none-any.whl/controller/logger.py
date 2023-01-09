"""@Author Rayane AMROUCHE

Logger Class.
"""

import os
import logging

from typing import Any


def make_logger(
    path: str,
    name: str,
    level: int = logging.INFO,
    verbose: int = 0,
    logger: Any = None,
) -> logging.Logger:
    """Generates a logging logger by giving file path, name and logging level.

    Args:
        path (str): Logging file path.
        name (str): Name of the logger.
        level (int, optional): Logging level. Defaults to logging.INFO.
        verbose (int, optional): Verbose level. Defaults to 0.
        logger (Any, optional): Default logger inherited to avoid duplication. Defaults
            to 0.

    Returns:
        logging.Logger: Logging logger generated.
    """
    if logger is None:
        logger = logging.getLogger(name)
    handlers = logger.handlers[:]
    for handler in handlers:
        logger.removeHandler(handler)
        handler.close()
    logger.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%a, %d %b %Y %H:%M:%S",
    )

    os.makedirs(path, exist_ok=True)

    file_handler = logging.FileHandler(os.path.join(path, name + ".log"))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    global_handler = logging.FileHandler(os.path.join(path, "all.log"))
    global_handler.setFormatter(formatter)
    logger.addHandler(global_handler)

    if verbose:
        console_handler = logging.StreamHandler()
        logger.addHandler(console_handler)

    return logger
