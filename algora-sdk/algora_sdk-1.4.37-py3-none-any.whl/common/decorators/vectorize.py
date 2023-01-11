import functools
from typing import Callable, Any

import numpy as np


def vectorize(function: Callable = None):
    """
    Decorator for wrapping numpy function in `np.vectorize(...)`

    Args:
        function (Callable): Numpy function

    Returns:
        Callable: Wrapped function
    """

    @functools.wraps(vectorize)
    def decorator(f):
        @functools.wraps(f)
        def wrap(*args, **kwargs) -> Any:
            vectorized = np.vectorize(f)
            return vectorized(*args, **kwargs)

        return wrap

    if function is None:
        return decorator
    return decorator(function)
