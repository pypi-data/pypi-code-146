import tempfile
from pathlib import Path

from .remove import remove


class TmpDir:
    tmp: Path

    def __init__(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())

    def __enter__(self) -> Path:
        return self.tmp

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        remove(self.tmp)
