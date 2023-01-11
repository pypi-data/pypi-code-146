from typing import Callable
from typing import Optional
from typing import Tuple
from typing import Union

import attrs
import pendulum
from typeguard import typechecked

from tecton_core import function_deserialization
from tecton_core import time_utils
from tecton_core.specs import tecton_object_spec
from tecton_core.specs import utils
from tecton_proto.args import data_source_config_pb2
from tecton_proto.args import data_source_pb2 as data_source__args_pb2
from tecton_proto.args import virtual_data_source_pb2 as virtual_data_source__args_pb2
from tecton_proto.common import data_source_type_pb2
from tecton_proto.common import schema_container_pb2
from tecton_proto.common import spark_schema_pb2
from tecton_proto.data import batch_data_source_pb2 as batch_data_source__data_pb2
from tecton_proto.data import stream_data_source_pb2 as stream_data_source__data_pb2
from tecton_proto.data import virtual_data_source_pb2 as virtual_data_source__data_pb2

__all__ = [
    "DataSourceSpec",
    "DataSourceSpecArgsSupplement",
    "BatchSourceSpec",
    "HiveSourceSpec",
    "FileSourceSpec",
    "SparkBatchSourceSpec",
    "RedshiftSourceSpec",
    "SnowflakeSourceSpec",
    "DatetimePartitionColumnSpec",
    "StreamSourceSpec",
    "KinesisSourceSpec",
    "KafkaSourceSpec",
    "SparkStreamSourceSpec",
]


@utils.frozen_strict
class BatchSourceSpec:
    """Base class for batch source specs, e.g. a HiveSourceSpec or SnowflakeSourceSpec."""

    timestamp_field: Optional[str]
    timestamp_format: Optional[str]
    post_processor: Optional[Callable] = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})
    # TODO(jake): Remove this divergence allowed tag once schema derivation is supported.
    spark_schema: spark_schema_pb2.SparkSchema = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})
    data_delay: Optional[pendulum.Duration]


@utils.frozen_strict
class StreamOptionSpec:
    key: str
    value: str


@utils.frozen_strict
class StreamSourceSpec:
    """Base class for stream source specs, e.g. a KinesisSourceSpec or KafkaSourceSpec."""

    deduplication_column_names: Tuple[str, ...]
    options: Tuple[StreamOptionSpec, ...]
    watermark_delay_threshold: pendulum.duration
    # TODO(jake): Remove this divergence allowed tag once schema derivation is supported.
    spark_schema: spark_schema_pb2.SparkSchema = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})


@attrs.define
class DataSourceSpecArgsSupplement:
    """A data class used for supplementing args protos during DataSourceSpec construction.

    This Python data class can be used to pass non-serializable types (e.g. Python functions) or data that is not
    included in args protos (e.g. schemas) into the DataSourceSpec constructor.
    """

    batch_schema: Optional[spark_schema_pb2.SparkSchema] = attrs.field(default=None)
    stream_schema: Optional[spark_schema_pb2.SparkSchema] = attrs.field(default=None)

    batch_post_processor: Optional[Callable] = attrs.field(default=None)
    stream_post_processor: Optional[Callable] = attrs.field(default=None)

    batch_data_source_function: Optional[Callable] = attrs.field(default=None)
    stream_data_source_function: Optional[Callable] = attrs.field(default=None)


