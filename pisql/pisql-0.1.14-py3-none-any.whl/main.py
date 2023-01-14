import random
import orjson
import typer
import rich
import sys
import os
import re

from pathlib import Path

from typing import List, Tuple, Dict, Union, Optional, Any, Iterator, TypeVar

from iotree.core.render.tables import tableFromRecords
from iotree.core.render.funcs import basic_pbar

from pisql.core.isql import iSQL
from pisql.utils.render import console, errors

from pisql.utils.paths import (
    base_dir, tests_dir, package_dir,
    config, assets_dir, data_dir
)

from .cli.execute import exe
from .cli.run import run


isql = iSQL(**config["default"])

app = typer.Typer(
    name="pisql",
    help="A simple but rich command line interface for Sybase ASE",
    no_args_is_help=True,
    rich_help_panel="rich",
    rich_markup_mode="rich",
)

dev = typer.Typer(
    name="dev",
    help=f"""Developer tools 💻.
    [yellow][bold]Aliases:[/] d, dev[/]
    """,
    rich_markup_mode="rich",
    rich_help_panel="rich",
    no_args_is_help=True,
)


app.add_typer(exe, name="execute")
app.add_typer(exe, name="exec", hidden=True)
app.add_typer(exe, name="e", hidden=True)
app.add_typer(exe, name="x", hidden=True)

app.add_typer(dev, name="dev", no_args_is_help=True)
app.add_typer(dev, name="d", no_args_is_help=True, hidden=True)

app.add_typer(run, name="run", no_args_is_help=True, chain=True, help="Run one or many 🧐 queries in a row with a rich progress bar 🏃‍♂️")
app.add_typer(run, name="@r", no_args_is_help=True, hidden=True, chain=True, )
app.add_typer(run, name="::", no_args_is_help=True, hidden=True, chain=True)



@dev.command(name="test", help="Run tests 🧪")
def test(
    test_type: str = typer.Argument(..., help="The type of test to run 🧪"),
    index: int = typer.Option(None, "-i", "-idx", "--index", help="The index of the subtest to run [dim](if your test has many options)[/] 🧪"),
    name: str = typer.Option(None, "-n", "--name", help="The name (a part of it) of the subtest to run [dim](if your test has many options)[/] 🧪"),
    ) -> None:
    """Run tests 🧪"""
    test_type = test_type.lower()
    if index is not None and name is not None:
        errors.print("[bold red]You can't specify both index and name[/]", style="bold red")
        errors.print("[dim yellow]Using `name`.[/]")
        index = None
        selector = name
    elif index is not None:
        selector = index
    elif name is not None:
        selector = name
    else:
        selector = None
    
    if test_type in ["parse", "parsing", "text"]:
        raw_outs = {
            name: open( data_dir / name, "r").read() for name in os.listdir(data_dir)
        }
        if selector is None:
            selector = random.randint(0, len(raw_outs) - 1)

        target = [
            name for name in raw_outs.keys() if selector in name
        ]

        if not len(target):
            raise typer.BadParameter(f"Couldn't find a test with name {selector}")

@dev.command(name="view", help="See the raw data 📰 🧪")
def test(
    name: str = typer.Argument(..., help="The name (a part of it) of the subtest to run [dim](if your test has many options)[/] 🧪"),
    head: int = typer.Option(500, "-h", "--head", help="The number of lines to show [dim](if your file is huge !)[/] 🧪"),
    raw: bool = typer.Option(False, "-ra", "--raw", help="Whether to show the raw data 📰 🧪"),
    remove_whitespaces: bool = typer.Option(False, "-rw", "--rm-ws", "--remove-whitespaces", help="Remove whitespaces from the output [dim](if your data uses them too much !)[/] 🧪"),
    columns: bool = typer.Option(False, "-c", "--cols", "--columns", help="Whether to only display the parsed columns 🏦"),
    ) -> None:

    raw_outs = {
            name: open( data_dir / name, "r").read() for name in os.listdir(data_dir)
        }
    target = [
        key for key in raw_outs.keys() if name in key
    ]

    if not len(target):
        raise typer.BadParameter(f"Couldn't find a raw datafile with name {name}")
    
    target = target.pop()
    raw_out = raw_outs[target]

    if raw:
        idx = 0
        for i in range(head):
            idx = raw_out.find("'", idx + 1)
        console.print(raw_out[:idx])
        sys.exit(0)

    if columns:
        df = isql.strRowColSplitter(raw_out)
        console.print(df.columns)
        sys.exit(0)
    else:
        df = isql.strRowColSplitter(raw_out)
        records = orjson.loads(df.write_json(row_oriented=True))
        console.print(tableFromRecords(records[:head], theme="default"))

    if remove_whitespaces:
        raw_out = re.sub(r"([ \t\n]+)", " ", raw_out)
    
    sys.exit(0)



@dev.command(name="list", help="List the test queries 📰🗄️")
def list():
    """List the test queries 📰🗄️"""
    queries_dir = assets_dir / "sql"
    console.print(f"[bold magenta]Test queries:[/]")
    
    for file in os.listdir(queries_dir):
        console.print(f"[yellow] \u2736 📰 {file}[/]")
    
    console.print(f"[bold magenta]Total:[/] {len(os.listdir(queries_dir))} 📰🗄️")
    console.print(f"Let's go to work ! 🚀🚀🚀")

if __name__ == "__main__":
    typer.run(app)