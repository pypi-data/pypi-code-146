import click
from ishutils import run


@click.command(name="brew")
def cmd() -> None:
    run("brew", "autoremove")
    run("brew", "cleanup")
