from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional

import pyspark
import pyspark.sql.functions as F

from tecton_core.aggregation_utils import get_aggregation_column_prefix_from_column_name
from tecton_core.aggregation_utils import get_aggregation_column_prefixes
from tecton_core.aggregation_utils import get_aggregation_function_name
from tecton_core.feature_view_utils import resolve_function_name
from tecton_core.query_consts import ANCHOR_TIME
from tecton_proto.common import aggregation_function_pb2 as afpb
from tecton_proto.data.feature_view_pb2 import TrailingTimeWindowAggregation
from tecton_spark.aggregation_plans import AggregationPlan
from tecton_spark.aggregation_plans import get_aggregation_plan
from tecton_spark.time_utils import convert_timestamp_to_epoch
from tecton_spark.time_utils import get_timestamp_in_seconds

WINDOW_COLUMN_NAME = "window"


def _get_feature_partial_aggregations(aggregation_plan: AggregationPlan, feature_name: str):
    column_names = set()
    for column_name, aggregated_column in zip(
        aggregation_plan.materialized_column_names(feature_name),
        aggregation_plan.partial_aggregation_transform(feature_name),
    ):
        if column_name in column_names:
            continue
        column_names.add(column_name)

        yield column_name, aggregated_column.alias(column_name)


def _get_continuous_aggregation_value(column_prefix, feature_input_name):
    if column_prefix == get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_COUNT):
        return F.lit(1).cast("long")
    elif column_prefix in set(
        [
            get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_LAST_DISTINCT_N),
            get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N),
            get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_FIRST_NON_DISTINCT_N),
            get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_FIRST_DISTINCT_N),
        ]
    ):
        return F.array(F.col(feature_input_name))
    elif column_prefix == get_aggregation_function_name(afpb.AGGREGATION_FUNCTION_MEAN):
        return F.col(feature_input_name).cast("double")
    else:
        return F.col(feature_input_name)


def _convert_window_to_anchor_time(
    output_df: pyspark.sql.DataFrame,
    is_continuous: bool,
    time_key: str,
    version: int,
    window_start_column_name: Optional[str],
    window_end_column_name: Optional[str],
    convert_window_times_to_epoch: bool,
) -> pyspark.sql.DataFrame:
    def _add_time_column(
        df: pyspark.sql.DataFrame, input_ts_column_name: str, output_column_name: str
    ) -> pyspark.sql.DataFrame:
        col = F.col(input_ts_column_name)
        return df.withColumn(
            output_column_name, convert_timestamp_to_epoch(col, version) if convert_window_times_to_epoch else col
        )

    # For continuous aggregations this will simply be the time key.
    if is_continuous:
        return _add_time_column(output_df, time_key, ANCHOR_TIME)

    # Grouping by Spark Window introduces the "window" struct with "start" and "end" columns.
    # We only need to keep the "start" column as an anchor time.
    anchor_column_name = window_start_column_name if window_start_column_name else ANCHOR_TIME
    output_df = _add_time_column(output_df, f"{WINDOW_COLUMN_NAME}.start", anchor_column_name)

    if window_end_column_name:
        output_df = _add_time_column(output_df, f"{WINDOW_COLUMN_NAME}.end", window_end_column_name)

    return output_df.drop(WINDOW_COLUMN_NAME)


