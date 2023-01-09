"""""
 Pupose : adding PMF(Presently only for Mulund west) NPI based on store assortment
 Author : saurav.maskar@zeno.health
"""""

import os
import sys

sys.path.append('../../../..')

from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper.email.email import Email
from zeno_etl_libs.db.db import DB, MySQL
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

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
parser.add_argument('-et', '--email_to', default="saurav.maskar@zeno.health", type=str, required=False)
parser.add_argument('-sku', '--sku_to_add_per_round', default=18, type=int, required=False)
parser.add_argument('-si', '--store_id', default=4, type=int, required=False)
parser.add_argument('-ccf', '--cold_chain_flag', default=1, type=str, required=False)
parser.add_argument('-dts', '--date_to_start', default='2022-11-01', type=str, required=False)
args, unknown = parser.parse_known_args()
env = args.env
email_to = args.email_to
sku_to_add_per_round = args.sku_to_add_per_round
store_id = args.store_id
cold_chain_flag = args.cold_chain_flag
date_to_start = args.date_to_start

store_id = int(store_id)

os.environ['env'] = env

logger = get_logger(level='INFO')

logger.info(f"env: {env}")

rs_db = DB()
rs_db.open_connection()

mysql_read = MySQL()

mysql_read.open_connection()


s3 = S3()
start_time = datetime.datetime.now()
logger.info('Script Manager Initialized')
logger.info("")
logger.info("parameters reading")
logger.info(f"env: {env}")
logger.info("email_to - " + email_to)
logger.info("sku_to_add_per_round - " + str(sku_to_add_per_round))
logger.info("store_id_to_close - " + str(store_id))
logger.info("cold_chain_flag  - " + str(cold_chain_flag))
logger.info("")

# date parameter
logger.info("code started at {}".format(datetime.datetime.now().strftime(
    '%Y-%m-%d %H:%M:%S')))
logger.info("")

cur_date = datetime.datetime.now(tz=gettz('Asia/Kolkata')).date()

store_last_sataus_query = """
    select
        *
    from
        (
        select
            row_number() over (partition by nd.`store-id`
        order by
            nd.`created-at` desc
                  ) as `row`,
            nd.`store-id`,
            nd.status ,
            nd.`created-at`
        from
            `npi-drugs` nd
            where nd.`store-id` = {store_id}) nd
    where
        nd.`row` = 1
 """.format(store_id=store_id)

store_last_sataus = pd.read_sql_query(store_last_sataus_query, mysql_read.connection)


