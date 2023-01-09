#!/usr/bin/env python
# coding: utf-8
"""
Owner -- Sanjay Bohra
Objective : to help calculating the incentive given for each goodaid drug_id,
            this script helps assign incentive to the drug_id's for all days within
            the start date and end date.
"""
import os
import sys
import argparse
import datetime as dt
import pandas as pd
import numpy as np
from dateutil.tz import gettz

sys.path.append('../../../..')

from zeno_etl_libs.helper.email.email import Email
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.helper import helper
from zeno_etl_libs.logger import get_logger

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
parser.add_argument('-et', '--email_to', default="sanjay.bohra@zeno.health",
                    type=str, required=False)
args, unknown = parser.parse_known_args()
email_to = args.email_to
env = args.env

os.environ['env'] = env
logger = get_logger()
logger.info(f"env: {env}")

rs_db = DB()
rs_db.open_connection()

s3 = S3()

# def main(rs_db, s3):
schema = 'prod2-generico'
table_name = 'goodaid-incentive-rate-day'
table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)

# Import data
query = '''
        select
            "drug-id" ,
            incentive ,
            "incentive-start-date" ,
            "incentive-end-date" 
        from
            "prod2-generico"."prod2-generico"."goodaid-incentive-rate-card" 
            '''
data = rs_db.get_df(query)
logger.info(f"Base ratecard read with length {len(data)}")
logger.info(f"Unique drug-id count {data['drug-id'].nunique()}")

# Explode
# This step splits every drug-id, incentive for each day
# between incentive start date and incentive end date
data['rate_date'] = [pd.date_range(s, e, freq='d') for s, e in
                         zip(pd.to_datetime(data['incentive-start-date']),
                             pd.to_datetime(data['incentive-end-date']))]
data.columns = [c.replace('-', '_') for c in data.columns]
data_export = pd.DataFrame({'drug_id': data.drug_id.repeat(data.rate_date.str.len()),
                            'incentive': data.incentive.repeat(data.rate_date.str.len()),
                            'rate_date': np.concatenate(data.rate_date.values)})
data_export.columns = [c.replace('_', '-') for c in data_export.columns]
logger.info(f"Exploded ratecard read with length {len(data_export)}")
logger.info(f"Unique drug-id count {data_export['drug-id'].nunique()}")

data_export['rate-date'] = data_export['rate-date'].dt.date
data_export['created-at'] = dt.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
data_export['created-by'] = 'etl-automation'
data_export['updated-at'] = dt.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
data_export['updated-by'] = 'etl-automation'

# =========================================================================
# Writing table in Redshift
# =========================================================================
if isinstance(table_info, type(None)):
    raise Exception(f"table: {table_name} do not exist, create the table first")
print(f"Table:{table_name} exists")
truncate_query = f''' DELETE FROM "{schema}"."{table_name}" '''
rs_db.execute(truncate_query)
logger.info(f"Table:{table_name} table truncated")

s3.write_df_to_db(df=data_export[table_info['column_name']], table_name=table_name, db=rs_db,
                      schema=schema)

logger.info(f"Table:{table_name} table uploaded")

data['Check_1'] = (data['incentive_end_date'] - data['incentive_start_date']).dt.days
x= sum(data.Check_1) + len(data)
diff = len(data_export) - x

if diff > 0:
    # Sending email
    subject = ''' Error in Goodaid Incentive Explode '''
    mail_body = '''There is a error in goodaid ratecard explode please review it.'''
    email = Email()
    email.send_email_file(subject=subject, mail_body=mail_body, to_emails=email_to)

# Closing the DB Connection
rs_db.close_connection()
