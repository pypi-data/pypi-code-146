import click


from tagbackup.lib import (
    api_post,
    download_file,
    file_exists,
    get_device_id,
    get_s3_resource,
    tags_to_csv,
)


@click.command()
@click.argument("filename", type=click.Path(exists=False, dir_okay=False))
@click.argument("tags", nargs=-1)
@click.option("--overwrite", is_flag=True)
def pull(filename, tags, overwrite):
    """
    Learn more at https://tagbackup.com/doc/client/pull
    """
    device_id = get_device_id()
    if not device_id:
        raise click.ClickException("this device is not linked to TagBackup")

    # bail out if no tags provided
    if len(tags) < 1:
        raise click.ClickException(
            "no tags provided. For more information visit https://tagbackup.com/doc/client/pull"
        )

    # bail out if we're about to overwrite an existing file
    if not overwrite and file_exists(filename):
        raise click.ClickException(
            f"a file already exists call {filename}. You can overwrite this file using the --overwrite flag. Learn more at https://tagbackup.com/doc/client/pull"
        )

    # POST details to tagbackup
    click.echo("Contacting TagBackup...")
    response = api_post(
        "v1/pull",
        device_id,
        {
            "tags": tags_to_csv(list(set(tags))),
        },
        True,
    )

    # bail on error
    if not response["isValid"]:
        raise click.ClickException(response["error"])

    # get s3 resource
    resource = get_s3_resource(response["access_key"], response["access_secret"])
    if resource is None:
        raise click.ClickException(
            "there was a problem communicating with your S3 bucket"
        )

    # download file
    success = download_file(
        resource, filename, response["bucket"], response["filename"]
    )
    if not success:
        raise click.ClickException("there was a problem uploading to your S3 bucket")

    # success
    click.echo("Done!")
