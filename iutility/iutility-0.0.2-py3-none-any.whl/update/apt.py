import click

from ..utils import execute


@click.command(name="apt")
def cmd() -> None:
    execute("sudo", "apt", "update")
    execute("sudo", "apt", "full-upgrade")
