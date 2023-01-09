"""
main wrapper for Distributor Ranking 2.0 algorithm
author: vivek.revi@zeno.health
"""

import os
import sys
import argparse

import pandas as pd
import numpy as np
import datetime as dt
from dateutil.tz import gettz
from ast import literal_eval

from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.db.db import DB, MySQL
from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper import helper
from zeno_etl_libs.helper.email.email import Email

from zeno_etl_libs.utils.distributor_ranking2.distributor_ranking_calc import \
    ranking_calc_dc, ranking_calc_franchisee
from zeno_etl_libs.utils.distributor_ranking2.tech_processing import \
    process_tech_df


def main(debug_mode, reset_date, time_interval_dc, time_interval_franchisee,
         volume_fraction, franchisee_ranking_active, franchisee_stores,
         as_ms_weights_dc_drug_lvl, as_ms_weights_dc_type_lvl,
         pr_weights_dc_drug_lvl, pr_weights_dc_type_lvl,
         weights_franchisee_drug_lvl, weights_franchisee_type_lvl, s3,
         rs_db_read, rs_db_write, read_schema, write_schema):

    mysql_write = MySQL(read_only=False)
    logger.info(f"Debug Mode: {debug_mode}")
    status = 'Failed'

    # define empty variables to return in case of fail
    final_ranks_franchisee = pd.DataFrame()
    ranked_features_franchisee = pd.DataFrame()
    dc_evaluated = []
    franchisee_stores_evaluated = []

    # ensure all weights adds upto 1
    sum_all_wts = sum(list(as_ms_weights_dc_drug_lvl.values())) + \
                  sum(list(as_ms_weights_dc_type_lvl.values())) + \
                  sum(list(pr_weights_dc_drug_lvl.values())) + \
                  sum(list(pr_weights_dc_type_lvl.values())) + \
                  sum(list(weights_franchisee_drug_lvl.values())) + \
                  sum(list(weights_franchisee_type_lvl.values()))
    if sum_all_wts == 6:
        logger.info("All input weights add upto 1 | Continue Execution")
    else:
        logger.info("Input weights does not add upto 1 | Stop Execution")
        return status, reset_date, dc_evaluated, franchisee_stores_evaluated

    try:
        # calculate ranks
        logger.info("Calculating Zippin DC-level Ranking")
        ranked_features_dc, final_ranks_dc = ranking_calc_dc(
                reset_date, time_interval_dc, as_ms_weights_dc_drug_lvl,
                as_ms_weights_dc_type_lvl, pr_weights_dc_drug_lvl,
                pr_weights_dc_type_lvl, logger, db=rs_db_read, schema=read_schema)

        if franchisee_ranking_active == 'Y':
            logger.info("Calculating Franchisee-level Ranking")
            ranked_features_franchisee, \
                final_ranks_franchisee = ranking_calc_franchisee(
                    reset_date, time_interval_franchisee, franchisee_stores,
                    weights_franchisee_drug_lvl, weights_franchisee_type_lvl,
                    logger, db=rs_db_read, schema=read_schema)
        else:
            logger.info("Skipping Franchisee-level Ranking")

        # process ranked dfs to tech required format
        distributor_ranking_rules, \
        distributor_ranking_rule_values = process_tech_df(
            final_ranks_dc, final_ranks_franchisee, volume_fraction)

        # combine rank df and feature df (dc & franchisee)
        final_ranks = pd.concat([final_ranks_dc, final_ranks_franchisee], axis=0)
        ranked_features = pd.concat([ranked_features_dc, ranked_features_franchisee], axis=0)
        ranked_features.rename(
            {"partial_dc_id": "dc_id", "partial_distributor_id": "distributor_id",
             "partial_distributor_credit_period": "distributor_credit_period",
             "partial_distributor_name": "distributor_name"}, axis=1, inplace=True)
        final_ranks.rename(
            {"partial_dc_id": "dc_id"}, axis=1, inplace=True)

        # for email info
        dc_evaluated = distributor_ranking_rules["dc_id"].unique().tolist()
        franchisee_stores_evaluated = distributor_ranking_rules[
            "store_id"].unique().tolist()

        # adding required fields in tech df
        distributor_ranking_rules['rule_start_date'] = reset_date
        distributor_ranking_rules['is_active'] = 1
        distributor_ranking_rules['created_at'] = dt.datetime.now(
            tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
        distributor_ranking_rules['created_by'] = 'etl-automation'

        # adding required fields in ds-internal df
        final_ranks.loc[:, 'reset_date'] = reset_date
        final_ranks['created_at'] = dt.datetime.now(
            tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
        final_ranks['created_by'] = 'etl-automation'
        final_ranks['updated_at'] = dt.datetime.now(
            tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
        final_ranks['updated_by'] = 'etl-automation'

        ranked_features.loc[:, 'reset_date'] = reset_date
        ranked_features['created_at'] = dt.datetime.now(
            tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
        ranked_features['created_by'] = 'etl-automation'
        ranked_features['updated_at'] = dt.datetime.now(
            tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
        ranked_features['updated_by'] = 'etl-automation'

        # formatting column names
        distributor_ranking_rule_values.columns = [c.replace('_', '-') for c in
                                                   distributor_ranking_rule_values.columns]
        distributor_ranking_rules.columns = [c.replace('_', '-') for c in
                                             distributor_ranking_rules.columns]
        final_ranks.columns = [c.replace('_', '-') for c in final_ranks.columns]
        ranked_features.columns = [c.replace('_', '-') for c in ranked_features.columns]

        if debug_mode == 'N':
            logger.info("Writing table to RS-DB")
            logger.info("Writing to table: distributor-ranking2-features")
            table_info = helper.get_table_info(db=rs_db_write,
                                               table_name='distributor-ranking2-features',
                                               schema=write_schema)
            columns = list(table_info['column_name'])
            ranked_features = ranked_features[columns]  # required column order
            s3.write_df_to_db(df=ranked_features,
                              table_name='distributor-ranking2-features',
                              db=rs_db_write, schema=write_schema)

            logger.info("Writing to table: distributor-ranking2-final-ranks")
            table_info = helper.get_table_info(db=rs_db_write,
                                               table_name='distributor-ranking2-final-ranks',
                                               schema=write_schema)
            columns = list(table_info['column_name'])
            final_ranks = final_ranks[columns]  # required column order
            s3.write_df_to_db(df=final_ranks,
                              table_name='distributor-ranking2-final-ranks',
                              db=rs_db_write, schema=write_schema)
            logger.info("Writing table to RS-DB completed!")

            mysql_write.open_connection()
            logger.info("Updating table to MySQL")
            try:
                index_increment = int(
                    pd.read_sql(
                        'select max(id) from `distributor-ranking-rules`',
                        con=mysql_write.connection).values[0]) + 1
                redundant_increment = int(
                    pd.read_sql(
                        'select max(id) from `distributor-ranking-rule-values`',
                        con=mysql_write.connection).values[0]) + 1
            except:
                index_increment = 1
                redundant_increment = 1

            logger.info(f"Incremented distributor-ranking-rules by {index_increment}")
            logger.info(f"Incremented distributor-ranking-rule-values by {redundant_increment}")

            distributor_ranking_rules['id'] = distributor_ranking_rules['id'] + index_increment
            distributor_ranking_rule_values['distributor-ranking-rule-id'] = distributor_ranking_rule_values[
                'distributor-ranking-rule-id'] + index_increment
            distributor_ranking_rule_values['id'] = distributor_ranking_rule_values['id'] + redundant_increment

            logger.info("Setting existing rules to inactive")
            mysql_write.engine.execute("UPDATE `distributor-ranking-rules` SET `is-active` = 0")
            # mysql_write.engine.execute("SET FOREIGN_KEY_CHECKS=0") # use only in staging

            logger.info("Writing to table: distributor-ranking-rules")
            distributor_ranking_rules.to_sql(
                name='distributor-ranking-rules',
                con=mysql_write.engine,
                if_exists='append', index=False,
                method='multi', chunksize=10000)
            logger.info("Writing to table: distributor-ranking-rule-values")
            distributor_ranking_rule_values.to_sql(
                name='distributor-ranking-rule-values',
                con=mysql_write.engine,
                if_exists='append', index=False,
                method='multi', chunksize=10000)

            # mysql_write.engine.execute("SET FOREIGN_KEY_CHECKS=1") # use only in staging
            logger.info("Updating table to MySQL completed!")
            mysql_write.close()

        else:
            logger.info("Writing to RS-DB & MySQL skipped")

        status = 'Success'
        logger.info(f"Distributor Ranking code execution status: {status}")

    except Exception as error:
        logger.exception(error)
        logger.info(f"Distributor Ranking code execution status: {status}")

    return status, reset_date, dc_evaluated, franchisee_stores_evaluated


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This is ETL script.")
    parser.add_argument('-e', '--env', default="dev", type=str, required=False)
    parser.add_argument('-et', '--email_to',
                        default="vivek.revi@zeno.health", type=str,
                        required=False)

    parser.add_argument('-d', '--debug_mode', default="N", type=str,
                        required=False)
    parser.add_argument('-rd', '--reset_date', default="YYYY-MM-DD", type=str,
                        required=False)
    parser.add_argument('-ti', '--time_interval_dc', default=90, type=int,
                        required=False)
    parser.add_argument('-tif', '--time_interval_franchisee', default=180, type=int,
                        required=False)
    parser.add_argument('-vf', '--volume_fraction', default="0.5-0.3-0.2", type=str,
                        required=False)
    parser.add_argument('-fra', '--franchisee_ranking_active', default="N", type=str,
                        required=False)
    parser.add_argument('-fs', '--franchisee_stores', default=[319, 320],
                        nargs='+', type=int, required=False)
    parser.add_argument('-amwdcdl', '--as_ms_weights_dc_drug_lvl',
                        default="{'margin':0.5,'ff':0.5}",
                        type=str, required=False)
    parser.add_argument('-amwdctl', '--as_ms_weights_dc_type_lvl',
                        default="{'margin':0.3,'ff':0.3, 'portfolio_size':0.4}",
                        type=str, required=False)
    parser.add_argument('-prwdcdl', '--pr_weights_dc_drug_lvl',
                        default="{'margin':0.4,'ff':0.6}",
                        type=str, required=False)
    parser.add_argument('-prwdctl', '--pr_weights_dc_type_lvl',
                        default="{'margin':0.2,'ff':0.4, 'portfolio_size':0.4}",
                        type=str, required=False)
    parser.add_argument('-wfdl', '--weights_franchisee_drug_lvl',
                        default="{'margin':0.5,'ff':0.5}",
                        type=str, required=False)
    parser.add_argument('-wftl', '--weights_franchisee_type_lvl',
                        default="{'margin':0.3,'ff':0.3, 'portfolio_size':0.4}",
                        type=str, required=False)

    args, unknown = parser.parse_known_args()

    env = args.env
    os.environ['env'] = env
    email_to = args.email_to

    # JOB EXCLUSIVE PARAMS
    debug_mode = args.debug_mode
    reset_date = args.reset_date
    time_interval_dc = args.time_interval_dc
    time_interval_franchisee = args.time_interval_franchisee
    volume_fraction = args.volume_fraction
    franchisee_ranking_active = args.franchisee_ranking_active
    franchisee_stores = args.franchisee_stores
    as_ms_weights_dc_drug_lvl = args.as_ms_weights_dc_drug_lvl
    as_ms_weights_dc_type_lvl = args.as_ms_weights_dc_type_lvl
    pr_weights_dc_drug_lvl = args.pr_weights_dc_drug_lvl
    pr_weights_dc_type_lvl = args.pr_weights_dc_type_lvl
    weights_franchisee_drug_lvl = args.weights_franchisee_drug_lvl
    weights_franchisee_type_lvl = args.weights_franchisee_type_lvl

    # EVALUATE REQUIRED JSON PARAMS
    as_ms_weights_dc_drug_lvl = literal_eval(as_ms_weights_dc_drug_lvl)
    as_ms_weights_dc_type_lvl = literal_eval(as_ms_weights_dc_type_lvl)
    pr_weights_dc_drug_lvl = literal_eval(pr_weights_dc_drug_lvl)
    pr_weights_dc_type_lvl = literal_eval(pr_weights_dc_type_lvl)
    weights_franchisee_drug_lvl = literal_eval(weights_franchisee_drug_lvl)
    weights_franchisee_type_lvl = literal_eval(weights_franchisee_type_lvl)

    if reset_date == 'YYYY-MM-DD':
        reset_date = dt.date.today()
    else:
        reset_date = dt.datetime.strptime(reset_date, "%Y-%m-%d").date()

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
    status, reset_date, dc_evaluated, \
        franchisee_stores_evaluated = main(
            debug_mode, reset_date, time_interval_dc, time_interval_franchisee,
            volume_fraction, franchisee_ranking_active, franchisee_stores,
            as_ms_weights_dc_drug_lvl, as_ms_weights_dc_type_lvl,
            pr_weights_dc_drug_lvl, pr_weights_dc_type_lvl,
            weights_franchisee_drug_lvl, weights_franchisee_type_lvl, s3,
            rs_db_read, rs_db_write, read_schema, write_schema)

    # close RS connection
    rs_db_read.close_connection()
    rs_db_write.close_connection()

    # SEND EMAIL ATTACHMENTS
    logger.info("Sending email attachments..")
    email = Email()
    email.send_email_file(
        subject=f"Distributor Ranking 2.0 Reset (SM-{env}) {reset_date}: {status}",
        mail_body=f"""
                Debug Mode: {debug_mode}
                DC's Evaluated: {dc_evaluated}
                Franchisee Stores Evaluated: {franchisee_stores_evaluated}
                Job Params: {args}
                """,
        to_emails=email_to)

    logger.info("Script ended")
