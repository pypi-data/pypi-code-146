# mypy: disable-error-code = misc
from typer import Exit
from typer import Typer

from .missed import find_missed_drafts
from .new import make_draft


drafts = Typer()


@drafts.command()
def new() -> None:
    make_draft()


@drafts.command()
def missed() -> None:
    if find_missed_drafts():
        raise Exit(code=1)
