import datetime
import functools
import inspect
from datetime import timedelta
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from pyspark.sql import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
from typeguard import typechecked

from tecton._internals.fco import Fco
from tecton._internals.repo import function_serialization
from tecton._internals.type_utils import to_tecton_schema
from tecton.declarative.base import BaseBatchConfig
from tecton.declarative.base import BaseDataSource
from tecton.declarative.base import BaseStreamConfig
from tecton.declarative.basic_info import prepare_basic_info
from tecton.declarative.datetime_partition_column import DatetimePartitionColumn
from tecton.types import Field
from tecton_core.feature_definition_wrapper import FrameworkVersion
from tecton_core.filter_context import FilterContext
from tecton_core.id_helper import IdHelper
from tecton_proto.args import data_source_pb2
from tecton_proto.args import virtual_data_source_pb2
from tecton_proto.args.basic_info_pb2 import BasicInfo
from tecton_proto.args.data_source_pb2 import FileDataSourceArgs
from tecton_proto.args.virtual_data_source_pb2 import VirtualDataSourceArgs
from tecton_proto.common.data_source_type_pb2 import DataSourceType
from tecton_proto.common.id_pb2 import Id
from tecton_proto.common.schema_container_pb2 import SchemaContainer
from tecton_spark import data_source_helper
from tecton_spark.spark_schema_wrapper import SparkSchemaWrapper


class RequestSource:
    """
    Declare a ``RequestSource``, for using request-time data in an ``OnDemandFeatureView``.
    """

    def __init__(
        self,
        schema: List[Field],
    ):
        """
        Creates a new RequestSource

        :param schema: Schema for the RequestSource inputs.

        Example of a RequestSource declaration:

        .. code-block:: python

            from tecton import RequestSource
            from tecton.types import Field, Float64

            schema = [Field('amount', Float64)]
            transaction_request = RequestSource(schema=schema)
        """
        self._schema = schema
        self.id = IdHelper.from_string(IdHelper.generate_string_id())

    @property
    def schema(self):
        return self._schema


class FileConfig(BaseBatchConfig):
    """
    Configuration used to reference a file or directory (S3, etc.)

    The FileConfig class is used to create a reference to a file or directory of files in S3,
    HDFS, or DBFS.

    The schema of the data source is inferred from the underlying file(s). It can also be modified using the
    ``post_processor`` parameter.

    This class is used as an input to a :class:`BatchSource`'s parameter ``batch_config``. This class is not
    a Tecton Object: it is a grouping of parameters. Declaring this class alone will not register a data source.
    Instead, declare a part of ``BatchSource`` that takes this configuration class instance as a parameter.
    """

    def __init__(
        self,
        uri: str,
        file_format: str,
        convert_to_glue_format=False,
        timestamp_field: Optional[str] = None,
        timestamp_format: Optional[str] = None,
        post_processor: Optional[Callable] = None,
        schema_uri: Optional[str] = None,
        schema_override: Optional[StructType] = None,
        data_delay: timedelta = timedelta(seconds=0),
    ):
        """
        Instantiates a new FileConfig.

        :param uri: S3 or HDFS path to file(s).
        :param file_format: File format. "json", "parquet", or "csv"
        :param convert_to_glue_format: Converts all schema column names to lowercase.
        :param timestamp_field: The timestamp column in this data source that should be used by `FilteredSource`
                                to filter data from this source, before any feature view transformations are applied.
                                Only required if this source is used with `FilteredSource`.
        :param timestamp_format: Format of string-encoded timestamp column (e.g. "yyyy-MM-dd'T'hh:mm:ss.SSS'Z'").
                                 If the timestamp string cannot be parsed with this format, Tecton will fallback and attempt to
                                 use the default timestamp parser.
        :param post_processor: Python user defined function f(DataFrame) -> DataFrame that takes in raw
                                     Pyspark data source DataFrame and translates it to the DataFrame to be
                                     consumed by the Feature View.
        :param schema_uri: A file or subpath of "uri" that can be used for fast schema inference.
                           This is useful for speeding up plan computation for highly partitioned data sources containing many files.
        :param schema_override: A pyspark.sql.types.StructType object that will be used as the schema when
                                reading from the file. If omitted, the schema will be inferred automatically.
        :param data_delay: By default, incremental materialization jobs run immediately at the end of the
                                batch schedule period. This parameter configures how long they wait after the end
                                of the period before starting, typically to ensure that all data has landed.
                                For example, if a feature view has a `batch_schedule` of 1 day and one of
                                the data source inputs has `data_delay=timedelta(hours=1)` set, then
                                incremental materialization jobs will run at `01:00` UTC.
        :return: A FileConfig class instance.

        Example of a FileConfig declaration:

        .. code-block:: python

            from tecton import FileConfig, BatchSource

            def convert_temperature(df):
                from pyspark.sql.functions import udf,col
                from pyspark.sql.types import DoubleType

                # Convert the incoming PySpark DataFrame temperature Celsius to Fahrenheit
                udf_convert = udf(lambda x: x * 1.8 + 32.0, DoubleType())
                converted_df = df.withColumn("Fahrenheit", udf_convert(col("Temperature"))).drop("Temperature")
                return converted_df

            # declare a FileConfig, which can be used as a parameter to a `BatchSource`
            ad_impressions_file_ds = FileConfig(uri="s3://tecton.ai.public/data/ad_impressions_sample.parquet",
                                                file_format="parquet",
                                                timestamp_field="timestamp",
                                                post_processor=convert_temperature)

            # This FileConfig can then be included as an parameter a BatchSource declaration.
            # For example,
            ad_impressions_batch = BatchSource(name="ad_impressions_batch",
                                               batch_config=ad_impressions_file_ds)

        """
        self._args = FileDataSourceArgs()
        self._args.uri = uri
        self._args.file_format = file_format
        self._args.convert_to_glue_format = convert_to_glue_format
        if schema_uri is not None:
            self._args.schema_uri = schema_uri
        if post_processor is not None:
            self._args.common_args.post_processor.CopyFrom(function_serialization.to_proto(post_processor))
        if timestamp_field:
            self._args.common_args.timestamp_field = timestamp_field
        if timestamp_format:
            self._args.timestamp_format = timestamp_format
        if schema_override:
            self._args.schema_override.CopyFrom(SparkSchemaWrapper(schema_override).to_proto())

        self._args.common_args.data_delay.FromTimedelta(data_delay)
        self._data_delay = data_delay
        self.post_processor = post_processor

    @property
    def data_delay(self) -> timedelta:
        return self._data_delay

    def _merge_batch_args(self, data_source_args: VirtualDataSourceArgs):
        data_source_args.file_ds_config.CopyFrom(self._args)


