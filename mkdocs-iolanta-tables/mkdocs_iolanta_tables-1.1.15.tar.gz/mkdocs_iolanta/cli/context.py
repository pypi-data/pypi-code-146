from pathlib import Path

from typer import Typer

app = Typer(name='context')


@app.callback(invoke_without_command=True)
def context(path: Path):
    """Print context for a path."""
    raise NotImplementedError('Not implemented yet.')

