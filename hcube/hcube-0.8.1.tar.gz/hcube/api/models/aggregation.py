from enum import Enum
from typing import Dict, List, Optional, Union

from hcube.api.exceptions import ConfigurationError
from hcube.api.models.dimensions import Dimension
from hcube.api.models.filters import Filter
from hcube.api.models.metrics import Metric


class AggregationOp(Enum):
    """
    Defines different aggregation operations which each cube backend should implement.
    """

    SUM = "sum"
    COUNT = "count"
    MAX = "max"
    MIN = "min"
    ARRAY = "array"


class Aggregation:

    allow_metric_none = False

    def __init__(
        self,
        metric: Union[str, Metric],
        op: AggregationOp,
        name: Optional[str] = None,
        distinct: Optional[Union[str, Dimension]] = None,
        filters: Optional[List[Union[Filter, Dict]]] = None,
    ):
        """
        If `filter` is given, it should be applied to each maching row before the aggregation
        and only matching rows should be aggregated.
        """
        self.metric = metric
        self.op: AggregationOp = op
        self.name: str = name if name else op.value
        self.distinct = distinct
        self.filters: List[Union[Filter, Dict]] = filters or []
        self._check_config()

    def _check_config(self):
        if self.distinct and self.op not in (AggregationOp.ARRAY, AggregationOp.COUNT):
            raise ConfigurationError(f"Aggregation {self.op.value} does not support `distinct`")
        if self.distinct and self.metric:
            raise ConfigurationError(
                "`distinct` [Dimension] and `metric` [Metric] are mutually exclusive"
            )


class AggregationShorthand(Aggregation):
    """
    aggregation shorthands can be used to more easily express the aggregation
    """

    agg_op = None

    def __init__(
        self,
        metric: Union[str, Metric] = None,
        name: Optional[str] = None,
        distinct: Optional[Union[str, Dimension]] = None,
        filters: Optional[List[Union[Filter, Dict]]] = None,
    ):
        super().__init__(metric, self.agg_op, name, distinct=distinct, filters=filters)


class Sum(AggregationShorthand):
    agg_op = AggregationOp.SUM


class Count(AggregationShorthand):
    agg_op = AggregationOp.COUNT
    allow_metric_none = True


class ArrayAgg(AggregationShorthand):
    agg_op = AggregationOp.ARRAY
    allow_metric_none = True


class Min(AggregationShorthand):
    agg_op = AggregationOp.MIN


class Max(AggregationShorthand):
    agg_op = AggregationOp.MAX
