import polars as pl
import typer
from pathlib import Path
from typing import List, Tuple, Dict, Union, Optional, Any, Iterator, TypeVar
from pisql.core.isql import iSQL
from pisql.utils.paths import (
    base_dir, tests_dir, package_dir
)


run = typer.Typer(
    name="run",
    help=f"""Execute queries 🧐 against a Sybase ASE database 💁. Is able to process many .sql files 📄 and even directories 📁",  
    [yellow][bold]Aliases:[/] @r , :: [/]  

    [green][bold]Example:[/]  

    >>> pisql @r name.sql cool.sql[/] [dim]# Execute multiple files[/]
    """,
    rich_markup_mode="rich",
    rich_help_panel="rich",
)


@run.command(name="f(x)", help="Execute a query 🧐 against a Sybase ASE database 📦. Accepts a dir 📁 of .sql files 📄 or a list of files")
def runall(
    args : List[str],
    ) -> None:
    """Execute a query 🧐 against a Sybase ASE database 📦. Accepts a dir 📁 of .sql files 📄 or a list of files"""
    files = []
    print(args)
    for arg in args:
        arg = Path(os.getcwd() + args[1:] if arg[0] == "." else arg)
        if arg.is_dir():
            files += [file for file in arg.iterdir() if file.suffix == ".sql"]
        elif arg.is_file():
            files.append(arg)
        else:
            raise ValueError(f"Invalid file or directory 📁: {arg}")
    
    return rich_func_chainer([isql.run_sql_file], params=files)
    

@run.command(name="+=", help="Execute a query 🧐 against a Sybase ASE database 📦. Accepts a dir 📁 of .sql files 📄 or a list of files")
def runallAlias(
    args : List[str],
    ) -> None:
    """Execute a query 🧐 against a Sybase ASE database 📦. Accepts a dir 📁 of .sql files 📄 or a list of files"""
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
    """List all tables 📓 in the server 📦 
    """
    listTablesServer()
