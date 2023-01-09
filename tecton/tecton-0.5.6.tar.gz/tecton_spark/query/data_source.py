import pandas as pd
import pyspark

from tecton_core.query.nodes import DataNode
from tecton_core.query.nodes import DataSourceScanNode
from tecton_core.query.nodes import MockDataSourceScanNode
from tecton_core.query.nodes import OfflineStoreScanNode
from tecton_core.query.nodes import RawDataSourceScanNode
from tecton_spark import data_source_helper
from tecton_spark import offline_store
from tecton_spark.query import translate
from tecton_spark.query.node import SparkExecNode


class DataSparkNode(SparkExecNode):
    def __init__(self, node: DataNode):
        self.data = node.data

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        if isinstance(self.data, pyspark.sql.DataFrame):
            return self.data
        if isinstance(self.data, pd.DataFrame):
            return spark.createDataFrame(self.data)
        else:
            raise Exception(f"Unimplemented data type: {self.data}")


class MockDataSourceScanSparkNode(SparkExecNode):
    def __init__(self, node: MockDataSourceScanNode):
        self.data = translate.spark_convert(node.data)
        self.ds = node.ds
        self.start_time = node.start_time
        self.end_time = node.end_time

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        df = self.data.to_dataframe(spark)
        return data_source_helper.apply_partition_and_timestamp_filter(
            df, self.ds.batch_data_source, self.start_time, self.end_time
        )


class DataSourceScanSparkNode(SparkExecNode):
    def __init__(self, node: DataSourceScanNode):
        self.ds = node.ds
        self.start_time = node.start_time
        self.end_time = node.end_time
        self.is_stream = node.is_stream

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        return data_source_helper.get_ds_dataframe(
            spark,
            self.ds,
            consume_streaming_data_source=self.is_stream,
            start_time=self.start_time,
            end_time=self.end_time,
        )


# This is used for debugging method.
class RawDataSourceScanSparkNode(SparkExecNode):
    def __init__(self, node: RawDataSourceScanNode):
        self.ds = node.ds

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        return data_source_helper.get_non_dsf_raw_dataframe(spark, self.ds)


class OfflineStoreScanSparkNode(SparkExecNode):
    def __init__(self, node: OfflineStoreScanNode):
        self.feature_definition_wrapper = node.feature_definition_wrapper
        self.time_filter = node.time_filter

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        offline_reader = offline_store.get_offline_store_reader(spark, self.feature_definition_wrapper)
        # None implies no timestamp filtering. When we implement time filter pushdown, it will go here
        return offline_reader.read(self.time_filter)
