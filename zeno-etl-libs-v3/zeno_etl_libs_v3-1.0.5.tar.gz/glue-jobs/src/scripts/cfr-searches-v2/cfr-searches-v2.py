#!/usr/bin/env python
# coding: utf-8

"""
Author - aashish.mishra@zeno.health, shubham.jangir@zeno.health
Purpose - script with database write for cfr searches v2
Purpose in detail - CFR searches is a terminology for billing panel compare tab drug search data
where-ever inventory of searched drug is 0. We then find out, whether they were made PR, or billed
In fixed time window, of 0 inventory search.

IPC algorithms and New stores stock launch algo, also take input from this job
"""

# !/usr/bin/env python
# coding: utf-8
import argparse
import sys
import os

sys.path.append('../../../..')

from zeno_etl_libs.db.db import DB
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper import helper
from zeno_etl_libs.logger import get_logger

from datetime import datetime
from datetime import timedelta
from dateutil.tz import gettz

import pandas as pd
import numpy as np

parser = argparse.ArgumentParser(description="This is ETL custom script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
parser.add_argument('-et', '--email_to', default="shubham.jangir@zeno.health", type=str, required=False)
parser.add_argument('-rd', '--runtime_date_exp', default="0101-01-01", type=str, required=False)

# any_period_run should be "yes" in case of manual run for historic data
parser.add_argument('-apr', '--any_period_run', default="no", type=str, required=False)

# start date should be assigned in case any_period_run =='yes'
parser.add_argument('-sd', '--start_date', default="0101-01-01", type=str, required=False)

# end date should be assigned in case any_period_run =='yes'
parser.add_argument('-ed', '--end_date', default="0101-01-01", type=str, required=False)

# run_type should be "delete" in case some past entries has to be deleted and
# "update" in case selected entries need update
parser.add_argument('-rt', '--run_type', default="no", type=str, required=False)

# Upload type should be "normal" on daily run, in case of manual update value should be changed
parser.add_argument('-ut', '--upload_type', default="normal", type=str, required=False)

args, unknown = parser.parse_known_args()
env = args.env
runtime_date_exp = args.runtime_date_exp
email_to = args.email_to
any_period_run = args.any_period_run
start_date = args.start_date
end_date = args.end_date
run_type = args.run_type
upload_type = args.upload_type

os.environ['env'] = env

logger = get_logger()
logger.info(f"env: {env}")

rs_db_write = DB(read_only=False)
rs_db_write.open_connection()

s3 = S3()

# Run date
if runtime_date_exp == '0101-01-01':
    # Timezone aware
    run_date = datetime.now(tz=gettz('Asia/Kolkata')).strftime("%Y-%m-%d")
else:
    run_date = runtime_date_exp
    # runtime_date = '2018-09-01'

# runtime_date = '2021-09-01'
logger.info("Running for {}".format(run_date))

# Period end date
# Paramatrize it
if any_period_run == 'no':
    period_end_d_ts = datetime.strptime(run_date, '%Y-%m-%d') - timedelta(days=1)
    period_end_d = period_end_d_ts.strftime('%Y-%m-%d')
else:
    period_end_d = end_date

logger.info("Run date minus 1 is {}".format(period_end_d))

# Read last list so that only new data to be uploaded

read_schema = 'prod2-generico'
rs_db_write.execute(f"set search_path to '{read_schema}'", params=None)

past_date_q = f"""
        SELECT
            "search-date"
        FROM
            "cfr-searches-v2"
        GROUP BY
            "search-date"
    """
logger.info(past_date_q)

last_data_date = rs_db_write.get_df(query=past_date_q)
last_data_date.columns = [c.replace('-', '_') for c in last_data_date.columns]

logger.info(f"length of last_data_date: {len(last_data_date)}")

if any_period_run == 'no':
    try:
        last_s_date_max = pd.to_datetime(last_data_date['search_date']).max().strftime('%Y-%m-%d')
    except ValueError:
        last_s_date_max = '2000-06-01'
else:
    last_s_date_max_ts = datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=1)
    last_s_date_max = last_s_date_max_ts.strftime('%Y-%m-%d')

logger.info("Last date in last data for cfr searches is : {}".format(last_s_date_max))

# Remaining data to be fetched


rs_db_write.execute(f"set search_path to '{read_schema}'", params=None)

search_q = """
        SELECT
            id,
            `store-id`,
            `created-at`,
            `drug-id`,
            `drug-name`,
            `composition`,
            `inventory-quantity`
        FROM
            `searches`
        WHERE date(`created-at`) > '{0}'
            and date(`created-at`) <= '{1}'
            and `inventory-quantity` = 0
""".format(last_s_date_max, period_end_d)

search_q = search_q.replace('`', '"')
logger.info(search_q)

data_s_zero = rs_db_write.get_df(query=search_q)
data_s_zero.columns = [c.replace('-', '_') for c in data_s_zero.columns]

logger.info("New Searches data length is : {}".format(len(data_s_zero)))

data_s_zero['search_timestamp'] = pd.to_datetime(data_s_zero['created_at'])
data_s_zero['search_date'] = pd.to_datetime(data_s_zero['search_timestamp'].dt.normalize())

# logger.info("Min date in new data is {} and max date is "
#      "{}".format(data_s['search_date'].min().strftime("%Y-%m-%d")
#               , data_s['search_date'].max().strftime("%Y-%m-%d")))

