import humanize
from pathlib import Path
import typer
from typing import List

from .lib.api import api_post
from .lib.identity import get_device_id
from .lib.misc import tags_to_csv
from .lib.s3 import download_file, get_s3_resource

app = typer.Typer()


@app.command()
def pull(file: Path, tags: List[str], overwrite: bool = False):
    # bail if a device ID doesn't exist
    device_id = get_device_id()
    if not device_id:
        raise typer.Exit("Error: this device is not linked to TagBackup")

    # bail if we're about to overwrite an existing file
    if not overwrite:
        if file.is_file():
            raise typer.Exit(f"Sorry, a file already exists call {file}")
        elif file.is_dir():
            raise typer.Exit(f"Sorry, a directory already exists call {file}")

    # POST details to tagbackup
    print("Contacting TagBackup...")
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
        raise typer.Exit(response["error"])

    # notify user we're about to download the file
    print(
        f"Pulling {file.name} ({humanize.naturalsize(response['filesize'], binary=True)}) from your S3 bucket..."
    )

    # get s3 resource
    resource = get_s3_resource(response["access_key"], response["access_secret"])
    if resource is None:
        raise typer.Exit("Error: there was a problem communicating with S3")

    # download file
    success = download_file(
        resource, file.name, response["bucket"], response["filename"]
    )
    if not success:
        raise typer.Exit("Error: there was a problem uploading to S3")

    # success
    print("Done!")
