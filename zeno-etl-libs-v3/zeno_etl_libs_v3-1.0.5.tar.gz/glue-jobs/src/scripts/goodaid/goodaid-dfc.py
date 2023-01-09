#!/usr/bin/env python
# coding: utf-8

#!/usr/bin/env python
# coding: utf-8
import os
import sys

sys.path.append('../../../..')

from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper.email.email import Email
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.helper import helper
from dateutil.tz import gettz
from zeno_etl_libs.logger import get_logger

import argparse
import pandas as pd
import datetime as dt
import numpy as np


parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
args, unknown = parser.parse_known_args()
env = args.env
os.environ['env'] = env


logger = get_logger()
logger.info(f"env: {env}")


rs_db = DB()
rs_db.open_connection()

rs_db_write = DB(read_only=False)
rs_db_write.open_connection()

s3 = S3()


# def main(rs_db, s3):
schema = 'prod2-generico'
table_name = 'goodaid-dfc'
table_info = helper.get_table_info(db=rs_db_write, table_name=table_name, schema=schema)

# =============================================================================
# Active Composition at warehouse
# =============================================================================
query = f'''
        select
            a."drug-id" , d.composition , d."composition-master-id" 
        from
            "prod2-generico"."prod2-generico"."wh-sku-subs-master" a
        inner join 
        "prod2-generico"."prod2-generico".drugs d on
            d.id = a."drug-id"
        where
            d."company-id" = 6984
            and a."add-wh" = 'Yes'
            and d."type" != 'discontinued-products'
        group by a."drug-id" , d.composition , d."composition-master-id"  '''

ga_active_compositions= rs_db.get_df(query)
ga_active_compositions.columns = [c.replace('-', '_') for c in ga_active_compositions.columns]

g_drugs = tuple(map(int, list(ga_active_compositions['drug_id'].unique())))
ga_active_compositions = ga_active_compositions[~ga_active_compositions['composition_master_id'].isna()]
gaid_compositions = tuple(map(str, list(ga_active_compositions['composition_master_id'].apply(pd.to_numeric, errors='ignore').astype('Int64').unique())))

logger.info("Data: ga_active_compositions, and ga_active_drugs fetched successfully: " +str(len(ga_active_compositions)))

# =============================================================================
# Net sales of GAID Drugs
# =============================================================================

query_drug_level = '''
   select
        s."store-id" ,
        s."drug-id" ,
        d."drug-name" ,
        max(gas."old-new-drug") as "goodaid-old-new-drugs",
        d.composition ,
        d."composition-master-id" ,
        SUM(s."quantity") as "total_quantity",
        SUM(s.rate * s."quantity") as "total_revenue",
        MIN(b."opened-at") as "store_opened_at"
    from
        "prod2-generico"."prod2-generico".sales s
    left join "prod2-generico"."prod2-generico".stores b
                        on
        s."store-id" = b.id
    left join "prod2-generico"."prod2-generico".drugs d 
            on
        s."drug-id" = d.id 
    left join "prod2-generico"."prod2-generico"."goodaid-atc-sr" gas 
    on
        s."drug-id" = gas."drug-id"
    where
        "bill-flag" = 'gross'
        and s."drug-id" in {}
        and s."company-id" = 6984
        and DATE(s."created-at") >= CURRENT_DATE - interval '31days'
    group by
        s."store-id" ,
        s."drug-id" ,
        d."drug-name" ,
        d."composition-master-id",
        d.composition '''

drug_sales= rs_db.get_df(query_drug_level.format(g_drugs))
drug_sales.columns = [c.replace('-', '_') for c in drug_sales.columns]
logger.info("Data: drugs sales data fetched successfully: " + str(len(drug_sales)))

