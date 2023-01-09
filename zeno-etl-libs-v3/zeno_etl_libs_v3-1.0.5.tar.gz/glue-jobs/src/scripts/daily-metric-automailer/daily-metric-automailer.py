"""
Author:shubham.gupta@zeno.health
Purpose: Daily Sales Dec - Sid
"""

import argparse
import os
import sys
from datetime import datetime as dt
from datetime import timedelta

import numpy as np
import pandas as pd

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.helper.email.email import Email
from zeno_etl_libs.helper.parameter.job_parameter import parameter

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
parser.add_argument('-et', '--email_to', default=["shubham.gupta@zeno.health"], type=str, required=False)
parser.add_argument('-fr', '--full_run', default=0, type=int, required=False)
args, unknown = parser.parse_known_args()
env = args.env
os.environ['env'] = env

email_to = args.email_to
logger = get_logger()

logger.info(f"env: {env}")

read_schema = "prod2-generico"

rs_db = DB()
rs_db.open_connection()

s3 = S3()

######################################################################
########################## Gross Sales ################################
######################################################################

gross_q = f"""
            select
                 b."store-id",
                 s."name" as "store-name",
                 s."franchisee-id", 
                 sum(bi.rate * bi.quantity) as "sales_e",
                 sum(case when (pc."created-by" != 'pooja.kamble@zeno.health' and pc."code-type" != 'referral' ) then bi."promo-discount" else 0 end) as "cat-promo",
                 "sales_e" - "cat-promo" as "actual-sales"
            from
                "{read_schema}"."bills-1" b
            left join "{read_schema}"."bill-items-1" bi on
                b.id = bi."bill-id"
            left join "{read_schema}"."promo-codes" pc on
                b."promo-code-id" = pc.id
            left join "{read_schema}".stores s on
                b."store-id" = s.id
            where
                date(b."created-at") = current_date - 1
            group by
                b."store-id",
                s."name",
                s."franchisee-id";
            """

gross_sales = rs_db.get_df(query=gross_q)

return_q = f"""
            select
                b."store-id", 
                s."name" as "store-name",
                s."franchisee-id", 
                sum(case
                    when (pc."created-by" != 'pooja.kamble@zeno.health'
                    and pc."code-type" != 'referral' ) then cri."return-value"
                    else (rate * "returned-quantity")
                end ) "actutal-return"
            from
                "{read_schema}"."customer-return-items-1" cri
            left join "{read_schema}"."bills-1" b on
                cri."bill-id" = b.id
            left join "{read_schema}"."promo-codes" pc on
                b."promo-code-id" = pc.id
            left join "{read_schema}".stores s on
                b."store-id" = s.id
            where
                date(cri."returned-at") = current_date - 1
            group by
                b."store-id", 
                s."name",
                s."franchisee-id";
            """

return_sales = rs_db.get_df(query=return_q)


sales = pd.merge(gross_sales, return_sales, on=['store-id', 'store-name', 'franchisee-id'], how='left')

sales.drop(columns=['sales_e', 'cat-promo'], inplace=True)
sales['net-sales'] = sales['actual-sales'] - sales['actutal-return']

file_name = 'Sales_Report.xlsx'
file_path = s3.write_df_to_excel(data={'Store_Level_Sales': sales
                                       }, file_name=file_name)

sales_body = f"""
Hey,

Here is the Daily Sales Report 
Overall Sales : {sales['net-sales'].sum()}

COCO Sales : {sales[sales["franchisee-id"]==1]['net-sales'].sum()}
FOFO Sales : {sales[sales["franchisee-id"]!=1]['net-sales'].sum()}

File can be downloaded for Store_Level Sales

Thanks

"""

email = Email()
email.send_email_file(subject=f"Sales Report Data : {dt.today().date() - timedelta(days=1)}",
                      mail_body=sales_body,
                      to_emails=email_to, file_uris=[], file_paths=[file_path])