class KafkaConfig(BaseStreamConfig):
    """
    Configuration used to reference a Kafka stream.

    The KafkaConfig class is used to create a reference to a Kafka stream.

    This class used as an input to a :class:`StreamSource`'s parameter ``stream_config``. This class is not
    a Tecton Object: it is a grouping of parameters. Declaring this class alone will not register a data source.
    Instead, declare as part of ``StreamSource`` that takes this configuration class instance as a parameter.

    """

    def __init__(
        self,
        kafka_bootstrap_servers: str,
        topics: str,
        post_processor,
        timestamp_field: str,
        watermark_delay_threshold: datetime.timedelta = datetime.timedelta(hours=24),
        options: Optional[Dict[str, str]] = None,
        ssl_keystore_location: Optional[str] = None,
        ssl_keystore_password_secret_id: Optional[str] = None,
        ssl_truststore_location: Optional[str] = None,
        ssl_truststore_password_secret_id: Optional[str] = None,
        security_protocol: Optional[str] = None,
        deduplication_columns: Optional[List[str]] = None,
    ):
        """
        Instantiates a new KafkaConfig.

        :param kafka_bootstrap_servers: A comma-separated list of the Kafka bootstrap server addresses. Passed directly
                                        to the Spark ``kafka.bootstrap.servers`` option.
        :param topics: A comma-separated list of Kafka topics to subscribe to. Passed directly to the Spark ``subscribe``
                       option.
        :param post_processor: Python user defined function f(DataFrame) -> DataFrame that takes in raw
                                      Pyspark data source DataFrame and translates it to the DataFrame to be
                                      consumed by the Feature View. See an example of
                                      post_processor in the `User Guide`_.
        :param timestamp_field: Name of the column containing timestamp for watermarking.
        :param watermark_delay_threshold: (Default: 24h) Watermark time interval, e.g: timedelta(hours=36), used by Spark Structured Streaming to account for late-arriving data. See: `Productionizing a Stream`_.
        :param options: A map of additional Spark readStream options
        :param ssl_keystore_location: An DBFS (Databricks only) or S3 URI that points to the keystore file that should be used for SSL brokers. Note for S3 URIs, this must be configured by your Tecton representative.
            Example: ``s3://tecton-<deployment name>/kafka-credentials/kafka_client_keystore.jks``
            Example: ``dbfs:/kafka-credentials/kafka_client_keystore.jks``
        :param ssl_keystore_password_secret_id: The config key for the password for the Keystore.
            Should start with ``SECRET_``, example: ``SECRET_KAFKA_PRODUCTION``.
        :param ssl_truststore_location: An DBFS (Databricks only) or S3 URI that points to the truststore file that should be used for SSL brokers. Note for S3 URIs, this must be configured by your Tecton representative. If not provided, the default truststore for your compute provider will be used. Note that this is required for AWS-signed keystores on Databricks.
            Example: ``s3://tecton-<deployment name>/kafka-credentials/kafka_client_truststore.jks``
            Example: ``dbfs:/kafka-credentials/kafka_client_truststore.jks``
        :param ssl_truststore_password_secret_id (Optional): The config key for the password for the Truststore.
            Should start with ``SECRET_``, example: ``SECRET_KAFKA_PRODUCTION``.
        :param security_protocol: Security protocol passed to kafka.security.protocol. See Kafka documentation for valid values.
        :param deduplication_columns: Columns in the stream data that uniquely identify data records.
                                        Used for de-duplicating. Spark will drop rows if there are duplicates in the deduplication_columns, but only within the watermark delay window.

        :return: A KafkaConfig class instance.

        .. _User Guide: https://docs.tecton.ai/0.5/examples/create-a-streaming-data-source.html#write-the-stream-message-post-processor-function
        .. _Productionizing a Stream: https://docs.tecton.ai/0.5/overviews/framework/feature_views/stream/index.html#productionizing-a-stream

        Example of a KafkaConfig declaration:

        .. code-block:: python

            import datetime
            import pyspark
            from tecton import KafkaConfig


            def raw_data_deserialization(df:pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
                from pyspark.sql.functions import from_json, col
                from pyspark.sql.types import StringType, TimestampType

                PAYLOAD_SCHEMA = (
                  StructType()
                        .add("accountId", StringType(), False)
                        .add("transaction_id", StringType(), False)
                )

                EVENT_ENVELOPE_SCHEMA = (
                  StructType()
                        .add("timestamp", TimestampType(), False)
                        .add("payload", PAYLOAD_SCHEMA, False)
                )

                value = col("value").cast("string")
                df = df.withColumn("event", from_json(value, EVENT_ENVELOPE_SCHEMA))
                df = df.withColumn("accountId", col("event.payload.accountId"))
                df = df.withColumn("transaction_id", col("event.payload.transaction_id"))
                df = df.withColumn("timestamp", col("event.timestamp"))

                return df

            # Declare Kafka Config instance object that can be used as an argument in StreamSource
            click_stream_kafka_ds = KafkaConfig(
                                        kafka_bootstrap_servers="127.0.0.1:12345",
                                        topics="click-events-json",
                                        timestamp_field="click_event_timestamp",
                                        post_processor=raw_data_deserialization)
        """
        self._args = args = data_source_pb2.KafkaDataSourceArgs()
        args.kafka_bootstrap_servers = kafka_bootstrap_servers
        args.topics = topics
        args.common_args.post_processor.CopyFrom(function_serialization.to_proto(post_processor))
        args.common_args.timestamp_field = timestamp_field
        if watermark_delay_threshold:
            args.common_args.watermark_delay_threshold.FromTimedelta(watermark_delay_threshold)
        for key in sorted((options or {}).keys()):
            option = data_source_pb2.Option()
            option.key = key
            option.value = options[key]
            args.options.append(option)
        if ssl_keystore_location:
            args.ssl_keystore_location = ssl_keystore_location
        if ssl_keystore_password_secret_id:
            args.ssl_keystore_password_secret_id = ssl_keystore_password_secret_id
        if ssl_truststore_location:
            args.ssl_truststore_location = ssl_truststore_location
        if ssl_truststore_password_secret_id:
            args.ssl_truststore_password_secret_id = ssl_truststore_password_secret_id
        if security_protocol:
            args.security_protocol = security_protocol
        if deduplication_columns:
            for column_name in deduplication_columns:
                args.common_args.deduplication_columns.append(column_name)

        self.post_processor = post_processor

    def _merge_stream_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.kafka_ds_config.CopyFrom(self._args)


