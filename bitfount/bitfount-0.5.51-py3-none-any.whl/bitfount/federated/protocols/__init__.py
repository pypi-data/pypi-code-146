"""Protocols for inter-machine communication.

Federated protocol plugins can also be imported from this package.
"""
import importlib as _importlib
import inspect as _inspect
import pkgutil as _pkgutil
from typing import List as _List

from bitfount.config import (
    BITFOUNT_FEDERATED_PLUGIN_PATH as _BITFOUNT_FEDERATED_PLUGIN_PATH,
)
from bitfount.federated.logging import _get_federated_logger
import bitfount.federated.protocols as protocols
from bitfount.federated.protocols.base import BaseProtocolFactory
import bitfount.federated.protocols.model_protocols as model_protocols
from bitfount.utils import _import_module_from_file

__all__: _List[str] = ["BaseProtocolFactory"]

_logger = _get_federated_logger(__name__)


# Create `protocols` plugin subdir if it doesn't exist
_protocols_plugin_path = _BITFOUNT_FEDERATED_PLUGIN_PATH / "protocols"
_protocols_plugin_path.mkdir(parents=True, exist_ok=True)


# Import all concrete implementations of BaseProtocolFactory in the protocols
# subdirectory as well as protocols plugins

for _module_info in _pkgutil.walk_packages(
    path=protocols.__path__
    + model_protocols.__path__
    + [str(_BITFOUNT_FEDERATED_PLUGIN_PATH / "protocols")],
):
    if _module_info.ispkg:
        continue

    try:
        _module = _importlib.import_module(f"{protocols.__name__}.{_module_info.name}")

    # Try to import the module from the model_protocols directory if it's not found in
    # the protocols directory
    except ImportError:
        try:
            _module = _importlib.import_module(
                f"{model_protocols.__name__}.{_module_info.name}"
            )
        # Try to import the module from the plugin directory if it's not found in the
        # protocols or model_protocols directories
        except ImportError:
            try:
                _module, _module_local_name = _import_module_from_file(
                    _BITFOUNT_FEDERATED_PLUGIN_PATH
                    / "protocols"
                    / f"{_module_info.name}.py",
                    parent_module=__package__,
                )
                # Adding the module to the protocols package so that it can be imported
                globals().update({_module_local_name: _module})
                _logger.info(
                    f"Imported protocol plugin {_module_info.name}"
                    f" as {_module.__name__}"
                )
            except ImportError as ex:
                _logger.error(
                    f"Error importing module {_module_info.name}"
                    f" under {__name__}: {str(ex)}"
                )
                _logger.debug(ex, exc_info=True)
                continue

    found_factory = False
    for _, cls in _inspect.getmembers(_module, _inspect.isclass):
        if issubclass(cls, BaseProtocolFactory) and not _inspect.isabstract(cls):
            # Adding the class to the protocols package so that it can be imported
            # as well as to the __all__ list so that it can be imported from bitfount
            # directly
            found_factory = True
            globals().update({cls.__name__: getattr(_module, cls.__name__)})
            __all__.append(cls.__name__)
        # There are too many false positives if we don't restrict classes to those
        # that inherit from BaseProtocolFactory for it to be a useful log message
        elif (
            issubclass(cls, BaseProtocolFactory)
            and cls.__name__ != "BaseProtocolFactory"
        ):
            found_factory = True
            _logger.warning(
                f"Found class {cls.__name__} in module {_module_info.name} which "
                f"did not fully implement BaseProtocolFactory. Skipping."
            )
        elif _module_info.name == "base" and cls.__name__ == "BaseProtocolFactory":
            # We don't want to log this because it's expected
            found_factory = True

    if not found_factory:
        _logger.warning(
            f"{_module_info.name} did not contain a subclass of BaseProtocolFactory."
        )
