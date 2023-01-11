import requests
import typer
from uuid import UUID

from .lib.api import api_post
from .lib.identity import get_device_id, get_machine_id, set_device_id

app = typer.Typer()


@app.command()
def link(key: UUID):
    # bail if a device ID already exists
    device_id = get_device_id()
    if device_id:
        raise typer.Exit("Error: this device is already linked to TagBackup")

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
        print(
            f"Device \"{response['name']}\" linked successfully. Welcome to TagBackup."
        )
    else:
        print(response["error"])
