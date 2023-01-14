import glob

import click
from ishutils import remove


@click.command(name="tmp")
def cmd() -> None:
    for path in glob.glob(pathname="/tmp/*"):
        try:
            remove(path=path, confirm=False)
        except PermissionError as e:
            pass
