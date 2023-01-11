import tempfile
from datetime import datetime
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Sequence
from typing import Union

import pandas as pd
import pendulum
from pyspark import sql as pyspark_sql
from pyspark.sql import streaming as pyspark_streaming

from tecton import tecton_context
from tecton._internals import errors
from tecton._internals import time_utils
from tecton._internals import utils
from tecton.interactive.data_frame import TectonDataFrame
from tecton.interactive.dataset import Dataset
from tecton.tecton_context import TectonContext
from tecton_core import materialization_context
from tecton_core import query_consts
from tecton_core import specs
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.feature_set_config import FeatureDefinitionAndJoinConfig
from tecton_core.logger import get_logger
from tecton_core.query import builder
from tecton_core.query import nodes
from tecton_core.query import sql_compat
from tecton_core.time_utils import align_time_downwards
from tecton_proto.args import feature_view_pb2
from tecton_proto.args import virtual_data_source_pb2 as virtual_data_source__args_pb2
from tecton_proto.common import schema_pb2
from tecton_proto.common import spark_schema_pb2
from tecton_proto.data.feature_view_pb2 import MaterializationTimeRangePolicy
from tecton_spark import data_source_helper
from tecton_spark import schema_derivation_utils
from tecton_spark import spark_schema_wrapper
from tecton_spark.spark_helper import check_spark_version
from tecton_spark.time_utils import convert_epoch_to_datetime
from tecton_spark.time_utils import convert_timestamp_to_epoch

logger = get_logger("spark_api")


def get_historical_features_for_feature_definition(
    feature_definition: FeatureDefinitionWrapper,
    spine: Optional[Union[pyspark_sql.DataFrame, pd.DataFrame, TectonDataFrame]],
    timestamp_key: Optional[str],
    start_time: Optional[Union[pendulum.DateTime, datetime]],
    end_time: Optional[Union[pendulum.DateTime, datetime]],
    entities: Optional[Union[pyspark_sql.DataFrame, pd.DataFrame, TectonDataFrame]],
    from_source: bool,
    save: bool,
    save_as: Optional[str],
) -> TectonDataFrame:
    if not feature_definition.is_on_demand:
        check_spark_version(feature_definition.fv_spec.batch_cluster_config)

    has_point_in_time_join_params = spine is not None
    has_get_features_params = start_time is not None or end_time is not None or entities is not None

    if has_point_in_time_join_params:
        if not isinstance(spine, TectonDataFrame):
            spine = TectonDataFrame._create(spine)
        if spine is not None and _should_infer_timestamp_of_spine(feature_definition, timestamp_key):
            timestamp_key = utils.infer_timestamp(spine.to_spark())

        df = _point_in_time_get_historical_features_for_feature_definition(
            feature_definition, spine, timestamp_key, from_source
        )
    else:
        df = _time_range_get_historical_features_for_feature_definition(
            feature_definition,
            start_time=start_time,
            end_time=end_time,
            entities=entities,
            from_source=from_source,
        )

    if save or save_as is not None:
        return Dataset._create(
            df=df,
            save_as=save_as,
            workspace=feature_definition.workspace,
            feature_definition_id=feature_definition.id,
            spine=spine,
            timestamp_key=timestamp_key,
        )
    return df


def _should_infer_timestamp_of_spine(
    feature_definition: FeatureDefinitionWrapper,
    timestamp_key: Optional[str],
):
    if feature_definition.is_on_demand:
        # If the ODFV does not depend on any materialized feature definitions, then there is no need to infer a
        # timestamp key.
        return (
            timestamp_key is None
            and utils.get_num_dependent_fv(feature_definition.pipeline.root, visited_inputs={}) > 0
        )
    else:
        return timestamp_key is None


def _point_in_time_get_historical_features_for_feature_definition(
    feature_definition: FeatureDefinitionWrapper,
    spine: TectonDataFrame,
    timestamp_key: Optional[str],
    from_source: bool,
) -> TectonDataFrame:
    # TODO(alvin) validation should not depend on spark
    if feature_definition.is_on_demand:
        utils.validate_spine_dataframe(spine.to_spark(), timestamp_key, feature_definition.request_context_keys)
    else:
        utils.validate_spine_dataframe(spine.to_spark(), timestamp_key)

    dac = FeatureDefinitionAndJoinConfig.from_feature_definition(feature_definition)
    return TectonDataFrame._create(
        builder.build_spine_join_querytree(
            dac,
            nodes.UserSpecifiedDataNode(spine).as_ref(),
            timestamp_key,
            from_source,
        )
    )


