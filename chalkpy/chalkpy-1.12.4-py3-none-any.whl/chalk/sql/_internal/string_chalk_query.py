from typing import Any, Mapping, Optional, Union

from sqlalchemy import text
from sqlalchemy.sql.elements import TextClause

from chalk.features import Feature
from chalk.sql.finalized_query import FinalizedChalkQuery, Finalizer
from chalk.sql.protocols import BaseSQLSourceProtocol, IncrementalSettings, StringChalkQueryProtocol
from chalk.utils.duration import Duration, parse_chalk_duration


class StringChalkQuery(StringChalkQueryProtocol):
    def __init__(
        self,
        source: BaseSQLSourceProtocol,
        params: Mapping[str, Any],
        query: Union[str, TextClause],
        fields: Mapping[str, Feature],
    ):
        self._source = source
        self._query = text(query) if isinstance(query, str) else query
        self._params = params
        self._fields = {k: Feature.from_root_fqn(v) if isinstance(v, str) else v for (k, v) in fields.items()}

    def __repr__(self):
        return f"StringChalkQuery(query='{self._query}')"

    def one_or_none(self):
        return FinalizedChalkQuery(
            query=self._query,
            params=self._params,
            finalizer=Finalizer.ONE_OR_NONE,
            incremental_settings=None,
            source=self._source,
            fields=self._fields,
        )

    def one(self):
        return FinalizedChalkQuery(
            query=self._query,
            params=self._params,
            finalizer=Finalizer.ONE_OR_NONE,
            incremental_settings=None,
            source=self._source,
            fields=self._fields,
        )

    def first(self):
        return FinalizedChalkQuery(
            query=self._query,
            params=self._params,
            finalizer=Finalizer.FIRST,
            incremental_settings=None,
            source=self._source,
            fields=self._fields,
        )

    def all(self):
        return FinalizedChalkQuery(
            query=self._query,
            params=self._params,
            finalizer=Finalizer.ALL,
            incremental_settings=None,
            source=self._source,
            fields=self._fields,
        )

    def incremental(
        self,
        *,
        incremental_column: Optional[str] = None,
        lookback_period: Duration = "0s",
        mode: str = "row",
    ):
        if mode in {"row", "group"} and incremental_column is None:
            raise ValueError(f"incremental mode set to '{mode}' but no 'incremental_column' argument was passed.")

        if mode == "parameter" and incremental_column is not None:
            raise ValueError(
                f"incremental mode set to '{mode}' but 'incremental_column' argument was passed."
                + " Please view documentation for proper usage."
            )

        return FinalizedChalkQuery(
            query=self._query,
            params=self._params,
            finalizer=Finalizer.ALL,
            incremental_settings=IncrementalSettings(
                lookback_period=(
                    parse_chalk_duration(lookback_period) if isinstance(lookback_period, str) else lookback_period
                ),
                incremental_column=None if incremental_column is None else incremental_column,
                mode=mode,
            ),
            source=self._source,
            fields=self._fields,
        )
