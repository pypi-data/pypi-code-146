import logging
from logging import Logger
from logging import config as logging_config
from akerbp.mlops.core.logger_config import LOGGING_CONFIG

base_name = "main"


def get_logger(name: str = base_name) -> Logger:
    """
    Set up a stream logger

    Args:
        name (str): name of the logger. Defaults to the global base_name variable

    Returns:
        (Logger): logger object
    """

    logging_config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(name)
    logging.captureWarnings(True)

    return logger
