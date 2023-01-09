"""
Author:shubham.gupta@zeno.health
Purpose: Diagnostic Data Visibility
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
from dateutil.tz import gettz

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
parser.add_argument('-et', '--email_to', default="shubham.gupta@zeno.health", type=str, required=False)
args, unknown = parser.parse_known_args()
env = args.env
os.environ['env'] = env

email_to = args.email_to
logger = get_logger()

logger.info(f"env: {env}")

read_schema = 'prod2-generico'
table_name = 'diagnostic-visibility'

rs_db = DB()
rs_db.open_connection()

end = dt.now().date()
start = end - timedelta(days=15)

s3 = S3()

table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=read_schema)

if isinstance(table_info, type(None)):
    logger.info(f"table: {table_name} do not exist")
else:
    truncate_query = f''' DELETE FROM "{read_schema}"."{table_name}" 
                    WHERE "date" BETWEEN '{start}' and '{end}' '''
    logger.info(truncate_query)
    rs_db.execute(truncate_query)

diagnostics_q = f"""
select
                   distinct *
                from
                    (
                    select
                        d1."cash-payment",
                        d2.*,
                        rcrm.comments,
                        zer."reason-name",
                        zer."type" as "reason-type",
                        test."number-of-tests",
                        test."booking-at",
                        sm.store,
                        sm.city,
                        sm.line,
                        sm.abo,
                        sm."store-manager",
                        acq."acq-medium",
                        (case
                            when d2.status in ('REDEMPTION', 'COMPLETED') then 1
                            else 0
                        end ) "red-com",
                        sum("red-com") over (partition by d2."patient-id"
                    order by
                        d2."date",
                        d2."redemption-id" rows unbounded preceding) as nodo
                        
                    from
                    (
                        select
                            r.id as "redemption-id",
                            r."patient-id",
                            r."source",
                            r."status",
                            r."store-id",
                            r."total-amount" as "total-sales",
                            r."redeemed-value" as "reward-payment",
                            date(r."created-at") as date,
                            r."call-status",
                            r."created-by" as pharmacist
                        from
                            "prod2-generico".redemption r) d2
                            left join 
                        (
                        select
                            rp."redemption-id",
                            SUM(case when rp."payment-type" in ('CASH', 'LINK') then rp.amount else 0 end) "cash-payment"
                        from
                            "prod2-generico"."redemption-payments" rp
                        group by
                            rp."redemption-id") d1
                            on

                        d2."redemption-id" = d1."redemption-id"
                    left join "prod2-generico"."redemption-cancellation-reason-mapping" rcrm on
                        rcrm."redemption-id" = d2."redemption-id"
                    left join "prod2-generico"."zeno-escalation-reason" zer on
                        rcrm."redemption-cancellation-reason-id" = zer.id
                    left join (
                        select
                            rs."redemption-id",
                            count(distinct rs."sku-id") as "number-of-tests",
                            max(rs."slot-date") as "booking-at"
                        from
                            "prod2-generico"."redemption-skus" rs
                        left join "prod2-generico"."reward-product" rp on
                            rs."sku-id" = rp.id
                        group by
                            rs."redemption-id") test on
                        d2."redemption-id" = test."redemption-id"
                    left join "prod2-generico"."stores-master" sm on
                        d2."store-id" = sm.id
                    left join (
                        select
                            r."patient-id",
                            (case
                                when (MIN(DATE(r."redemption-date")) - MIN(DATE(b."created-at"))) > 0 
                        then 'drug_store'
                                when (MIN(DATE(r."redemption-date")) - MIN(DATE(b."created-at"))) < 0 
                        then 'diagnostic'
                                else 'diagnostic_no_visit_store'
                            end ) "acq-medium"
                        from
                            "prod2-generico".redemption r
                        left join "prod2-generico"."bills-1" b on
                            r."patient-id" = b."patient-id"
                        where
                            r.status in ('REDEMPTION', 'COMPLETED')
                        group by
                            r."patient-id") acq on
                        d2."patient-id" = acq."patient-id") X
                where
                    X."date" between '{start}' and '{end}';
                """
diagnostics = rs_db.get_df(diagnostics_q)

diagnostics['store-id'] = diagnostics['store-id'].fillna(0)

diagnostics['source'] = diagnostics['source'].map({'OPS_DASHBOARD': 'OPS Oracle',
                                                   'LOYALTY_UI': 'App',
                                                   'STORE': 'Store'})
# datatype correction
diagnostics['number-of-tests'] = diagnostics['number-of-tests'].fillna(0)
diagnostics['number-of-tests'] = diagnostics['number-of-tests'].astype(int)
diagnostics['cash-payment'] = diagnostics['cash-payment'].astype(float)
diagnostics['store-id'] = diagnostics['store-id'].astype(int)
diagnostics['total-sales'] = diagnostics['total-sales'].astype(float)
diagnostics['reward-payment'] = diagnostics['reward-payment'].astype(float)

# etl
diagnostics['created-at'] = dt.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
diagnostics['created-by'] = 'etl-automation'
diagnostics['updated-at'] = dt.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
diagnostics['updated-by'] = 'etl-automation'

# Write to csv
s3.save_df_to_s3(df=diagnostics[table_info['column_name']], file_name='data.csv')
s3.write_df_to_db(df=diagnostics[table_info['column_name']], table_name=table_name, db=rs_db, schema=read_schema)

# closing the connection
rs_db.close_connection()
