import argparse
import os
import sys

import pandas as pd

from zeno_etl_libs.db.db import PostGreWrite, DB
from zeno_etl_libs.helper import helper

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stage, prod)")
parser.add_argument('-fr', '--full_run', default="yes", type=str, required=False)
parser.add_argument('-dfs', '--db_fetch_size', default=1000, type=int, required=False)
parser.add_argument('-ibs', '--insert_batch_size', default=100, type=int, required=False)

args, unknown = parser.parse_known_args()
env = args.env
full_run = args.full_run
db_fetch_size = args.db_fetch_size
insert_batch_size = args.insert_batch_size

os.environ['env'] = env

logger = get_logger()

logger.info(f"env: {env}")
logger.info(f"full_run: {full_run}")
logger.info(f"db_fetch_size: {db_fetch_size}")
logger.info(f"insert_batch_size: {insert_batch_size}")

""" opening the Redshift connection """
rs_db = DB()
rs_db.open_connection()

""" opening the postgres connection """
pg_db_w = PostGreWrite()
pg_db_w.open_connection()

pg_schema = "public"
rs_schema = "prod2-generico" if env == "dev" else "prod2-generico"

rs_table = "patients-metadata-2"
pg_table = rs_table.replace("-", "_")
pg_temp_table = pg_table + "_temp"

query = f""" SELECT max(updated_at) as "last_updated_at" FROM "{pg_schema}"."patients_metadata_2" """
df = pd.read_sql_query(query, pg_db_w.connection)
date_filter = ""
if df.last_updated_at[0] is not None:
    date_filter = f""" where "updated-at" >= '{df.last_updated_at[0]}' """

table_info = helper.get_table_info(db=rs_db, table_name=rs_table, schema=rs_schema)
columns = ["id",
           "value-segment",
           "value-segment-calculation-date",
           "behaviour-segment",
           "behaviour-segment-calculation-date",
           "last-bill-date",
           "number-of-bills",
           "total-spend",
           "average-bill-value",
           "is-chronic",
           "total-quantity",
           "quantity-generic",
           "quantity-generic-pc",
           "hd-bills",
           "referred-count",
           "latest-nps-rating",
           "latest-nps-rating-comment",
           "latest-nps-rating-date",
           "latest-nps-rating-store-id",
           "latest-nps-rating-store-name",
           "first-bill-date",
           "is-goodaid"]


def get_patients_metadata_from_rs(batch=1):
    limit = db_fetch_size
    """ Query to get patients-metadata from RS """
    query = f""" SELECT "{'","'.join(columns)}" FROM "{rs_schema}"."{rs_table}" {date_filter} 
    order by "updated-at" limit {limit} offset {(batch - 1) * limit} """
    logger.info(f"Batch: {batch}, limit:{limit} ")
    df: pd.DataFrame = rs_db.get_df(query=query)
    df.columns = [c.replace('-', '_') for c in df.columns]

    # fix data types
    for col in ['total_spend', 'average_bill_value', 'quantity_generic_pc']:
        df[col] = df[col].fillna(0.0).astype(float)

    for col in ['behaviour_segment_calculation_date', 'value_segment_calculation_date',
                'last_bill_date', 'latest_nps_rating_date', 'first_bill_date']:
        df[col] = pd.to_datetime(df[col], errors='ignore')

    for col in ['number_of_bills', 'total_quantity', 'quantity_generic', 'hd_bills',
                'referred_count', 'latest_nps_rating', 'latest_nps_rating_store_id']:
        df[col] = df[col].fillna(0).astype(int)

    for col in ['is_chronic', 'is_goodaid']:
        df[col] = df[col].fillna(False).astype(bool)
    logger.info("fetched data from RS DB successfully.")
    return df


try:
    # clean the temp table
    query = f""" delete from {pg_schema}.{pg_temp_table}; """
    pg_db_w.engine.execute(query)

    # insert_batch_size = 10000
    batch = 1
    while True:
        df = get_patients_metadata_from_rs(batch=batch)
        if df.empty:
            logger.info("Nothing to sync since last update.")
            break

        "Insert into the PostGre temp table"
        small_batch_counter = 1
        for ga_df in helper.batch(df, insert_batch_size):
            ga_df.to_sql(name=pg_temp_table, con=pg_db_w.engine, if_exists='append', chunksize=500,
                         method='multi', index=False)
            logger.info(f"small_batch_counter: {small_batch_counter}")
            small_batch_counter += 1
        logger.info("Inserted data in Postgres DB temp table.")

        if full_run.lower() != 'yes':
            break
        batch += 1
    """Sync temp and main table"""
    # 1. Delete the common records
    query = f"""
    delete from {pg_schema}.{pg_table} as tgt using {pg_schema}.{pg_temp_table} as src
    where tgt.id = src.id ;
    """
    pg_db_w.engine.execute(query)

    # 2. Insert the temp table records to main table
    query = f""" insert into {pg_schema}.{pg_table} select * from {pg_schema}.{pg_temp_table}; """
    pg_db_w.engine.execute(query)
    logger.info("Synced data in Postgres DB successfully")
except Exception as e:
    # logger.exception(e)
    raise e
finally:
    pg_db_w.close_connection()
    rs_db.close_connection()
