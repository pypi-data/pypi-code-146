import typer

from .lib.api import api_post
from .lib.identity import get_device_id, set_device_id

app = typer.Typer()


@app.command()
def unlink():
    # bail if a device ID doesn't exist
    device_id = get_device_id()
    if not device_id:
        raise typer.Exit("Error: this device is not linked to TagBackup")

    # unlink locally regardless
    set_device_id(str(""))

    # POST details to tagbackup
    response = api_post("v1/unlink", device_id, {}, True)
    if response["isValid"]:
        print("Device unlinked successfully")
    else:
        print(response["error"])
