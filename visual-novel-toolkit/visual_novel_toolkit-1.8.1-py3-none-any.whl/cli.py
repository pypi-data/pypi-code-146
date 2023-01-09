# mypy: disable-error-code = misc
from asyncio import run
from pathlib import Path

from typer import Argument
from typer import Exit
from typer import Typer

from .find_missed_drafts import find_missed_drafts
from .find_unused_words import find_unused_words
from .make_draft import make_draft
from .plot_events import plot_events
from .proofread_words import proofread_words
from .sort_words import sort_words


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


drafts = Typer()


@drafts.command()
def new() -> None:
    make_draft()


@drafts.command()
def missed() -> None:
    if find_missed_drafts():
        raise Exit(code=1)


events = Typer()


@events.command()
def plot() -> None:
    plot_events()


cli = Typer()
cli.add_typer(speller, name="speller")
cli.add_typer(drafts, name="drafts")
cli.add_typer(events, name="events")
