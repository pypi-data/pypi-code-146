import os
import shutil
from pathlib import Path

from ..log import Action, get_logger
from .confirm import confirm as _confirm


def remove(path: str | Path, confirm: bool = True, default: bool = True) -> None:
    logger = get_logger()
    path = Path(path)
    if path.is_file() or path.is_dir():
        if confirm:
            default = _confirm(message=f"Remove: {path}", default=default)
        if not default:
            logger.skipped(action=Action.REMOVE, message=str(path))
            return
        if path.is_file():
            os.remove(path=path)
        elif path.is_dir():
            shutil.rmtree(path=path)
        else:
            logger.skipped(action=Action.REMOVE, message=str(path))
            return
        logger.success(action=Action.REMOVE, message=str(path))
    else:
        logger.skipped(action=Action.REMOVE, message=str(path))
        return
