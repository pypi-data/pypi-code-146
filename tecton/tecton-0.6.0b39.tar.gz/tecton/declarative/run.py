import warnings
from datetime import datetime
from datetime import timedelta
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple

import pendulum
from google.protobuf.duration_pb2 import Duration
from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
from pyspark.sql.types import TimestampType
from typeguard import typechecked

from tecton._internals import errors
from tecton._internals.feature_views.aggregations import construct_full_tafv_df
from tecton.run_api_consts import AGGREGATION_LEVEL_DISABLED
from tecton.run_api_consts import AGGREGATION_LEVEL_FULL
from tecton.run_api_consts import AGGREGATION_LEVEL_PARTIAL
from tecton.run_api_consts import DEFAULT_AGGREGATION_TILES_WINDOW_END_COLUMN_NAME
from tecton.run_api_consts import DEFAULT_AGGREGATION_TILES_WINDOW_START_COLUMN_NAME
from tecton.run_api_consts import SUPPORTED_AGGREGATION_LEVEL_VALUES
from tecton_core import specs
from tecton_core import time_utils
from tecton_core.feature_view_utils import construct_aggregation_output_feature_name
from tecton_core.id_helper import IdHelper
from tecton_core.query_consts import ANCHOR_TIME
from tecton_proto.args.feature_view_pb2 import FeatureAggregation as FeatureAggregationProto
from tecton_proto.args.feature_view_pb2 import FeatureViewArgs
from tecton_proto.args.feature_view_pb2 import StreamProcessingMode as StreamProcessingModeProto
from tecton_proto.args.pipeline_pb2 import PipelineNode
from tecton_proto.common import spark_schema_pb2
from tecton_proto.common.aggregation_function_pb2 import AggregationFunction
from tecton_proto.data.feature_store_pb2 import FeatureStoreFormatVersion
from tecton_proto.data.feature_view_pb2 import AggregateFeature
from tecton_proto.data.feature_view_pb2 import TrailingTimeWindowAggregation
from tecton_spark.partial_aggregations import construct_partial_time_aggregation_df
from tecton_spark.partial_aggregations import rename_partial_aggregate_columns
from tecton_spark.pipeline_helper import get_all_input_keys
from tecton_spark.pipeline_helper import pipeline_to_dataframe

_AGGREGATION_FUNC_STR_TO_ENUM = {
    "variance": AggregationFunction.AGGREGATION_FUNCTION_VAR_SAMP,
    "stddev": AggregationFunction.AGGREGATION_FUNCTION_STDDEV_SAMP,
    "stddev_samp": AggregationFunction.AGGREGATION_FUNCTION_STDDEV_SAMP,
    "last": AggregationFunction.AGGREGATION_FUNCTION_LAST,
    "count": AggregationFunction.AGGREGATION_FUNCTION_COUNT,
    "mean": AggregationFunction.AGGREGATION_FUNCTION_MEAN,
    "min": AggregationFunction.AGGREGATION_FUNCTION_MIN,
    "max": AggregationFunction.AGGREGATION_FUNCTION_MAX,
    "var_pop": AggregationFunction.AGGREGATION_FUNCTION_VAR_POP,
    "stddev_pop": AggregationFunction.AGGREGATION_FUNCTION_STDDEV_POP,
    "sum": AggregationFunction.AGGREGATION_FUNCTION_SUM,
    "lastn": AggregationFunction.AGGREGATION_FUNCTION_LAST_DISTINCT_N,
    "last_non_distinct_n": AggregationFunction.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N,
    "first_non_distinct_n": AggregationFunction.AGGREGATION_FUNCTION_FIRST_NON_DISTINCT_N,
    "first_distinct_n": AggregationFunction.AGGREGATION_FUNCTION_FIRST_NON_DISTINCT_N,
}


