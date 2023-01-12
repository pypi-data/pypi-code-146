import os
import shutil
from pathlib import Path

from ..log import get_logger
from .confirm import confirm


def remove(path: str | Path, ask: bool = True, default: bool = True) -> None:
    logger = get_logger()
    path = Path(path)
    message = f"Remove: {path}"
    if path.is_file() or path.is_dir():
        if ask:
            default = confirm(message=message, default=default)
        if not default:
            logger.skipped(msg=message)
            return
        if path.is_file():
            os.remove(path=path)
        elif path.is_dir():
            shutil.rmtree(path=path)
        else:
            logger.skipped(msg=message)
            return
        logger.success(msg=message)
    else:
        logger.skipped(msg=message)
        return
