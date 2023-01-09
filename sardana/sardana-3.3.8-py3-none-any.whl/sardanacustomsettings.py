#!/usr/bin/env python

#############################################################################
##
# This file is part of Sardana
##
# http://www.sardana-controls.org/
##
# Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
##
# Taurus is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##
# Taurus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
##
# You should have received a copy of the GNU Lesser General Public License
# along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
##
#############################################################################

"""
This module contains some Sardana-wide default configurations. It declares the default
values of some of these options,  but they may be modified when loading custom
settings configuration files (e.g., at import time).
"""

import os as _os

if _os.name == "posix":
    #: Path to the system-wide config file
    SYSTEM_CFG_FILE = "/etc/sardana/sardana.ini"
    #: Path to the user-specific config file
    USER_CFG_FILE = _os.path.join(
        _os.path.expanduser("~"), ".sardana", "sardana.ini"
    )
else:
    #: Path to the system-wide config file
    SYSTEM_CFG_FILE = _os.path.join(
        _os.environ.get("PROGRAMDATA"), "sardana", "sardana.ini"
    )
    #: Path to the user-specific config file
    USER_CFG_FILE = _os.path.join(
        _os.environ.get("APPDATA"), "sardana", "sardana.ini"
    )


def load_configs(filenames=None, section="sardana"):
    """Read configuration key, values from given ini files and expose them as
    members of the current module.

    The keys must appear in the given section ("sardana" by default) and are
    case-sensitive. The values are interpreted as python literals.

    In case of conflicting keys, the filenames determine the precedence
    (increasing order). If a given file cannot be read, it is skipped. The
    list of names of successfully read files is returned.

    :param filenames: sequence of ini file names in increasing precedence
        order. If None passed (default), it uses
        `(SYSTEM_CFG_FILE, USER_CFG_FILE)`
    :type filenames: sequence of str
    :param section: section of the ini files to be read (default:`sardana`)
    :type section: str
    :returns: list of names of successfully read configuration files
    :rtype: list<str>
    """

    import configparser
    import ast

    if filenames is None:
        filenames = (SYSTEM_CFG_FILE, USER_CFG_FILE)

    parser = configparser.ConfigParser()
    parser.optionxform = lambda option: option  # make keys case-sensitive
    read = parser.read(filenames)

    try:
        sardana_cfg = parser[section]
    except KeyError:
        sardana_cfg = {}
    for k, v in sardana_cfg.items():
        globals()[k] = ast.literal_eval(v)
    return read


#: UnitTest door name: the door to be used by unit tests.
#: UNITTEST_DOOR_NAME must be defined for running sardana unittests.
UNITTEST_DOOR_NAME = "door/demo1/1"
#: UnitTests Pool DS name: Pool DS to use in unit tests.
UNITTEST_POOL_DS_NAME = "unittest1"
#: UnitTests Pool Device name: Pool Device to use in unit tests.
UNITTEST_POOL_NAME = "pool/demo1/1"

#: Size of rotating backups of the log files.
#: The Pool device server will use these values for its logs.
POOL_LOG_FILES_SIZE = 1e7
#: Size of rotating backups of the log files.
#: The MacroServer device server will use these values for its logs.
MS_LOG_FILES_SIZE = 1e7
#: Size of rotating backups of the log files.
#: The Sardana device server will use these values for its logs.
SARDANA_LOG_FILES_SIZE = 1e7

#: Number of rotating backups of the log files.
#: The Pool device server will use these values for its logs.
POOL_LOG_BCK_COUNT = 5
#: Number of rotating backups of the log files.
#: The MacroServer device server will use these values for its logs.
MS_LOG_BCK_COUNT = 5
#: Number of rotating backups of the log files.
#: The Sardana device server will use these values for its logs.
SARDANA_LOG_BCK_COUNT = 5

#: Input handler for spock interactive macros. Accepted values are:
#:
#: - "CLI": Input via spock command line. This is the default.
#: - "Qt": Input via Qt dialogs
SPOCK_INPUT_HANDLER = "CLI"

#: Use this map in order to avoid ambiguity with scan recorders (file) if
#: extension is intended to be the recorder selector.
#: Set it to a dict<str, str> where:
#:
#: - key   - scan file extension e.g. ".h5"
#: - value - recorder name
#:
#: The SCAN_RECORDER_MAP will make an union with the dynamically (created map
#: at the MacroServer startup) taking precedence in case the extensions repeats
#: in both of them.
SCAN_RECORDER_MAP = None

#: Filter for macro logging: name of the class to be used as filter
#: for the macro logging
#:
#: - if LOG_MACRO_FILTER is not defined no filter will be used
#: - if LOG_MACRO_FILTER is wrongly defined a user warning will be issued and
#:   no filter will be used
#: - if LOG_MACRO_FILTER is correctly defined but macro filter can not be
#:   initialized a user warning will be issued and no filter will be used
LOG_MACRO_FILTER = "sardana.macroserver.msmacromanager.LogMacroFilter"

# TODO: Temporary solution, available while Taurus3 is being supported.
# Maximum number of Taurus deprecation warnings allowed to be displayed.
TAURUS_MAX_DEPRECATION_COUNTS = 0

#: Type of encoding for ValueBuffer Tango attribute of experimental channels
VALUE_BUFFER_CODEC = "pickle"

#: Type of encoding for ValueRefBuffer Tango attribute of experimental
#: channels
VALUE_REF_BUFFER_CODEC = "pickle"

#: Database backend for MacroServer environment implemented using shelve.
#: Available options:
#:
#: - None (default) - first try "gnu" and if not available fallback to "dumb"
#: - "gnu" - better performance than dumb, but requires installation of
#:   additional package e.g. python3-gdbm on Debian. At the time of writing of
#:   this documentation it is not available for conda.
#: - "dumb" - worst performance but directly available with Python 3.
MS_ENV_SHELVE_BACKEND = None

#: macroexecutor maximum number of macros stored in the history.
#: Available options:
#:
#: - None (or no setting) - unlimited history (may slow down the GUI operation
#:   if grows too big)
#: - 0 - history will not be filled
#: - <int> - max number of macros stored in the history
MACROEXECUTOR_MAX_HISTORY = 100

#: pre-move and post-move hooks applied in simple mv-based macros
#: Available options:
#:
#: - True (or no setting) - macros which are hooked to the pre-move and
#:   post-move hook places are called before and/or after any move of a motor
#: - False - macros which are hooked to the pre-move and post-move hook
#:   places are not called in simple mv-based macros but only in scan-based
#:   macros
PRE_POST_MOVE_HOOK_IN_MV = True


#: Default SPEC recorder *custom data* format.
#: Custom data can be added using 
#: `DataHandler.addCustomData() <sardana.macroserver.scan.recorder.DataHandler.addCustomData>`
#: and this default format can be changed with
#: the ``spec_custom_fmt`` *kwarg* of this method.
#:
#: For backward compatibility change to: ``#C {name} : {value}\n``.
SPEC_CUSTOM_DATA_FORMAT = '#UVAR {name} {value}\n'

#: Duplicate the pre_scan_snapshot fields into the measurement collection
#: via SoftLinks for the NXscanH5_recorder#: Available options:
#:
#: - False (or no setting) - pre_scan_snapshot fields are not duplicated
#: - True - pre_scan_snapshot fields are duplicated into the measurement
#:   collection via SoftLinks
NXSCANH5_RECORDER_LINK_PRE_SCAN_SNAPSHOT = False


# Load the configuration from the ini files if they exist
load_configs()