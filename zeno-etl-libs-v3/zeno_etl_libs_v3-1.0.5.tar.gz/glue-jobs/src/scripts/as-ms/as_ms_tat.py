# Taking Lot of time while applying the function
# Need to Optimise it Or Add SLA's In Shortbook only

import os
import sys

sys.path.append('../../../..')

from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper.email.email import Email
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.config.common import Config
from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper import helper
from dateutil.tz import gettz

import json
import datetime

import argparse
import pandas as pd
import numpy as np
import traceback
import calendar

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
parser.add_argument('-et', '--email_to', default="saurav.maskar@zeno.health", type=str, required=False)
args, unknown = parser.parse_known_args()
env = args.env
email_to = args.email_to

os.environ['env'] = env

logger = get_logger(level='INFO')

logger.info(f"env: {env}")

rs_db = DB()
rs_db.open_connection()

rs_db_write = DB(read_only=False)
rs_db_write.open_connection()

s3 = S3()
start_time = datetime.datetime.now()
logger.info('Script Manager Initialized')
logger.info("")
logger.info("parameters reading")
logger.info(f"env: {env}")
logger.info("email_to - " + email_to)
logger.info("")

# date parameter
logger.info("code started at {}".format(datetime.datetime.now().strftime(
    '%Y-%m-%d %H:%M:%S')))
logger.info("")

cur_date = datetime.datetime.now(tz=gettz('Asia/Kolkata')).date()

sla_input = pd.read_csv(s3.download_file_from_s3(file_name="SLA/SLA_Format.csv"))

sla_input["order_time"] = pd.to_datetime(sla_input["order_time"], format='%I:%M:%S %p').dt.time
sla_input['invoice_time'] = pd.to_datetime(sla_input['invoice_time'], format='%I:%M:%S %p').dt.time
sla_input['dispatch_time'] = pd.to_datetime(sla_input['dispatch_time'], format='%I:%M:%S %p').dt.time
sla_input['delivery_time'] = pd.to_datetime(sla_input['delivery_time'], format='%I:%M:%S %p').dt.time
sla_input['reorder_time'] = pd.to_datetime(sla_input['reorder_time'], format='%I:%M:%S %p').dt.time
sla_input['store_id'] = sla_input['store_id'].astype(str)
sla_input['city_id'] = sla_input['city_id'].astype(str)

sla_input['city_id'] = sla_input['city_id'].str.split('-')
sla_input = sla_input.explode('city_id')

sla_input['store_id'] = sla_input['store_id'].str.split('-')
sla_input = sla_input.explode('store_id')

sla_input['store_id'] = sla_input['store_id'].astype(int)
sla_input['city_id'] = sla_input['city_id'].astype(int)

