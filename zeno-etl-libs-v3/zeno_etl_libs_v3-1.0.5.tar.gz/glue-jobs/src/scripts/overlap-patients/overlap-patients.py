"""
purpose: to fetch and store overlap patients data which are to be excluded from each cohort sent
author : neha.karekar@zeno.health
"""

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

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stag, prod)")

args, unknown = parser.parse_known_args()

env = args.env
os.environ['env'] = env
logger = get_logger()


rs_db = DB()
rs_db.open_connection()

s3 = S3()

schema = 'prod2-generico'
table_name = 'overlap-patients'
table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)

# Read from gsheet
gs = GoogleSheet()
overlap_data = gs.download(data={
    "spreadsheet_id": "1wXY_0eIE5ZnjMxRfcQq92oDIU9rFLtqR1vvNyRxylAc",
    "sheet_name": "overlap",
    "listedFields": []
})
overlap_data = pd.DataFrame(overlap_data)

# etl
overlap_data['created-at'] = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')

overlap_data.columns = [c.replace('_', '-') for c in overlap_data.columns]

truncate_query = f''' DELETE FROM "{schema}"."{table_name}" '''
rs_db.execute(truncate_query)

s3.write_df_to_db(df=overlap_data[table_info['column_name']], table_name=table_name, db=rs_db,
                  schema=schema)
# Closing the DB Connection
rs_db.close_connection()
