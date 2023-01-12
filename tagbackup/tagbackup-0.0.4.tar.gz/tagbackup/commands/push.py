import click

from tagbackup.lib import (
    api_post,
    get_device_id,
    get_filesize,
    get_s3_resource,
    tags_to_csv,
    upload_file,
)


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.argument("tags", nargs=-1)
def push(filename, tags):
    """
    Learn more at https://tagbackup.com/doc/client/push
    """
    device_id = get_device_id()
    if not device_id:
        raise click.ClickException("this device is not linked to TagBackup")

    # show error if this is a directory
    # raise click.ClickException("sorry, TagBackup doesn't support directories (yet)")
    #
    #

    # bail out if no tags provided
    if len(tags) < 1:
        raise click.ClickException(
            "no tags provided. For more information visit https://tagbackup.com/doc/client/push"
        )

    # POST details to tagbackup
    click.echo("Contacting TagBackup...")
    response = api_post(
        "v1/push/init",
        device_id,
        {
            "filename": filename,
            "filesize": get_filesize(filename, False),
            "tags": tags_to_csv(list(set(tags))),
        },
        True,
    )

    # bail on error
    if not response["isValid"]:
        raise click.ClickException(response["error"])

    # notify user we're about to upload the file
    click.echo(
        f"Pushing {filename} ({get_filesize(filename, True)}) to your S3 bucket..."
    )

    # get s3 resource
    resource = get_s3_resource(response["access_key"], response["access_secret"])
    if resource is None:
        raise click.ClickException("there was a problem communicating with S3")

    # upload file
    success = upload_file(resource, filename, response["bucket"], response["filename"])
    if not success:
        raise click.ClickException("there was a problem uploading to S3")

    # POST completion to tagbackup
    response = api_post(
        "v1/push/complete",
        device_id,
        {"filename": response["filename"]},
        True,
    )

    # bail on error
    if not response["isValid"]:
        raise click.ClickException(response["error"])

    # success
    click.echo("Done!")
