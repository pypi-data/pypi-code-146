import click

from ..utils import execute


@click.command(name="snap")
def cmd() -> None:
    execute("sudo", "snap", "refresh")
