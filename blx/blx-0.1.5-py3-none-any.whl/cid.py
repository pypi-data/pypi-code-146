from __future__ import annotations

import hashlib
import os
from pathlib import Path

from blx.progress import Progress

__all__ = ["CID"]

BUFSIZE = 4 * 1024 * 1024


def is_hex(x: str):
    hset = set("0123456789abcdef")
    xset = set(x)
    return len(hset & xset) == len(xset)


class CID:
    def __init__(self, sha256hex: str):
        if len(sha256hex) != 64 or not is_hex(sha256hex):
            raise ValueError(f"Not a valid sha256hex: {sha256hex}")
        self._sha256hex = sha256hex

    @classmethod
    def from_file(cls, file: Path, progress: Progress):
        return CID(digest(file, progress))

    def hex(self) -> str:
        return self._sha256hex

    def __eq__(self, x: CID):
        return x.hex() == self.hex()


def digest(file: Path, progress: Progress) -> str:
    h = hashlib.sha256()
    size = os.path.getsize(file)
    progress.set_meta(size)
    with open(file, "rb") as f:
        while data := f.read(BUFSIZE):
            progress.update(len(data))
            h.update(data)
    progress.set_completed()
    return h.hexdigest()
