"""
A package for computing Fabry-Perot optical cavity parameters.

The main port-of-call, for interacting with cavcalc, should be via the
recommended "single-function interface" :func:`.calculate`. See
:ref:`module` for in-depth details on using cavcalc programmatically.
"""

import configparser as _configparser
import os as _os
import shutil as _shutil
import warnings as _warnings

try:
    from .__version__ import __version__
except ImportError:
    __version__ = "?.?.?"


import pint as _pint


ureg = _pint.UnitRegistry(cache_folder=":auto:")
_pint.set_application_registry(ureg)  # ensure compatibility when pickling / unpickling data
Q_ = ureg.Quantity

# Construct the session singleton, holding environment information
from ._session import _CavCalcSession

_SESSION = _CavCalcSession()


_HERE = _os.path.dirname(_os.path.realpath(__file__))


def _get_usr_config_dir():
    return _os.path.join(
        _os.environ.get("APPDATA")
        or _os.environ.get("XDG_CONFIG_HOME", _os.path.expanduser("~/.config")),
        "cavcalc",
    )


def _write_config_file():
    from ._exiters import quit_print as _quit_print

    usr_conf_path = _get_usr_config_dir()
    _os.makedirs(usr_conf_path, exist_ok=True)

    package_conf_file = _os.path.join(_HERE, "cavcalc.ini")
    if not _os.path.exists(package_conf_file):
        _quit_print(
            f"No 'cavcalc.ini' file present in the package install directory: {_HERE}. "
            "\n\nTry re-installing cavcalc, and file a bug report if this does not work."
        )

    usr_conf_file = _os.path.join(usr_conf_path, "cavcalc.ini")
    if not _os.path.isfile(usr_conf_file):
        _shutil.copyfile(package_conf_file, usr_conf_file)


def _read_config_file():
    from ._exiters import quit_print as _quit_print

    config = _configparser.ConfigParser()

    # Read in order (if they exist):
    #    1. package config file
    #    2. user .config directory file
    #    3. current directory file
    # with options from later successfully read files taking priority.
    read_files = config.read(
        tuple(_os.path.join(d, "cavcalc.ini") for d in (_HERE, _get_usr_config_dir(), ""))
    )
    if not read_files:
        _quit_print("Unable to read any 'cavcalc.ini' config files!")

    return config


def _process_config(config: _configparser.ConfigParser):
    from ._exiters import quit_print as _quit_print

    if "plotting" not in config:
        _warnings.warn(
            "No [plotting] section in any loaded cavcalc config file. This may lead to errors."
        )

    if "units" not in config:
        _quit_print(f"No [units] section present in any loaded cavcalc config file.")

    parents_map = {
        "div": "Angles",
        "w": "Beamsizes",
        "w1": "Beamsizes",
        "w2": "Beamsizes",
        "w0": "Beamsizes",
        "Rc": "RoCs",
        "Rc1": "RoCs",
        "Rc2": "RoCs",
        "L": "Distances",
        "z0": "Distances",
        "FSR": "Frequencies",
        "FWHM": "Frequencies",
        "modesep": "Frequencies",
        "pole": "Frequencies",
        "gouy": "Phases",
        "wl": "Waves",
    }

    units_sec = config["units"]

    # Ensure each parameter, which does *not* have a units override
    # specified, inherits units from its corresponding parent category
    for param, parent in parents_map.items():
        if not units_sec.get(param):
            parent_units = units_sec.get(parent)
            if not parent_units:
                _quit_print(
                    f"No units specified in category '{parent.capitalize()}' for "
                    "any loaded cavcalc config file."
                )

            units_sec[param] = parent_units


_write_config_file()
_CONFIG = _read_config_file()
_process_config(_CONFIG)


from .calculate import calculate
from .env import configure
from .output import load
from .parameters import ParameterType, get_default_units
