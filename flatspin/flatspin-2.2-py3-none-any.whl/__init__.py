from setuptools_scm import get_version
try:
    # If flatspin source is a git repo, try to determine version at runtime
    __version__ = get_version()
except LookupError:
    # Fall back to version detected at package installation time
    from ._version import version as __version__

from .model import *
from .data import Dataset
from .grid import Grid
