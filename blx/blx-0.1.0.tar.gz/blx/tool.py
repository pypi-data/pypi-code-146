from __future__ import annotations

from pathlib import Path

from blx.cid import CID
from blx.client import get_client
from blx.progress import Progress
from blx.service_exit import ServiceExit

__all__ = ["digest", "upload", "download"]


def digest(file: Path, show_progress=True):
    with Progress("Digest", disable=not show_progress) as progress:
        try:
            return CID.from_file(file, progress)
        except ServiceExit as excp:
            progress.shutdown()
            raise excp


def upload(cid: CID, file: Path, show_progress=True):
    with Progress("Upload", disable=not show_progress) as progress:
        try:
            client = get_client()
            client.put(cid, file, progress)
        except ServiceExit as excp:
            progress.shutdown()
            raise excp


def download(cid: CID, file: Path, show_progress=True):
    with Progress("Download", disable=not show_progress) as progress:
        try:
            client = get_client()
            client.get(cid, file, progress)
        except ServiceExit as excp:
            progress.shutdown()
            raise excp
