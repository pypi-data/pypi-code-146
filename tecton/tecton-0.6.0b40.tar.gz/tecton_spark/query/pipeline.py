from datetime import datetime
from typing import Dict
from typing import Optional

import attrs
import pendulum
import pyspark

from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_spark import data_observability
from tecton_spark.partial_aggregations import construct_partial_time_aggregation_df
from tecton_spark.pipeline_helper import _PipelineBuilder
from tecton_spark.pipeline_helper import dataframe_with_input
from tecton_spark.query.node import SparkExecNode
from tecton_spark.schema_spark_utils import schema_to_spark


@attrs.frozen
class OdfvPipelineSparkNode(SparkExecNode):
    input_node: SparkExecNode
    feature_definition_wrapper: FeatureDefinitionWrapper
    namespace: str

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        return dataframe_with_input(
            spark,
            self.feature_definition_wrapper.pipeline,
            self.input_node.to_dataframe(spark),
            schema_to_spark(self.feature_definition_wrapper.view_schema),
            transformations=self.feature_definition_wrapper.transformations,
            name=self.feature_definition_wrapper.name,
            fv_id=self.feature_definition_wrapper.id,
            namespace_separator=self.feature_definition_wrapper.namespace_separator,
            namespace=self.namespace,
        )


@attrs.frozen
class PipelineEvalSparkNode(SparkExecNode):
    inputs_map: Dict[str, SparkExecNode]
    feature_definition_wrapper: FeatureDefinitionWrapper

    # Needed for correct behavior by tecton_sliding_window udf if it exists in the pipeline
    feature_time_limits: Optional[pendulum.Period]

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        df = _PipelineBuilder(
            spark,
            self.feature_definition_wrapper.pipeline,
            consume_streaming_data_sources=False,
            data_sources=self.feature_definition_wrapper.data_sources,
            transformations=self.feature_definition_wrapper.transformations,
            feature_time_limits=self.feature_time_limits,
            schedule_interval=self.feature_definition_wrapper.batch_materialization_schedule,
            passed_in_inputs={k: self.inputs_map[k].to_dataframe(spark) for k in self.inputs_map},
        ).get_dataframe()
        return df


@attrs.frozen
class PartialAggSparkNode(SparkExecNode):
    input_node: SparkExecNode
    fdw: FeatureDefinitionWrapper = attrs.field()
    window_start_column_name: str
    window_end_column_name: Optional[str] = None
    aggregation_anchor_time: Optional[datetime] = None

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        df = construct_partial_time_aggregation_df(
            self.input_node.to_dataframe(spark),
            list(self.fdw.join_keys),
            self.fdw.trailing_time_window_aggregation,
            self.fdw.get_feature_store_format_version,
            window_start_column_name=self.window_start_column_name,
            window_end_column_name=self.window_end_column_name,
            aggregation_anchor_time=self.aggregation_anchor_time,
        )
        return df


@attrs.frozen
class MetricsCollectorSparkNode(SparkExecNode):
    input_node: SparkExecNode
    metrics_collector: data_observability.MetricsCollector = attrs.field(
        factory=data_observability.get_active_metrics_collector
    )

    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        return self.metrics_collector.observe(self.input_node.to_dataframe(spark))
