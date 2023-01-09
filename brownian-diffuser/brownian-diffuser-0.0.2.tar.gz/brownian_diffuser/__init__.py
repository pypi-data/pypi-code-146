
__module_name__ = "__init__.py"
__doc__ = """__init__.py module"""
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu"])
__version__ = "0.0.2"


# -- import sub-modules: -----------------------------------------------------------------
from ._core import BrownianMotion, BrownianDiffuser, nn_int
from . import _core
