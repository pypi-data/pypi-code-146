
import typer
from pydpn import DeeperNetwork
from pydpn._utils.cli_tools import check_config
app = typer.Typer()

config = check_config()

@app.command("memory")
def memory():
    """used memory from dpn device

    Args:
       
    """
    print("memory")
    if config:

        d = DeeperNetwork(**config).dashboard
        print(d.memory)


@app.command("cpu")
def cpu():
    """used memory from dpn device

    Args:
       
    """
    print("cpu")
    if config:
        d = DeeperNetwork(**config).dashboard
        print(d.cpu)


def main():
    """main"""
    app()
