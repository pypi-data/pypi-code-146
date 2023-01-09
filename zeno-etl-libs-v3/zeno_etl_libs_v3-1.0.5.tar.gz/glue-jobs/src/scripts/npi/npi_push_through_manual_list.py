
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
from zeno_etl_libs.utils.doid_write import doid_custom_write

import json
import datetime

import argparse
import pandas as pd
import numpy as np
import traceback

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
parser.add_argument('-et', '--email_to', default="saurav.maskar@zeno.health", type=str, required=False)
parser.add_argument('-sku', '--sku_to_add_per_round', default=50, type=int, required=False)
parser.add_argument('-si', '--store_id_to_close', default=330, type=str, required=False)
parser.add_argument('-ccf', '--cold_chain_flag', default=0, type=str, required=False)
parser.add_argument('-dts', '--date_to_start', default='2022-09-11', type=str, required=False)
parser.add_argument('-lsos3', '--list_name_on_s3', default='NPI_Palghar_list_upload', type=str, required=False)
parser.add_argument('-ssmm', '--change_ss_min_max_to_zero_flag', default=0, type=int, required=False)
parser.add_argument('-bif', '--block_ipc_flag', default=0, type=int, required=False)
parser.add_argument('-bind', '--block_ipc_for_n_days', default=30, type=int, required=False)
args, unknown = parser.parse_known_args()
env = args.env
email_to = args.email_to
sku_to_add_per_round = args.sku_to_add_per_round
store_id_to_close = args.store_id_to_close
cold_chain_flag = args.cold_chain_flag
date_to_start = args.date_to_start
list_name_on_s3 = args.list_name_on_s3
change_ss_min_max_to_zero_flag = args.change_ss_min_max_to_zero_flag
block_ipc_flag = args.block_ipc_flag
block_ipc_for_n_days = args.block_ipc_for_n_days

store_id_to_close = int(store_id_to_close)

os.environ['env'] = env

logger = get_logger(level='INFO')

logger.info(f"env: {env}")

rs_db = DB()
rs_db.open_connection()

