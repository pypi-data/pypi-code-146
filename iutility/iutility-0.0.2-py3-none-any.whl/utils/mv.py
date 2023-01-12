import shutil
from pathlib import Path

from ..logger import get_logger


def move(src: str | Path, dst: str | Path) -> None:
    logger = get_logger()
    shutil.move(src=src, dst=dst)
    logger.success(msg=f"Move: {src} -> {dst}")
