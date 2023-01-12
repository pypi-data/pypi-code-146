import platform
import urllib.parse
from pathlib import Path

import click

from ...utils.download import download
from ...utils.extract import extract
from ...utils.link import link
from ...utils.remove import remove
from ...utils.replace import replace
from ...utils.run import run
from ...utils.ubuntu import DESKTOP_FILE_INSTALL_DIR
from .. import DOWNLOADS, OPT
from . import DOWNLOAD_URL, NAME


@click.command()
def main() -> None:
    query: dict[str, str] = {
        "channel": "release",
        "platform": f"{platform.system().lower()}-{platform.machine()}",
    }
    url: str = urllib.parse.urlunparse(
        urllib.parse.ParseResult(
            scheme=DOWNLOAD_URL.scheme,
            netloc=DOWNLOAD_URL.netloc,
            path=DOWNLOAD_URL.path,
            params="",
            query=urllib.parse.urlencode(query=query),
            fragment="",
        )
    )
    filename: str = f"{NAME}.tar.bz2"
    filepath: Path = DOWNLOADS / filename
    download(url=url, output=filepath)
    extract(src=filepath, dst=OPT)
    tmpdir: Path = OPT / f"{NAME.title()}_{query['platform']}"
    replace(src=tmpdir, dst=OPT / NAME)
    remove(path=tmpdir)
    run(str(OPT / NAME / "set_launcher_icon"))
    desktop_filename = f"{NAME}.desktop"
    link(
        src=OPT / NAME / desktop_filename,
        dst=DESKTOP_FILE_INSTALL_DIR / desktop_filename,
    )
