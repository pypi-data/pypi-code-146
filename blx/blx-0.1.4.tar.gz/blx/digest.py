from __future__ import annotations

from pathlib import Path

from blx.cid import CID
from blx.progress import Progress
from blx.service_exit import ServiceExit

__all__ = ["digest"]


def digest(file: Path, show_progress=True):
    with Progress("Digest", disable=not show_progress) as progress:
        try:
            return CID.from_file(file, progress)
        except ServiceExit as excp:
            progress.shutdown()
            raise excp
