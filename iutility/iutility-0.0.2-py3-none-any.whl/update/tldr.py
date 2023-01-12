import click

from ..utils import execute


@click.command(name="tldr")
def cmd() -> None:
    execute("tldr", "--update")
