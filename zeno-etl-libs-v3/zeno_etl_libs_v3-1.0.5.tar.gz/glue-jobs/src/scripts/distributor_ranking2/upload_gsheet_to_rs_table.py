"""
created to upload data from ghseet to prod table
(can be modified and used for any such data upload case)
author: vivek.revi@zeno.health
"""

import os
import sys
import argparse

import pandas as pd
import datetime as dt
import numpy as np
from dateutil.tz import gettz

from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.db.db import DB

from zeno_etl_libs.helper.google.sheet.sheet import GoogleSheet
from zeno_etl_libs.helper import helper


def main():
    s3 = S3()

    # Read from GSheet
    gs = GoogleSheet()
    spreadsheet_id = "1AymJanamWzBk8zZ7UrHGerVpXXaVBt-bpplyghJTD5A"
    ast_data = gs.download(data={
        "spreadsheet_id": spreadsheet_id,
        "sheet_name": "Sheet1",
        "listedFields": []})
    df_sheet = pd.DataFrame(ast_data)
    df_sheet.columns = [c.replace('_', '-') for c in df_sheet.columns]

    df_sheet['created-at'] = dt.datetime.now(
        tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
    df_sheet['created-by'] = 'vivek.revi@zeno.health'
    df_sheet['updated-at'] = dt.datetime.now(
        tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
    df_sheet['updated-by'] = 'vivek.revi@zeno.health'

    table_info = helper.get_table_info(db=rs_db_write,
                                       table_name='dc-distributor-mapping',
                                       schema=write_schema)
    columns = list(table_info['column_name'])
    df_sheet = df_sheet[columns]  # required column order
    s3.write_df_to_db(df=df_sheet,
                      table_name='dc-distributor-mapping',
                      db=rs_db_write, schema=write_schema)

    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="This is ETL script.")
    parser.add_argument('-e', '--env', default="dev", type=str, required=False)

    args, unknown = parser.parse_known_args()

    env = args.env
    os.environ['env'] = env

    read_schema = 'prod2-generico'
    write_schema = 'prod2-generico'
    rs_db = DB()
    rs_db_write = DB(read_only=False)

    # open RS connection
    rs_db.open_connection()
    rs_db_write.open_connection()

    """ calling the main function """
    main()

    # close RS connection
    rs_db.close_connection()
    rs_db_write.close_connection()
