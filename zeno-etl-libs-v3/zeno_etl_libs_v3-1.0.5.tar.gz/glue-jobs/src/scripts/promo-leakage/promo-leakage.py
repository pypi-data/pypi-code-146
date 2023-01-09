"""
Author : shubham.gupta@zeno.health
Purpose : Promo Leakage by Tech, Marketing or Category team issues
"""

# Essential Libraries
import json
from datetime import date, timedelta
# Warnings
from warnings import filterwarnings as fw

import pandas as pd

fw('ignore')

import argparse
import os
import sys

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.db.db import DB, MySQL
from zeno_etl_libs.helper.email.email import Email

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
parser.add_argument('-et', '--email_to', default="shubham.gupta@zeno.health", type=str, required=False)
parser.add_argument('-sd1', '--start_date', default=None, type=str, required=False)
parser.add_argument('-ed1', '--end_date', default=None, type=str, required=False)
parser.add_argument('-sec', '--section', default='all', type=str, required=False)

args, unknown = parser.parse_known_args()
env = args.env
os.environ['env'] = env

# parameters
email_to = args.email_to
start_date = args.start_date
end_date = args.end_date
section = args.section

if end_date is None:
    end_date = date.today()
    start_date = end_date - timedelta(days=365)

logger = get_logger()
logger.info(f"env: {env}")

rs_db = DB(read_only=True)
rs_db.open_connection()

mysql_read_db = MySQL(read_only=True)
mysql_read_db.open_connection()

s3 = S3()
read_schema = 'prod2-generico'

file_paths = []

if ('all' in section) or ('tech' in section):
    ##############################################
    ############# Tech Section ###################
    ##############################################
    # CASE1
    # Where total bill value is less than promo-min-purchase condition

    case1_t_q = f"""
                select
                    id as "bill-id",
                    "patient-id", 
                    "store-id", 
                    store as "store-name",
                    "promo-code-id", 
                    "promo-code", 
                    "promo-discount", 
                    "created-by" as "staff",
                    "total-spend" 
                    "promo-min-purchase",
                    "created-at",
                    "ecom-flag" 
                from
                    "{read_schema}"."retention-master" rm 
                where
                    "promo-min-purchase" > "total-spend" 
                    and date("bill-date") between '{start_date}' and '{end_date}';"""

    case1_t = rs_db.get_df(case1_t_q)
    case1_t_agg = case1_t.groupby(['store-name', 'ecom-flag'], as_index=False).agg({'promo-discount' : 'sum'})

    # CASE2
    # where promo total used is above max-time

    case2_t_q = f"""select
                        *
                    from
                        (
                        select
                            rm.id,
                            rm."patient-id",
                            rm."bill-date",
                            rm.store as "store-name",
                            rm."promo-discount",
                            rm."promo-code",
                            pc."max-time",
                            rm."promo-code-type",
                            rm."ecom-flag", 
                            rank() over(partition by rm."promo-code-id" order by rm."created-at") Rank_
                        from
                            "{read_schema}"."retention-master" rm
                        left join "{read_schema}"."promo-codes" pc on rm."promo-code-id" = pc.id) T
                    where
                        T.Rank_>T."max-time"
                        and DATE(T."bill-date") between '{start_date}' and '{end_date}';"""

    case2_t = rs_db.get_df(case2_t_q)
    case2_t_agg = case2_t.groupby(['store-name', 'ecom-flag'], as_index=False).agg({'promo-discount' : 'sum'})

    # CASE 3
    # where promo per-patient-total-used is above max-per-patient

    case3_t_q = f"""select
                        *
                    from
                        (
                        select
                            rm.id,
                            rm."patient-id",
                            rm."bill-date",
                            rm.store as "store-name",
                            rm."promo-discount",
                            rm."promo-code",
                            pc."max-per-patient",
                            rm."promo-code-type",
                            rm."ecom-flag", 
                            rank() over(partition by rm."patient-id", rm."promo-code-id" order by rm."created-at") Rank_
                        from
                            "{read_schema}"."retention-master" rm
                        left join "{read_schema}"."promo-codes" pc on rm."promo-code-id" = pc.id) T
                    where
                        T.Rank_>T."max-per-patient"
                        and DATE(T."bill-date") between '{start_date}' and '{end_date}';"""

    case3_t = rs_db.get_df(case3_t_q)
    case3_t_agg = case3_t.groupby(['store-name', 'ecom-flag'], as_index=False).agg({'promo-discount' : 'sum'})

    # CASE 4
    # After expiry bills
    case4_t_q = f"""
                select
                    rm.id,
                    rm."patient-id",
                    rm.store as "store-name",
                    rm."bill-date",
                    rm."promo-discount",
                    rm."promo-code",
                    pc."max-time",
                    rm."promo-code-type",
                    rm."ecom-flag",
                    pc.expiry 
                from
                    "{read_schema}"."retention-master" rm
                left join "{read_schema}"."promo-codes" pc on
                    rm."promo-code-id" = pc.id
                where
                    DATE(rm."bill-date") between '{start_date}' and '{end_date}'
                    and rm."bill-date" > DATE(pc.expiry);"""

    case4_t = rs_db.get_df(case4_t_q)
    case4_t_agg = case4_t.groupby(['store-name', 'ecom-flag'], as_index=False).agg({'promo-discount' : 'sum'})

    # Generating Excel File

    file_name = 'promo_leakage_tech_issues.xlsx'
    file_path_t = s3.write_df_to_excel(data={'bill-value > promo-min-purchase': case1_t_agg,
                                             'exceeded max limit of usage': case2_t_agg,
                                             'exceeded max-per-patient usage': case3_t_agg,
                                             'bills after promo expiry': case4_t_agg}, file_name=file_name)
    file_paths.append(file_path_t)

