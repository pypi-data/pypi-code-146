from __future__ import annotations

from os import PathLike
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Literal,
    Mapping,
    Optional,
    Protocol,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

import pyarrow as pa
from sqlalchemy.engine import URL, Engine
from sqlalchemy.orm import Session

from chalk.features import DataFrame, Feature, Features, FeatureWrapper
from chalk.sql._internal.incremental import IncrementalSettings
from chalk.utils.duration import Duration

if TYPE_CHECKING:
    from chalk.sql.finalized_query import FinalizedChalkQuery

TTableIngestProtocol = TypeVar("TTableIngestProtocol", bound="TableIngestProtocol")


class StringChalkQueryProtocol(Protocol):
    def execute(self) -> DataFrame:
        """
        Materialize the query. Chalk queries are lazy, which allows Chalk
        to perform performance optimizations like push-down filters.
        Instead of calling execute, consider returning this query from
        a resolver as an intermediate feature, and processing that
        intermediate feature in a different resolver.
        """
        ans = self.all().execute()
        assert isinstance(ans, DataFrame)
        return ans

    def one_or_none(self) -> FinalizedChalkQuery:
        """
        Return at most one result or raise an exception.
        Returns None if the query selects no rows. Raises if
        multiple object identities are returned, or if multiple
        rows are returned for a query that returns only scalar
        values as opposed to full identity-mapped entities.
        """
        ...

    def one(self) -> FinalizedChalkQuery:
        """
        Return exactly one result or raise an exception.
        """
        ...

    def all(self) -> FinalizedChalkQuery:
        """
        Return the results represented by this Query as a list.
        :return:
        """
        ...

    @overload
    def incremental(
        self,
        *,
        incremental_column: str,
        lookback_period: Duration = "0s",
        mode: Literal["row", "group"] = "row",
    ) -> FinalizedChalkQuery:
        ...

    @overload
    def incremental(
        self,
        *,
        incremental_column: None = None,
        lookback_period: None = None,
        mode: Literal["parameter"],
    ) -> FinalizedChalkQuery:
        ...

    def incremental(
        self,
        *,
        incremental_column: Optional[str] = None,
        lookback_period: Optional[Duration] = "0s",
        mode: Literal["row", "group", "parameter"] = "row",
    ) -> FinalizedChalkQuery:
        """
        Operates like `all()`, but tracks "previous_latest_row_timestamp" between query executions in
        order to limit the amount of data returned.

        "previous_latest_row_timestamp" will be set the start of the query execution, or if you return
        a "feature_time"-mapped column, Chalk will update "previous_latest_row_timestamp" to the maximum
        observed "feature_time" value.

        In "row" mode:
            "incremental_column" MUST be set.

            Returns the results represented by this query as a list (like `.all()`), but modifies the query to
            only return "new" results, by adding a clause that looks like:

            "WHERE <incremental_column> >= <previous_latest_row_timestamp> - <lookback_period>"

        In "group" mode:
            "incremental_column" MUST be set.

            Returns the results represented by this query as a list (like `.all()`), but modifies the query to
            only results from "groups" which have changed since the last run of the query.

            This works by (1) parsing your query, (2) finding the "group keys", (3) selecting only changed groups.
            Concretely:

            SELECT
                user_id, sum(amount) as sum_amount
            FROM payments
            GROUP BY user_id

            would be rewritten like this:

            SELECT
                user_id, sum(amount) as sum_amount
            FROM payments
            **
            WHERE user_id in
                (
                 SELECT DISTINCT(user_id)
                 FROM payments WHERE created_at >= <previous_latest_row_timestamp> - <lookback_period>
                )
            **
            GROUP BY user_id

        In "parameter" mode:
            incremental_column WILL BE IGNORED.

            This mode is for cases where you want full control of incrementalization. Chalk will not manipulate your query.
            Chalk will include a query parameter named "chalk_incremental_timestamp". Depending on your SQL
            dialect, you can use this value to incrementalize your query with ":chalk_incremental_timestamp" or
            "%(chalk_incremental_timestamp)s".

        :param incremental_column: This should reference a timestamp column in your underlying table, typically something
                                like "updated_at", "created_at", "event_time", etc.
        :param lookback_period: Defaults to "0", which means we only return rows that are strictly newer than
                                the last observed row.
        :param mode: Defaults to "row", which indicates that only "rows" newer than the last observed row should be
                     considered. When set to "group", Chalk will only ingest features from "groups" which are newer
                     than the last observation time. This requires that the query is grouped by a primary key.
        :return:
        """
        ...


