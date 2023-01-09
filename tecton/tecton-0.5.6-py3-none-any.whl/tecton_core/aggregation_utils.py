from tecton_proto.common import aggregation_function_pb2 as afpb

AGGREGATION_FUNCTIONS_TO_COLUMN_NAME = {
    afpb.AGGREGATION_FUNCTION_COUNT: "count",
    afpb.AGGREGATION_FUNCTION_SUM: "sum",
    afpb.AGGREGATION_FUNCTION_MEAN: "mean",
    afpb.AGGREGATION_FUNCTION_LAST: "last",
    afpb.AGGREGATION_FUNCTION_MIN: "min",
    afpb.AGGREGATION_FUNCTION_MAX: "max",
    afpb.AGGREGATION_FUNCTION_VAR_SAMP: "var_samp",
    afpb.AGGREGATION_FUNCTION_VAR_POP: "var_pop",
    afpb.AGGREGATION_FUNCTION_STDDEV_SAMP: "stddev_samp",
    afpb.AGGREGATION_FUNCTION_STDDEV_POP: "stddev_pop",
    # TODO(TEC-10550): we should rename the AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N to "lastn" and AGGREGATION_FUNCTION_LAST_DISTINCT_N to "last_distinct_n".
    afpb.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N: "last_non_distinct_n",
    afpb.AGGREGATION_FUNCTION_LAST_DISTINCT_N: "lastn",
}


def get_aggregation_function_name(aggregation_function_enum):
    return AGGREGATION_FUNCTIONS_TO_COLUMN_NAME[aggregation_function_enum]


def get_aggregation_column_prefix_from_column_name(aggregation_function_enum, column_name):
    """
    Get the aggregation column prefix from a given intermediate aggregation result column name.

    For example, Feature view with aggregation function AGGREGATE_FUNCTION_MEAN on input "transactions" produces
    intermediate aggregation result columns of "count_transactions", or "mean_transactions".
        - get_aggregation_column_prefix_from_column_name(AGGREGATE_FUNCTION_MEAN, "count_transactions") => "count"
        - get_aggregation_column_prefix_from_column_name(AGGREGATE_FUNCTION_MEAN, "mean_transactions") => "mean"
        - get_aggregation_column_prefix_from_column_name(AGGREGATE_FUNCTION_MEAN, "lastn_transactions") => raise error
    """
    column_prefixes = AGGREGATION_COLUMN_PREFIX_MAP.get(aggregation_function_enum, None)
    for column_prefix in column_prefixes:
        if column_name.startswith(f"{column_prefix}"):
            return column_prefix
    raise ValueError(
        f"Unsupported prefix for column name '{column_name}' for aggregation function '{get_aggregation_function_name(aggregation_function_enum)}'"
    )


def get_aggregation_column_prefixes(aggregation_function):
    col_names = AGGREGATION_COLUMN_PREFIX_MAP.get(aggregation_function, None)
    if col_names is None:
        raise ValueError(f"Unsupported aggregation function {aggregation_function}")
    return col_names


# Sample and Population Standard Deviation and Variance only depend on sum of squares, count, and sum. For example, to
# calculate population variance you can divide the sum of squares by the count and subtract the square of the mean.
var_stddev_prefixes = [
    get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_SUM) + "_of_squares",
    get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_COUNT),
    get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_SUM),
]

AGGREGATION_COLUMN_PREFIX_MAP = {
    afpb.AGGREGATION_FUNCTION_SUM: [get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_SUM)],
    afpb.AGGREGATION_FUNCTION_MIN: [get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_MIN)],
    afpb.AGGREGATION_FUNCTION_MAX: [get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_MAX)],
    afpb.AGGREGATION_FUNCTION_COUNT: [get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_COUNT)],
    afpb.AGGREGATION_FUNCTION_LAST: [get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_LAST)],
    afpb.AGGREGATION_FUNCTION_LAST_DISTINCT_N: [
        get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_LAST_DISTINCT_N)
    ],
    afpb.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N: [
        get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N)
    ],
    afpb.AGGREGATION_FUNCTION_MEAN: [
        get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_MEAN),
        get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_COUNT),
    ],
    afpb.AGGREGATION_FUNCTION_VAR_SAMP: var_stddev_prefixes,
    afpb.AGGREGATION_FUNCTION_STDDEV_SAMP: var_stddev_prefixes,
    afpb.AGGREGATION_FUNCTION_VAR_POP: var_stddev_prefixes,
    afpb.AGGREGATION_FUNCTION_STDDEV_POP: var_stddev_prefixes,
}
