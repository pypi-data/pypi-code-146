"""Diligent module."""

from .cli import cli
from .storage import Client

__all__ = ["Client", "cli"]


from . import _version
__version__ = _version.get_versions()['version']