class ChalkQueryProtocol(Protocol):
    def first(self) -> FinalizedChalkQuery:
        """
        Return the first result of this Query or None if the result doesn't contain any row.
        :return:
        """
        ...

    def one_or_none(self) -> FinalizedChalkQuery:
        """
        Return at most one result or raise an exception.
        Returns None if the query selects no rows. Raises if
        multiple object identities are returned, or if multiple
        rows are returned for a query that returns only scalar
        values as opposed to full identity-mapped entities.
        """
        ...

    def one(self) -> FinalizedChalkQuery:
        """
        Return exactly one result or raise an exception.
        """
        ...

    def all(self) -> FinalizedChalkQuery:
        """
        Return the results represented by this Query as a DataFrame.
        """
        ...

    def incremental(
        self,
        lookback_period: Duration = "0s",
        mode: str = "row",
        incremental_column: Optional[Union[str, Feature]] = None,
    ) -> FinalizedChalkQuery:
        """

        Operates like `all()`, but tracks "previous_latest_row_timestamp" between query executions in
        order to limit the amount of data returned.

        "previous_latest_row_timestamp" will be set the start of the query execution, or if you return
        a "feature_time"-mapped column, Chalk will update "previous_latest_row_timestamp" to the maximum
        observed "feature_time" value.

        In "row" mode:
            "incremental_column" MUST be set.

            Returns the results represented by this query as a list (like `.all()`), but modifies the query to
            only return "new" results, by adding a clause that looks like:

            "WHERE <incremental_column> >= <previous_latest_row_timestamp> - <lookback_period>"

        In "group" mode:
            "incremental_column" MUST be set.

            Returns the results represented by this query as a list (like `.all()`), but modifies the query to
            only results from "groups" which have changed since the last run of the query.

            This works by (1) parsing your query, (2) finding the "group keys", (3) selecting only changed groups.
            Concretely:

            SELECT
                user_id, sum(amount) as sum_amount
            FROM payments
            GROUP BY user_id

            would be rewritten like this:

            SELECT
                user_id, sum(amount) as sum_amount
            FROM payments
            **
            WHERE user_id in
                (
                 SELECT DISTINCT(user_id)
                 FROM payments WHERE created_at >= <previous_latest_row_timestamp> - <lookback_period>
                )
            **
            GROUP BY user_id

        In "parameter" mode:
            incremental_column WILL BE IGNORED.

            This mode is for cases where you want full control of incrementalization. Chalk will not manipulate your query.
            Chalk will include a query parameter named "chalk_incremental_timestamp". Depending on your SQL
            dialect, you can use this value to incrementalize your query with ":chalk_incremental_timestamp" or
            "%(chalk_incremental_timestamp)s".

        :param incremental_column: Defaults to the column mapped to the "feature_time" feature for this feature class.
                                This should reference a timestamp column in your underlying table, typically something
                                like "updated_at", "created_at", "event_time", etc.
        :param mode: Defaults to "row", which indicates that only "rows" newer than the last observed row should be considered.
                     When set to "group", Chalk will only ingest features from "groups" which are newer than the last
                     observation time. This requires that the query is grouped by a primary key.
        :param lookback_period: Defaults to "0", which means we only return rows that are strictly newer than
                                the last observed row.
        :return:
        """

        ...

    def filter_by(self, **kwargs: Any) -> "ChalkQueryProtocol":
        """
        Apply the given filtering criterion to a copy of this Query, using keyword expressions.
        eg:
            session.query(UserFeatures(id=UserSQL.id)).filter_by(name="Maria")

        :param kwargs: the column names assigned to the desired values (ie. name="Maria")
        :return:
        """

        ...

    def filter(self, *criterion: Any) -> "ChalkQueryProtocol":
        """
        Apply the given filtering criterion to a copy of this Query, using SQL expressions.

        :param criterion: SQLAlchemy filter criterion
        :return:
        """
        ...

    def order_by(self, *clauses: Any) -> "ChalkQueryProtocol":
        """
        Apply one or more ORDER BY criteria to the query and return the newly resulting Query.

        :param clauses: SQLAlchemy columns
        """
        ...

    def group_by(self, *clauses: Any) -> "ChalkQueryProtocol":
        ...

    def having(self, criterion: Any) -> "ChalkQueryProtocol":
        ...

    def union(self, *q: "ChalkQueryProtocol") -> "ChalkQueryProtocol":
        ...

    def union_all(self, *q: "ChalkQueryProtocol") -> "ChalkQueryProtocol":
        ...

    def intersect(self, *q: "ChalkQueryProtocol") -> "ChalkQueryProtocol":
        ...

    def intersect_all(self, *q: "ChalkQueryProtocol") -> "ChalkQueryProtocol":
        ...

    def join(self, target: Any, *props: Any, **kwargs: Any) -> "ChalkQueryProtocol":
        ...

    def outerjoin(self, target: Any, *props: Any, **kwargs: Any) -> "ChalkQueryProtocol":
        ...

    def select_from(self, *from_obj: Any) -> "ChalkQueryProtocol":
        ...

    def execute(self):
        """
        Materialize the query. Chalk queries are lazy, which allows Chalk
        to perform performance optimizations like push-down filters.
        Instead of calling execute, consider returning this query from
        a resolver as an intermediate feature, and processing that
        intermediate feature in a different resolver.
        """
        return self.all().execute()


