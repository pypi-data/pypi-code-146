import click
from ishutils import run


@click.command(name="npm")
def cmd() -> None:
    run("pnpm", "store", "prune")
