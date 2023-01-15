from typer import Typer

from .drafts.cli import drafts
from .events.cli import events
from .speller.cli import speller


cli = Typer()

cli.add_typer(speller, name="speller")
cli.add_typer(drafts, name="drafts")
cli.add_typer(events, name="events")
