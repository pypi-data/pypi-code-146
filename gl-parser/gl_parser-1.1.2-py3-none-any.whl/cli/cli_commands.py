"""Console script for gl_parser."""
import sys
import logging
from platform import python_version

import click

from gl_parser.cli.config_commands import config
from gl_parser.cli.convert_commmands import convert
from .. import __version__ as current_version, CONFIGURATION_MANAGER

logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version=current_version)
def main():
    pass


@click.command()
def about():
    banner_char = '-'
    app_name = 'General ledger parser'
    length = len(app_name) + 4
    click.echo(banner_char * length)
    click.echo(f'{banner_char} {app_name} {banner_char}')
    click.echo(banner_char * length)
    click.echo(f'Operating System: {sys.platform}')
    click.echo(f'Python : {python_version()}')
    click.echo(f'Configuration file: {CONFIGURATION_MANAGER.config_file}')
    logger.debug('Ran about command.')


main.add_command(about)
main.add_command(config)
main.add_command(convert)

if __name__ == "__main__":
    main()  # pragma: no cover
