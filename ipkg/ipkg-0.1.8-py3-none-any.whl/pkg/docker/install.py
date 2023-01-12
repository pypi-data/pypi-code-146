from pathlib import Path

import click

from ...utils.download import download
from ...utils.run import run
from .. import DOWNLOADS
from . import GET_DOCKER_URL


@click.command(
    help="https://docs.docker.com/engine/install/ubuntu/#install-using-the-convenience-script"
)
def main() -> None:
    url: str = GET_DOCKER_URL
    filename: str = "get-docker.sh"
    filepath: Path = DOWNLOADS / filename
    download(url=url, output=filepath)
    run("sudo", "bash", str(filepath))
    run("sudo", "apt", "install", "uidmap")
    run("dockerd-rootless-setuptool.sh", "install")
