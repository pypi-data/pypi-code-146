# Version 1 - target - Backend tat-sla table - done

# Version 2 plan
# For providing front end - few changes can be done to make it more user friedly input (Groups can be identified, User can add store infront of group)
# Drop whole table is risky - Provide option of update and new entry while providing UI

import os
import sys

sys.path.append('../../../..')

from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper.email.email import Email
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.config.common import Config
from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper import helper
from dateutil.tz import gettz

import json
import datetime

import argparse
import pandas as pd
import numpy as np
import traceback
import calendar

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
parser.add_argument('-et', '--email_to', default="saurav.maskar@zeno.health", type=str, required=False)
args, unknown = parser.parse_known_args()
env = args.env
email_to = args.email_to

os.environ['env'] = env

logger = get_logger(level='INFO')

logger.info(f"env: {env}")

rs_db = DB()
rs_db.open_connection()

s3 = S3()
start_time = datetime.datetime.now()
logger.info('Script Manager Initialized')
logger.info("")
logger.info("parameters reading")
logger.info(f"env: {env}")
logger.info("email_to - " + email_to)
logger.info("")

# date parameter
logger.info("code started at {}".format(datetime.datetime.now().strftime(
    '%Y-%m-%d %H:%M:%S')))
logger.info("")

# SLA Provided via Retool

as_ms_sla = pd.read_csv(s3.download_file_from_s3(file_name="SLA/sla_tat/AS_MS_SLA.csv"))
pr_sla  = pd.read_csv(s3.download_file_from_s3(file_name="SLA/sla_tat/PR_SLA.csv"))
# as_ms_sla = pd.read_csv(r'D:\Dashboards TAT\SLA Automations\AS_MS_SLA.csv')
# pr_sla = pd.read_csv(r'D:\Dashboards TAT\SLA Automations\PR_sla.csv')

sla = pd.concat([as_ms_sla,pr_sla],sort=True)
logger.info('fetched SLA sheet provided by planning team')

# Fetching Active stores
store_query = '''
    select
        s.id as "store-id",
        case
            when s."franchisee-id" = 1 then 'coco'
            else 'fofo'
        end as "franchisee-flag",
        s."franchisee-id" ,
        s."city-id",
        s."is-active" ,
        s.category
    from
        "prod2-generico".stores s
        '''
stores_data = rs_db.get_df(store_query)
stores_data.columns = [c.replace('-', '_') for c in stores_data.columns]

# Fetching only active, retail stores

stores_data = stores_data[stores_data['category']=='retail']
stores_data = stores_data[stores_data['is_active']==1]

del stores_data['category']

logger.info('fetched current active store list')

# Creating SLA table

sla_db = pd.DataFrame()

for as_ms_pr_flag in sla['as_ms_pr_flag'].unique():
    if as_ms_pr_flag == 'as_ms':
        auto_short = 1
    elif as_ms_pr_flag == 'pr':
        auto_short = 0

    for franchisee_flag in sla['franchisee_flag'].unique():

        for distributor_type in sla['distributor_type'].unique():

            for round in sla['round'].unique():

                for day in sla['day'].unique():

                    sla_temp = sla[(sla['as_ms_pr_flag']==as_ms_pr_flag)&
                                   (sla['franchisee_flag']==franchisee_flag)&
                                   (sla['distributor_type']==distributor_type)&
                                   (sla['round']==round)&
                                   (sla['day']==day)]

                    sla_temp['store_id'] = sla_temp['store_ids'].str.split('|')
                    sla_temp = sla_temp.explode('store_id')
                    sla_temp['store_id'] = sla_temp['store_id'].astype(int)
                    store_temp = sla_temp['store_id'].unique()
                    stores_data_temp = stores_data[stores_data['franchisee_flag']==franchisee_flag]

                    sla_temp = sla_temp.merge(stores_data_temp ,on = ['franchisee_flag','store_id'],how = 'outer')

                    for col in sla_temp.columns:
                        fillna_number = sla_temp[sla_temp['store_id'] == 0][col].squeeze()
                        sla_temp[col] = sla_temp[col].fillna(fillna_number)

                    sla_temp['auto_short'] = auto_short

                    sla_temp = sla_temp[sla_temp['store_id']!=0]
                    sla_temp = sla_temp[sla_temp['is_active']==1]

                    sla_db = pd.concat([sla_temp,sla_db],sort=True)

del sla_db['store_ids']
del sla_db['is_active']

logger.info('table created at same granularity that is required in DB')

# Checking If any duplicate entry

dup_col_check_cols = ['as_ms_pr_flag', 'day','round','store_id','distributor_type']
boolean = sla_db[dup_col_check_cols ].duplicated().any()

if boolean:
    logger.info(f'duplicated entry found - {boolean}')
    duplicateRowsDF = sla_db[sla_db.duplicated(subset=dup_col_check_cols,keep=False)]
    sla_db.drop_duplicates(subset=dup_col_check_cols,
                      keep='first', inplace=True)
else:
    logger.info(f'duplicated entry found - {boolean}')
    duplicateRowsDF = pd.DataFrame()

# formatting sla_db to upload
sla_db.columns =  [c.replace('_', '-') for c in sla_db.columns]
cols_to_convert_to_int = ['auto-short', 'city-id', 'day', 'delivery-date',
       'delivery-time', 'dispatch-date', 'dispatch-time',
       'franchisee-id', 'invoice-date', 'invoice-time',
       'order-date', 'order-time', 'reorder-date', 'reorder-time', 'round',
       'store-id']
sla_db[cols_to_convert_to_int] = sla_db[cols_to_convert_to_int].astype(int)

# Uploading to RS
schema = 'prod2-generico'
table_name = 'tat-sla'
table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)
status2 = False

if isinstance(table_info, type(None)):
    raise Exception(f"table: {table_name} do not exist, create the table first")
else:
    logger.info(f"Table:{table_name} exists")

    truncate_query = f''' delete
                        from "{schema}"."{table_name}" '''
    rs_db.execute(truncate_query)
    logger.info(str(table_name) + ' table deleted')

    s3.write_df_to_db(df=sla_db[table_info['column_name']], table_name=table_name, db=rs_db,
                      schema=schema)

    logger.info(str(table_name) + ' table uploaded')
    status2 = True

if status2 is True:
    status = 'Success'
else:
    status = 'Failed'

# Email
cur_date = datetime.datetime.now(tz=gettz('Asia/Kolkata')).date()
duplicate_entry_uri = s3.save_df_to_s3(df=duplicateRowsDF, file_name=f'sla_duplicate_entries_{cur_date}.csv')
sla_db_uri = s3.save_df_to_s3(df=sla_db, file_name=f'tat_sla_final_{cur_date}.csv')

email = Email()

email.send_email_file(subject=f"{env}-{status} : SLA update",
                      mail_body=f"duplicated entry found - {boolean}",
                      to_emails=email_to, file_uris=[duplicate_entry_uri,sla_db_uri])

rs_db.close_connection()
