# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.ml
#  Copyright (C) 2021 Comet ML INC
#  This file can not be copied and/or distributed without the express
#  permission of Comet ML Inc.
# *******************************************************

import getpass
import logging
import os
import re
from datetime import datetime
from typing import Optional

from .logging_messages import (
    LOGGING_DIRECTORY_CREATION_ERROR,
    LOGGING_LOG_FILE_OPEN_ERROR,
)
from .settings import LogLevel, LogSettings, get_model

LOGGER = logging.getLogger(__name__)

MSG_FORMAT = "COMET %(levelname)s: %(message)s"

FILE_MSG_FORMAT = "[%(process)d-%(processName)s:%(thread)d] %(relativeCreated)d COMET %(levelname)s [%(filename)s:%(lineno)d]: %(message)s"


def get_user() -> str:
    try:
        return getpass.getuser()
    except KeyError:
        return "unknown"


def _make_valid(s: str) -> str:
    s = str(s).strip().replace(" ", "_")
    return re.sub(r"(?u)[^-\w.]", "", s)


def expand_log_file_path(log_file_path: Optional[str]) -> Optional[str]:
    """
    Expand patterns in the file logging path.

    Allowed patterns:
        * {datetime}
        * {pid}
        * {project}
        * {user}
    """

    if log_file_path is None:
        return None

    user = _make_valid(get_user())

    patterns = {
        "datetime": datetime.now().strftime("%Y%m%d-%H%M%S"),
        "pid": os.getpid(),
        "user": user,
    }

    try:
        return log_file_path.format(**patterns)
    except KeyError:
        LOGGER.info(
            "Invalid logging file pattern: '%s'; ignoring",
            log_file_path,
            exc_info=True,
        )
        return log_file_path


class CometLoggingConfig(object):
    def __init__(self, settings: LogSettings) -> None:
        self.root = logging.getLogger("comet_mpm")
        logger_level = logging.CRITICAL

        # Don't send comet-mpm to the application logger
        self.root.propagate = settings.mpm_logging_propagate

        # Add handler for console, basic INFO:
        self.console_handler = logging.StreamHandler()

        logging_console_level = settings.mpm_logging_console
        self.console_formatter = logging.Formatter(MSG_FORMAT)

        self.console_handler.setLevel(logging_console_level)
        self.console_handler.setFormatter(self.console_formatter)
        self.root.addHandler(self.console_handler)

        logger_level = min(logger_level, self.console_handler.level)

        # The std* logger might conflicts with the logging if a log record is
        # emitted for each WS message as it would results in an infinite loop. To
        # avoid this issue, all log records after the creation of a message should
        # be at a level lower than info as the console handler is set to info
        # level.

        # Add an additional file handler
        log_file_path = expand_log_file_path(
            settings.mpm_logging_file,
        )
        log_file_level = settings.mpm_logging_file_level
        log_file_overwrite = settings.mpm_logging_file_overwrite

        self.file_handler = None
        self.file_formatter = None

        if log_file_path is not None:

            # Create logfile path, if possible:
            try:
                os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
            except Exception:
                LOGGER.error(
                    LOGGING_DIRECTORY_CREATION_ERROR, log_file_path, exc_info=True
                )

            try:
                # Overwrite file if comet_mpm_file_overwrite:
                if log_file_overwrite:
                    self.file_handler = logging.FileHandler(log_file_path, "w+")
                else:
                    self.file_handler = logging.FileHandler(log_file_path)

                if log_file_level is None:
                    log_file_level = LogLevel(logging.DEBUG)

                self.file_handler.setLevel(log_file_level)
                logger_level = min(logger_level, log_file_level)

                self.file_formatter = logging.Formatter(FILE_MSG_FORMAT)
                self.file_handler.setFormatter(self.file_formatter)
                self.root.addHandler(self.file_handler)
            except Exception:
                LOGGER.error(
                    LOGGING_LOG_FILE_OPEN_ERROR,
                    log_file_path,
                    exc_info=True,
                )

        self.root.setLevel(logger_level)


COMET_LOGGING_CONFIG = None


def _setup_comet_mpm_logging() -> None:
    global COMET_LOGGING_CONFIG

    # Create a settings, read env variables if set and validate values
    settings = get_model(LogSettings)
    COMET_LOGGING_CONFIG = CometLoggingConfig(settings)
