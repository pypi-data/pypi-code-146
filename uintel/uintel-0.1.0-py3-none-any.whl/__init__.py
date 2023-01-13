"""
Urban Intelligence's collection of Python code for everyday use
"""

import uintel.install as _install

def reset_fonts():
    """
    Force re-install all fonts, in case at least one was modified or deleted from this computer
    """
    _install._install_fonts(force=True, verbose=True)

def reset_styles():
    """
    Force re-install all matplotlib styles, in case at least one was modified or deleted from this computer
    """
    _install._install_styles(force=True, verbose=True)

def reset_config():
    """
    Force re-make the configuration file, in case at least one saved bit of information needs updating
    """
    _install._create_config_file()

_install._update_config_file()
_install._install_styles(force=False, verbose=True)
_install._install_fonts(force=False, verbose=True)
config = _install._get_config()

import uintel.aws as aws
import uintel.esri as esri
import uintel.geometry as geometry
import uintel.plot as plot
import uintel.server as server
import uintel.slack as slack
import uintel.sql as sql
__all__ = ["aws", "esri", "geometry", "plot", "server", "slack", "sql"]