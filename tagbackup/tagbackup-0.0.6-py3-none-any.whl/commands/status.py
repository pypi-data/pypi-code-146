import click

from tagbackup.lib import api_get, get_device_id, show_upgrade_available_message


@click.command()
def status():
    """
    Learn more at https://tagbackup.com/docs/client/status
    """
    device_id = get_device_id()

    # show basic message if the device is not linked, then bail out
    if not device_id:
        click.echo("This device is not linked to TagBackup.")
        return

    # retrieve status from tagbackup
    click.echo("Contacting tagbackup...")
    response = api_get("v1/status", device_id, True)

    # bail out if error
    if not response["isValid"]:
        raise click.ClickException(response["error"])

    # everything ok
    click.echo(
        f"Your device is linked to your TagBackup. Your device name is: {response['deviceName']}"
    )
    show_upgrade_available_message(response)
