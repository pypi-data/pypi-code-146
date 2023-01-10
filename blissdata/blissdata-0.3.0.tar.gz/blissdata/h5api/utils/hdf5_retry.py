import inspect
from functools import wraps
from typing import Callable

from silx.io import h5py_utils
from silx.utils.retry import RetryTimeoutError, RetryError


class SoftRetryError(Exception):
    pass


def retry_file_access(method: Callable) -> Callable:
    return _reset_on_retry_failed(
        h5py_utils.retry(retry_on_error=_retry_on_error)(_reset_before_retry(method))
    )


def ignore_retry_timeout(method: Callable) -> Callable:
    if inspect.isgeneratorfunction(method):

        @wraps(method)
        def wrapper(self, *args, **kw):
            try:
                yield from method(self, *args, *kw)
            except RetryTimeoutError:
                pass

    else:

        @wraps(method)
        def wrapper(self, *args, **kw):
            try:
                return method(self, *args, **kw)
            except RetryTimeoutError:
                pass

    return wrapper


def _retry_on_error(e: BaseException) -> bool:
    return h5py_utils._is_h5py_exception(e) or isinstance(e, RetryError)


def _reset_before_retry(method: Callable) -> Callable:
    if inspect.isgeneratorfunction(method):

        @wraps(method)
        def wrapper(self, *args, start_index: int = 0, **kw):
            try:
                yield from method(self, *args, start_index=start_index, **kw)
            except SoftRetryError:
                raise RetryError
            except Exception as e:
                if _retry_on_error(e):
                    self.reset()
                raise

    else:

        @wraps(method)
        def wrapper(self, *args, **kw):
            try:
                return method(self, *args, **kw)
            except SoftRetryError:
                raise RetryError
            except Exception as e:
                if _retry_on_error(e):
                    self.reset()
                raise

    return wrapper


def _reset_on_retry_failed(method: Callable) -> Callable:
    if inspect.isgeneratorfunction(method):

        @wraps(method)
        def wrapper(self, *args, start_index: int = 0, **kw):
            kw.update(self._retry_options)
            try:
                yield from method(self, *args, start_index=start_index, **kw)
            except RetryTimeoutError:
                self.reset()
                raise

    else:

        @wraps(method)
        def wrapper(self, *args, **kw):
            kw.update(self._retry_options)
            try:
                return method(self, *args, **kw)
            except RetryTimeoutError:
                self.reset()
                raise

    return wrapper
