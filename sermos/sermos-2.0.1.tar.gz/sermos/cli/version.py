""" Sermos and Sermos CLI version
"""
import click
from sermos import __version__

CLI_VERSION = "0.1.0"


@click.group()
def get_version():
    """ Sermos and Sermos CLI Version
    """


@get_version.command()
def version():
    """ Print version of Sermos and Sermos CLI
    """
    click.echo(
        f"Sermos Version: {__version__}; Sermos CLI Version: {CLI_VERSION}")