if ('all' in section) or ('mdm' in section):
    ##############################################
    ############# Category Section ###############
    ##############################################

    bills_q = f"""select
                    "created-at",
                    s."patient-id",
                    s."store-id",
                    s."store-name",
                    s."bill-id",
                    s."drug-id",
                    s."type-at-selling", 
                    s."type",
                    s."promo-code-id",
                    s."promo-code",
                    s."promo-discount" as "promo-spend", 
                    s.mrp * "net-quantity" as "mrp-value"
                from
                    "prod2-generico".sales s
                where
                    date(s."created-at") between '{start_date}' and '{end_date}'
                    and s."promo-discount" > 0
                    and s."code-type" != 'referral'
                    and "bill-flag" = 'gross';"""

    bills = rs_db.get_df(bills_q)

    promo_q = f"""
                SELECT
                    *
                FROM
                    `promo-codes` pc
                where
                    rules is not null
                    and date(`start`)<= '{end_date}'
                    and date(expiry)>= '{start_date}'
                    and `code-type` != 'referral';"""

    promo = pd.read_sql_query(promo_q, mysql_read_db.connection)


    def drug(x):
        try:
            return json.loads(x.decode("utf-8"))
        except:
            return []


    def burn(x):
        try:
            if x['type'] not in x['rules_drugs'][0]:
                return 'MDM_Burn'
            else:
                return 'Correct'
        except:
            return 0


    promo['rules_json'] = promo['rules'].apply(lambda x: drug(x))
    promo['rules_drugs'] = promo['rules_json'].apply(
        lambda x: [i['match-values'] for i in x if i['level'] == 'drug-type'])
    promo['rules_drugs'] = promo['rules_drugs'].apply(lambda x: [[]] if len(x) == 0 else x)
    promo.rename(columns={'id': 'promo-code-id'}, inplace=True)
    promo['rules_drugs_type'] = promo['rules_drugs'].apply(lambda x: type(x[0]))
    mdm_issue = pd.merge(bills, promo, on='promo-code-id', how='inner')
    mdm_issue['Burn'] = mdm_issue.apply(lambda x: burn(x), 1)
    mdm_issue['Burn'] = mdm_issue.apply(lambda x: 'Correct' if x['rules_drugs'] == [[]] else x['Burn'], 1)
    mdm_issue = mdm_issue[(mdm_issue['Burn'] == 'MDM_Burn')]

    # Generating excel file for mdm issues

    file_name = 'promo_leakage_mdm_issue.xlsx'
    file_path_mdm = s3.write_df_to_excel(data={'category changed later': mdm_issue}, file_name=file_name)
    file_paths.append(file_path_mdm)

