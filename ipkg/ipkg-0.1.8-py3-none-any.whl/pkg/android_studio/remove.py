from pathlib import Path

import click

from ...utils.remove import remove
from ...utils.ubuntu.desktop import DESKTOP_FILE_INSTALL_DIR
from .. import OPT
from . import NAME


@click.command()
def main() -> None:
    for path in DESKTOP_FILE_INSTALL_DIR.glob(pattern="*android-studio*"):
        remove(path=path)
    remove(path=OPT / NAME)
    for path in Path.home().glob(pattern="*[aA]ndroid*"):
        remove(path=path)