class KinesisConfig(BaseStreamConfig):
    """
    Configuration used to reference a Kinesis stream.

    The KinesisConfig class is used to create a reference to an AWS Kinesis stream.

    This class used as an input to a :class:`StreamSource`'s parameter ``stream_config``. This class is not
    a Tecton Object: it is a grouping of parameters. Declaring this class alone will not register a data source.
    Instead, declare as part of ``StreamSource`` that takes this configuration class instance as a parameter.
    """

    def __init__(
        self,
        stream_name: str,
        region: str,
        post_processor,
        timestamp_field: str,
        initial_stream_position: str,
        watermark_delay_threshold: datetime.timedelta = datetime.timedelta(hours=24),
        deduplication_columns: Optional[List[str]] = None,
        options: Optional[Dict[str, str]] = None,
    ):
        """
        Instantiates a new KinesisConfig.

        :param stream_name: Name of the Kinesis stream.
        :param region: AWS region of the stream, e.g: "us-west-2".
        :param post_processor: Python user defined function f(DataFrame) -> DataFrame that takes in raw
                                      Pyspark data source DataFrame and translates it to the DataFrame to be
                                      consumed by the Feature View. See an example of
                                      post_processor in the `User Guide`_.
        :param timestamp_field: Name of the column containing timestamp for watermarking.
        :param initial_stream_position: Initial position in stream, e.g: "latest" or "trim_horizon".
                                                More information available in `Spark Kinesis Documentation`_.
        :param watermark_delay_threshold: (Default: 24h) Watermark time interval, e.g: timedelta(hours=36), used by Spark Structured Streaming to account for late-arriving data. See: `Productionizing a Stream`_.
        :param deduplication_columns: Columns in the stream data that uniquely identify data records.
                                        Used for de-duplicating.
        :param options: A map of additional Spark readStream options

        :return: A KinesisConfig class instance.

        .. _User Guide: https://docs.tecton.ai/0.5/examples/create-a-streaming-data-source.html#write-the-stream-message-post-processor-function
        .. _Productionizing a Stream: https://docs.tecton.ai/0.5/overviews/framework/feature_views/stream/index.html#productionizing-a-stream
        .. _Spark Kinesis Documentation: https://spark.apache.org/docs/latest/streaming-kinesis-integration.html

        Example of a KinesisConfig declaration:

        .. code-block:: python

            import pyspark
            from tecton import KinesisConfig


            # Define our deserialization raw stream translator
            def raw_data_deserialization(df:pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
                from pyspark.sql.functions import col, from_json, from_utc_timestamp
                from pyspark.sql.types import StructType, StringType

                payload_schema = (
                  StructType()
                        .add('amount', StringType(), False)
                        .add('isFraud', StringType(), False)
                        .add('timestamp', StringType(), False)
                )

                return (
                    df.selectExpr('cast (data as STRING) jsonData')
                    .select(from_json('jsonData', payload_schema).alias('payload'))
                    .select(
                        col('payload.amount').cast('long').alias('amount'),
                        col('payload.isFraud').cast('long').alias('isFraud'),
                        from_utc_timestamp('payload.timestamp', 'UTC').alias('timestamp')
                    )
                )
            # Declare KinesisConfig instance object that can be used as argument in `StreamSource`
            stream_config = KinesisConfig(
                                    stream_name='transaction_events',
                                    region='us-west-2',
                                    initial_stream_position='latest',
                                    timestamp_field='timestamp',
                                    post_processor=raw_data_deserialization,
                                    options={'roleArn': 'arn:aws:iam::472542229217:role/demo-cross-account-kinesis-ro'}
            )
        """

        args = data_source_pb2.KinesisDataSourceArgs()
        args.stream_name = stream_name
        args.region = region
        args.common_args.post_processor.CopyFrom(function_serialization.to_proto(post_processor))
        args.common_args.timestamp_field = timestamp_field
        if initial_stream_position:
            args.initial_stream_position = data_source_helper.INITIAL_STREAM_POSITION_STR_TO_ENUM[
                initial_stream_position
            ]
        if watermark_delay_threshold:
            args.common_args.watermark_delay_threshold.FromTimedelta(watermark_delay_threshold)
        if deduplication_columns:
            for column_name in deduplication_columns:
                args.common_args.deduplication_columns.append(column_name)
        options_ = options or {}
        for key in sorted(options_.keys()):
            option = data_source_pb2.Option()
            option.key = key
            option.value = options_[key]
            args.options.append(option)

        self._args = args
        self.post_processor = post_processor

    def _merge_stream_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.kinesis_ds_config.CopyFrom(self._args)