class BaseSQLSourceProtocol(Protocol):
    def query_string(
        self,
        query: str,
        fields: Optional[Mapping[str, Union[Feature, FeatureWrapper, str, Any]]] = None,
        args: Optional[Mapping[str, str]] = None,
    ) -> StringChalkQueryProtocol:
        """
        Run a query from a SQL string.
        :param query: The query that you'd like to run
        :param fields: A mapping from the column names selected to features.
        :param args: Any args in the sql string specified by `query` need
          to have corresponding value assignments in `args`.
        :return:
        """
        ...

    def query_sql_file(
        self,
        path: Union[str, bytes, PathLike],
        fields: Optional[Mapping[str, Union[Feature, FeatureWrapper, str, Any]]] = None,
        args: Optional[Mapping[str, str]] = None,
    ) -> StringChalkQueryProtocol:
        """
        Run a query from a .sql file

        :param path: The path to the file with the sql file,
                     relative to the caller's file, or to the
                     directory that you chalk.yaml file lives in.
        :param fields: A mapping from the column names selected to features.
        :param args: Any args in the sql file specified by `path` need
          to have corresponding value assignments in `args`.
        """
        ...

    def query(self, *entities: Any) -> ChalkQueryProtocol:
        """
        Query using a SQLAlchemy model
        """
        ...

    def local_engine_url(self) -> URL:
        ...

    def engine_args(self) -> Mapping[str, Any]:
        return {}

    def get_engine(self) -> Engine:
        """Get an SQLAlchemy Engine. The engine will be created and cached on the first call of this method."""
        ...

    def warm_up(self) -> None:
        """Warm up the Engine by issuing a simple query."""
        ...

    def raw_session(self) -> Session:
        ...

    def execute_query(self, finalized_query: FinalizedChalkQuery, connection: Optional[Any] = None) -> pa.Table:
        """Execute a query to a PyArrow table"""
        ...

    def compile_query(self, finalized_query: FinalizedChalkQuery) -> Tuple[str, Sequence[Any], Mapping[str, Any]]:
        """Compile a query into a string and the (positional parameters, named parameters)"""
        ...


class TableIngestProtocol(Protocol):
    def with_table(
        self: Type[TTableIngestProtocol],
        *,
        name: str,
        features: Type[Union[Features, Any]],
        ignore_columns: Optional[List[str]] = None,
        ignore_features: Optional[List[Union[str, Any]]] = None,
        require_columns: Optional[List[str]] = None,
        require_features: Optional[List[Union[str, Any]]] = None,
        column_to_feature: Optional[Dict[str, Any]] = None,
        cdc: Optional[Union[bool, IncrementalSettings]] = None,
    ) -> TTableIngestProtocol:
        # Allowing Type[Any] for `features` as IDEs won't know that @features classes
        # "inherit" from Features
        ...


class SQLSourceWithTableIngestProtocol(TableIngestProtocol, BaseSQLSourceProtocol, Protocol):
    ...


__all__ = [
    "StringChalkQueryProtocol",
    "ChalkQueryProtocol",
    "BaseSQLSourceProtocol",
    "TableIngestProtocol",
    "SQLSourceWithTableIngestProtocol",
]
