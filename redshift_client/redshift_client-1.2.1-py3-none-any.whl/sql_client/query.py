from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from deprecated import (
    deprecated,
)
from fa_purity.frozen import (
    FrozenDict,
)
from psycopg2.sql import (
    Identifier,
    SQL,
)
from typing import (
    cast,
)


def _purifier(statement: str, identifiers: FrozenDict[str, str]) -> SQL:
    raw_sql = SQL(statement)
    safe_args = FrozenDict(
        {key: Identifier(value) for key, value in identifiers.items()}
    )
    return cast(SQL, raw_sql.format(**safe_args))  # type: ignore[no-untyped-call]


def _pretty(raw: str) -> str:
    return " ".join(raw.strip(" \n\t").split())


@dataclass(frozen=True)
class _Query:
    statement: SQL


@dataclass(frozen=True)
class Query:
    _inner: _Query

    @staticmethod
    def new_query(stm: str) -> Query:
        draft = _Query(SQL(_pretty(stm)))
        return Query(draft)

    @staticmethod
    def dynamic_query(stm: str, identifiers: FrozenDict[str, str]) -> Query:
        draft = _Query(_purifier(_pretty(stm), identifiers))
        return Query(draft)


new_query = deprecated(reason="Use Query.new_query instead")(Query.new_query)
dynamic_query = deprecated(reason="Use Query.dynamic_query")(
    Query.dynamic_query
)
