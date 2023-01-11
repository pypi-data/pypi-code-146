from __future__ import annotations

import hashlib
import os
from pathlib import Path

from blx.progress import Progress

__all__ = ["CID"]

BUFSIZE = 4 * 1024 * 1024


class CID:
    def __init__(self, sha256hex: str):
        self._sha256hex = sha256hex

    @classmethod
    def from_file(cls, file: Path, progress: Progress):
        return CID(digest(file, progress))

    def hex(self) -> str:
        return self._sha256hex


def digest(file: Path, progress: Progress) -> str:
    h = hashlib.sha256()
    size = os.path.getsize(file)
    progress.set_meta(size)
    with open(file, "rb") as f:
        while data := f.read(BUFSIZE):
            progress.update(len(data))
            h.update(data)
    progress.shutdown()
    return h.hexdigest()
