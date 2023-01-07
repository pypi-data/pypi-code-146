"""Command line interface."""

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.traceback import install

from .sqlpygen import generate


@click.command()
@click.option(
    "-i",
    "--input",
    "input_file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    required=True,
    help="Annotated sql file.",
)
@click.option(
    "-o",
    "--output",
    "output_file",
    type=click.Path(exists=False, file_okay=True, dir_okay=False, path_type=Path),
    required=True,
    help="Generated python file.",
)
@click.option(
    "-d",
    "--dbcon",
    type=click.Choice(["sqlite3", "apsw"]),
    required=True,
    help="Database connection type.",
)
@click.option(
    "-nt",
    "--no-typeguard",
    is_flag=True,
    help="Do not add typechecked decorator to query args.",
)
@click.option("-v", "--verbose", is_flag=True, help="Print out intermediate results.")
def cli(input_file, output_file, dbcon, no_typeguard, verbose):
    """SqlPyGen

    Generated type annotated python code from annotated SQL
    """
    install(show_locals=False, console=Console(stderr=False), suppress=[click])
    typeguard = not no_typeguard

    input_ = input_file.read_text()
    try:
        output = generate(input_, input_file.name, dbcon, typeguard, verbose)
    except RuntimeError as e:
        click.secho(str(e), fg="red")
        sys.exit(1)

    output_file.write_text(output)
    click.secho("Python Code generated successfully", fg="green")
