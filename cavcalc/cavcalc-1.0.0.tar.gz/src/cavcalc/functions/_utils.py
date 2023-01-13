from functools import wraps
import numpy as np
import warnings

from .._exiters import quit_print


def check_physical():
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                    result = function(*args, **kwargs)
            except ZeroDivisionError:
                target = function.__name__.split("_")[0]
                quit_print(f"Division by zero occurred when computing target: '{target}'")

            return result

        return wrapper

    return decorator


def modesep_adjust(rtgouy, L):
    """Compute the mode-separation frequency taking into account
    the value of the round-trip Gouy phase.
    """
    from .resonance import _fsr_base

    gouy = np.atleast_1d(rtgouy)
    df = (0.5 * gouy / np.pi) * _fsr_base(L)
    df = np.where(gouy > np.pi, _fsr_base(L) - df, df)

    if not isinstance(rtgouy, np.ndarray) and not isinstance(L, np.ndarray):
        return df[0]

    return df
