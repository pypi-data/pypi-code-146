import importlib
from typing import Any

from bitorch_engine.extensions import EXTENSION_PREFIX

MESSAGE = """The extension '{}' could not be imported. It is either not yet implemented or was not build correctly.
This message is expected during the build process. If it appears later on, try installing the package again."""


class ExtensionModulePlaceholder:
    def __init__(self, name: str) -> None:
        self._name = name

    def __getattr__(self, item: str) -> Any:
        raise RuntimeError(MESSAGE.format(self._name))

    def __setattr__(self, key: Any, value: Any) -> None:
        if key == "_name":
            self.__dict__["_name"] = value
            return
        raise RuntimeError(MESSAGE.format(self._name))


def import_extension(module_name: str, not_yet_implemented: bool = False) -> Any:
    """
    For importing extension modules safely.

    Usage: binary_linear_cuda = import_extension_safely("binary_linear_cuda")
    """
    if not_yet_implemented:
        return ExtensionModulePlaceholder(module_name)

    try:
        return importlib.import_module(EXTENSION_PREFIX + module_name)
    except ModuleNotFoundError:
        print("Warning:", MESSAGE.format(module_name))
        return ExtensionModulePlaceholder(module_name)