class HiveConfig(BaseBatchConfig):
    """
    Configuration used to reference a Hive table.

    The HiveConfig class is used to create a reference to a Hive Table.

    This class used as an input to a :class:`BatchSource`'s parameter ``batch_config``. This class is not
    a Tecton Object: it is a grouping of parameters. Declaring this class alone will not register a data source.
    Instead, declare as part of ``BatchSource`` that takes this configuration class instance as a parameter.
    """

    def __init__(
        self,
        table: str,
        database: str,
        timestamp_field: Optional[str] = None,
        timestamp_format: Optional[str] = None,
        datetime_partition_columns: Optional[List[DatetimePartitionColumn]] = None,
        post_processor: Optional[Callable] = None,
        data_delay: timedelta = timedelta(seconds=0),
    ):
        """
        Instantiates a new HiveConfig.

        :param table: A table registered in Hive MetaStore.
        :param database: A database registered in Hive MetaStore.
        :param timestamp_field: The timestamp column in this data source that should be used by `FilteredSource`
                                    to filter data from this source, before any feature view transformations are applied.
                                    Only required if this source is used with `FilteredSource`.
        :param timestamp_format: Format of string-encoded timestamp column (e.g. "yyyy-MM-dd'T'hh:mm:ss.SSS'Z'").
                                 If the timestamp string cannot be parsed with this format, Tecton will fallback and attempt to
                                 use the default timestamp parser.
        :param datetime_partition_columns: List of DatetimePartitionColumn the raw data is partitioned by, otherwise None.
        :param post_processor: Python user defined function f(DataFrame) -> DataFrame that takes in raw
                                     PySpark data source DataFrame and translates it to the DataFrame to be
                                     consumed by the Feature View.
        :param data_delay: By default, incremental materialization jobs run immediately at the end of the
                                    batch schedule period. This parameter configures how long they wait after the end
                                    of the period before starting, typically to ensure that all data has landed.
                                    For example, if a feature view has a `batch_schedule` of 1 day and one of
                                    the data source inputs has `data_delay=timedelta(hours=1)` set, then
                                    incremental materialization jobs will run at `01:00` UTC.

        :return: A HiveConfig class instance.


        Example of a HiveConfig declaration:

        .. code-block:: python

            from tecton import HiveConfig
            import pyspark

            def convert_temperature(df: pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
                from pyspark.sql.functions import udf,col
                from pyspark.sql.types import DoubleType

                # Convert the incoming PySpark DataFrame temperature Celsius to Fahrenheit
                udf_convert = udf(lambda x: x * 1.8 + 32.0, DoubleType())
                converted_df = df.withColumn("Fahrenheit", udf_convert(col("Temperature"))).drop("Temperature")
                return converted_df

            # declare a HiveConfig instance, which can be used as a parameter to a BatchSource
            batch_config=HiveConfig(database='global_temperatures',
                                        table='us_cities',
                                        timestamp_field='timestamp',
                                        post_processor=convert_temperature)

        """
        self._args = data_source_pb2.HiveDataSourceArgs()
        self._args.table = table
        self._args.database = database
        if timestamp_field:
            self._args.common_args.timestamp_field = timestamp_field
        if timestamp_format:
            self._args.timestamp_format = timestamp_format

        if datetime_partition_columns:
            for column in datetime_partition_columns:
                column_args = data_source_pb2.DatetimePartitionColumnArgs()
                column_args.column_name = column.column_name
                column_args.datepart = column.datepart
                column_args.zero_padded = column.zero_padded
                if column.format_string:
                    column_args.format_string = column.format_string
                self._args.datetime_partition_columns.append(column_args)
        if post_processor is not None:
            self._args.common_args.post_processor.CopyFrom(function_serialization.to_proto(post_processor))

        self._args.common_args.data_delay.FromTimedelta(data_delay)
        self._data_delay = data_delay
        self.post_processor = post_processor

    @property
    def data_delay(self):
        return self._data_delay

    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.hive_ds_config.CopyFrom(self._args)


class SnowflakeConfig(BaseBatchConfig):
    """
    Configuration used to reference a Snowflake table or query.

    The SnowflakeConfig class is used to create a reference to a Snowflake table. You can also create a
    reference to a query on one or more tables, which will be registered in Tecton in a similar way as a view
    is registered in other data systems.

    This class used as an input to a :class:`BatchSource`'s parameter ``batch_config``. This class is not
    a Tecton Object: it is a grouping of parameters. Declaring this class alone will not register a data source.
    Instead, declare as part of ``BatchSource`` that takes this configuration class instance as a parameter.
    """

    def __init__(
        self,
        *,
        database: str,
        schema: str,
        warehouse: Optional[str] = None,
        url: Optional[str] = None,
        role: Optional[str] = None,
        table: Optional[str] = None,
        query: Optional[str] = None,
        timestamp_field: Optional[str] = None,
        post_processor: Optional[Callable] = None,
        data_delay: timedelta = timedelta(seconds=0),
    ):
        """
        Instantiates a new SnowflakeConfig. One of table and query should be specified when creating this file.

        :param database: The Snowflake database for this Data source.
        :param schema: The Snowflake schema for this Data source.
        :param warehouse: The Snowflake warehouse for this Data source.
        :param url: The connection URL to Snowflake, which contains account information
                         (e.g. https://xy12345.eu-west-1.snowflakecomputing.com).
        :param role: The Snowflake role that should be used for this Data source.

        :param table: The table for this Data source. Only one of `table` and `query` must be specified.
        :param query: The query for this Data source. Only one of `table` and `query` must be specified.
                        This parameter is not supported in Tecton on Snowflake.
        :param timestamp_field: The timestamp column in this data source that should be used by `FilteredSource`
                                    to filter data from this source, before any feature view transformations are applied.
                                    Only required if this source is used with `FilteredSource`.
        :param post_processor: Python user defined function f(DataFrame) -> DataFrame that takes in raw
                                     PySpark data source DataFrame and translates it to the DataFrame to be
                                     consumed by the Feature View. This parameter is not supported in Tecton on Snowflake.
        :param data_delay: By default, incremental materialization jobs run immediately at the end of the
                                    batch schedule period. This parameter configures how long they wait after the end
                                    of the period before starting, typically to ensure that all data has landed.
                                    For example, if a feature view has a `batch_schedule` of 1 day and one of
                                    the data source inputs has `data_delay=timedelta(hours=1)` set, then
                                    incremental materialization jobs will run at `01:00` UTC.

        :return: A SnowflakeConfig class instance.


        Example of a SnowflakeConfig declaration:

        .. code-block:: python

            from tecton import SnowflakeConfig, BatchSource

            # Declare SnowflakeConfig instance object that can be used as an argument in BatchSource
            snowflake_ds_config = SnowflakeConfig(
                                              url="https://<your-cluster>.eu-west-1.snowflakecomputing.com/",
                                              database="CLICK_STREAM_DB",
                                              schema="CLICK_STREAM_SCHEMA",
                                              warehouse="COMPUTE_WH",
                                              table="CLICK_STREAM_FEATURES",
                                              query="SELECT timestamp as ts, created, user_id, clicks, click_rate"
                                                     "FROM CLICK_STREAM_DB.CLICK_STREAM_FEATURES")

            # Use in the BatchSource
            snowflake_ds = BatchSource(name="click_stream_snowflake_ds",
                                           batch_config=snowflake_ds_config)
        """
        self._args = args = data_source_pb2.SnowflakeDataSourceArgs()
        args.database = database
        args.schema = schema
        if url:
            args.url = url
        if warehouse:
            args.warehouse = warehouse

        if role:
            args.role = role

        if table:
            args.table = table
        if query:
            args.query = query

        if post_processor is not None:
            args.common_args.post_processor.CopyFrom(function_serialization.to_proto(post_processor))
        if timestamp_field:
            args.common_args.timestamp_field = timestamp_field

        args.common_args.data_delay.FromTimedelta(data_delay)
        self._data_delay = data_delay
        self.post_processor = post_processor

    @property
    def data_delay(self):
        return self._data_delay

    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.snowflake_ds_config.CopyFrom(self._args)


