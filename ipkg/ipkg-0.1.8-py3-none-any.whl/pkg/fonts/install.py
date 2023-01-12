import typing
from pathlib import Path

import click
import requests

from ...utils.download import download
from ...utils.extract import extract
from ...utils.run import run
from .. import DOWNLOADS
from . import FONT_DIR


def install_meslolgs_nf(font_dir: str | Path) -> None:
    FONT_NAME = "MesloLGS NF"
    STYLES = ["Regular", "Bold", "Italic", "Bold Italic"]
    font_dir = Path(font_dir)
    for style in STYLES:
        filename = f"{FONT_NAME} {style}.ttf"
        filepath = font_dir / FONT_NAME / filename
        url = f"https://github.com/romkatv/powerlevel10k-media/raw/master/{filename}"
        download(url=url, output=filepath)


def install_fira_code(
    font_dir: str | Path, version: typing.Optional[str] = None
) -> None:
    FONT_NAME = "Fira_Code"
    font_dir = Path(font_dir)
    if not version:
        res = requests.get(
            url="https://api.github.com/repos/tonsky/FiraCode/releases/latest"
        ).json()
        version = res["name"]
    filename = f"{FONT_NAME}_v{version}.zip"
    url = f"https://github.com/tonsky/FiraCode/releases/download/{version}/{filename}"
    filepath = DOWNLOADS / filename
    download(url=url, output=filepath)
    extract(src=filepath, dst=font_dir / FONT_NAME)


def install_noto_sans_cjk_sc(font_dir: str | Path) -> None:
    FONT_NAME = "08_NotoSansCJKsc"
    font_dir = Path(font_dir)
    filename = f"{FONT_NAME}.zip"
    filepath = DOWNLOADS / filename
    url = f"https://mirrors.tuna.tsinghua.edu.cn/github-release/googlefonts/noto-cjk/LatestRelease/{filename}"
    download(url=url, output=filepath)
    extract(src=filepath, dst=font_dir / FONT_NAME)


@click.command()
@click.option("--font-dir", type=click.Path(), default=FONT_DIR)
def main(font_dir: str | Path) -> None:
    install_meslolgs_nf(font_dir=font_dir)
    install_fira_code(font_dir=font_dir)
    install_noto_sans_cjk_sc(font_dir=font_dir)
    run("fc-cache", "--force")
