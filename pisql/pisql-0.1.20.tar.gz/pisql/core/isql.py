import polars as pl
import subprocess
import orjson
import uuid
import rich
import copy
import sys
import os
import re

from pathlib import Path
from typing import List, Tuple, Dict, Union, Optional, Any, Iterator, TypeVar, MutableSequence

from iotree.core.render.funcs import rich_func_chainer
from iotree.core.render.tables import tableFromRecords

from ..utils.render import console, errors
from ..utils.paths import data_dir, config, assets_dir

iSqlColumns = Union[str, List[str]]
iSqlRows = Union[str, List[List[str]]]
iSqlRecord = Union[Dict[str, str]]
iSqlRecords = List[iSqlRecord]
iSqlResponse = Union[str, Tuple[iSqlColumns, iSqlRows]]
iSqlError = Dict[str, str]
iSqlPath = Union[str, os.PathLike, Path]
iSqlPathList = List[Union[str, os.PathLike, Path]]

class iSqlDF(pl.DataFrame):
    def __rich_repr__(self) -> rich.table.Table:
        records = orjson.loads(self.write_json(row_oriented=True))
        return tableFromRecords(records, theme="default").__rich_console__()
    def __rich_console__(self) -> rich.table.Table:
        records = orjson.loads(self.write_json(row_oriented=True))
        return tableFromRecords(records, theme="default").__rich_console__()
    
    def asRichTable(self):
        records = orjson.loads(self.write_json(row_oriented=True))
        return tableFromRecords(records, theme="default")



def check_sql(txt):
    return (
        'select' in txt.lower() or
        'insert' in txt.lower() or
        'update' in txt.lower() or
        'delete' in txt.lower() or 
        'create' in txt.lower() or
        'drop' in txt.lower() or
        'alter' in txt.lower()
    )

def checkError(raw : str) -> Union[bool, None]:
    """Check if the raw output of isql contains an error message."""
    pattern = r"Msg (\d+), Level (\d+), State (\d+):\nServer '([\w\d\-_]+)', Line (\d+):"
    
    if groups := re.search(pattern, raw):
        base = {
            "msg": groups.group(1),
            "level": groups.group(2),
            "state": groups.group(3),
            "server": groups.group(4),
            "line": groups.group(5),
        }
        idx = groups.span()[1]
        reason = raw[idx:].strip()

        errors.print(f"[bold red]Couldn't parse error message.\n{orjson.dumps(base, option=orjson.OPT_INDENT_2).decode()}[/]\n[bold yellow]Reason: [/][yellow]{reason}[/]")
        sys.exit(1)

    else:
        if (
            "invalid" in raw.lower()
            and "level" in raw.lower()
            and "state" in raw.lower()
            and "line" in raw.lower()
            ):

            base = {
                "msg": None,
                "level": None,
                "state": None,
                "server": None,
                "line": None,
            }
            reason = "Couldn't parse reason, but error is present."
            errors.print(f"[bold red]Couldn't parse error message.\n{orjson.dumps(base, option=orjson.OPT_INDENT_2).decode()}[/]\n[bold yellow]Reason: [/][yellow]{reason}[/]")
            sys.exit(1)
        else:
            return False
    

    
def format_sql_file(filename: Union[str, os.PathLike, Path]) -> None:
    """Format a SQL file. isql doesn't accept scripts with no `GO` statements at the end of each query."""
    content = open(filename, "r").read().lower().strip()
    if not check_sql(content):
        return filename
    elif content.endswith("go"):
        return filename
    else:
        open(filename, "a").write("\nGO")
        return
    
