import click

from tagbackup.lib import get_device_id, get_version


@click.command()
def status():
    """
    Learn more at https://tagbackup.com/doc/client/status
    """
    device_id = get_device_id()
    version = get_version()

    if device_id:
        # todo: fetch status endpoint
        # add the device name to the output
        # if new version available, add that to the output
        click.echo(f"TagBackup client v{version}")
        click.echo(f"Device ID: {device_id}")
    else:
        click.echo(f"TagBackup client v{version}")
        click.echo("This device is not linked to TagBackup.")
