from typing import List

import pendulum
from pyspark.sql import functions
from pyspark.sql import SparkSession
from pyspark.sql.window import Window

from tecton_core.query_consts import ANCHOR_TIME
from tecton_core.time_utils import convert_timedelta_for_version
from tecton_proto.data.feature_store_pb2 import FeatureStoreFormatVersion
from tecton_proto.data.feature_view_pb2 import TrailingTimeWindowAggregation
from tecton_spark.aggregation_plans import get_aggregation_plan
from tecton_spark.time_utils import convert_epoch_to_timestamp_column

"""
This file contains internal methods of feature_views/aggregations.py
Separate file helps de-clutter the main user-visible file.
"""

# TODO(TEC-9494) - deprecate this method, which is just used by the non-querytree read/run apis
def construct_full_tafv_df(
    spark: SparkSession,
    time_aggregation: TrailingTimeWindowAggregation,
    join_keys: List[str],
    feature_store_format_version: FeatureStoreFormatVersion,
    tile_interval: pendulum.Duration,
    all_partial_aggregations_df=None,
    use_materialized_data=True,
):
    """Construct a full time-aggregation data frame from a partial aggregation data frame.

    :param spark: Spark Session
    :param time_aggregation: trailing time window aggregation.
    :param join_keys: join keys to use on the dataframe.
    :param feature_store_format_version: indicates the time precision used by FeatureStore.
    :param tile_interval: Duration of the aggregation tile interval.
    :param fd: Required only if spine_df is provided. The BWAFV/SWAFV object.
    :param spine_df: (Optional) The spine to join against. If present, the returned data frame
        will contain rollups for all (join key, temporal key) combinations that are required
        to compute a full frame from the spine.
    :param all_partial_aggregations_df: (Optional) The full partial
        aggregations data frame to use in place of the a data frame read from the
        materialized parquet tables.
    :param use_materialized_data: (Optional) Use materialized data if materialization is enabled
    :param raw_data_time_limits: (Optional) Spine Time Bounds
    :param wildcard_key_not_in_spine: (Optional) Whether or not the wildcard join_key is present in the spine.
        Defaults to False if spine is not specified or if the FeatureView has no wildcard join_key.
    """
    output_df = _construct_full_tafv_df_with_anchor_time(
        spark,
        time_aggregation,
        join_keys,
        feature_store_format_version,
        tile_interval,
        all_partial_aggregations_df,
        use_materialized_data,
    )
    output_df = output_df.withColumn(
        ANCHOR_TIME,
        convert_epoch_to_timestamp_column(functions.col(ANCHOR_TIME), feature_store_format_version),
    )
    output_df = output_df.withColumnRenamed(ANCHOR_TIME, time_aggregation.time_key)

    return output_df


def _construct_full_tafv_df_with_anchor_time(
    spark: SparkSession,
    time_aggregation: TrailingTimeWindowAggregation,
    join_keys: List[str],
    feature_store_format_version: FeatureStoreFormatVersion,
    tile_interval: pendulum.Duration,
    all_partial_aggregations_df,
    use_materialized_data=True,
):
    # If spine isn't provided, the fake timestamp equals to anchor time + tile_interval, s.t. the output timestamp
    # completely contains the time range of the fully aggregated window. Note, that ideally we would either subtract
    # 1 second from the timestamp, due to tiles having [start, end) format, or convert tiles in (start, end] format.
    # For now, we're not doing 1 due to it being confusing in preview, and not doing 2 due to it requiring more work
    partial_aggregations_df = all_partial_aggregations_df.withColumn(
        ANCHOR_TIME,
        functions.col(ANCHOR_TIME) + convert_timedelta_for_version(tile_interval, feature_store_format_version),
    )

    aggregations = []
    for feature in time_aggregation.features:
        # We do + 1 since RangeBetween is inclusive, and we do not want to include the last row of the
        # previous tile. See https://github.com/tecton-ai/tecton/pull/1110
        window_duration = pendulum.Duration(seconds=feature.window.ToSeconds())
        upper_range = -(convert_timedelta_for_version(window_duration, feature_store_format_version)) + 1
        window_spec = (
            Window.partitionBy(join_keys).orderBy(functions.col(ANCHOR_TIME).asc()).rangeBetween(upper_range, 0)
        )
        aggregation_plan = get_aggregation_plan(
            feature.function, feature.function_params, time_aggregation.is_continuous, time_aggregation.time_key
        )
        names = aggregation_plan.materialized_column_names(feature.input_feature_name)

        agg = aggregation_plan.full_aggregation_transform(names, window_spec)

        filtered_agg = agg
        aggregations.append(filtered_agg.alias(feature.output_feature_name))

    output_df = partial_aggregations_df.select(join_keys + [ANCHOR_TIME] + aggregations)

    return output_df
