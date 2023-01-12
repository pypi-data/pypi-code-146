import click

from ...utils.remove import remove
from ...utils.ubuntu import DESKTOP_FILE_INSTALL_DIR
from .. import OPT
from . import NAME


@click.command()
def main() -> None:
    remove(OPT / NAME)
    remove(DESKTOP_FILE_INSTALL_DIR / f"{NAME}.desktop")
