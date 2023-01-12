import click
from qbeast.auth.commands import login
from qbeast.expo.commands import expo
from qbeast.curator.commands import curator

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """qbeast commands"""
    pass


cli.add_command(login)
cli.add_command(expo)
cli.add_command(curator)

cli()
