from abc import abstractmethod
from typing import List

import attrs
import pyspark

from tecton_core.query import node_interface
from tecton_spark.query import translate


@attrs.frozen
class SparkExecNode:
    columns: List[str]

    @classmethod
    def from_query_node(cls, query_node: node_interface.QueryNode):
        kwargs = attrs.asdict(query_node, value_serializer=translate.attrs_spark_converter, recurse=False)
        kwargs["columns"] = query_node.columns
        return cls(**kwargs)

    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        df = self._to_dataframe(spark)
        if set([c.lower() for c in df.columns]) != set([c.lower() for c in self.columns]):
            pass
            # Because we do not refresh schemas on data sources, we can sometimes get different columns than what we have
            # cached. This is problematic but will require separate solution; don't fail for now
            # raise RuntimeError(f"Returned mismatch of columns: received: {df.columns}, expected: {self.columns}")
        return df

    @abstractmethod
    def _to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        raise NotImplementedError
