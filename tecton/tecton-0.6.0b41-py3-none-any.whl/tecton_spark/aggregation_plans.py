from typing import Callable
from typing import List

import attr
from pyspark import SparkContext
from pyspark.sql import Column
from pyspark.sql import functions
from pyspark.sql import WindowSpec
from pyspark.sql.functions import expr

from tecton_core.aggregation_utils import get_aggregation_function_name
from tecton_proto.common import aggregation_function_pb2 as afpb


# WARNING: If you're changing this class there's a good chance you need to change
# AggregationPlans.kt. Please look over that file carefully.


@attr.s(auto_attribs=True)
class AggregationPlan(object):
    """
    An AggregationPlan contains all the methods required to compute feature values for a specific Tecton aggregation.

    Partial aggregates are returned as a list of pyspark columns. Full aggregates use the partial aggregate columns as inputs and are returned as a single pyspark column.

    The order of the columns must be the same in:
    * the return list in partial_aggregation_transform
    * the arguments list in full_aggregation_transform
    * materialized_column_prefixes

    Attributes:
        partial_aggregation_transform: A method that maps an input column name to a list of output pyspark columns containing the partial aggregates.
        full_aggregation_transform: A method that maps a list of input partial aggregate columns and a WindowSpec to an output pyspark column containing the full aggregates.
        materialized_column_prefixes: The list of prefixes that should be applied to the pyspark columns produced by `partial_aggregation_transform`.
    """

    partial_aggregation_transform: Callable[[str], List[Column]]
    full_aggregation_transform: Callable[[List[str], WindowSpec], Column]
    materialized_column_prefixes: List[str]

    def materialized_column_names(self, input_column_name: str) -> List[str]:
        return [f"{prefix}_{input_column_name}" for prefix in self.materialized_column_prefixes]


def get_aggregation_plan(
    aggregation_function: afpb.AggregationFunction,
    function_params: afpb.AggregationFunctionParams,
    is_continuous: bool,
    time_key: str,
) -> AggregationPlan:
    plan = AGGREGATION_PLANS.get(aggregation_function, None)
    if plan is None:
        raise ValueError(f"Unsupported aggregation function {aggregation_function}")

    if callable(plan):
        return plan(time_key, function_params, is_continuous)
    else:
        return plan


def _simple_partial_aggregation_transform(spark_transform):
    return lambda col: [spark_transform(col)]


def _simple_full_aggregation_transform(spark_transform):
    return lambda cols, window: spark_transform(cols[0]).over(window)


def _simple_aggregation_plan(aggregation_function: afpb.AggregationFunction, spark_transform):
    return AggregationPlan(
        partial_aggregation_transform=_simple_partial_aggregation_transform(spark_transform),
        full_aggregation_transform=_simple_full_aggregation_transform(spark_transform),
        materialized_column_prefixes=[get_aggregation_function_name(aggregation_function)],
    )


# Partial aggregator used by both first non-distinct and distinct N.
def FirstNAgg(timestamp: str, col: str, n: int, distinct: bool) -> Column:
    sc = SparkContext._active_spark_context
    udf_name = (
        f"tecton_first_distinct_{n}_partial_aggregation"
        if distinct
        else f"tecton_first_non_distinct_{n}_partial_aggregation"
    )
    sc._jvm.com.tecton.udfs.spark3.FirstNRegister().register(n, udf_name, distinct)
    return expr(f"{udf_name}({timestamp},{col}).values")


def _make_first_n_partial_aggregation(time_key: str, n: int, distinct: bool) -> Callable:
    def _first_n_partial_aggregation(col: str) -> List[Column]:
        return [FirstNAgg(time_key, col, n, distinct)]

    return _first_n_partial_aggregation


# Partial aggregator used by both last non-distinct and distinct N.
def LastNAgg(col1: str, col2: str, n: int, distinct: bool) -> Column:
    sc = SparkContext._active_spark_context
    udf_name = (
        f"tecton_last_distinct_{n}_partial_aggregation"
        if distinct
        else f"tecton_last_non_distinct_{n}_partial_aggregation"
    )
    sc._jvm.com.tecton.udfs.spark3.LastNRegister().register(n, udf_name, distinct)
    return expr(f"{udf_name}({col1}, {col2}).values")


def _make_last_n_partial_aggregation(time_key: str, n: int, distinct: bool) -> Callable:
    def _last_n_partial_aggregation(col: str) -> List[Column]:
        return [LastNAgg(time_key, col, n, distinct)]

    return _last_n_partial_aggregation


