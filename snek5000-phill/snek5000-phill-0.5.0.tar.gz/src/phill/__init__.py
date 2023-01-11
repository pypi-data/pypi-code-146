"""
Python package for managing case files.


**Contents**

.. autosummary::
   :toctree:

   solver
   output
   templates

"""
from ._version import __version__  # noqa: F401
from .output import Output
from .solver import Simul

short_name = "phill"
__all__ = ["Simul", "Output", "short_name"]
