"""
Author:shubham.gupta@zeno.health
Purpose: Tagging effect of campaign on customer
"""
import argparse
import os
import sys
from datetime import datetime as dt

# Model save
import joblib
import numpy as np
from dateutil.tz import gettz

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.helper import helper

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
table_name = 'campaign-uplift'

rs_db = DB()
rs_db.open_connection()

table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=read_schema)

###################################################################
###################### Model Loading ##############################
###################################################################


bucket_name = 'aws-prod-glue-assets-921939243643-ap-south-1'
s3 = S3(bucket_name=bucket_name)
file_path_control = s3.download_file_from_s3('artifact/glue-jobs/src/scripts/uplift_modelling/dt_model_control.pkl')
file_path_test = s3.download_file_from_s3('artifact/glue-jobs/src/scripts/uplift_modelling/dt_model_test.pkl')

# Load the model from the file
clf_test = joblib.load(file_path_control)
clf_control = joblib.load(file_path_test)

###################################################################
###################### Data Preparation ###########################
###################################################################

data_q = """select
                T1.*,
                T2."mean-interval",
                T2."std-interval",
                T2."cov"
            from
                (
                select
                    "patient-id",
                    current_date - max("bill-date") as "recency",
                    count(id) as "frquency",
                    avg("total-spend") as "monetary",
                    max(case when "is-generic" = true then 1 else 0 end) as "is-generic",
                    max(case when "is-chronic" = true then 1 else 0 end) as "is-chronic",
                    (case
                        when min("p-promo-min-bill-date")= min("created-at") then 1
                        else 0
                    end) "is-promo-acquired",
                    max(case when "hd-flag" = true then 1 else 0 end) "is-hd",
                    max(case when "pr-flag" = true then 1 else 0 end) "is-pr",
                    max(case when "ecom-flag" = true then 1 else 0 end) "is-ecomm",
                    avg(case when "promo-code-id" is not null then 1.0 else 0.0 end) "redemption-perc"
                from
                    "prod2-generico"."retention-master" rm
                where
                    "bill-date" <= current_date
                group by
                    "patient-id") T1
            inner join 
                (
                select
                    "x1"."patient-id" as "patient-id",
                    AVG("x1"."purchase-interval") as "mean-interval",
                    STDDEV("x1"."purchase-interval") as "std-interval",
                    STDDEV("x1"."purchase-interval") / AVG("x1"."purchase-interval") as "cov"
                from
                    (
                    select
                        "s"."patient-id" as "patient-id",
                        "s"."created-date" as "bill-date",
                        lead("s"."created-date", 1) over (partition by "s"."patient-id"
                    order by
                        "s"."created-date" desc nulls first) as "prev-bill-date",
                        "s"."created-date" - lead("s"."created-date", 1) over (partition by "s"."patient-id"
                    order by
                        "s"."created-date" desc nulls first) as "purchase-interval"
                    from
                        "prod2-generico"."sales" as "s"
                    where
                        "s"."bill-flag" = 'gross'
                        and "bill-date" <= current_date
                    group by
                        "s"."patient-id",
                        "s"."created-date"
                    order by
                        "s"."patient-id" asc nulls last,
                        "s"."created-date" asc nulls last) as "x1"
                group by
                    "x1"."patient-id") T2 on
                T1."patient-id" = T2."patient-id";"""

data = rs_db.get_df(data_q)
data = data.fillna(-1)

###################################################################
###################### Prediction #################################
###################################################################

# Use the loaded model to make predictions

data['treatment-prob'] = clf_test.predict_proba(data[data.columns[1:]])[:, 1]
data['non-treatment-prob'] = clf_control.predict_proba(data[data.columns[1:-1]])[:, 1]

data['treatment_pred'] = data['treatment-prob'] >= 0.19  # Harcode cutoff
data['non_treatment_pred'] = data['non-treatment-prob'] >= 0.26  # Hardcode cutoff

data['consumer-type'] = np.where((data['treatment_pred'] == True) & (data['non_treatment_pred'] == True), 'Sure Things',
                                 0)
data['consumer-type'] = np.where((data['treatment_pred'] == False) & (data['non_treatment_pred'] == False),
                                 'Lost Causes', data['consumer-type'])
data['consumer-type'] = np.where((data['treatment_pred'] == True) & (data['non_treatment_pred'] == False),
                                 'Persuadable', data['consumer-type'])
data['consumer-type'] = np.where((data['treatment_pred'] == False) & (data['non_treatment_pred'] == True),
                                 'Do Not Disturb', data['consumer-type'])

data_upload = data[['patient-id', 'consumer-type', 'treatment-prob', 'non-treatment-prob']]

# etl
data_upload['created-at'] = dt.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
data_upload['created-by'] = 'etl-automation'
data_upload['updated-at'] = dt.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
data_upload['updated-by'] = 'etl-automation'

# Truncating Table

if isinstance(table_info, type(None)):
    logger.info(f"table: {table_name} do not exist")
else:
    truncate_query = f"""
            DELETE
            FROM
                "{read_schema}"."{table_name}";
                """

    logger.info(f"truncate query : \n {truncate_query}")
    rs_db.execute(truncate_query)

# Write to csv
s3.save_df_to_s3(df=data_upload[table_info['column_name']],
                 file_name='campaign/campaing_uplift.csv')
s3.write_df_to_db(df=data_upload[table_info['column_name']], table_name=table_name, db=rs_db,
                  schema=read_schema)
