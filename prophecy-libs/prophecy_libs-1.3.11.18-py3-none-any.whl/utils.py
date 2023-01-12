from typing import Optional

from pyspark.sql import *


class ProphecyDataFrame:
    def __init__(self, df: DataFrame, spark: SparkSession):
        self.jvm = spark.sparkContext._jvm
        self.sqlContext = SQLContext(spark.sparkContext, sparkSession=spark)

        if type(df) == DataFrame:
            try:  # for backward compatibility
                self.extended_dataframe = self.jvm.org.apache.spark.sql.ProphecyDataFrame.extendedDataFrame(df._jdf)
            except TypeError:
                self.extended_dataframe = self.jvm.io.prophecy.libs.package.ExtendedDataFrameGlobal(df._jdf)
            self.dataframe = df
        else:
            try:
                self.extended_dataframe = self.jvm.org.apache.spark.sql.ProphecyDataFrame.extendedDataFrame(df._jdf)
            except TypeError:
                self.extended_dataframe = self.jvm.io.prophecy.libs.package.ExtendedDataFrameGlobal(df._jdf)
            self.dataframe = DataFrame(df, self.sqlContext)

    def interim(self, subgraph, component, port, subPath, numRows, interimOutput, detailedStats=False) -> DataFrame:
        result = self.extended_dataframe.interim(subgraph, component, port, subPath, numRows, interimOutput,
                                                 detailedStats)
        return DataFrame(result, self.sqlContext)

    def __getattr__(self, item: str):
        if item == "interim":
            self.interim

        if hasattr(self.extended_dataframe, item):
            return getattr(self.extended_dataframe, item)
        else:
            return getattr(self.dataframe, item)


class InterimConfig:

    def __init__(self):
        self.isInitialized = False
        self.interimOutput = None

    def initialize(self, spark: SparkSession, sessionForInteractive: str = ""):
        self.isInitialized = True
        self.interimOutput = spark.sparkContext._jvm.org.apache.spark.sql.InterimOutputHive2.apply(
            sessionForInteractive)

    def maybeInitialize(self, spark: SparkSession, sessionForInteractive: str = ""):
        if not self.isInitialized:
            self.initialize(spark, sessionForInteractive)

    def clear(self):
        self.isInitialized = False
        self.interimOutput = None


interimConfig = InterimConfig()


class MetricsCollector:

    # Called only for interactive execution and metrics mode.
    @classmethod
    def initializeMetrics(cls, spark: SparkSession):
        spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.initializeMetrics(spark._jsparkSession)

    @classmethod
    def start(cls, spark: SparkSession, sessionForInteractive: str = "", pipelineId: str = ""):
        global interimConfig
        interimConfig.maybeInitialize(spark, sessionForInteractive)
        try:
            spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.start(spark._jsparkSession, pipelineId,
                                                                                sessionForInteractive)
        except:
            #### making sure for compatibility with older prophecy-libs releases
            spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.start(spark._jsparkSession,
                                                                                sessionForInteractive)

    @classmethod
    def end(cls, spark: SparkSession):
        try:
            spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.end(spark._jsparkSession)
        except:
            #### making sure for compatibility with older prophecy-libs releases
            spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.end()
        global interimConfig
        interimConfig.clear()


def collectMetrics(spark: SparkSession, df: DataFrame, subgraph: str, component: str, port: str,
                   numRows: int = 40) -> DataFrame:
    global interimConfig
    interimConfig.maybeInitialize(spark)
    pdf = ProphecyDataFrame(df, spark)
    return pdf.interim(subgraph, component, port, "dummy", numRows, interimConfig.interimOutput)


def createEventSendingListener(spark: SparkSession, execution_url: str, session: str, scheduled: bool):
    spark.sparkContext._jvm.org.apache.spark.sql.MetricsCollector.addSparkListener(
        spark._jsparkSession, execution_url, session, scheduled)


def postDataToSplunk(props: dict, payload):
    import gzip
    import requests
    from requests import HTTPError
    from requests.adapters import HTTPAdapter
    from urllib3 import Retry

    with requests.Session() as session:
        with HTTPAdapter(max_retries=Retry(total=int(props.get("maxRetries", 4)),
                                           backoff_factor=float(props.get("backoffFactor", 1)),
                                           status_forcelist=[429, 500, 502, 503, 504])) as adapter:
            session.mount("http://", adapter)
            session.headers.update({"Authorization": "Splunk " + props["token"],
                                    "Content-Encoding": "gzip",
                                    "BatchId": props.get("batchId", None)})
            try:
                res = session.post(props["url"], gzip.compress(bytes(payload, encoding='utf8')))
                if res.status_code != 200 and props.get("stopOnFailure", False):
                    raise HTTPError(res.reason)
            finally:
                session.close()


def splunkHECForEachWriter(props: dict):
    def wrapper(batchDF: DataFrame, batchId: int):
        max_load: Optional[int] = props.get("maxPayload")
        # Take 90% of the payload limit and convert KB into Bytes
        max_load = int(0.9 * 1024 * int(max_load)) if max_load else None
        props.update({"batchId": str(batchId)})

        def f(iterableDF):
            payload, prevsize = "", 0

            for row in iterableDF:
                if max_load and prevsize + len(row) >= max_load:
                    print(f"buffer hit at size {prevsize}")
                    postDataToSplunk(props, payload)
                    payload, prevsize = "", 0
                else:
                    payload += '{"event":' + row + '}'
                    prevsize += len(row) + 10  # 10 bytes is for padding

            if payload:
                print(f"last payload with size {prevsize}")
                postDataToSplunk(props, payload)

        batchDF.toJSON().foreachPartition(f)

    return wrapper