def _most_recent_tile_end_time(fd: FeatureDefinitionWrapper, timestamp: datetime) -> int:
    """Computes the most recent tile end time which is ready to be computed.

    :param timestamp: The timestamp in python datetime format
    :return: The timestamp in seconds of the greatest ready tile end time <= timestamp.
    """
    # Account for data delay
    timestamp = timestamp - fd.allowed_upstream_lateness
    aligned_left = align_time_downwards(timestamp, fd.min_scheduling_interval)
    return convert_timestamp_to_epoch(aligned_left, fd.get_feature_store_format_version)


def _time_range_get_historical_features_for_feature_definition(
    fd: FeatureDefinitionWrapper,
    entities: Optional[Union[pyspark_sql.DataFrame, pd.DataFrame, TectonDataFrame]],
    start_time: Optional[Union[pendulum.DateTime, datetime]],
    end_time: Optional[Union[pendulum.DateTime, datetime]],
    from_source: bool,
) -> TectonDataFrame:
    if start_time is not None and isinstance(start_time, datetime):
        start_time = pendulum.instance(start_time)
    if end_time is not None and isinstance(end_time, datetime):
        end_time = pendulum.instance(end_time)

    if start_time is not None and fd.feature_start_timestamp is not None and start_time < fd.feature_start_timestamp:
        logger.warning(
            f'The provided start_time ({start_time}) is before "{fd.name}"\'s feature_start_time ({fd.feature_start_timestamp}). No feature values will be returned before the feature_start_time.'
        )
        start_time = fd.feature_start_timestamp

    # TODO(brian): construct the timestamps a bit more directly. This code in
    # general reuses utilities not really meant for the semantics of this API.
    if fd.is_temporal_aggregate or fd.is_temporal:
        # Feature views where materialization is not enabled may not have a feature_start_time.
        _start = start_time or fd.feature_start_timestamp or pendulum.datetime(1970, 1, 1)
        # we need to add 1 to most_recent_anchor since we filter end_time exclusively
        if end_time:
            _end = end_time
        else:
            anchor_time = _most_recent_tile_end_time(fd, pendulum.now("UTC") - fd.min_scheduling_interval)
            _end = convert_epoch_to_datetime(anchor_time, fd.get_feature_store_format_version) + pendulum.duration(
                microseconds=1
            )
    else:
        _start = start_time or pendulum.datetime(1970, 1, 1)
        _end = end_time or pendulum.now("UTC")

    time_range = pendulum.Period(_start, _end)

    tc = TectonContext.get_instance()
    spark = tc._spark
    effective_timestamp_field = sql_compat.default_case(query_consts.EFFECTIVE_TIMESTAMP)

    # TODO(felix): Move this logic to `builder.py` once it does not rely on Spark-specific time util functions.
    if fd.is_temporal or fd.is_feature_table:
        qt = builder.build_get_features(fd, from_source=from_source, feature_data_time_limits=time_range)
        qt = nodes.RenameColsNode(qt, drop=[sql_compat.default_case(query_consts.ANCHOR_TIME)]).as_ref()
        batch_schedule_seconds = 0 if fd.is_feature_table else fd.batch_materialization_schedule.in_seconds()

        qt = nodes.AddEffectiveTimestampNode(
            qt,
            timestamp_field=fd.timestamp_key,
            effective_timestamp_name=effective_timestamp_field,
            batch_schedule_seconds=batch_schedule_seconds,
            data_delay_seconds=fd.online_store_data_delay_seconds,
            is_stream=fd.is_stream,
            is_temporal_aggregate=False,
        ).as_ref()
    else:
        feature_data_time_limits = time_utils.get_feature_data_time_limits(
            fd=fd,
            spine_time_limits=time_range,
        )
        # TODO(brian): refactor to share more with run api full aggregation
        qt = builder.build_get_full_agg_features(
            fd,
            from_source=from_source,
            feature_data_time_limits=feature_data_time_limits,
            show_effective_time=True,
        )

    # Validate that entities only contains Join Key Columns.
    if entities is not None:
        if not isinstance(entities, TectonDataFrame):
            entities = TectonDataFrame._create(entities)
        assert set(entities._dataframe.columns).issubset(
            set(fd.join_keys)
        ), f"Entities should only contain columns that can be used as Join Keys: {fd.join_keys}"
        columns = entities.columns
        entities_df = nodes.SelectDistinctNode(nodes.UserSpecifiedDataNode(entities).as_ref(), columns).as_ref()
        qt = nodes.JoinNode(qt, entities_df, columns, how="right").as_ref()

    qt = nodes.FeatureTimeFilterNode(
        qt,
        feature_data_time_limits=time_range,
        policy=MaterializationTimeRangePolicy.MATERIALIZATION_TIME_RANGE_POLICY_FILTER_TO_RANGE,
        timestamp_field=fd.timestamp_key,
    ).as_ref()
    return TectonDataFrame._create(qt)