class RedshiftConfig(BaseBatchConfig):
    """
    Configuration used to reference a Redshift table or query.

    The RedshiftConfig class is used to create a reference to a Redshift table. You can also create a
    reference to a query on one or more tables, which will be registered in Tecton in a similar way as a view
    is registered in other data systems.

    This class used as an input to a :class:`BatchSource`'s parameter ``batch_config``. This class is not
    a Tecton Object: it is a grouping of parameters. Declaring this class alone will not register a data source.
    Instead, declare as part of ``BatchSource`` that takes this configuration class instance as a parameter.
    """

    def __init__(
        self,
        endpoint: str,
        table: Optional[str] = None,
        post_processor: Optional[Callable] = None,
        temp_s3: Optional[str] = None,
        query: Optional[str] = None,
        timestamp_field: Optional[str] = None,
        data_delay: timedelta = timedelta(seconds=0),
    ):
        """
        Instantiates a new RedshiftConfig. One of table and query should be specified when creating this file.

        :param endpoint: The connection endpoint to Redshift
                         (e.g. redshift-cluster-1.cigcwzsdltjs.us-west-2.redshift.amazonaws.com:5439/dev).
        :param table: The Redshift table for this Data source. Only one of table and query should be specified.
        :param post_processor: Python user defined function f(DataFrame) -> DataFrame that takes in raw
                                     PySpark data source DataFrame and translates it to the DataFrame to be
                                     consumed by the Feature View.
        :param temp_s3: [deprecated] An S3 URI destination for intermediate data that is needed for Redshift.
                        (e.g. s3://tecton-ai-test-cluster-redshift-data)
        :param query: A Redshift query for this Data source. Only one of table and query should be specified.
        :param timestamp_field: The timestamp column in this data source that should be used by `FilteredSource`
                                    to filter data from this source, before any feature view transformations are applied.
                                    Only required if this source is used with `FilteredSource`.
        :param data_delay: By default, incremental materialization jobs run immediately at the end of the
                                    batch schedule period. This parameter configures how long they wait after the end
                                    of the period before starting, typically to ensure that all data has landed.
                                    For example, if a feature view has a `batch_schedule` of 1 day and one of
                                    the data source inputs has `data_delay=timedelta(hours=1)` set, then
                                    incremental materialization jobs will run at `01:00` UTC.

        :return: A RedshiftConfig class instance.

        Example of a RedshiftConfig declaration:

        .. code-block:: python

            from tecton import RedshiftConfig

            # Declare RedshiftConfig instance object that can be used as an argument in BatchSource
            redshift_ds_config = RedshiftConfig(endpoint="cluster-1.us-west-2.redshift.amazonaws.com:5439/dev",
                                                  query="SELECT timestamp as ts, created, user_id, ad_id, duration"
                                                        "FROM ad_serving_features")
        """
        self._args = args = data_source_pb2.RedshiftDataSourceArgs()
        args.endpoint = endpoint

        if table and query:
            raise AssertionError(f"Should only specify one of table and query sources for redshift")
        if not table and not query:
            raise AssertionError(f"Missing both table and query sources for redshift, exactly one must be present")

        if table:
            args.table = table
        else:
            args.query = query

        if post_processor is not None:
            args.common_args.post_processor.CopyFrom(function_serialization.to_proto(post_processor))
        if timestamp_field:
            args.common_args.timestamp_field = timestamp_field

        args.common_args.data_delay.FromTimedelta(data_delay)
        self._data_delay = data_delay
        self.post_processor = post_processor

    @property
    def data_delay(self):
        return self._data_delay

    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.redshift_ds_config.CopyFrom(self._args)


