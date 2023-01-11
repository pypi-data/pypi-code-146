import os
import sys

# add the repo/python folder to sys.path
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
    )
)

import click

from truera.client.cli.activate import activate
from truera.client.cli.add import add
from truera.client.cli.cli_utils import CLI_CONTEXT_SETTINGS
import truera.client.cli.cli_utils as cli_utils
from truera.client.cli.delete import delete
from truera.client.cli.get import get
from truera.client.cli.package import package
from truera.client.cli.restore import restore
from truera.client.cli.save import save
from truera.client.cli.scheduled_ingestion import scheduled_ingestion
from truera.client.cli.verify import verify


@click.group()
def tru():
    pass


@tru.command(
    help="Get the commit this cli was built from.",
    context_settings=CLI_CONTEXT_SETTINGS
)
def version():
    commit, build_time, cli_version = cli_utils.get_build_info()

    if not commit and not build_time:
        click.echo("Build info file is not present in this installation.")
    else:
        click.echo("This cli was built from commit: " + commit)
        click.echo("This cli was built at: " + build_time)
    if not cli_version:
        click.echo("Version file is not present in this installation.")
    else:
        click.echo("This cli is version: " + cli_version)


tru.add_command(add)
tru.add_command(activate)
tru.add_command(package)
tru.add_command(verify)
tru.add_command(get)
tru.add_command(save)
tru.add_command(delete)
tru.add_command(scheduled_ingestion)
if not cli_utils.feature_is_hidden('admin'):
    tru.add_command(restore)

if __name__ == '__main__':
    tru()
