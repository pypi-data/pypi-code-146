from norma2.__dependencies__ import dependencies
from norma2.__main__ import entrypoint
from norma2.__version__ import __version__
from norma2.main import main as norma2_main

version = __version__

__all__ = ["entrypoint", "norma2_main", "__version__", "dependencies"]