class SparkBatchConfig(BaseBatchConfig):
    """
    Configuration used to define a batch source using a Data Source Function.

    The ``SparkBatchConfig`` class is used to configure a batch source using a user defined Data Source Function.

    This class is used as an input to a :class:`BatchSource`'s parameter ``batch_config``. This class is not
    a Tecton Object: it is a grouping of parameters. Declaring this class alone will not register a data source.
    Instead, declare as part of ``BatchSource`` that takes this configuration class instance as a parameter.

    **Do not instantiate this class directly.** Use :class:`tecton.declarative.spark_batch_config` instead.
    """

    def __init__(
        self,
        data_source_function: Union[
            Callable[[SparkSession], DataFrame], Callable[[SparkSession, FilterContext], DataFrame]
        ],
        data_delay: timedelta = timedelta(seconds=0),
        supports_time_filtering: bool = False,
    ):
        """
        Instantiates a new SparkBatchConfig.

        :param data_source_function: User defined Data Source Function that takes in a ``SparkSession`` and an optional
                                    :class:`tecton.FilterContext`, if ``supports_time_filtering=True``. Returns a ``DataFrame``.
        :param data_delay: By default, incremental materialization jobs run immediately at the end of the
                                    batch schedule period. This parameter configures how long they wait after the end
                                    of the period before starting, typically to ensure that all data has landed.
                                    For example, if a feature view has a ``batch_schedule`` of 1 day and one of
                                    the data source inputs has a ``data_delay`` of 1 hour, then
                                    incremental materialization jobs will run at ``01:00`` UTC.
        :param supports_time_filtering: When set to ``True``, the Data Source Function must take the ``filter_context``
                                    parameter and implement time filtering logic.
                                    ``supports_time_filtering`` must be set to `True` if ``<data source>.get_dataframe()`` is called with ``start_time``
                                    or ``end_time``. ``supports_time_filtering`` must also be set to ``True`` if using :class:`tecton.declarative.FilteredSource`
                                    with a Data Source when defining a ``FeatureView``. The ``FeatureView`` will call
                                    the Data Source Function with the :class:`tecton.FilterContext`, which has the ``start_time`` and
                                    ``end_time`` set.

        :return: A SparkBatchConfig class instance.
        """
        params = list(inspect.signature(data_source_function).parameters)
        function_name = data_source_function.__name__
        if supports_time_filtering and params != ["spark", "filter_context"]:
            raise AssertionError(
                f"The Data Source Function {function_name}'s signature needs to be `{function_name}(spark, filter_context)` when supports_time_filtering is True"
            )
        elif not supports_time_filtering and params != ["spark"]:
            raise AssertionError(
                f"The Data Source Function {function_name}'s signature needs to be `{function_name}(spark)` when supports_time_filtering is False"
            )

        self._args = data_source_pb2.SparkBatchConfigArgs()
        self._args.data_source_function.CopyFrom(function_serialization.to_proto(data_source_function))
        self._args.data_delay.FromTimedelta(data_delay)
        self._args.supports_time_filtering = supports_time_filtering
        self._data_delay = data_delay
        self.data_source_function = data_source_function

    @property
    def data_delay(self) -> timedelta:
        return self._data_delay

    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.spark_batch_config.CopyFrom(self._args)

    def __call__(self, *args, **kwargs):
        return self.data_source_function(*args, **kwargs)


@typechecked
def spark_batch_config(
    *, data_delay: Optional[timedelta] = timedelta(seconds=0), supports_time_filtering: Optional[bool] = False
):
    """
    Declare a :class:`tecton.declarative.data_source.SparkBatchConfig` for configuring a batch source with a Data Source Function.
    The function takes in a ``SparkSession`` and an optional :class:`tecton.FilterContext`, if ``supports_time_filtering=True``. Returns a ``DataFrame``.

    :param data_delay: By default, incremental materialization jobs run immediately at the end of the
                                batch schedule period. This parameter configures how long they wait after the end
                                of the period before starting, typically to ensure that all data has landed.
                                For example, if a feature view has a ``batch_schedule`` of 1 day and one of
                                the data source inputs has `data_delay=timedelta(hours=1)` set, then
                                incremental materialization jobs will run at ``01:00`` UTC.
    :param supports_time_filtering: When set to ``True``, the Data Source Function must take the ``filter_context``
                                    parameter and implement time filtering logic.
                                    ``supports_time_filtering`` must be set to `True` if ``<data source>.get_dataframe()`` is called with ``start_time``
                                    or ``end_time``. ``supports_time_filtering`` must also be set to ``True`` if using :class:`tecton.declarative.FilteredSource`
                                    with a Data Source when defining a ``FeatureView``. The ``FeatureView`` will call
                                    the Data Source Function with the :class:`tecton.FilterContext`, which has the ``start_time`` and
                                    ``end_time`` set.

    Example defining a Data Source Function using ``spark_batch_config``:

    .. code-block:: python

        from tecton import spark_batch_config

        @spark_batch_config(supports_time_filtering=True)
        def redshift_data_source_function(spark, filter_context):
            spark_format = "com.databricks.spark.redshift"
            params = {
                "user": "<user name>",
                "password": os.environ["redshift_password"]
            }
            endpoint = "<redshift endpoint>"
            full_connection_string = f"jdbc:redshift://{endpoint};user={params['user']};password={params['password']}"
            df_reader = (
                spark.read.format(spark_format)
                .option("url", full_connection_string)
                .option("forward_spark_s3_credentials", "true")
            )
            df_reader = df_reader.option("dbtable", "your_table_name")
            df = df_reader_load()
            ts_column = "timestamp"
            df = df.withColumn(ts_column, col(ts_column).cast("timestamp"))
            # Handle time filtering
            if filter_context:
                if filter_context.start_time:
                    df = df.where(col(ts_column) >= filter_context.start_time)
                if filter_context.end_time:
                    df = df.where(col(ts_column) < filter_context.end_time)
            return df
    """

    def decorator(data_source_function):
        batch_config = SparkBatchConfig(
            data_source_function=data_source_function,
            data_delay=data_delay,
            supports_time_filtering=supports_time_filtering,
        )
        functools.update_wrapper(wrapper=batch_config, wrapped=data_source_function)
        return batch_config

    return decorator


