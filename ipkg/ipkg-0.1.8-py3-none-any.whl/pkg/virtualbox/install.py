from pathlib import Path

import click

from ...utils.download import download
from ...utils.run import run
from .. import DOWNLOADS
from . import KEY_NAME, KEY_URL


@click.command(help="https://www.virtualbox.org/wiki/Linux_Downloads")
def main() -> None:
    key_path: Path = DOWNLOADS / KEY_NAME
    download(url=KEY_URL, output=key_path)
    run(
        "sudo",
        "gpg",
        "--dearmor",
        "--output",
        "/etc/apt/trusted.gpg.d/oracle-virtualbox-2016.gpg",
        str(key_path),
    )
    codename: str = str(
        run("lsb_release", "--codename", "--short", capture_output=True).stdout,
        encoding="utf-8",
    ).strip()
    sources_list: str = (
        f"deb https://download.virtualbox.org/virtualbox/debian {codename} contrib"
    )
    run(
        "sudo",
        "bash",
        "-c",
        f'echo "{sources_list}" > /etc/apt/sources.list.d/virtualbox.list',
    )
    run("sudo", "apt", "update")
    run("sudo", "apt", "install", "virtualbox-6.1")
