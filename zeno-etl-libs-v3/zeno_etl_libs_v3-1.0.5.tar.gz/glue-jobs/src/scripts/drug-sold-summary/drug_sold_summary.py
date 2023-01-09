"""
Owner: kuldeep.singh@zeno.health
Purpose: This script calculates the drug substitutes. Which means, what all drug ids can be
substituted by each other.
And lastly, it is stored in a table.
"""
import argparse
import os
import sys

import pandas as pd

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.db.db import MySQL, DB

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stage, prod)")
parser.add_argument('-mtp', '--main_table_prefix', default="NA", type=str, required=False)
parser.add_argument('-ttp', '--temp_table_prefix', default="pre", type=str, required=False)
parser.add_argument('-bs', '--batch_size', default=10, type=int, required=False)
parser.add_argument('-td', '--total_drugs', default=30, type=int, required=False)

args, unknown = parser.parse_known_args()
env = args.env
batch_size = args.batch_size
total_drugs = args.total_drugs
main_table_prefix = args.main_table_prefix
temp_table_prefix = f"-{args.temp_table_prefix}"
main_table_prefix = "" if main_table_prefix == "NA" else main_table_prefix

os.environ['env'] = env
logger = get_logger()

table_name = "drug-sold-summary"

""" Setting the schema name as per the env """
if env == "dev":
    ms_source_schema = "test-generico"
    rs_source_schema = "test-generico"
elif env == "stage":
    ms_source_schema = "test-generico"
    rs_source_schema = "test-generico"
elif env == "prod":
    ms_source_schema = "prod2-generico"
    rs_source_schema = "prod2-generico"
else:
    raise Exception("Set the env first!")

ms_target_schema = ms_source_schema

temp_table_name = f"`{ms_target_schema}`.`{table_name}{temp_table_prefix}`"
main_table_name = f"`{ms_target_schema}`.`{table_name}{main_table_prefix}`"

logger.info(f"temp_table_name: {temp_table_name}")
logger.info(f"main_table_name: {main_table_name}")


def get_drug_summary_mysql(mysql_read_db, batch=1, batch_size=10000):
    query = f"""
    select
        i.`drug-id` ,
        COUNT(distinct b2.`patient-id`) as `sold-count`
    from
        `{ms_source_schema}`.`inventory-1` i
    inner join `{ms_source_schema}`.`bill-items-1` bi on
        i.id = bi.`inventory-id`
    inner join `{ms_source_schema}`.`bills-1` b2 on
        bi.`bill-id` = b2.id
    group by
        i.`drug-id`
    order by
        i.`drug-id`
    LIMIT {batch_size} OFFSET {(batch - 1) * batch_size};
    """

    logger.info(f"query to get the data: {query}")

    df = pd.read_sql_query(con=mysql_read_db.connection, sql=query)

    return df


def get_drug_summary_redshift(redshift_read_db, batch=1, batch_size=10000):
    query = f"""
    select
        i."drug-id" ,
        COUNT(distinct b2."patient-id") as "sold-count"
    from
        "{rs_source_schema}"."inventory-1" i
    inner join "{rs_source_schema}"."bill-items-1" bi on
        i.id = bi."inventory-id"
    inner join "{rs_source_schema}"."bills-1" b2 on
        bi."bill-id" = b2.id
    group by
        i."drug-id"
    order by
        i."drug-id"
    """

    logger.info(f"query to get the data: {query}")

    df = redshift_read_db.get_df(query=query)

    return df


def get_drug_summary_doctor_redshift(redshift_read_db, batch=1, batch_size=10000):
    query = f"""
        select
            i."drug-id",
            COUNT(distinct b2."patient-id") as "sold-to-doctors-count"
        from
            "{rs_source_schema}"."inventory-1" i
        inner join "{rs_source_schema}"."bill-items-1" bi on
            i.id = bi."inventory-id"
        inner join "{rs_source_schema}"."bills-1" b2 on
            bi."bill-id" = b2.id
        inner join "{rs_source_schema}".patients p on
            b2."patient-id" = p.id
        where
            lower(p."name") like 'dr %'
        group by
            i."drug-id"
        order by
            i."drug-id"
    """

    logger.info(f"query to get the data: {query}")

    df = redshift_read_db.get_df(query=query)

    return df


