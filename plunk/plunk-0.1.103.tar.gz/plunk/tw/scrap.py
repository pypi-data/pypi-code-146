from functools import partial, wraps
from typing import Callable, Any


def __call_func_handling_error(
    error_handler: Callable, func: Callable, *args, **kwargs
):
    try:
        return func(*args, **kwargs)
    except BaseException as error_obj:
        return error_handler(error_obj, func, args, kwargs)


def _call_func_handling_error(error_handler: Callable, func: Callable):
    return wraps(func)(partial(__call_func_handling_error, error_handler, func))


def _handle_error(error_handler: Callable):
    return partial(_call_func_handling_error, error_handler)


HandlerSpecs = Any
ErrorHandlerFactory = Callable[[HandlerSpecs], Callable]


def handle_error(
    handler_specs: HandlerSpecs, error_handler_factory: ErrorHandlerFactory
):
    error_handler = error_handler_factory(handler_specs)
    return _handle_error(error_handler)