def construct_partial_time_aggregation_df(
    df: pyspark.sql.DataFrame,
    join_keys: List[str],
    time_aggregation: TrailingTimeWindowAggregation,
    version: int,
    window_start_column_name: Optional[str] = None,
    window_end_column_name: Optional[str] = None,
    convert_to_epoch: bool = True,
    aggregation_anchor_time: Optional[datetime] = None,
):
    """Constructs a dataframe that performs partial aggregations on the input dataframe.

    Also removes the default window column that is generated, and replaces it with a start time column, and optionally
    an end time column.

    If the time aggregation is continuous, no aggregations will be performed. Instead, a start time column will be added
    but will simply be the same as the timestamp column in the input dataframe.

    Args:
        df: The input dataframe.
        join_keys: The columns to be grouped by for the partial aggregations.
        time_aggregation: The set of partial aggregations to be performed.
        version: The feature store version.
        window_start_column_name: If specified, the name of the start time column; otherwise it will use the default value "_anchor_time".
        window_end_column_name: If specified, the end time column will be included with this name.
        convert_to_epoch: If True, the window start and end times will be converted to epoch.
        aggregation_anchor_time: If specified, the offset for the aggregation windows.

    Returns:
        A dataframe with the partial aggregations. For example, if `user_id` is the only join key, there are two
        aggregations (min and max), `window_start_column_name` is `tile_start_time`, `window_end_column_name` is
        `tile_end_time`, and `convert_to_epoch` is `False`, then the resulting dataframe might look something like:

        +-------+------------+------------+-------------------+-------------------+
        |user_id|value_min_1d|value_max_1d|    tile_start_time|      tile_end_time|
        +-------+------------+------------+-------------------+-------------------+
        |      1|           7|           9|2022-05-15 00:00:00|2022-05-16 00:00:00|
        |      2|          10|          12|2022-05-16 00:00:00|2022-05-17 00:00:00|
        |      1|          13|          13|2022-05-16 00:00:00|2022-05-17 00:00:00|
        +-------+------------+------------+-------------------+-------------------+
    """
    output_columns = set()
    if not time_aggregation.is_continuous:
        group_by_cols = [F.col(join_key) for join_key in join_keys]
        slide_str = f"{time_aggregation.aggregation_slide_period.seconds} seconds"

        anchor_time_offset_string = None
        if aggregation_anchor_time:
            # Compute the offset from the epoch such that anchor_time aligns to an interval boundary of size
            # aggregation_slide_period. i.e. `epoch + offset + (X * slide_period) = anchor_time`, where X is
            # an integer.
            anchor_time_epoch = get_timestamp_in_seconds(aggregation_anchor_time)
            slide_period_seconds = time_aggregation.aggregation_slide_period.seconds
            anchor_time_offset_seconds = anchor_time_epoch % slide_period_seconds
            anchor_time_offset_string = f"{anchor_time_offset_seconds} seconds"

        window_spec = F.window(time_aggregation.time_key, slide_str, slide_str, anchor_time_offset_string)
        group_by_cols = [window_spec] + group_by_cols
        aggregations = []
        for feature in time_aggregation.features:
            aggregation_plan = get_aggregation_plan(
                feature.function, feature.function_params, time_aggregation.is_continuous, time_aggregation.time_key
            )
            for name, aggregation in _get_feature_partial_aggregations(aggregation_plan, feature.input_feature_name):
                if name in output_columns:
                    continue
                output_columns.add(name)
                aggregations.append(aggregation)
        output_df = df.groupBy(*group_by_cols).agg(*aggregations)
    else:
        columns_to_drop = set()
        for feature in time_aggregation.features:
            column_prefixes = get_aggregation_column_prefixes(feature.function)
            for column_prefix in column_prefixes:
                full_name = f"{column_prefix}_{feature.input_feature_name}"
                if full_name in output_columns:
                    continue
                output_columns.add(full_name)
                df = df.withColumn(
                    full_name, _get_continuous_aggregation_value(column_prefix, feature.input_feature_name)
                )
            columns_to_drop.add(feature.input_feature_name)
        # Drop the original feature columns.
        for column in columns_to_drop:
            df = df.drop(column)
        output_df = df

    output_df = _convert_window_to_anchor_time(
        output_df,
        time_aggregation.is_continuous,
        time_aggregation.time_key,
        version,
        window_start_column_name,
        window_end_column_name,
        convert_to_epoch,
    )
    # TOOD: TEC-12299 drop the `timestamp` column in m13n schema for continuous WAFV
    return output_df


def partial_aggregate_column_renames(
    slide_interval_string: str, trailing_time_window_aggregation: TrailingTimeWindowAggregation
) -> Dict[str, str]:
    """Rename partial aggregate columns to human readable format."""
    # Create a map from intermediate rollup column name to preferred column names.
    renaming_map = dict()
    for feature in trailing_time_window_aggregation.features:
        aggregation_plan = get_aggregation_plan(
            feature.function,
            feature.function_params,
            trailing_time_window_aggregation.is_continuous,
            trailing_time_window_aggregation.time_key,
        )
        for old_name in aggregation_plan.materialized_column_names(feature.input_feature_name):
            aggregation_function_name = resolve_function_name(
                get_aggregation_column_prefix_from_column_name(feature.function, old_name), feature.function_params
            )
            renaming_map[old_name] = f"{feature.input_feature_name}_{aggregation_function_name}_{slide_interval_string}"
    return renaming_map


def rename_partial_aggregate_columns(
    df: pyspark.sql.DataFrame,
    slide_interval_string: str,
    trailing_time_window_aggregation: TrailingTimeWindowAggregation,
) -> pyspark.sql.DataFrame:
    """Rename partial aggregate columns to human readable format."""
    # Create a map from intermediate rollup column name to preferred column names.
    renaming_map = partial_aggregate_column_renames(slide_interval_string, trailing_time_window_aggregation)
    for (old_name, new_name) in renaming_map.items():
        df = df.withColumnRenamed(old_name, new_name)
    return df
