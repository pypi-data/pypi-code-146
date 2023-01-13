import asyncio
import sys
from abc import ABC, abstractmethod
from enum import Enum
from io import StringIO
from typing import Optional

import sqlalchemy.engine.row
import typer
from databases import Database
from rich import print
from rich.console import Console
from rich.table import Table

from dbs.exceptions import DBSException
from dbs.rows_transformation import sql_rows_to_json

app = typer.Typer()


class QueryType(str, Enum):
    fetch = "fetch"
    execute = "execute"


class OutputType(str, Enum):
    table = "table"
    json = "json"


class RowsPrinter(ABC):
    @abstractmethod
    def print_rows(self, rows: list[sqlalchemy.engine.row.Row]):
        ...


class JsonRowsPrinter(RowsPrinter):
    def print_rows(self, rows: list[sqlalchemy.engine.row.Row]):
        json_rows = sql_rows_to_json(rows)
        print(json_rows)


class TableRowsPrinter(RowsPrinter):
    def __init__(self, console: Console):
        self.console = console

    def print_rows(self, rows: list[sqlalchemy.engine.row.Row]):
        if not rows:
            return
        keys = [key for key in rows[0].keys()]
        table = Table(*keys)
        for row in rows:
            table.add_row(*[str(row[key]) for key in keys])
        self.console.print(table)


async def query_main(
    host: str,
    query: str,
    params: Optional[StringIO] = None,
    query_type: QueryType = QueryType.fetch,
    ssl: Optional[bool] = False,
) -> list[sqlalchemy.engine.row.Row]:
    try:
        database = Database(host)
    except Exception:
        # Failed to create database object
        raise DBSException("Failed to parse host")

    try:
        await database.connect()
    except Exception:
        raise DBSException("Failed to connect")

    try:
        if query_type == QueryType.fetch:
            result = await database.fetch_all(query)
        else:
            result_number = await database.execute(query)
            result = [{"result": result_number}]
    except Exception:
        raise DBSException("Failed to execute the query")
    finally:
        database.disconnect()
        return result


@app.command()
def main(
    host: str,
    query_file: typer.FileText,
    params: Optional[typer.FileText] = typer.Argument("-", allow_dash=True),
    query_type: QueryType = QueryType.fetch,
    output_type: OutputType = OutputType.table,
    ssl: Optional[bool] = False,
):
    if params == "-":
        params = sys.stdin
    result = asyncio.run(query_main(host, query_file.read(), params, query_type, ssl))
    if output_type == OutputType.table:
        console = Console()
        TableRowsPrinter(console).print_rows(result)
    elif output_type == OutputType.json:
        JsonRowsPrinter().print_rows(result)


if __name__ == "__main__":
    app()
