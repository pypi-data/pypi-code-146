from __future__ import annotations

import warnings
from enum import Enum
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

from sqlalchemy.sql import Select
from sqlalchemy.sql.elements import TextClause

from chalk.features import DataFrame, Feature, Features, FeatureWrapper, ensure_feature
from chalk.sql._internal.incremental import IncrementalSettings
from chalk.sql.protocols import BaseSQLSourceProtocol
from chalk.utils.missing_dependency import missing_dependency_exception
from chalk.utils.string import normalize_string_for_matching


class Finalizer(str, Enum):
    ONE_OR_NONE = "OneOrNone"
    ONE = "One"
    FIRST = "First"
    ALL = "All"


def _get_matching_root_fqn(normalized_col_name: str, expected_features: Sequence[Feature]) -> Optional[str]:
    candidates: List[str] = []
    for x in expected_features:
        root_fqn_normalized = normalize_string_for_matching(x.root_fqn.lower())
        without_root_ns = normalize_string_for_matching(".".join(x.root_fqn.split(".")[1:]))
        if normalized_col_name == root_fqn_normalized or normalized_col_name == without_root_ns:
            candidates.append(x.root_fqn)
    if len(candidates) == 0:
        return None
    if len(candidates) > 1:
        # We really shouldn't hit this, unless if features are case-sensitive and the user is querying
        # snowflake which is case-insensitive
        raise ValueError(
            (
                f"Column '{normalized_col_name}' was ambiguous which feature it referred to. "
                f"Possible candidates were: {candidates}"
            )
        )
    return candidates[0]


class FinalizedChalkQuery:
    def __init__(
        self,
        query: Union[Select, TextClause],
        params: Mapping[str, Any],
        finalizer: Finalizer,
        incremental_settings: Optional[IncrementalSettings],
        source: BaseSQLSourceProtocol,
        fields: Mapping[str, Feature],
    ) -> None:
        self._query = query
        self._params = dict(params)
        self._finalizer = finalizer
        self._incremental_settings = incremental_settings
        self._source = source
        self._fields = fields

    @property
    def incremental_settings(self):
        return self._incremental_settings

    @property
    def finalizer(self):
        return self._finalizer

    @property
    def query(self):
        return self._query

    @property
    def source(self):
        return self._source

    @property
    def fields(self):
        return self._fields

    @property
    def params(self):
        return self._params

    def execute(
        self,
        expected_features: Optional[Sequence[Feature]] = None,
        connection: Optional[Any] = None,
    ) -> Union[Features, DataFrame, None]:
        """Actually execute the query.

        If the finalizer was ONE, ONE_OR_NONE, or FIRST, then a :class:`Features` instance
        is returned. Otherwise, if the `finalizer` is ALL, then a :class:`.DataFrame` instance is returned

        Args:
            expected_features: The list of expected features for the output, as provided by the resovler in which this query is executed.
                If not specified, then then the column names as returned by the query will be used to determine the output features.
            connection: Execute the query using the supplied connection. If None (the default), then a new connection will be acquired
                from the underlying source for the query

        Returns:
            A DataFrame, if the :attr:`.finalizer` is ALL; otherwise, :class:`Features` set. If the finalizer is ONE_OR_NONE or FIRST,
            then the result may be None if no row was found
        """
        res = self.execute_to_dataframe(expected_features, connection)

        if self._finalizer in (Finalizer.ONE_OR_NONE, Finalizer.FIRST) and len(res) == 0:
            return None
        if self._finalizer in (Finalizer.ONE, Finalizer.ONE_OR_NONE, Finalizer.FIRST):
            return res.slice(0, 1).to_features()[0]
        return res

    def execute_to_dataframe(
        self,
        expected_features: Optional[Sequence[Feature]] = None,
        connection: Optional[Any] = None,
    ) -> DataFrame:
        """Actually execute the query, and return a DataFrame. Unlike :meth:`.execute`, this method will always keep the results
        as a DataFrame, even if the finalizer implies a singleton results (e.g. ONE, ONE_OR_NONE, or FIRST).

        Args:
            Same as :meth:`.execute`
        Returns:
            A dataframe, even if the result contains 0 or 1 rows.
        """
        try:
            import polars as pl
        except ImportError:
            raise missing_dependency_exception("chalkpy[polars]")
        if self.incremental_settings is not None:
            # FIXME: Move the incrementalization logic here, so then the `execute` and `execute_to_dataframe`
            # methods can take the hwm timestamp as a paramater, to allow for direct execution
            warnings.warn(
                (
                    "This query specified an incremental configuration, which has not been applied. "
                    "This is likely because the resolver is being executed directly. "
                    "The query will be attempted without any high-water-mark timestamp. This will attempt to select all data, "
                    "or if the filters depend on the incremental timestamp, will result in a query execution error. "
                )
            )
        pa_table = self.source.execute_query(self, connection)
        col_name_mapping = self.get_col_name_mapping(pa_table.column_names, expected_features)
        pa_table = pa_table.select(col_name_mapping.keys())
        pa_table = pa_table.rename_columns([col_name_mapping[x] for x in pa_table.column_names])
        df = pl.from_arrow(pa_table)
        assert isinstance(df, pl.DataFrame)

        if self._finalizer == Finalizer.ONE:
            if len(df) != 1:
                raise ValueError(f"Expected exactly one row; got {len(df)} rows")

        if self._finalizer == Finalizer.ONE_OR_NONE:
            if len(df) > 1:
                raise ValueError(f"Expected zero or one rows; got {len(df)} rows")

        if self._finalizer in (Finalizer.ONE, Finalizer.ONE_OR_NONE, Finalizer.FIRST):
            df = df.slice(0, 1)

        return DataFrame(df)

    def get_col_name_mapping(
        self,
        result_columns: List[str],
        expected_features: Optional[Sequence[Union[str, Feature, FeatureWrapper]]],
    ):
        """Map the output columns to the expected feature fqns

        Args:
            result_columns: A list of the columns, in order, returned by the query.
            expected_features: The expected features for the query, as provided by the resolver signature. If a column name that is not
            in ``fields`` corresponds to a column in ``expected_features``, then it will be mapped automatically. If a feature in
                ``expected_features`` does not have a corresponding output column,  an error is raised.
        Returns:
            A mapping from output column names to root fqns
        """
        ans: Dict[str, str] = {}
        normalized_to_original_col = {normalize_string_for_matching(x): x for x in result_columns}
        for (k, v) in self._fields.items():
            original_col_name = normalized_to_original_col.get(normalize_string_for_matching(k))
            if original_col_name is None:
                raise ValueError(f"Column {k} was not returned by the query.")
            ans[original_col_name] = v.root_fqn
        if expected_features is not None:
            unexpected_fields = [x for x in self._fields.values() if x not in expected_features]
            if len(unexpected_fields) > 0:
                raise ValueError(
                    f"Fields {unexpected_fields} were in the field mapping but are not included in the resolver output signature."
                )
            expected_features = [ensure_feature(y) for y in expected_features]
            for normalized_col_name, original_col_name in normalized_to_original_col.items():
                if original_col_name not in ans:
                    maybe_matching_root_fqn = _get_matching_root_fqn(normalized_col_name, expected_features)
                    if maybe_matching_root_fqn is not None:
                        ans[original_col_name] = maybe_matching_root_fqn
        return ans
