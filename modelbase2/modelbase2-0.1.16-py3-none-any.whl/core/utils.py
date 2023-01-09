from __future__ import annotations

import inspect
from typing import Callable


def check_function_arity(function: Callable, arity: int) -> bool:
    """Check if the amount of arguments given match argument count"""
    argspec = inspect.getfullargspec(function)
    # Give up on *args functions
    if argspec.varargs is not None:
        return True

    # The sane case
    if len(argspec.args) == arity:
        return True

    # It might be that the user has set some args to default values,
    # in which case they are also ok (might be kwonly as well)
    defaults = argspec.defaults
    if defaults is not None:
        if len(argspec.args) + len(defaults) == arity:
            return True
    kwonly = argspec.kwonlyargs
    if defaults is not None:
        if len(argspec.args) + len(kwonly) == arity:
            return True
    return False
