"""Command line interface for Diligent."""

import click

from .start import start_server

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version="0.0.1")
def cli():
    """Diligent command line interface."""


# add start command
@cli.command()
@click.option('-t', '--toml', 'config_file', type=click.Path(exists=True), required=True)
def start(config_file):
    """Start the Diligent server."""
    if not config_file:
        click.echo('Please specify the config toml file.')
        return

    click.echo('Starting the Diligent server...')

    start_server(config_file)


@cli.command()
def stop():
    """Stop the Diligent server."""
    print("Stopping Diligent server...")


__all__ = ["cli", "start_server"]