as_ms_query = '''
        select
              a.id as "short-book-id",
               a."patient-id",
            getdate() as "refreshed_at",
            a."store-name" as "store-name",
            sm."franchisee-name" as "franchisee-name",
            a."drug-name" as "drug-name",
            a."as-ms" as "AS/MS",
            a."status" as "sb-status",
            a."requested-quantity" as "requested-quantity",
            a."quantity" as "quantity",
            a."required-quantity" as "required-quantity",
            a."created-at",
            Date(a."ordered-time") as "ordered-at",
            Date(a."invoiced-at") as "invoiced-at",
            Date(a."dispatched-at") as "Dispatched-at",
            Date(a."store-delivered-at") as "received-at",
            Date(a."completed-at") as "completed-at",
            Date(a."delivered-at") as "delivered-at",
            a."created-at" as "created-time",
            a."ordered-time" as "ordered-time",
            a."invoiced-at" as "invoiced-time",
            a."dispatched-at" as "dispatch-time",
            a."delivered-at" as "delivered-time",
            a."completed-at" as "completed-time",
            a."decline-reason" as "decline reason",
            a."re-ordered-at" as "re-ordered-at",
            a."type",
            a."store-id",
            a."drug-id",
            a."company",
            a."preferred-distributor-name" as "preferred dist",
            a."drug-grade",
            '' as "distributor type",
            a."preferred-distributor-id" as "preferred-distributor-id",
            a."received-distributor-name" as "received distributor",
            a."recieved-distributor-id",
            sm."old-new-static" as "store-type",
            a."forward-dc-id",
            a."dc-name" as "dc_name",
            a."store-delivered-at" as "store_received_at",
            a."purchase-rate" as "purchase-rate",
            sm."line-manager" as "line_manager",
            sm.abo,
            sm.city as "city-store-master",
            zc."name" as "city",
            s."city-id",
            sm."store-b2b" as "store_b2b",
            s."franchisee-id" as "franchise_id",
            case when s."franchisee-id"=1 then 'COCO' 
            when s."franchisee-id"!= 1 then 'FOFO' 
            else 'default' end as "franchisee_flag",
            sm."franchisee-name" as "franchise_name",
            sm."opened-at",
            a."franchisee-short-book" ,
            bl."buyer-name" as "Buyer",
            sbol."status-log",
                case
                    when sbol."status-log" in ('presaved,lost') then 'FOFO-partner-rejected'
                else a.status
            end as "status",
                fofo_approved_at."presaved_approved_at"
        from
            "prod2-generico"."as-ms" a
        left join "prod2-generico"."stores-master" sm
                      on
            sm.id = a."store-id"
        left join "prod2-generico"."buyer-store-mapping" bsm
                      on
            bsm."store-id" = a."store-id"
        left join "prod2-generico"."buyers-list" bl
                      on
            bl.id = bsm."buyer-id"
        left join "prod2-generico".stores s 
                     on
            s.id = a."store-id"
        left join "prod2-generico"."zeno-city" zc 
                     on
            zc.id = s."city-id"
        left join(
            select
                            sbol."short-book-id" ,
                            listagg(distinct sbol.status,
                ',') within group (
                order by sbol.id) as "status-log"
            from
                            "prod2-generico"."short-book-order-logs" sbol
            left join "prod2-generico"."prod2-generico"."short-book-1" sb 
                        on
                sbol."short-book-id" = sb.id
            where
                Date(sb."created-at") >= date(date_trunc('month', current_date) - interval '2 month')
            group by
                            sbol."short-book-id") sbol 
                    on
            a.id = sbol."short-book-id"
        left join (
            select
                            sbol."short-book-id" ,
                            min(sbol."created-at") as "presaved_approved_at"
            from
                            "prod2-generico"."prod2-generico"."short-book-order-logs" sbol
            left join "prod2-generico"."prod2-generico"."short-book-1" sb2 
                            on
                            sb2.id = sbol."short-book-id"
            left join "prod2-generico"."prod2-generico".stores s2 
                            on
                            s2.id = sb2."store-id"
            where
                            s2."franchisee-id" != 1
                and sbol.status not in ('presaved', 'lost', 'failed', 'declined', 'deleted')
            group by
                            sbol."short-book-id"
                        )fofo_approved_at
                    on
            fofo_approved_at."short-book-id" = a.id
        where
            Date(a."created-at") >=  date(date_trunc('month', current_date) - interval '1 day')
        '''
data = rs_db.get_df(as_ms_query)

logger.info('fetched data')

