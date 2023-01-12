import os
import typing
from pathlib import Path

from httpie.core import main

from ..logger import get_logger
from . import confirm


def download(
    url: str, output: str | Path, ask: bool = True, overwrite: bool = False
) -> None:
    logger = get_logger()
    output = Path(output)
    if output.exists():
        if ask:
            overwrite = confirm(
                message=f"Download: overwrite {output}", default=overwrite
            )
        if not overwrite:
            logger.skipped(f"Download: {url} -> {output}")
            return
    os.makedirs(name=output.parent, exist_ok=True)
    main(args=["https", "--body", "--output", str(output), "--download", url])
    logger.success(msg=f"Download: {url} -> {output}")
