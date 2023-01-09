"""""
 author name : neha.karekar@zeno.health
 to drug count in assortment daily

"""""

import argparse
import sys
import os

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper import helper
import pandas as pd
import dateutil
import datetime
from dateutil.tz import gettz
import numpy as np
from datetime import timedelta

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
table_name = 'system-drug-assortment-count'
table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)

try:
        # count of drugs in assortment
        df_q = """
                select "type",count(distinct d.id) "drug-id-count",
                count(distinct case when "is-validated" ='Yes' then d.id end) "verified-drug-count"
                from "prod2-generico".drugs d 
                group by 1
                """
        df = rs_db.get_df(df_q)

        # etl
        df['created-at'] = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
        df['updated-at'] = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
        df['created-by'] = 'etl-automation'
        df['updated-by'] = 'etl-automation'

        if isinstance(table_info, type(None)):
            raise Exception(f"table: {table_name} do not exist, create the table first")
        else:
            logger.info(f"Table:{table_name} exists")

            truncate_query = f''' DELETE FROM "{schema}"."{table_name}" where date("created-at")=current_date'''
            rs_db.execute(truncate_query)
            s3.write_df_to_db(df=df[table_info['column_name']], table_name=table_name, db=rs_db,
                              schema=schema)
except :
    raise Exception("error")
finally:
    rs_db.close_connection()
    rs_db.close_connection()