# =============================================================================
# Net sales of GAID compositions
# =============================================================================
query = '''
    select
        s."store-id" ,
        d.composition ,
        d."composition-master-id" ,
        SUM(case
                        when s."company-id" = 6984 then (s."quantity")
                        else 0
                    end) as "goodaid_quantity",
        SUM(case
                        when s."type" = 'ethical' then (s."quantity")
                        else 0
                    end) as "ethical_quantity",
        SUM(case
                        when s."type" = 'generic' then (s."quantity")
                        else 0
                    end) as "total_generic_quantity",
        SUM(case
                        when s."company-id" = 6984 then (s.rate * s."quantity")
                        else 0
                    end) as "goodaid_revenue_value",
        SUM(case
                        when datediff(day, s."created-at", (current_date- 1)) <= 15 then s.quantity 
                        else 0
                    end) as "total_quantity_15d",
        SUM(case
                        when datediff(day, s."created-at", (current_date- 1)) <= 15 then (s.rate * s."quantity")
                        else 0
                    end) as "total_revenue_15d",
        SUM(case
                        when
                            s."company-id" = 6984 
                                and datediff(day, s."created-at", (current_date- 1)) <= 15
                        then
                            (s."quantity")
                        else 0
                    end) as "goodaid_quantity_15d",
        SUM(case
                        when
                            s."type" = 'ethical'
                                and datediff(day, s."created-at", (current_date- 1)) <= 15
                        then
                            (s."quantity")
                        else 0
                    end) as "ethical_quantity_15d",
        SUM(case
                        when
                           s."type" = 'generic'
                                and datediff(day, s."created-at", (current_date- 1)) <= 15
                        then
                            (s."quantity")
                        else 0
                    end) as "total_generic_quantity_15d",
        SUM(case
                        when
                            s."company-id" = 6984
                                and datediff(day, s."created-at", (current_date- 1)) <= 15
                        then
                            (s.rate * s."quantity")
                        else 0
                    end) as "goodaid_revenue_value_15"
    from
        "prod2-generico"."prod2-generico".sales s
    left join "prod2-generico"."prod2-generico".stores b
                        on
        s."store-id" = b.id
    left join "prod2-generico"."prod2-generico".drugs d 
            on
        d.id = s."drug-id" 
    where
        "bill-flag" = 'gross'
        and d."composition-master-id" in {}
        and DATE(s."created-at") >= CURRENT_DATE - interval '31days'
    group by
        s."store-id" ,
        d."composition-master-id",
        d.composition '''

first_purchase= rs_db.get_df(query.format(gaid_compositions))
first_purchase.columns = [c.replace('-', '_') for c in first_purchase.columns]
logger.info("Data: purchase data fetched successfully: " + str(len(first_purchase)))

first_purchase = drug_sales.merge(first_purchase,how = 'left', on = ['store_id','composition','composition_master_id'])

# =============================================================================
# Goodaid-comp-store first bill
# =============================================================================
query = """
     select
        "store-id" ,
        s."drug-id" ,
        min("created-at") as "ga_comp_first_bill"
    from
        "prod2-generico"."prod2-generico".sales s
    where
        s."drug-id" in {}
        and "company-id" = 6984
        and date("created-at")>= '2021-02-01'
    group by
        "store-id" ,
        s."drug-id"
            """
comp_first_b= rs_db.get_df(query.format(g_drugs))
comp_first_b.columns= [c.replace('-','_') for c in comp_first_b.columns]
logger.info("Data: comp_first_b fetched successfully: " + str(len(comp_first_b)))

first_purchase = pd.merge(left=first_purchase, right=comp_first_b, on=['store_id', 'drug_id'], how='left')


def month_diff(a, b):
    return 12 * (a.year - b.dt.year) + (a.month - b.dt.month)


first_purchase['store_age_months'] = month_diff(dt.datetime.now(), first_purchase['store_opened_at'])

first_purchase['store_type'] = np.where(first_purchase['store_age_months'] <= 3, 'new_store', 'old_store')

first_purchase['drug_age_days'] = (dt.datetime.now() - first_purchase['ga_comp_first_bill']).dt.days
first_purchase['drug_age_days'].fillna(0,inplace=True)
first_purchase['drug_type'] = np.where(first_purchase['drug_age_days'] <= 60, 'new_drug', 'old_drug')


# DFc calculation to be written post signoff from goodaid team

first_purchase['ga_share_30'] = first_purchase['total_quantity'] / (
    first_purchase['total_generic_quantity']) * 100

first_purchase['ga_share_15'] = first_purchase['goodaid_quantity_15d'] / (
    first_purchase['total_generic_quantity_15d']) * 100

first_purchase.replace([np.inf, -np.inf], 0, inplace=True)
first_purchase['ga_share_30'].fillna(0, inplace=True)
first_purchase['ga_share_15'].fillna(0, inplace=True)


