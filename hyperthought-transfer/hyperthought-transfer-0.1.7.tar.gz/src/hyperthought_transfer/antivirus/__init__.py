"""
Plug-in framework for antivirus scanners.

Built-in scanners can be accessed directly, e.g.
hyperthought_transfer.antivirus.McAfee.

There is also a plug-in framework that can be used to add scanners.
See the add method for adding scanners and the get method for getting scanners
once added.

All scanners must subclass hyperthought_transfer.antivirus.base.BaseAntivirus.

The get method will return an antivirus class, which can then be used to create
an object instance.
"""

import importlib
import inspect
import os

from .base import BaseAntivirus

# Make antivirus classes available from the antivirus package.
# Ex: hyperthought_transfer.antivirus.McAfee is to be preferred over
#     hyperthought_transfer.antivirus._mcafee.McAfee.
from ._mcafee import McAfee


SCANNERS = {
    "McAfee": McAfee,
}


class ScannerNotFoundException(Exception):
    pass


def get(antivirus_name):
    """
    Get an antivirus class given a name.

    This can be used to get built-in scanners as well as scanners added via the
    plugin framework.
    """
    if not isinstance(antivirus_name, str):
        raise TypeError("antivirus_name must be a string")

    if antivirus_name not in SCANNERS:
        raise ScannerNotFoundException(
            f"No antivirus scanner named '{antivirus_name} could be found."
        )

    return SCANNERS[antivirus_name]


def add(path):
    """
    Add a scanner or scanners at a given file or directory path.

    If the path is for a Python file, the contents will be examined for
    subclasses of hyperthought.antivirus.base.BaseAntivirus.  If it is for a
    directory, the contents will be searched recursively for Python files.

    Parameters
    ----------
    path : str
        A path to a file or directory.

    Results
    -------
    Antivirus classes found in the file or directory will be added to module
    for retrieval via the get method.
    """
    if not os.path.exists(path):
        raise ValueError(f"{path} is not a valid path")

    if os.path.isfile(path):
        file_name, file_extension = os.path.splitext(path)
        file_extension = file_extension.strip(".").lower()

        if file_extension != "py":
            return

        spec = importlib.util.spec_from_file_location(file_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        class_members = inspect.getmembers(module, inspect.isclass)

        for class_name, class_ in class_members:
            if class_name in SCANNERS:
                print(
                    f"Unable to add {class_name} from {path} "
                    "due to name conflict"
                )

            if issubclass(class_, BaseAntivirus):
                SCANNERS[class_name] = class_
    elif os.path.isdir(path):
        for de in os.scandir(path):
            add(de.path)
