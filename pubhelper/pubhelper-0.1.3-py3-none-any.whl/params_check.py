import functools
import logging


def params_check(fn=None, *, required: list = None, optional: list = None, debug=False, logger=None):
    logger = logger or logging.getLogger('__params_check__')
    debug and logger.setLevel(logging.DEBUG)

    def _check_required(func_name: str, **kwargs):
        for item in (required or []):
            if item not in kwargs:
                raise Exception(f'[{func_name}] required param({item}) not found')

    def _check_optional(func_name: str, **kwargs):
        for item in (optional or []):
            if item not in kwargs:
                logger.debug(f'[{func_name}] optional param({item}) not found')

    def inner(f):
        @functools.wraps(f)
        def _inner(*args, **kwargs):
            _check_required(f.__name__, **kwargs)
            _check_optional(f.__name__, **kwargs)

            return f(*args, **kwargs)

        return _inner

    return callable(fn) and inner(fn) or inner


__all__ = ('params_check',)
