"""
# Helper Functions
"""
from collections.abc import Iterable

from .settings import Settings


def chunks(data, size=Settings.chunk_size) -> Iterable:
    """
    Make chunks for filling data into DB.
    10000 is a good size if working with higher RAM.
    Choose around 1000 on local computer.
    """
    for i in range(0, len(data), size):
        yield data[i: i + size]
