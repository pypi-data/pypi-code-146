from datetime import datetime
from typing import List
from typing import Optional
from typing import Union

import attrs
import pendulum
import pyspark
from pyspark.sql import DataFrame
from pyspark.sql import functions
from pyspark.sql import SparkSession
from pyspark.sql.types import LongType
from pyspark.sql.types import TimestampType

import tecton_core
from tecton_core import conf
from tecton_proto.data.feature_view_pb2 import MaterializationTimeRangePolicy
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


@attrs.frozen
class CustomFilterSparkNode(SparkExecNode):
    input_node: SparkExecNode
    filter_str: str

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        return input_df.filter(self.filter_str)


@attrs.frozen
class FeatureTimeFilterSparkNode(SparkExecNode):
    input_node: SparkExecNode
    feature_data_time_limits: pendulum.Period
    policy: MaterializationTimeRangePolicy
    timestamp_field: str

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        input_df = self.input_node.to_dataframe(spark)
        return _apply_or_check_feature_data_time_limits(
            spark, input_df, self.policy, self.timestamp_field, self.feature_data_time_limits
        )


@attrs.frozen
class EntityFilterSparkNode(SparkExecNode):
    feature_data: SparkExecNode
    entities: SparkExecNode
    entity_cols: List[str]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        feature_df = self.feature_data.to_dataframe(spark)
        entities_df = self.entities.to_dataframe(spark)
        return feature_df.join(entities_df, how="inner", on=self.entity_cols).select(feature_df.columns)


@attrs.frozen
class RespectFeatureStartTimeSparkNode(SparkExecNode):
    input_node: SparkExecNode
    retrieval_time_col: str
    feature_start_time: Union[pendulum.datetime, int]
    features: List[str]
    feature_store_format_version: int

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        ret = self.input_node.to_dataframe(spark)

        ts_col_datatype = ret.schema[self.retrieval_time_col].dataType
        if isinstance(self.feature_start_time, int):
            if not isinstance(ts_col_datatype, LongType):
                raise RuntimeError(
                    f"Invalid feature_start_time column type, expected LongType but got: {ts_col_datatype}"
                )
        elif isinstance(self.feature_start_time, datetime):
            if not isinstance(ts_col_datatype, TimestampType):
                raise RuntimeError(
                    f"Invalid feature_start_time column type, expected TimestampType but got: {ts_col_datatype}"
                )
        else:
            raise RuntimeError(f"Invalid feature_start_time type: {type(self.feature_start_time)}")

        cond = functions.col(self.retrieval_time_col) >= functions.lit(self.feature_start_time)
        # select all non-feature cols, and null out any features outside of feature start time
        project_list = [col for col in ret.columns if col not in self.features]
        for c in self.features:
            newcol = functions.when(cond, functions.col(f"`{c}`")).otherwise(functions.lit(None)).alias(c)
            project_list.append(newcol)
        return ret.select(project_list)


@attrs.frozen
class RespectTTLSparkNode(SparkExecNode):
    input_node: SparkExecNode
    retrieval_time_col: str
    expiration_time_col: str
    features: List[str]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        ret = self.input_node.to_dataframe(spark)
        cond = functions.col(self.retrieval_time_col) < functions.col(self.expiration_time_col)
        # select all non-feature cols, and null out any features outside of ttl
        project_list = [col for col in ret.columns if col not in self.features]
        for c in self.features:
            newcol = functions.when(cond, functions.col(c)).otherwise(functions.lit(None)).alias(c)
            project_list.append(newcol)
        return ret.select(project_list)


@attrs.frozen
class StreamWatermarkSparkNode(SparkExecNode):
    input_node: SparkExecNode
    time_column: str
    stream_watermark: str

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        ret = self.input_node.to_dataframe(spark)
        return ret.withWatermark(self.time_column, self.stream_watermark)
