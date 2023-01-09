from os import PathLike
from typing import Any, Dict, TypeVar, Union

from sqlalchemy.engine.url import URL

from chalk.sql._internal.sql_source import BaseSQLSource, TableIngestMixIn
from chalk.sql.protocols import SQLSourceWithTableIngestProtocol

T = TypeVar("T")


class SQLiteInMemorySourceImpl(TableIngestMixIn, BaseSQLSource, SQLSourceWithTableIngestProtocol):
    def __init__(self):
        super(SQLiteInMemorySourceImpl, self).__init__()
        self.ingested_tables: Dict[str, Any] = {}

    def local_engine_url(self) -> URL:
        return URL.create(drivername="sqlite", database=":memory:", query={"check_same_thread": "true"})


class SQLiteFileSourceImpl(TableIngestMixIn, BaseSQLSource, SQLSourceWithTableIngestProtocol):
    def __init__(self, filename: Union[PathLike, str]):
        self.filename = str(filename)
        self.ingested_tables: Dict[str, Any] = {}
        super(SQLiteFileSourceImpl, self).__init__()

    def local_engine_url(self) -> URL:
        return URL.create(drivername="sqlite", database=self.filename, query={"check_same_thread": "true"})
