import webbrowser

import click

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.helpers.constants import SYM_DOCUMENTATION_URL


@click.command(short_help="Opens a link to Sym documentation")
def docs() -> None:
    """Opens a link to the Sym documentation website in a new window.

    Example:
        `symflow docs`
    """

    cli_output.info(f"Opening a link to Sym documentation: {SYM_DOCUMENTATION_URL}")
    webbrowser.open(SYM_DOCUMENTATION_URL)