def get_dataframe_for_data_source(
    data_source: specs.DataSourceSpec,
    start_time: datetime,
    end_time: datetime,
    apply_translator: bool,
) -> TectonDataFrame:
    spark = TectonContext.get_instance()._spark
    if isinstance(data_source.batch_source, specs.SparkBatchSourceSpec):
        if not data_source.batch_source.supports_time_filtering and (start_time or end_time):
            raise errors.DS_INCORRECT_SUPPORTS_TIME_FILTERING

        node = builder.build_datasource_scan_node(
            data_source, for_stream=False, start_time=start_time, end_time=end_time
        )
        return TectonDataFrame._create(node)

    elif apply_translator:
        timestamp_key = data_source.batch_source.timestamp_field
        if not timestamp_key and (start_time or end_time):
            raise errors.DS_DATAFRAME_NO_TIMESTAMP

        node = builder.build_datasource_scan_node(
            data_source, for_stream=False, start_time=start_time, end_time=end_time
        )
        return TectonDataFrame._create(node)
    else:
        if start_time is not None or end_time is not None:
            raise errors.DS_RAW_DATAFRAME_NO_TIMESTAMP_FILTER

        node = nodes.RawDataSourceScanNode(data_source).as_ref()
        return TectonDataFrame._create(node)


def start_stream_preview(
    data_source: specs.DataSourceSpec,
    table_name: str,
    apply_translator: bool,
    option_overrides: Optional[Dict[str, str]],
) -> pyspark_streaming.StreamingQuery:
    df = get_stream_preview_dataframe(data_source, apply_translator, option_overrides)

    with tempfile.TemporaryDirectory() as d:
        return (
            df.writeStream.format("memory")
            .queryName(table_name)
            .option("checkpointLocation", d)
            .outputMode("append")
            .start()
        )


def get_stream_preview_dataframe(
    data_source: specs.DataSourceSpec, apply_translator: bool, option_overrides: Optional[Dict[str, str]]
) -> pyspark_sql.DataFrame:
    """
    Helper function that allows start_stream_preview() to be unit tested, since we can't easily unit test writing
    to temporary tables.
    """
    spark = tecton_context.TectonContext.get_instance()._spark

    if apply_translator or isinstance(data_source.stream_source, specs.SparkStreamSourceSpec):
        return data_source_helper.get_ds_dataframe(
            spark, data_source, consume_streaming_data_source=True, stream_option_overrides=option_overrides
        )
    else:
        return data_source_helper.get_non_dsf_raw_stream_dataframe(spark, data_source.stream_source, option_overrides)


def derive_view_schema_for_feature_view(
    fv_args: feature_view_pb2.FeatureViewArgs,
    transformations: Sequence[specs.TransformationSpec],
    data_sources: Sequence[specs.DataSourceSpec],
) -> schema_pb2.Schema:
    spark = TectonContext.get_instance()._spark
    return schema_derivation_utils.get_feature_view_view_schema(spark, fv_args, transformations, data_sources)


