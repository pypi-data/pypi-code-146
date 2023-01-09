"""
purpose -- checks default table size in RS and alerts if threshold is crossed
Author -- abhinav.srivastava@zeno.health
"""

import os
import sys
import argparse
import numpy as np
import pandas as pd

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.helper.email.email import Email
from zeno_etl_libs.db.db import DB, MySQL

parser = argparse.ArgumentParser(description="This is ETL custom script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
parser.add_argument('-d', '--default_size', default=1024, type=int, required=False)
parser.add_argument('-m', '--mail_list', default="data@generico.in", type=str, required=False)

args, unknown = parser.parse_known_args()
env = args.env
default_size = args.default_size
mail_list = args.mail_list

os.environ['env'] = env
logger = get_logger()

rs_db = DB()
rs_db.open_connection()

mysql = MySQL(read_only=False)
mysql.open_connection()

email = Email()

SCHEMA = "prod2-generico"
TABLE_NAME = "table-size-config"

try:
    QUERY = """SELECT   TRIM(pgdb.datname) AS Database,
                         TRIM(a.name) AS Table,
                         ((b.mbytes/part.total::decimal)*100)::decimal(5,2) AS pct_of_total,
                         b.mbytes,
                         b.unsorted_mbytes
                FROM     stv_tbl_perm a
                JOIN     pg_database AS pgdb
                  ON     pgdb.oid = a.db_id
                JOIN     ( SELECT   tbl,
                                    SUM( DECODE(unsorted, 1, 1, 0)) AS unsorted_mbytes,
                                    COUNT(*) AS mbytes
                           FROM     stv_blocklist
                           GROUP BY tbl ) AS b
                       ON a.id = b.tbl
                JOIN     ( SELECT SUM(capacity) AS total
                           FROM   stv_partitions
                           WHERE  part_begin = 0 ) AS part
                      ON 1 = 1
                WHERE    a.slice = 0
                ORDER BY 4 desc, db_id, name
            """
    df_rs_size = rs_db.get_df(query=QUERY)
    table_size_conf = f"""select * from "{SCHEMA}"."{TABLE_NAME}";"""
    df_table_size_conf = rs_db.get_df(query=table_size_conf)
    df_imp_tables = pd.merge(df_table_size_conf, df_rs_size,
                             left_on="table-name", right_on="table", how="inner")
    df_imp_tables = df_imp_tables.loc[df_imp_tables['mbytes'] >
                                      df_imp_tables['default-size'].astype(int)]
    df_imp_tables = df_imp_tables.drop(['id', 'schema', 'table-name',
                                        'database', 'unsorted_mbytes'], axis=1)
    df_imp_tables = df_imp_tables[['table', 'pct_of_total', 'mbytes', 'default-size']]
    df_other_tables = pd.merge(df_table_size_conf,
                               df_rs_size, left_on="table-name", right_on="table", how="right")
    df_other_tables_filtered = df_other_tables.loc[df_other_tables[
                                'table-name'].isin([np.NaN, None])]
    df_other_tables_filtered = df_other_tables_filtered[
                                df_other_tables_filtered['mbytes'] > 1024]
    df_other_tables_filtered = df_other_tables_filtered.drop([
                                'id', 'schema', 'table-name', 'database',
                                'unsorted_mbytes'], axis=1)
    df_other_tables_filtered['default-size'] = default_size
    df_other_tables_filtered = df_other_tables_filtered[
                                ['table', 'pct_of_total', 'mbytes', 'default-size']]
    final_df = pd.concat([df_imp_tables, df_other_tables_filtered])
    final_df.columns = ['table_name', '%_of_total_RS',
                        'Actual_size_MB', 'default_size_configured_MB']
    QUERY = """ 
                show tables;
            """
    df_mysql_source = pd.read_sql_query(con=mysql.connection, sql=QUERY)
    final_df = pd.merge(final_df, df_mysql_source, left_on='table_name',
                               right_on='Tables_in_prod2-generico', how='outer', indicator=True)\
        .query("_merge != 'both'").drop('_merge', axis=1).reset_index(drop=True)
    final_df = final_df.drop(['Tables_in_prod2-generico'], axis=1).dropna().sort_values('Actual_size_MB', ascending=False)
    file_path = '/tmp/output.csv'
    final_df.to_csv(file_path)
    email.send_email_file(subject='[Alert] List of ETL tables exceeding size limit',
                          mail_body="list of tables exceeding"
                                    " default size defined are as attached \n",
                          to_emails=mail_list,
                          file_paths=[file_path])

except Exception as error:
    raise Exception from error
finally:
    rs_db.close_connection()
    mysql.close()
