import click

from ..utils import execute


@click.command(name="npm")
def cmd() -> None:
    execute("pnpm", "store", "prune")
