"""Manage bioinformatics pipelines.

Import the package::

   import lnbfx

This is the complete API reference:

.. autosummary::
   :toctree: .

   BfxRun
   schema
   datasets
   dev
"""

__version__ = "0.7.1"

from . import datasets, dev, schema
from ._core import BfxRun
from ._lookup import lookup
