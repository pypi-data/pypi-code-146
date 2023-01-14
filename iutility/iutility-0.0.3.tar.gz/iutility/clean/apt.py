import click
from ishutils import run


@click.command(name="apt")
def cmd() -> None:
    run("sudo", "apt", "autoremove")
    run("sudo", "apt-get", "autoclean")
