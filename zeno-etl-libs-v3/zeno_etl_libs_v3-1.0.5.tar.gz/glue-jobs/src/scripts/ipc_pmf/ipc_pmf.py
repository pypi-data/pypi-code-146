"""IPC combination level forecast for PMF stores"""

import os
import sys
import argparse

import pandas as pd
import datetime as dt
from dateutil.tz import gettz
from ast import literal_eval

sys.path.append('../../../..')

from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.email.email import Email
from zeno_etl_libs.helper import helper

from zeno_etl_libs.utils.ipc_pmf.ipc_combination_fcst.forecast_main import ipc_comb_forecast
from zeno_etl_libs.utils.ipc_pmf.ipc_drug_fcst.forecast_main import ipc_drug_forecast
from zeno_etl_libs.utils.ipc_pmf.ipc_combination_fcst.fcst_mapping import fcst_comb_drug_map
from zeno_etl_libs.utils.ipc_pmf.safety_stock import safety_stock_calc
from zeno_etl_libs.utils.ipc_pmf.post_processing import post_processing
from zeno_etl_libs.utils.ipc_pmf.heuristics.recency_corr import fcst_correction
from zeno_etl_libs.utils.ipc.doid_update_ss import doid_update


def main(debug_mode, reset_stores, reset_date, type_list_comb_lvl,
         type_list_drug_lvl, v4_active_flag, drug_type_list_v4,
         read_schema, rs_db_read, write_schema, rs_db_write, logger):

    logger.info(f"Debug Mode: {debug_mode}")
    status = 'Failed'

    # Define empty variables if required in case of fail
    safety_stock_df = pd.DataFrame()
    df_one_one = pd.DataFrame()
    df_one_many = pd.DataFrame()
    df_one_none = pd.DataFrame()
    df_none_one = pd.DataFrame()
    new_drug_entries = pd.DataFrame()
    missed_entries = pd.DataFrame()

    try:
        for store_id in reset_stores:
            logger.info(f"Running for store id: {store_id} and reset date: {reset_date}")

            type_list_comb_lvl_str = str(type_list_comb_lvl).replace('[', '(').replace(']', ')')
            type_list_drug_lvl_str = str(type_list_drug_lvl).replace('[', '(').replace(']', ')')

            # RUNNING IPC-COMBINATION FORECAST PIPELINE
            logger.info("Combination Forecast Pipeline starts")
            fcst_df_comb_lvl, seg_df_comb_lvl, \
            comb_sales_latest_12w, comb_sales_4w_wtd = ipc_comb_forecast(
                store_id, reset_date, type_list_comb_lvl_str, read_schema, rs_db_read,
                logger)

            # RUNNING IPC-DRUG FORECAST PIPELINE
            logger.info("Drug Forecast Pipeline starts")
            fcst_df_drug_lvl, seg_df_drug_lvl, drug_sales_latest_12w,\
            drug_sales_latest_4w, drug_sales_4w_wtd = ipc_drug_forecast(
                store_id, reset_date, type_list_drug_lvl_str, read_schema,
                rs_db_read, logger)

            # RECENCY CORRECTION IF FCST=0, FCST=AVG_DEMAND_28D (FROM LATEST 12W)
            logger.info("Recency correction starts")
            fcst_df_comb_lvl, fcst_df_drug_lvl = fcst_correction(
                fcst_df_comb_lvl, comb_sales_latest_12w, fcst_df_drug_lvl,
                drug_sales_latest_12w, drug_sales_latest_4w, comb_sales_4w_wtd,
                drug_sales_4w_wtd, logger)

            # MAPPING FORECASTS TO ASSORTMENT DRUGS
            logger.info("Allotting combination forecasts to drugs")
            df_fcst_final, df_one_one, df_one_many, \
            df_one_none, df_none_one = fcst_comb_drug_map(
                store_id, reset_date, fcst_df_comb_lvl, fcst_df_drug_lvl,
                type_list_comb_lvl, read_schema, rs_db_read, logger)

            # SAFETY STOCK CALCULATIONS
            logger.info("Safety Stock Calculations starts")
            safety_stock_df = safety_stock_calc(
                df_fcst_final, store_id, reset_date,
                v4_active_flag, drug_type_list_v4, drug_sales_latest_12w,
                read_schema, rs_db_read, logger)

            # POST PROCESSING SS DF
            logger.info("Post Processing SS-DF starts")
            safety_stock_df, seg_df_comb_lvl, seg_df_drug_lvl = post_processing(
                store_id, safety_stock_df, seg_df_comb_lvl, seg_df_drug_lvl,
                read_schema, rs_db_read, logger)

            # WRITING TO RS-DB
            if debug_mode == 'N':
                logger.info("Writing table to RS-DB")
                # writing table ipc-pmf-safety-stock
                safety_stock_df['reset_date'] = dt.datetime.strptime(reset_date,
                                                                     '%Y-%m-%d').date()
                safety_stock_df['store_id'] = safety_stock_df['store_id'].astype(int)
                safety_stock_df['drug_id'] = safety_stock_df['drug_id'].astype(int)
                safety_stock_df['created-at'] = dt.datetime.now(
                    tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
                safety_stock_df['created-by'] = 'etl-automation'
                safety_stock_df['updated-at'] = dt.datetime.now(
                    tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
                safety_stock_df['updated-by'] = 'etl-automation'
                safety_stock_df.columns = [c.replace('_', '-') for c in
                                           safety_stock_df.columns]
                table_info = helper.get_table_info(db=rs_db_write,
                                                   table_name='ipc-pmf-safety-stock',
                                                   schema=write_schema)
                columns = list(table_info['column_name'])
                safety_stock_df = safety_stock_df[columns]  # required column order

                logger.info("Writing to table: ipc-pmf-safety-stock")
                s3.write_df_to_db(df=safety_stock_df,
                                  table_name='ipc-pmf-safety-stock',
                                  db=rs_db_write, schema=write_schema)

                # writing table ipc-pmf-comb-segmentation
                seg_df_comb_lvl['reset_date'] = dt.datetime.strptime(reset_date,
                                                            '%Y-%m-%d').date()
                seg_df_comb_lvl['created-at'] = dt.datetime.now(
                    tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
                seg_df_comb_lvl['created-by'] = 'etl-automation'
                seg_df_comb_lvl['updated-at'] = dt.datetime.now(
                    tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
                seg_df_comb_lvl['updated-by'] = 'etl-automation'
                seg_df_comb_lvl.columns = [c.replace('_', '-') for c in seg_df_comb_lvl.columns]
                table_info = helper.get_table_info(db=rs_db_write,
                                                   table_name='ipc-pmf-comb-segmentation',
                                                   schema=write_schema)
                columns = list(table_info['column_name'])
                seg_df_comb_lvl = seg_df_comb_lvl[columns]  # required column order

                logger.info("Writing to table: ipc-pmf-comb-segmentation")
                s3.write_df_to_db(df=seg_df_comb_lvl,
                                  table_name='ipc-pmf-comb-segmentation',
                                  db=rs_db_write, schema=write_schema)

                # writing table ipc-pmf-drug-segmentation
                seg_df_drug_lvl['reset_date'] = dt.datetime.strptime(reset_date,
                                                                     '%Y-%m-%d').date()
                seg_df_drug_lvl['created-at'] = dt.datetime.now(
                    tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
                seg_df_drug_lvl['created-by'] = 'etl-automation'
                seg_df_drug_lvl['updated-at'] = dt.datetime.now(
                    tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
                seg_df_drug_lvl['updated-by'] = 'etl-automation'
                seg_df_drug_lvl.columns = [c.replace('_', '-') for c in
                                           seg_df_drug_lvl.columns]
                table_info = helper.get_table_info(db=rs_db_write,
                                                   table_name='ipc-pmf-drug-segmentation',
                                                   schema=write_schema)
                columns = list(table_info['column_name'])
                seg_df_drug_lvl = seg_df_drug_lvl[columns]  # required column order

                logger.info("Writing to table: ipc-pmf-drug-segmentation")
                s3.write_df_to_db(df=seg_df_drug_lvl,
                                  table_name='ipc-pmf-drug-segmentation',
                                  db=rs_db_write, schema=write_schema)

                logger.info("All writes to RS-DB completed!")

                # UPLOADING MIN, SS, MAX in DOI-D
                logger.info("Updating new SS to DrugOrderInfo-Data")
                safety_stock_df.columns = [c.replace('-', '_') for c in
                                           safety_stock_df.columns]
                ss_data_upload = safety_stock_df.loc[
                    (safety_stock_df["order_upto_point"] > 0)]
                ss_data_upload = ss_data_upload[['store_id', 'drug_id',
                                                 'safety_stock',
                                                 'reorder_point',
                                                 'order_upto_point']]
                ss_data_upload.columns = ['store_id', 'drug_id', 'corr_min',
                                          'corr_ss', 'corr_max']
                new_drug_entries_str, missed_entries_str = doid_update(
                    ss_data_upload, type_list_drug_lvl_str, rs_db_write,
                    write_schema, logger, gaid_omit=False)
                new_drug_entries = new_drug_entries.append(new_drug_entries_str)
                missed_entries = missed_entries.append(missed_entries_str)

        status = 'Success'

    except Exception as error:
        logger.exception(error)

    return status, safety_stock_df, df_one_one, df_one_many, df_one_none, \
           df_none_one, new_drug_entries, missed_entries


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This is ETL script.")
    parser.add_argument('-e', '--env', default="dev", type=str, required=False)
    parser.add_argument('-et', '--email_to',
                        default="vivek.revi@zeno.health",
                        type=str, required=False)
    parser.add_argument('-d', '--debug_mode', default="Y", type=str,
                        required=False)
    parser.add_argument('-rd', '--reset_date', default="YYYY-MM-DD", type=str,
                        required=False)
    parser.add_argument('-rs', '--reset_stores',
                        default=[4], nargs='+', type=int,
                        required=False)
    parser.add_argument('-v4', '--v4_active_flag', default="Y", type=str,
                        required=False)
    parser.add_argument('-v4tl', '--drug_type_list_v4',
                        default="{'generic':'{0:[0,0,0], 1:[0,0,1], 2:[0,1,2],3:[1,2,3]}',"
                                "'ethical':'{0:[0,0,0], 1:[0,0,1], 2:[0,1,2],3:[1,2,3]}',"
                                "'others':'{0:[0,0,0], 1:[0,0,1], 2:[0,1,2],3:[1,2,3]}'}",
                        type=str, required=False)

    args, unknown = parser.parse_known_args()

    env = args.env
    os.environ['env'] = env
    email_to = args.email_to
    debug_mode = args.debug_mode

    # JOB EXCLUSIVE PARAMS
    reset_date = args.reset_date
    reset_stores = args.reset_stores
    v4_active_flag = args.v4_active_flag
    drug_type_list_v4 = args.drug_type_list_v4

    # EVALUATE REQUIRED JSON PARAMS
    drug_type_list_v4 = literal_eval(drug_type_list_v4)

    type_list_comb_lvl = ['ethical', 'generic', 'discontinued-products',
                          'high-value-ethical']
    type_list_drug_lvl = ['ethical', 'ayurvedic', 'generic',
                          'discontinued-products', 'banned', 'general',
                          'high-value-ethical', 'baby-product', 'surgical',
                          'otc', 'glucose-test-kit', 'category-2', 'category-1',
                          'category-4', 'baby-food', '', 'category-3']

    if reset_date == 'YYYY-MM-DD':  # Take current date
        reset_date = dt.date.today().strftime("%Y-%m-%d")

    logger = get_logger()
    s3 = S3()
    rs_db_read = DB(read_only=True)
    rs_db_write = DB(read_only=False)
    read_schema = 'prod2-generico'
    write_schema = 'prod2-generico'

    # open RS connection
    rs_db_read.open_connection()
    rs_db_write.open_connection()

    """ calling the main function """
    status, safety_stock_df, df_one_one, df_one_many, df_one_none, \
        df_none_one, new_drug_entries, missed_entries = main(
            debug_mode, reset_stores, reset_date, type_list_comb_lvl,
            type_list_drug_lvl, v4_active_flag, drug_type_list_v4,
            read_schema, rs_db_read, write_schema, rs_db_write, logger)

    # open RS connection
    rs_db_read.close_connection()
    rs_db_write.close_connection()

    ss_df_uri = s3.save_df_to_s3(
        safety_stock_df, file_name=f"safety_stock_df_{reset_date}.csv")
    new_drug_entries_uri = s3.save_df_to_s3(new_drug_entries,
                                            file_name=f"new_drug_entries_{reset_date}.csv")
    missed_entries_uri = s3.save_df_to_s3(missed_entries,
                                          file_name=f"missed_entries_{reset_date}.csv")
    all_cases_xl_path = s3.write_df_to_excel(data={
        'C1_one_one': df_one_one, 'C2_one_many': df_one_many,
        'C3_one_none': df_one_none, 'C4_none_one': df_none_one},
        file_name=f"all_mappings_{reset_date}.xlsx")

    email = Email()
    email.send_email_file(
        subject=f"IPC Combination Fcst (SM-{env}) {reset_date}: {status}",
        mail_body=f"""
                   Debug Mode: {debug_mode}
                   Reset Stores: {reset_stores}
                   Job Params: {args}
                   """,
        to_emails=email_to, file_uris=[ss_df_uri, new_drug_entries_uri,
                                       missed_entries_uri],
        file_paths=[all_cases_xl_path])

