"""
Urban Intelligence's collection of Python code for everyday use
"""

import os, json
_config_path = os.path.expanduser("~/.ui/config")

def reset(force=False, verbose=True):
    """
    Complete all necessary installations, including matplotlib stylesheets and Rubik fonts, onto this machine. To revert stylesheets back to default (in case they were manually edited) and revert fonts, use force=True. To re-create the configuration file, please delete the configuration file and run 'import ui'.
    """
    import uintel.install
    uintel.install._create_config_file()
    uintel.install._install_styles(force, verbose)
    uintel.install._install_fonts(force, verbose)

reset()

config = json.load(open(_config_path, "r"))

import uintel.aws as aws
import uintel.colours as colours
import uintel.esri as esri
import uintel.geometry as geometry
import uintel.server as server
import uintel.slack as slack
import uintel.sql as sql
import uintel.zonal_statistics as zonal_statistics
__all__ = ["aws", "colours", "esri", "geometry", "server", "slack", "sql", "zonal_statistics"]
