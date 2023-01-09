import logging
import os

ALVIN_VERBOSE_LOG = os.environ.get("ALVIN_VERBOSE_LOG", False)


def is_verbose_logging():
    return ALVIN_VERBOSE_LOG


def log_verbose(message: str, enable_verbose_log: bool = False):
    if is_verbose_logging() or enable_verbose_log:
        print(message)


class AlvinLoggerAdapter(logging.LoggerAdapter):
    """
    This allows for more flexible troubleshooting on Cloud platforms e.g. GCP Composer.
    Each log statement coming from this Alvin plugin has a [alvin] prefix.
    https://docs.python.org/3/howto/logging-cookbook.html#using-loggeradapters-to-impart-contextual-information
    """

    def process(self, msg, kwargs):
        return f"[alvin] {msg}", kwargs