class SparkStreamConfig(BaseStreamConfig):
    """
    Configuration used to define a stream source using a Data Source Function.

    The ``SparkStreamConfig`` class is used to configure a stream source using a user defined Data Source Function.

    This class is used as an input to a :class:`StreamSource`'s parameter ``stream_config``. This class is not
    a Tecton Object: it is a grouping of parameters. Declaring this class alone will not register a data source.
    Instead, declare as part of ``StreamSource`` that takes this configuration class instance as a parameter.

    **Do not instantiate this class directly.** Use :class:`tecton.declarative.spark_stream_config` instead.
    """

    def __init__(self, data_source_function: Callable[[SparkSession], DataFrame]):
        """
        Instantiates a new SparkBatchConfig.

        :param data_source_function: User-defined Data Source Function that takes in a ``SparkSession`` and returns
                    a streaming ``DataFrame``.

        :return: A SparkStreamConfig class instance.
        """
        params = list(inspect.signature(data_source_function).parameters)
        function_name = data_source_function.__name__
        if params != ["spark"]:
            raise AssertionError(
                f"The Data Source Function {function_name}'s signature needs to be `{function_name}(spark)`"
            )

        self._args = data_source_pb2.SparkStreamConfigArgs()
        self._args.data_source_function.CopyFrom(function_serialization.to_proto(data_source_function))
        self.data_source_function = data_source_function

    def _merge_stream_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        data_source_args.spark_stream_config.CopyFrom(self._args)

    def __call__(self, *args, **kwargs):
        return self.data_source_function(*args, **kwargs)


def spark_stream_config():
    """
    Declare an :class:`tecton.declarative.data_source.SparkStreamConfig` for configuring a stream source with a Data Source Function. The function takes in a ``SparkSession`` returns a streaming ``DataFrame``.

    Example defining a Data Source Function using ``spark_stream_config``:

    .. code-block:: python

        from tecton import spark_stream_config

        def raw_data_deserialization(df):
            from pyspark.sql.functions import col, from_json, from_utc_timestamp, when
            from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType, BooleanType, IntegerType
            payload_schema = StructType([
                StructField("user_id", StringType(), False),
                StructField("transaction_id", StringType(), False),
                StructField("category", StringType(), False),
                StructField("amt", StringType(), False),
                StructField("timestamp", StringType(), False),
            ])
            return (
                df.selectExpr("cast (data as STRING) jsonData")
                .select(from_json("jsonData", payload_schema).alias("payload"))
                .select(
                    col("payload.user_id").alias("user_id"),
                    col("payload.transaction_id").alias("transaction_id"),
                    col("payload.category").alias("category"),
                    col("payload.amt").cast("double").alias("amt"),
                    from_utc_timestamp("payload.timestamp", "UTC").alias("timestamp")
                )
            )

        @spark_stream_config()
        def kinesis_data_source_function(spark):
            options = {
                "streamName": "<stream name>",
                "roleArn": "<role ARN>",
                "region": "<region>",
                "shardFetchInterval": "30s",
                "initialPosition": "latest"
            }
            reader = spark.readStream.format("kinesis").options(**options)
            df = reader.load()
            df = raw_data_deserialization(df)
            watermark = "{} seconds".format(timedelta(hours=24).seconds)
            df = df.withWatermark("timestamp", watermark)
            return df
    """

    def decorator(data_source_function):
        stream_config = SparkStreamConfig(
            data_source_function=data_source_function,
        )
        functools.update_wrapper(wrapper=stream_config, wrapped=data_source_function)
        return stream_config

    return decorator


class BatchSource(BaseDataSource):
    """
    Declare a ``BatchSource``, used to read batch data into Tecton.

    ``BatchFeatureViews`` ingest data from a BatchSource.
    """

    @typechecked
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        owner: Optional[str] = None,
        batch_config: Union[FileConfig, HiveConfig, RedshiftConfig, SnowflakeConfig, SparkBatchConfig],
    ) -> None:
        """
        Creates a new BatchSource

        :param name: An unique name of the DataSource.
        :param description: A human readable description.
        :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
        :param owner: Owner name (typically the email of the primary maintainer).
        :param batch_config: BatchConfig object containing the configuration of the batch data source to be included
            in this DataSource.

        :return: A :class:`BatchSource` class instance.

        Example of a BatchSource declaration:

        .. code-block:: python

            # Declare a BatchSource with HiveConfig instance as its batch_config parameter
            # Refer to Configs API documentation other batch_config types.
            from tecton import HiveConfig, BatchSource

            credit_scores_batch = BatchSource(
                name='credit_scores_batch',
                batch_config=HiveConfig(
                    database='demo_fraud',
                    table='credit_scores',
                    timestamp_field='timestamp'
                ),
                owner='matt@tecton.ai',
                tags={'release': 'production'}
            )
        """
        from tecton.cli.common import get_fco_source_info

        self._source_info = get_fco_source_info()

        basic_info = prepare_basic_info(name=name, description=description, owner=owner, family=None, tags=tags)
        args = prepare_ds_args(
            basic_info=basic_info, batch_config=batch_config, stream_config=None, ds_type=DataSourceType.BATCH
        )

        self._args = args
        self._data_delay = batch_config.data_delay

        Fco._register(self)

    @property
    def _id(self) -> Id:
        return self._args.virtual_data_source_id

    @property
    def name(self) -> str:
        """
        The name of this DataSource.
        """
        return self._args.info.name

    @property
    def data_delay(self) -> timedelta:
        return self._data_delay


