import os
import tempfile
from pathlib import Path

import click

from ...utils.download import download
from ...utils.extract import extract
from ...utils.remove import remove
from ...utils.replace import replace
from .. import BIN, DOWNLOADS
from . import NAME


@click.command(help="https://github.com/libthu/reserves-lib-tsinghua-downloader")
def main():
    filename: str = "downloader-ubuntu-latest-py3.9.zip"
    filepath: Path = DOWNLOADS / filename
    download(
        url="https://github.com/libthu/reserves-lib-tsinghua-downloader/releases/latest/download/downloader-ubuntu-latest-py3.9.zip",
        output=filepath,
    )
    tmpdir: Path = Path(tempfile.mkdtemp())
    extract(src=filepath, dst=tmpdir)
    replace(src=tmpdir / "downloader", dst=BIN / NAME)
    mode = os.stat(path=BIN / NAME).st_mode
    mode |= (mode & 0o444) >> 2
    exec: Path = BIN / NAME
    exec.chmod(mode=mode)
    remove(tmpdir)
