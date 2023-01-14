import subprocess

import click
from ishutils import run


def set_pypi() -> None:
    pypi_token: str = str(
        run("bw", "get", "notes", "PYPI_TOKEN", stdout=subprocess.PIPE).stdout,
        encoding="utf-8",
    ).strip()
    run("gh", "secret", "set", "PYPI_TOKEN", "--body", pypi_token)


@click.command(name="secret")
@click.argument("name", type=click.Choice(choices=["pypi"]))
def cmd(name: str) -> None:
    if name == "pypi":
        set_pypi()
