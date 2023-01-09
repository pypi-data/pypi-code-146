"""
purpose -- Gets exotel call log data from MongoDB
Author -- kuldeep.singh@zeno.health
"""

import argparse
import os
import sys
from datetime import datetime

import pandas as pd

sys.path.append('../../../..')

from zeno_etl_libs.db.db import DB, MongoDB
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper import helper
from zeno_etl_libs.logger import get_logger

parser = argparse.ArgumentParser(description="This is ETL custom script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
parser.add_argument('-bs', '--batch_size', default=1000, type=int, required=False)

args, unknown = parser.parse_known_args()
env = args.env
batch_size = args.batch_size

os.environ['env'] = env

s3 = S3()

rs_db = DB(read_only=False)
rs_db.open_connection()

mg_db = MongoDB()
mg_client = mg_db.open_connection("generico-crm")

schema = 'prod2-generico' if env == 'prod' else 'test-generico'
table_name = 'exotelincomingcalllogs'

database = mg_client["generico-crm"]
collection = database["exotelIncomingCallLogs"]

logger = get_logger()


def max_last_date():
    query = f""" select max(updatedat) as max_date from "{schema}"."{table_name}" """
    df = pd.read_sql_query(query, rs_db.connection)
    if df[b'max_date'][0] is None:
        return "2020-01-01 00:00:00.000000"
    else:
        return str(df[b'max_date'][0])


max_update_date = max_last_date()
logger.info(f"max update-at date: {max_update_date}")

query = {}
# query["CallTo"] = {u"$eq": u"02248900429"}
# query["RecordingUrl"] = {u"$ne": u"null"}
query["updatedAt"] = {u"$gt": datetime.strptime(f"{max_update_date}", "%Y-%m-%d %H:%M:%S.%f")}
sort = [(u"updatedAt", 1)]
skip = 0
df = pd.DataFrame()
cursor = collection.find(query, sort=sort, skip=0, limit=batch_size)
temp_df = pd.DataFrame(data=list(cursor))
df = temp_df.copy()

while not temp_df.empty:
    skip += batch_size
    logger.info(f"skip: {skip}")
    cursor = collection.find(query, sort=sort, skip=skip, limit=batch_size)
    temp_df = pd.DataFrame(data=list(cursor))
    df = pd.concat([df, temp_df])

if not df.empty:
    df.rename(columns={"_id": "oid__id"}, inplace=True)
    df.is_active = df.is_active.replace({True: 1, False: 0})
    df.is_exist_in_db = df.is_exist_in_db.replace({True: 1, False: 0}).fillna(0)
    df.columns = [c.lower() for c in df.columns]

    table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)

    """
    Fill the absent columns with default data in the dataframe
    """
    for i, c in table_info.iterrows():
        default_value = None
        if c['data_type'] == 'character varying':
            default_value = ""
        if c['data_type'] == 'timestamp without time zone':
            default_value = datetime.now(tz=None)
        if c['data_type'] == 'integer':
            default_value = 0
        df[c['column_name']] = df.get(c['column_name'], default_value)

    df['is_exist_in_db'] = df['is_exist_in_db'].astype(int)
    logger.info(f"Total {len(df)} new records found.")
    logger.info(f"df.head: {df.head()}")
    s3.write_df_to_db(df=df[table_info['column_name']], table_name=table_name, db=rs_db,
                      schema=schema)
else:
    logger.info("New data NOT found.")

mg_db.close()
rs_db.close_connection()