if store_last_sataus.loc[0,'status']=='completed':

    # Getting inventory detail
    prod_inventory_query = '''
        select
            i."store-id" ,
            i."drug-id" ,
            d."drug-name" ,
            d."pack-form" ,
            d."type" ,
            d."cold-chain" ,
            sum(i.quantity) as "quantity",
            sum(i.quantity + i."locked-for-check" + i."locked-for-audit" + i."locked-for-return" + i."locked-for-transfer" ) as "quantity-available-physically-at-store"
        from
            "prod2-generico"."prod2-generico"."inventory-1" i
        left join "prod2-generico"."prod2-generico".stores s 
        on
            i."store-id" = s.id
        left join "prod2-generico"."prod2-generico".drugs d 
        on
            d.id = i."drug-id"
        left join "prod2-generico"."prod2-generico"."invoices-1" i2
        on
            i."franchisee-invoice-id" = i2.id
        where
            i."store-id" = {store_id}
            and i2."franchisee-invoice" = 0
            and (i.quantity >0
                --  or i."locked-for-check" >0
                -- or i."locked-for-audit" >0
                -- or i."locked-for-return" >0
                -- or i."locked-for-transfer" >0
                )
        group by
            i."store-id" ,
            i."drug-id" ,
            d."drug-name",
            d."pack-form" ,
            d."type" ,
            d."cold-chain" 
            '''.format(store_id=store_id)
    prod_inventory = rs_db.get_df(prod_inventory_query)

    store_assortment_query = """
        SELECT
            sda."store-id" ,
	        sda."drug-id" 
        FROM
            "prod2-generico"."store-drug-assortment" sda
        WHERE
            sda."is-active" = 1
            and sda."store-id" ={store_id}
    """.format(store_id=store_id)
    store_assortment = rs_db.get_df(store_assortment_query)

    drugs_in_assortment = tuple(map(int, list(store_assortment['drug-id'].unique())))

    npi_drug_list = prod_inventory[~prod_inventory['drug-id'].isin(drugs_in_assortment)]

    npi_remaning = False

    if len(npi_drug_list)== 0:
        npi_remaning = False
    else:
        npi_remaning = True

        logger.info('npi-present-check-1')

        store_drug_prod_query = '''
                select
                    "store-id" ,
                    "drug-id",
                    1 as "dummy"
                from
                    "prod2-generico"."npi-drugs" nd
                where
                    date(nd."created-at") >= date(dateadd(d,-15,current_date))
                    and nd."store-id" = {store_id}
                '''.format(store_id=store_id,date_to_start=date_to_start)
        store_drug_prod = rs_db.get_df(store_drug_prod_query)

        # merging prod and DSS to avoid duplicate entries
        npi_drug_list = npi_drug_list.merge(store_drug_prod, how='left', on=['store-id', 'drug-id'])

        npi_drug_list = npi_drug_list.replace(np.nan, 0)

        npi_drug_list = npi_drug_list[npi_drug_list.dummy == 0]

        if len(npi_drug_list) == 0:
            npi_remaning = False
        else:
            npi_remaning = True

            logger.info('npi-present-check-2')

            choice = [npi_drug_list['type'] == 'high-value-ethical',
                      npi_drug_list['type'] == 'ethical',
                      npi_drug_list['type'] == 'generic',
                      npi_drug_list['type'] == 'ayurvedic',
                      npi_drug_list['type'] == 'surgical',
                      npi_drug_list['type'] == 'category-4',
                      npi_drug_list['type'] == 'otc',
                      npi_drug_list['type'] == 'general',
                      npi_drug_list['type'] == 'baby-food',
                      npi_drug_list['type'] == 'baby-product',
                      npi_drug_list['type'] == 'glucose-test-kit',
                      npi_drug_list['type'] == 'discontinued-products',
                      npi_drug_list['type'] == 'banned']

            select = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

            npi_drug_list['sort-type'] = np.select(choice, select, default=999)

            choice = [npi_drug_list['pack-form'] == 'STRIP',
                      npi_drug_list['pack-form'] == 'PACKET',
                      npi_drug_list['pack-form'] == 'SACHET',
                      npi_drug_list['pack-form'] == 'TUBE',
                      npi_drug_list['pack-form'] == 'BOTTLE',
                      npi_drug_list['pack-form'] == 'TETRA PACK',
                      npi_drug_list['pack-form'] == 'PRE FILLED SYRINGE',
                      npi_drug_list['pack-form'] == 'VIAL',
                      npi_drug_list['pack-form'] == 'CARTRIDGE',
                      npi_drug_list['pack-form'] == 'JAR',
                      npi_drug_list['pack-form'] == 'SPRAY BOTTLE',
                      npi_drug_list['pack-form'] == 'BOX',
                      npi_drug_list['pack-form'] == 'TIN',
                      npi_drug_list['pack-form'] == 'AMPOULE',
                      npi_drug_list['pack-form'] == 'KIT']

            select = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

            npi_drug_list['sort-pack-form'] = np.select(choice, select, default=999)

            npi_drug_list.sort_values(['cold-chain', 'sort-pack-form', 'drug-name','sort-type'],
                                      ascending=[True,True,True,True], inplace=True)


            if int(cold_chain_flag) == 0:
                npi_drug_list = npi_drug_list[npi_drug_list['cold-chain'] == 0]
                logger.info('removing cold chain products')
            elif int(cold_chain_flag) == 2:
                npi_drug_list = npi_drug_list[npi_drug_list['cold-chain'] == 1]
                logger.info('considering only cold chain products')
            else:
                logger.info('Not caring whether cold chain items are added or not')

            npi_drug_list = npi_drug_list.head(sku_to_add_per_round).reset_index(drop=True)

            final_list_npi = npi_drug_list[['store-id', 'drug-id']]

            mysql_write = MySQL(read_only=False)
            mysql_write.open_connection()

            # inserting data into prod

            logger.info("mySQL - Insert starting")

            final_list_npi.to_sql(name='npi-drugs', con=mysql_write.engine,
                                  if_exists='append', index=False,
                                  method='multi', chunksize=500)

            logger.info("mySQL - Insert ended")

            mysql_write.close()

            # npi_added_uri = s3.save_df_to_s3(df=npi_drug_list, file_name='npi_removal_details_{}.csv'.format(cur_date))

    if npi_remaning:
        status = 'added'
    else:
        status = 'not-added-because-no-npi'

    email = Email()

    email.send_email_file(subject=f"{env} : {store_id} NPI List",
                          mail_body=f"list-{status},{len(final_list_npi)} SKU {status}",
                          to_emails=email_to, file_uris=[])

else:
    status = 'not-added'

    email = Email()

    email.send_email_file(subject=f"{env} : {store_id} NPI List",
                          mail_body=f"list-{status},Previos Status - {store_last_sataus.loc[0,'status']}",
                          to_emails=email_to, file_uris=[])

rs_db.close_connection()
mysql_read.close()