class As_ms_tat:
    def __init__(self,sla_input_main):
        self.sla_input_main = sla_input_main

    def weekday_calender(self,day):
        if day == 0 :
            return 'Monday'
        elif day == 1:
            return 'Tuesday'
        elif day ==2:
            return 'Wednesday'
        elif day == 3:
            return 'Thursday'
        elif day==4:
            return 'Friday'
        elif day == 5:
            return 'Saturday'
        elif day == 6:
            return 'Sunday'

    def timecheck(self, start_time_sla, end_time_sla, check_time):
        if str(start_time_sla) == '0' or str(end_time_sla) == '0':
            return 'default_time'

        start_time_sla = datetime.datetime.strptime(start_time_sla, '%I:%M:%S %p').time()
        end_time_sla = datetime.datetime.strptime(end_time_sla, '%I:%M:%S %p').time()

        if check_time >= start_time_sla and check_time <= end_time_sla:
            return 'time_found'
        else:
            return 'time_not_found'

    def tat_sla_calculator(self,created_time, pre_saved_approved_at_time,store_id, franchisee, city_id, distributor_id, drug_type):

        print(1)
        # print(1) np.where, CFR_PR, Np.select
        if franchisee == 'COCO':
            start_time = created_time
        else:
            start_time = pre_saved_approved_at_time

        if pd.isnull(start_time) or start_time is pd.NaT:
            return pd.NaT, pd.NaT, pd.NaT, pd.NaT, pd.NaT, None
        else:
            start_time = pd.to_datetime(start_time)

        sla_input = self.sla_input_main.copy(deep = True)
        store_parameter = False

        # start_time = datetime.datetime.strptime(start_time , '%Y-%m-%d %H:%M:%S')
        day_in_number = start_time.weekday()
        day = self.weekday_calender(day_in_number)

        if franchisee in sla_input['franchisee_flag'].unique():
            franchisee = franchisee
        else:
            franchisee = 'default'

        sla_input = sla_input[((sla_input['franchisee_flag'] == franchisee) & (sla_input['day'] == day))]

        if city_id in sla_input['city_id'].unique():
            city = city_id
        else:
            city = 0

        # city = 0
        # for city_ids in sla_input['city_id'].unique():
        #     if str(city_id) in (str(city_ids).split('-')):
        #         city = city_ids
        #         city_parameter = True
        #         break

        if store_id in sla_input['store_id'].unique():
            store = 0
        else:
            store = 0

        # store = 0
        # for store_ids in sla_input['store_id'].unique():
        #     if str(store_id) in (str(store_ids).split('-')):
        #         store = store_ids
        #         store_parameter = True
        #         break

        if store_parameter:
            city = 0

        sla_input = sla_input[((sla_input['store_id'] == (store)) & (sla_input['city_id'] == (city)))]

        if drug_type in sla_input['drug_type'].unique():
            drug_type = drug_type
        else:
            drug_type = 'default'

        sla_input = sla_input[((sla_input['drug_type'] == (drug_type)))]

        if int(distributor_id) == 8105:
            distributor = 'WH'
        else:
            distributor = 'DC'

        if distributor in sla_input['distributor_name'].unique():
            distributor = distributor
        else:
            distributor = 'default'

        sla_input = sla_input[((sla_input['distributor_name'] == (distributor)))]

        # print(2)

        if len(sla_input)>1:
            sla_input['timecheck'] = np.vectorize(self.timecheck)(sla_input['start_time'], sla_input['end_time'], start_time.time())

            if 'time_found' in sla_input['timecheck'].unique():
                sla_input = sla_input[sla_input['timecheck']=='time_found']
            else:
                sla_input = sla_input[sla_input['timecheck']=='default_time']

        sla_input = sla_input.reset_index(drop=True)

        order_date = sla_input.loc[0, 'order_date']
        order_time = sla_input.loc[0, 'order_time']

        order_sla = start_time + datetime.timedelta(days=int(order_date))

        order_sla = order_sla.replace(hour=order_time.hour, minute=order_time.minute, second=order_time.second)

        invoice_date = sla_input.loc[0, 'invoice_date']
        invoice_time = sla_input.loc[0, 'invoice_time']

        invoice_sla = start_time + datetime.timedelta(days=int(invoice_date))

        invoice_sla = invoice_sla.replace(hour=invoice_time.hour, minute=invoice_time.minute,
                                          second=invoice_time.second)

        dispatch_date = sla_input.loc[0, 'dispatch_date']
        dispatch_time = sla_input.loc[0, 'dispatch_time']

        dispatch_sla = start_time + datetime.timedelta(days=int(dispatch_date))

        dispatch_sla = dispatch_sla.replace(hour=dispatch_time.hour, minute=dispatch_time.minute,
                                            second=dispatch_time.second)

        delivery_date = sla_input.loc[0, 'delivery_date']
        delivery_time = sla_input.loc[0, 'delivery_time']

        delivery_sla = start_time + datetime.timedelta(days=int(delivery_date))

        delivery_sla = delivery_sla.replace(hour=delivery_time.hour, minute=delivery_time.minute,
                                            second=delivery_time.second)

        reorder_date = sla_input.loc[0, 'reorder_date']
        reorder_time = sla_input.loc[0, 'reorder_time']

        reorder_sla = start_time + datetime.timedelta(days=int(reorder_date))

        reorder_sla = reorder_sla.replace(hour=reorder_time.hour, minute=reorder_time.minute,
                                          second=reorder_time.second)
        # print(4)

        return order_sla, invoice_sla, dispatch_sla, delivery_sla, reorder_sla,sla_input.loc[0, 'id']

    def tat_checker(self,ordered_at,order_sla):

        if pd.isnull('ordered_at') or ordered_at is pd.NaT or ordered_at is None:
            return 'Pending'
        elif order_sla<=ordered_at:
            return 'ontime'
        else:
            return 'delayed'

