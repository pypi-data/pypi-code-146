import pyspark
import pyspark.sql.functions as F
import pyspark.sql.window as spark_window

from tecton_core import conf
from tecton_core.logger import get_logger
from tecton_core.query.nodes import AsofJoinNode
from tecton_core.query.nodes import JoinNode
from tecton_spark.query import translate
from tecton_spark.query.node import SparkExecNode

logger = get_logger("query_tree")
ASOF_JOIN_TIMESTAMP_COL_1 = "_asof_join_timestamp_1"
ASOF_JOIN_TIMESTAMP_COL_2 = "_asof_join_timestamp_2"


class JoinSparkNode(SparkExecNode):
    """
    A basic left join on 2 inputs
    """

    def __init__(self, node: JoinNode):
        self.left = translate.spark_convert(node.left)
        self.right = translate.spark_convert(node.right)
        self.join_cols = node.join_cols
        self.how = node.how

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        left_df = self.left.to_dataframe(spark)
        right_df = self.right.to_dataframe(spark)
        return left_df.join(right_df, how=self.how, on=self.join_cols)


class AsofJoinSparkNode(SparkExecNode):
    """
    A "basic" asof join on 2 inputs.
    LEFT asof_join RIGHT has the following behavior:
        For each row on the left side, find the latest (but <= in time) matching (by join key) row on the right side, and associate the right side's columns to that row.
    The result is a dataframe with the same number of rows as LEFT, with additional columns. These additional columns are prefixed with f"{right_prefix}_". This is the built-in behavior of the tempo library.

    There are a few ways this behavior can be implemented, but by test the best performing method has been to union the two inputs and use a "last" window function with skip_nulls.
    In order to match the rows together.
    """

    def __init__(self, node: AsofJoinNode):
        self.left_container = node.left_container
        self.right_container = node.right_container
        self.join_cols = node.join_cols

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        left_df = translate.spark_convert(self.left_container.node).to_dataframe(spark)
        right_df = translate.spark_convert(self.right_container.node).to_dataframe(spark)
        # The left and right dataframes are unioned together and sorted using 2 columns.
        # The spine will use the spine timestamp and the features will be ordered by their
        # (effective_timestamp, feature_timestamp) because multiple features can have the same effective
        # timestamp. We want to return the closest feature to the spine timestamp that also satisfies
        # the condition => effective timestamp < spine timestamp.
        # The ASOF_JOIN_TIMESTAMP_COL_1 and ASOF_JOIN_TIMESTAMP_COL_2 columns will be used for sorting.
        left_df = left_df.withColumn(ASOF_JOIN_TIMESTAMP_COL_1, F.col(self.left_container.timestamp_field))
        left_df = left_df.withColumn(ASOF_JOIN_TIMESTAMP_COL_2, F.col(self.left_container.timestamp_field))
        right_df = right_df.withColumn(ASOF_JOIN_TIMESTAMP_COL_1, F.col(self.right_container.effective_timestamp_field))
        right_df = right_df.withColumn(ASOF_JOIN_TIMESTAMP_COL_2, F.col(self.right_container.timestamp_field))

        if conf.get_bool("ENABLE_TEMPO"):
            from tempo import TSDF

            # TODO: Tempo needs to asof join using 2 columns.
            logger.warning("Do not use Tempo for ASOF join. It has not been validated.")

            # We'd like to do the following:
            left_tsdf = TSDF(left_df, ts_col=ASOF_JOIN_TIMESTAMP_COL_1, partition_cols=self.join_cols)
            right_tsdf = TSDF(right_df, ts_col=ASOF_JOIN_TIMESTAMP_COL_1, partition_cols=self.join_cols)
            # TODO(TEC-9494) - we could speed up by setting partition_ts to ttl size
            out = left_tsdf.asofJoin(right_tsdf, right_prefix=self.right_container.prefix, skipNulls=False).df
            return out
        else:
            # includes both fv join keys and the temporal asof join key
            timestamp_join_cols = [ASOF_JOIN_TIMESTAMP_COL_1, ASOF_JOIN_TIMESTAMP_COL_2]
            common_cols = self.join_cols + timestamp_join_cols
            left_nonjoin_cols = list(set(left_df.columns) - set(common_cols))
            # we additionally include the right time field though we join on the left's time field.
            # This is so we can see how old the row we joined against is and later determine whether to exclude on basis of ttl
            right_nonjoin_cols = list(set(right_df.columns) - set(self.join_cols + timestamp_join_cols))

            right_struct_col_name = "_right_values_struct"
            # wrap fields on the right in a struct. This is to work around null feature values and ignorenulls
            # used during joining/window function.
            cols_to_wrap = [F.col(c).alias(f"{self.right_container.prefix}_{c}") for c in right_nonjoin_cols]
            right_df = right_df.withColumn(right_struct_col_name, F.struct(*cols_to_wrap))
            # schemas have to match exactly so that the 2 dataframes can be unioned together.
            right_struct_schema = right_df.schema[right_struct_col_name].dataType
            left_full_cols = (
                [F.lit(True).alias("is_left")]
                + [F.col(x) for x in common_cols]
                + [F.col(x) for x in left_nonjoin_cols]
                + [F.lit(None).alias(right_struct_col_name).cast(right_struct_schema)]
            )
            right_full_cols = (
                [F.lit(False).alias("is_left")]
                + [F.col(x) for x in common_cols]
                + [F.lit(None).alias(x) for x in left_nonjoin_cols]
                + [F.col(right_struct_col_name)]
            )
            left_df = left_df.select(left_full_cols)
            right_df = right_df.select(right_full_cols)
            union = left_df.union(right_df)
            window_spec = (
                spark_window.Window.partitionBy(self.join_cols)
                .orderBy([F.col(c).cast("long").asc() for c in timestamp_join_cols])
                .rangeBetween(spark_window.Window.unboundedPreceding, spark_window.Window.currentRow)
            )
            right_window_funcs = [
                F.last(F.col(right_struct_col_name), ignorenulls=True).over(window_spec).alias(right_struct_col_name)
            ]
            # We use the right side of asof join to find the latest values to augment to the rows from the left side.
            # Then, we drop the right side's rows.
            spine_with_features_df = union.select(common_cols + left_nonjoin_cols + right_window_funcs).filter(
                f"is_left"
            )
            # unwrap the struct to return the fields
            return spine_with_features_df.select(self.join_cols + left_nonjoin_cols + [f"{right_struct_col_name}.*"])
