"""
Author:shubham.gupta@zeno.health
Purpose: Patient_NOB_ABV_History & Campaign effectiveness
"""

import argparse
import os
import sys

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.helper import helper

from datetime import datetime as dt
from datetime import timedelta
import pandas as pd
from dateutil.tz import gettz

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
parser.add_argument('-et', '--email_to', default="shubham.gupta@zeno.health", type=str, required=False)
parser.add_argument('-fr', '--full_run', default=0, type=int, required=False)
args, unknown = parser.parse_known_args()
env = args.env
os.environ['env'] = env

email_to = args.email_to
full_run = args.full_run
logger = get_logger()

logger.info(f"env: {env}")
logger.info(f"print the env again: {env}")

# params
if full_run:
    start = dt.strptime('2017-05-13', '%Y-%m-%d')
    end = dt.today().date() - timedelta(days=1)
else:
    start = dt.today().date() - timedelta(days=91)
    end = dt.today().date() - timedelta(days=1)

interval = (end - start).days

schema = 'prod2-generico'
table_name = "campaign-prepost"

rs_db = DB()
rs_db.open_connection()

s3 = S3()

table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)

read_schema = 'prod2-generico'

if isinstance(table_info, type(None)):
    logger.info(f"table: {table_name} do not exist")
else:
    truncate_query = f"""
            DELETE
            FROM
                "{read_schema}"."{table_name}"
            WHERE
                "bill-date" BETWEEN '{start}' AND '{end}';
                """
    logger.info(truncate_query)
    rs_db.execute(truncate_query)

# Fetching all patient who used promo
df_q = f"""select
                b.*,
                r1."previous-3trips-abv",
                r1."previous-90days-trips",
                r1."pre3trips-promo",
                r2."next-3trips-abv",
                r2."next-90days-trips",
                r2."post3trips-promo"
            from
                (
                select
                    rm.id as "bill-id",
                    rm."patient-id",
                    rm."promo-code",
                    rm."promo-code-type" as "code-type",
                    rm."store-id",
                    rm."bill-date",
                    rm."prev-cum-nob" as "previous-total-trips",
                    rm.store,
                    rm.abo,
                    rm."store-manager",
                    rm."line-manager",
                    rm."store-opened-at",
                    rm."is-chronic",
                    rm."hd-flag",
                    rm."is-generic",
                    rm."pr-flag",
                    rm."is-repeatable",
                    rm."behaviour-segment",
                    rm."value-segment",
                    rm."total-spend" as "bill-value",
                    rm."promo-discount",
                    rm."recency-customer-days" as "last-visit-in-days",
                    pc."type",
                    pc."discount-type",
                    pc."discount-level",
                    pc."flat-discount",
                    pc."percent-discount",
                    pc."max-discount",
                    pc."min-purchase",
                    pc."max-time",
                    pc."max-per-patient",
                    pc."start",
                    pc.expiry, 
                    pc."campaign-id",
                    c.campaign 
                from
                    "{read_schema}"."retention-master" rm
                left join "{read_schema}"."promo-codes" pc on rm."promo-code-id" = pc.id 
                left join "{read_schema}".campaigns c on pc."campaign-id" = c.id 
                where
                    rm."promo-code-id" is not null
                    and datediff('days', rm."created-at", current_date) <= {interval}
                    ) b
            left join (
                select
                    "bill-id",
                    avg("total-spend") as "previous-3trips-abv",
                    max("bill-rank-2") as "previous-90days-trips",
                    sum("promo-bill") as "pre3trips-promo"
                from
                    (
                    select
                        rm1.id as "bill-id",
                        rm1."bill-date" as "bill-date-1",
                        rm2."bill-date" as "bill-date-2",
                        rm2."total-spend",
                        datediff('days', "bill-date-1", "bill-date-2") as "datediff",
                        rank() over (partition by rm1."id" order by "datediff" desc) as "bill-rank-1",
                        rank() over (partition by rm1."id" order by "datediff" asc) as "bill-rank-2",
                        datediff('days', "bill-date-1", current_date) as "datediff-filter",
                        (case
                            when rm2."promo-code-id" is not null then 1
                            else 0
                        end) "promo-bill"
                    from
                        "{read_schema}"."retention-master" rm1
                    left join "{read_schema}"."retention-master" rm2 on
                        rm1."patient-id" = rm2."patient-id"
                    where
                        "datediff" between -90 and 0
                        and rm1.id != rm2.id
                        and "datediff-filter" between 0 and {interval}
                        and rm1."promo-code-id" is not null
                )
                where
                    "bill-rank-1" <= 3
                group by
                    "bill-id") r1 on
                b."bill-id" = r1."bill-id"
            left join (
                select
                    "bill-id",
                    avg("total-spend") as "next-3trips-abv",
                    max("bill-rank-2") as "next-90days-trips",
                    sum("promo-bill") as "post3trips-promo"
                from
                    (
                    select
                        rm1.id as "bill-id",
                        rm1."bill-date" as "bill-date-1",
                        rm2."bill-date" as "bill-date-2",
                        rm2."total-spend",
                        datediff('days', "bill-date-1", "bill-date-2") as "datediff",
                        rank() over (partition by rm1."id" order by "datediff" asc) as "bill-rank-1",
                        rank() over (partition by rm1."id" order by "datediff" desc) as "bill-rank-2",
                        datediff('days', "bill-date-1", current_date) as "datediff-filter",
                        (case
                            when rm2."promo-code-id" is not null then 1
                            else 0
                        end) "promo-bill"
                    from
                        "{read_schema}"."retention-master" rm1
                    left join "{read_schema}"."retention-master" rm2 on
                        rm1."patient-id" = rm2."patient-id"
                    where
                        "datediff" between 0 and 90
                        and rm1.id != rm2.id
                        and "datediff-filter" between 0 and {interval}
                        and rm1."promo-code-id" is not null
                )
                where
                    "bill-rank-1" <= 3
                group by
                    "bill-id") r2 on
                b."bill-id" = r2."bill-id";
            """

