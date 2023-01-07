import humanize
import os
from pathlib import Path
import typer
from typing import List

from .lib.api import api_post
from .lib.identity import get_device_id
from .lib.misc import tags_to_csv
from .lib.s3 import get_s3_resource, upload_file

app = typer.Typer()


@app.command()
def push(file: Path, tags: List[str]):
    # bail if a device ID doesn't exist
    device_id = get_device_id()
    if not device_id:
        raise typer.Exit("Error: this device is not linked to TagBackup")

    # ensure this is a single file
    if file.is_file():
        pass
    elif file.is_dir():
        raise typer.Exit("Sorry, TagBackup doesn't support directories (yet)")
    else:
        raise typer.Exit(f"Error: I couldn't find a file called {file}")

    # POST details to tagbackup
    print("Contacting TagBackup...")
    filesize = os.stat(file).st_size
    response = api_post(
        "v1/push/init",
        device_id,
        {
            "filename": file.name,
            "filesize": filesize,
            "tags": tags_to_csv(list(set(tags))),
        },
        True,
    )

    # bail on error
    if not response["isValid"]:
        raise typer.Exit(response["error"])

    # notify user we're about to upload the file
    print(
        f"Pushing {file.name} ({humanize.naturalsize(filesize, binary=True)}) to your S3 bucket..."
    )

    # get s3 resource
    resource = get_s3_resource(response["access_key"], response["access_secret"])
    if resource is None:
        raise typer.Exit("Error: there was a problem communicating with S3")

    # upload file
    success = upload_file(resource, file, response["bucket"], response["filename"])
    if not success:
        raise typer.Exit("Error: there was a problem uploading to S3")

    # POST completion to tagbackup
    response = api_post(
        "v1/push/complete",
        device_id,
        {"filename": response["filename"]},
        True,
    )

    # bail on error
    if not response["isValid"]:
        raise typer.Exit(response["error"])

    # success
    print("Done!")
