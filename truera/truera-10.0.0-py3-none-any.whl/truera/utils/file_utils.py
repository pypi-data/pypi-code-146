import inspect
import os
from pathlib import Path


def identify_caller(depth: int = 0):
    """
    Return a string identifying the callsite where the method calling this one
    was called (2 frames deep). Pass in depth to get callers deeper than that
    (default=0).
    """

    caller = inspect.getframeinfo(inspect.stack()[2 + depth][0])
    return f"{caller.filename}:{caller.function}:{caller.lineno}"


def as_path(o: object, warn=False) -> Path:
    """
    Convert the given object to pathlib.Path if it is not, either printing a
    warning or throwing a runtime error.
    """

    caller: str = identify_caller()
    if o is None:
        return None
    elif not isinstance(o, Path):
        if warn:
            print(
                f"WARNING: use of non-pathlib.Path filenames/paths ({o}) will be deprecated"
            )
            print(f"WARNING: {caller}")
            return Path(o)
        else:
            raise RuntimeError(
                f"{caller}: pathlib.Path expected, got {type(o)} instead"
            )
    return o


def join_path(path, *paths) -> str:
    return strip_slashes(os.path.join(path, *paths))


def strip_slashes(path: str) -> str:
    return path.replace("//", "/").replace("\\\\", "\\")