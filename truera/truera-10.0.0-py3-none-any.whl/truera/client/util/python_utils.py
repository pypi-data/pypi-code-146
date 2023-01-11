from copy import copy
import functools
import importlib
import inspect
from inspect import BoundArguments
import types
from typing import Any, Optional

# NOTE(piotrm): Some functions here would make better sense to put in func_utils
# but since we use them in type_utils and other core utils, we have to include
# them here to avoid circular imports.


def copy_bindings(bindings: BoundArguments) -> BoundArguments:
    """
    Duplicate the given bindings into a new BoundArguments object.
    """

    return BoundArguments(
        bindings.signature.replace(), copy(bindings.arguments)
    )


def cache_on_first_arg(func):
    """
    Create a memoized version of `method` that does caching only on the first
    argument, ignoring the rest for cache-lookup purposes.
    """

    cache = dict()

    @functools.wraps(func)
    def wrapper(k, *args, **kwargs):
        kh = hash(k)
        if kh in cache:
            return cache[kh]
        else:
            v = func(k, *args, **kwargs)
            cache[kh] = v
            return v

    return wrapper


def caller_frame():
    """
    Get the frame of the caller of the method that calls this method, i.e. two
    frames deep in the stack.    
    """
    frame = inspect.currentframe()
    return frame.f_back.f_back


@functools.lru_cache(maxsize=128)
def import_optional_module(module_name: str) -> Optional[types.ModuleType]:
    """
    Split the module importing part of the next method into a cached function
    here as searching for missing modules may be expensive. This returns None if
    module is not imported.
    """

    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None


# Might as well cache this as well.
@functools.lru_cache(maxsize=1024)
def import_optional(
    module_name: str, purpose: Optional[str] = None
) -> types.ModuleType:
    """
    Import the module with the given name. If this fails, return an object which
    will raise an exception if it is used for anything indicating that the given
    module was required.

    This can be used to import modules at the top of a python file even if they
    do not exist for a particular SDK deployment. If the methods that rely on
    those imports never get called, things will be fine. Otherwise if someone
    tries to use the optional module without having it installed, an exception
    will be raised with the given `purpose` message. For example, trulens is
    required for SDK for use with neural networks but not for use with
    tabular/diagnostic models; When using tabular, trulens does not need to be
    installed.
    """

    module = import_optional_module(module_name)

    if module is not None:
        return module

    if purpose is not None:
        fail_msg = (
            f"Module {module_name} is required for {purpose}. "
            "You may need to install it."
        )
    else:
        fail_msg = (
            f"Module {module_name} is required. "
            "You may need to install it."
        )

    class FailWhenUsed:

        def __getattribute__(self, _: str) -> Any:
            raise ImportError(fail_msg)

    return FailWhenUsed()
