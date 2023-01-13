import logging
import sys
import importlib
from pathlib import Path
from typing import Union

from powerstrip.exceptions import ModuleException
from powerstrip.utils.utils import ensure_path


# prepare logger
log = logging.getLogger(__name__)


def load_module(module_name: str, path: Union[str, Path]):
    """
    load module by name from given directory

    :param module_name: name of the module
    :type module_name: str
    :param path: complete path of the python file
    :type path: Union[str, Path]
    :raises ModuleException: if file does not exist or module cannot be loaded
    """
    assert isinstance(module_name, str)
    assert isinstance(path, (str, Path))

    # ensure that directory is a Path
    path = ensure_path(path)
    if not path.exists():
        # not a path
        raise ModuleException(
            f"The file '{path}' does not exist! Abort."
        )

    # get modules spec
    log.debug(
        f"getting specs for module '{module_name}' in "
        f"'{path.as_posix()}'..."
    )
    spec = importlib.util.spec_from_file_location(
        name=module_name, location=path.as_posix()
    )
    if spec is None:
        # spec not found
        raise ModuleException(
            f"Could not get specs for module '{module_name}' "
            f"in file '{path}'! Abort."
        )

    if spec.name not in sys.modules:
        # get module from spec, if not yet loaded
        log.debug(f"getting module for spec '{spec.name}'...")
        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod

        # load the module
        log.debug(f"loading module '{spec.name}'...")
        spec.loader.exec_module(mod)
