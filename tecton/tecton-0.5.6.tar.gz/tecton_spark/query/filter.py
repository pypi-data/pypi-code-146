from typing import Optional

import pendulum
import pyspark
from pyspark.sql import DataFrame
from pyspark.sql import functions
from pyspark.sql import SparkSession

import tecton_core
from tecton_core import conf
from tecton_core.query.nodes import CustomFilterNode
from tecton_core.query.nodes import EntityFilterNode
from tecton_core.query.nodes import FeatureTimeFilterNode
from tecton_core.query.nodes import RespectFSTNode
from tecton_core.query.nodes import RespectTTLNode
from tecton_core.query.nodes import StreamWatermarkNode
from tecton_core.query.nodes import TimeFilterNode
from tecton_proto.data.feature_view_pb2 import MaterializationTimeRangePolicy
from tecton_spark.query import translate
from tecton_spark.query.node import SparkExecNode

TECTON_FEATURE_TIMESTAMP_VALIDATOR = "_tecton_feature_timestamp_validator"
SKIP_FEATURE_TIMESTAMP_VALIDATION_ENV = "SKIP_FEATURE_TIMESTAMP_VALIDATION"
TIMESTAMP_VALIDATOR_UDF_REGISTERED = False


logger = tecton_core.logger.get_logger("QueryTree")


def _apply_or_check_feature_data_time_limits(
    spark: SparkSession,
    feature_df: DataFrame,
    time_range_policy: MaterializationTimeRangePolicy,
    timestamp_key: str,
    feature_data_time_limits: Optional[pendulum.Period],
) -> DataFrame:
    if time_range_policy == MaterializationTimeRangePolicy.MATERIALIZATION_TIME_RANGE_POLICY_FAIL_IF_OUT_OF_RANGE:
        return _validate_feature_timestamps(spark, feature_df, feature_data_time_limits, timestamp_key)
    elif time_range_policy == MaterializationTimeRangePolicy.MATERIALIZATION_TIME_RANGE_POLICY_FILTER_TO_RANGE:
        return _filter_to_feature_data_time_limits(feature_df, feature_data_time_limits, timestamp_key)
    else:
        raise ValueError(f"Unhandled time range policy: {time_range_policy}")


def _filter_to_feature_data_time_limits(
    feature_df: DataFrame,
    feature_data_time_limits: Optional[pendulum.Period],
    timestamp_key: Optional[str],
) -> DataFrame:
    if feature_data_time_limits:
        feature_df = feature_df.filter(
            (feature_df[timestamp_key] >= feature_data_time_limits.start)
            & (feature_df[timestamp_key] < feature_data_time_limits.end)
        )

    return feature_df


def _ensure_timestamp_validation_udf_registered(spark):
    """
    Register the Spark UDF that is contained in the JAR files and that is part of passed Spark session.
    If the UDF was already registered by the previous calls, do nothing. This is to avoid calling the JVM
    registration code repeatedly, which can be flaky due to Spark. We cannot use `SHOW USER FUNCTIONS` because
    there is a bug in the AWS Glue Catalog implementation that omits the catalog ID.

    Jars are included the following way into the Spark session:
     - For materialization jobs scheduled by Orchestrator, they are included in the Job submission API.
       In this case, we always use the default Spark session of the spun-up Spark cluster.
     - For interactive execution (or remote over db-connect / livy), we always construct Spark session
       manually and include appropriate JARs ourselves.
    """
    global TIMESTAMP_VALIDATOR_UDF_REGISTERED
    if not TIMESTAMP_VALIDATOR_UDF_REGISTERED:
        udf_generator = spark.sparkContext._jvm.com.tecton.udfs.spark3.RegisterFeatureTimestampValidator()
        udf_generator.register(TECTON_FEATURE_TIMESTAMP_VALIDATOR)
        TIMESTAMP_VALIDATOR_UDF_REGISTERED = True


