import typer
from .lib.identity import get_device_id

app = typer.Typer()


@app.command()
def status():
    device_id = get_device_id()
    print(f"Device ID: {device_id}")