# conditions = [
#     (
#             (first_purchase['store_type'] == 'old_store') &
#             (first_purchase['drug_type'] == 'old_drug') &
#             (first_purchase['ga_share_30'] >= 50)
#     ),
#     (
#             (first_purchase['store_type'] == 'old_store') &
#             (first_purchase['drug_type'] == 'old_drug') &
#             (first_purchase['ga_share_30'] < 50)
#     ),
#     (
#             (first_purchase['store_type'] == 'old_store') &
#             (first_purchase['drug_type'] == 'new_drug') &
#             (first_purchase['ga_share_15'] >= 50)
#     ),
#     (
#             (first_purchase['store_type'] == 'old_store') &
#             (first_purchase['drug_type'] == 'new_drug') &
#             (first_purchase['ga_share_15'] < 50)
#     ),
#
#     (
#             (first_purchase['store_type'] == 'new_store') &
#             (first_purchase['drug_type'] == 'new_drug')
#     ),
#     (
#             (first_purchase['store_type'] == 'new_store') &
#             (first_purchase['drug_type'] == 'old_drug')
#     )
# ]
# choices = [first_purchase['goodaid_quantity'] / 30,
#            0.5 * first_purchase['total_generic_quantity_15d'] / 15,
#            first_purchase['goodaid_quantity_15d'] / 15,
#            0.5 * first_purchase['total_generic_quantity_15d'] / 15,
#            first_purchase['total_generic_quantity_15d'] / 15,
#            first_purchase['total_generic_quantity'] / 30]


conditions = [True]
choices = [first_purchase['goodaid_quantity'] / 30]


first_purchase['dfc_val'] = np.select(conditions, choices, default=0.01)

first_purchase['dfc_val'].fillna(0.01, inplace=True)

first_purchase['dfc_val'] = np.where(first_purchase['dfc_val'] == 0, 0.01, first_purchase['dfc_val'])
logger.info("Data: first_purchase table fetched successfully: " +str(len(first_purchase)))

goodaid_dfc=first_purchase

goodaid_dfc.columns= [c.replace('_', '-') for c in goodaid_dfc.columns]
goodaid_dfc['created-at'] = dt.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
goodaid_dfc['created-by'] = 'etl-automation'
goodaid_dfc['updated-at'] = dt.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
goodaid_dfc['updated-by'] = 'etl-automation'
goodaid_dfc = goodaid_dfc.astype({'drug-age-days':'int'})
goodaid_dfc['goodaid-quantity'] = goodaid_dfc['goodaid-quantity'].fillna(0)
goodaid_dfc['ethical-quantity'] = goodaid_dfc['ethical-quantity'].fillna(0)
goodaid_dfc['total-generic-quantity'] = goodaid_dfc['total-generic-quantity'].fillna(0)
goodaid_dfc['total-quantity-15d'] = goodaid_dfc['total-quantity-15d'].fillna(0)
goodaid_dfc['goodaid-quantity-15d'] = goodaid_dfc['goodaid-quantity-15d'].fillna(0)
goodaid_dfc['ethical-quantity-15d'] = goodaid_dfc['ethical-quantity-15d'].fillna(0)
goodaid_dfc['total-generic-quantity-15d'] = goodaid_dfc['total-generic-quantity-15d'].fillna(0)
goodaid_dfc = goodaid_dfc.astype({'goodaid-quantity':'int',
                                  'ethical-quantity':'int',
                                  'total-generic-quantity':'int',
                                  'total-quantity-15d':'int',
                                  'goodaid-quantity-15d':'int',
                                  'ethical-quantity-15d':'int',
                                  'total-generic-quantity-15d':'int'})

logger.info("Data: goodaid_dfc table fetched successfully: " +str(len(goodaid_dfc)))

# =========================================================================
# Writing table in Redshift
# =========================================================================
if isinstance(table_info, type(None)):
    raise Exception(f"table: {table_name} do not exist, create the table first")
else:
    print(f"Table:{table_name} exists")
truncate_query = f''' DELETE FROM "{schema}"."{table_name}" '''
rs_db_write.execute(truncate_query)
logger.info(f"Table:{table_name} table truncated")

s3.write_df_to_db(df=goodaid_dfc[table_info['column_name']], table_name=table_name, db=rs_db_write,
                      schema=schema)

logger.info(f"Table:{table_name} table uploaded")

# Closing the DB Connection
rs_db.close_connection()