rs_db_write = DB(read_only=False)
rs_db_write.open_connection()

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
logger.info("store_id_to_close - " + str(store_id_to_close))
logger.info("cold_chain_flag  - " + str(cold_chain_flag))
logger.info("date_to_start  - " + str(date_to_start))
logger.info("list_name_on_s3  - " + str(list_name_on_s3))
logger.info("change_ss_min_max_to_zero_flag  - " + str(change_ss_min_max_to_zero_flag))
logger.info("block_ipc_flag  - " + str(block_ipc_flag))
logger.info("block_ipc_for_n_days  - " + str(block_ipc_for_n_days))
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
            where nd.`store-id` = {store_id_to_close}) nd
    where
        nd.`row` = 1
 """.format(store_id_to_close=store_id_to_close)

store_last_sataus = pd.read_sql_query(store_last_sataus_query, mysql_read.connection)


if (len(store_last_sataus)==0) or (store_last_sataus.loc[0,'status']=='completed'):

    # Getting npi list
    npi_drug_list =pd.read_csv(s3.download_file_from_s3(file_name=f"npi_add_by_manual_list/{list_name_on_s3}.csv"))

    npi_drug_list= npi_drug_list[['store-id','drug-id']]

    drugs = tuple(map(int,npi_drug_list['drug-id'].unique()))

    store_drug_prod_inv_query = '''
    SELECT
                    i.`drug-id`,
                    d.`type` ,
                    d.`pack-form` ,
                    d.`cold-chain` ,
                    sum(i.quantity) as 'quantity'
                FROM
                    `inventory-1` i
                left join drugs d on i.`drug-id` = d.id 
                WHERE
                    i.`store-id` = {store_id_to_close}
                    and i.`drug-id` in {drugs}
                group by
                    i.`drug-id`,
                    d.`type` ,
                    d.`pack-form` ,
                    d.`cold-chain` 
            '''.format(store_id_to_close=store_id_to_close,drugs=drugs)
    store_drug_prod_inv = pd.read_sql_query(store_drug_prod_inv_query, mysql_read.connection)

    npi_drug_list = npi_drug_list.merge(store_drug_prod_inv,on = 'drug-id', how = 'left')
    npi_drug_list['quantity'] = npi_drug_list['quantity'].fillna(0)
    npi_drug_list = npi_drug_list[npi_drug_list['quantity']>0]

    store_drug_prod_query = '''
            select
                `store-id` ,
                `drug-id`,
                1 as `dummy`
            from
                `npi-drugs` nd
            where
                date(nd.`created-at`) >= '{date_to_start}'
                and nd.`store-id` = {store_id_to_close}
            '''.format(store_id_to_close=store_id_to_close,date_to_start=date_to_start)
    store_drug_prod = pd.read_sql_query(store_drug_prod_query, mysql_read.connection)

    # store_drug_prod_query = '''
    #         select
    #             "store-id" ,
    #             "drug-id",
    #             1 as "dummy"
    #         from
    #             "prod2-generico"."npi-drugs" nd
    #         where
    #             date(nd."created-at") >= '{date_to_start}'
    #             and nd."store-id" = {store_id_to_close}
    #         '''.format(store_id_to_close=store_id_to_close,date_to_start=date_to_start)
    # store_drug_prod = rs_db.get_df(store_drug_prod_query)

    # merging prod and DSS to avoid duplicate entries
    npi_drug_list = npi_drug_list.merge(store_drug_prod, how='left', on=['store-id', 'drug-id'])

    npi_drug_list = npi_drug_list.replace(np.nan, 0)

    npi_drug_list = npi_drug_list[npi_drug_list.dummy == 0]

    audit_drug_prod_query = '''
            SELECT
                a."store-id" ,
                a."drug-id" ,
                1 as dummy_audit
            from
                (
                select
                    b."store-id" ,
                    a."drug-id" ,
                    1 as dummy,
                    ROW_NUMBER() OVER(PARTITION BY b."store-id" ,
                    a."drug-id"
                ORDER BY
                    a.id DESC) as "row"
                from
                    "prod2-generico"."inventory-check-items-1" as a
                join "prod2-generico"."inventory-check-1" as b on
                    a."check-id" = b.id
                where
                    b."complete" = 0)a
            WHERE
                a."row" = 1
    	'''
    audit_drug_prod = rs_db.get_df(audit_drug_prod_query)
    logger.info('Read audit_drug_prod - from RS')

    # merging with audit drugs to avoid audit drugs entry
    npi_drug_list = npi_drug_list.merge(audit_drug_prod, how='left', on=['store-id', 'drug-id'])

    # replaceing null with 0 and extracting 35 rows
    npi_drug_list = npi_drug_list.replace(np.nan, 0)

    npi_drug_list = npi_drug_list[npi_drug_list.dummy_audit == 0]

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

    npi_drug_list.sort_values([ 'sort-pack-form', 'sort-type'],
                              ascending=[True,True], inplace=True)

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

    if int(change_ss_min_max_to_zero_flag) == 1:
        logger.info('start - change SS Min Max to 0')
        # set max=0 for npi drugs in DOID
        npi_store_drugs = final_list_npi[["store-id", "drug-id"]]
        npi_store_drugs.columns = [c.replace('-', '_') for c in npi_store_drugs.columns]
        doid_missed_entries = doid_custom_write(npi_store_drugs, logger)

        # save email attachements to s3
        # curr_date = str(datetime.date.today())
        # doid_missed_entries_uri = s3.save_df_to_s3(doid_missed_entries,
        #                                        file_name=f"doid_missed_entries_{curr_date}.csv")
        logger.info('end - change SS Min Max to 0')
    else:
        # doid_missed_entries_uri = []
        logger.info('Not Changing SS Min Max to 0')


    if int(block_ipc_flag) ==1:
        logger.info(f'start : block ipc for {block_ipc_for_n_days} days')
    # Rotation drugs to be appended in omit_ss_reset table
        omit_drug_store = final_list_npi[["drug-id",
                                             "store-id"]].drop_duplicates()
        omit_drug_store["updated-at"] = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
        omit_drug_store["created-at"] = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
        omit_drug_store["created-by"] = 'data.sciene@zeno.health'
        omit_drug_store["updated-by"] = 'data.sciene@zeno.health'
        omit_drug_store["start-date"] = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d')
        omit_drug_store["end-date"] =  (datetime.datetime.now(tz=gettz('Asia/Kolkata')) + datetime.timedelta(
            days=block_ipc_for_n_days)).strftime('%Y-%m-%d')
        omit_drug_store["is-active"] = 1
        omit_drug_store["reason"] = 'NPI'
        schema = 'prod2-generico'
        table_name = 'omit-ss-reset'

        # Uncomment following part once omit-ss-reset table is transferred to DSS

        table_info = helper.get_table_info(db=rs_db, table_name=table_name, schema=schema)

        s3.write_df_to_db(df=omit_drug_store[table_info['column_name']], table_name=table_name, db=rs_db_write,
                          schema=schema)

        logger.info(f'End : block ipc for {block_ipc_for_n_days} days')

    else:
        logger.info(f'Not Blocking IPC for {block_ipc_for_n_days} days')



    # npi_added_uri = s3.save_df_to_s3(df=npi_drug_list, file_name='npi_removal_details_{}.csv'.format(cur_date))

    status = 'added'

    email = Email()

    email.send_email_file(subject=f"{env} : store id - {store_id_to_close} NPI List",
                          mail_body=f"list-{status},{len(final_list_npi)} SKU Added\n"
                          f"ipc change flag - {change_ss_min_max_to_zero_flag}, block ipc flag - {block_ipc_for_n_days}, block ipc for {block_ipc_for_n_days} days\n",
                          to_emails=email_to, file_uris=[])

else:
    status = 'not-added'

    email = Email()

    email.send_email_file(subject=f"{env} : store id - {store_id_to_close} NPI List",
                          mail_body=f"list-{status},Previos Status - {store_last_sataus.loc[0,'status']}",
                          to_emails=email_to, file_uris=[])

rs_db.close_connection()
rs_db_write.close_connection()
mysql_read.close()