if ('all' in section) or ('marketing' in section):
    ##############################################
    ############# Marketing Section ##############
    ##############################################

    # CASE 1
    # Marketing perspective
    # Assuming the latest code is the correct one, where min purchase in increased
    # So cases where min purchase was set low is promo leakage

    case1_m_q = f"""
                select
                    *
                from
                    (
                    select
                        rm.id,
                        rm."promo-code-id" as "old-promo-code-id",
                        rm."promo-code" as "old-promo-code",
                        rm."total-spend",
                        rm.store as "store-name",
                        rm."ecom-flag",
                        rm."promo-discount",
                        pc."min-purchase" as "old-min-purchase condition"
                    from
                        "prod2-generico"."retention-master" rm
                    left join "prod2-generico"."promo-codes" pc on
                        rm."promo-code-id" = pc.id
                    where
                        date(rm."created-at") between '{start_date}' and '{end_date}'
                        and rm."promo-code-id" is not null
                        and rm."promo-code-type" != 'referral') t1
                inner join 
                (
                    select
                        *
                    from
                        (
                        select
                            pc.id as "new-promo-code-id",
                            pc."promo-code" as "new-promo-code",
                            pc."min-purchase" as "new-min-purchase",
                            rank() over(partition by pc."promo-code"
                        order by
                            pc."created-at" desc) as "promo-rank"
                        from
                            "prod2-generico"."promo-codes" pc
                        where
                            "code-type" != 'referral') t2
                    where
                        t2."promo-rank" = 1) t2_2 on
                    t1."old-promo-code" = t2_2."new-promo-code"
                    and t1."old-promo-code-id" != t2_2."new-promo-code-id"
                    and t1."old-min-purchase condition" < t2_2."new-min-purchase";"""

    case1_m = rs_db.get_df(case1_m_q)
    case1_m_agg = case1_m.groupby(['store-name', 'ecom-flag'], as_index=False).agg({'promo-discount' : 'sum'})

    # CASE 2
    # Promo created again user got benefited more than how much is supposed to

    cas2_m_q = f"""
                select
                    *
                from
                    (
                    select
                        rm.id as "bill-id",
                        rm."patient-id",
                        rm."created-at",
                        rm."promo-code",
                        rm."promo-discount",
                        rm.store as "store-name",
                        rm."ecom-flag",
                        rank() over(partition by rm."patient-id",
                        rm."promo-code"
                    order by
                        rm."created-at") "promo-used-rank"
                    from
                        "prod2-generico"."retention-master" rm
                    where
                        rm."promo-code" is not null
                        and date("created-at") between '{start_date}' and '{end_date}'
                        and rm."promo-code-type" != 'referral') t1
                left join 
                (
                    select
                        *
                    from
                        (
                        select
                            pc.id as "new-promo-code-id",
                            pc."promo-code" as "new-promo-code",
                            pc."max-per-patient" as "new-max-per-patient",
                            rank() over(partition by pc."promo-code"
                        order by
                            pc."created-at" desc) as "promo-rank"
                        from
                            "prod2-generico"."promo-codes" pc
                        where
                            "code-type" != 'referral') t2
                    where
                        t2."promo-rank" = 1) t2_2 on
                    t1."promo-code" = t2_2."new-promo-code"
                where t1."promo-used-rank" > t2_2."new-max-per-patient";
                """

    case2_m = rs_db.get_df(cas2_m_q)
    case2_m_agg = case2_m.groupby(['store-name', 'ecom-flag'], as_index=False).agg({'promo-discount' : 'sum'})

    # Generating Excel for Marketing issues

    file_name = 'promo_leakage_marketing_issue.xlsx'
    file_path_m = s3.write_df_to_excel(data={'Lower min purchase limit': case1_m_agg,
                                             'Max-per-patient limit exceeded': case2_m_agg,
                                             }, file_name=file_name)
    file_paths.append(file_path_m)

