import click


from tagbackup.lib import api_post, get_device_id, get_machine_id, set_device_id


@click.command()
@click.argument("key", type=click.UUID)
def link(key):
    """
    Learn more at https://tagbackup.com/doc/client/link
    """
    device_id = get_device_id()
    if device_id:
        raise click.ClickException(
            "this device is already linked to TagBackup. If you want to link it to a different account your must unlink it first."
        )

    # POST details to tagbackup
    response = api_post(
        "v1/link",
        None,
        {
            "key": str(key),
            "machine": get_machine_id(),
        },
        False,
    )
    if response["isValid"]:
        set_device_id(str(key))
        click.echo(
            f"Device \"{response['name']}\" linked successfully. Welcome to TagBackup."
        )
    else:
        click.echo(response["error"])