##################################################
# Now loss calculation starts
##################################################

# MySQL drugs table


rs_db_write.execute(f"set search_path to '{read_schema}'", params=None)

drugs_q = """
        SELECT
            id as drug_id,
            `drug-name`,
            `composition`,
            category as drug_category,
            type as drug_type,
            `repeatability-index`
        FROM
            drugs
"""

drugs_q = drugs_q.replace('`', '"')
logger.info(drugs_q)

data_drugs = rs_db_write.get_df(query=drugs_q)
data_drugs.columns = [c.replace('-', '_') for c in data_drugs.columns]

logger.info("Drug master length is : {}".format(len(data_drugs)))

# Join PR data with drugs
data_s_zero = data_s_zero.merge(data_drugs, how='left', on=['drug_id'])

logger.info("New Searches data length with zero inventory is : {}".format(len(data_s_zero)))

# Group at store, date, timestamp, drug level
data_s_zero_unique = data_s_zero.groupby(['store_id', 'search_date', 'search_timestamp',
                                          'drug_id', 'drug_name_y', 'composition_y',
                                          'repeatability_index', 'drug_category', 'drug_type']
                                         )['id'].count().reset_index().rename(columns={'id': 'search_count'})

# Todo - to be checked later, since it doesn't make a row count difference currently,
#  and drugs table used for other joins also
"""
Merge with the drugs table and groupby can be done in single query:
It will save compute time and memory utilisation
"""

logger.info("Zero inventory search data with grouping at store, date, timestamp, drug is length : "
            "{}".format(len(data_s_zero_unique)))
logger.info("Unique length is {}".format(len(data_s_zero_unique[['store_id', 'search_timestamp',
                                                                 'drug_id', 'drug_name_y']].drop_duplicates())))

#########################################
# Sales data
########################################


rs_db_write.execute(f"set search_path to '{read_schema}'", params=None)

sales_q = """
        SELECT
            `store-id`,
            `drug-id`,
            date(`created-at`) as sales_date,
            `created-at` as sold_timestamp,
            sum(quantity) as sold_quantity
        FROM
            sales
        WHERE date(`created-at`) >= '{0}'
            and date(`created-at`) <= '{1}'
            and `bill-flag` = 'gross'
        GROUP BY
            `store-id`,
            `drug-id`,
            date(`created-at`),
            `created-at`
""".format(last_s_date_max, period_end_d)

sales_q = sales_q.replace('`', '"')
logger.info(sales_q)

data_sales = rs_db_write.get_df(query=sales_q)
data_sales.columns = [c.replace('-', '_') for c in data_sales.columns]
logger.info(len(data_sales))

logger.info("Sales data length is {}".format(len(data_sales)))

data_sales['sold_timestamp'] = pd.to_datetime(data_sales['sold_timestamp'])
data_sales['sales_date'] = pd.to_datetime(data_sales['sales_date'])

# Merge
data_sales_merge = data_s_zero_unique[['store_id', 'drug_id', 'search_date', 'search_timestamp']].merge(
    data_sales[['store_id', 'drug_id', 'sales_date', 'sold_timestamp']], how='inner', on=['store_id', 'drug_id'])

logger.info("Length of search and sales data merged (containing all combinations) is "
            "{}".format(len(data_sales_merge)))

data_sales_merge['sold_timestamp_diff'] = (data_sales_merge['sold_timestamp'] -
                                           data_sales_merge['search_timestamp']
                                           ).astype('timedelta64[s]')

logger.info("Data sales merge head is {}".format(data_sales_merge.head()))

# Date same
data_sales_merge = data_sales_merge[data_sales_merge['sales_date'] == data_sales_merge['search_date']].copy()
logger.info("Data sales merge length after filtering same date is {}".format(len(data_sales_merge)))

# Time diff > 0
data_sales_merge = data_sales_merge[data_sales_merge['sold_timestamp_diff'] > 0].copy()
logger.info("Data sales merge length after filtering positive time difference is "
            "{}".format(len(data_sales_merge)))

# Flag
data_sales_merge_unique = data_sales_merge.drop_duplicates(
    subset=['store_id', 'drug_id', 'search_date', 'search_timestamp'])
data_sales_merge_unique['drug_sold_same_day_flag'] = 1
logger.info("Data sales merge length after dropping duplicates at search timestamp is "
            "{}".format(len(data_sales_merge_unique)))

# Merge with main dataframe
data_s_zero_unique = data_s_zero_unique.merge(
    data_sales_merge_unique[['store_id', 'drug_id',
                             'search_date', 'search_timestamp',
                             'drug_sold_same_day_flag']], how='left',
    on=['store_id', 'drug_id', 'search_date', 'search_timestamp'])
data_s_zero_unique['drug_sold_same_day_flag'] = data_s_zero_unique['drug_sold_same_day_flag'].fillna(0)

logger.info("Zero inventory search data after merging with sold data, length : "
            "{}".format(len(data_s_zero_unique)))

###############################################
# Composition sold same day (but after search)
###############################################
data_sales_comp = data_sales.merge(data_drugs[['drug_id', 'composition']], how='left', on='drug_id')
data_sales_comp = data_sales_comp[~data_sales_comp['composition'].isnull()].copy()
data_sales_comp = data_sales_comp[data_sales_comp['composition'] != ''].copy()

logger.info("Composition sales data length is {}".format(len(data_sales_comp)))

