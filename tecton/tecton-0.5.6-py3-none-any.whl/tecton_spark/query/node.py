from abc import ABC
from abc import abstractmethod

import pyspark


class SparkExecNode(ABC):
    @abstractmethod
    def to_dataframe(self, spark: pyspark.sql.SparkSession) -> pyspark.sql.DataFrame:
        raise NotImplementedError
