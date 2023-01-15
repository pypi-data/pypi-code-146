# mypy: disable-error-code = misc
from typer import Typer

from .plot import plot_events


events = Typer()


@events.command()
def plot() -> None:
    plot_events()
