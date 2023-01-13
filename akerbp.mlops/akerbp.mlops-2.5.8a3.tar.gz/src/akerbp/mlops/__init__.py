from importlib.metadata import version
from importlib.metadata import PackageNotFoundError

try:
    __version__ = version("akerbp.mlops")
except PackageNotFoundError:
    __version__ = "unknown"
