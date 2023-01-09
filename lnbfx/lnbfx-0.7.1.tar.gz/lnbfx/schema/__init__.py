"""Schema.

Tables.

.. autosummary::
   :toctree: .

   Pipeline
   Run
   Bfxmeta
   DObjectBfxmeta

Dev tools.

.. autosummary::
   :toctree: .

   dev

"""
from .. import __version__ as _version

_schema_id = "tsds"
_name = "bfx"
_migration = "b93449654dce"
__version__ = _version

from . import dev
from ._core import Bfxmeta, DObjectBfxmeta, Pipeline, Run  # noqa
