import polars as pl
import typer

from typing import List, Tuple, Dict, Union, Optional, Any, Iterator, TypeVar
from pisql.core.isql import iSQL
from pisql.utils.paths import (
    base_dir, tests_dir, package_dir
)

qapp = typer.Typer(
    name="query",
    help="Run a query against a Sybase ASE database",
    no_args_is_help=True,
)

@qapp.command()
def query(
    query: typer.Argument(..., help="The query to run"),
    ):
    pass