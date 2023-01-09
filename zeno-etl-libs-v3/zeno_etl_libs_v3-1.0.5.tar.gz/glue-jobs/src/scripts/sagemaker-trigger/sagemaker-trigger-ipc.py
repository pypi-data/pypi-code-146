"""
CAUTION:
This is a common script, any changes to this script will be reflected across all
ipc sagemaker triggers
"""

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import json
import os
import time
import datetime as dt
import pandas as pd

sys.path.append('../../../..')
from zeno_etl_libs.helper.run_notebook import run_notebook
from zeno_etl_libs.helper.parameter.job_parameter import parameter
from zeno_etl_libs.db.db import PostGre
from zeno_etl_libs.logger import get_logger

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'env', 'in_vpc', 'instance_type',
                                     'timeout_in_sec', 'parameters', 'script_name',
                                     'script_location', 'job_param_id', 'batch_size'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
env = args['env']
os.environ['env'] = env
logger = get_logger()
in_vpc = args['in_vpc']
instance_type = args['instance_type']
timeout_in_sec = args['timeout_in_sec']
parameters = args['parameters']
parameters = json.loads(parameters)
logger.info(type(parameters))
parameters['env'] = env
script_name = args['script_name']
script_location = args['script_location']

# check job params
job_params = parameter.get_params(job_id=int(args['job_param_id']))
reset_stores = job_params["reset_stores"]
batch_size = int(args['batch_size'])

# batch_size cannot be 0
if batch_size <= 0:
        batch_size = 1

if reset_stores == [0]:
        # QUERY TO GET SCHEDULED STORES AND TYPE FROM OPS ORACLE
        reset_date = dt.date.today().strftime("%Y-%m-%d")
        pg_internal = PostGre(is_internal=True)
        pg_internal.open_connection()
        reset_store_query = """
                SELECT
                    "ssr"."id" as object_id,
                    "s"."bpos_store_id" as store_id,
                    "dc"."slug" as type,
                    "ssr"."drug_grade"
                FROM
                    "safety_stock_reset_drug_category_mapping" ssr
                    INNER JOIN "ops_store_manifest" osm
                    ON ( "ssr"."ops_store_manifest_id" = "osm"."id" )
                    INNER JOIN "retail_store" s
                    ON ( "osm"."store_id" = "s"."id" )
                    INNER JOIN "drug_category" dc
                    ON ( "ssr"."drug_category_id" = "dc"."id")
                WHERE
                    (
                        ( "ssr"."should_run_daily" = TRUE OR
                            "ssr"."trigger_dates" && ARRAY[ date('{reset_date}')] )
                        AND "ssr"."is_auto_generate" = TRUE
                        AND "osm"."is_active" = TRUE
                    AND "osm"."is_generate_safety_stock_reset" = TRUE
                    AND "dc"."is_safety_stock_reset_enabled" = TRUE
                    AND "dc"."is_active" = TRUE
                    )
                """.format(reset_date=reset_date)
        reset_store_ops = pd.read_sql_query(reset_store_query,
                                            pg_internal.connection)
        pg_internal.close_connection()

        # get scheduled stores and create batch split
        reset_stores = reset_store_ops['store_id'].unique().tolist()
        store_batch_split = [reset_stores[i:i+batch_size]
                             for i in range(0, len(reset_stores), batch_size)]

else:
        store_batch_split = [reset_stores[i:i+batch_size]
                             for i in range(0, len(reset_stores), batch_size)]

# spawn sagemaker instances for each batch
for batch_stores in store_batch_split:
        run_batch = store_batch_split.index(batch_stores) + 1
        tot_batch = len(store_batch_split)

        # add to parameters
        parameters["run_batch"] = run_batch
        parameters["tot_batch"] = tot_batch
        parameters["batch_stores"] = batch_stores

        run_notebook.execute_notebook(
                image=env + "-notebook-runner",
                input_path=f"s3://aws-{env}-glue-assets-921939243643-ap-south-1/artifact/sagemaker-jobs/scripts/" + script_location + "/" + script_name,
                output_prefix=run_notebook.get_output_prefix(),
                notebook=script_location + '/' + script_name,
                parameters=parameters,
                role="arn:aws:iam::921939243643:role/service-role/AmazonSageMaker-ExecutionRole-20220412T145187",
                env=env,
                instance_type=instance_type,
                session=None,
                in_vpc=in_vpc,
                timeout_in_sec=int(timeout_in_sec)
            )

        # to have a time difference for preventing same sagemaker job name
        time.sleep(1)

job.init(args['JOB_NAME'], args)
job.commit()