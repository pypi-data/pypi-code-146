import platform
from pathlib import Path

import click

from ...utils.download import download
from ...utils.run import run
from .. import DOWNLOADS, SHELL
from . import DEFAULT_PREFIX, HELP_PREFIX

FILENAME = f"Miniconda3-latest-{platform.system()}-{platform.machine()}.sh"


@click.command(
    help="https://conda.io/projects/conda/en/latest/user-guide/install/macos.html"
)
@click.option(
    "-b",
    "--batch / --no-batch",
    default=True,
    is_flag=True,
    help="Batch mode with no PATH modifications to shell scripts. Assumes that you agree to the license agreement. Does not edit shell scripts such as .bashrc, .bash_profile, .zshrc, etc.",
)
@click.option(
    "-p",
    "--prefix",
    "--path",
    type=click.Path(),
    default=DEFAULT_PREFIX,
    help=HELP_PREFIX,
)
@click.option(
    "-f",
    "--force",
    default=False,
    is_flag=True,
    help="Force installation even if prefix -p already exists.",
)
def main(batch: bool, prefix: str | Path, force: bool) -> None:
    filepath = DOWNLOADS / FILENAME
    url = f"https://repo.anaconda.com/miniconda/{FILENAME}"
    download(url=url, output=filepath)
    args: list[str] = [str(SHELL), str(filepath)]
    if batch:
        args.append("-b")
    if prefix:
        args += ["-p", str(prefix)]
    if force:
        args.append("-f")
    run(*args)
