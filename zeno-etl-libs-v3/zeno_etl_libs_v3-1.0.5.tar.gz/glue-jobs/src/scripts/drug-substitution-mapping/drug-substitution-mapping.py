"""
Owner: kuldeep.singh@zeno.health
Purpose: This script calculates the drug substitutes. Which means, what all drug ids can be
substituted by each other.
And lastly, it is stored in a table.
"""
import argparse
import datetime
import os
import sys

import pandas as pd

sys.path.append('../../../..')

from zeno_etl_libs.logger import get_logger
from zeno_etl_libs.db.db import MySQL
from zeno_etl_libs.helper.aws.s3 import S3

parser = argparse.ArgumentParser(description="This is ETL script.")
parser.add_argument('-e', '--env', default="dev", type=str, required=False,
                    help="This is env(dev, stage, prod)")
parser.add_argument('-mtp', '--main_table_prefix', default="NA", type=str, required=False)
parser.add_argument('-ttp', '--temp_table_prefix', default="pre", type=str, required=False)
parser.add_argument('-bs', '--batch_size', default=10000, type=int, required=False)
parser.add_argument('-td', '--total_drugs', default=100000, type=int, required=False)

args, unknown = parser.parse_known_args()
env = args.env
batch_size = args.batch_size
total_drugs = args.total_drugs
main_table_prefix = args.main_table_prefix
temp_table_prefix = f"-{args.temp_table_prefix}"
main_table_prefix = "" if main_table_prefix == "NA" else main_table_prefix

os.environ['env'] = env
logger = get_logger()

table_name = "drug-substitution-mapping"

""" Setting the schema name as per the env """
if env == "dev":
    ms_source_schema = "test-generico"
elif env == "stage":
    ms_source_schema = "test-generico"
elif env == "prod":
    ms_source_schema = "prod2-generico"
else:
    raise Exception("Set the env first!")

# rs_source_schema = "test-generico" if env == "stage" else "prod2-generico"
# ms_source_schema = "test-generico" if env == "stage" else "prod2-generico"
ms_target_schema = ms_source_schema

temp_table_name = f"`{ms_target_schema}`.`{table_name}{temp_table_prefix}`"
main_table_name = f"`{ms_target_schema}`.`{table_name}{main_table_prefix}`"

logger.info(f"temp_table_name: {temp_table_name}")
logger.info(f"main_table_name: {main_table_name}")


def get_drug_groups_mysql(mysql_read_db, discard_na_mol_drugs=False, batch=1, batch_size=10000):
    """
    if discard_na_mol_drugs  = False --> Considers the strengths as 0(zero) for unit-type 'NA' molecules
    if discard_na_mol_drugs  = True --> Discards the drugs from substitution logic all together
                                        where unit-type of one or many molecule is 'NA'
    """

    # this filter to discard drugs, which have one or many molecule unit-type as 'NA'
    filter_na_mol_drugs = ""
    if discard_na_mol_drugs:
        filter_na_mol_drugs = f"""
            where
                d.`composition-master-id` not in (
                select
                    DISTINCT `composition-master-id`
                from
                    `{ms_source_schema}`.`composition-master-molecules-master-mapping`
                where
                    (`unit-type-value` = '' or `unit-type` = 'NA') )
        """

    query = f"""
    SELECT
        `drug-id`,
        GROUP_CONCAT(DISTINCT `molecule-combination` ORDER BY `molecule-combination`) as combination,
        md5(GROUP_CONCAT(DISTINCT `molecule-combination`)) as `group`
    from
        (
        SELECT
            `drug-id`,
            CONCAT(' name_or_group:' , dm.`molecule-group-or-name` ,
                ' strength:' , dm.`strength-in-smallest-unit` , dm.`smallest-unit` ,
                ' release-pattern:' , `release-pattern-group` , 
                ' available-in:' , `available-in-group`) as "molecule-combination"
        from
            (
            select
                d.id as `drug-id`,
                case
                    when (mm.`molecule-group` = ''
                    or mm.`molecule-group` is null) then mm.id
                    else mm.`molecule-group`
                end as `molecule-group-or-name`,
                case when cmmmm.`unit-type-value` = '' then 0 else 
                cmmmm.`unit-type-value` * uomm.`smallest-unit-value` end  as `strength-in-smallest-unit`,
                uomm.`smallest-unit` as `smallest-unit`,
                rpm.`group` as `release-pattern-group`,
                aidfm.`available-group` as `available-in-group`
            from
                `{ms_source_schema}`.drugs d
            inner join `{ms_source_schema}`.`composition-master-molecules-master-mapping` cmmmm on
                d.`composition-master-id` = cmmmm.`composition-master-id`
            inner join `{ms_source_schema}`.`molecule-master` mm on
                mm.id = cmmmm.`molecule-master-id`
            inner join `{ms_source_schema}`.`drug-molecule-release` dmr on
                d.id = dmr.`drug-id`
                and cmmmm.`molecule-master-id` = dmr.`molecule-master-id`
            inner join `{ms_source_schema}`.`available-in-group-mapping` aidfm on
                d.`available-in` = aidfm.`available-in`
            inner join `{ms_source_schema}`.`release-pattern-master` rpm on
                dmr.`release` = rpm.name
            inner join `{ms_source_schema}`.`unit-of-measurement-master` uomm on
                cmmmm.`unit-type` = uomm.unit
            {filter_na_mol_drugs}
            ) dm ) a
    group by
        a.`drug-id`
    order by 
        a.`drug-id`
    LIMIT {batch_size} OFFSET {(batch - 1) * batch_size};
    """

    logger.info(f"query to get the data: {query}")

    df = pd.read_sql_query(con=mysql_read_db.connection, sql=query)
    return df



