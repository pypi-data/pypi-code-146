
import os
import sys
import pandas as pd
import numpy as np
import datetime
import argparse

sys.path.append('../../../..')
from datetime import date
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper.email.email import Email
from zeno_etl_libs.logger import get_logger


parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
args, unknown = parser.parse_known_args()
# email_to = args.email_to
env = args.env
os.environ['env'] = env
email = Email()

logger = get_logger()

logger.info(f"env: {env}")

rs_db = DB()
rs_db.open_connection()

s3 = S3()
# Below is incentive lost automailer will run on every monday
if date.today().weekday() == 0:
    query = '''
            select
                c.abo, 
                c."store-id" as "store_id",
                sm.store as "store_name",
                sum(c."total-opportunity"-c."achived") as "missed_opportunity_yesterday",
                sum((c."total-opportunity"-c."achived")*gi.incentive ) as "missed_incentive_value_yesterday",
                s."franchisee-email" as "store_email"
            from
                (
                select
                    a.abo, 
                    a."composition",
                    a."store-id",
                    a."date",
                    a."achived",
                    b."total-opportunity"
                from
                    (
                    select
                        abo, 
                        composition ,
                        "store-id" ,
                        "date",
                        count(distinct ("patient-id" || "composition-master-id" || "group-molecule")) as "achived"
                    from
                        "prod2-generico"."prod2-generico"."goodaid-incentive-v3" a
                    where
                        "date" >= dateadd(day, -7, current_date)
                    group by
                        abo,
                        composition,
                        "store-id",
                        "date"
                    ) a
                left join (
                    select
                        abo, 
                        composition,
                        "store-id" ,
                        "date",
                        sum("actaul-total-opp") as "total-opportunity"
                    from
                        "prod2-generico"."prod2-generico"."goodaid-daily-store-opportunity" g
                    where
                        "date" >= dateadd(day, -7, current_date)
                    group by
                        abo,
                        composition,
                        "store-id" ,
                        "date") b
                    on
                    a."store-id" = b."store-id"
                    and a."composition" = b."composition"
                    and a."date" = b."date") c
                left join "prod2-generico"."prod2-generico"."goodaid-incentive-rate-card" gi	on 
                c.composition= gi.composition
                left join "prod2-generico"."prod2-generico"."stores-master" sm on 
                c."store-id"=sm.id 
                left join "prod2-generico"."prod2-generico".stores s on 
                c."store-id" = s.id 
                    where gi.status = 'live'
                    and sm."franchisee-id" = 1
                    and c.abo is not null
            group by
                c.abo, c."store-id", store, s."franchisee-email" 
            having missed_opportunity_yesterday >=0
            order by abo; '''
    incentive_data = rs_db.get_df(query)

    # MTD incentive miss data
    query = '''
            select
                c.abo, 
                c."store-id" as "store_id",
                sm.store as "store_name",
                sum(c."total-opportunity"-c."achived") as "missed_opportunity_MTD",
                sum((c."total-opportunity"-c."achived")*gi.incentive ) as "missed_incentive_value_MTD",
                s."franchisee-email" as "store_email"
            from
                (
                select
                    a.abo, 
                    a."composition",
                    a."store-id",
                    a."date",
                    a."achived",
                    b."total-opportunity"
                from
                    (
                    select
                        abo, 
                        composition ,
                        "store-id" ,
                        "date",
                        count(distinct ("patient-id" || "composition-master-id" || "group-molecule")) as "achived"
                    from
                        "prod2-generico"."prod2-generico"."goodaid-incentive-v3" a
                    where
                        "date" > DATE_TRUNC('day', dateadd(day, -(extract(day from current_date)), current_date))
                    group by
                        abo,
                        composition,
                        "store-id",
                        "date"
                    ) a
                left join (
                    select
                        abo, 
                        composition,
                        "store-id" ,
                        "date",
                        sum("actaul-total-opp") as "total-opportunity"
                    from
                        "prod2-generico"."prod2-generico"."goodaid-daily-store-opportunity" g
                    where
                        "date" > DATE_TRUNC('day', dateadd(day, -(extract(day from current_date)), current_date))
                    group by
                        abo,
                        composition,
                        "store-id" ,
                        "date") b
                    on
                    a."store-id" = b."store-id"
                    and a."composition" = b."composition"
                    and a."date" = b."date") c
                left join "prod2-generico"."prod2-generico"."goodaid-incentive-rate-card" gi	on 
                c.composition= gi.composition
                left join "prod2-generico"."prod2-generico"."stores-master" sm on 
                c."store-id"=sm.id 
                left join "prod2-generico"."prod2-generico".stores s on 
                c."store-id" = s.id 
                    where gi.status = 'live'
                    and sm."franchisee-id" = 1
                    and c.abo is not null
            group by
                c.abo, c."store-id", store, s."franchisee-email"
            having missed_opportunity_MTD >=0
            order by abo;  '''
    incentive_data_mtd = rs_db.get_df(query)

    incentive_data = incentive_data.merge(incentive_data_mtd, on=['abo', 'store_id', 'store_name',
                                                                  'store_email'], how='left')

    # last month incentive miss data
    query = '''
            select
                c.abo, 
                c."store-id" as "store_id",
                sm.store as "store_name",
                sum(c."total-opportunity"-c."achived") as "missed_opportunity_lm",
                sum((c."total-opportunity"-c."achived")*gi.incentive ) as "missed_incentive_value_lm",
                s."franchisee-email" as "store_email"
            from
                (
                select
                    a.abo, 
                    a."composition",
                    a."store-id",
                    a."date",
                    a."achived",
                    b."total-opportunity"
                from
                    (
                    select
                        abo, 
                        composition ,
                        "store-id" ,
                        "date",
                        count(distinct ("patient-id" || "composition-master-id" || "group-molecule")) as "achived"
                    from
                        "prod2-generico"."prod2-generico"."goodaid-incentive-v3" a
                    where
                        "date" between date_trunc('month', current_date) - interval '1 month' and date_trunc('month', current_date) - interval '1 day'
                    group by
                        abo,
                        composition,
                        "store-id",
                        "date"
                    ) a
                left join (
                    select
                        abo, 
                        composition,
                        "store-id" ,
                        "date",
                        sum("actaul-total-opp") as "total-opportunity"
                    from
                        "prod2-generico"."prod2-generico"."goodaid-daily-store-opportunity" g
                    where
                        "date" between date_trunc('month', current_date) - interval '1 month' and date_trunc('month', current_date) - interval '1 day'
                    group by
                        abo,
                        composition,
                        "store-id" ,
                        "date") b
                    on
                    a."store-id" = b."store-id"
                    and a."composition" = b."composition"
                    and a."date" = b."date") c
                left join "prod2-generico"."prod2-generico"."goodaid-incentive-rate-card" gi	on 
                c.composition= gi.composition
                left join "prod2-generico"."prod2-generico"."stores-master" sm on 
                c."store-id"=sm.id 
                left join "prod2-generico"."prod2-generico".stores s on 
                c."store-id" = s.id 
                    where gi.status = 'live'
                    and sm."franchisee-id" = 1
                    and c.abo is not null
            group by
                c.abo, c."store-id", store, s."franchisee-email"
            having missed_opportunity_lm >=0
            order by abo '''
    incentive_data_lm = rs_db.get_df(query)

    incentive_data = incentive_data.merge(incentive_data_lm, on=['abo', 'store_id', 'store_name', 'store_email'],
                                          how='left')

    query = '''
            select
                abo,
                email
            from
                "prod2-generico"."prod2-generico"."stores-master" sm
            left join "prod2-generico"."prod2-generico".users u on
                sm.abo = u."name"
            where abo is not null
                and u."type" = 'area-business-owner'
            group by
                1,2
            order by abo'''
    abo_data = rs_db.get_df(query)

    incentive_data = incentive_data.merge(abo_data, how='left', on='abo')
    incentive_data = incentive_data[incentive_data['email'].notna()]
    abo_list = incentive_data.abo.unique()
    abo_list = tuple(abo_list)
    store_list = incentive_data.store_name.unique()
    store_list = tuple(store_list)

    now = datetime.date.today()
    then = now + datetime.timedelta(days=-7)
    currentMonth = datetime.datetime.now().strftime('%m')
    currentYear = datetime.datetime.now().year
    datetime_object = datetime.datetime.strptime(currentMonth, "%m")
    full_month_name = datetime_object.strftime("%B")
    last_month = datetime.datetime.now() - pd.DateOffset(months=1)
    last_month = last_month.strftime('%m')
    datetime_object_lm = datetime.datetime.strptime(last_month, "%m")
    full_month_name_lm = datetime_object_lm.strftime("%B")

    for x in abo_list:
        incentive_data_1 = incentive_data[incentive_data['abo'] == x]
        abo_incentive_data = incentive_data_1.groupby(['abo', 'store_name', 'store_id']).agg(
            {'missed_incentive_value_yesterday': 'sum', 'missed_incentive_value_mtd': 'sum', \
             'missed_incentive_value_lm': 'sum'}).reset_index()
        abo_incentive_data[
            ["missed_incentive_value_yesterday", "missed_incentive_value_mtd", "missed_incentive_value_lm"]] = \
        abo_incentive_data[["missed_incentive_value_yesterday",\
                            "missed_incentive_value_mtd", "missed_incentive_value_lm"]].astype(np.int64)
        total_incentive_missed = abo_incentive_data.missed_incentive_value_yesterday.sum()
        abo_incentive_data.rename(columns={'missed_incentive_value_yesterday': f'Lost incentive last week(Rs)-{then}', \
                                           'missed_incentive_value_mtd': f'Lost incentive (Rs) MTD {full_month_name}-{currentYear}', \
                                           'missed_incentive_value_lm': f'Lost incentive (Rs) last Month {full_month_name_lm}-{currentYear}', \
                                           'store_name': f'Store Name', 'store_id': f'Store ID'}, inplace=True)
        email_to = str(incentive_data_1.email.iloc[0])
        # Sending email
        subject = f'Rs.{total_incentive_missed} Incentive Lost Last Week'
        mail_body = f" Hi {(abo_incentive_data.abo.iloc[0])} your stores have lost Rs.{total_incentive_missed} last week " \
                    f"({str(then)}) by not substituting GoodAid drugs in your stores. \
        Please try and substitute Goodaid as much as possible to earn maximum incentive."
        file_uris = [s3.save_df_to_s3(df=abo_incentive_data,
                                      file_name=f'{incentive_data_1.abo.iloc[0]} total incentive Loss on {now}.csv')]
        email.send_email_file(subject=subject, mail_body=mail_body, to_emails=email_to, file_uris=file_uris)

        # deleteing the old files
        for uri in file_uris:
            s3.delete_s3_obj(uri=uri)

    for x in store_list:
        incentive_data_2 = incentive_data[incentive_data['store_name'] == x]
        store_incentive_data = incentive_data_2.groupby(['abo', 'store_name', 'store_id']).agg(
            {'missed_incentive_value_yesterday': 'sum', 'missed_incentive_value_mtd': 'sum', \
             'missed_incentive_value_lm': 'sum'}).reset_index()
        store_incentive_data[
            ["missed_incentive_value_yesterday", "missed_incentive_value_mtd", "missed_incentive_value_lm"]] = \
        store_incentive_data[["missed_incentive_value_yesterday", \
                              "missed_incentive_value_mtd", "missed_incentive_value_lm"]].astype(np.int64)
        email_to = str(incentive_data_2.store_email.iloc[0])
        # Sending email
        subject = f'Rs.{(store_incentive_data.missed_incentive_value_yesterday.iloc[0])} Incentive Lost Yesterday'
        mail_body = f" Hi {(store_incentive_data.store_name.iloc[0])} store you have lost Rs.{(store_incentive_data.missed_incentive_value_yesterday.iloc[0])} last week ({str(then)})\
         by not substituting GoodAid drugs in your store. Please try and substitute Goodaid as much as possible to earn maximum incentive."
        store_incentive_data.rename(columns={'missed_incentive_value_yesterday': f'Lost incentive last week(Rs)-{then}',
                                             'missed_incentive_value_mtd': f'Lost incentive (Rs) MTD '
                                                                           f'{full_month_name}-{currentYear}', \
                                             'missed_incentive_value_lm': f'Lost incentive (Rs) last Month '
                                                                          f'{full_month_name_lm}-{currentYear}',
                                             'store_name': f'Store Name', 'store_id': f'Store ID'}, inplace=True)
        file_uris = [s3.save_df_to_s3(df=store_incentive_data,
                                      file_name=f'{incentive_data_2.store_name.iloc[0]} total incentive Loss on {now}.csv')]
        email.send_email_file(subject=subject, mail_body=mail_body, to_emails=email_to, file_uris=file_uris)

        # deleteing the old files
        for uri in file_uris:
            s3.delete_s3_obj(uri=uri)


