import os
import shutil
from pathlib import Path
from stat import S_IRWXG, S_IRWXO, S_IRWXU
from zipfile import ZipFile, ZipInfo

from ..log import get_logger
from .confirm import confirm


class MyZipFile(ZipFile):
    def _extract_member(self, member: str | ZipInfo, target_path: str, pwd: str):
        if isinstance(member, ZipInfo):
            zipinfo = member
        else:
            zipinfo = self.getinfo(member)
        target_path = super()._extract_member(zipinfo, target_path, pwd)  # type: ignore
        attr = (zipinfo.external_attr >> 16) & (S_IRWXU | S_IRWXG | S_IRWXO)
        if attr != 0:
            os.chmod(target_path, attr)
        return target_path


def unzip(src: str | Path, dst: str | Path) -> None:
    with MyZipFile(file=src, mode="r") as zip_file:
        zip_file.extractall(path=dst)


shutil.unregister_unpack_format(name="zip")
shutil.register_unpack_format(name="zip", extensions=[".zip"], function=unzip)


def extract(
    src: str | Path, dst: str | Path, ask: bool = True, overwrite: bool = True
) -> None:
    logger = get_logger()
    dst = Path(dst)
    if dst.exists():
        if ask:
            overwrite = confirm(message=f"Extract: overwrite {dst}", default=overwrite)
        if not overwrite:
            logger.skipped(msg=f"Extract: {src} -> {dst}")
            return
    os.makedirs(name=dst.parent, exist_ok=True)
    shutil.unpack_archive(filename=src, extract_dir=dst)
    logger.success(msg=f"Extract: {src} -> {dst}")
