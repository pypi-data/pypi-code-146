"""Algorithms for remote processing of data.

Federated algorithm plugins can also be imported from this package.
"""
import importlib as _importlib
import inspect as _inspect
import pkgutil as _pkgutil
from typing import List as _List

from bitfount.config import (
    BITFOUNT_FEDERATED_PLUGIN_PATH as _BITFOUNT_FEDERATED_PLUGIN_PATH,
)
import bitfount.federated.algorithms as algorithms
from bitfount.federated.algorithms.base import BaseAlgorithmFactory
import bitfount.federated.algorithms.model_algorithms as model_algorithms
from bitfount.federated.logging import _get_federated_logger
from bitfount.utils import _import_module_from_file

__all__: _List[str] = []

_logger = _get_federated_logger(__name__)


# Create `algorithms` plugin subdir if it doesn't exist
_algorithms_plugin_path = _BITFOUNT_FEDERATED_PLUGIN_PATH / "algorithms"
_algorithms_plugin_path.mkdir(parents=True, exist_ok=True)


# Import all concrete implementations of BaseAlgorithmFactory in the algorithms
# subdirectory as well as algorithms plugins

for _module_info in _pkgutil.walk_packages(
    path=algorithms.__path__
    + model_algorithms.__path__
    + [str(_BITFOUNT_FEDERATED_PLUGIN_PATH / "algorithms")],
):
    if _module_info.ispkg:
        continue

    try:
        _module = _importlib.import_module(f"{algorithms.__name__}.{_module_info.name}")

    # Try to import the module from the model_algorithms directory if it's not found in
    # the algorithms directory
    except ImportError:
        try:
            _module = _importlib.import_module(
                f"{model_algorithms.__name__}.{_module_info.name}"
            )
        # Try to import the module from the plugin directory if it's not found in the
        # algorithms or model_algorithms directories
        except ImportError:
            try:
                _module, _module_local_name = _import_module_from_file(
                    _BITFOUNT_FEDERATED_PLUGIN_PATH
                    / "algorithms"
                    / f"{_module_info.name}.py",
                    parent_module=__package__,
                )
                # Adding the module to the algorithms package so that it can be imported
                globals().update({_module_local_name: _module})
                _logger.info(
                    f"Imported algorithm plugin {_module_info.name}"
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
        if issubclass(cls, BaseAlgorithmFactory) and not _inspect.isabstract(cls):
            # Adding the class to the algorithms package so that it can be imported
            # as well as to the __all__ list so that it can be imported from bitfount
            # directly
            found_factory = True
            globals().update({cls.__name__: getattr(_module, cls.__name__)})
            __all__.append(cls.__name__)
        # There are too many false positives if we don't restrict classes to those
        # that inherit from BaseAlgorithmFactory for it to be a useful log message
        elif (
            issubclass(cls, BaseAlgorithmFactory)
            and cls.__name__ != "BaseAlgorithmFactory"
        ):
            found_factory = True
            _logger.warning(
                f"Found class {cls.__name__} in module {_module_info.name} which "
                f"did not fully implement BaseAlgorithmFactory. Skipping."
            )
        elif _module_info.name == "base" and cls.__name__ == "BaseAlgorithmFactory":
            # We don't want to log this because it's expected
            found_factory = True

    if not found_factory:
        _logger.warning(
            f"{_module_info.name} did not contain a subclass of BaseAlgorithmFactory."
        )
