# mypy: disable-error-code = misc
from asyncio import run
from pathlib import Path

from typer import Argument
from typer import Exit
from typer import Typer

from .proofread import proofread_words
from .sort import sort_words
from .unused import find_unused_words


speller = Typer()


@speller.command()
def sort(files: list[Path] = Argument(None)) -> None:
    if sort_words(files):
        raise Exit(code=1)


@speller.command()
def unused(files: list[Path] = Argument(None)) -> None:
    if find_unused_words(files):
        raise Exit(code=1)


@speller.command()
def proofread() -> None:
    run(proofread_words())
