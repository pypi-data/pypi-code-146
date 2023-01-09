"""""
 author name : neha.karekar@zeno.health
 to get operational cost from accounts team gsheet

"""""

import argparse
import sys
import os

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper import helper
from zeno_etl_libs.helper.google.sheet.sheet import GoogleSheet
import pandas as pd
import dateutil
import datetime
from dateutil.tz import gettz
import numpy as np
from datetime import timedelta

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stag, prod)")
parser.add_argument('-d', '--full_run', default=0, type=int, required=False)

args, unknown = parser.parse_known_args()

env = args.env
full_run = args.full_run
os.environ['env'] = env
logger = get_logger()
logger.info(f"full_run: {full_run}")

rs_db = DB()
rs_db_write = DB(read_only=False)
rs_db.open_connection()
rs_db_write.open_connection()

s3 = S3()

schema = 'prod2-generico'
table_name = 'cash-burn-tableau-health-board'
table_info = helper.get_table_info(db=rs_db_write, table_name=table_name, schema=schema)

# max of data
burn_q = """
select
            date(max("burn-date")) max_exp
        from
            "prod2-generico"."cash-burn-tableau-health-board" 
        """
rs_db.execute(burn_q, params=None)
max_exp_date: pd.DataFrame = rs_db.cursor.fetch_dataframe()
max_exp_date['max_exp'].fillna(np.nan ,inplace=True)
print(max_exp_date.info())
max_exp_date = max_exp_date['max_exp'].to_string(index=False)
print(max_exp_date)
# Read from gsheet
gs = GoogleSheet()
burn_data = gs.download(data={
    "spreadsheet_id": "1WR5VeO1OyBqwMp3xXF2hn9ZIA5BxmVaqqEUBbOv4tzk",
    "sheet_name": "cash burn",
    "listedFields": []
})
df = pd.DataFrame(burn_data)
print(type(df['date']))
df[['date']] = df[
    ['date']] \
    .apply(pd.to_datetime, errors='coerce')
print(type(df['date']))
burn = df.copy()

# params
if full_run or max_exp_date == 'NaN':
    start = '2017-05-13'
else:
    start = max_exp_date
start = dateutil.parser.parse(start)
startminus2 = start - timedelta(days=2)
burn = burn[(burn['date'] >= start)]
# etl
burn['created-at'] = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
burn['updated-at'] = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
burn['created-by'] = 'etl-automation'
burn['updated-by'] = 'etl-automation'
burn.columns = [c.replace('_', '-') for c in burn.columns]
dict = {'date': 'burn-date'}
burn.rename(columns=dict,
          inplace=True)
if isinstance(table_info, type(None)):
    raise Exception(f"table: {table_name} do not exist, create the table first")
else:
    logger.info(f"Table:{table_name} exists")

    truncate_query = f''' DELETE FROM "{schema}"."{table_name}" where "burn-date">='{startminus2}' '''
    rs_db_write.execute(truncate_query)
    s3.write_df_to_db(df=burn[table_info['column_name']], table_name=table_name, db=rs_db_write,
                      schema=schema)
# Closing the DB Connection
rs_db.close_connection()
rs_db_write.close_connection()

