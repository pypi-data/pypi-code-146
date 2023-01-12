import os
import shutil
from pathlib import Path

from ..log import get_logger


def copy(src: str | Path, dst: str | Path) -> None:
    logger = get_logger()
    src = Path(src)
    dst = Path(dst)
    os.makedirs(dst.parent, exist_ok=True)
    if src.is_file():
        shutil.copy2(src=src, dst=dst)
    elif src.is_dir():
        shutil.copytree(src=src, dst=dst)
    else:
        raise FileNotFoundError(src)
    logger.success(f"Copy: {src} -> {dst}")