@utils.frozen_strict
class DataSourceSpec(tecton_object_spec.TectonObjectSpec):
    batch_source: BatchSourceSpec
    stream_source: Optional[StreamSourceSpec]
    schema: Optional[schema_container_pb2.SchemaContainer]
    type: data_source_type_pb2.DataSourceType.ValueType

    # Temporarily expose the underlying data proto during migration.
    # TODO(TEC-12443): Remove this attribute.
    data_proto: Optional[virtual_data_source__data_pb2.VirtualDataSource] = attrs.field(
        metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True}
    )

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: virtual_data_source__data_pb2.VirtualDataSource) -> "DataSourceSpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_data_proto(
                proto.virtual_data_source_id, proto.fco_metadata
            ),
            batch_source=create_batch_source_from_data_proto(proto.batch_data_source),
            stream_source=create_stream_source_from_data_proto(proto.stream_data_source),
            type=utils.get_field_or_none(proto, "data_source_type"),
            schema=utils.get_field_or_none(proto, "schema"),
            data_proto=proto,
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls,
        proto: virtual_data_source__args_pb2.VirtualDataSourceArgs,
        supplement: DataSourceSpecArgsSupplement,
    ) -> "DataSourceSpec":
        return cls(
            metadata=tecton_object_spec.TectonObjectMetadataSpec.from_args_proto(
                proto.virtual_data_source_id, proto.info
            ),
            batch_source=create_batch_source_from_args_proto(proto, supplement),
            stream_source=create_stream_source_from_args_proto(proto, supplement),
            schema=utils.get_field_or_none(proto, "schema"),
            type=utils.get_field_or_none(proto, "type"),
            data_proto=None,
        )


@typechecked
def create_batch_source_from_data_proto(
    proto: batch_data_source__data_pb2.BatchDataSource,
) -> Optional[
    Union["HiveSourceSpec", "SparkBatchSourceSpec", "FileSourceSpec", "RedshiftSourceSpec", "SnowflakeSourceSpec"]
]:
    if proto.HasField("hive_table"):
        return HiveSourceSpec.from_data_proto(proto)
    elif proto.HasField("spark_data_source_function"):
        return SparkBatchSourceSpec.from_data_proto(proto)
    elif proto.HasField("redshift_db"):
        return RedshiftSourceSpec.from_data_proto(proto)
    elif proto.HasField("snowflake"):
        return SnowflakeSourceSpec.from_data_proto(proto)
    elif proto.HasField("file"):
        return FileSourceSpec.from_data_proto(proto)
    else:
        return None


@typechecked
def create_batch_source_from_args_proto(
    proto: virtual_data_source__args_pb2.VirtualDataSourceArgs, supplement: DataSourceSpecArgsSupplement
) -> Optional[
    Union["HiveSourceSpec", "SparkBatchSourceSpec", "FileSourceSpec", "RedshiftSourceSpec", "SnowflakeSourceSpec"]
]:
    if proto.HasField("hive_ds_config"):
        return HiveSourceSpec.from_args_proto(proto.hive_ds_config, supplement)
    elif proto.HasField("spark_batch_config"):
        return SparkBatchSourceSpec.from_args_proto(proto.spark_batch_config, supplement)
    elif proto.HasField("redshift_ds_config"):
        return RedshiftSourceSpec.from_args_proto(proto.redshift_ds_config, supplement)
    elif proto.HasField("snowflake_ds_config"):
        return SnowflakeSourceSpec.from_args_proto(proto.snowflake_ds_config, supplement)
    elif proto.HasField("file_ds_config"):
        return FileSourceSpec.from_args_proto(proto.file_ds_config, supplement)
    else:
        return None


