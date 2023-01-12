import os
from pathlib import Path

import click

from ...utils.download import download
from ...utils.ubuntu.desktop import DesktopEntry, make_desktop_file
from .. import OPT
from . import DOWNLOAD_URL, ICON_URL, NAME


@click.command()
def main() -> None:
    exec: Path = OPT / NAME / (NAME + ".AppImage")
    download(url=DOWNLOAD_URL, output=exec)
    os.chmod(path=exec, mode=0o775)
    icon_path: Path = OPT / NAME / "icon.png"
    download(url=ICON_URL, output=icon_path)
    make_desktop_file(
        slug=NAME,
        entry=DesktopEntry(Name="Motrix", Exec=str(exec), Icon=str(icon_path)),
    )
