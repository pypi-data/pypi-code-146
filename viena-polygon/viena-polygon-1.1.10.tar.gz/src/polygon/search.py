"""This module provides the CLI."""
# cli-module/cli.py


from typing import List, Optional
import typer
from polygon import rest_connect
app = typer.Typer()


#it is just one command now so taken care in the cli.py

if __name__ == "__main__":
    app()
