from __future__ import annotations

from enum import IntEnum
from pathlib import Path

import typer

from blx.cid import CID
from blx.client import get_client
from blx.digest import digest
from blx.download import download
from blx.service_exit import ServiceExit, register_service_exit
from blx.upload import upload

__all__ = ["app"]


class EXIT_CODE(IntEnum):
    SUCCESS = 0
    FAILURE = 1


app = typer.Typer(add_completion=False)

PROGRESS_OPTION = typer.Option(
    True, "--progress/--no-progress", help="Display progress bar."
)


@app.command()
def has(file: Path, progress: bool = PROGRESS_OPTION):
    """
    Check if file exists.
    """
    register_service_exit()

    try:
        cid = digest(file, progress)
    except ServiceExit:
        raise typer.Exit(EXIT_CODE.FAILURE)

    client = get_client()
    raise typer.Exit(EXIT_CODE.SUCCESS if client.has(cid) else EXIT_CODE.FAILURE)


@app.command()
def cid(file: Path, progress: bool = PROGRESS_OPTION):
    """
    CID of file.
    """
    register_service_exit()

    try:
        cid = digest(file, progress)
        typer.echo(cid.hex())
    except ServiceExit:
        raise typer.Exit(EXIT_CODE.FAILURE)

    raise typer.Exit(EXIT_CODE.SUCCESS)


@app.command()
def put(file: Path, progress: bool = PROGRESS_OPTION):
    """
    Upload file.
    """
    register_service_exit()

    try:
        cid = digest(file, progress)
        upload(cid, file, progress)
    except ServiceExit:
        raise typer.Exit(EXIT_CODE.FAILURE)

    raise typer.Exit(EXIT_CODE.SUCCESS.value)


@app.command()
def get(sha256hex: str, file_output: Path, progress: bool = PROGRESS_OPTION):
    """
    Download file.
    """
    register_service_exit()

    try:
        cid = CID(sha256hex)
        download(cid, file_output, progress)
    except ServiceExit:
        raise typer.Exit(EXIT_CODE.FAILURE)

    raise typer.Exit(EXIT_CODE.SUCCESS.value)