@utils.frozen_strict
class DatetimePartitionColumnSpec:
    column_name: str
    format_string: str
    minimum_seconds: int

    @classmethod
    @typechecked
    def from_data_proto(
        cls, proto: batch_data_source__data_pb2.DatetimePartitionColumn
    ) -> "DatetimePartitionColumnSpec":
        return cls(
            column_name=utils.get_field_or_none(proto, "column_name"),
            format_string=utils.get_field_or_none(proto, "format_string"),
            minimum_seconds=utils.get_field_or_none(proto, "minimum_seconds"),
        )

    @classmethod
    @typechecked
    def from_args_proto(cls, proto: data_source__args_pb2.DatetimePartitionColumnArgs) -> "DatetimePartitionColumnSpec":
        # This constructor mirrors backend Kotlin logic: https://github.com/tecton-ai/tecton/blob/6107d76680fa97e6155c6da9ee7d2da47bc3d6a7/java/com/tecton/datamodel/datasource/Utils.kt#L41.
        # In the short-term, divergence between Python and Kotlin will be prevented using integration test coverage. Longer-term, these values should probably be derived client-side only and included in the data source args.
        if proto.datepart == "year":
            format_string = "%Y"
            minimum_seconds = 365 * 24 * 60 * 60
        elif proto.datepart == "month":
            format_string = "%m"
            minimum_seconds = 28 * 24 * 60 * 60
        elif proto.datepart == "day":
            format_string = "%d"
            minimum_seconds = 24 * 60 * 60
        elif proto.datepart == "hour":
            format_string = "%H"
            minimum_seconds = 60 * 60
        elif proto.datepart == "date":
            assert proto.zero_padded or not proto.format_string, "Non-zero padded date strings are not supported."
            format_string = "%Y-%m-%d"
            minimum_seconds = 24 * 60 * 60
        else:
            assert False, f"Unexpected datepart string: {proto.datepart}"

        if proto.format_string:
            format_string = proto.format_string
        elif not proto.zero_padded:
            format_string = format_string.replace("%", "%-")

        return DatetimePartitionColumnSpec(
            column_name=proto.column_name, format_string=format_string, minimum_seconds=minimum_seconds
        )


@utils.frozen_strict
class HiveSourceSpec(BatchSourceSpec):
    database: str
    table: str
    datetime_partition_columns: Tuple[DatetimePartitionColumnSpec, ...]

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: batch_data_source__data_pb2.BatchDataSource) -> "HiveSourceSpec":
        # Needed for canary backwards compatability. Can be deleted on the following release.
        if proto.date_partition_column and not proto.datetime_partition_columns:
            proto.datetime_partition_columns.append(
                batch_data_source__data_pb2.DatetimePartitionColumn(
                    column_name=proto.date_partition_column,
                    format_string="%Y-%m-%d",
                    minimum_seconds=24 * 60 * 60,
                )
            )

        post_processor = None
        if proto.HasField("raw_batch_translator"):
            post_processor = function_deserialization.from_proto(proto.raw_batch_translator)

        return cls(
            timestamp_field=utils.get_field_or_none(proto.timestamp_column_properties, "column_name"),
            timestamp_format=utils.get_field_or_none(proto.timestamp_column_properties, "format"),
            post_processor=post_processor,
            data_delay=utils.get_duration_field_or_none(proto, "data_delay"),
            spark_schema=utils.get_field_or_none(proto, "spark_schema"),
            table=utils.get_field_or_none(proto.hive_table, "table"),
            database=utils.get_field_or_none(proto.hive_table, "database"),
            datetime_partition_columns=tuple(
                DatetimePartitionColumnSpec.from_data_proto(column) for column in proto.datetime_partition_columns
            ),
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: data_source__args_pb2.HiveDataSourceArgs, supplement: DataSourceSpecArgsSupplement
    ) -> "HiveSourceSpec":
        return cls(
            timestamp_field=utils.get_field_or_none(proto.common_args, "timestamp_field"),
            timestamp_format=utils.get_field_or_none(proto, "timestamp_format"),
            post_processor=supplement.batch_post_processor,
            data_delay=utils.get_duration_field_or_none(proto.common_args, "data_delay"),
            spark_schema=supplement.batch_schema,
            table=utils.get_field_or_none(proto, "table"),
            database=utils.get_field_or_none(proto, "database"),
            datetime_partition_columns=tuple(
                DatetimePartitionColumnSpec.from_args_proto(column) for column in proto.datetime_partition_columns
            ),
        )


