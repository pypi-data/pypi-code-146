from pathlib import Path
from .snake_wrapper import SnakEcdysis, SnakeInstaller
from .cli_wrapper import main_wrapper
from .usefull_function import *


__version__ = Path(__file__).parent.resolve().joinpath("VERSION").open("r").readline().strip()

__doc__ = """
:author: Sebastien Ravel
:contact: sebastien.ravel@cirad.fr
:date: 01-01-2023
:version: """ + __version__ + """

Use it to wrapped snakemake workflow.

"""