class StreamSource(BaseDataSource):
    """
    Declare a ``StreamSource``, used to read streaming data into Tecton.

    ``StreamFeatureViews`` ingest data from StreamSources. A StreamSource contains both a batch config and a stream config.
    """

    @typechecked
    def __init__(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        owner: Optional[str] = None,
        batch_config: Union[FileConfig, HiveConfig, RedshiftConfig, SnowflakeConfig, SparkBatchConfig],
        stream_config: Union[KinesisConfig, KafkaConfig, SparkStreamConfig],
    ) -> None:
        """
        Creates a new StreamSource.

        :param name: An unique name of the DataSource.
        :param description: A human readable description.
        :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
        :param owner: Owner name (typically the email of the primary maintainer).
        :param batch_config: BatchConfig object containing the configuration of the batch data source that is to be included
            in this DataSource.
        :param stream_config: StreamConfig object containing the configuration of the
            stream data source that is to be included in this DataSource.

        :return: A :class:`StreamSource` class instance.

        Example of a StreamSource declaration:

        .. code-block:: python

         import pyspark
            from tecton import KinesisConfig, HiveConfig, StreamSource
            from datetime import timedelta


            # Define our deserialization raw stream translator
            def raw_data_deserialization(df:pyspark.sql.DataFrame) -> pyspark.sql.DataFrame:
                from pyspark.sql.functions import col, from_json, from_utc_timestamp
                from pyspark.sql.types import StructType, StringType

                payload_schema = (
                  StructType()
                        .add('amount', StringType(), False)
                        .add('isFraud', StringType(), False)
                        .add('timestamp', StringType(), False)
                )
                return (
                    df.selectExpr('cast (data as STRING) jsonData')
                    .select(from_json('jsonData', payload_schema).alias('payload'))
                    .select(
                        col('payload.amount').cast('long').alias('amount'),
                        col('payload.isFraud').cast('long').alias('isFraud'),
                        from_utc_timestamp('payload.timestamp', 'UTC').alias('timestamp')
                    )
                )

            # Declare a StreamSource with both a batch_config and a stream_config as parameters
            # See the API documentation for both BatchConfig and StreamConfig
            transactions_stream = StreamSource(
                                    name='transactions_stream',
                                    stream_config=KinesisConfig(
                                        stream_name='transaction_events',
                                        region='us-west-2',
                                        initial_stream_position='latest',
                                        watermark_delay_threshold=timedelta(minutes=30),
                                        timestamp_field='timestamp',
                                        post_processor=raw_data_deserialization,
                                        options={'roleArn': 'arn:aws:iam::472542229217:role/demo-cross-account-kinesis-ro'}
                                    ),
                                    batch_config=HiveConfig(
                                        database='demo_fraud',
                                        table='transactions',
                                        timestamp_field='timestamp',
                                    ),
                                    owner='jules@tecton.ai',
                                    tags={'release': 'staging'}
                                    )
        """
        from tecton.cli.common import get_fco_source_info

        self._source_info = get_fco_source_info()

        basic_info = prepare_basic_info(name=name, description=description, owner=owner, family=None, tags=tags)
        args = prepare_ds_args(
            basic_info=basic_info,
            batch_config=batch_config,
            stream_config=stream_config,
            ds_type=DataSourceType.STREAM_WITH_BATCH,
        )

        self._args = args
        self._data_delay = batch_config.data_delay

        Fco._register(self)

    @property
    def _id(self) -> Id:
        return self._args.virtual_data_source_id

    @property
    def name(self) -> str:
        """
        The name of this DataSource.
        """
        return self._args.info.name

    @property
    def data_delay(self) -> timedelta:
        return self._data_delay


class PushSource(BaseDataSource):
    """
    Declare a ``PushSource``, used to push events in real time into Tecton’s online store via an online Push API.
    ``PushSource`` is currently in private preview, please contact support if you are interested in participating in the preview.

    ``StreamFeatureViews`` ingest data from PushSources. A PushSource also contains a batch config for backfilling.
    """

    @typechecked
    def __init__(
        self,
        *,
        name: str,
        schema: List[Field],
        description: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        owner: Optional[str] = None,
        batch_config: Union[FileConfig, HiveConfig, RedshiftConfig, SparkBatchConfig, SnowflakeConfig],
    ) -> None:
        """
        Creates a new PushSource.

        :param name: An unique name of the DataSource.
        :param schema: A schema for the PushSource
        :param description: A human readable description.
        :param tags: Tags associated with this Tecton Object (key-value pairs of arbitrary metadata).
        :param owner: Owner name (typically the email of the primary maintainer).
        :param batch_config: BatchConfig object containing the configuration of the batch data source that is to be included
            in this DataSource. Must contain at least all of the columns defined in the schema.

        :return: A :class:`PushSource` class instance.

        Example of a PushSource declaration:

        .. code-block:: python

            from tecton import HiveConfig, PushSource, BatchSource
            from tecton.types import Field, Int64, String, Timestamp

            # Declare a schema for the Push Source
            input_schema = [
                Field(name='user_id', dtype=String),
                Field(name='event_timestamp', dtype=String),
                Field(name='clicked', dtype=Int64),
            ]

            # Declare a PushSource with a name, schema and a batch_config parameters
            # See the API documentation for BatchConfig
            click_event_source = PushSource(
                                    name="click_event_source",
                                    schema=input_schema,
                                    batch_config=HiveConfig(
                                        database='demo_ads',
                                        table='impressions_batch',
                                    ),
                                    description="Sample Push Source for click events",
                                    owner="pooja@tecton.ai",
                                    tags={'release': 'staging'}
                                    )
        """

        from tecton.cli.common import get_fco_source_info

        self._source_info = get_fco_source_info()

        basic_info = prepare_basic_info(name=name, description=description, owner=owner, family=None, tags=tags)
        args = prepare_ds_args(
            basic_info=basic_info, batch_config=batch_config, stream_config=None, ds_type=DataSourceType.PUSH
        )
        args.schema.CopyFrom(_prepare_schema(input_schema=schema))
        self._args = args
        self._data_delay = batch_config.data_delay

        Fco._register(self)

    @property
    def _id(self) -> Id:
        return self._args.virtual_data_source_id

    @property
    def name(self) -> str:
        """
        The name of this DataSource.
        """
        return self._args.info.name

    @property
    def data_delay(self) -> timedelta:
        return self._data_delay


def prepare_ds_args(
    *,
    basic_info: BasicInfo,
    batch_config: BaseBatchConfig,
    stream_config: Optional[BaseStreamConfig],
    ds_type: Optional["DataSourceType"],
):
    args = virtual_data_source_pb2.VirtualDataSourceArgs()
    args.virtual_data_source_id.CopyFrom(IdHelper.from_string(IdHelper.generate_string_id()))
    args.info.CopyFrom(basic_info)
    args.version = FrameworkVersion.FWV5.value
    batch_config._merge_batch_args(args)
    if stream_config is not None:
        stream_config._merge_stream_args(args)
    if ds_type:
        args.type = ds_type
    return args


def _prepare_schema(input_schema: List[Field]) -> SchemaContainer:
    schema_container = SchemaContainer()
    schema_container.tecton_schema.CopyFrom(to_tecton_schema(input_schema))
    return schema_container