@utils.frozen_strict
class FileSourceSpec(BatchSourceSpec):
    uri: Optional[str]
    file_format: batch_data_source__data_pb2.FileDataSourceFormat.ValueType
    convert_to_glue_format: bool
    schema_uri: Optional[str]
    schema_override: Optional[spark_schema_pb2.SparkSchema]

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: batch_data_source__data_pb2.BatchDataSource) -> "FileSourceSpec":
        post_processor = None
        if proto.HasField("raw_batch_translator"):
            post_processor = function_deserialization.from_proto(proto.raw_batch_translator)

        return cls(
            timestamp_field=utils.get_field_or_none(proto.timestamp_column_properties, "column_name"),
            timestamp_format=utils.get_field_or_none(proto.timestamp_column_properties, "format"),
            post_processor=post_processor,
            data_delay=utils.get_duration_field_or_none(proto, "data_delay"),
            spark_schema=utils.get_field_or_none(proto, "spark_schema"),
            uri=utils.get_field_or_none(proto.file, "uri"),
            file_format=utils.get_field_or_none(proto.file, "format"),
            convert_to_glue_format=proto.file.convert_to_glue_format,
            schema_uri=utils.get_field_or_none(proto.file, "schema_uri"),
            schema_override=utils.get_field_or_none(proto.file, "schema_override"),
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: data_source__args_pb2.FileDataSourceArgs, supplement: DataSourceSpecArgsSupplement
    ) -> "FileSourceSpec":
        return cls(
            timestamp_field=utils.get_field_or_none(proto.common_args, "timestamp_field"),
            timestamp_format=utils.get_field_or_none(proto, "timestamp_format"),
            post_processor=supplement.batch_post_processor,
            data_delay=utils.get_duration_field_or_none(proto.common_args, "data_delay"),
            spark_schema=supplement.batch_schema,
            uri=utils.get_field_or_none(proto, "uri"),
            file_format=FileSourceSpec._convert_file_format_string_to_enum(proto.file_format),
            convert_to_glue_format=proto.convert_to_glue_format,
            schema_uri=utils.get_field_or_none(proto, "schema_uri"),
            schema_override=utils.get_field_or_none(proto, "schema_override"),
        )

    @staticmethod
    @typechecked
    def _convert_file_format_string_to_enum(
        file_format: str,
    ) -> batch_data_source__data_pb2.FileDataSourceFormat.ValueType:
        return batch_data_source__data_pb2.FileDataSourceFormat.Value(f"FILE_DATA_SOURCE_FORMAT_{file_format.upper()}")


@utils.frozen_strict
class SparkBatchSourceSpec(BatchSourceSpec):
    function: Callable = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})
    supports_time_filtering: bool

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: batch_data_source__data_pb2.BatchDataSource) -> "SparkBatchSourceSpec":
        function = None
        if proto.spark_data_source_function.HasField("function"):
            function = function_deserialization.from_proto(proto.spark_data_source_function.function)

        return cls(
            timestamp_field=None,
            timestamp_format=None,
            post_processor=None,
            data_delay=utils.get_duration_field_or_none(proto, "data_delay"),
            spark_schema=utils.get_field_or_none(proto, "spark_schema"),
            supports_time_filtering=proto.spark_data_source_function.supports_time_filtering,
            function=function,
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: data_source__args_pb2.SparkBatchConfigArgs, supplement: DataSourceSpecArgsSupplement
    ) -> "SparkBatchSourceSpec":
        return cls(
            timestamp_field=None,
            timestamp_format=None,
            post_processor=None,
            data_delay=utils.get_duration_field_or_none(proto, "data_delay"),
            spark_schema=supplement.batch_schema,
            supports_time_filtering=proto.supports_time_filtering,
            function=supplement.batch_data_source_function,
        )


