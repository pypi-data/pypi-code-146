import yaml
from pyspark.sql import SparkSession
from odapdbxbundle.common.logger import logger


def optimize_table(table_path, zorder):
    spark = SparkSession.getActiveSession()
    spark.sql(f"OPTIMIZE {table_path} ZORDER BY ({zorder})")
    logger.info(f"Table {table_path} optimized.")


def optimize_tables(config_path: str):
    with open(config_path, "r") as yamlfile:
        tables = yaml.load(yamlfile, Loader=yaml.FullLoader)

    for table in tables["tables"]:
        if table["zorder"] != "":
            optimize_table(table["table_path"], table["zorder"])