data_sales_comp_unique = data_sales_comp[
    ['store_id', 'composition', 'sales_date', 'sold_timestamp']].drop_duplicates()
logger.info("Composition sales data unique - length is {}".format(len(data_sales_comp_unique)))

# Merge
data_sales_comp_merge = data_s_zero_unique[['store_id', 'drug_id', 'composition_y', 'search_date',
                                            'search_timestamp']].merge(
    data_sales_comp_unique[['store_id', 'composition', 'sales_date', 'sold_timestamp']], how='inner',
    left_on=['store_id', 'composition_y'],
    right_on=['store_id', 'composition'])
data_sales_comp_merge = data_sales_comp_merge.drop(columns=['composition'], axis=1)

logger.info(
    "Length of search and comp sales data merged (containing all combinations) is {}".format(
        len(data_sales_comp_merge)))

data_sales_comp_merge['sold_timestamp_diff'] = (data_sales_comp_merge['sold_timestamp'] -
                                                data_sales_comp_merge['search_timestamp']
                                                ).astype('timedelta64[s]')

logger.info("Data comp sales merge head is {}".format(data_sales_comp_merge.head()))

# Date same
data_sales_comp_merge = data_sales_comp_merge[
    data_sales_comp_merge['sales_date'] == data_sales_comp_merge['search_date']].copy()
logger.info("Data comp sales merge length after filtering same date is "
            "{}".format(len(data_sales_comp_merge)))

# Time diff > 0
data_sales_comp_merge = data_sales_comp_merge[data_sales_comp_merge['sold_timestamp_diff'] > 0].copy()
logger.info("Data comp sales merge length after filtering positive time difference is "
            "{}".format(len(data_sales_comp_merge)))

# Flag
data_sales_comp_merge_unique = data_sales_comp_merge.drop_duplicates(
    subset=['store_id', 'drug_id', 'search_timestamp'])
data_sales_comp_merge_unique['comp_sold_same_day_flag'] = 1
logger.info("Data comp sales merge length after dropping duplicates at search timestamp is "
            "{}".format(len(data_sales_comp_merge_unique)))

# Merge with main dataframe
data_s_zero_unique = data_s_zero_unique.merge(
    data_sales_comp_merge_unique[['store_id', 'drug_id', 'search_timestamp',
                                  'comp_sold_same_day_flag']], how='left',
    on=['store_id', 'drug_id', 'search_timestamp'])
data_s_zero_unique['comp_sold_same_day_flag'] = data_s_zero_unique['comp_sold_same_day_flag'].fillna(0)

logger.info("Zero inventory search data after merging with comp sold data, length : "
            "{}".format(len(data_s_zero_unique)))

###################################
# Composition sold in window
##################################
data_sales_comp = data_sales.merge(data_drugs[['drug_id', 'composition']], how='left', on='drug_id')
data_sales_comp = data_sales_comp[~data_sales_comp['composition'].isnull()].copy()
data_sales_comp = data_sales_comp[data_sales_comp['composition'] != ''].copy()

logger.info("Window-Composition sales data length is {}".format(len(data_sales_comp)))

data_sales_comp_unique = data_sales_comp[['store_id', 'composition', 'sold_timestamp']].drop_duplicates()
logger.info("Window-Composition sales data unique - length is {}".format(len(data_sales_comp_unique)))

# Merge
data_sales_comp_merge = data_s_zero_unique[['store_id', 'drug_id', 'composition_y', 'search_timestamp']].merge(
    data_sales_comp_unique[['store_id', 'composition', 'sold_timestamp']], how='inner',
    left_on=['store_id', 'composition_y'],
    right_on=['store_id', 'composition'])
data_sales_comp_merge = data_sales_comp_merge.drop(columns=['composition'], axis=1)

logger.info(
    "Window-Length of search and comp sales data merged (containing all combinations) is {}".format(
        len(data_sales_comp_merge)))

data_sales_comp_merge['sold_timestamp_diff'] = (data_sales_comp_merge['sold_timestamp'] -
                                                data_sales_comp_merge['search_timestamp']
                                                ).astype('timedelta64[s]')

logger.info("Window-Data comp sales merge head is {}".format(data_sales_comp_merge.head()))

# Time diff > 0
data_sales_comp_merge = data_sales_comp_merge[data_sales_comp_merge['sold_timestamp_diff'] > 0].copy()
logger.info("Window-Data comp sales merge length after filtering positive time difference is "
            "{}".format(len(data_sales_comp_merge)))

# Time diff window 30 minutes = 1800 seconds
data_sales_comp_merge = data_sales_comp_merge[data_sales_comp_merge['sold_timestamp_diff'].between(1, 1800)].copy()
logger.info(
    "Window-Data comp sales merge length after filtering for window (30minutes) is {}".format(
        len(data_sales_comp_merge)))

# Flag
data_sales_comp_merge_unique = data_sales_comp_merge.drop_duplicates(
    subset=['store_id', 'drug_id', 'search_timestamp'])
data_sales_comp_merge_unique['comp_sold_window_flag'] = 1
logger.info("Window-Data comp sales merge length after dropping duplicates at search timestamp is "
            "{}".format(len(data_sales_comp_merge_unique)))

# Merge with main dataframe
data_s_zero_unique = data_s_zero_unique.merge(
    data_sales_comp_merge_unique[['store_id', 'drug_id', 'search_timestamp',
                                  'comp_sold_window_flag']], how='left',
    on=['store_id', 'drug_id', 'search_timestamp'])