@utils.frozen_strict
class RedshiftSourceSpec(BatchSourceSpec):
    endpoint: str
    table: Optional[str]
    query: Optional[str]
    temp_s3: Optional[str]

    def __attrs_post_init__(self):
        assert self.table or self.query, "Invalid RedshiftSourceSpec: no table or query provided."

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: batch_data_source__data_pb2.BatchDataSource) -> "RedshiftSourceSpec":
        post_processor = None
        if proto.HasField("raw_batch_translator"):
            post_processor = function_deserialization.from_proto(proto.raw_batch_translator)

        return cls(
            timestamp_field=utils.get_field_or_none(proto.timestamp_column_properties, "column_name"),
            timestamp_format=utils.get_field_or_none(proto.timestamp_column_properties, "format"),
            post_processor=post_processor,
            data_delay=utils.get_duration_field_or_none(proto, "data_delay"),
            spark_schema=utils.get_field_or_none(proto, "spark_schema"),
            endpoint=utils.get_field_or_none(proto.redshift_db, "endpoint"),
            table=utils.get_field_or_none(proto.redshift_db, "table"),
            query=utils.get_field_or_none(proto.redshift_db, "query"),
            temp_s3=utils.get_field_or_none(proto.redshift_db, "temp_s3"),
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: data_source__args_pb2.RedshiftDataSourceArgs, supplement: DataSourceSpecArgsSupplement
    ) -> "RedshiftSourceSpec":
        return cls(
            timestamp_field=utils.get_field_or_none(proto.common_args, "timestamp_field"),
            timestamp_format=None,
            post_processor=supplement.batch_post_processor,
            data_delay=utils.get_duration_field_or_none(proto.common_args, "data_delay"),
            spark_schema=supplement.batch_schema,
            endpoint=utils.get_field_or_none(proto, "endpoint"),
            table=utils.get_field_or_none(proto, "table"),
            query=utils.get_field_or_none(proto, "query"),
            temp_s3=None,
        )


@utils.frozen_strict
class SnowflakeSourceSpec(BatchSourceSpec):
    database: str
    schema: str
    warehouse: Optional[str]
    url: Optional[str]
    role: Optional[str]
    table: Optional[str]
    query: Optional[str]

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: batch_data_source__data_pb2.BatchDataSource) -> "SnowflakeSourceSpec":
        post_processor = None
        if proto.HasField("raw_batch_translator"):
            post_processor = function_deserialization.from_proto(proto.raw_batch_translator)
        return cls(
            timestamp_field=utils.get_field_or_none(proto.timestamp_column_properties, "column_name"),
            timestamp_format=utils.get_field_or_none(proto.timestamp_column_properties, "format"),
            post_processor=post_processor,
            data_delay=utils.get_duration_field_or_none(proto, "data_delay"),
            spark_schema=utils.get_field_or_none(proto, "spark_schema"),
            url=utils.get_field_or_none(proto.snowflake.snowflakeArgs, "url"),
            database=utils.get_field_or_none(proto.snowflake.snowflakeArgs, "database"),
            schema=utils.get_field_or_none(proto.snowflake.snowflakeArgs, "schema"),
            warehouse=utils.get_field_or_none(proto.snowflake.snowflakeArgs, "warehouse"),
            role=utils.get_field_or_none(proto.snowflake.snowflakeArgs, "role"),
            table=utils.get_field_or_none(proto.snowflake.snowflakeArgs, "table"),
            query=utils.get_field_or_none(proto.snowflake.snowflakeArgs, "query"),
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: data_source__args_pb2.SnowflakeDataSourceArgs, supplement: DataSourceSpecArgsSupplement
    ) -> "SnowflakeSourceSpec":
        return cls(
            timestamp_field=utils.get_field_or_none(proto.common_args, "timestamp_field"),
            timestamp_format=None,
            post_processor=supplement.batch_post_processor,
            data_delay=utils.get_duration_field_or_none(proto.common_args, "data_delay"),
            spark_schema=supplement.batch_schema,
            url=utils.get_field_or_none(proto, "url"),
            database=utils.get_field_or_none(proto, "database"),
            schema=utils.get_field_or_none(proto, "schema"),
            warehouse=utils.get_field_or_none(proto, "warehouse"),
            role=utils.get_field_or_none(proto, "role"),
            table=utils.get_field_or_none(proto, "table"),
            query=utils.get_field_or_none(proto, "query"),
        )


