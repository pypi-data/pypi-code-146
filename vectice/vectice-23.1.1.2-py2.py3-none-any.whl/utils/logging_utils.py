from __future__ import annotations

import logging
import logging.config
import sys

# Logging format example:
# 2022/09/27 15:13:24 INFO vectice.models.project: Job with id: 33694 successfully retrieved.
LOGGING_LINE_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
LOGGING_DATETIME_FORMAT = "%Y/%m/%d %H:%M:%S"


class VecticeLoggingStream:
    """
    A Python stream for use with event logging APIs throughout vectice
    `(`logger.info()`, etc.). This stream wraps `sys.stderr`, forwarding `write()`
    and `flush()` calls to the stream referred to by `sys.stderr` at the time of the call.
    It also provides capabilities for disabling the stream to silence event logs and
    enable propagation for pytest.
    """

    def __init__(self):
        self._enabled = True

    def write(self, text):
        if self._enabled:
            sys.stderr.write(text)

    def flush(self):
        if self._enabled:
            sys.stderr.flush()

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value


VECTICE_LOGGING_STREAM = VecticeLoggingStream()


def disable_logging():
    """
    Disables the `VecticeLoggingStream` used by event logging APIs throughout Vectice
    `logger.info()` silencing all subsequent event logs.
    """
    VECTICE_LOGGING_STREAM.enabled = False


def enable_logging():
    """
    Enables the `VecticeLoggingStream` used by event logging APIs throughout Vectice
    (`logger.info()`, etc), emitting all subsequent event logs. This
    reverses the effects of `disable_logging()`.
    """
    VECTICE_LOGGING_STREAM.enabled = True


def enable_propagation():
    """
    Enables the `VecticeLoggingStream` propagation used by event logging APIs throughout Vectice
    so that the testing suite can use caplog to test the logging stdout.
    """
    _configure_vectice_loggers("vectice", propagate=True)


def _configure_vectice_loggers(root_module_name, propagate=False):
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "vectice_formatter": {
                    "format": LOGGING_LINE_FORMAT,
                    "datefmt": LOGGING_DATETIME_FORMAT,
                },
            },
            "handlers": {
                "vectice_handler": {
                    "formatter": "vectice_formatter",
                    "class": "logging.StreamHandler",
                    "stream": VECTICE_LOGGING_STREAM,
                },
            },
            "loggers": {
                root_module_name: {
                    "handlers": ["vectice_handler"],
                    "level": "INFO",
                    "propagate": propagate,
                },
            },
        }
    )