data_s_zero_unique['comp_sold_window_flag'] = data_s_zero_unique['comp_sold_window_flag'].fillna(0)

logger.info("Window-Zero inventory search data after merging with comp sold data, length : "
            "{}".format(len(data_s_zero_unique)))

######################################################
# PR Made same day (but after search)
######################################################


rs_db_write.execute(f"set search_path to '{read_schema}'", params=None)

pr_q = """
            SELECT
                `store-id`,
                date(`created-at`) AS pr_date,
                `drug-id`,
                `created-at` as pr_timestamp
            FROM `patient-requests`
            WHERE date(`created-at`) >= '{0}'
                and date(`created-at`) <= '{1}'
            GROUP BY
                `store-id`,
                date(`created-at`),
                `drug-id`,
                `created-at`
""".format(last_s_date_max, period_end_d)

pr_q = pr_q.replace('`', '"')
logger.info(pr_q)

data_pr = rs_db_write.get_df(query=pr_q)
data_pr.columns = [c.replace('-', '_') for c in data_pr.columns]
logger.info(len(data_pr))

logger.info("PR data length is {}".format(len(data_pr)))

data_pr['pr_timestamp'] = pd.to_datetime(data_pr['pr_timestamp'])
data_pr['pr_date'] = pd.to_datetime(data_pr['pr_date'])

# Merge
data_pr_merge = data_s_zero_unique[['store_id', 'drug_id', 'search_date', 'search_timestamp']].merge(
    data_pr[['store_id', 'drug_id', 'pr_date', 'pr_timestamp']], how='inner', on=['store_id', 'drug_id'])

logger.info("Length of search and PR data merged (containing all combinations) is "
            "{}".format(len(data_pr_merge)))

data_pr_merge['pr_timestamp_diff'] = (data_pr_merge['pr_timestamp'] -
                                      data_pr_merge['search_timestamp']
                                      ).astype('timedelta64[s]')

logger.info("Data pr merge head is {}".format(data_pr_merge.head()))

# Date same
data_pr_merge = data_pr_merge[data_pr_merge['pr_date'] == data_pr_merge['search_date']].copy()
logger.info("Data pr merge length after filtering same date is {}".format(len(data_pr_merge)))

# Time diff > 0
data_pr_merge = data_pr_merge[data_pr_merge['pr_timestamp_diff'] > 0].copy()
logger.info("Data pr merge length after filtering positive time difference is {}".format(len(data_pr_merge)))

# Flag
data_pr_merge_unique = data_pr_merge.drop_duplicates(subset=['store_id', 'drug_id', 'search_timestamp'])
data_pr_merge_unique['pr_same_day_flag'] = 1
logger.info("Data pr merge length after dropping duplicates at search timestamp is "
            "{}".format(len(data_pr_merge_unique)))

# Merge with main dataframe
data_s_zero_unique = data_s_zero_unique.merge(data_pr_merge_unique[['store_id', 'drug_id',
                                                                    'search_timestamp',
                                                                    'pr_same_day_flag']],
                                              how='left',
                                              on=['store_id', 'drug_id', 'search_timestamp'])
data_s_zero_unique['pr_same_day_flag'] = data_s_zero_unique['pr_same_day_flag'].fillna(0)

logger.info("Zero inventory search data after merging with pr data, length : "
            "{}".format(len(data_s_zero_unique)))

###################################
# Composition PR same day (but after search)
##################################
data_pr_comp = data_pr.merge(data_drugs[['drug_id', 'composition']], how='left', on='drug_id')
data_pr_comp = data_pr_comp[~data_pr_comp['composition'].isnull()].copy()
data_pr_comp = data_pr_comp[data_pr_comp['composition'] != ''].copy()

logger.info("Composition pr data length is {}".format(len(data_pr_comp)))

data_pr_comp_unique = data_pr_comp[['store_id', 'composition',
                                    'pr_date', 'pr_timestamp']].drop_duplicates()
logger.info("Composition pr data unique - length is {}".format(len(data_pr_comp_unique)))

# Merge
data_pr_comp_merge = data_s_zero_unique[
    ['store_id', 'drug_id', 'composition_y', 'search_date', 'search_timestamp']].merge(
    data_pr_comp_unique[['store_id', 'composition', 'pr_date', 'pr_timestamp']], how='inner',
    left_on=['store_id', 'composition_y'],
    right_on=['store_id', 'composition'])
data_pr_comp_merge = data_pr_comp_merge.drop(columns=['composition'], axis=1)

logger.info(
    "Length of search and comp pr data merged (containing all combinations) is "
    "{}".format(len(data_pr_comp_merge)))

data_pr_comp_merge['pr_timestamp_diff'] = (data_pr_comp_merge['pr_timestamp'] -
                                           data_pr_comp_merge['search_timestamp']
                                           ).astype('timedelta64[s]')

logger.info("Data comp pr merge head is {}".format(data_pr_comp_merge.head()))

# Date same
data_pr_comp_merge = data_pr_comp_merge[data_pr_comp_merge['pr_date'] == data_pr_comp_merge['search_date']].copy()
logger.info("Data comp pr merge length after filtering same date is {}".format(len(data_pr_comp_merge)))

# Time diff > 0
data_pr_comp_merge = data_pr_comp_merge[data_pr_comp_merge['pr_timestamp_diff'] > 0].copy()
logger.info("Data comp pr merge length after filtering positive time difference is "
            "{}".format(len(data_pr_comp_merge)))

