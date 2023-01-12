import click

from tagbackup.commands import link, pull, push, status, unlink


@click.group()
@click.version_option(message="TagBackup client v%(version)s")
def app():
    """
    Learn more at https://tagbackup.com/docs/client
    """
    pass


app.add_command(link)
app.add_command(pull)
app.add_command(push)
app.add_command(status)
app.add_command(unlink)