as_ms_tat= As_ms_tat(sla_input)

data['recieved-distributor-id'] = data['recieved-distributor-id'].fillna(0)
#
# logger.info('apply')
#
# data['order_sla'],data['invoice_sla'],data['dispatch_sla'],data['delivery_sla'],data['reorder_sla'],data['sla_id']  = data.apply(lambda x: as_ms_tat.tat_sla_calculator(x['created-at'], x['presaved_approved_at'], x['store-id'], x['franchisee_flag'], x['city-id'],x['recieved-distributor-id'],x['type']), axis=1)

logger.info('vectorise')

data['order_sla'],data['invoice_sla'],data['dispatch_sla'],data['delivery_sla'],data['reorder_sla'],data['sla_id']  = np.vectorize(as_ms_tat.tat_sla_calculator)(data['created-at'], data['presaved_approved_at'], data['store-id'], data['franchisee_flag'], data['city-id'],data['recieved-distributor-id'],data['type'])

logger.info('fetched SLA Timelines')

data['ordered timing'] = np.vectorize(as_ms_tat.tat_checker)(data['ordered-time'], data['order_sla'])
data['fullfilment on invoice'] = np.vectorize(as_ms_tat.tat_checker)(data['invoiced-time'], data['invoice_sla'])
data['fullfilment on dispatch'] = np.vectorize(as_ms_tat.tat_checker)(data['dispatch-time'], data['dispatch_sla'])
data['fullfilment on delivery'] = np.vectorize(as_ms_tat.tat_checker)(data['store_received_at'], data['delivery_sla'])
data['re-order timing'] = np.vectorize(as_ms_tat.tat_checker)(data['re-ordered-at'], data['reorder_sla'])

logger.info('fetched SLA ')
# =============================================================================
# writing to Redshift
# =============================================================================
schema = 'prod2-generico'
table_name = 'as-ms-tat'
table_info = helper.get_table_info(db=rs_db_write, table_name=table_name, schema=schema)
status2 = False

if isinstance(table_info, type(None)):
    raise Exception(f"table: {table_name} do not exist, create the table first")
else:
    logger.info(f"Table:{table_name} exists")

    truncate_query = f''' delete
                        from "{schema}"."{table_name}" '''
    rs_db_write.execute(truncate_query)
    logger.info(str(table_name) + ' table deleted')

    s3.write_df_to_db(df=data[table_info['column_name']], table_name=table_name, db=rs_db_write,
                      schema=schema)

    logger.info(str(table_name) + ' table uploaded')
    status2 = True

if status2 is True:
    status = 'Success'
else:
    status = 'Failed'

#logger.close()
end_time = datetime.datetime.now()
difference = end_time - start_time
min_to_complete = round(difference.total_seconds()/60 , 2)
email = Email()

email.send_email_file(subject=f"{env}-{status} : {table_name} table updated",
                      mail_body=f"{table_name} table updated, Time for job completion - {min_to_complete} mins ",
                      to_emails=email_to, file_uris=[])

rs_db.close_connection()
rs_db_write.close_connection()