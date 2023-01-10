import time

from functools import wraps
from inspect import iscoroutinefunction
from typing import Callable


def show_cost_time(view_func: Callable):
    """Run the function and show cost time.

    Supports async and sync function.
    """

    if iscoroutinefunction(view_func):
        @wraps(view_func)
        async def wrapped_view(*args, **kwargs):
            se = time.time()
            result = await view_func(*args, **kwargs)
            print(f'Function {view_func.__name__} cost time is {time.time() - se} s')
            return result
        return wrapped_view

    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        se = time.time()
        result = view_func(*args, **kwargs)
        print(f'Function {view_func.__name__} cost time is {time.time() - se} s')
        return result
    return wrapped_view


def try_and_get_bool(view_func):
    """Run the function use try/catch.

    Returns False if there was an error. Otherwise return True.

    Supports async and sync function.
    """

    # Return async wrapped_view if view_func is coro
    if iscoroutinefunction(view_func):
        @wraps(view_func)
        async def wrapped_view(*args, **kwargs):
            try:
                await view_func(*args, **kwargs)
                return True
            except:
                return False
        return wrapped_view

    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        try:
            view_func(*args, **kwargs)
            return True
        except:
            return False
    return wrapped_view


def try_and_get_data(view_func):
    """Run the function use try/catch.

    Returns None if there was an error. Otherwise return the function result.

    Supports async and sync function.
    """

    # Return async wrapped_view if view_func is coro
    if iscoroutinefunction(view_func):
        @wraps(view_func)
        async def wrapped_view(*args, **kwargs):
            try:
                return await view_func(*args, **kwargs)
            except:
                pass
        return wrapped_view

    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except:
            pass
    return wrapped_view
