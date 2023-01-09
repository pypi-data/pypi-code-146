import os
import sys
import argparse

import pandas as pd
import numpy as np
import datetime as dt
from dateutil.tz import gettz

sys.path.append('../../../..')

from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.db.db import DB, MySQL
from zeno_etl_libs.helper import helper
from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.email.email import Email


def main(debug_mode, run_stores, run_date, s3, mysql, rs_db_read, rs_db_write,
         read_schema, write_schema, logger, online_email, offline_email):
    status = 'Failed'

    logger.info("PMF Conversion Code Execution Starts")
    logger.info(f"Stores: {run_stores}")
    logger.info(f"Run Date: {run_date}")
    logger.info(f"Debug Mode: {debug_mode}")
    logger.info(f"Online Session Login IDs: {online_email}")
    logger.info(f"Offline Session Login IDs: {offline_email}")

    online_email = online_email.split(",")
    offline_email = offline_email.split(",")
    logins = tuple(online_email + offline_email)

    try:
        # ======================================================================
        # alternative searches
        # ======================================================================
        q_bb = f"""
        select
            ad.`unique-id` as `session-id`,
            pso.`order-number`,
            ad.`patients-store-orders-id`,
            ad.`patient-id` as `ad-patient-id`,
            pso.`patient-id` as `pso-patient-id`,    
            ad.`store-id`,
            ad.`requested-drug-id`,
            ad.`requested-drug-name`,
            d.`type` as `drug-type`,
            d.category,
            ad.`required-drug-quantity`,
            ad.`suggested-drug-id`,
            ad.`suggested-drug-name`,
            ad.`suggested-drug-inventory-quantity`,
            sda.`is-active` as `assortment_active`,
            date(ad.`created-at`) as `session-date`,
            pso.`bill-id`, 
            pso.`order-type`,
            ad.`created-by` as `session-created-by`
        from
            `alternate-drugs` ad
        left join `patients-store-orders` pso on
            pso.`id` = ad.`patients-store-orders-id`
        left join `bills-1` b on 
            b.`id` = pso.`bill-id`
        left join drugs d on 
            d.id = ad.`requested-drug-id`
        left join `store-drug-assortment` sda on
            sda.`store-id` = ad.`store-id` and sda.`drug-id` = ad.`requested-drug-id`
        where
            date(ad.`created-at`) = '{run_date}'
            and ad.`store-id` in {run_stores}
            and ad.`created-by` in {logins}
        """
        df_bb = pd.read_sql_query(q_bb, mysql.connection)
        df_bb.columns = [c.replace('-', '_') for c in df_bb.columns]

        # have a patient across every session
        df_bb['pid'] = np.where(df_bb['ad_patient_id'].isnull(),
                                df_bb['pso_patient_id'], df_bb['ad_patient_id'])
        df_bb["patient_id"] = df_bb.groupby("session_id")['pid'].transform(
            lambda x: x.fillna(x.mean()))
        df_bb.drop(['ad_patient_id', 'pso_patient_id', 'pid'], axis=1, inplace=True)

        df_bb['assortment_active'].fillna(0, inplace=True)

        # add patient name/number.
        tempp = df_bb[df_bb['patient_id'].notnull()][['patient_id']]
        tempp['patient_id'] = tempp['patient_id'].apply(np.int64)
        patients = tuple(map(int, list((tempp['patient_id']).unique())))
        pt = """
        select
            `id` as `patient-id`, `name` as `patient-name`, `phone`
        from
            `patients` p
        where id in %s
        """
        pts = pd.read_sql_query(pt, mysql.connection, params=[patients])
        pts.columns = [c.replace('-', '_') for c in pts.columns]

        df_bb = pd.merge(left=df_bb, right=pts, how='left', on=['patient_id'])
        cols_to_move = ['patient_id', 'patient_name', 'phone']
        df_bb = df_bb[cols_to_move + [col for col in
                                      df_bb.columns if col not in cols_to_move]]

        # assortment flag
        conditions = [(
                (df_bb.suggested_drug_id.isnull()) &
                (df_bb['assortment_active'] == 0)
        ),

            (df_bb.suggested_drug_id.isnull()) &
            (df_bb['assortment_active'] == 1),

            (df_bb.suggested_drug_id.notnull())
        ]
        choices = ['not-in-assortment', 'in-assortment', 'in-assortment']
        df_bb['flag_assort'] = np.select(conditions, choices)

        # availability flag
        conditions = [
            (df_bb['flag_assort'] == 'not-in-assortment'),
            (df_bb['required_drug_quantity'] > df_bb[
                'suggested_drug_inventory_quantity']),
            (df_bb['required_drug_quantity'] <= df_bb[
                'suggested_drug_inventory_quantity'])
        ]
        choices = ['full', 'short', 'full']
        df_bb['flag_availability'] = np.select(conditions, choices)

        # conversion flag

        # patients who have billed not in same session & same day, make them converted

        # billed in whole day flag
        bil = """
        select
            `patient-id`,
            1 AS `billed`
        from
            `bills-1` b
        where
            `patient-id` in %s
            and date(`created-at`) = %s
        group by
            `patient-id`;
        """
        bills = pd.read_sql_query(bil, mysql.connection, params=[patients, run_date])
        bills.columns = [c.replace('-', '_') for c in bills.columns]
        df_bb = pd.merge(left=df_bb, right=bills[['patient_id', 'billed']],
                         how='left', on=['patient_id'])

        bt = """
        select
            `id` as `pso_id`, `order-number` as `pso-order-number`, 
            `order-type` as `pso-order-type`,
            `patient-id`, `drug-id` as `suggested_drug_id`, 
            `bill-id` as `pso-bill-id`, `created-at` as `pso-date`
        from
            `patients-store-orders` pso
        where
            `patient-id` in %s
            and date(`created-at`) = %s
        group by `id`, `order-number`, `order-type`,
                `patient-id`, `drug-id`, `bill-id`, `created-at`;
        """
        psos = pd.read_sql_query(bt, mysql.connection, params=[patients, run_date])
        psos.columns = [c.replace('-', '_') for c in psos.columns]
        psos.drop_duplicates(['patient_id', 'suggested_drug_id'],
                             keep='last', inplace=True)
        df_bb = pd.merge(left=df_bb, right=psos,
                         how='left', on=['patient_id', 'suggested_drug_id'])
        df_bb['patients_store_orders_id'] = np.where(
            df_bb['patients_store_orders_id'].isnull(),
            df_bb['pso_id'], df_bb['patients_store_orders_id'])
        df_bb['order_number'] = np.where(
            df_bb['order_number'].isnull(),
            df_bb['pso_order_number'], df_bb['order_number'])
        df_bb['bill_id'] = np.where(
            df_bb['bill_id'].isnull(),
            df_bb['pso_bill_id'], df_bb['bill_id'])
        df_bb['order_type'] = np.where(
            df_bb['order_type'].isnull(),
            df_bb['pso_order_type'], df_bb['order_type'])

        # conversion logic
        df_temp = df_bb[(~df_bb.patients_store_orders_id.isnull()) |
                        (df_bb['billed'] == 1)][['session_id']]
        df_temp1 = df_temp.drop_duplicates(subset=['session_id'])
        df_temp1['flag_conversion'] = 'converted'

        df_cc = pd.merge(left=df_bb, right=df_temp1, how='left', on=['session_id'])
        conditions = [(df_cc.flag_conversion.isnull()),
                      (df_cc.flag_conversion.notnull())]
        choices = ['not_converted', 'converted']
        df_cc['flag_conversion'] = np.select(conditions, choices)

        # patient metadata2
        q_code = """
        select
            "id" as "patient_id",
            "total-spend",
            "average-bill-value",
            "number-of-bills",
            "system-age-days",
            "avg-purchase-interval",
            "previous-bill-date",
            "is-repeatable",
            "is-generic",
            "is-chronic",
            "is-ethical",
            "value-segment-anytime",
            "behaviour-segment-anytime",
            "primary-disease"
        from
            "{schema}"."patients-metadata-2" pm
        where
            id in {ptt};
        
        """.format(ptt=patients, schema=read_schema)
        pmeta = rs_db_read.get_df(q_code)
        pmeta.columns = [c.replace('-', '_') for c in pmeta.columns]

        df_dd = pd.merge(left=df_cc, right=pmeta, how='left', on=['patient_id'])

        df_to_upload = df_dd
        df_to_upload.drop(['pso_id', 'pso_order_number', 'pso_order_type',
                           'pso_bill_id', 'pso_date'], axis=1, inplace=True)
        # session-channel
        df_to_upload['session_channel'] = np.where(df_to_upload['session_created_by'].isin(offline_email), 'offline',
                                                   'online')

        # WRITING TO RS-DB
        if debug_mode == 'N':
            logger.info("Writing to RS table: pmf-conversion")
            df_to_upload['run-date'] = dt.datetime.strptime(run_date, '%Y-%m-%d').date()
            df_to_upload['created-at'] = dt.datetime.now(
                tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
            df_to_upload['created-by'] = 'etl-automation'
            df_to_upload['updated-at'] = dt.datetime.now(
                tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
            df_to_upload['updated-by'] = 'etl-automation'
            df_to_upload.columns = [c.replace('_', '-') for c in
                                    df_to_upload.columns]
            table_info = helper.get_table_info(db=rs_db_write,
                                               table_name='pmf-conversion',
                                               schema=write_schema)
            # To Avoid Duplication
            truncate_query = f"""
                    DELETE
                    FROM
                        "{write_schema}"."pmf-conversion"
                    WHERE
                        "run-date" = '{run_date}';
                        """
            logger.info(truncate_query)
            rs_db_write.execute(truncate_query)

            columns = list(table_info['column_name'])
            df_to_upload = df_to_upload[columns]  # required column order

            s3.write_df_to_db(df=df_to_upload,
                              table_name='pmf-conversion',
                              db=rs_db_write, schema=write_schema)

    except Exception as error:
        logger.exception(error)
        logger.info(f"PMF Conversion Code Execution Status: {status}")

    status = 'Success'

    return status


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This is ETL script.")
    parser.add_argument('-e', '--env', default="dev", type=str, required=False)
    parser.add_argument('-et', '--email_to',
                        default="vivek.revi@zeno.health,vijay.pratap@zeno.health,shubham.gupta@zeno.health",
                        type=str, required=False)
    parser.add_argument('-d', '--debug_mode', default="N", type=str,
                        required=False)
    parser.add_argument('-rs', '--run_stores', default="4", type=str,
                        required=False)
    parser.add_argument('-rd', '--run_date', default="YYYY-MM-DD", type=str,
                        required=False)
    parser.add_argument('-offs', '--offline_session', default='generico2@letsreap.com, sonali.meshram@zeno.health',
                        type=str, required=False)
    parser.add_argument('-ons', '--online_session', default='mulund.west@zippin.org', type=str, required=False)

    args, unknown = parser.parse_known_args()

    env = args.env
    os.environ['env'] = env
    email_to = args.email_to
    debug_mode = args.debug_mode
    online_email = args.online_session
    offline_email = args.offline_session

    # JOB EXCLUSIVE PARAMS
    run_stores = args.run_stores.replace(" ", "").split(",")
    run_date = args.run_date

    run_stores = list(map(int, run_stores))
    run_stores = str(run_stores).replace('[', '(').replace(']', ')')
    run_date_list = run_date.split(",")


    logger = get_logger()

    # define connections
    s3 = S3()
    mysql = MySQL(read_only=True)
    rs_db_read = DB(read_only=True)
    rs_db_write = DB(read_only=False)
    read_schema = 'prod2-generico'
    write_schema = 'prod2-generico'

    # open connections
    rs_db_read.open_connection()
    rs_db_write.open_connection()
    mysql.open_connection()

    for run_date in run_date_list:
        if run_date == 'YYYY-MM-DD':  # Take current date
            run_date = dt.date.today().strftime("%Y-%m-%d")

        """ calling the main function """
        status = main(debug_mode, run_stores, run_date, s3, mysql, rs_db_read,
                      rs_db_write, read_schema, write_schema, logger, online_email, offline_email)
        if email_to:
            # SEND EMAIL OF EXECUTION STATUS
            logger.info("Sending email attachments..")
            email = Email()
            email.send_email_file(
                subject=f"PMF Conversion Code (GLUE-{env}) {run_date}: {status}",
                mail_body=f"""
                              Debug Mode: {debug_mode}
                              Run Stores: {run_stores}
                              Run Date: {run_date}
                              Job Params: {args}
                              """,
                to_emails=email_to, file_uris=[])

    # close connections
    rs_db_read.close_connection()
    rs_db_write.close_connection()
    mysql.close()


