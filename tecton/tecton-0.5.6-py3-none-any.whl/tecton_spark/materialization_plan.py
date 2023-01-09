from typing import Optional

import attr
import pendulum
from pyspark.sql import DataFrame
from pyspark.sql import functions
from pyspark.sql import SparkSession

from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper as FeatureDefinition
from tecton_core.logger import get_logger
from tecton_core.query.builder import build_run_querytree
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.rewrite import rewrite_tree
from tecton_core.time_utils import convert_timedelta_for_version
from tecton_spark.data_observability import MetricsCollector
from tecton_spark.partial_aggregations import TEMPORAL_ANCHOR_COLUMN_NAME
from tecton_spark.query import translate

MATERIALIZED_RAW_DATA_END_TIME = "_materialized_raw_data_end_time"
logger = get_logger("MaterializationPlan")


@attr.s(auto_attribs=True)
class MaterializationPlan:
    _fd: FeatureDefinition
    base_data_frame: DataFrame

    @classmethod
    def from_querytree(cls, fd: FeatureDefinition, query_tree: NodeRef, spark: SparkSession) -> "MaterializationPlan":
        spark_df = translate.spark_convert(query_tree).to_dataframe(spark)
        return cls(fd=fd, base_data_frame=spark_df)

    @property
    def offline_store_data_frame(self) -> DataFrame:
        return self.base_data_frame

    @property
    def online_store_data_frame(self) -> DataFrame:
        online_df = self.base_data_frame

        # batch online and offline df are slightly different
        if self._fd.is_temporal and not online_df.isStreaming:
            version = self._fd.get_feature_store_format_version
            batch_mat_schedule = convert_timedelta_for_version(self._fd.batch_materialization_schedule, version)
            online_df = self.base_data_frame.withColumn(
                MATERIALIZED_RAW_DATA_END_TIME, functions.col(TEMPORAL_ANCHOR_COLUMN_NAME) + batch_mat_schedule
            ).drop(TEMPORAL_ANCHOR_COLUMN_NAME)
        return online_df


def get_batch_materialization_plan(
    *,
    spark: SparkSession,
    feature_definition: FeatureDefinition,
    feature_data_time_limits: Optional[pendulum.Period],
    metrics_collector: Optional[MetricsCollector] = None,
) -> MaterializationPlan:
    """
    NOTE: We rely on Spark's lazy evaluation model to infer partially materialized tile Schema during FeatureView
    creation time without actually performing any materialization.
    Please make sure to not perform any Spark operations under this function's code path that will actually execute
    the Spark query (e.g: df.count(), df.show(), etc.).
    """
    query_tree = build_run_querytree(
        feature_definition,
        for_stream=False,
        feature_data_time_limits=feature_data_time_limits,
        enable_feature_metrics=(metrics_collector is not None),
    )
    rewrite_tree(query_tree)
    return MaterializationPlan.from_querytree(fd=feature_definition, query_tree=query_tree, spark=spark)


def get_stream_materialization_plan(
    *,
    spark: SparkSession,
    feature_definition: FeatureDefinition,
    metrics_collector: Optional[MetricsCollector] = None,
) -> MaterializationPlan:
    query_tree = build_run_querytree(
        feature_definition, for_stream=True, enable_feature_metrics=(metrics_collector is not None)
    )
    rewrite_tree(query_tree)
    return MaterializationPlan.from_querytree(fd=feature_definition, query_tree=query_tree, spark=spark)
