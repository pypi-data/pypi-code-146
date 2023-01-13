from functools import wraps
from time import sleep
from typing import Iterable, Union

from . import logger

_INT_BYTES_ORDER = 'big'


def int_to_bytes(i: int) -> bytes:
    length = (i.bit_length() + 7) // 8
    return i.to_bytes(length, _INT_BYTES_ORDER)


def bytes_to_int(bs: bytes) -> int:
    return int.from_bytes(bs, _INT_BYTES_ORDER)


_EXCEPTIONS_TYPE = Union[Exception, Iterable[Exception]]
_MAX_RETRY = 10
_MAX_SLEEP = 30


def retry(times: int = 5, exceptions: _EXCEPTIONS_TYPE = Exception):
    """Retry if exceptions raised.

    :args
        :times
            How many times to retry.
        :exceptions
            If specified, will and only will retry when the specified exceptions
            raised.
    """
    def decorate(func):
        assert isinstance(times, int) and times > 0, f'invalid times: {times}'
        assert times <= _MAX_RETRY, f'at most retry for {_MAX_RETRY} times'
        assert (
            isinstance(exceptions, Iterable) or issubclass(exceptions, Exception)
        ), f'invalid type of exceptions: {type(exceptions)}'
        if isinstance(exceptions, Iterable):
            assert all(
                issubclass(_exc, Exception) for _exc in exceptions
            ), f'every member in exceptions must be of type Excetion: {tuple(exceptions)}'

        @wraps(func)
        def wrapper(*args, **kwargs):
            excepted = tuple(exceptions) if isinstance(exceptions, Iterable) else exceptions
            for i in range(times):
                try:
                    return func(*args, **kwargs)
                except excepted:
                    if i < times - 1:
                        sleep(min(2**(i - 2), _MAX_SLEEP))
                        logger.exception(f'the {i + 1} time attempt failed')
                    else:
                        raise

        return wrapper
    return decorate
