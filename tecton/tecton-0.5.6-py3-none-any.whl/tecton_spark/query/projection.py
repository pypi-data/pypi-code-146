import pyspark
from pyspark.sql import functions
from pyspark.sql.functions import expr

from tecton_core.query.nodes import AddDurationNode
from tecton_core.query.nodes import ConvertEpochToTimestamp
from tecton_core.query.nodes import EffectiveTimestampNode
from tecton_core.query.nodes import RenameColsNode
from tecton_core.query.nodes import SetAnchorTimeNode
from tecton_spark.partial_aggregations import TEMPORAL_ANCHOR_COLUMN_NAME
from tecton_spark.query import translate
from tecton_spark.query.node import SparkExecNode
from tecton_spark.time_utils import convert_epoch_to_timestamp_column
from tecton_spark.time_utils import convert_timestamp_to_epoch


class SetAnchorTimeSparkNode(SparkExecNode):
    def __init__(self, node: SetAnchorTimeNode):
        # Anchor time for retrieval must be offset by data delay
        self.input_node = translate.spark_convert(node.input_node)
        self.offline = node.offline
        self.feature_store_format_version = node.feature_store_format_version
        self.batch_schedule_in_feature_store_specific_version_units = (
            node.batch_schedule_in_feature_store_specific_version_units
        )
        self.tile_version_in_feature_store_specific_version_units = (
            node.tile_version_in_feature_store_specific_version_units
        )
        self.timestamp_field = node.timestamp_field
        self.for_retrieval = node.for_retrieval
        self.is_stream = node.is_stream
        self.data_delay_seconds = node.data_delay_seconds

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        if self.for_retrieval:
            anchor_time_val = convert_timestamp_to_epoch(
                functions.col(self.timestamp_field) - expr(f"interval {self.data_delay_seconds} seconds"),
                self.feature_store_format_version,
            )
            # tile_version_in_feature_store_specific_version_units will be 0 for continuous
            if self.tile_version_in_feature_store_specific_version_units == 0:
                df = input_df.withColumn(TEMPORAL_ANCHOR_COLUMN_NAME, anchor_time_val)
            else:
                # For stream, we use the tile interval for bucketing since the data is available as soon as
                # the aggregation interval ends.
                # For BAFV, we use the batch schedule to get the last tile written.
                if self.is_stream:
                    df = input_df.withColumn(
                        TEMPORAL_ANCHOR_COLUMN_NAME,
                        anchor_time_val
                        - anchor_time_val % self.tile_version_in_feature_store_specific_version_units
                        - self.tile_version_in_feature_store_specific_version_units,
                    )
                else:
                    df = input_df.withColumn(
                        TEMPORAL_ANCHOR_COLUMN_NAME,
                        anchor_time_val
                        - anchor_time_val % self.batch_schedule_in_feature_store_specific_version_units
                        - self.tile_version_in_feature_store_specific_version_units,
                    )
        else:
            anchor_time_val = convert_timestamp_to_epoch(
                functions.col(self.timestamp_field), self.feature_store_format_version
            )
            df = input_df.withColumn(
                TEMPORAL_ANCHOR_COLUMN_NAME,
                anchor_time_val - anchor_time_val % self.batch_schedule_in_feature_store_specific_version_units,
            )
        if not self.offline:
            MATERIALIZED_RAW_DATA_END_TIME = "_materialized_raw_data_end_time"
            df = df.withColumn(
                MATERIALIZED_RAW_DATA_END_TIME,
                functions.col(TEMPORAL_ANCHOR_COLUMN_NAME)
                + self.batch_schedule_in_feature_store_specific_version_units,
            ).drop(TEMPORAL_ANCHOR_COLUMN_NAME)
        return df


class RenameColsSparkNode(SparkExecNode):
    def __init__(self, node: RenameColsNode):
        self.input_node = translate.spark_convert(node.input_node)
        self.mapping = node.mapping

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        for old_name, new_name in self.mapping.items():
            if new_name:
                input_df = input_df.withColumnRenamed(old_name, new_name)
            else:
                input_df = input_df.drop(old_name)
        return input_df


class ConvertEpochToTimestampSparkNode(SparkExecNode):
    def __init__(self, node: ConvertEpochToTimestamp):
        self.input_node = translate.spark_convert(node.input_node)
        self.feature_store_formats = node.feature_store_formats

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        for name, feature_store_format_version in self.feature_store_formats.items():
            input_df = input_df.withColumn(
                name,
                convert_epoch_to_timestamp_column(functions.col(name), feature_store_format_version),
            )
        return input_df


class EffectiveTimestampSparkNode(SparkExecNode):
    def __init__(self, node: EffectiveTimestampNode):
        # Anchor time for retrieval must be offset by data delay
        self.input_node = translate.spark_convert(node.input_node)
        self.timestamp_field = node.timestamp_field
        self.effective_timestamp_name = node.effective_timestamp_name
        self.batch_schedule_seconds = node.batch_schedule_seconds
        self.for_stream = node.for_stream
        self.is_temporal_aggregate = node.is_temporal_aggregate
        self.data_delay_seconds = node.data_delay_seconds

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        # For feature table(batch_schedule = 0) or for stream fv,
        # the effective timestamp is just the timestamp.
        if self.batch_schedule_seconds == 0 or self.for_stream:
            effective_timestamp = functions.col(self.timestamp_field)
        else:
            slide_str = f"{self.batch_schedule_seconds} seconds"
            timestamp_col = functions.col(self.timestamp_field)
            # Timestamp of temporal aggregate is end of the anchor time window. Subtract 1 micro
            # to get the correct bucket for batch schedule.
            if self.is_temporal_aggregate:
                timestamp_col -= expr(f"interval 1 microseconds")
            window_spec = functions.window(timestamp_col, slide_str, slide_str)
            effective_timestamp = window_spec.end + expr(f"interval {self.data_delay_seconds} seconds")

        df = input_df.withColumn(self.effective_timestamp_name, effective_timestamp)
        return df


class AddDurationSparkNode(SparkExecNode):
    def __init__(self, node: AddDurationNode):
        self.input_node = translate.spark_convert(node.input_node)
        self.timestamp_field = node.timestamp_field
        self.duration = node.duration
        self.new_column_name = node.new_column_name

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)

        return input_df.withColumn(
            self.new_column_name,
            functions.col(self.timestamp_field) + expr(f"interval {self.duration.total_seconds()} seconds"),
        )