mysql_write_db = MySQL(read_only=False)
mysql_write_db.open_connection()

# Truncate the temp table before starting
query = f""" delete from  {temp_table_name};"""
mysql_write_db.engine.execute(query)

logger.info(f"deleted from temp table, query: {query}")
# drug_group_df = get_drug_groups_redshift()

# drug_group_df = get_drug_groups_mysql(discard_na_mol_drugs=False)  # to discard NA moles drugs
drug_group_df = pd.DataFrame()

mysql_read_db = MySQL()
mysql_read_db.open_connection()
# query = "SELECT count(id) as `drug-count` FROM `{ms_source_schema}`.drugs "
# c_df = pd.read_sql_query(con=mysql_read_db.connection, sql=query)

s3 = S3(bucket_name=f"{env}-zeno-s3-db")

# total_drugs = 125000
for i in range(1, round(total_drugs / batch_size) + 1):
    temp_df = get_drug_groups_mysql(mysql_read_db=mysql_read_db, discard_na_mol_drugs=True, batch=i,
                                    batch_size=batch_size)  # to consider NA moles drugs
    drug_group_df = pd.concat([drug_group_df, temp_df])
    logger.info(f"fetched batch: {i}")
mysql_read_db.close()

total_count = len(drug_group_df)
logger.info(f"Total drug count: {total_count}")

# store the data in the temp table
drug_group_df.to_sql(
    con=mysql_write_db.engine, name=f"{table_name}{temp_table_prefix}", schema=ms_target_schema,
    if_exists="append", chunksize=500, index=False)

# # This is correct query but lock the transaction.
# query = f""" DELETE FROM t1 USING {main_table_name} t1 LEFT JOIN {temp_table_name} t2 ON
#         t1.`drug-id` = t2.`drug-id` where t2.`drug-id` is null ;"""

# # Delete the drugs which are NOT in the temp table.
# query = f""" DELETE FROM t1 USING {main_table_name} t1 JOIN {temp_table_name} t2 ON
#         ( t1.`drug-id` = t2.`drug-id` and t2.`drug-id` is null );"""


# response = mysql_write_db.engine.execute(query)
# logger.info(
#     f"Delete the records from main table, which are absent in temp table: {response.rowcount}")
#
# # Delete the data from temp table which is already present in main table
# query = f""" DELETE FROM t1 USING {temp_table_name} t1 INNER JOIN {main_table_name} t2 ON
#         ( t1.`drug-id` = t2.`drug-id` and t1.group = t2.group); """
#
# response = mysql_write_db.engine.execute(query)
# present_correct_count = response.rowcount
# logger.info(f"Correct drug-ids count: {present_correct_count}")
#
# # Delete the incorrect substitutes from main table
# query = f""" DELETE FROM t1 USING {main_table_name} t1 INNER JOIN {temp_table_name} t2 ON
#         ( t1.`drug-id` = t2.`drug-id` );"""
#
# response = mysql_write_db.engine.execute(query)
# present_incorrect_count = response.rowcount
# logger.info(f"Incorrect drug-ids count: {present_incorrect_count}")

logger.info("Delete main table: start")
# Method 2: delete all the records from main and refill #
query = f""" delete from  {main_table_name};"""
mysql_write_db.engine.execute(query)

# Now Insert the records in main table
query = f""" INSERT INTO {main_table_name} (`drug-id`, `combination`, `group`)
        SELECT `drug-id`, `combination`, `group` FROM {temp_table_name} """
response = mysql_write_db.engine.execute(query)
new_insert_count = response.rowcount
logger.info(f"Insert/Update drug-ids count: {new_insert_count}")

# log the changes
query = f""" SELECT `drug-id`, `combination`, `group` FROM {temp_table_name}; """
df = pd.read_sql_query(con=mysql_write_db.connection, sql=query)
if not df.empty:
    start_ts = datetime.datetime.now() + datetime.timedelta(days=-1)
    start_ts = start_ts.strftime("%Y-%m-%d-%H-%M-%S")
    f_name = 'drug-substitution-mapping-change-log/{}/data.csv'.format(
        start_ts[:16].replace("-", "/"))
    uri = s3.save_df_to_s3(df=df, file_name=f_name)
    print(f"changes have been logged at uri: {uri}")
else:
    print("No change detected!")

mysql_write_db.close()

# if total_count == present_correct_count + new_insert_count:
#     logger.info("Drug substitute data updated successfully")
# else:
#     raise Exception("Data count mismatch")
