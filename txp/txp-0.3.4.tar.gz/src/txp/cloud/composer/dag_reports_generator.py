import pytz
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.contrib.operators.dataflow_operator import DataFlowPythonOperator
from airflow import configuration
import datetime
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
#######################################################################################
# PARAMETERS
#######################################################################################

nameDAG = 'dag_reports_generator'

default_args = {
    'depends_on_past': True,
    'start_date': datetime.datetime(2021, 11, 5),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': datetime.timedelta(minutes=1),
    'project_id': os.environ.get("GCP_PROJECT_ID", "tranxpert-mvp"),
    'dataset': os.environ.get("REPORTS_DATASET", "reports"),
    'reports_bucket': os.environ.get("REPORTS_BUCKET", "txp-reports"),
    'trigger_time': "0 11 * * *",
    "composer_resources_bucket": os.environ.get("RESOURCES_BUCKET", "gs://composer-resources"),
    'location': os.environ.get('LOCATION', 'us-west4')
}

LOCAL_SETUP_FILE = os.path.join(os.path.join(configuration.get('core', 'dags_folder'), 'reports_generator'), 'setup.py')

#######################################################################################

with DAG(nameDAG,
         default_args=default_args,
         catchup=False,
         max_active_runs=3,
         schedule_interval=default_args["trigger_time"]) as dag:
    t_begin = DummyOperator(task_id="begin")

    task_launch_batch_dataflow = DataFlowPythonOperator(
        task_id='task_launch_batch_dataflow',
        py_file=f'{default_args["composer_resources_bucket"]}/pipelines/reports/batch_pipeline/batch_pipeline.py',
        gcp_conn_id='google_cloud_default',
        options={
            "job_name": 'reports-batch-from-composer',
            "reports_dataset": "tranxpert-mvp:reports",
            "reports_bucket_name": default_args["reports_bucket"],
            "setup_file": LOCAL_SETUP_FILE,
        },
        dataflow_default_options={
            "project": default_args['project_id'],
            "region": default_args["location"],
            "temp_location": 'gs://txp-reports-bucket',
        },
        dag=dag
    )

    t_end = DummyOperator(task_id="end")

    t_begin >> task_launch_batch_dataflow >> t_end