# Flag
data_pr_comp_merge_unique = data_pr_comp_merge.drop_duplicates(subset=['store_id', 'drug_id', 'search_timestamp'])
data_pr_comp_merge_unique['comp_pr_same_day_flag'] = 1
logger.info("Data comp pr merge length after dropping duplicates at search timestamp is {}".format(
    len(data_pr_comp_merge_unique)))

# Merge with main dataframe
data_s_zero_unique = data_s_zero_unique.merge(data_pr_comp_merge_unique[['store_id', 'drug_id',
                                                                         'search_timestamp',
                                                                         'comp_pr_same_day_flag']],
                                              how='left',
                                              on=['store_id', 'drug_id', 'search_timestamp'])
data_s_zero_unique['comp_pr_same_day_flag'] = data_s_zero_unique['comp_pr_same_day_flag'].fillna(0)

logger.info("Zero inventory search data after merging with comp pr data, length : "
            "{}".format(len(data_s_zero_unique)))

#################################################
# MS made same day (but after search)
#################################################

rs_db_write.execute(f"set search_path to '{read_schema}'", params=None)

ms_q = """
        SELECT
            `store-id`,
            date(`created-at`) AS ms_date,
            `drug-id`,
            `created-at` as ms_timestamp
        FROM `short-book-1`
        WHERE `auto-short` = 1
            and `patient-id` != 4480
            and date(`created-at`) >= '{0}'
            and date(`created-at`) <= '{1}'
        GROUP BY
            `store-id`,
            date(`created-at`),
            `drug-id`,
            `created-at`
""".format(last_s_date_max, period_end_d)

ms_q = ms_q.replace('`', '"')
logger.info(ms_q)

data_ms = rs_db_write.get_df(query=ms_q)
data_ms.columns = [c.replace('-', '_') for c in data_ms.columns]
logger.info(len(data_ms))

logger.info("MS data length is {}".format(len(data_pr)))

data_ms['ms_timestamp'] = pd.to_datetime(data_ms['ms_timestamp'])
data_ms['ms_date'] = pd.to_datetime(data_ms['ms_date'])

# Merge
data_ms_merge = data_s_zero_unique[['store_id', 'drug_id', 'search_date', 'search_timestamp']].merge(
    data_ms[['store_id', 'drug_id', 'ms_date', 'ms_timestamp']], how='inner', on=['store_id', 'drug_id'])

logger.info("Length of search and ms data merged (containing all combinations) is "
            "{}".format(len(data_ms_merge)))

data_ms_merge['ms_timestamp_diff'] = (data_ms_merge['ms_timestamp'] -
                                      data_ms_merge['search_timestamp']
                                      ).astype('timedelta64[s]')

logger.info("Data ms merge head is {}".format(data_ms_merge.head()))

# Date same
data_ms_merge = data_ms_merge[data_ms_merge['ms_date'] == data_ms_merge['search_date']].copy()
logger.info("Data ms merge length after filtering same date is {}".format(len(data_ms_merge)))

# Time diff > 0
data_ms_merge = data_ms_merge[data_ms_merge['ms_timestamp_diff'] > 0].copy()
logger.info("Data ms merge length after filtering positive time difference is "
            "{}".format(len(data_ms_merge)))

# Flag
data_ms_merge_unique = data_ms_merge.drop_duplicates(subset=['store_id', 'drug_id', 'search_timestamp'])
data_ms_merge_unique['ms_same_day_flag'] = 1
logger.info("Data ms merge length after dropping duplicates at search timestamp is "
            "{}".format(len(data_ms_merge_unique)))

# Merge with main dataframe
data_s_zero_unique = data_s_zero_unique.merge(data_ms_merge_unique[['store_id', 'drug_id', 'search_timestamp',
                                                                    'ms_same_day_flag']], how='left',
                                              on=['store_id', 'drug_id', 'search_timestamp'])
data_s_zero_unique['ms_same_day_flag'] = data_s_zero_unique['ms_same_day_flag'].fillna(0)

logger.info("Zero inventory search data after merging with ms data, length : "
            "{}".format(len(data_s_zero_unique)))

######################################################
# Short-book present same day (but after search)
#####################################################


rs_db_write.execute(f"set search_path to '{read_schema}'", params=None)

sb_q = """
        SELECT
            `store-id`,
            date(`created-at`) as shortbook_date,
            `drug-id`,
            `created-at` as shortbook_timestamp
        FROM `short-book-1`
        WHERE `auto-short` = 0
            and `auto-generated` = 0
            and date(`created-at`) >= '{0}'
            and date(`created-at`) <= '{1}'
        GROUP BY
            `store-id`,
            date(`created-at`),
            `drug-id`,
            `created-at`
    """.format(last_s_date_max, period_end_d)

sb_q = sb_q.replace('`', '"')
logger.info(sb_q)

data_sb = rs_db_write.get_df(query=sb_q)
data_sb.columns = [c.replace('-', '_') for c in data_sb.columns]
logger.info(len(data_sb))

logger.info("short-book data length is {}".format(len(data_sb)))

data_sb['shortbook_timestamp'] = pd.to_datetime(data_sb['shortbook_timestamp'])
data_sb['shortbook_date'] = pd.to_datetime(data_sb['shortbook_date'])

