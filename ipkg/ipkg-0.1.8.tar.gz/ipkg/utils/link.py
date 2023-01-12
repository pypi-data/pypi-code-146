import os
from pathlib import Path

from ..log import get_logger
from .remove import remove


def link(src: str | Path, dst: str | Path) -> None:
    logger = get_logger()
    src = Path(src)
    dst = Path(dst)
    if dst.exists():
        remove(path=dst)
    os.symlink(src=src, dst=dst, target_is_directory=src.is_dir())
    logger.success(msg=f"Link: {src} <- {dst}")
