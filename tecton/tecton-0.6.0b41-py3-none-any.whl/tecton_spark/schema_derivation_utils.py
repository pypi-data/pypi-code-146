"""Utilities for deriving data source and feature view schemas. Shared by backend and local schema derivation."""
import datetime
from typing import Callable
from typing import Optional
from typing import Sequence

import pendulum
import pyspark
from pyspark.sql import types as pyspark_types
from typeguard import typechecked

from tecton_core import filter_context
from tecton_core import specs
from tecton_proto.args import feature_view_pb2
from tecton_proto.common import schema_pb2
from tecton_proto.common import spark_schema_pb2
from tecton_spark import data_source_helper
from tecton_spark import errors_spark
from tecton_spark import pipeline_helper
from tecton_spark import schema_spark_utils
from tecton_spark import spark_schema_wrapper


@typechecked
def get_hive_table_schema(
    spark: pyspark.sql.SparkSession,
    database: str,
    table: str,
    post_processor: Optional[Callable],
    timestamp_field: str,
    timestamp_format: str,
) -> spark_schema_pb2.SparkSchema:
    df = data_source_helper._get_raw_hive_table_dataframe(spark, database, table)
    if post_processor is not None:
        df = post_processor(df)
    if timestamp_field:
        ts_format = None
        if timestamp_format:
            ts_format = timestamp_format
        df = data_source_helper.apply_timestamp_column(df, timestamp_field, ts_format)
    return spark_schema_wrapper.SparkSchemaWrapper.from_spark_schema(df.schema)


@typechecked
def get_snowflake_schema(
    spark: pyspark.sql.SparkSession,
    url: str,
    database: str,
    schema: str,
    warehouse: str,
    role: Optional[str],
    table: Optional[str],
    query: Optional[str],
    post_processor: Optional[Callable],
) -> spark_schema_pb2.SparkSchema:

    assert table is not None or query is not None, "Both table and query cannot be None"

    df = data_source_helper.get_snowflake_dataframe(
        spark,
        url,
        database,
        schema,
        warehouse,
        role=role,
        table=table,
        query=query,
    )
    if post_processor is not None:
        df = post_processor(df)
    return spark_schema_wrapper.SparkSchemaWrapper.from_spark_schema(df.schema)


@typechecked
def get_batch_data_source_function_schema(
    spark: pyspark.sql.SparkSession, data_source_function: Callable, supports_time_filtering: bool
) -> spark_schema_pb2.SparkSchema:
    if supports_time_filtering:
        df_fc_none = data_source_function(spark=spark, filter_context=None)
        df_fc_none_start_none_end = data_source_function(
            spark=spark, filter_context=filter_context.FilterContext(None, None)
        )
        df_fc_none_end = data_source_function(
            spark=spark, filter_context=filter_context.FilterContext(pendulum.datetime(1970, 1, 1), None)
        )
        df_fc_none_start = data_source_function(
            spark=spark, filter_context=filter_context.FilterContext(None, pendulum.now())
        )
        schema = df_fc_none.schema
        # Verify filter_context is handled correctly. Schema should be the same for all values of filter_context.
        filter_context_error_message = (
            f"Invalid handling of filter_context and time filtering. Data Source Function {data_source_function.__name__} "
            f"needs to return a DataFrame with the same schema for all values of filter_context"
        )
        assert all(
            df.schema == schema for df in [df_fc_none_start_none_end, df_fc_none_end, df_fc_none_start]
        ), filter_context_error_message

        df = df_fc_none
    else:
        df = data_source_function(spark=spark)
    assert isinstance(df, pyspark.sql.dataframe.DataFrame), "Data Source Function must return a DataFrame"
    return spark_schema_wrapper.SparkSchemaWrapper.from_spark_schema(df.schema)


def get_file_source_schema(
    spark: pyspark.sql.SparkSession,
    file_format: str,
    file_uri: str,
    convert_to_glue: bool,
    schema_uri: Optional[str],
    schema_override: Optional[spark_schema_wrapper.SparkSchemaWrapper],
    post_processor: Optional[Callable],
    timestamp_col: Optional[str],
    timestmap_format: Optional[str],
) -> spark_schema_pb2.SparkSchema:
    reader = spark.read
    if schema_uri is not None:
        uri = schema_uri
        assert schema_uri.startswith(file_uri), f"{schema_uri} must contain {file_uri}"
        # Setting basePath includes the path-based partitions in the DataFrame schema.
        # https://spark.apache.org/docs/latest/sql-data-sources-parquet.html#partition-discovery
        reader = reader.option("basePath", file_uri)
    else:
        uri = file_uri

    if schema_override is not None:
        reader = reader.schema(schema_override.unwrap())

    if file_format == "json":
        action = lambda: reader.json(uri)
    elif file_format == "parquet":
        action = lambda: reader.parquet(uri)
    elif file_format == "csv":
        action = lambda: reader.csv(uri, header=True)
    else:
        raise AssertionError(f"Unsupported file format '{file_format}'")

    df = errors_spark.handleDataAccessErrors(action, file_uri)

    if convert_to_glue:
        df = data_source_helper.convert_json_like_schema_to_glue_format(spark, df)
    if post_processor is not None:
        df = post_processor(df)

    if timestamp_col is not None:
        df = data_source_helper.apply_timestamp_column(df, timestamp_col, timestmap_format)

    return spark_schema_wrapper.SparkSchemaWrapper.from_spark_schema(df.schema)


