"""
purpose: pmf conversion
author : neha.karekar@zeno.health
"""

import argparse
import sys
import os

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper import helper
from zeno_etl_libs.helper.google.sheet.sheet import GoogleSheet
import pandas as pd
import dateutil
import datetime as dt
from dateutil.tz import gettz
import numpy as np

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stag, prod)")

args, unknown = parser.parse_known_args()

env = args.env
os.environ['env'] = env
logger = get_logger()

rs_db = DB()
rs_db.open_connection()

s3 = S3()

schema = 'prod2-generico'
table_name = 'pmf-conversion-table'
table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema='prod2-generico')
table_name1 = 'pmf-conversion-temp'
table_info1 = helper.get_table_info(db=rs_db, table_name=table_name1, schema='prod2-generico')

try:
        # update session id

        update_session_q = """
            select
                "session-id"
            FROM
                "prod2-generico"."pmf-conversion-table" pmf
            left join "prod2-generico"."patient-requests-metadata" prm on
                pmf."patients-store-orders-id" = prm.id
            where
                nvl(pmf."bill-id-thru-pso",
                0) != nvl(prm."bill-id",
                0)
            group by
                1
                """
        update_session = rs_db.get_df(update_session_q)

        truncate_query = f"""
                DELETE
                FROM
                    "prod2-generico"."pmf-conversion-temp"
                    """
        logger.info(truncate_query)
        rs_db.execute(truncate_query)
        s3.write_df_to_db(df=update_session[table_info1['column_name']],
                          table_name='pmf-conversion-temp',
                          db=rs_db, schema='prod2-generico')

        base_q = f"""
         select
                        ad."store-id" ,
                        ad."unique-id" as "session-id",
                        ad."patients-store-orders-id" ,
                        ad."requested-drug-id" ,
                        ad."requested-drug-name" ,
                        ad."suggested-drug-id",
                        ad."suggested-drug-name",
                        ad."patient-phone" ,ad."patient-id",
                        d2."type" as suggested_drug_type,
                        d."type" as requested_drug_type,
                        prm."bill-id" as bill_id_thru_pso ,sda."drug-id" as ass_drug,
                        ad."created-by" as "session-created-by",
                        ad."created-at" as "session-date",
                        sda."is-active" as assortment_active,
                        plt."tag" as session_source,
                        nvl(ga."generic-affinity-score",0)"generic-affinity-score" ,
                        cl."patient-phone" as called_patient,
                        max(sgdp."requested-selling-rate")"requested-drug-rate",
                        max(ad."suggested-drug-rate")"suggested-drug-rate",
                        max(ad."requested-drug-quantity")"requested-drug-quantity",
                        max(ad."suggested-drug-quantity")"suggested-drug-quantity",
                        max(ad."required-drug-quantity")"required-drug-quantity",
                        max(prm."bill-id") over (partition by ad."unique-id") as max_bill,
                        max(prm."gross-quantity") as "drug-sold",
                        max(case when b."net-payable">0 then 1 else 0 end) as "billed-same-day",
                        max(case when sa."gross-quantity">0 then 1 else 0 end) as "drug-sold-same-day",
                        max(ad."suggested-drug-inventory-quantity") "suggested-drug-inventory-quantity",
                        max(ad."requested-drug-inventory-quantity") "requested-drug-inventory-quantity",
                        max(prm."created-by") over (partition by ad."unique-id") as "max-pso-created-by"   
                        from
                        "prod2-generico"."alternate-drugs" ad
                        inner join  "prod2-generico"."pmf-conversion-temp" pct
                        on ad."unique-id"= pct."session-id"
                        left join "prod2-generico"."patient-requests-metadata" prm
                        on
                        prm.id = ad."patients-store-orders-id"
                        left join "prod2-generico".patients p
                        on right(REPLACE(REPLACE(p."phone",'.',''),' ',''), 10) = 
                        right(REPLACE(REPLACE(ad."patient-phone",'.',''),' ',''), 10)
                        left join "prod2-generico"."bills-1" b
                        on
                        b."patient-id" = (case
                        when ad."patient-id" is null then prm."patient-id"
                        when ad."patient-id" is null and prm."patient-id" is null then p.id
                        else ad."patient-id"
                        end)
                        and date(ad."created-at") = date(b."created-at")
                        left join "prod2-generico"."sales-agg" sa
                        on sa."patient-id" = (case
                        when ad."patient-id" is null then prm."patient-id"
                        when ad."patient-id" is null and prm."patient-id" is null then p.id
                        else ad."patient-id"
                        end)
                        and sa."drug-id" = prm."drug-id"
                        and date(sa."created-date") = date(ad."created-at")
                        left join "prod2-generico"."store-drug-assortment" sda 
                        on sda."store-id" = ad."store-id" and sda."drug-id" = ad."requested-drug-id"
                        and sda."is-active" =1
                        left join "prod2-generico".drugs d 
                        on d.id = ad."requested-drug-id"
                        left join "prod2-generico".drugs d2 
                        on d2.id = ad."suggested-drug-id"
                        inner join "prod2-generico"."pmf-login-tag" plt
                        on ad."created-by" = plt."login-id"
                        left join "prod2-generico"."generic-affinity" ga
                        on  ga."patient-id"=(case
                        when ad."patient-id" is null then prm."patient-id"
                        when ad."patient-id" is null and prm."patient-id" is null then p.id
                        else ad."patient-id"
                        end)
                        left join (
                                            select
                                                "drug-id" ,
                                                max("selling-rate") as "requested-selling-rate"
                                            from
                                                "prod2-generico"."store-group-drug-price" i
        
                                            group by
                                                1
                                ) sgdp on
                                ad."requested-drug-id" = sgdp."drug-id"
                                        left join (
                            select
                                right(callfrom, 10) as "patient-phone",
                                min(starttime) as "call-time"
                            from
                                "prod2-generico"."prod2-generico".exotelincomingcalllogs e
                            where
                                calltype = 'completed'
                            group by
                                1,
                                date(starttime)) cl on
                            ad."patient-phone" = cl."patient-phone"
                            and date(ad."created-at") = date(cl."call-time")
                        group by
                        ad."store-id" ,
                        ad."unique-id" ,
                        ad."patients-store-orders-id" ,
                        ad."requested-drug-id" ,
                        ad."requested-drug-name" ,
                        prm."drug-id",
                        prm."drug-name" ,
                        prm."bill-id",sda."drug-id",ga."generic-affinity-score",d."type",d2."type",
                        ad."created-by",
                        ad."suggested-drug-id",
                        ad."suggested-drug-name",
                        ad."patient-phone",
                        ad."created-at",
                        sda."is-active",
                        plt."tag",
                        cl."patient-phone" ,
                        ad."patient-id" ,
                        prm."created-by"               
                 """
        base = rs_db.get_df(base_q)
        base.columns = [c.replace('-', '_') for c in base.columns]

        base['assortment_active'].fillna(0, inplace=True)
        # assortment flag
        conditions = [(
                (base.suggested_drug_id.isnull()) &
                (base['assortment_active'] == 0)
        ),
            (
                    (base.suggested_drug_id.isnull()) &
                    (base['assortment_active'] == 1)
            ),

            (base.suggested_drug_id.notnull())
        ]
        choices = [1, 0, 0]
        base['flag_not_assort'] = np.select(conditions, choices)
        base2 = base[(base['session_id'] == '1663646353324')]
        # unavailability flag
        conditions = [
            (base['flag_not_assort'] == 1),
            (base['required_drug_quantity'] > base[
                'suggested_drug_inventory_quantity']),
            (base['required_drug_quantity'] <= base[
                'suggested_drug_inventory_quantity'])
        ]
        choices = [1, 1, 0]
        base['flag_unavailability'] = np.select(conditions, choices)

        # sessions where patient had called
        base['patient_called_flag'] = np.where(base['called_patient'].isnull(), 0, 1)

        # session converted (anyone drug converted then converted)
        base['session_conv_flag'] = np.where(base['max_bill'].isnull(), 0, 1)

        # session drug converted
        base['session_drug_conv_flag'] = np.where(base['bill_id_thru_pso'].isnull(), 0, 1)

        # drug level expensive or not
        base['drug_expensive_flag'] = np.where((base['suggested_drug_id'] != base['requested_drug_id'])
                                               & (base['suggested_drug_rate'] > base['requested_drug_rate']), 1, 0)

        session_expensive_count = base.groupby('session_id')['drug_expensive_flag'].sum().reset_index()
        session_expensive_count = session_expensive_count.rename(columns={'drug_expensive_flag': 'expensive_drugs'})

        session_not_in_assortment_count = base.groupby('session_id')['flag_not_assort'].sum().reset_index()
        session_not_in_assortment_count = session_not_in_assortment_count.rename(
            columns={'flag_not_assort': 'not_in_assortment_drugs'})

        session_drug_count = base[(base['suggested_drug_id'] != base['requested_drug_id'])].groupby('session_id')[
            'suggested_drug_id'].nunique().reset_index()
        session_drug_count = session_drug_count.rename(columns={'suggested_drug_id': 'suggested_drug_cnt'})

        session_ethical_count = base[base['requested_drug_type'] == 'ethical'].groupby('session_id')[
            'requested_drug_id'].nunique().reset_index()
        session_ethical_count = session_ethical_count.rename(columns={'requested_drug_id': 'eth_drugs'})

        session_generic_count = base[base['requested_drug_type'] == 'generic'].groupby('session_id')[
            'requested_drug_id'].nunique().reset_index()
        session_generic_count = session_generic_count.rename(columns={'requested_drug_id': 'gen_drugs'})

        session_unavailable_count = base.groupby('session_id')['flag_unavailability'].sum().reset_index()
        session_unavailable_count = session_unavailable_count.rename(columns={'flag_unavailability': 'unavailable_drugs'})

        base = pd.merge(base, session_ethical_count, how='left', on=['session_id'])
        base = pd.merge(base, session_generic_count, how='left', on=['session_id'])
        base = pd.merge(base, session_expensive_count, how='left', on=['session_id'])
        base = pd.merge(base, session_drug_count, how='left', on=['session_id'])
        base = pd.merge(base, session_not_in_assortment_count, how='left', on=['session_id'])
        base = pd.merge(base, session_unavailable_count, how='left', on=['session_id'])
        # base2=base[(base['session_id']== '1663646353324')]

        # ethical prefering session
        base['ethical_preference_issue'] = np.where(
            (base['eth_drugs'] > base['gen_drugs']) & (base['generic_affinity_score'] <= 2), 1, 0)

        # drug rate comparison
        base['rate_issue'] = np.where((base['expensive_drugs'] > 0), 1, 0)

        # assortment issue
        base['assortment_issue'] = np.where((base['not_in_assortment_drugs'] > 0), 1, 0)

        # availability issue
        base['availability_issue'] = np.where((base['unavailable_drugs'] > 0), 1, 0)

        # issue
        conditions = [
            (base['assortment_issue'] == 1),
            (base['availability_issue'] == 1),
            (base['rate_issue'] == 1),
            (base['ethical_preference_issue'] == 1)
        ]
        choices = ['assortment', 'availability', 'rate', 'ethical preference']
        base['issue'] = np.select(conditions, choices)
        base[['patients_store_orders_id', 'max_bill', 'suggested_drug_id', 'bill_id_thru_pso', 'patient_id', 'drug_sold']] = \
            base[['patients_store_orders_id', 'max_bill', 'suggested_drug_id', 'bill_id_thru_pso', 'patient_id',
                  'drug_sold']].fillna(0)

        base[
            ['patients_store_orders_id', 'max_bill', 'suggested_drug_id', 'bill_id_thru_pso', 'assortment_active', 'patient_id',
             'drug_sold']] = base[
            ['patients_store_orders_id', 'max_bill', 'suggested_drug_id', 'bill_id_thru_pso', 'assortment_active', 'patient_id',
             'drug_sold']] \
            .apply(np.int64)

        base[['patients_store_orders_id', 'max_bill', 'suggested_drug_id', 'bill_id_thru_pso', 'patient_id', 'drug_sold']] = \
            base[['patients_store_orders_id', 'max_bill', 'suggested_drug_id', 'bill_id_thru_pso', 'patient_id',
                  'drug_sold']].replace({0: None})

        base.columns = [c.replace('_', '-') for c in base.columns]
        base['etl-created-at'] = dt.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')

        # To Avoid Duplication
        truncate_query = f"""
                DELETE
                FROM
                    "prod2-generico"."pmf-conversion-table"
                    where "session-id" in 
                (select "session-id" from "prod2-generico"."pmf-conversion-temp" group by 1)
                    """
        logger.info(truncate_query)
        rs_db.execute(truncate_query)
        s3.write_df_to_db(df=base[table_info['column_name']],
                          table_name='pmf-conversion-table',
                          db=rs_db, schema='prod2-generico')

except Exception as e:
    logger.exception(e)
finally:
    rs_db.close_connection()

