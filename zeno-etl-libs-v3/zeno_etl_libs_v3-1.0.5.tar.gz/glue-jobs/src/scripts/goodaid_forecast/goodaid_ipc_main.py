import os
import sys
import argparse

sys.path.append('../../../..')

import pandas as pd
import numpy as np
import datetime as dt
from dateutil.tz import gettz


from zeno_etl_libs.utils.goodaid_forecast.engine.config_goodaid import *
from zeno_etl_libs.utils.goodaid_forecast.engine.goodaid_ts_forecast import *
from zeno_etl_libs.utils.goodaid_forecast.engine.goodaid_safety_stock_calculation\
    import safety_stock_calc
from zeno_etl_libs.utils.goodaid_forecast.engine.goodaid_forecast_main import goodaid_ipc_forecast
from zeno_etl_libs.utils.goodaid_forecast.engine.goodaid_doid_update_ss import goodaid_doid_update


from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.db.db import DB, PostGre
from zeno_etl_libs.django.api import Django
from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.email.email import Email
from zeno_etl_libs.helper import helper


def main(debug_mode, reset_stores, reset_date, type_list,
          rs_db_read, rs_db_write, read_schema, write_schema,
         s3, django, logger):

    logger.info(f"Debug Mode: {debug_mode}")
    status = 'Failed'

    # Define empty variables if required in case of fail
    order_value_all = pd.DataFrame()
    new_drug_entries = pd.DataFrame()
    missed_entries = pd.DataFrame()
    df_outliers_all = pd.DataFrame()
    manual_doid_upd_all = pd.DataFrame()

    try:
        for store_id in reset_stores:
            logger.info(f"Running for store id: {store_id} and reset date: {reset_date}")

            # RUNNING IPC2.0 FORECAST PIPELINE
            logger.info("Forecast Pipeline starts...")
            agg_fcst, cal_sales, weekly_fcst, seg_df, drug_class = goodaid_ipc_forecast(
                store_id, reset_date, type_list, read_schema, rs_db_read,
                logger)

            # SAFETY STOCK CALCULATIONS
            logger.info("Safety Stock Calculations starts...")
            agg_fcst_s = agg_fcst[agg_fcst['store_id'] == store_id]
            # cal_sales = cal_sales[cal_sales['store_id']==store_id]
            safety_stock_df = safety_stock_calc(agg_fcst_s, cal_sales, store_id, reset_date,
                                                schema, db, logger)

            # Temporary Fix it at safety stock module level
            safety_stock_df['safety_stock'].fillna(2, inplace=True)
            safety_stock_df['reorder_point'].fillna(2, inplace=True)
            safety_stock_df['order_upto_point'] = safety_stock_df['order_upto_point'].replace(0, 3)
            safety_stock_df['order_upto_point'].fillna(3, inplace=True)


            # WRITING TO RS-DB
            if debug_mode == 'N':
                logger.info("Writing table to RS-DB")

                # writing table ipc2-safety-stock
                safety_stock_df['store_id'] = safety_stock_df['store_id'].astype(int)
                safety_stock_df['drug_id'] = safety_stock_df['drug_id'].astype(int)
                safety_stock_df['reset_date'] = dt.datetime.strptime(reset_date, '%Y-%m-%d').date()
                safety_stock_df['created-at'] = dt.datetime.now(
                    tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
                safety_stock_df['created-by'] = 'etl-automation'
                safety_stock_df['updated-at'] = dt.datetime.now(
                    tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
                safety_stock_df['updated-by'] = 'etl-automation'
                safety_stock_df.columns = [c.replace('_', '-') for c in
                                           safety_stock_df.columns]
                table_info = helper.get_table_info(db=rs_db_write,
                                                   table_name='goodaid-safety-stock',
                                                   schema=write_schema)

                columns = list(table_info['column_name'])
                safety_stock_df = safety_stock_df[columns]  # required column order

                logger.info("Writing to table: goodaid-safety-stock")
                s3.write_df_to_db(df=safety_stock_df,
                                  table_name='goodaid-safety-stock',
                                  db=rs_db_write, schema=write_schema)

                logger.info("All writes to RS-DB completed!")

                # UPLOADING MIN, SS, MAX in DOI-D
                logger.info("Updating new SS to DrugOrderInfo-Data")
                safety_stock_df.columns = [c.replace('-', '_') for c in safety_stock_df.columns]
                ss_data_upload = safety_stock_df.loc[
                    (safety_stock_df["order_upto_point"] > 0)]
                ss_data_upload = ss_data_upload[['store_id', 'drug_id',
                        'safety_stock', 'reorder_point', 'order_upto_point']]
                ss_data_upload.columns = ['store_id', 'drug_id', 'corr_min',
                                          'corr_ss', 'corr_max']
                new_drug_entries_str, missed_entries_str = goodaid_doid_update(
                    ss_data_upload, type_list, rs_db_write, write_schema,
                    logger)
                new_drug_entries = new_drug_entries.append(new_drug_entries_str)
                missed_entries = missed_entries.append(missed_entries_str)

            else:
                logger.info("Writing to RS-DB skipped")

        status = 'Success'
        logger.info(f"IPC code execution status: {status}")

    except Exception as error:
        logger.exception(error)
        logger.info(f"IPC code execution status: {status}")

    return status,  new_drug_entries, missed_entries,\
           df_outliers_all, manual_doid_upd_all



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This is ETL script.")
    parser.add_argument('-e', '--env', default="dev", type=str, required=False)
    parser.add_argument('-et', '--email_to',
                        default="saurav.maskar@zeno.health",
                        type=str, required=False)
    parser.add_argument('-d', '--debug_mode', default="N", type=str,
                        required=False)
    parser.add_argument('-exsto', '--exclude_stores',
                        default=[52, 60, 92, 243, 281,297,4], nargs='+', type=int,
                        required=False)
    parser.add_argument('-rd', '--reset_date', default="YYYY-MM-DD", type=str,
                        required=False)
    parser.add_argument('-rs', '--reset_stores',
                        default=[0], nargs='+', type=int,
                        required=False)

    args, unknown = parser.parse_known_args()

    env = args.env
    os.environ['env'] = env
    email_to = args.email_to
    debug_mode = args.debug_mode

    # JOB EXCLUSIVE PARAMS
    exclude_stores = args.exclude_stores
    reset_date = args.reset_date
    reset_stores = args.reset_stores

    logger = get_logger()
    s3 = S3()
    django = Django()
    rs_db_read = DB(read_only=True)
    rs_db_read.open_connection()
    rs_db_write = DB(read_only=False)
    rs_db_write.open_connection()
    read_schema = 'prod2-generico'
    write_schema = 'prod2-generico'

    schema = 'prod2-generico'
    db = rs_db_read

    if reset_date == 'YYYY-MM-DD':  # Take current date
        reset_date = dt.date.today().strftime("%Y-%m-%d")

    if reset_stores == [0]:  # Fetch stores
        store_list_query = """
                select
                    s.id as "store_id"
                from
                    "{schema}".stores s
                where
                    DATEDIFF(day,
                    "opened-at",
                    current_date)>90
                    and name <> 'Zippin Central'
                    and "is-active" = 1
                    and "opened-at" != '0101-01-01 00:00:00'
                    and id not in {exclude_stores}
                    --  and s."franchisee-id" != 1
        """.format(exclude_stores=str(exclude_stores).replace('[', '(').replace(']', ')'),
                               schema=schema)
        store_list_df = db.get_df(store_list_query)
        store_id_list = tuple(map(int,store_list_df['store_id'].unique()))
        reset_store = store_id_list

    type_list =('ethical', 'ayurvedic', 'generic', 'general', 'high-value-ethical', 'baby-product'," \
                        " 'surgical', 'otc', 'glucose-test-kit', 'category-2', " \
                        "'category-1', 'category-4', 'baby-food', '', 'category-3')


    """ calling the main function """
    status, new_drug_entries, missed_entries, \
    df_outliers_all, manual_doid_upd_all = main(debug_mode, reset_stores, reset_date, type_list,
         rs_db_read, rs_db_write, read_schema, write_schema,
         s3, django, logger)

    # close RS connection
    rs_db_read.close_connection()
    rs_db_write.close_connection()

    # save email attachements to s3
    new_drug_entries_uri = s3.save_df_to_s3(new_drug_entries,
                                            file_name=f"goodaid_new_drug_entries_{reset_date}.csv")
    missed_entries_uri = s3.save_df_to_s3(missed_entries,
                                          file_name=f"goodaid_missed_entries_{reset_date}.csv")
    df_outliers_all_uri = s3.save_df_to_s3(df_outliers_all,
                                           file_name=f"goodaid_df_outliers_all_{reset_date}.csv")
    manual_doid_upd_all_uri = s3.save_df_to_s3(manual_doid_upd_all,
                                               file_name=f"goodaid_manual_doid_upd_all_{reset_date}.csv")

    # SEND EMAIL ATTACHMENTS (IPC-RUN STATUS)
    logger.info("Sending email attachments..")
    email = Email()
    email.send_email_file(
        subject=f"GOODAID IPC SS Reset (SM-{env}) {reset_date}: {status}",
        mail_body=f"""
                  Debug Mode: {debug_mode}
                  Reset Stores: {reset_stores}
                  Job Params: {args}
                  """,
        to_emails=email_to, file_uris=[
                                       new_drug_entries_uri,
                                       missed_entries_uri])

    logger.info("Script ended")
