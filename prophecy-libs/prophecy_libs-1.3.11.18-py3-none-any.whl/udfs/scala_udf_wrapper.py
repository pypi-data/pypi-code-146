from typing import Optional

from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType


class UDFBase:
    sparkSession = None
    UDFUtils = None

    def __init__(self, spark):
        self.UDFUtils = spark.sparkContext._jvm.io.prophecy.libs.python.UDFUtils
        self.sparkSession = spark


udfConfig: Optional[UDFBase] = None


def initializeUDFBase(spark):
    global udfConfig
    if udfConfig is None:
        udfConfig = UDFBase(spark)
    return udfConfig


def rest_api(*cols):
    _cols = udfConfig.sparkSession.sparkContext._jvm.PythonUtils.toList([item._jc for item in list(cols)])
    rest_api_response = udfConfig.UDFUtils.rest_api(_cols)
    return 1
