# heath --- Manage projections
# Copyright © 2021, 2022 Bioneland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
from typing import Optional

import pkg_resources
import typer

from heath import commands

__version__ = pkg_resources.get_distribution(__name__).version
app = typer.Typer()


@app.command()
def init() -> None:
    """Initialises required schemas."""

    commands.initialise(read_dsn())


@app.command()
def status() -> None:
    """Lists all known projections and their corresponding event ID."""

    commands.status(read_dsn(), typer.echo)


@app.command()
def purge(name: str, force: Optional[bool] = False) -> None:
    """Removes the projection's data and the matching record in the ledger."""

    if not force:
        typer.confirm("Are you sure you want to purge it?", abort=True)

    try:
        commands.purge(read_dsn(), name)
    except ValueError as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1)


@app.command()
def stall(name: str) -> None:
    """Mark a projection as being stalled."""

    try:
        commands.stall(read_dsn(), name)
    except commands.UnknownProjection as exc:
        typer.echo(str(exc))
        raise typer.Exit(code=1)


def read_dsn() -> str:
    if dsn := os.environ.get("HEATH_DSN", ""):
        return dsn
    typer.echo("Heath's DSN must be set using `HEATH_DSN` environment variable.")
    raise typer.Exit(code=1)