# Full aggregator used by both last and first distinct N.
def LimitedListConcatAgg(col1: str, n: int, keep_last_items: bool) -> Column:
    sc = SparkContext._active_spark_context
    udf_name = (
        f"tecton_last_distinct_{n}_full_aggregation"
        if keep_last_items
        else f"tecton_first_distinct_{n}_full_aggregation"
    )
    sc._jvm.com.tecton.udfs.spark3.LimitedListConcatRegister().register(n, udf_name, keep_last_items)
    return expr(f"{udf_name}({col1})")


def _make_fixed_size_n_full_aggregation(n: int, keep_last_items: bool):
    def _fixed_size_n_full_aggregation(column_name: List[str], window: WindowSpec) -> Column:
        col = (LimitedListConcatAgg(column_name[0], n, keep_last_items).over(window)).values
        return col

    return _fixed_size_n_full_aggregation


# Full aggregator used by last non-distinct N.
def _make_last_non_distinct_n_full_aggregation(n: int) -> Callable:
    def _last_non_distinct_n_full_aggregation(cols: List[str], window: WindowSpec) -> Column:
        return functions.reverse(
            functions.slice(functions.reverse(functions.flatten(functions.collect_list(cols[0]).over(window))), 1, n)
        )

    return _last_non_distinct_n_full_aggregation


# Full aggregator used by first non-distinct N.
def _make_first_non_distinct_n_full_aggregation(n: int) -> Callable:
    def _first_non_distinct_n_full_aggregation(cols: List[Column], window: WindowSpec) -> Column:
        return functions.slice(functions.flatten(functions.collect_list(cols[0]).over(window)), 1, n)

    return _first_non_distinct_n_full_aggregation


def _sum_with_default(columns: List[str], window: WindowSpec):
    col = functions.sum(columns[0]).over(window)
    # Fill null
    col = functions.when(col.isNull(), functions.lit(0)).otherwise(col)
    return col


# population variation equation: Σ(x^2)/n - μ^2
def _var_pop_full_aggregation(cols: List[str], window: WindowSpec):
    sum_of_squares_col, count_col, sum_col = cols
    return functions.sum(sum_of_squares_col).over(window) / functions.sum(count_col).over(window) - functions.pow(
        functions.sum(sum_col).over(window) / functions.sum(count_col).over(window), 2
    )


def _stddev_pop_full_aggregation(cols: List[str], window: WindowSpec):
    return functions.sqrt(_var_pop_full_aggregation(cols, window))


# sample variation equation: (Σ(x^2) - (Σ(x)^2)/N)/N-1
def _var_samp_full_aggregation(cols: List[str], window: WindowSpec):
    sum_of_squares_col, count_col, sum_col = cols
    total_count_col = functions.sum(count_col).over(window)
    # check if count is equal to 0 for divide by 0 errors
    var_samp_col = functions.when(
        total_count_col != 1,
        (
            functions.sum(sum_of_squares_col).over(window)
            - functions.pow(functions.sum(sum_col).over(window), 2) / total_count_col
        )
        / (total_count_col - functions.lit(1)),
    )
    return var_samp_col


def _stddev_samp_full_aggregation(cols: List[str], window: WindowSpec):
    return functions.sqrt(_var_samp_full_aggregation(cols, window))


def _stddev_var_partial(col: List[str]):
    return [
        functions.sum(functions.pow(col, 2)),
        functions.count(col),
        functions.sum(functions.col(col)),
    ]


stddev_var_materialized_column_prefixes = [
    get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_SUM) + "_of_squares",
    get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_COUNT),
    get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_SUM),
]

