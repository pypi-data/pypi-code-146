import click

from ...utils.run import run


@click.command()
def main() -> None:
    run("gh", "auth", "login")
    run("gh", "auth", "setup-git")