@typechecked
def create_stream_source_from_data_proto(
    proto: stream_data_source__data_pb2.StreamDataSource,
) -> Optional[Union["KinesisSourceSpec", "KafkaSourceSpec", "SparkStreamSourceSpec"]]:
    if proto.HasField("kinesis_data_source"):
        return KinesisSourceSpec.from_data_proto(proto)
    elif proto.HasField("kafka_data_source"):
        return KafkaSourceSpec.from_data_proto(proto)
    elif proto.HasField("spark_data_source_function"):
        return SparkStreamSourceSpec.from_data_proto(proto)
    else:
        return None


@typechecked
def create_stream_source_from_args_proto(
    proto: virtual_data_source__args_pb2.VirtualDataSourceArgs, supplement: DataSourceSpecArgsSupplement
) -> Optional[Union["KinesisSourceSpec", "KafkaSourceSpec", "SparkStreamSourceSpec"]]:
    if proto.HasField("kinesis_ds_config"):
        return KinesisSourceSpec.from_args_proto(proto.kinesis_ds_config, supplement)
    elif proto.HasField("kafka_ds_config"):
        return KafkaSourceSpec.from_args_proto(proto.kafka_ds_config, supplement)
    elif proto.HasField("spark_stream_config"):
        return SparkStreamSourceSpec.from_args_proto(proto.spark_stream_config, supplement)
    else:
        return None


@utils.frozen_strict
class KinesisSourceSpec(StreamSourceSpec):
    post_processor: Callable = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})
    stream_name: str
    region: str
    initial_stream_position: data_source_config_pb2.InitialStreamPosition

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: stream_data_source__data_pb2.StreamDataSource) -> "KinesisSourceSpec":
        post_processor = None
        if proto.HasField("raw_stream_translator"):
            post_processor = function_deserialization.from_proto(proto.raw_stream_translator)

        return cls(
            deduplication_column_names=utils.get_tuple_from_repeated_field(proto.deduplication_column_names),
            post_processor=post_processor,
            options=tuple(StreamOptionSpec(key=option.key, value=option.value) for option in proto.options),
            watermark_delay_threshold=time_utils.proto_to_duration(proto.stream_config.watermark_delay_threshold),
            spark_schema=utils.get_field_or_none(proto, "spark_schema"),
            stream_name=utils.get_field_or_none(proto.kinesis_data_source, "stream_name"),
            region=utils.get_field_or_none(proto.kinesis_data_source, "region"),
            initial_stream_position=proto.stream_config.initial_stream_position,
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: data_source__args_pb2.KinesisDataSourceArgs, supplement: DataSourceSpecArgsSupplement
    ) -> "KinesisSourceSpec":
        return cls(
            deduplication_column_names=utils.get_tuple_from_repeated_field(proto.common_args.deduplication_columns),
            post_processor=supplement.stream_post_processor,
            options=tuple(StreamOptionSpec(key=option.key, value=option.value) for option in proto.options),
            watermark_delay_threshold=time_utils.proto_to_duration(proto.common_args.watermark_delay_threshold),
            spark_schema=supplement.stream_schema,
            stream_name=utils.get_field_or_none(proto, "stream_name"),
            region=utils.get_field_or_none(proto, "region"),
            initial_stream_position=proto.initial_stream_position,
        )