# Merge
data_sb_merge = data_s_zero_unique[['store_id', 'drug_id', 'search_date', 'search_timestamp']].merge(
    data_sb[['store_id', 'drug_id', 'shortbook_date', 'shortbook_timestamp']], how='inner',
    on=['store_id', 'drug_id'])

logger.info(
    "Length of search and shortbook data merged (containing all combinations) is "
    "{}".format(len(data_sb_merge)))

data_sb_merge['sb_timestamp_diff'] = (data_sb_merge['shortbook_timestamp'] -
                                      data_sb_merge['search_timestamp']
                                      ).astype('timedelta64[s]')

logger.info("Data shortbook merge head is {}".format(data_sb_merge.head()))

# Date same
data_sb_merge = data_sb_merge[data_sb_merge['shortbook_date'] == data_sb_merge['search_date']].copy()
logger.info("Data shortbook merge length after filtering same date is {}".format(len(data_sb_merge)))

# Time diff > 0
data_sb_merge = data_sb_merge[data_sb_merge['sb_timestamp_diff'] > 0].copy()
logger.info("Data shortbook merge length after filtering positive time difference is "
            "{}".format(len(data_sb_merge)))

# Flag
data_sb_merge_unique = data_sb_merge.drop_duplicates(subset=['store_id', 'drug_id', 'search_timestamp'])
data_sb_merge_unique['shortbook_present'] = 1
logger.info("Data shortbook merge length after dropping duplicates at search timestamp is "
            "{}".format(len(data_sb_merge_unique)))

# Merge with main dataframe
data_s_zero_unique = data_s_zero_unique.merge(data_sb_merge_unique[['store_id', 'drug_id',
                                                                    'search_timestamp',
                                                                    'shortbook_present']],
                                              how='left',
                                              on=['store_id', 'drug_id', 'search_timestamp'])
data_s_zero_unique['shortbook_present'] = data_s_zero_unique['shortbook_present'].fillna(0)

logger.info("Zero inventory search data after merging with sb data, length : "
            "{}".format(len(data_s_zero_unique)))

#########################################
# Group at store, date, drug level
#########################################
data_s_zero_grp = data_s_zero_unique.groupby(['store_id', 'search_date', 'drug_id',
                                              'drug_name_y', 'composition_y',
                                              'repeatability_index',
                                              'drug_category', 'drug_type']
                                             )['search_count', 'drug_sold_same_day_flag',
                                               'comp_sold_same_day_flag',
                                               'comp_sold_window_flag',
                                               'pr_same_day_flag',
                                               'comp_pr_same_day_flag',
                                               'ms_same_day_flag',
                                               'shortbook_present'].sum().reset_index()

logger.info(
    "Zero inventory search data with grouping at store, date, drug is length : "
    "{}".format(len(data_s_zero_grp)))

# Convert some columns into binary columns
for col in ['drug_sold_same_day_flag', 'comp_sold_same_day_flag',
            'comp_sold_window_flag', 'pr_same_day_flag', 'comp_pr_same_day_flag',
            'ms_same_day_flag', 'shortbook_present']:
    data_s_zero_grp[col] = np.where(data_s_zero_grp[col] > 0, 1, 0)

logger.info(
    "Zero inventory search data after taking binary columns - length : "
    "{}".format(len(data_s_zero_grp)))

# Populate rate for those not fulfilled
drugs = tuple(list(data_s_zero_grp['drug_id'].dropna().drop_duplicates().astype(int)))

logger.info("Count of drugs to look up in historical sales is : {}".format(len(drugs)))


rs_db_write.execute(f"set search_path to '{read_schema}'", params=None)

rate_q = """
        SELECT
            "drug-id",
            SUM("revenue-value")/SUM("quantity") AS avg_rate_system
        FROM
            "sales"
        WHERE
            date("created-at") <= '{0}'
            and "bill-flag" = 'gross'
        GROUP BY
            "drug-id"
""".format(period_end_d)

rate_q = rate_q.replace('`', '"')
logger.info(rate_q)

data_d = rs_db_write.get_df(query=rate_q)
data_d.columns = [c.replace('-', '_') for c in data_d.columns]
logger.info(len(data_d))

logger.info("Count of drugs to looked up successfully in historical sales is : "
            "{}".format(len(data_d)))

# Join with main data
data_s_zero_grp = data_s_zero_grp.merge(data_d, how='left', on=['drug_id'])

data_s_zero_grp['rate_present'] = np.where(data_s_zero_grp['avg_rate_system'] > 0, 1, 0)

# What should the final rate be, if not present in system
data_s_zero_grp['attributed_rate'] = np.where(data_s_zero_grp['rate_present'] == 1,
                                              data_s_zero_grp['avg_rate_system'],
                                              np.where(data_s_zero_grp['drug_type'] == 'generic',
                                                       35, 100))

# Read standard quantity
# Write connection for now, because it's a dependency table
# Change to read connection later


rs_db_write.execute(f"set search_path to '{read_schema}'", params=None)

std_q = """
        SELECT
            "drug-id",
            "std-qty" as "standard-quantity"
        FROM
            "drug-std-info"
"""

std_q = std_q.replace('`', '"')
logger.info(std_q)

data_drugs_q = rs_db_write.get_df(query=std_q)
data_drugs_q.columns = [c.replace('-', '_') for c in data_drugs_q.columns]
logger.info(len(data_drugs_q))

# Merge with main data
data_s_zero_grp = data_s_zero_grp.merge(data_drugs_q, how='left', on=['drug_id'])

