"""""
 To update store-drug-assortment mysql table from gsheet (Presently only for Mulund west)
 Author : neha.karekar@zeno.health
"""""

import argparse
import sys
import os

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.email.email import Email
from zeno_etl_libs.db.db import DB, MySQL
from zeno_etl_libs.helper.aws.s3 import S3
from zeno_etl_libs.helper import helper
from zeno_etl_libs.helper.google.sheet.sheet import GoogleSheet
import pandas as pd
import dateutil
import datetime
from dateutil.tz import gettz
import numpy as np

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stag, prod)")
parser.add_argument('-et', '--email_to', default="saurav.maskar@zeno.health,neha.karekar@zeno.health", type=str, required=False)

args, unknown = parser.parse_known_args()

env = args.env
email_to = args.email_to
os.environ['env'] = env
logger = get_logger()

rs_db = DB()
rs_db.open_connection()
mysql_write = MySQL(read_only=False)
mysql_write.open_connection()

s3 = S3()

status = 'Failed'
try:
    # Read from gsheet
    gs = GoogleSheet()
    spreadsheet_id = "1-WRZbBTVX1ANeKPmc2I1kyj2XkG5hu2L-Tau9Fb6lWw"
    schema = 'test-generico'
    if env == 'prod':
        spreadsheet_id = "1tFHCTr3CHdb0UOFseK_ntjAUJSHQHcjLmysPPCWRM04"
        schema = 'prod2-generico'

    ast_data = gs.download(data={
        "spreadsheet_id": spreadsheet_id,
        "sheet_name": "Sheet1",
        "listedFields": []
    })
    df = pd.DataFrame(ast_data)
    df['store-id'] = 4
    df['is-active'] = 1
    df['created-by'] = 'data team'
    df['updated-by'] = 'data team'
    df['created-at'] = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
    df['updated-at'] = datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
    today= datetime.datetime.now(tz=gettz('Asia/Kolkata')).strftime('%Y-%m-%d %H:%M:%S')
    df.columns = [c.replace('_', '-') for c in df.columns]
    df['drug-id'] = df['drug-id'].astype(str)
    df = df[['store-id', 'drug-id', 'is-active', 'created-at', 'created-by', 'updated-at', 'updated-by']]
    df.drop_duplicates(subset=["store-id", "drug-id"],
                       keep=False, inplace=True)

    # existing data
    ast_q = f"""
        select id,
            `drug-id`,
            `store-id`,
            `is-active`
        from
            `{schema}`.`store-drug-assortment`
            """
    ast_table = pd.read_sql_query(ast_q, mysql_write.connection)
    ast_table['drug-id'] = ast_table['drug-id'].astype(str)
    # set active to zero for below records
    mysql_write.engine.execute(f"UPDATE  `{schema}`.`store-drug-assortment` SET `is-active` = 0, `updated-at`='{today}'")
    left_data = df.merge(ast_table, on=["drug-id"], how='left')
    # set active to one for common records
    keep_left_data = left_data.loc[left_data['id'].notnull()]
    # append below new records
    append_left_data = left_data.loc[left_data['id'].isnull()]
    tuple_id = tuple(keep_left_data['id'].unique().tolist())
    if not tuple_id:
        tuple_id = str('(0)')

    # update
    mysql_write.engine.execute(f"UPDATE  `{schema}`.`store-drug-assortment` SET `is-active` = 1,`updated-at`='{today}' where `id` in {tuple_id}")
    print(f"UPDATE  `{schema}`.`store-drug-assortment` SET `is-active` = 1 and `updated-at`='{today}' where `id` in {tuple_id}")
    print(tuple_id)
    # append
    append_left_data.drop(['id', 'store-id_y', 'is-active_y'], axis=1, inplace=True)
    append_left_data = append_left_data.reset_index()
    append_left_data.rename({'store-id_x': 'store-id', 'is-active_x': 'is-active', 'index': 'id'}, axis=1, inplace=True)
    ast_table_max_id = ast_table['id'].max()
    if np.isnan(ast_table_max_id):
        ast_table_max_id = 0

    append_left_data['id'] = append_left_data['id'] + ast_table_max_id + 1
    append_left_data['drug-id'] = append_left_data['drug-id'].astype('int')
    append_left_data['created-at'] = pd.to_datetime(append_left_data['created-at'])
    append_left_data['updated-at'] = pd.to_datetime(append_left_data['updated-at'])
    append_left_data.drop_duplicates(subset=["store-id", "drug-id"],
                                     keep=False, inplace=True)
    append_left_data.to_sql(
        name='store-drug-assortment',
        con=mysql_write.engine,
        if_exists='append', index=False,
        method='multi', chunksize=1000)
    status = 'Success'
except:
    status = 'Failed'


email = Email()
email.send_email_file(subject=f"{env}-{status} : store-drug-assortment table update",
                      mail_body=f"table update status - {status}",
                      to_emails=email_to, file_uris=[])


rs_db.close_connection()
mysql_write.close()
