from dataclasses import (
    dataclass,
)
from fa_purity import (
    Maybe,
    PureIter,
    Stream,
)
from fa_purity.cmd import (
    Cmd,
)
from fa_purity.frozen import (
    FrozenDict,
    FrozenList,
)
from fa_purity.pure_iter.factory import (
    from_flist,
    infinite_range,
)
from fa_purity.stream.factory import (
    from_piter,
)
from fa_purity.stream.transform import (
    chain,
    until_empty,
)
from logging import (
    Logger,
)
from psycopg2 import (
    extras,
)
from redshift_client.sql_client import (
    _assert,
)
from redshift_client.sql_client.connection import (
    DbConnection,
)
from redshift_client.sql_client.primitive import (
    PrimitiveVal,
)
from redshift_client.sql_client.query import (
    Query,
)
from typing import (
    Any,
    Optional,
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from psycopg2 import (
        cursor as CursorStub,
    )
else:
    CursorStub = Any


@dataclass(frozen=True)
class RowData:
    data: FrozenList[PrimitiveVal]


@dataclass(frozen=True)
class QueryValues:
    values: FrozenDict[str, PrimitiveVal]


@dataclass(frozen=True)
class SqlClient:
    _log: Logger
    _cursor: CursorStub

    def execute(self, query: Query, args: Optional[QueryValues]) -> Cmd[None]:
        _values = args.values if args else FrozenDict({})
        preview: str = self._cursor.mogrify(query._inner.statement, _values)  # type: ignore[no-untyped-call]

        def _action() -> None:
            self._log.debug("Executing: %s", preview)
            self._cursor.execute(query._inner.statement, _values)

        return Cmd.from_cmd(_action)

    def batch(self, query: Query, args: FrozenList[QueryValues]) -> Cmd[None]:
        def _action() -> None:
            _args = tuple(v.values for v in args)
            self._log.debug(
                "Batch execution (%s items): %s",
                len(_args),
                query._inner.statement,
            )
            extras.execute_batch(self._cursor, query._inner.statement, _args)

        return Cmd.from_cmd(_action)

    def values(
        self, query: Query, args: PureIter[RowData], limit: int
    ) -> Cmd[None]:
        def _action() -> None:
            self._log.debug(
                "Executing query over values: %s", query._inner.statement
            )
            _args = args.map(lambda r: r.data)
            extras.execute_values(
                self._cursor, query._inner.statement, _args, page_size=limit
            )

        return Cmd.from_cmd(_action)

    def fetch_one(self) -> Cmd[Maybe[RowData]]:
        def _action() -> Maybe[RowData]:
            self._log.debug("Fetching one row")
            return Maybe.from_optional(
                _assert.assert_fetch_one(self._cursor.fetchone())  # type: ignore[misc]
            ).map(RowData)

        return Cmd.from_cmd(_action)

    def fetch_all(self) -> Cmd[FrozenList[RowData]]:
        def _action() -> FrozenList[RowData]:
            self._log.debug("Fetching all rows")
            items = _assert.assert_fetch_list(tuple(self._cursor.fetchall()))  # type: ignore[misc]
            return tuple(map(RowData, items))

        return Cmd.from_cmd(_action)

    def fetch_many(self, chunk: int) -> Cmd[FrozenList[RowData]]:
        def _action() -> FrozenList[RowData]:
            self._log.debug("Fetching %s rows", chunk)
            items = _assert.assert_fetch_list(tuple(self._cursor.fetchmany(chunk)))  # type: ignore[misc]
            return tuple(map(RowData, items))

        return Cmd.from_cmd(_action)

    def data_chunks_stream(self, chunk: int) -> Stream[FrozenList[RowData]]:
        return (
            infinite_range(0, 1)
            .map(
                lambda _: self.fetch_many(chunk).map(
                    lambda i: Maybe.from_optional(i if i else None)
                )
            )
            .transform(lambda i: from_piter(i))
            .transform(lambda i: until_empty(i))
        )

    def data_stream(self, chunk: int) -> Stream[RowData]:
        return (
            self.data_chunks_stream(chunk)
            .map(lambda i: from_flist(i))
            .transform(lambda i: chain(i))
        )


def new_client(connection: DbConnection, log: Logger) -> Cmd[SqlClient]:
    def _action() -> SqlClient:
        return SqlClient(log, connection._inner._connection.cursor())

    return Cmd.from_cmd(_action)


__all__ = [
    "Query",
    "DbConnection",
]