# Impute for missing standard quantity
data_s_zero_grp['standard_quantity'] = data_s_zero_grp['standard_quantity'].fillna(1).astype(int)

# Remove outlier quantity
data_s_zero_grp['search_count_clean'] = np.where(data_s_zero_grp['search_count'] > 30, 30,
                                                 data_s_zero_grp['search_count'])

data_s_zero_grp['loss_quantity'] = data_s_zero_grp['search_count_clean'] * data_s_zero_grp[
    'standard_quantity']

data_s_zero_grp['lost_sales'] = data_s_zero_grp['loss_quantity'].astype(float) * data_s_zero_grp[
    'attributed_rate'].astype(float)


rs_db_write.execute(f"set search_path to '{read_schema}'", params=None)

sales_summ_q = """
    SELECT
        "store-id",
        "drug-id",
        COUNT(distinct date("created-at")) AS num_days_sold,
        MAX(date("created-at")) as last_sold
    FROM
        "sales"
    WHERE
        date("created-at") <= '{0}'
        and "drug-id" in {1}
        and "bill-flag" = 'gross'
    GROUP BY
        "store-id",
        "drug-id"
""".format(period_end_d, drugs)

sales_summ_q = sales_summ_q.replace('`', '"')
# logger.info(sales_summ_q)

data_d2 = rs_db_write.get_df(query=sales_summ_q)
data_d2.columns = [c.replace('-', '_') for c in data_d2.columns]
logger.info(len(data_d2))

logger.info("Count of drugs with sold quantity and num_days_sold is : {}".format(len(data_d2)))

# Join with main data
data_s_zero_grp = data_s_zero_grp.merge(data_d2, how='left', on=['store_id', 'drug_id'])

# Put 0 for those not sold in that store
data_s_zero_grp['num_days_sold'] = data_s_zero_grp['num_days_sold'].fillna(0)

############################################
# Final loss (to be defined)
############################################
data_s_zero_grp['sold_or_substituted_flag'] = np.where(((data_s_zero_grp['comp_sold_window_flag'] > 0) |
                                                        (data_s_zero_grp['drug_sold_same_day_flag'] > 0)), 1, 0)

data_s_zero_grp['pr_opportunity_flag'] = np.where(data_s_zero_grp['sold_or_substituted_flag'] > 0, 0, 1)

data_s_zero_grp['pr_converted_flag'] = np.where(data_s_zero_grp['comp_pr_same_day_flag'] > 0, 1, 0)

# Those which are already converted, should also be get added in opportunity

data_s_zero_grp['pr_opportunity_flag'] = np.where(data_s_zero_grp['pr_converted_flag'] > 0, 1,
                                                  data_s_zero_grp['pr_opportunity_flag'])

data_s_zero_grp['pr_opportunity_converted_flag'] = np.where((data_s_zero_grp['pr_opportunity_flag'] > 0) &
                                                            (data_s_zero_grp['pr_converted_flag'] > 0), 1, 0)

# Amount
data_s_zero_grp['lost_sales_not_substituted'] = np.where(data_s_zero_grp['sold_or_substituted_flag'] == 0,
                                                         data_s_zero_grp['lost_sales'], 0)

data_s_zero_grp['lost_sales_not_substituted_not_pr'] = np.where(data_s_zero_grp['pr_converted_flag'] == 0,
                                                                data_s_zero_grp['lost_sales_not_substituted'], 0)

# Final lost sales, sensitive
data_s_zero_grp['final_loss_flag'] = np.where((data_s_zero_grp['sold_or_substituted_flag'] == 0) &
                                              (data_s_zero_grp['pr_converted_flag'] == 0), 1, 0)

data_s_zero_grp['final_lost_sales'] = np.where(data_s_zero_grp['final_loss_flag'] == 1, data_s_zero_grp['lost_sales'],
                                               0)

# Round off some values
for i in ['attributed_rate', 'lost_sales', 'lost_sales_not_substituted',
          'lost_sales_not_substituted_not_pr', 'final_lost_sales']:
    data_s_zero_grp[i] = np.round(data_s_zero_grp[i].astype(float), 2)

# Merge with drug order info data to get safe-stock,min and max quantity on store_id,drug_id level


rs_db_write.execute(f"set search_path to '{read_schema}'", params=None)

doi_q = """
    SELECT 
        `store-id` ,
        `drug-id` ,
        `safe-stock` safety_stock,
        `min` minimum_quantity,
        `max` maximum_quantity
    FROM
        `drug-order-info` doi
    WHERE
        `drug-id` in {}
""".format(drugs)

doi_q = doi_q.replace('`', '"')
# logger.info(doi_q)

drug_order_info_data = rs_db_write.get_df(query=doi_q)
drug_order_info_data.columns = [c.replace('-', '_') for c in drug_order_info_data.columns]
logger.info(len(drug_order_info_data))

data_s_zero_grp = data_s_zero_grp.merge(drug_order_info_data, how='left', on=['store_id', 'drug_id'])

logger.info("Data length after merging with drug-order-info, is {}".format(len(data_s_zero_grp)))

# Merge stores


rs_db_write.execute(f"set search_path to '{read_schema}'", params=None)

stores_q = """
        SELECT
            id AS store_id,
            store AS store_name
        FROM
            "stores-master"
    """

stores_q = stores_q.replace('`', '"')
logger.info(stores_q)

