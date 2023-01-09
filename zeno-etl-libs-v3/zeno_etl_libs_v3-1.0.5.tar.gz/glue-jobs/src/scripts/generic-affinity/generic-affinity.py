import argparse
import os
import sys

sys.path.append('../../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper import helper
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import datetime
from dateutil.tz import gettz
from zeno_etl_libs.db.db import DB, PostGreWrite
from zeno_etl_libs.helper import helper

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stag, prod)")
parser.add_argument('-bs', '--batch_size', default=10000, type=int, required=False)

args, unknown = parser.parse_known_args()

env = args.env
batch_size = args.batch_size
os.environ['env'] = env
logger = get_logger()

rs_db = DB()
rs_db.open_connection()

# PostGre
pg = PostGreWrite()
pg.open_connection()

s3 = S3()

schema = 'prod2-generico'
table_name = 'generic-affinity'
table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)


# =============================================================================
# Retrieve recent patient entries
# =============================================================================
mdate ="""
select
	max(date(last_visit)) as max_date
from
	generic_affinity ga ;
"""

mdate1 ="""
select
	max("last-visit"::date) as max_date
from
	"prod2-generico"."generic-affinity";
"""

m_date = pd.read_sql_query(mdate, pg.connection)
m_date1 = rs_db.get_df(mdate1)
m_date = m_date.append(m_date1)
max_date = m_date['max_date'].min()

if pd.isna(max_date)==False:
    date1 = max_date
else:
    date1= '2017-05-13'
    date1= datetime.datetime.strptime(date1, '%Y-%m-%d')
date1 = date1.strftime('%Y-%m-%d')

mquery = f""" (select
	"patient-id"
from
	"prod2-generico"."sales"
where
	"created-date" >= '{date1}'
    and "created-date" < CURRENT_DATE
group by
	"patient-id")    """

# =============================================================================
# patient level bill count
# =============================================================================
gb = f"""
    select
    	s1."patient-id" ,
    	count(distinct case when s1."type" = 'generic' and s1."bill-flag" = 'gross' then s1."bill-id" end ) as "generic_bill_count",
    	count(distinct case when s1."bill-flag" = 'gross' then s1."bill-id" end) as gross_bill_count
    from
    	"prod2-generico".sales s1
    	inner join 
    	{mquery} s2 on
        s1."patient-id" = s2."patient-id"
    where
    	date(s1."created-at")< CURRENT_DATE
    group by
    	s1."patient-id"
    """
p_bills=rs_db.get_df(gb)

logger.info("Data: patient level bill count fetched successfully")

p_bills.columns = [c.replace('-', '_') for c in p_bills.columns]
p_bills[['generic_bill_count', 'gross_bill_count']].fillna(0, inplace=True)

p_bills['generic_bill_pct'] = (p_bills['generic_bill_count'] / (p_bills['gross_bill_count'])) * 100

# =============================================================================
# patient level substitution
# =============================================================================
subs = f"""
    select
    	s1."patient-id" ,
    	s1."substitution-status" ,
    	sum(s1."quantity") as quantity
    from
    	"prod2-generico"."sales" s1
    	inner join 
        {mquery} s2 on
        s2."patient-id" = s1."patient-id"
    where
    	s1."bill-flag" = 'gross'
    	and s1."type" = 'generic'
    	and date(s1."created-at")<CURRENT_DATE 
    group by
    	s1."patient-id", s1."substitution-status" 
    """
p_subs=rs_db.get_df(subs)
p_subs.columns = [c.replace('-', '_') for c in p_subs.columns]

logger.info(f"p_subs: {len(p_subs)}")

p_subs['quantity'].fillna(0, inplace=True)
p_subs1 = pd.pivot_table(
    p_subs, values='quantity', index=['patient_id'], columns=['substitution_status']).reset_index()
p_subs1.columns = [c.replace('-', '_') for c in p_subs1.columns]

p_subs1.fillna(0, inplace=True)
col_list=[]
act_col=['substituted','not_substituted','not_in_inventory','generic_unavailable']
for i in act_col:
    if i not in p_subs1.columns:
        p_subs1[i]=0

p_subs1['subs_pct'] = (p_subs1['substituted'] / (p_subs1['substituted'] + p_subs1['not_substituted'])) * 100
metadata = pd.merge(right=p_subs1, left=p_bills, on=['patient_id'], how='left')