def derive_batch_schema(
    ds_args: virtual_data_source__args_pb2.VirtualDataSourceArgs,
    batch_post_processor: Optional[Callable],
    batch_data_source_function: Optional[Callable],
) -> spark_schema_pb2.SparkSchema:
    spark = TectonContext.get_instance()._spark
    if ds_args.HasField("hive_ds_config"):
        return schema_derivation_utils.get_hive_table_schema(
            spark=spark,
            table=ds_args.hive_ds_config.table,
            database=ds_args.hive_ds_config.database,
            post_processor=batch_post_processor,
            timestamp_field=ds_args.hive_ds_config.common_args.timestamp_field,
            timestamp_format=ds_args.hive_ds_config.timestamp_format,
        )
    elif ds_args.HasField("spark_batch_config"):
        return schema_derivation_utils.get_batch_data_source_function_schema(
            spark=spark,
            data_source_function=batch_data_source_function,
            supports_time_filtering=ds_args.spark_batch_config.supports_time_filtering,
        )
    elif ds_args.HasField("redshift_ds_config"):
        # TODO(jake)
        return spark_schema_pb2.SparkSchema()
    elif ds_args.HasField("snowflake_ds_config"):
        assert ds_args.snowflake_ds_config.HasField("url"), "url cannot be None"
        assert ds_args.snowflake_ds_config.HasField("database"), "database cannot be None"
        assert ds_args.snowflake_ds_config.HasField("schema"), "schema cannot be None"
        assert ds_args.snowflake_ds_config.HasField("warehouse"), "warehouse cannot be None"

        return schema_derivation_utils.get_snowflake_schema(
            spark=spark,
            url=ds_args.snowflake_ds_config.url,
            database=ds_args.snowflake_ds_config.database,
            schema=ds_args.snowflake_ds_config.schema,
            warehouse=ds_args.snowflake_ds_config.warehouse,
            role=ds_args.snowflake_ds_config.role if ds_args.snowflake_ds_config.HasField("role") else None,
            table=ds_args.snowflake_ds_config.table if ds_args.snowflake_ds_config.HasField("table") else None,
            query=ds_args.snowflake_ds_config.query if ds_args.snowflake_ds_config.HasField("query") else None,
            post_processor=batch_post_processor,
        )
    elif ds_args.HasField("file_ds_config"):
        schema_override = None
        if ds_args.file_ds_config.HasField("schema_override"):
            schema_override = spark_schema_wrapper.SparkSchemaWrapper.from_proto(ds_args.file_ds_config.schema_override)

        schema_uri = ds_args.file_ds_config.schema_uri if ds_args.file_ds_config.HasField("schema_uri") else None
        timestamp_column = (
            ds_args.file_ds_config.common_args.timestamp_field
            if ds_args.file_ds_config.common_args.HasField("timestamp_field")
            else None
        )
        timestamp_format = (
            ds_args.file_ds_config.timestamp_format if ds_args.file_ds_config.HasField("timestamp_format") else None
        )

        return schema_derivation_utils.get_file_source_schema(
            spark=spark,
            file_format=ds_args.file_ds_config.file_format,
            file_uri=ds_args.file_ds_config.uri,
            convert_to_glue=ds_args.file_ds_config.convert_to_glue_format,
            schema_uri=schema_uri,
            schema_override=schema_override,
            post_processor=batch_post_processor,
            timestamp_col=timestamp_column,
            timestmap_format=timestamp_format,
        )
    else:
        raise ValueError(f"Invalid batch source args: {ds_args}")


def derive_stream_schema(
    ds_args: virtual_data_source__args_pb2.VirtualDataSourceArgs,
    stream_post_processor: Optional[Callable],
    stream_data_source_function: Optional[Callable],
) -> spark_schema_pb2.SparkSchema:
    spark = TectonContext.get_instance()._spark
    if ds_args.HasField("kinesis_ds_config"):
        return schema_derivation_utils.get_kinesis_schema(
            spark, ds_args.kinesis_ds_config.stream_name, stream_post_processor
        )
    elif ds_args.HasField("kafka_ds_config"):
        return schema_derivation_utils.get_kafka_schema(spark, stream_post_processor)
    elif ds_args.HasField("spark_stream_config"):
        return schema_derivation_utils.get_stream_data_source_function_schema(spark, stream_data_source_function)
    else:
        raise ValueError(f"Invalid stream source args: {ds_args}")


_TRANSFORMATION_RUN_TEMP_VIEW_PREFIX = "_tecton_transformation_run_"
CONST_TYPE = Union[str, int, float, bool]


def run_transformation_mode_spark_sql(
    *inputs: Union[pd.DataFrame, pd.Series, TectonDataFrame, pyspark_sql.DataFrame, CONST_TYPE],
    transformer: Callable,
    context: materialization_context.BaseMaterializationContext = None,
    transformation_name: str,
) -> TectonDataFrame:
    def create_temp_view(df, dataframe_index) -> str:
        df = TectonDataFrame._create(df).to_spark()
        temp_view = f"{_TRANSFORMATION_RUN_TEMP_VIEW_PREFIX}{transformation_name}_input_{dataframe_index}"
        df.createOrReplaceTempView(temp_view)
        return temp_view

    args = [create_temp_view(v, i) if not isinstance(v, CONST_TYPE.__args__) else v for i, v in enumerate(inputs)]
    if context is not None:
        args.append(context)

    spark = TectonContext.get_instance()._get_spark()
    return TectonDataFrame._create(spark.sql(transformer(*args)))


def run_transformation_mode_pyspark(
    *inputs: Union[pd.DataFrame, pd.Series, TectonDataFrame, pyspark_sql.DataFrame, CONST_TYPE],
    transformer: Callable,
    context: materialization_context.BaseMaterializationContext,
) -> TectonDataFrame:
    args = [TectonDataFrame._create(v).to_spark() if not isinstance(v, CONST_TYPE.__args__) else v for v in inputs]
    if context is not None:
        args.append(context)

    return TectonDataFrame._create(transformer(*args))
