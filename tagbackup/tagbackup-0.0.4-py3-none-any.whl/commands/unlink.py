import click


from tagbackup.lib import api_post, get_device_id, set_device_id


@click.command()
def unlink():
    """
    Learn more at https://tagbackup.com/doc/client/unlink
    """
    device_id = get_device_id()
    if not device_id:
        raise click.ClickException("this device is not linked to TagBackup")

    # unlink locally regardless
    set_device_id(str(""))

    # POST details to tagbackup
    response = api_post("v1/unlink", device_id, {}, True)
    if response["isValid"]:
        click.echo("Device unlinked successfully")
    else:
        click.echo(response["error"])
