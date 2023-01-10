import click

from classiq import __version__

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(name="classiq", context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__, "-V", "--version")
def cli():
    """Main entrypoint."""
