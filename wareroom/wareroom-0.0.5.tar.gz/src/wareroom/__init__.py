"""Cloud storage backends for Diligent."""

from .storage import Client

__all__ = ["Client"]
from . import _version

__version__ = _version.get_versions()['version']