# 2nd automailer for new stock at stores this runs everyday.
query = '''
        select
            i."store-id" as "store_id" ,
            s."name" as "store_name",
            i."drug-id"  as "drug_id",
            d."drug-name" as "drug_name", 
            d.composition , 
            d.company ,
            s."franchisee-email" as "email", 
            sum(i.quantity+i."locked-quantity"+i."locked-for-check"+i."locked-for-return"+i."locked-for-audit"+
            i."locked-for-transfer") as "quantity_available_at_store"
        FROM
            "prod2-generico"."prod2-generico"."inventory-1" i 
        inner join "prod2-generico"."prod2-generico".drugs d on d.id = i."drug-id"  
        left join "prod2-generico"."prod2-generico".stores s on i."store-id" = s.id 
        where d."company-id"  = 6984
        and s."franchisee-id" =1
        GROUP by
            1,2,3,4,5,6,7
        HAVING
            min(date(i."created-at")) = CURRENT_DATE-1 '''
new_drug_data = rs_db.get_df(query)

store_list = new_drug_data.store_name.unique()
store_list = tuple(store_list)
nl = '\n'
now = datetime.date.today()

if len(new_drug_data) > 0:
    for x in store_list:
        store_drug_data = new_drug_data[new_drug_data['store_name'] == x]
        store_drug_data_1 = store_drug_data[['store_id', 'store_name', 'drug_id', 'drug_name', 'composition', 'company',
                                             'quantity_available_at_store']].reset_index(drop = True)
        email_to = str(store_drug_data.email.iloc[0])
        # email_to = 'sanjay.bohra@zeno.health'
        subject = f'{len(store_drug_data)} New Goodaid Drugs Arrived at your Store'
        mail_body = f" Hi {(store_drug_data_1.store_name.iloc[0])} store {nl}{len(store_drug_data)} New Goodaid SKU/Drugs " \
                    f"have arrived at your store please start substituting."
        file_uris = [s3.save_df_to_s3(df=store_drug_data_1, file_name=f'{store_drug_data_1.store_name.iloc[0]} '
                                                                        f'drugs arrived at {now}.csv')]
        email.send_email_file(subject=subject, mail_body=mail_body, to_emails=email_to, file_uris=file_uris, from_email='data-goodaid@zeno.health')

        # deleteing the old files
        for uri in file_uris:
            s3.delete_s3_obj(uri=uri)
        # Closing the DB Connection
        rs_db.close_connection()