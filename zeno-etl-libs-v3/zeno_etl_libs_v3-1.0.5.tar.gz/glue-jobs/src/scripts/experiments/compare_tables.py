"""
Owner: kuldeep.singh@zeno.health
Purpose: Compares tables
"""
import argparse
import sys
import os

import pandas as pd

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.db.db import MySQL

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stage, prod)")
parser.add_argument('-ss', '--source_schema', default="prod2-generico-14-08-22", type=str,
                    required=False)
parser.add_argument('-ts', '--target_schema', default="dev-3-9-22-generico", type=str,
                    required=False)
# parser.add_argument('-tn', '--table_name', default="molecule-master", type=str, required=False)
# parser.add_argument('-cns', '--column_names', default="name,molecule-group", type=str,
#                     required=False)

args, unknown = parser.parse_known_args()
env = args.env
source_schema = args.source_schema
target_schema = args.target_schema


def get_data(table=None, columns=None, db=None, count=None):
    column_str = ",".join(["`" + col + "`" for col in columns])
    limit_str = f" limit {count} " if count else " "
    # limit_str = f" limit 10 "
    query = f"""
        SELECT 
            id, {column_str}
        from 
            {table} 
        order by 
            id
        {limit_str}; 
    """

    return pd.read_sql_query(con=db.connection, sql=query)


os.environ['env'] = env
logger = get_logger()

# DB source
mysql_db_source = MySQL(read_only=False)
mysql_db_source.open_connection()

# DB target
mysql_db_target = MySQL(read_only=False)
mysql_db_target.open_connection()

table_columns = {
    "molecule-master": "name,molecule-group,hash",
    "composition-master-molecules-master-mapping": "molecule-master-id,composition-master-id,unit-type,unit-type-value",
    "composition-master": "composition,hash",
    "release-pattern-master": "name,group,short-form",
    "drug-molecule-release": "molecule-master-id,release,drug-id",
    "drugs": "available-in,composition-master-id",
    "available-in-group-mapping": "available-in,available-group"
}

for table_name, column_names in table_columns.items():
    logger.info(f"table: {table_name}")
    # table_name = args.table_name
    # column_names = args.column_names
    column_names = column_names.split(",")

    source_table_name = f"`{source_schema}`.`{table_name}`"
    target_table_name = f"`{target_schema}`.`{table_name}`"

    # logger.info(f"source_table_name: {source_table_name}")
    # logger.info(f"target_table_name: {target_table_name}")

    df_source = get_data(table=source_table_name, columns=column_names, db=mysql_db_source)
    length = len(df_source)
    logger.info(f"df_source: {df_source.head(2)}")
    logger.info(f"df_source length: {length}")

    df_target = get_data(table=target_table_name, columns=column_names, db=mysql_db_target,
                         count=length)
    logger.info(f"df_target: {df_target.head(2)}")

    df = df_source.compare(df_target)
    if df.empty:
        logger.info(f"Matched Successfully!")
    else:
        logger.info(f"\n\nMatch Failed: {df}")

    # logger.info("\n\n")