patient_data = rs_db.get_df(query=df_q)
logger.info(f'Patient promo data query : {df_q}')
logger.info(f'Patient promo data query size : {len(patient_data)}')

logger.info(patient_data.info())

# data type correction
patient_data['bill-value'] = patient_data['bill-value'].astype(float)
patient_data['promo-discount'] = patient_data['promo-discount'].astype(float)
patient_data['flat-discount'] = patient_data['flat-discount'].fillna(0).astype(int)
patient_data['percent-discount'] = patient_data['percent-discount'].fillna(0).astype(int)
patient_data['max-discount'] = patient_data['max-discount'].fillna(0).astype(int)
patient_data['min-purchase'] = patient_data['min-purchase'].fillna(0).astype(int)
patient_data['max-time'] = patient_data['max-time'].fillna(0).astype(int)
patient_data['max-per-patient'] = patient_data['max-per-patient'].fillna(0).astype(int)
patient_data['campaign-id'] = patient_data['campaign-id'].fillna(0).astype(int)

patient_data['hd-flag'] = patient_data['hd-flag'].astype(int)
patient_data['pr-flag'] = patient_data['pr-flag'].astype(int)
patient_data['is-generic'] = patient_data['is-generic'].astype(int)
patient_data['is-chronic'] = patient_data['is-chronic'].astype(int)
patient_data['is-repeatable'] = patient_data['is-repeatable'].astype(int)

patient_data['previous-total-trips'] = patient_data['previous-total-trips'].fillna(0).astype(int)
patient_data['previous-90days-trips'] = patient_data['previous-90days-trips'].fillna(0).astype(int)
patient_data['pre3trips-promo'] = patient_data['pre3trips-promo'].fillna(0).astype(int)
patient_data['next-90days-trips'] = patient_data['next-90days-trips'].fillna(0).astype(int)
patient_data['post3trips-promo'] = patient_data['post3trips-promo'].fillna(0).astype(int)
patient_data['last-visit-in-days'] = patient_data['last-visit-in-days'].fillna(-1).astype(int)
patient_data['bill-date'] = pd.to_datetime(patient_data['bill-date']).dt.date

# etl
patient_data['created-at'] = dt.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
patient_data['created-by'] = 'etl-automation'
patient_data['updated-at'] = dt.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
patient_data['updated-by'] = 'etl-automation'

# Write to csv
s3.save_df_to_s3(df=patient_data[table_info['column_name']], file_name='Shubham_G/43/campaign_prepost.csv')
s3.write_df_to_db(df=patient_data[table_info['column_name']], table_name=table_name, db=rs_db, schema=schema)

# remove blanks
value_q = f"""update "{schema}"."{table_name}"  
            set "value-segment" = null 
            where "value-segment" = '';
            """
rs_db.execute(value_q)

# remove blanks
behaviour_q = f"""update "{schema}"."{table_name}"  
            set "behaviour-segment" = null 
            where "behaviour-segment" = '';
            """
rs_db.execute(behaviour_q)

# closing the connection
rs_db.close_connection()
