import click

import sym.flow.cli.helpers.output as cli_output

from ..version import __version__


@click.command(short_help="Print the version")
def version() -> None:
    cli_output.info(__version__)
