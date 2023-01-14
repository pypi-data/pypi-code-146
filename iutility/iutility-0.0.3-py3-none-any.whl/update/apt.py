import click
from ishutils import run


@click.command(name="apt")
def cmd() -> None:
    run("sudo", "apt", "update")
    run("sudo", "apt", "full-upgrade")