@typechecked
def declarative_run(
    args: FeatureViewArgs,
    spark: SparkSession,
    start_time: Optional[datetime],
    end_time: Optional[datetime],
    aggregation_level: Optional[str],
    mock_sources: Dict[str, DataFrame],
) -> DataFrame:
    """
    Internal implementation of run() for materialized (i.e. not on-demand) feature view declarative objects.
    """
    assert args.HasField(
        "materialized_feature_view_args"
    ), "declarative_run can only be used with materialized feature views"
    if aggregation_level and not args.materialized_feature_view_args.aggregations:
        raise errors.FV_UNSUPPORTED_ARG("aggregation_level")

    # Set default aggregation_level.
    if not aggregation_level:
        aggregation_level = (
            AGGREGATION_LEVEL_FULL if args.materialized_feature_view_args.aggregations else AGGREGATION_LEVEL_DISABLED
        )

    if aggregation_level not in SUPPORTED_AGGREGATION_LEVEL_VALUES:
        raise errors.FV_INVALID_ARG_VALUE(
            "aggregation_level", str(aggregation_level), str(SUPPORTED_AGGREGATION_LEVEL_VALUES)
        )

    _validate_batch_mock_sources_keys(args, mock_sources)

    batch_schedule = _get_batch_schedule(args)
    start_time, end_time = _resolve_times(batch_schedule, start_time, end_time)
    _warn_incorrect_time_range_size(args, start_time, end_time, aggregation_level)

    df = pipeline_to_dataframe(
        spark,
        pipeline=args.pipeline,
        consume_streaming_data_sources=False,
        data_sources=_get_data_sources(args),
        transformations=get_transformations(args),
        feature_time_limits=pendulum.period(start_time, end_time),
        schedule_interval=batch_schedule,
        passed_in_inputs=mock_sources,
    )
    timestamp_field = _get_timestamp_field(args, df.schema)
    df = df.filter((df[timestamp_field] >= start_time) & (df[timestamp_field] < end_time))
    if aggregation_level == AGGREGATION_LEVEL_DISABLED:
        return df

    trailing_time_window_aggregation = _construct_trailing_time_window_aggregation(args, df.schema)
    join_keys = [join_key for entity in args.entities for join_key in entity.join_keys]

    if aggregation_level == AGGREGATION_LEVEL_PARTIAL:
        # Perform partial rollup with human readable output format.
        df = construct_partial_time_aggregation_df(
            df=df,
            join_keys=join_keys,
            time_aggregation=trailing_time_window_aggregation,
            version=FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_TTL_FIELD,
            window_start_column_name=DEFAULT_AGGREGATION_TILES_WINDOW_START_COLUMN_NAME,
            window_end_column_name=DEFAULT_AGGREGATION_TILES_WINDOW_END_COLUMN_NAME,
            convert_to_epoch=False,
            aggregation_anchor_time=end_time,
        )
        if (
            args.materialized_feature_view_args.stream_processing_mode
            == StreamProcessingModeProto.STREAM_PROCESSING_MODE_CONTINUOUS
        ):
            # Drop the anchor time, it's redundant with the `timestamp` column and doesn't need to be user facing.
            df = df.drop(ANCHOR_TIME)
            aggregation_interval_string = "continuous"
        else:
            aggregation_interval_string = time_utils.to_human_readable_str(
                args.materialized_feature_view_args.aggregation_interval
            )
        return rename_partial_aggregate_columns(
            df=df,
            slide_interval_string=aggregation_interval_string,
            trailing_time_window_aggregation=trailing_time_window_aggregation,
        )

    # Perform partial rollup for each aggregate tile.
    df = construct_partial_time_aggregation_df(
        df=df,
        join_keys=join_keys,
        time_aggregation=trailing_time_window_aggregation,
        version=FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_TTL_FIELD,
        aggregation_anchor_time=end_time,
    )

    # Perform final rollup from aggregate tiles up to each result window.
    return construct_full_tafv_df(
        spark=spark,
        time_aggregation=trailing_time_window_aggregation,
        join_keys=join_keys,
        feature_store_format_version=FeatureStoreFormatVersion.FEATURE_STORE_FORMAT_VERSION_TTL_FIELD,
        tile_interval=time_utils.proto_to_duration(args.materialized_feature_view_args.aggregation_interval),
        all_partial_aggregations_df=df,
        use_materialized_data=False,
    )


