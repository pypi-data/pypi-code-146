"""
Owner: kuldeep.singh@zeno.health
Purpose: Copy the list of table from mysql to reshift
"""
import argparse
import sys
import os

import pandas as pd

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.db.db import DB, MySQL
from zeno_etl_libs.helper.aws.s3 import S3

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stage, prod)")
parser.add_argument('-ss', '--source_schema_name', default="test-generico", type=str,
                    required=False)
parser.add_argument('-ts', '--target_schema_name', default="test-generico", type=str,
                    required=False)
parser.add_argument('-lot', '--list_of_tables',
                    default="""drugs""",
                    type=str,
                    required=False)

args, unknown = parser.parse_known_args()
env = args.env
os.environ['env'] = env

logger = get_logger()
logger.info(f"env: {env}")

source_schema_name = args.source_schema_name
target_schema_name = args.target_schema_name
list_of_tables = args.list_of_tables.split(",")

""" write connection """
db = DB(read_only=False)
db.open_connection()

""" read connection """
mysql_db = MySQL(read_only=False)
mysql_db.open_connection()

s3 = S3()


def df_type_change(df: pd.DataFrame):
    type_map = {"company-id": int, "pack-of": int, "preferred-distributor": int}
    df_cols = df.columns
    for key, type_name in type_map.items():
        if key in df_cols:
            df[key] = df[key].fillna(0).astype(type_name)
    return df


for table in list_of_tables:
    logger.info(f"Select table: {table}")
    """ read the data from source database """
    query = f""" select * from `{source_schema_name}`.`{table}` ; """
    df = pd.read_sql(con=mysql_db.connection, sql=query)

    """ clean the table first """
    logger.info(f"Delete started: {table}")
    query = f""" delete from "{target_schema_name}"."{table}" ; """
    db.execute(query=query)

    logger.info(f"Insert started: {table}")
    """ insert the data """
    df = df_type_change(df)
    s3.write_df_to_db(df=df, table_name=table, db=db, schema=target_schema_name)
    logger.info(f"End table: {table}")
