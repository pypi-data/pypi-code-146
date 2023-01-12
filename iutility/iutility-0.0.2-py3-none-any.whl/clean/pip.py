import click

from ..utils import execute


@click.command(name="pip")
def cmd() -> None:
    execute("conda", "clean", "--all")
    execute("pip", "cache", "purge")