@utils.frozen_strict
class KafkaSourceSpec(StreamSourceSpec):
    post_processor: Callable = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})
    bootstrap_servers: str
    topics: str
    ssl_keystore_location: Optional[str]
    ssl_keystore_password_secret_id: Optional[str]
    ssl_truststore_location: Optional[str]
    ssl_truststore_password_secret_id: Optional[str]
    security_protocol: Optional[str]

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: stream_data_source__data_pb2.StreamDataSource) -> "KafkaSourceSpec":
        post_processor = None
        if proto.HasField("raw_stream_translator"):
            post_processor = function_deserialization.from_proto(proto.raw_stream_translator)

        return cls(
            deduplication_column_names=utils.get_tuple_from_repeated_field(proto.deduplication_column_names),
            post_processor=post_processor,
            options=tuple(StreamOptionSpec(key=option.key, value=option.value) for option in proto.options),
            watermark_delay_threshold=time_utils.proto_to_duration(proto.stream_config.watermark_delay_threshold),
            spark_schema=utils.get_field_or_none(proto, "spark_schema"),
            bootstrap_servers=utils.get_field_or_none(proto.kafka_data_source, "bootstrap_servers"),
            topics=utils.get_field_or_none(proto.kafka_data_source, "topics"),
            ssl_keystore_location=utils.get_field_or_none(proto.kafka_data_source, "ssl_keystore_location"),
            ssl_keystore_password_secret_id=utils.get_field_or_none(
                proto.kafka_data_source, "ssl_keystore_password_secret_id"
            ),
            ssl_truststore_location=utils.get_field_or_none(proto.kafka_data_source, "ssl_truststore_location"),
            ssl_truststore_password_secret_id=utils.get_field_or_none(
                proto.kafka_data_source, "ssl_truststore_password_secret_id"
            ),
            security_protocol=utils.get_field_or_none(proto.kafka_data_source, "security_protocol"),
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: data_source__args_pb2.KafkaDataSourceArgs, supplement: DataSourceSpecArgsSupplement
    ) -> "KafkaSourceSpec":
        return cls(
            deduplication_column_names=utils.get_tuple_from_repeated_field(proto.common_args.deduplication_columns),
            post_processor=supplement.stream_post_processor,
            options=tuple(StreamOptionSpec(key=option.key, value=option.value) for option in proto.options),
            watermark_delay_threshold=time_utils.proto_to_duration(proto.common_args.watermark_delay_threshold),
            spark_schema=supplement.stream_schema,
            bootstrap_servers=utils.get_field_or_none(proto, "kafka_bootstrap_servers"),
            topics=utils.get_field_or_none(proto, "topics"),
            ssl_keystore_location=utils.get_field_or_none(proto, "ssl_keystore_location"),
            ssl_keystore_password_secret_id=utils.get_field_or_none(proto, "ssl_keystore_password_secret_id"),
            ssl_truststore_location=utils.get_field_or_none(proto, "ssl_truststore_location"),
            ssl_truststore_password_secret_id=utils.get_field_or_none(proto, "ssl_truststore_password_secret_id"),
            security_protocol=utils.get_field_or_none(proto, "security_protocol"),
        )


@utils.frozen_strict
class SparkStreamSourceSpec(StreamSourceSpec):
    function: Callable = attrs.field(metadata={utils.LOCAL_REMOTE_DIVERGENCE_ALLOWED: True})

    @classmethod
    @typechecked
    def from_data_proto(cls, proto: stream_data_source__data_pb2.StreamDataSource) -> "SparkStreamSourceSpec":
        function = None
        if proto.spark_data_source_function.HasField("function"):
            function = function_deserialization.from_proto(proto.spark_data_source_function.function)

        return cls(
            deduplication_column_names=utils.get_tuple_from_repeated_field(proto.deduplication_column_names),
            options=tuple(StreamOptionSpec(key=option.key, value=option.value) for option in proto.options),
            watermark_delay_threshold=time_utils.proto_to_duration(proto.stream_config.watermark_delay_threshold),
            spark_schema=utils.get_field_or_none(proto, "spark_schema"),
            function=function,
        )

    @classmethod
    @typechecked
    def from_args_proto(
        cls, proto: data_source__args_pb2.SparkStreamConfigArgs, supplement: DataSourceSpecArgsSupplement
    ) -> "SparkStreamSourceSpec":
        return cls(
            deduplication_column_names=tuple(),
            options=tuple(),
            watermark_delay_threshold=pendulum.Duration(),
            spark_schema=supplement.stream_schema,
            function=supplement.stream_data_source_function,
        )
