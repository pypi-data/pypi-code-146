from __future__ import annotations

import os
import shutil
from functools import lru_cache
from pathlib import Path

from platformdirs import user_cache_dir

from blx.cid import CID
from blx.digest import digest

from .meta import __author__, __name__

__all__ = ["cache"]


def filepath(cid: CID):
    return get_cache_dir() / cid.hex()


class Cache:
    def put(self, cid: CID, file: Path):
        if not self.has(cid):
            shutil.copyfile(file, filepath(cid))

        self.check(cid)

    def get(self, cid: CID):
        self.check(cid)

        if not self.has(cid):
            raise FileNotFoundError(str(filepath(cid).resolve()))

        return filepath(cid)

    def has(self, cid: CID):
        return filepath(cid).exists()

    def check(self, cid: CID):
        if filepath(cid).exists():
            t = digest(filepath(cid), False)
            if t != cid:
                filepath(cid).unlink(True)


cache = Cache()


@lru_cache
def get_cache_dir() -> Path:
    dir = user_cache_dir(__name__, __author__)
    os.makedirs(dir, exist_ok=True)
    return Path(dir)
