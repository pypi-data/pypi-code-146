from pathlib import Path

from .cp import copy
from .remove import remove


def replace(src: str | Path, dst: str | Path) -> None:
    remove(path=dst)
    copy(src=src, dst=dst)
