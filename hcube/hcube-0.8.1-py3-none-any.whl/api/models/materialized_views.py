from collections import OrderedDict

from hcube.api.exceptions import ConfigurationError
from hcube.api.models.aggregation import Sum
from hcube.api.models.cube import Cube


class AggregatingMaterializedViewMeta(type):
    """
    This is a special type of materialized view that is obtained by removing some of the dimensions
    from a cube and aggregating the metrics for rows that are left the same after the dimensions
    are removed.

    This leads to reduction of the size of the cube.

    To simplify matters, at present the only aggregation supported is SUM() and we do not support
    renaming the metric in the aggregation. This should simplify implementation of automatic
    materialized view detection/use.
    """

    default_metric_aggregation = Sum

    def __new__(cls, *args, **kwargs):
        new_cls = super().__new__(cls, *args, **kwargs)
        new_cls._process_attrs()
        return new_cls

    def _process_attrs(cls):
        # we do not process the top-level class in the hierarchy
        if cls.__name__ == "AggregatingMaterializedView":
            return
        if not hasattr(cls, "cube"):
            raise ConfigurationError("Materialized view instance must have a `cube` class attr")
        if not issubclass(cls.cube, Cube):
            raise ConfigurationError("Attribute `cube` must be a `Cube` subclass")
        # registers this materialized view with `cube`
        cls.cube._materialized_views.append(cls)
        # process dimension specification
        excludes_dims = getattr(cls, "excluded_dimensions", None)
        preserved_dims = getattr(cls, "preserved_dimensions", None)
        if excludes_dims and preserved_dims:
            raise ConfigurationError(
                "`excluded_dimensions` and `preserved_dimensions` attrs are mutually exclusive"
            )
        cls._dimensions = OrderedDict()
        if excludes_dims:
            for dim_name in excludes_dims:
                if dim_name not in cls.cube._dimensions:
                    raise ConfigurationError(
                        f"Excluded dimension `{dim_name} is not part of cube definition"
                    )
            for dim_name, dim in cls.cube._dimensions.items():
                if dim_name not in excludes_dims:
                    cls._dimensions[dim_name] = dim
        elif preserved_dims:
            for dim_name in preserved_dims:
                dim = cls.cube.dimension_by_name(dim_name)
                if not dim:
                    raise ConfigurationError(
                        f"Preserved dimension `{dim_name} is not part of cube definition"
                    )
                cls._dimensions[dim_name] = dim
        else:
            raise ConfigurationError(
                "`excluded_dimensions` or `preserved_dimensions` attr is required"
            )
        # process metric aggregation specification
        aggregated_metrics = getattr(cls, "aggregated_metrics")
        cls._aggregations = []
        if aggregated_metrics:
            for m_name in aggregated_metrics:
                metric = cls.cube.metric_by_name(m_name)
                if not metric:
                    raise ConfigurationError(
                        f"Aggregated metric `{m_name} is not part of cube definition"
                    )
                cls._aggregations.append(Sum(metric))
        else:
            raise ConfigurationError("`aggregated_metrics` attr is required")


class AggregatingMaterializedView(metaclass=AggregatingMaterializedViewMeta):

    excluded_dimensions: list = []
    preserved_dimensions: list = []
    aggregated_metrics: list = []
    projection: bool = False  # should this be a projection rather than a materialized view
    preserve_sign: bool = True  # should we preserve the sign column in the materialized view
