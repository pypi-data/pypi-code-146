import click

from tagbackup.commands import link, pull, push, status, unlink
from tagbackup.lib import get_version


@click.group(invoke_without_command=True)
@click.option("-v", "--version", is_flag=True, help="Show the version number")
def app(version):
    if version:
        click.echo(get_version())


app.add_command(link)
app.add_command(pull)
app.add_command(push)
app.add_command(status)
app.add_command(unlink)
