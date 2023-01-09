"""@Author: Rayane AMROUCHE

Saving functions for all modules.
"""

from typing import Any
import os

import _pickle as c_pickle  # type: ignore


def save_obj(obj: Any, dir_path: str, name: str) -> None:
    """Pickle save a given object in a given path.

    Args:
        obj (Any): Object to save.
        dir_path (str): Directory path for the obj to save.
        name (str): Name of the object to save.
    """
    with open(os.path.join(dir_path, name), "wb") as save_file:
        c_pickle.dump(obj, save_file)


def load_obj(path: str) -> Any:
    """Load a saved object at a given path.

    Args:
        path (str): Path of the saved object.

    Returns:
        Any: Object loaded.
    """
    obj = None
    with open(path, "rb") as load_file:
        obj = c_pickle.load(load_file)
    return obj
