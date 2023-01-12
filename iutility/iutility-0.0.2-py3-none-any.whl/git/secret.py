import subprocess

import click

from ..utils import execute


def set_pypi() -> None:
    pypi_token: str = str(
        execute("bw", "get", "notes", "PYPI_TOKEN", stdout=subprocess.PIPE).stdout,
        encoding="utf-8",
    ).strip()
    execute("gh", "secret", "set", "PYPI_TOKEN", "--body", pypi_token)


@click.command(name="secret")
@click.argument("name", type=click.Choice(choices=["pypi"]))
def cmd(name: str) -> None:
    if name == "pypi":
        set_pypi()
