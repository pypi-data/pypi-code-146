import click

from ..utils import execute


@click.command(name="apt")
def cmd() -> None:
    execute("sudo", "apt", "autoremove")
    execute("sudo", "apt-get", "autoclean")
