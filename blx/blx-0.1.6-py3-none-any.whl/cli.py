from __future__ import annotations

from enum import IntEnum
from pathlib import Path
from typing import Optional

import typer

from blx.cid import CID
from blx.client import get_client
from blx.digest import digest
from blx.download import download
from blx.meta import __version__
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


@app.callback(invoke_without_command=True)
def cli(version: Optional[bool] = typer.Option(None, "--version", is_eager=True)):
    if version:
        print(__version__)
        raise typer.Exit()


@app.command()
def has(cid: str):
    """
    Check if file exists.
    """
    found = get_client().has(CID(cid))
    raise typer.Exit(EXIT_CODE.SUCCESS if found else EXIT_CODE.FAILURE)


@app.command()
def cid(path: Path, progress: bool = PROGRESS_OPTION):
    """
    CID of file.
    """
    register_service_exit()

    try:
        cid = digest(path, progress)
        typer.echo(cid.hex())
    except ServiceExit:
        raise typer.Exit(EXIT_CODE.FAILURE)

    raise typer.Exit(EXIT_CODE.SUCCESS)


@app.command()
def put(path: Path, progress: bool = PROGRESS_OPTION):
    """
    Upload file.
    """
    register_service_exit()

    try:
        cid = digest(path, progress)
        upload(cid, path, progress)
    except ServiceExit:
        raise typer.Exit(EXIT_CODE.FAILURE)

    raise typer.Exit(EXIT_CODE.SUCCESS.value)


@app.command()
def get(cid: str, path: Path, progress: bool = PROGRESS_OPTION):
    """
    Download file.
    """
    register_service_exit()

    try:
        download(CID(cid), path, progress)
    except ServiceExit:
        raise typer.Exit(EXIT_CODE.FAILURE)

    raise typer.Exit(EXIT_CODE.SUCCESS.value)
