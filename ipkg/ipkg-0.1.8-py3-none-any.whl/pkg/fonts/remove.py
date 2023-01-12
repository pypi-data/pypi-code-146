from pathlib import Path

import click

from ...utils.remove import remove
from ...utils.run import run
from . import FONT_DIR


@click.command()
@click.option("--font-dir", type=click.Path(), default=FONT_DIR)
def main(font_dir: str | Path) -> None:
    remove(path=font_dir)
    run("fc-cache", "--force")
