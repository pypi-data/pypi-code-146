import shutil
from pathlib import Path

from ..log import Action, get_logger


def move(src: str | Path, dst: str | Path) -> None:
    logger = get_logger()
    shutil.move(src=src, dst=dst)
    logger.success(action=Action.MOVE, message=f"{src} -> {dst}")