mysql_write_db = MySQL(read_only=False)
mysql_write_db.open_connection()

# Truncate the temp table before starting
query = f""" delete from  {temp_table_name};"""
mysql_write_db.engine.execute(query)

logger.info(f"deleted from temp table, query: {query}")

#
# mysql_read_db = MySQL()
# mysql_read_db.open_connection()

redshift_read_db = DB()
redshift_read_db.open_connection()

# query = "SELECT count(id) as `drug-count` FROM `{ms_source_schema}`.drugs "
# c_df = pd.read_sql_query(con=mysql_read_db.connection, sql=query)

# drug_summary_df = pd.DataFrame()
# total_drugs = 125000
# for i in range(1, round(total_drugs / batch_size) + 1):
#     temp_df = get_drug_summary_mysql(mysql_read_db=mysql_read_db, batch=i,
#                                      batch_size=batch_size)  # to consider NA moles drugs
#     drug_summary_df = pd.concat([drug_summary_df, temp_df])
#     logger.info(f"fetched batch: {i}")
# mysql_read_db.close()

drug_summary_df = get_drug_summary_redshift(redshift_read_db=redshift_read_db)
drug_doctor_summary_df = get_drug_summary_doctor_redshift(redshift_read_db=redshift_read_db)
drug_summary_df = drug_summary_df.merge(drug_doctor_summary_df, how="left", on="drug-id")
drug_summary_df.fillna(0, inplace=True)
drug_summary_df['sold-to-doctors-count'] = drug_summary_df['sold-to-doctors-count'].astype(int)
redshift_read_db.close_connection()

total_count = len(drug_summary_df)
logger.info(f"Total drug count: {total_count}")

# store the data in the temp table
drug_summary_df[['drug-id', 'sold-count', 'sold-to-doctors-count']].to_sql(
    con=mysql_write_db.engine, name=f"{table_name}{temp_table_prefix}", schema=ms_target_schema,
    if_exists="append", chunksize=500, index=False)

# Delete the drugs from main table which are NOT in the temp table.
query = f""" DELETE FROM t1 USING {main_table_name} t1 LEFT JOIN {temp_table_name} t2 ON
        t1.`drug-id` = t2.`drug-id` where t2.`drug-id` is null ;"""
response = mysql_write_db.engine.execute(query)
logger.info(
    f"Deleted the records from main table, which are absent in temp table: {response.rowcount}")

# Delete the data from temp table which is already present in main table
query = f""" DELETE FROM t1 USING {temp_table_name} t1 INNER JOIN {main_table_name} t2 ON
        t1.`drug-id` = t2.`drug-id` where t1.`sold-count` = t2.`sold-count` 
        and t1.`sold-to-doctors-count` = t2.`sold-to-doctors-count`; """

response = mysql_write_db.engine.execute(query)
present_correct_count = response.rowcount
logger.info(f"Correct drug-ids count: {present_correct_count}")

# Delete the incorrect substitutes from main table
query = f""" DELETE FROM t1 USING {main_table_name} t1 INNER JOIN {temp_table_name} t2 ON
        t1.`drug-id` = t2.`drug-id`;"""

response = mysql_write_db.engine.execute(query)
present_incorrect_count = response.rowcount
logger.info(f"Incorrect drug-ids count: {present_incorrect_count}")

# Now Insert the records in main table
query = f""" INSERT INTO {main_table_name} (`drug-id`, `sold-count`, `sold-to-doctors-count`)
        SELECT `drug-id`, `sold-count`, `sold-to-doctors-count` FROM {temp_table_name} """
response = mysql_write_db.engine.execute(query)
new_insert_count = response.rowcount
logger.info(f"Insert/Update drug-ids count: {new_insert_count}")

mysql_write_db.close()

if total_count == present_correct_count + new_insert_count:
    logger.info("Drug sold-count data updated successfully")
else:
    raise Exception("Data count mismatch")
