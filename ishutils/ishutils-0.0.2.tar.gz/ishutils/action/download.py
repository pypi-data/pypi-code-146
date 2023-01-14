import os
from pathlib import Path

from httpie.core import main

from ..log import Action, get_logger
from .confirm import confirm as _confirm


def download(
    url: str, output: str | Path, confirm: bool = True, overwrite: bool = False
) -> None:
    logger = get_logger()
    output = Path(output)
    if output.exists():
        if confirm:
            overwrite = _confirm(
                message=f"Download: overwrite {output}", default=overwrite
            )
        if not overwrite:
            logger.skipped(action=Action.DOWNLOAD, message=f"{url} -> {output}")
            return
    os.makedirs(name=output.parent, exist_ok=True)
    main(args=["https", "--body", "--output", str(output), "--download", url])
    logger.success(action=Action.DOWNLOAD, message=f"{url} -> {output}")