AGGREGATION_PLANS = {
    afpb.AGGREGATION_FUNCTION_SUM: _simple_aggregation_plan(afpb.AGGREGATION_FUNCTION_SUM, functions.sum),
    afpb.AGGREGATION_FUNCTION_MIN: _simple_aggregation_plan(afpb.AGGREGATION_FUNCTION_MIN, functions.min),
    afpb.AGGREGATION_FUNCTION_MAX: _simple_aggregation_plan(afpb.AGGREGATION_FUNCTION_MAX, functions.max),
    afpb.AGGREGATION_FUNCTION_LAST: _simple_aggregation_plan(
        afpb.AGGREGATION_FUNCTION_LAST, lambda col: functions.last(col, ignorenulls=True)
    ),
    # Needs to use COUNT for partial and SUM for full aggregation
    afpb.AGGREGATION_FUNCTION_COUNT: AggregationPlan(
        partial_aggregation_transform=_simple_partial_aggregation_transform(functions.count),
        full_aggregation_transform=_sum_with_default,
        materialized_column_prefixes=[get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_COUNT)],
    ),
    afpb.AGGREGATION_FUNCTION_LAST_DISTINCT_N: lambda time_key, params, is_continuous: AggregationPlan(
        partial_aggregation_transform=_make_last_n_partial_aggregation(time_key, params.last_n.n, True),
        full_aggregation_transform=_make_fixed_size_n_full_aggregation(params.last_n.n, True),
        materialized_column_prefixes=[
            get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_LAST_DISTINCT_N)
            + (str(params.last_n.n) if not is_continuous else "")
        ],
    ),
    afpb.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N: lambda time_key, params, is_continuous: AggregationPlan(
        partial_aggregation_transform=_make_last_n_partial_aggregation(time_key, params.last_n.n, False),
        full_aggregation_transform=_make_last_non_distinct_n_full_aggregation(params.last_n.n),
        materialized_column_prefixes=[
            get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N)
            + (str(params.last_n.n) if not is_continuous else "")
        ],
    ),
    afpb.AGGREGATION_FUNCTION_VAR_POP: AggregationPlan(
        partial_aggregation_transform=lambda col: _stddev_var_partial(col),
        full_aggregation_transform=_var_pop_full_aggregation,
        materialized_column_prefixes=stddev_var_materialized_column_prefixes,
    ),
    afpb.AGGREGATION_FUNCTION_STDDEV_POP: AggregationPlan(
        partial_aggregation_transform=lambda col: _stddev_var_partial(col),
        full_aggregation_transform=_stddev_pop_full_aggregation,
        materialized_column_prefixes=stddev_var_materialized_column_prefixes,
    ),
    afpb.AGGREGATION_FUNCTION_VAR_SAMP: AggregationPlan(
        partial_aggregation_transform=lambda col: _stddev_var_partial(col),
        full_aggregation_transform=_var_samp_full_aggregation,
        materialized_column_prefixes=stddev_var_materialized_column_prefixes,
    ),
    afpb.AGGREGATION_FUNCTION_STDDEV_SAMP: AggregationPlan(
        partial_aggregation_transform=lambda col: _stddev_var_partial(col),
        full_aggregation_transform=_stddev_samp_full_aggregation,
        materialized_column_prefixes=stddev_var_materialized_column_prefixes,
    ),
    afpb.AGGREGATION_FUNCTION_FIRST_NON_DISTINCT_N: lambda time_key, params, is_continuous: AggregationPlan(
        partial_aggregation_transform=_make_first_n_partial_aggregation(time_key, params.first_n.n, False),
        full_aggregation_transform=_make_first_non_distinct_n_full_aggregation(params.first_n.n),
        materialized_column_prefixes=[
            get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_FIRST_NON_DISTINCT_N)
            + (str(params.first_n.n) if not is_continuous else "")
        ],
    ),
    afpb.AGGREGATION_FUNCTION_FIRST_DISTINCT_N: lambda time_key, params, is_continuous: AggregationPlan(
        partial_aggregation_transform=_make_first_n_partial_aggregation(time_key, params.first_n.n, True),
        full_aggregation_transform=_make_fixed_size_n_full_aggregation(params.first_n.n, False),
        materialized_column_prefixes=[
            get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_FIRST_DISTINCT_N)
            + (str(params.first_n.n) if not is_continuous else "")
        ],
    ),
}


def _mean_full_aggregation(cols: List[str], window: WindowSpec):
    # Window aggregation doesn't work with more than one built-in function like this
    #   sum(mean_clicked * count_clicked) / sum(count_clicked)
    # And it does not support UDFs on bounded windows (the kind we use)
    #   https://issues.apache.org/jira/browse/SPARK-22239
    # We work around this limitations by calculating ratio over two window aggregations
    mean_col, count_col = cols
    return functions.sum(functions.col(mean_col) * functions.col(count_col)).over(window) / functions.sum(
        count_col
    ).over(window)


# It is important that `partial_aggregation_transform` or `materialized_column_prefixes`
# contain aggregation data in the same ordering.
AGGREGATION_PLANS[afpb.AGGREGATION_FUNCTION_MEAN] = AggregationPlan(
    partial_aggregation_transform=lambda col: [functions.mean(col), functions.count(col)],
    full_aggregation_transform=_mean_full_aggregation,
    materialized_column_prefixes=[
        get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_MEAN),
        get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_COUNT),
    ],
)
