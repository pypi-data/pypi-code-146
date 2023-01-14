import click
from ishutils import run


@click.command(name="pip")
def cmd() -> None:
    run("conda", "clean", "--all")
    run("pip", "cache", "purge")
