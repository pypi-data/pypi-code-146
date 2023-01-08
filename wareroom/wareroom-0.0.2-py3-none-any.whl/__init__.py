"""Cloud storage backends for Diligent."""

from .obs import Client, read_config

__all__ = ["Client", "read_config"]
from . import _version
__version__ = _version.get_versions()['version']