stores = rs_db_write.get_df(query=stores_q)
stores.columns = [c.replace('-', '_') for c in stores.columns]
logger.info(len(stores))

data_s_zero_grp = data_s_zero_grp.merge(stores, how='left', on=['store_id'])

logger.info("Data length after merging with stores, is {}".format(len(data_s_zero_grp)))

# DB upload columns
final_cols = ['store_id', 'store_name', 'search_date',
              'drug_id', 'drug_name_y', 'composition_y',
              'repeatability_index', 'drug_category',
              'drug_type', 'search_count_clean',
              'rate_present', 'attributed_rate',
              'standard_quantity', 'loss_quantity',
              'lost_sales', 'lost_sales_not_substituted',
              'lost_sales_not_substituted_not_pr',
              'shortbook_present', 'final_lost_sales',
              'num_days_sold', 'last_sold',
              'safety_stock', 'minimum_quantity', 'maximum_quantity',
              'comp_sold_window_flag',
              'drug_sold_same_day_flag', 'comp_sold_same_day_flag',
              'pr_same_day_flag', 'comp_pr_same_day_flag',
              'ms_same_day_flag',
              'sold_or_substituted_flag', 'pr_opportunity_flag',
              'pr_converted_flag', 'pr_opportunity_converted_flag',
              'final_loss_flag']

data_export = data_s_zero_grp[final_cols]

# For redshift specific
# Convert int columns to int
for i in ['num_days_sold', 'safety_stock', 'minimum_quantity', 'maximum_quantity']:
    data_export[i] = data_export[i].fillna(0).astype(int)

logger.info(data_export.columns)

################################
# DB WRITE
###############################

write_schema = 'prod2-generico'
write_table_name = 'cfr-searches-v2'
update_table_name = 'cfr-searches-v2-etl-update'

table_info = helper.get_table_info(db=rs_db_write, table_name=write_table_name, schema=write_schema)

################################
# Table info for update table
###############################
table_info_update = helper.get_table_info(db=rs_db_write, table_name=update_table_name, schema=write_schema)

# table_info_clean = table_info[~table_info['column_name'].isin(['id', 'created-at', 'updated-at'])]

data_export.columns = [c.replace('_', '-') for c in data_export.columns]

# id and created-at
# Todo change to - later and remove id
data_export['id'] = -1
# Mandatory lines
data_export['created_at'] = datetime.now(
    tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')

# Deleting data for the choosen time period
if any_period_run == 'yes':
    if run_type == 'delete':

        rs_db_write.execute(f"set search_path to '{read_schema}'", params=None)
        delete_main_query = f"""
                                delete
                                from
                                    "cfr-searches-v2" 
                                where
                                    date("search-date") > '{last_s_date_max}' 
                                    and date("search-date") <= '{period_end_d}'
        """
        rs_db_write.execute(delete_main_query)

        s3.write_df_to_db(df=data_export[table_info['column_name']], table_name=write_table_name,
                          db=rs_db_write, schema=write_schema)
        logger.info("Uploading successful with length: {}".format(len(data_export)))

        # logger.info(str('cfr-searches-v2') + ' table data deleted for specific time period')
    elif run_type == 'update':


        rs_db_write.execute(f"set search_path to '{read_schema}'", params=None)

        delete_query = f"""                            
            delete from
                "cfr-searches-v2-etl-update"
        """
        rs_db_write.execute(delete_query)

        s3.write_df_to_db(df=data_export[table_info_update['column_name']], table_name=update_table_name,
                          db=rs_db_write, schema=write_schema)
        logger.info("Uploading successful with length: {}".format(len(data_export)))

        rs_db_write.execute(query="begin ;")

        update_main_query = f"""                    
                update
                    "cfr-searches-v2" set
                    "rate-present" = cfe2."rate-present" ,
                    "attributed-rate" = cfe2."attributed-rate" ,
                    "num-days-sold" = cfe2."num-days-sold" ,
                    "last-sold" = cfe2."last-sold" ,
                    "sold-or-substituted-flag" = cfe2."sold-or-substituted-flag" ,
                    "pr-opportunity-flag" = cfe2."pr-opportunity-flag" ,
                    "pr-converted-flag" = cfe2."pr-converted-flag" ,
                    "lost-sales-not-substituted" = cfe2."lost-sales-not-substituted" ,
                    "lost-sales-not-substituted-not-pr" = cfe2."lost-sales-not-substituted-not-pr" ,
                    "final-loss-flag" = cfe2."final-loss-flag" ,
                    "final-lost-sales" = cfe2."final-lost-sales" ,
                    "search-count-clean" = cfe2."search-count-clean" ,
                    "loss-quantity" = cfe2."loss-quantity" ,
                    "lost-sales" = cfe2."lost-sales"
                from
                    "prod2-generico"."cfr-searches-v2" cf2
                inner join "cfr-searches-v2-etl-update" cfe2 on
                    cfe2."search-date" = cf2."search-date"
                    and cfe2."store-id" = cf2."store-id"
                    and cfe2."drug-id" = cf2."drug-id" """
        rs_db_write.execute(update_main_query)

        rs_db_write.execute(query="commit ;")

if upload_type == 'normal':
    s3.write_df_to_db(df=data_export[table_info['column_name']], table_name=write_table_name,
                      db=rs_db_write, schema=write_schema)
    logger.info("Uploading successful with length: {}".format(len(data_export)))

# Closing the DB Connection
rs_db_write.close_connection()

logger.info("File ends")