@typechecked
def get_kinesis_schema(
    spark: pyspark.sql.SparkSession, stream_name: str, post_processor: Callable
) -> spark_schema_pb2.SparkSchema:
    """Compute the Kinesis schema using mock Kinesis data.

    Creates a mocked DataFrame for this stream, without actually creating a stream reader.
    This method returns a message in the Kinesis message format (below) with mocked contents.

    |-- approximateArrivalTimestamp: timestamp
    |-- data: binary
    |-- partitionKey: string
    |-- sequenceNumber: string
    |-- streamName: string
    """
    row = pyspark.Row(
        data=bytearray("no_data", "utf-8"),
        streamName=stream_name,
        partitionKey="0",
        sequenceNumber="0",
        approximateArrivalTimestamp=datetime.datetime.fromtimestamp(0),
    )
    df = spark.createDataFrame([row])

    df = post_processor(df)

    return spark_schema_wrapper.SparkSchemaWrapper.from_spark_schema(df.schema)


# https://docs.databricks.com/spark/latest/structured-streaming/kafka.html
KAFKA_SCHEMA = pyspark_types.StructType(
    [
        pyspark_types.StructField("key", pyspark_types.BinaryType(), True),
        pyspark_types.StructField("value", pyspark_types.BinaryType(), True),
        pyspark_types.StructField("topic", pyspark_types.StringType(), True),
        pyspark_types.StructField("partition", pyspark_types.IntegerType(), True),
        pyspark_types.StructField("offset", pyspark_types.LongType(), True),
        pyspark_types.StructField("timestamp", pyspark_types.TimestampType(), True),
        pyspark_types.StructField("timestampType", pyspark_types.IntegerType(), True),
    ]
)


@typechecked
def get_kafka_schema(spark: pyspark.sql.SparkSession, post_processor: Callable) -> spark_schema_pb2.SparkSchema:
    """Compute the Kafka schema using mock Kafka data."""
    df = spark.createDataFrame([], KAFKA_SCHEMA)
    df = post_processor(df)
    return spark_schema_wrapper.SparkSchemaWrapper.from_spark_schema(df.schema)


@typechecked
def get_stream_data_source_function_schema(
    spark: pyspark.sql.SparkSession, data_source_fn: Callable
) -> spark_schema_pb2.SparkSchema:
    """Compute the Kafka schema using mock Kafka data."""
    df = data_source_fn(spark=spark)
    assert (
        isinstance(df, pyspark.sql.dataframe.DataFrame) and df.isStreaming
    ), "Data Source Function must return a streaming DataFrame"
    return spark_schema_wrapper.SparkSchemaWrapper.from_spark_schema(df.schema)


@typechecked
def get_feature_view_view_schema(
    spark: pyspark.sql.SparkSession,
    feature_view: feature_view_pb2.FeatureViewArgs,
    transformations: Sequence[specs.TransformationSpec],
    data_sources: Sequence[specs.DataSourceSpec],
) -> schema_pb2.Schema:
    """Compute the Feature View view schema."""
    df = get_feature_view_empty_view_df(spark, feature_view, transformations, data_sources)
    return schema_spark_utils.schema_from_spark(df.schema).to_proto()


@typechecked
def get_feature_view_empty_view_df(
    spark: pyspark.sql.SparkSession,
    feature_view: feature_view_pb2.FeatureViewArgs,
    transformations: Sequence[specs.TransformationSpec],
    data_sources: Sequence[specs.DataSourceSpec],
) -> pyspark.sql.DataFrame:
    """Return a pyspark dataframe for the feature view "view" (i.e. before agggregations) using mock/empty data."""
    # TODO: rm temporary check here and put in DataSource validation
    for ds in data_sources:
        # Data sources are not required to have the timestamp column set, but if it is set, the column should be in
        # the data source schema.
        if ds.batch_source.timestamp_field:
            assert any(
                [ds.batch_source.timestamp_field == column.name for column in ds.batch_source.spark_schema.fields]
            ), "Timestamp column not found in data source schema"

    # Create empty data frames for each DS input matching the DS schema.
    id_to_ds = {ds.id: ds for ds in data_sources}
    empty_mock_inputs = pipeline_helper.populate_empty_passed_in_inputs(feature_view.pipeline.root, id_to_ds, spark)

    return pipeline_helper.pipeline_to_dataframe(
        spark,
        pipeline=feature_view.pipeline,
        consume_streaming_data_sources=False,
        data_sources=data_sources,
        transformations=transformations,
        passed_in_inputs=empty_mock_inputs,
        schedule_interval=_batch_schedule_from_fv(feature_view),
    )


def _batch_schedule_from_fv(feature_view: feature_view_pb2.FeatureViewArgs) -> Optional[pendulum.Duration]:
    if feature_view.HasField("temporal_args"):
        return pendulum.Duration(seconds=feature_view.temporal_args.schedule_interval.ToSeconds())
    elif feature_view.HasField("temporal_aggregate_args"):
        return pendulum.Duration(seconds=feature_view.temporal_aggregate_args.schedule_interval.ToSeconds())
    elif feature_view.HasField("materialized_feature_view_args"):
        return pendulum.Duration(seconds=feature_view.materialized_feature_view_args.batch_schedule.ToSeconds())
    else:
        return None
