from __future__ import annotations

try:
    import importlib.metadata

    __version__ = importlib.metadata.version(__package__ or __name__)
except ImportError:
    __version__ = "__version__ is set using importlib.metadata which is part of the " \
                  "standard library since python 3.8"

from .datasets import load_data
from .plotto import mark_plot
