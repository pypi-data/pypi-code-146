"""Cloud storage backends for Diligent."""

from .obs import Client

__all__ = ["Client"]
from . import _version

__version__ = _version.get_versions()['version']