def _validate_feature_timestamps(
    spark: SparkSession,
    feature_df: DataFrame,
    feature_data_time_limits: Optional[pendulum.Period],
    timestamp_key: Optional[str],
) -> DataFrame:
    if conf.get_or_none(SKIP_FEATURE_TIMESTAMP_VALIDATION_ENV) is True:
        logger.info(
            f"Note: skipping the feature timestamp validation step because `SKIP_FEATURE_TIMESTAMP_VALIDATION` is set to true."
        )
        return feature_df

    if feature_data_time_limits:
        _ensure_timestamp_validation_udf_registered(spark)

        start_time_expr = f"to_timestamp('{feature_data_time_limits.start}')"
        # Registered feature timestamp validation UDF checks that each timestamp is within *closed* time interval: [start_time, end_time].
        # So we subtract 1 microsecond here, before passing time limits to the UDF.
        end_time_expr = f"to_timestamp('{feature_data_time_limits.end - pendulum.duration(microseconds=1)}')"
        filter_expr = f"{TECTON_FEATURE_TIMESTAMP_VALIDATOR}({timestamp_key}, {start_time_expr}, {end_time_expr}, '{timestamp_key}')"

        # Force the output of the UDF to be filtered on, so the UDF cannot be optimized away.
        feature_df = feature_df.where(filter_expr)

    return feature_df


class CustomFilterSparkNode(SparkExecNode):
    def __init__(self, node: CustomFilterNode):
        self.input_node = translate.spark_convert(node.input_node)
        self.filter_str = node.filter_str

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        return input_df.filter(self.filter_str)


class FeatureTimeFilterSparkNode(SparkExecNode):
    def __init__(self, node: FeatureTimeFilterNode):
        self.input_node = translate.spark_convert(node.input_node)
        self.feature_data_time_limits = node.feature_data_time_limits
        self.policy = node.policy
        self.timestamp_field = node.timestamp_field

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        return _apply_or_check_feature_data_time_limits(
            spark, input_df, self.policy, self.timestamp_field, self.feature_data_time_limits
        )


class EntityFilterSparkNode(SparkExecNode):
    def __init__(self, node: EntityFilterNode):
        self.feature_data = translate.spark_convert(node.feature_data)
        self.entities = translate.spark_convert(node.entities)
        self.entity_cols = node.entity_cols

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        feature_df = self.feature_data.to_dataframe(spark)
        entities_df = self.entities.to_dataframe(spark)
        return feature_df.join(entities_df, how="inner", on=self.entity_cols).select(feature_df.columns)


class TimeFilterSparkNode(SparkExecNode):
    def __init__(self, node: TimeFilterNode):
        self.input_node = translate.spark_convert(node.input_node)
        self.start_time = node.start_time
        self.end_time = node.end_time
        self.timestamp_field = node.timestamp_field

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        if self.start_time and self.end_time:
            return input_df.filter(
                (input_df[self.timestamp_field] >= self.start_time) & (input_df[self.timestamp_field] < self.end_time)
            )
        if self.start_time:
            return input_df.filter(input_df[self.timestamp_field] >= self.start_time)
        if self.end_time:
            return input_df.filter(input_df[self.timestamp_field] < self.end_time)


class RespectFSTSparkNode(SparkExecNode):
    def __init__(self, node: RespectFSTNode):
        self.input_node = translate.spark_convert(node.input_node)
        self.feature_start_time = node.feature_start_time
        self.retrieval_time_col = node.retrieval_time_col
        self.features = node.features

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        ret = self.input_node.to_dataframe(spark)
        cond = functions.col(self.retrieval_time_col) >= functions.lit(self.feature_start_time)
        # select all non-feature cols, and null out any features outside of feature start time
        project_list = [col for col in ret.columns if col not in self.features]
        for c in self.features:
            newcol = functions.when(cond, functions.col(f"`{c}`")).otherwise(functions.lit(None)).alias(c)
            project_list.append(newcol)
        return ret.select(project_list)


class RespectTTLSparkNode(SparkExecNode):
    def __init__(self, node: RespectTTLNode):
        self.input_node = translate.spark_convert(node.input_node)
        self.retrieval_time_col = node.retrieval_time_col
        self.expiration_time_col = node.expiration_time_col
        self.features = node.features

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        ret = self.input_node.to_dataframe(spark)
        cond = functions.col(self.retrieval_time_col) < functions.col(self.expiration_time_col)
        # select all non-feature cols, and null out any features outside of ttl
        project_list = [col for col in ret.columns if col not in self.features]
        for c in self.features:
            newcol = functions.when(cond, functions.col(c)).otherwise(functions.lit(None)).alias(c)
            project_list.append(newcol)
        return ret.select(project_list)


class StreamWatermarkSparkNode(SparkExecNode):
    def __init__(self, node: StreamWatermarkNode):
        self.input_node = translate.spark_convert(node.input_node)
        self.time_column = node.time_column
        self.stream_watermark = node.stream_watermark

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        ret = self.input_node.to_dataframe(spark)
        return ret.withWatermark(self.time_column, self.stream_watermark)