class iSQL:
    def __init__(
        self, 
        server: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        db: Optional[str] = None
        ) -> None:

        default_config = config['default']

        self.server = server or default_config['server']
        self.user = user or default_config['user']
        self.password = password or default_config['password']
        self.db = db or default_config['db']

        self.preprocess = None
        
        if not self.server or not self.user or not self.password:
            raise ValueError("Must provide server, user, and password")
        
    def run_sql_file(
        self,
        filename: Union[str, os.PathLike, Path],
        preprocess: Optional[bool] = True,
        ) -> pl.DataFrame:
        """Run a query and return the result as a list of tuples."""
        
        self.preprocess = preprocess
        
        self.command = [
            'isql',
            "-S", self.server,
            "-U", self.user,
            "-P", self.password,
            "-s", "';'",
            "-D", self.db,
            "-J", "utf8",
            "-X", # encrypt pwd
            "-i", filename
        ]
        
        format_sql_file(filename) # format the file if necessary
        
        self.result = subprocess.run(
            self.command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW,
            text=True,
            shell=True,
        )

        try:
            self.raw = self.result.stdout
            self.raw = self.decode('utf-8', errors='ignore') if isinstance(self.raw, bytes) else self.raw
        except Exception as err:
            raise err

        try:
            if preprocess:
                df = iSQL.strRowColSplitter(self.raw)
                return df
            else:
                return self.raw
        
        except Exception as err:
            raise err
        
    def query(
        self,
        query: str,
        preprocess: Optional[bool] = True,
        clean : Optional[bool] = True,
        ) -> Union[iSqlResponse, iSqlRecords, iSqlError]:
        """
        Run a query by storing it into a temporary .sql file
        and return the result as a list of tuples.
        """
        tmpdir = data_dir.joinpath('tmp')
        tmpdir.mkdir(exist_ok=True)
        filename = tmpdir.joinpath(f"tmp{uuid.uuid4()}.sql")

        open(filename, "w+", encoding='utf-8').write(query)
        
        try:
            return self.run_sql_file(
                file = filename,
                preprocess = preprocess
            )
        except Exception as err:
            if clean:
                filename.unlink(missing_ok=True)
            raise err
        finally:
            filename.unlink(missing_ok=True)

    @staticmethod
    def strRowColSplitter(raw: str) -> List[str]:
        """Split a raw string output into rows and columns."""

        checkError(raw)
        endings = ["row affected)", "rows affected)"]
        for end in endings:
            idx = raw.rfind(end)
            if idx != -1:
                jdx = raw.rfind("(")
                raw = raw[:jdx]

        output = re.sub(r"( [ ]+)", " ", raw).strip()

        unicode = r"-"
        dbunicode = r"--"
        startcols = output.find(unicode)
        endcols = output.rfind(dbunicode)
        rawcols = output[:startcols]
        rawrows = output[endcols:]

        rawcols = re.sub(r"(\s+)", ";;", rawcols)
        cols = re.split(r"(;;|')", rawcols)
        cols = [ col for col in cols if col.strip() not in ["", ";;", "'"]]

        ko_rows = []
        ok_rows = []
        rawrows_aslist = rawrows.split("\'\n\'")
        rawrows_aslist = [ row for row in rawrows_aslist if set(row) != set("-") and row.strip() not in ["", "''"]]
        rawrows_aslist = list(map(lambda row: re.sub(r"(\n\t)", ";", row), rawrows_aslist))
        rawrows_aslist = list(map(lambda row: re.sub(r"(\d+)'", r"\1;", re.sub(r"(NULL')", "NULL;", row)), rawrows_aslist))

        if len(rawrows_aslist) == 1:
            row = rawrows_aslist[0]
            cols = cols if len(cols) else None
            if ";" in row and cols:
                return iSqlDF([{col: rs.strip() for col,rs in zip(cols,row.split(";")) if rs.strip() != ""}], orient="row")
            elif ";" in row and not cols:
                return iSqlDF([[rs.strip() for rs in row.split(";") if rs.strip() != ""]], orient="row")
            else:
                return iSqlDF([[row]], columns=cols[0], orient="row")

        result_rows = [ [v.strip() for v in row.split(";")] for row in rawrows_aslist ]
        df = iSqlDF(result_rows, columns=cols, orient="row")

        return df

    def multiquery(self, queries_source: Union[str, os.PathLike, Path]) -> List[iSqlDF]:
        """Run multiple queries and return the result as a list of pl.DataFrames"""
        if isinstance(queries_source, (Path, os.PathLike, str, list)):
            if not isinstance(queries_source, list):
                if Path(queries_source).is_dir():
                    queries = list(Path(queries_source).glob("*.sql"))
                else:
                    queries = [queries_source]
            if isinstance(queries_source, list):
                queries = []
                for query in queries_source:
                    if Path(query).is_dir():
                        queries += list(Path(query).glob("*.sql"))
                    else:
                        queries.append(query)
        else:
            raise TypeError(f"queries_source must be a string, a Path or a directory name, not {type(queries_source)}")
        callbacks = [self.run_sql_file for _ in range(len(queries))]
        return rich_func_chainer(callbacks, params=queries)

    def __repr__(self) -> str:
        return f"<iSQL: {self.server}>"
    
    def __str__(self) -> str:
        return self.__repr__()

    def __enter__(self):
        return self

    def copy(self, deep: Optional[bool] = False):
        return copy.deepcopy(self) if deep else copy.copy(self)

    def __or__(self, other):
        return self.copy().query(other)

    def __ror__(self, other):
        return self.copy().query(other)

    def __gt__(self, other):
        return self.copy().query(other)
    
    def __lt__(self, other):
        return self.copy().query(other)

    def __rshift__(self, queries_source: Union[str, os.PathLike, Path]) -> List[pl.DataFrame]:
        """Pipes a list of .sql files or a directory name to the pisql 🐍 command 🦾"""
        return self.multiquery(queries_source)

    def __rshift__(self, queries_source: Union[str, os.PathLike, Path]) -> List[pl.DataFrame]:
        """Pipes a list of .sql files or a directory name to the pisql 🐍 command 🦾"""
        return self.multiquery(queries_source)
        