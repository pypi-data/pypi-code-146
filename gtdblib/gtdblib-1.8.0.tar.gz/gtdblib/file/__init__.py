from pathlib import Path

from gtdblib.exception import GtdbLibException


class File:
    """The base class that all files inherit from."""

    __slots__ = ('path',)

    def __init__(self, path: Path):
        # Validate arguments
        if not isinstance(path, Path):
            raise GtdbLibException("path must be a pathlib.Path object")
        if path.is_dir():
            raise GtdbLibException(f"path must be a file, not a directory: {path}")

        self.path: Path = path