@typechecked
def _warn_incorrect_time_range_size(
    args: FeatureViewArgs, start_time: datetime, end_time: datetime, aggregation_level: Optional[str]
):
    time_range = end_time - start_time
    batch_schedule = _get_batch_schedule(args)
    if args.materialized_feature_view_args.aggregations:
        if (
            args.materialized_feature_view_args.stream_processing_mode
            == StreamProcessingModeProto.STREAM_PROCESSING_MODE_CONTINUOUS
        ):
            # There should not be any time range warnings for continuous aggregates.
            return
        aggregation_interval = args.materialized_feature_view_args.aggregation_interval.ToTimedelta()
        if aggregation_level == AGGREGATION_LEVEL_FULL:
            max_aggregation = max(
                (agg.time_window.ToTimedelta() for agg in args.materialized_feature_view_args.aggregations)
            )
            if time_range < max_aggregation:
                # Uses warnings.warn() instead of tecton_core.logger.warning() because it works better with pytest.
                warnings.warn(
                    f"Run time range ({start_time}, {end_time}) is smaller than the maximum aggregation size: {max_aggregation}. This may lead to incorrect aggregate feature values."
                )
            if time_range.total_seconds() % aggregation_interval.total_seconds() != 0:
                warnings.warn(
                    f"Run time range ({start_time}, {end_time}) is not a multiple of the aggregation_interval: {aggregation_interval}. This may lead to incorrect aggregate feature values, since Tecton pre-aggregates data in smaller time windows based on the aggregation_interval size."
                )
        elif aggregation_level == AGGREGATION_LEVEL_PARTIAL:
            if time_range.total_seconds() % aggregation_interval.total_seconds() != 0:
                warnings.warn(
                    f"Run time range ({start_time}, {end_time}) is not a multiple of the aggregation_interval: {aggregation_interval}. This may lead to incorrect aggregate feature values, since Tecton pre-aggregates data in smaller time windows based on the aggregation_interval size."
                )
    elif args.materialized_feature_view_args.incremental_backfills and time_range != batch_schedule:
        warnings.warn(
            f"Run time range ({start_time}, {end_time}) is not equivalent to the batch_schedule: {batch_schedule}. This may lead to incorrect feature values since feature views with incremental_backfills typically implicitly rely on the materialization range being equivalent to the batch_schedule."
        )


@typechecked
def _get_data_sources(args: FeatureViewArgs) -> List[specs.DataSourceSpec]:
    """
    Returns a list of all of the data source specs that this feature view depends on.
    """
    from tecton._internals.fco import _ALL_FCOS

    ds_ids = _get_ids_from_pipeline(args.pipeline.root, "data_source_node")

    # Data source post processors and data source functions should not be executed during declarative run, however
    # the data source spec expects these callables to be set for certain data source types. E.g. a stream data source
    # must always have a stream post processor. Provide a "fail fast" function to satisfy the requirement but to make
    # sure the fake function is never accidentally used.
    def data_source_fake_function(*args, **kwargs):
        raise RuntimeError("Declarative run should not invoke data source functions or post-processors.")

    args_supplement = specs.DataSourceSpecArgsSupplement(
        batch_schema=spark_schema_pb2.SparkSchema(),
        stream_schema=spark_schema_pb2.SparkSchema(),
        batch_data_source_function=data_source_fake_function,
        stream_post_processor=data_source_fake_function,
        stream_data_source_function=data_source_fake_function,
    )

    data_source_specs = []
    for ds_id in ds_ids:
        ds = _ALL_FCOS[ds_id]
        data_source_specs.append(specs.DataSourceSpec.from_args_proto(ds._args, args_supplement))

    return data_source_specs


@typechecked
def get_transformations(args: FeatureViewArgs) -> List[specs.TransformationSpec]:
    """
    Returns a list of all of the transformation specs built from args protos that this feature view depends on.
    """
    from tecton._internals.fco import _ALL_FCOS

    transformation_ids = _get_ids_from_pipeline(args.pipeline.root, "transformation_node")

    transformation_specs = []
    for transformation_id in transformation_ids:
        transformation = _ALL_FCOS[transformation_id]
        transformation_specs.append(
            specs.TransformationSpec.from_args_proto(transformation._args_proto(), transformation.user_function)
        )

    return transformation_specs


@typechecked
def _get_ids_from_pipeline(node: PipelineNode, desired_node_type: str) -> Set[str]:
    """
    Returns the FCO ids of all ancestor pipeline nodes of the desired node type.
    """
    assert desired_node_type in ("data_source_node", "transformation_node"), "Unsupported desired_node_type"
    ids = set()
    if node.HasField("data_source_node") and desired_node_type == "data_source_node":
        ids.add(IdHelper.to_string(node.data_source_node.virtual_data_source_id))
    elif node.HasField("transformation_node"):
        if desired_node_type == "transformation_node":
            ids.add(IdHelper.to_string(node.transformation_node.transformation_id))
        for child in node.transformation_node.inputs:
            ids.update(_get_ids_from_pipeline(child.node, desired_node_type))
    return ids


@typechecked
def _resolve_times(
    batch_schedule: timedelta,
    start_time: Optional[datetime],
    end_time: Optional[datetime],
) -> Tuple[datetime, datetime]:
    assert start_time or end_time, "At least one of start_time or end_time should be set."
    # If start_time or end_time time is missing, default to one batch_schedule.
    if start_time is None:
        start_time = end_time - batch_schedule
    elif end_time is None:
        end_time = start_time + batch_schedule

    if end_time <= start_time:
        raise errors.END_TIME_BEFORE_START_TIME(start_time, end_time)

    return start_time, end_time


