import pkg_resources  # part of setuptools

from .main import *
from .analyse import *
from .generate import *
from .plotting import *

__version__ = pkg_resources.require("orientationpy")[0].version
