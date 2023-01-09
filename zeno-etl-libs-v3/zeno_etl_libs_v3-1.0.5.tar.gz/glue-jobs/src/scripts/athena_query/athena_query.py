import os
import argparse
from datetime import datetime, timedelta
from zeno_etl_libs.db.db import Athena
from zeno_etl_libs.db.db import DB
from zeno_etl_libs.helper.aws.s3 import S3

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False)
args, unknown = parser.parse_known_args()
env = args.env
os.environ['env'] = env

# setting up Athena connection
Athena = Athena()
conn = Athena.connection()

db = DB()
db.open_connection()

table_name = "customer-returns-1"
schema = "prod2-generico-mis-replica-2022-12-07"

last_year_date = datetime.now() - timedelta(365)

# query = f"""select * from "{schema}"."{table_name}" where "closing-date" < date('{last_year_date}') limit 10;"""
query = f"""select * from "{schema}"."{table_name}" limit 10;"""
df = db.get_df(query=query)

# for writing df to Datalake in parquet format
Athena.ingest_df_to_datalake(df, table_name='test')

# query = """select * from out_of_shelf_drug_level;"""
#
# # Reading data from Athena need to pass only query and connection name stored in above step
# df_data = Athena.get_df(query=query)
# print(df_data.to_string())





