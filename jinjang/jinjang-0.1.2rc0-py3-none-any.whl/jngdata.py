#!/usr/bin/env python3

###
# This module manages the data that will be used to feed ne template.
###


from typing import Any, Iterator


import              contextlib
from io      import TextIOWrapper
from json    import load as json_load
import              os
from pathlib import Path
from runpy   import run_path
import              sys
from yaml    import safe_load as yaml_load


# ----------- #
# -- TOOLS -- #
# ----------- #

###
# prototype::
#     path : a path to be added temporarily to the system path.
#
#     :action: temporarily add ``path`` to the system path.
###
@contextlib.contextmanager
def addpath2sys(path: Path) -> Iterator[None]:
    path = os.fspath(str(path))

    try:
        sys.path.insert(0, path)
        yield

    finally:
        sys.path.remove(path)


# ---------------------------- #
# -- DATA TO FEED TEMPLATES -- #
# ---------------------------- #

JNGDATA_PYNAME = "JNGDATA"


###
# This class produces the internal version of data from different kinds
# of input.
###
class JNGData:
###
# prototype::
#     launch_py : the value ``True`` allows the execution of ¨python files
#                 to build data feeding a template.
#                 Otherwise, no ¨python script will be launched.
###
    def __init__(
        self,
        launch_py: bool
    ) -> None:
        self.launch_py = launch_py


###
# prototype::
#     data : data feeding a template.
#            If the type used is not a ¨python ¨dict, then this argument
#            will be transformed into a string in order to construct a path
#            used as the one of the data file.
#          @ type(data) != dict ==> exists path(str(data))
#
#     :return: a ¨python ¨dict of the data to feed a template (no chek done).
###
    def build(
        self,
        data: Any
    ) -> dict:
# Just one dictionary.
        if isinstance(data, dict):
            return data

# We need a path of one existing file.
        data = Path(str(data))

        if not data.is_file():
            raise IOError(
                f"missing file:\n{data}"
            )

# Do we manage this kind of file?
        ext = data.suffix[1:]

        try:
            builder = getattr(self, f"build_from{ext}")

        except:
            raise ValueError(
                f"no data builder for the extension {ext}."
            )

# Special case of the Python files.
        if ext == 'py':
            dictdata = builder(data)

# Other kind of files.
        else:
            with data.open(
                encoding = 'utf-8',
                mode     = "r",
            ) as f:
                dictdata = builder(f)

        return dictdata


###
# prototype::
#     file: the ``IO``-like contents of a ¨json file.
#
#     :return: :see: self.build
###
    def build_fromjson(
        self,
        file: TextIOWrapper
    ) -> dict:
        return json_load(file)


###
# prototype::
#     file: the ``IO``-like contents of a ¨yaml file.
#
#     :return: :see: self.build
###
    def build_fromyaml(
        self,
        file: TextIOWrapper
    ) -> dict:
        return yaml_load(file)


###
# prototype::
#     file: the path of a ¨python file.
#
#     :return: :see: self.build
###
    def build_frompy(
        self,
        file: Path
    ) -> dict:
# Are we allowed to launch a Python file?
        if not self.launch_py:
            raise Exception(
                "``launch_py`` disabled, no Python file can't "
                "be launched to build data."
            )

# Lets's launch the Python file, and then recover the expected value
# of the special variable.
#
# Suchas to allow relative imports inside a ``data.py`` file, we have
# to change ``sys.path`` temporarly.
        with addpath2sys(file.parent):
            dictdata = run_path(file)

# The special variable is missing.
        if not JNGDATA_PYNAME in dictdata:
            raise Exception(
                f"no ``{JNGDATA_PYNAME}`` variable found in the Python file :"
                 "\n"
                f"{file}"
            )

# The job has been done.
        return dictdata[JNGDATA_PYNAME]
