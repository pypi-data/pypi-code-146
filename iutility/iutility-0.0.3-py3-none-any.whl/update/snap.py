import click
from ishutils import run


@click.command(name="snap")
def cmd() -> None:
    run("sudo", "snap", "refresh")
