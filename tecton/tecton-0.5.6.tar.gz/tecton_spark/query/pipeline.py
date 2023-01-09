import pyspark

from tecton_core.query.nodes import FeatureViewPipelineNode
from tecton_core.query.nodes import FullAggNode
from tecton_core.query.nodes import MetricsCollectorNode
from tecton_core.query.nodes import OdfvPipelineNode
from tecton_core.query.nodes import PartialAggNode
from tecton_spark.aggregations import construct_full_tafv_df_with_anchor_time
from tecton_spark.data_observability import get_active_metrics_collector
from tecton_spark.partial_aggregations import construct_partial_time_aggregation_df
from tecton_spark.pipeline_helper import _PipelineBuilder
from tecton_spark.pipeline_helper import dataframe_with_input
from tecton_spark.query import translate
from tecton_spark.query.node import SparkExecNode
from tecton_spark.schema_spark_utils import schema_to_spark


class OdfvPipelineSparkNode(SparkExecNode):
    def __init__(self, node: OdfvPipelineNode):
        self.input_node = translate.spark_convert(node.input_node)
        self.feature_definition_wrapper = node.feature_definition_wrapper
        self.namespace = node.namespace

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
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


class PipelineEvalSparkNode(SparkExecNode):
    def __init__(self, node: FeatureViewPipelineNode):
        self.inputs_map = {key: translate.spark_convert(node.inputs_map[key]) for key in node.inputs_map}
        self.feature_definition_wrapper = node.feature_definition_wrapper
        # Needed for correct behavior on MaterializationContextNode in the pipeline
        self.feature_time_limits = node.feature_time_limits
        self.schedule_interval = node.schedule_interval

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        return _PipelineBuilder(
            spark,
            self.feature_definition_wrapper.pipeline,
            consume_streaming_data_sources=False,
            data_sources=self.feature_definition_wrapper.data_sources,
            transformations=self.feature_definition_wrapper.transformations,
            feature_time_limits=self.feature_time_limits,
            schedule_interval=self.schedule_interval,
            passed_in_inputs={k: self.inputs_map[k].to_dataframe(spark) for k in self.inputs_map},
        ).get_dataframe()


class PartialAggSparkNode(SparkExecNode):
    def __init__(self, node: PartialAggNode):
        self.input_node = translate.spark_convert(node.input_node)
        self.fdw = node.fdw
        self.window_start_column_name = node.window_start_column_name
        self.window_end_column_name = node.window_end_column_name
        self.aggregation_anchor_time = node.aggregation_anchor_time

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
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


class FullAggSparkNode(SparkExecNode):
    def __init__(self, node: FullAggNode):
        self.input_node = translate.spark_convert(node.input_node)
        self.fdw = node.fdw
        self.spine_spark_node = translate.spark_convert(node.spine) if node.spine else None
        self.respect_feature_start_time = node.respect_feature_start_time

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        spine_spark_df = self.spine_spark_node.to_dataframe(spark) if self.spine_spark_node else None
        res = construct_full_tafv_df_with_anchor_time(
            spark=spark,
            time_aggregation=self.fdw.trailing_time_window_aggregation,
            join_keys=self.fdw.join_keys,
            feature_store_format_version=self.fdw.get_feature_store_format_version,
            tile_interval=self.fdw.get_tile_interval,
            all_partial_aggregations_df=self.input_node.to_dataframe(spark),
            use_materialized_data=False,
            spine_df=spine_spark_df,
            fd=self.fdw,
            spine_join_keys=self.fdw.join_keys,
            respect_feature_start_time=self.respect_feature_start_time,
        )
        return res


class MetricsCollectorSparkNode(SparkExecNode):
    def __init__(self, node: MetricsCollectorNode):
        self.input_node = translate.spark_convert(node.input_node)
        self.metrics_collector = get_active_metrics_collector()

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        return self.metrics_collector.observe(self.input_node.to_dataframe(spark))
