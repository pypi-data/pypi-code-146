# This file is part of emzed (https://emzed.ethz.ch), a software toolbox for analysing
# LCMS data with Python.
#
# Copyright (C) 2020 ETH Zurich, SIS ID.
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.


if True:  # avoids resorting by Isort, if we change order we run into circulare imports:
    import sys as _sys

    if _sys.platform == "linux":
        # importing matplotlib crashes on linux, this hack avoids this:
        import ctypes

        try:
            _dll = ctypes.CDLL("libgcc_s.so.1")
        except OSError:
            pass
    elif _sys.platform == "win32":
        import matplotlib
        # tkinter is missing on some windows Python distributions
        matplotlib.use("agg")


import pkg_resources as _pkg_resources  # noqa: F401

# disable isort, import order matters to avoid cirular imports below
# isort: off

# next module has top level code which imports pyopenms including some fixes /
# preparations because of linkage issues:
from .pyopenms import pyopenms  # noqa: F401
from . import ms_data as _msdata  # noqa: F401
from . import quantification  # noqa F401
from .peak_picking import run_feature_finder_metabo  # noqa: F401
from .peak_picking import run_feature_finder_metabo_on_folder  # noqa: F401
from .table import Table, to_table  # noqa F401
from .table.table_utils import MzType, RtType  # noqa F401

PeakMap = _msdata.PeakMap
Spectrum = _msdata.Spectrum

from . import align  # noqa: F401,E402
from . import io  # noqa: F401,E402
from .chemistry import abundance, adducts, elements, mass  # noqa: F401,E402
from .chemistry import MolecularFormula as mf  # noqa: F401,E402
from . import chemistry  # noqa: F401,E402
from . import db  # noqa: F401,E402
from . import gui  # noqa: F401,E402
from . import ext  # noqa: F401,E402
from . import targeted  # noqa: F401,E402
from . import ms2  # noqa: F401,E402
from . import annotate  # noqa: F401,E402

# isort: on


def __dir__():
    return [
        "MzType",
        "PeakMap",
        "RtType",
        "Spectrum",
        "Table",
        "abundance",
        "adducts",
        "annotate",
        "align",
        "chemistry",
        "db",
        "elements",
        "ext",
        "gui",
        "io",
        "mass",
        "mf",
        "ms2",
        "quantification",
        "run_feature_finder_metabo",
        "run_feature_finder_metabo_on_folder",
        "targeted",
        "to_table",
    ]


try:
    profile
except NameError:
    __builtins__["profile"] = lambda x: x


if _sys.platform == "win32":
    from .check_pyopenms import check_pyopenms_win32 as _check

    _check
    del check_pyopenms


elif _sys.platform == "linux":
    from .check_pyopenms import check_pyopenms_linux as _check

    _check
    del check_pyopenms


__version__ = _pkg_resources.require("emzed")[0].version

__all__ = __dir__()
