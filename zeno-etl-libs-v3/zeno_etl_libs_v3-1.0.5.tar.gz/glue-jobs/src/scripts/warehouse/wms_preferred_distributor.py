# -*- coding: utf-8 -*-
"""
Created on Wed May 4 11:52:28 2022

@author: akshay.bhutada@zeno.health

Purpose: To get WMS preferred distributors and Review period of distributors
"""

from zeno_etl_libs.db.db import DB, MongoDB, MSSql
import sys
import os
import argparse

sys.path.append('../../../..')

from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper import helper
import pandas as pd
from datetime import datetime
from dateutil.tz import gettz


parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
parser.add_argument('-et', '--email_to', default="akshay.bhutada@zeno.health",
                    type=str, required=False)
args, unknown = parser.parse_known_args()
env = args.env
email_to = args.email_to

os.environ['env'] = env

#   Part 1:  Preferred Distributor

mg_db = MongoDB()
mg_client = mg_db.open_connection("generico-crm")

db = mg_client['generico-crm']
collection = db["wmsDrugDistributorMappingV2"].find()

dist_list = pd.DataFrame(list(collection))

pref_dist=dist_list[['wms_id','is_active','drug_id','drug_name','rank1','rank1_name','moq']]

pref_dist=pref_dist.rename(columns={'rank1':'distributor_id','rank1_name':'distributor_name'})


pref_dist[['drug_id','distributor_id']]=\
    pref_dist[['drug_id','distributor_id']].apply(pd.to_numeric, errors='ignore').astype('Int64')


created_at = datetime.now(tz=gettz('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")

pref_dist['created-date']=datetime.strptime(created_at,"%Y-%m-%d %H:%M:%S")

pref_dist['etl-created-at']=datetime.strptime(created_at,"%Y-%m-%d %H:%M:%S")

updated_at = datetime.now(tz=gettz('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")

pref_dist['etl-updated-at']=datetime.strptime(updated_at,"%Y-%m-%d %H:%M:%S")

pref_dist['etl-created-by'] = 'etl-automation'

pref_dist['etl-updated-by'] = 'etl-automation'

pref_dist.columns = [c.replace('_', '-') for c in pref_dist.columns]


rs_db= DB()
rs_db.open_connection()
s3=S3()

schema = "prod2-generico"
table_name = "preferred-distributor"


table_info = helper.get_table_info(db=rs_db
                                   , table_name=table_name, schema=schema)

#Truncate the Query

snapshot_date = datetime.now().date()


truncate_query = '''
       delete from "prod2-generico"."preferred-distributor"
       '''

rs_db.execute(truncate_query)

s3.write_df_to_db(df=pref_dist[table_info['column_name']], table_name=table_name,
                      db=rs_db, schema='prod2-generico')



# Part 2 : Review Time

mg_db = MongoDB()
mg_client = mg_db.open_connection("generico-crm")

db = mg_client['generico-crm']
collection = db["distributorConfiguration"].find()

dist_list = pd.DataFrame(list(collection))

review_time=dist_list[['is_active','wms_id','distributor_id','distributor_name','weekly_po','proxy_wh']]


pd.options.mode.chained_assignment = None

review_time['days_in_week']=review_time['weekly_po'].copy().apply(lambda a:len(a))

review_time['days_in_week']=review_time['days_in_week'].replace(0,4)

review_time['review_days']=\
    review_time['days_in_week'].copy()\
        .apply(lambda a: 4 if a==2 else (3 if a==3 else (7 if a==1 else (1 if a==7 else 4))))


review_time[['distributor_id']]=\
    review_time[['distributor_id']].apply(pd.to_numeric, errors='ignore').astype('Int64')


review_time[['proxy_wh']]=\
    review_time[['proxy_wh']].astype('str')




created_at = datetime.now(tz=gettz('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")

review_time['created-date']=datetime.strptime(created_at,"%Y-%m-%d %H:%M:%S")

review_time['etl-created-at']=datetime.strptime(created_at,"%Y-%m-%d %H:%M:%S")

updated_at = datetime.now(tz=gettz('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")

review_time['etl-updated-at']=datetime.strptime(updated_at,"%Y-%m-%d %H:%M:%S")

review_time['etl-created-by'] = 'etl-automation'

review_time['etl-updated-by'] = 'etl-automation'

review_time.columns = [c.replace('_', '-') for c in review_time.columns]


rs_db= DB()
rs_db.open_connection()
s3=S3()

schema = "prod2-generico"
table_name = "wms-distributors-review-time"

table_info = helper.get_table_info(db=rs_db
                                   , table_name=table_name, schema=schema)

#Truncate the Query

snapshot_date = datetime.now().date()


truncate_query = '''
       delete from "prod2-generico"."wms-distributors-review-time"
       '''

rs_db.execute(truncate_query)

s3.write_df_to_db(df=review_time[table_info['column_name']], table_name=table_name,
                      db=rs_db, schema='prod2-generico')


rs_db.close_connection()

mg_db.close_connection()