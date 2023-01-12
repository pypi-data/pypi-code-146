import glob

import click

from ..utils import remove


@click.command(name="tmp")
def cmd() -> None:
    for path in glob.glob(pathname="/tmp/*"):
        try:
            remove(path=path, ask=False)
        except PermissionError as e:
            pass
