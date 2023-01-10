import logging
from time import gmtime

LOG_LEVEL_MAP = {"info": logging.INFO, "debug": logging.DEBUG, "error": logging.ERROR}


def get_logger(name: str, log_level: str = "info"):
    logging.Formatter.converter = gmtime
    logging.basicConfig(
        level=LOG_LEVEL_MAP[log_level],
        format="%(asctime)s | %(levelname)s | %(name)s | %(filename)s | %(funcName)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,
    )
    return logging.getLogger(name)