# =============================================================================
# patient level return %
# =============================================================================
ret = f"""
    select
    	s1."patient-id" ,
    	count(distinct case when s1."type" = 'generic' and s1."bill-flag" = 'return' then s1."bill-id" end ) as "generic_return_bill_count",
    	count(distinct case when s1."bill-flag" = 'return' then s1."bill-id" end) as "gross_return_bill"
    from
    	"prod2-generico".sales s1
    	inner join
    	{mquery} s2 
        on s2."patient-id" = s1."patient-id"
    where
    	date(s1."created-at")< CURRENT_DATE
    group by
    	s1."patient-id"
    """
p_return=rs_db.get_df(ret)
logger.info(f"p_return: {len(p_return)}")
p_return.columns = [c.replace('-', '_') for c in p_return.columns]

p_return[['generic_return_bill_count', 'gross_return_bill']].fillna(0, inplace=True)
p_return['return_pct'] = ((p_return['generic_return_bill_count']) / (p_return['gross_return_bill'])) * 100

p_return['not_return_pct'] = 100 - p_return['return_pct']

metadata = pd.merge(left=metadata, right=p_return, on=['patient_id'], how='left')

metadata['not_return_pct'].fillna(100, inplace=True)

# =============================================================================
# patient level recency
# =============================================================================
rec = f"""
    select
    	s1."patient-id" ,
    	max(s1."created-at") as "last_visit"
    from
    	"prod2-generico".sales s1 
    	inner join 
    	{mquery} s2 
        on s2."patient-id" = s1."patient-id"
    where
    	s1."bill-flag" = 'gross'
    	and date(s1."created-at")<CURRENT_DATE
    group by
    	s1."patient-id"
    """
p_recency=rs_db.get_df(rec)
logger.info(f"p_recency: {len(p_recency)}")

p_recency.columns = [c.replace('-', '_') for c in p_recency.columns]
prev_date = (datetime.datetime.today() + relativedelta(days=-1))
p_recency['last_visit'] = pd.to_datetime(p_recency['last_visit'], format="%y-%m-%d")
p_recency['prev_date'] = prev_date
p_recency['prev_date'] = pd.to_datetime(p_recency['prev_date'], format="%y-%m-%d")

p_recency['num_months'] = (p_recency['prev_date'] - p_recency['last_visit']) / np.timedelta64(1, 'M')

conditions = [
    (
        (p_recency['num_months'] <= 3)
    ),
    (
            (p_recency['num_months'] > 3) &
            (p_recency['num_months'] <= 6)
    ),
    (
            (p_recency['num_months'] > 6) &
            (p_recency['num_months'] <= 12)
    ),
    (
        (p_recency['num_months'] > 12)
    )
]
choices = [100, 75, 50, 25]
p_recency['recency_pct'] = np.select(conditions, choices, default=0)
p_recency['recency_pct'].fillna(0, inplace=True)
metadata = pd.merge(left=metadata, right=p_recency, on=['patient_id'], how='left')

# =============================================================================
# patient level generic recency
# =============================================================================
gen_rec = f"""
    select
    	s1."patient-id" ,
    	max(s1."created-at") as "last_generic_visit"
    from
    	"prod2-generico".sales s1 
    	inner join 
    	{mquery} s2 
        on s2."patient-id" = s1."patient-id"
    where
    	s1."bill-flag" = 'gross'
    	and s1."type" ='generic'
    	and date(s1."created-at")<CURRENT_DATE
    group by
    	s1."patient-id"
    """
p_grecency=rs_db.get_df(gen_rec)
logger.info(f"p_grecency: {len(p_grecency)}")

p_grecency.columns = [c.replace('-', '_') for c in p_grecency.columns]
p_grecency['last_generic_visit'] = pd.to_datetime(p_grecency['last_generic_visit'], format="%y-%m-%d")
p_grecency['g_prev_date'] = prev_date
p_grecency['g_prev_date'] = pd.to_datetime(p_grecency['g_prev_date'], format="%y-%m-%d")
p_grecency['g_num_months'] = ((p_grecency['g_prev_date'] - p_grecency['last_generic_visit'])
                              / np.timedelta64(1, 'M'))

conditions = [
    (
        (p_grecency['g_num_months'] <= 3)
    ),
    (
            (p_grecency['g_num_months'] > 3) &
            (p_grecency['g_num_months'] <= 6)
    ),
    (
            (p_grecency['g_num_months'] > 6) &
            (p_grecency['g_num_months'] <= 12)
    ),
    (
        (p_grecency['g_num_months'] > 12)
    )
]
choices = [100, 75, 50, 25]
p_grecency['gen_recency_pct'] = np.select(conditions, choices, default=0)
p_grecency.drop('g_prev_date', axis='columns', inplace=True)
p_grecency['gen_recency_pct'].fillna(0, inplace=True)

