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



isql = iSQL(**config["default"])

app = typer.Typer(
    name="pisql",
    help="A simple but rich command line interface for Sybase ASE",
    no_args_is_help=True,
    rich_help_panel="rich",
    rich_markup_mode="rich",
)

exe = typer.Typer(
    name="execute",
    help=f"""Execute a query ❓ against a Sybase ASE database 🧑‍💻. Accepts a .sql file 📄",
    [yellow][bold]Alias:[/] x[/]  
    [green][bold]Example:[/]  
    >>> pisql x name.sql[/]
    """,
    rich_markup_mode="rich",
    rich_help_panel="rich",
)


run = typer.Typer(
    name="run",
    help=f"""Execute queries ❓ against a Sybase ASE database 💁. Is able to process many .sql files 📄 and even directories 📁",  
    [yellow][bold]Aliases:[/] @r , := [/]  

    [green][bold]Example:[/]  
      
    >>> pisql @r name.sql cool.sql[/] [dim]# Execute multiple files[/]
    """,
    rich_markup_mode="rich",
    rich_help_panel="rich",
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

@exe.callback(invoke_without_command=True, no_args_is_help=True)
def executer(
    file: str = typer.Argument(..., help="The .sql file 📄 to execute"),
    out: str = typer.Option(None, "-o", "--out", "--out-file", help="The output file 📰, defaults to rich table 📊 on console"),
    override_default_dir: str = typer.Option(None, "-od", "--override-default-dir", help="Override the default directory 📁. Defaults to `~/pisql` 😉"),
    ) -> None:
    """Execute a query ❓ against a Sybase ASE database 📦. Accepts a .sql file 📄"""

    file = Path(file)

    if not override_default_dir:
        dir = Path(os.path.expanduser("~")) / "pisql" / "results"
        dir.mkdir(parents=True, exist_ok=True)
    else:
        dir = Path(override_default_dir) if override_default_dir != "." else Path.cwd()
        dir.mkdir(parents=True, exist_ok=True)

    with basic_pbar() as pbar:
        task = pbar.add_task(f"Executing {file.name}", total=None)
        df = isql.run_sql_file(file)

        pbar.update(task, advance=50)
        pbar.update(task, description=f"Writing results to {dir}")

        csv_file = dir / "{file.stem}.csv"
        parquet_file = dir / "{file.stem}.parquet"

        if out is None:
            csv_out = df.write_csv(file=csv_file)
            parquet_out = df.write_parquet(file=parquet_file,  compression="lz4")
            records = orjson.loads(df.write_json(row_oriented=True))
            console.print(tableFromRecords(records, theme="default"))
        else:
            outfile = dir / file.name
            csv_out = df.write_csv(file=csv_file)
            parquet_out = df.write_parquet(file=parquet_file, compression="lz4")
            if out.lower() in ["json", "excel"]:
                errors.print(f"[bold red]Output format {out} not supported yet with the base version.[/]", style="bold red")
                errors.print(f"[dim yellow]Please install `pandas` to get excel support[/]")
                sys.exit(1)
        pbar.update(task, advance=50)
        pbar.update(task, description=f"✅ Donew writing results to {dir}", completed=True)
        sys.exit(0)

@run.command(name="=>", help="Execute a query ❓ against a Sybase ASE database 📦. Accepts a dir 📁 of .sql files 📄 or a list of files")
def runall(
    args : List[Path],
    dir: str = typer.Option(None, "-d", "--dir", help="the base directory of all the files")
    ) -> None:
    """Execute a query ❓ against a Sybase ASE database 📦. Accepts a dir 📁 of .sql files 📄 or a list of files"""
    files = []

    if dir is not None:
        dir = Path(dir)
        if dir.is_dir():
            files += [file for file in dir.iterdir() if file.suffix == ".sql"]
        else:
            errors.print(f"[bold red]Invalid directory {dir}[/]", style="bold red")
            sys.exit(1)
    
    for arg in args:
        arg = Path(arg)
        if arg.is_dir():
            files += [file for file in arg.iterdir() if file.suffix == ".sql"]
        elif arg.is_file():
            files.append(arg)
        else:
            errors.print(f"[bold red]Invalid file/dir {arg}[/]", style="bold red")
            sys.exit(1)
    for file in files:
        executer(file=file)

@run.command(name="@", help="Execute a query ❓ against a Sybase ASE database 📦. Accepts a dir 📁 of .sql files 📄 or a list of files")
def runallAlias(
    args : List[Path],
    dir: str = typer.Option(None, "-d", "--dir", help="the base directory of all the files")
    ) -> None:
    """Execute a query ❓ against a Sybase ASE database 📦. Accepts a dir 📁 of .sql files 📄 or a list of files"""
    runall(args=args, dir=dir)


def listTablesServer() -> None:
    """List all tables 📓 in the server 📦"""
    querytxt = """
        SELECT t.name, c.name
        FROM sysobjects t, syscolumns c
        WHERE t.id = c.id AND t.type IN ('U', 'V')
        """
    df = isql.query(querytxt)
    console.print(df)
    df.write_parquet(pisql_home / "results" / "tables.parquet", compression="lz4")

@run.command(name="tables?", help="List all tables 📓 in the server 📦. [bold yellow]Alias: `?`[/]")
def listTables() -> None:
    """List all tables 📓 in the server 📦"""
    listTablesServer()

@run.command(name="?", help="List all tables 📓 in the server 📦")
def listTables() -> None:
    """List all tables 📓 in the server 📦"""
    listTablesServer()


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

app.add_typer(exe, name="execute")
app.add_typer(exe, name="exec", hidden=True)
app.add_typer(exe, name="e", hidden=True)
app.add_typer(exe, name="x", hidden=True)

app.add_typer(dev, name="dev", no_args_is_help=True)
app.add_typer(dev, name="d", no_args_is_help=True, hidden=True)
app.add_typer(run, name="run", no_args_is_help=True)
app.add_typer(run, name="@r", no_args_is_help=True, hidden=True)
app.add_typer(run, name=":=", no_args_is_help=True, hidden=True)

