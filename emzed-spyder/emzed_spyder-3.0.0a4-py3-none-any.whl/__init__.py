import os
import sys

import pkg_resources

__version__ = pkg_resources.require(__package__)[0].version

os.environ["QT_API"] = "pyqt5"

if sys.platform == "darwin":
    # https://sissource.ethz.ch/sispub/emzed/emzed-spyder/-/issues/23
    os.environ["QT_MAC_WANTS_LAYER"] = "1"
