"""
purpose -- Gets minimum bill creation date for a pso and store from MongoDB to store in RS
Author -- abhinav.srivastava@zeno.health
"""

import os
import sys
import argparse
import pandas as pd

sys.path.append('../../../../../../../..')

from zeno_etl_libs.db.db import DB, MongoDB
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.logger import get_logger

parser = argparse.ArgumentParser(description="This is ETL custom script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)

args, unknown = parser.parse_known_args()
env = args.env

os.environ['env'] = env
logger = get_logger()

table_name = 'bill-click'
schema = 'prod2-generico'

s3 = S3()

rs_db = DB()
rs_db.open_connection()

mg_db = MongoDB()
mg_client = mg_db.open_connection("generico-crm")
db = mg_client['generico-crm']


def max_last_date():
    query = f""" select max("created-at") as max_date from "{schema}"."{table_name}" """
    df = pd.read_sql_query(query, rs_db.connection)
    if df[b'max_date'][0] is None:
        return "2020-01-01 00:00:00.000000"
    else:
        return str(df[b'max_date'][0])


try:
    collection = db['psoBillClickLogs'].find()
    data_raw = pd.DataFrame(list(collection))

    processed_data = data_raw.groupby(['pso_id', 'store_id'])\
        .aggregate({'createdAt': 'min'}).reset_index()
    processed_data.columns = [c.replace('_', '-').lower() for c in processed_data.columns]
    processed_data.rename(columns={'createdat':'created-at'}, inplace=True)

    max_update_date = max_last_date()
    logger.info(f"max update-at date: {max_update_date}")

    processed_data = processed_data.loc[processed_data['created-at'] >= max_update_date]

    s3.write_df_to_db(df=processed_data, table_name=table_name, db=rs_db, schema=schema)

except Exception as error:
    raise Exception(error)

finally:
    rs_db.close_connection()
    mg_db.close_connection()
