# -*- coding: utf-8 -*-

""" subgit """

# python stdlib
import logging
import logging.config
import os

__author__ = "Johan Andersson <johan@dynamist.se>"
__version_info__ = (0, 6, 0)
__version__ = ".".join(map(str, __version_info__))


log_level_to_string_map = {
    5: "DEBUG",
    4: "INFO",
    3: "WARNING",
    2: "ERROR",
    1: "CRITICAL",
    0: "INFO",
}

DEFAULT_LOG_LEVEL_TO_MSG_MAPPING_VALUE = "%(message)s"

log_level_to_msg_mapping = {
    5: "%(levelname)s - %(name)s:%(lineno)s - %(message)s",
}


def init_logging(log_level):
    """
    Init logging settings with default set to INFO
    """
    log_level_str = log_level_to_string_map[min(log_level, 5)]

    msg = log_level_to_msg_mapping.get(
        min(log_level, 5),
        DEFAULT_LOG_LEVEL_TO_MSG_MAPPING_VALUE,
    )

    logging_conf = {
        "version": 1,
        "root": {
            "level": log_level_str,
            "handlers": [
                "console",
            ],
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": log_level_str,
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
        },
        "formatters": {
            "simple": {
                "format": f"{msg}",
            },
        },
    }

    logging.config.dictConfig(logging_conf)
