import click

from ...utils.remove import remove
from ...utils.ubuntu.desktop import DESKTOP_FILE_INSTALL_DIR
from .. import OPT
from . import NAME


@click.command()
def main() -> None:
    remove(path=OPT / NAME)
    remove(path=DESKTOP_FILE_INSTALL_DIR / (NAME + ".desktop"))
