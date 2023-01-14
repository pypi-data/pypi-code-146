from typing import Any, List, Mapping, Optional, Union

from sqlalchemy.orm import Query
from sqlalchemy.sql import Select

from chalk.features import Feature
from chalk.sql.finalized_query import FinalizedChalkQuery, Finalizer
from chalk.sql.protocols import BaseSQLSourceProtocol, ChalkQueryProtocol, IncrementalSettings
from chalk.utils.duration import Duration, parse_chalk_duration


class ChalkQuery(ChalkQueryProtocol):
    def __init__(
        self,
        features: Mapping[str, Feature],
        targets: List[Any],
        source: BaseSQLSourceProtocol,
    ):
        self._query = Query(entities=targets)
        self._features = features
        self._source = source

    def first(self, params: Optional[Mapping[str, Any]] = None):
        self._query = self._query.limit(1)
        assert isinstance(self._query.selectable, Select), "A text query's selectable should always be a Select"
        return FinalizedChalkQuery(
            query=self._query.selectable,
            finalizer=Finalizer.FIRST,
            source=self._source,
            incremental_settings=None,
            params=params or {},
            fields=self._features,
        )

    def one_or_none(self, params: Optional[Mapping[str, Any]] = None):
        self._query = self._query.limit(1)
        assert isinstance(self._query.selectable, Select), "A text query's selectable should always be a Select"
        return FinalizedChalkQuery(
            query=self._query.selectable,
            finalizer=Finalizer.ONE_OR_NONE,
            source=self._source,
            incremental_settings=None,
            params=params or {},
            fields=self._features,
        )

    def one(self, params: Optional[Mapping[str, Any]] = None):
        self._query = self._query.limit(1)
        assert isinstance(self._query.selectable, Select), "A text query's selectable should always be a Select"
        return FinalizedChalkQuery(
            query=self._query.selectable,
            finalizer=Finalizer.ONE,
            source=self._source,
            incremental_settings=None,
            params=params or {},
            fields=self._features,
        )

    def all(self, params: Optional[Mapping[str, Any]] = None):
        assert isinstance(self._query.selectable, Select), "A text query's selectable should always be a Select"
        return FinalizedChalkQuery(
            query=self._query.selectable,
            finalizer=Finalizer.ALL,
            source=self._source,
            incremental_settings=None,
            params=params or {},
            fields=self._features,
        )

    def incremental(
        self,
        lookback_period: Duration = "0s",
        mode: str = "row",
        incremental_column: Optional[Union[str, Feature]] = None,
        params: Optional[Mapping[str, Any]] = None,
    ):
        assert isinstance(self._query.selectable, Select)
        return FinalizedChalkQuery(
            query=self._query.selectable,
            finalizer=Finalizer.ALL,
            source=self._source,
            incremental_settings=IncrementalSettings(
                lookback_period=(
                    parse_chalk_duration(lookback_period) if isinstance(lookback_period, str) else lookback_period
                ),
                incremental_column=None if incremental_column is None else str(incremental_column),
                mode=mode,
            ),
            params=params or {},
            fields=self._features,
        )

    def filter_by(self, **kwargs: Any):
        self._query = self._query.filter_by(**kwargs)
        return self

    def filter(self, *criterion: Any):
        self._query = self._query.filter(*criterion)
        return self

    def limit(self, *limits: Any):
        self._query = self._query.limit(*limits)
        return self

    def order_by(self, *clauses: Any):
        self._query = self._query.order_by(*clauses)
        return self

    def group_by(self, *clauses: Any):
        self._query = self._query.group_by(*clauses)
        return self

    def having(self, criterion: Any):
        self._query = self._query.having(*criterion)
        return self

    def union(self, *q: Any):
        self._query = self._query.union(*q)
        return self

    def union_all(self, *q: Any):
        self._query = self._query.union_all(*q)
        return self

    def intersect(self, *q: Any):
        self._query = self._query.intersect(*q)
        return self

    def intersect_all(self, *q: Any):
        self._query = self._query.intersect_all(*q)
        return self

    def join(self, target: Any, *props: Any, **kwargs: Any):
        self._query = self._query.join(target, *props, **kwargs)
        return self

    def outerjoin(self, target: Any, *props: Any, **kwargs: Any):
        self._query = self._query.outerjoin(target, *props, **kwargs)
        return self

    def select_from(self, *from_obj: Any):
        self._query = self._query.select_from(*from_obj)
        return self
