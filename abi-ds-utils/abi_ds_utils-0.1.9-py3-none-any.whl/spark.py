import os
from pyspark.sql import SparkSession
import pyspark.sql.functions as F


def getSpark(driver_memory: str = "21g") -> SparkSession:
    spark = (
        SparkSession.builder
        # General
        .master('local[*]')
        .config("spark.driver.maxResultSize", 0)

        # Get 80% of free memory (this might be a bad idea)
        .config("spark.driver.memory", driver_memory)
        .config("spark.dynamicAllocation.enabled", "true")

        # PyArrow for dtypes conversions
        .config("spark.sql.execution.arrow.pyspark.enabled", "true")

        # Jars compatible with the base-notebook image (Python 3.8.8, PySpark 3.1.1)
        .config('spark.jars.packages', 'org.apache.hadoop:hadoop-aws:3.1.1,io.delta:delta-core_2.12:1.0.1')

        # Delta Lake setup
        .config("spark.hadoop.fs.s3a.connection.maximum", 128)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        .config("spark.delta.logStore.class", "org.apache.spark.sql.delta.storage.S3SingleDriverLogStore")
    )
    if os.environ.get('AWS_SESSION_TOKEN') is not None:
        spark = spark.config(
            "fs.s3a.aws.credentials.provider",
            "org.apache.hadoop.fs.s3a.TemporaryAWSCredentialsProvider"
        )
    return spark.getOrCreate()


