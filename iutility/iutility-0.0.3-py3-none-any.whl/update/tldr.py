import click
from ishutils import run


@click.command(name="tldr")
def cmd() -> None:
    run("tldr", "--update")
