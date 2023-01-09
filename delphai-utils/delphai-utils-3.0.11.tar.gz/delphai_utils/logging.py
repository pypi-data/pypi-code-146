import logging as _logging
import warnings

import coloredlogs

from delphai_utils.config import get_config


LOGGING_LEVEL = "INFO"

LOGGING_FORMAT = "[%(asctime)s.%(msecs)03d] [%(levelname)s] [%(name)s] %(message)s"

LOGGERS_RESET = [
    "uvicorn",
    "uvicorn.error",
    "uvicorn.access",
]

LOGGERS_LEVELS = {
    "aiohttp": "ERROR",
    "aiokafka": "ERROR",
    "azure": "ERROR",
    "elasticsearch": "ERROR",
    "faust": "ERROR",
    "httpx": "WARNING",
    "mode": "ERROR",
    "urllib3": "ERROR",
}


def configure_logging(*, loggers_levels={}):
    logging_config = get_config("logging") or {}

    coloredlogs.install(
        level=_logging.NOTSET, fmt=logging_config.get("format", LOGGING_FORMAT)
    )

    for logger_name in LOGGERS_RESET:
        logger_object = _logging.getLogger(logger_name)
        logger_object.propagate = True
        logger_object.setLevel(_logging.NOTSET)
        logger_object.handlers.clear()

    _logging.root.setLevel(logging_config.get("level", LOGGING_LEVEL))

    loggers_levels = dict(LOGGERS_LEVELS, **(loggers_levels or {}))
    for logger_name, logger_level in loggers_levels.items():
        _logging.getLogger(logger_name).setLevel(logger_level)

    for logger_name, logger_config in logging_config.get("loggers", {}).items():
        if "level" in logger_config:
            _logging.getLogger(logger_name).setLevel(logger_config["level"])


def error_with_traceback():
    """
    Writes to log an occured exception with a last line of traceback
    """

    warnings.warn(
        'Use `logger.exception("Your message")` instead of:',
        RuntimeWarning,
        stacklevel=2,
    )
    _logging.exception("Error")


class _LoggingWrapper:
    def __getattr__(self, name):
        if "warning_showed" not in self.__dict__:
            self.warning_showed = True

            if not _logging.root.handlers:
                warnings.warn(
                    "You need to initialize logging by calling `delphai_utils.logging.configure_logging()`",
                    RuntimeWarning,
                    stacklevel=2,
                )

        warnings.warn(
            "Use internal logging ( https://wiki.delphai.dev/wiki/Logging ) instead of:",
            RuntimeWarning,
            stacklevel=2,
        )
        return getattr(_logging, name)


logging = _LoggingWrapper()
