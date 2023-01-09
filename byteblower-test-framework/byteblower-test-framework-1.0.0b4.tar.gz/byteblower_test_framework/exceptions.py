"""Module related to excepctions and handling of them."""
import logging
from functools import wraps
from typing import Callable  # for type hinting

from byteblowerll.byteblower import ConfigError, DomainError

__all__ = ('log_api_error', )


def log_api_error(func: Callable) -> Callable:
    """Decorate method or function to logs ByteBlower API errors.

    Any exception will be (re-)raised.

    :param func: Function to decorate
    :type func: Callable
    :return: Decorated function
    :rtype: Callable
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ConfigError, DomainError) as e:
            logging.error("API error: %s", e.getMessage())
            raise

    return wrapper