metadata = pd.merge(left=metadata, right=p_grecency, on=['patient_id'], how='left')

metadata.fillna(0, inplace=True)

metadata['generic_likelihood'] = ((metadata['generic_bill_pct'] + metadata['gen_recency_pct']
                                   + metadata['subs_pct'] + metadata['not_return_pct'] +
                                   metadata['recency_pct']) / (5))

conditions = [
    (
        (metadata['generic_likelihood'] >= 80)
    ),
    (
            (metadata['generic_likelihood'] < 80) &
            (metadata['generic_likelihood'] >= 60)
    ),
    (
            (metadata['generic_likelihood'] < 60) &
            (metadata['generic_likelihood'] >= 50)
    ),
    (

            (metadata['generic_likelihood'] < 50) &
            (metadata['generic_likelihood'] >= 25)
    ),
    (
        (metadata['generic_likelihood'] < 25)
    )
]

choices = [5, 4, 3, 2, 1]
metadata['generic_affinity_score'] = np.select(conditions, choices, default=3)

generic_affinity = metadata
logger.info('length of generic_affinity is :' + str(len(generic_affinity)))

generic_affinity.columns = [c.replace('_', '-') for c in generic_affinity.columns]
generic_affinity['refreshed-at'] = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime(
    '%Y-%m-%d %H:%M:%S')
generic_affinity['refreshed-at'] = pd.to_datetime(generic_affinity['refreshed-at'],
                                                  format="%Y-%m-%d %H:%M:%S")

generic_affinity = generic_affinity[generic_affinity['gross-bill-count'] > 0]

generic_affinity = generic_affinity[['patient-id'
    , 'gross-bill-count', 'generic-bill-count', 'generic-bill-pct'
    , 'generic-unavailable', 'not-in-inventory', 'not-substituted'
    , 'substituted', 'subs-pct', 'gross-return-bill', 'generic-return-bill-count'
    , 'return-pct', 'not-return-pct', 'last-visit', 'prev-date'
    , 'num-months', 'recency-pct', 'last-generic-visit', 'g-num-months'
    , 'gen-recency-pct', 'generic-likelihood', 'generic-affinity-score', 'refreshed-at']]

generic_affinity.columns = [c.replace('-', '_') for c in generic_affinity.columns]

table_update = f"{table_name}-update".replace("-", "_")

# Write to PostGre
query = f''' DELETE FROM {table_update}'''
pg.engine.execute(query)
generic_affinity[['patient_id']].to_sql(
    name=table_update, con=pg.engine, if_exists='append', chunksize=500, method='multi',
    index=False)
main_table = table_name.replace("-", "_")
query = f''' DELETE FROM {main_table} m1 using (select patient_id from {table_update}) m2 where
m1.patient_id = m2.patient_id'''
pg.engine.execute(query)
generic_affinity= generic_affinity.sort_values(by='last_visit',ascending=True)
total_insert = 0
for ga_df in helper.batch(generic_affinity, batch_size):
    ga_df.to_sql(name=main_table, con=pg.engine, if_exists='append',
                        chunksize=500, method='multi', index=False)
    total_insert += ga_df.shape[0]
    logger.info(f"Postgres DB write completed: {total_insert}")

# Write to Redshift Also
generic_affinity.columns = [c.replace('_', '-') for c in generic_affinity.columns]
generic_affinity['created-at'] = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime(
    '%Y-%m-%d %H:%M:%S')
generic_affinity['created-by'] = 'etl-automation'
generic_affinity['updated-at'] = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime(
    '%Y-%m-%d %H:%M:%S')
generic_affinity['updated-by'] = 'etl-automation'
truncate_query = f''' DELETE FROM "{schema}"."{table_name}" where date("last-visit")>= '{date1}' '''
rs_db.execute(truncate_query)

total_insert1 = 0
for ga_df1 in helper.batch(generic_affinity, batch_size):
    s3.write_df_to_db(df=ga_df1[table_info['column_name']], table_name=table_name, db=rs_db,
                  schema=schema)
    total_insert1 += ga_df1.shape[0]
    logger.info(f"Redshift DB write completed: {total_insert}")

# Closing the DB Connection
rs_db.close_connection()
pg.close_connection()
