import click


from tagbackup.lib import (
    api_post,
    get_device_id,
    show_upgrade_available_message,
    set_device_id,
)


@click.command()
def unlink():
    """
    Learn more at https://tagbackup.com/docs/client/unlink
    """
    device_id = get_device_id()
    if not device_id:
        raise click.ClickException("this device is not linked to TagBackup")

    # unlink locally regardless
    set_device_id(str(""))

    # POST details to tagbackup
    response = api_post("v1/unlink", device_id, {}, True)

    # bail out if error
    if not response["isValid"]:
        raise click.ClickException(response["error"])

    # success
    click.echo("Device unlinked successfully")
    show_upgrade_available_message(response)