@typechecked
def _construct_trailing_time_window_aggregation(
    args: FeatureViewArgs, df_schema: StructType
) -> TrailingTimeWindowAggregation:
    aggregation = TrailingTimeWindowAggregation()
    aggregation.time_key = _get_timestamp_field(args, df_schema)
    is_continuous = (
        args.materialized_feature_view_args.stream_processing_mode
        == StreamProcessingModeProto.STREAM_PROCESSING_MODE_CONTINUOUS
    )
    aggregation.is_continuous = is_continuous
    aggregation.aggregation_slide_period.CopyFrom(args.materialized_feature_view_args.aggregation_interval)

    for feature_aggregation in args.materialized_feature_view_args.aggregations:
        aggregation.features.extend(
            _create_aggregate_features(
                feature_aggregation, args.materialized_feature_view_args.aggregation_interval, is_continuous
            )
        )
    return aggregation


@typechecked
def _create_aggregate_features(
    feature_aggregation: FeatureAggregationProto, aggregation_interval_seconds: Duration, is_continuous: bool
) -> List[AggregateFeature]:
    """Build a list of AggregateFeature from the input FeatureAggregationProto."""
    aggregation_features = []
    feature_function = _AGGREGATION_FUNC_STR_TO_ENUM[feature_aggregation.function.lower()]
    assert feature_function, f"Unknown aggregation name: {feature_aggregation.function}"
    feature = AggregateFeature()
    feature.input_feature_name = feature_aggregation.column
    feature.function = feature_function
    feature.window.CopyFrom(feature_aggregation.time_window)

    if feature.function in {
        AggregationFunction.AGGREGATION_FUNCTION_LAST_DISTINCT_N,
        AggregationFunction.AGGREGATION_FUNCTION_LAST_NON_DISTINCT_N,
    }:
        feature.function_params.last_n.n = feature_aggregation.function_params["n"].int64_value
        function_name = feature_aggregation.function.lower() + str(feature.function_params.last_n.n)
    elif feature.function in {
        AggregationFunction.AGGREGATION_FUNCTION_FIRST_DISTINCT_N,
        AggregationFunction.AGGREGATION_FUNCTION_FIRST_NON_DISTINCT_N,
    }:
        feature.function_params.first_n.n = feature_aggregation.function_params["n"].int64_value
        function_name = feature_aggregation.function.lower() + str(feature.function_params.first_n.n)
    else:
        function_name = feature_aggregation.function.lower()
    feature.output_feature_name = feature_aggregation.name or construct_aggregation_output_feature_name(
        column=feature_aggregation.column,
        function=function_name,
        window=feature_aggregation.time_window,
        aggregation_interval=aggregation_interval_seconds,
        is_continuous=is_continuous,
    )
    aggregation_features.append(feature)
    return aggregation_features


@typechecked
def _get_batch_schedule(args: FeatureViewArgs) -> timedelta:
    assert args.HasField("materialized_feature_view_args")
    batch_schedule = args.materialized_feature_view_args.batch_schedule.ToTimedelta()
    if batch_schedule > timedelta(0):
        return batch_schedule

    aggregation_interval = args.materialized_feature_view_args.aggregation_interval.ToTimedelta()
    assert aggregation_interval > timedelta(0), "batch_schedule or aggregation_interval must be > 0"
    return aggregation_interval


@typechecked
def _get_timestamp_field(args: FeatureViewArgs, df_schema: StructType) -> str:
    if args.materialized_feature_view_args.timestamp_field:
        return args.materialized_feature_view_args.timestamp_field

    timestamp_fields = [field for field in df_schema if field.dataType == TimestampType()]

    assert (
        len(timestamp_fields) == 1
    ), "To use run(), timestamp_field must be set or the feature view output should contain exactly one TimestampType column."
    return timestamp_fields[0].name


@typechecked
def _validate_batch_mock_sources_keys(args: FeatureViewArgs, mock_sources: Dict[str, DataFrame]):
    expected_input_names = get_all_input_keys(args.pipeline.root)
    mock_sources_keys = set(mock_sources.keys())
    if not mock_sources_keys.issubset(expected_input_names):
        raise errors.FV_INVALID_MOCK_SOURCES(mock_sources_keys, expected_input_names)
