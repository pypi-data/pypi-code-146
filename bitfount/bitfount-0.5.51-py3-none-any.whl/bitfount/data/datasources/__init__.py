"""Modules for data sources.

Datasource plugins can also be imported from this package.
"""
import logging as _logging
import pkgutil as _pkgutil

from bitfount.config import BITFOUNT_PLUGIN_PATH as _BITFOUNT_PLUGIN_PATH
from bitfount.utils import _import_module_from_file

_logger = _logging.getLogger(__name__)

# Create `datasources` plugin subdir if it doesn't exist
_datasource_plugin_path = _BITFOUNT_PLUGIN_PATH / "datasources"
_datasource_plugin_path.mkdir(parents=True, exist_ok=True)

# Add datasource plugin modules to the `datasources` namespace alongside the existing
# built-in datasource modules. This is not essential, but it allows users to import
# the entire plugin module as opposed to just the Datasource class which is what is done
# in the `bitfount.data` __init__ module.
for _module_info in _pkgutil.walk_packages(
    [str(_datasource_plugin_path)],
):
    try:
        _module, _module_local_name = _import_module_from_file(
            _datasource_plugin_path / f"{_module_info.name}.py",
            parent_module=__package__,
        )
        globals().update({_module_local_name: _module})
        _logger.info(
            f"Imported datasource plugin {_module_info.name} as {_module.__name__}"
        )
    except ImportError as ex:
        # This is deliberately at DEBUG as we don't care about this being exposed
        # to the user at this level but would be good to mark the failure somewhere.
        _logger.debug(
            f"Error importing datasource plugin {_module_info.name}"
            f" under {__name__}: {str(ex)}"
        )
        _logger.debug(ex, exc_info=True)
