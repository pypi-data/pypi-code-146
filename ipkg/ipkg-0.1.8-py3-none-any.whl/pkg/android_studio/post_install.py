from pathlib import Path

import click

from ...utils.link import link
from .. import BIN


@click.command()
def main() -> None:
    link(
        src=Path.home() / "Android" / "Sdk" / "platform-tools" / "adb", dst=BIN / "adb"
    )