if ('all' in section) or ('referral' in section):
    ##############################################
    ############# Referral Section ##############
    ##############################################

    ref_q = """	
            select
                    t1.*,
                    rm_d."patient-id" "abuser-patient-id",
                    rm_d."id" "abused-bill-id",
                    rm_d."created-at",
                    rm_d."created-by" "abuser",
                    rm_d."total-spend",
                    rm_d."redeemed-points"
                from
                    (
                    select
                        rm.store,
                        rm."created-by",
                        rm."promo-code-id",
                        count(distinct rm.id) "bill-count",
                        max(rm."created-at") "last-promo-use"
                    from
                        "prod2-generico"."retention-master" rm
                    where
                        rm."promo-code-id" is not null
                        and rm."promo-code-type" = 'referral'
                    group by
                        rm.store,
                        rm."created-by",
                        rm."promo-code-id"
                    having
                        "bill-count" = 11
                        and DATE("last-promo-use") between '2022-08-01' and '2022-08-31') t1
                left join "prod2-generico"."patients-promo-codes" ppc on
                    t1."promo-code-id" = ppc."promo-code-id"
                left join "prod2-generico"."retention-master" rm_d on
                    ppc."patient-id" = rm_d."patient-id"
                where
                    rm_d."created-at" >= t1."last-promo-use"
                    and t1."created-by" = rm_d."created-by"
                    and rm_d."redeemed-points" > 0
            """

    ref = rs_db.get_df(ref_q)
    ref_user = ref[['store', 'created-by', 'promo-code-id', 'bill-count']].drop_duplicates()
    ref_user['abused-amount'] = 51

    ref_user = ref_user.groupby(['store',
                                 'created-by'],
                                as_index=False).agg({'bill-count': 'sum',
                                                     'abused-amount': 'sum'})

    ref_owner = ref[['store', 'abuser', 'abused-bill-id', 'redeemed-points']].drop_duplicates()

    ref_owner = ref_owner.groupby(['store',
                                   'abuser'],
                                  as_index=False).agg({'abused-bill-id': 'nunique',
                                                       'redeemed-points': 'sum'})

    # Generating Excel for referral issues

    file_name = 'promo_leakage_referral_issue.xlsx'
    file_path_r = s3.write_df_to_excel(data={'ref user': ref_user,
                                             'ref_owner': ref_owner,
                                             }, file_name=file_name)
    file_paths.append(file_path_r)

mail_body = f"""
Hi,

This report contains a summary of promo leakage that happened during {start_date} and {end_date}

There are three types of promo - leakage 

1. Tech issues ( Leakage happened due to code logic/failure of logic )

2. Category issue ( Promo discount supposed to be available on some selected categories but category got changed after availing the offer; previous set category was not correct )

3. Marketing issue ( Issue where multiple times new code got introduced with some minor correction; we assumed the latest code is correct )


For each leakage, there could be obvious explanations, please provide explanations and I will iterate the logic accordingly 
1. Tech Issue 
Min-Purchase (Min-Purchase logic is failing ): 
Ecomm - {case1_t_agg[case1_t_agg['ecom-flag'] == True]['promo-discount'].sum()}
Store - {case1_t_agg[case1_t_agg['ecom-flag'] == False]['promo-discount'].sum()}
Max-time ( Max-time code use logic failure ) :
Ecomm - {case2_t_agg[case2_t_agg['ecom-flag'] == True]['promo-discount'].sum()}
Store - {case2_t_agg[case2_t_agg['ecom-flag'] == False]['promo-discount'].sum()}
Max-per-patient (Max-per-patient logic failure) :
Ecomm - {case3_t_agg[case3_t_agg['ecom-flag'] == True]['promo-discount'].sum()}
Store - {case3_t_agg[case3_t_agg['ecom-flag'] == False]['promo-discount'].sum()}
bill-after expiry ( expiry logic failed )
Ecomm - {case4_t_agg[case4_t_agg['ecom-flag'] == True]['promo-discount'].sum()}
Store - {case4_t_agg[case4_t_agg['ecom-flag'] == False]['promo-discount'].sum()}
For all ecomm cases: Tech has given the explanation that the agent has overwritten access for promo codes (in multiple scenarios they can use it ) but that will still come under leakage and can be discussed.  

2. Category issue: {mdm_issue['Burn'].sum()}

3. Marketing Issue :
Min-Purchase (Min-Purchase logic changed in latest code ): {case1_m_agg['promo-discount'].sum()}
Max-per-patient (Max-per-patient logic failure because of multiple code creation) : {case2_m_agg['promo-discount'].sum()}
**This report will be generated monthly**
Thanks & regards"""

email = Email()
email.send_email_file(subject="Promo Leakage",
                      mail_body=mail_body,
                      to_emails=email_to,
                      file_uris=[],
                      file_paths=file_paths)