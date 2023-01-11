from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.dataflow_operator import DataFlowPythonOperator
from airflow import configuration

import google.cloud.firestore as firestore
import datetime
import os

#######################################################################################
# PARAMETROS
#######################################################################################
"""nameDAG: DAG name to be deployed """
nameDAG = 'DAG-signals-publisher'
"""trigger_time: UTC time according to https://crontab.guru/ format. e.g. 0 11 * * * = 11:00 UTC = 5:00 CST"""
trigger_time = "0 11 * * *"

default_args = {
    'depends_on_past': True,
    'start_date': datetime.datetime(2021, 11, 5),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': datetime.timedelta(minutes=1),
    'project_id': os.environ.get("GCP_PROJECT_ID", "tranxpert-mvp"),
    'firestore_pending_signal_chunks_collection': os.environ.get("PENDING_SIGNALS_CHUNKS_COLLECTION",
                                                                 "pending_signal_chunks_test"),
    'firestore_signals_queue_collection': os.environ.get("SIGNALS_QUEUE_COLLECTION",
                                                         "signals_queue_test"),
    'model_signals_topic_name': os.environ.get("MODEL_SIGNALS_TOPIC_NAME", "txp-model-serving-signals-test"),
    'dataset': os.environ.get("TELEMETRY_DATASET", "telemetry_test"),
    'data_lake': os.environ.get("DATA_LAKE", "tranxpert-mvp-telemetry-data-lake-test"),
    'composer_resources_bucket': os.environ.get("RESOURCES_BUCKET", "gs://composer-resources-test"),
    'location': os.environ.get('LOCATION')
}


LOCAL_SETUP_FILE = os.path.join(os.path.join(configuration.get('core', 'dags_folder'), 'signals_publisher'), "setup.py")


#######################################################################################


def get_prefix_id(path):
    split_path = path.split("/")[1].split("|")
    return f"{split_path[0]}|{split_path[1]}|{split_path[2]}|{split_path[3]}"


def check_completeness(paths):
    for path in paths:
        split_path = path.split("|")
        if split_path[5] == '0':
            if (int(split_path[4]) + 1) == len(paths):
                return True
    return False


def get_complete_signals(entries):
    by_id = {}
    for entry in entries:
        if entry.to_dict():
            path = entry.get("path")
            prefix_id = get_prefix_id(path)
            if prefix_id in by_id:
                by_id[prefix_id].append(path)
            else:
                by_id[prefix_id] = [path]
    for prefix_id in by_id:
        if check_completeness(by_id[prefix_id]):
            yield by_id[prefix_id]


######################################################

def python_get_signals_from_datalake_and_push_to_queue(ds, **kwargs):
    db = firestore.Client()
    entries = db.collection(default_args['firestore_pending_signal_chunks_collection']).stream()

    paths = list(get_complete_signals(entries))
    firestore_db = firestore.Client()

    for item in paths:
        push_signal_to_signals_queue(get_prefix_id(item[0]), item, firestore_db)
        delete_documents(firestore_db, item)


def delete_documents(db, paths):
    for path in paths:
        doc = path.split("/")[1]
        db.collection(default_args['firestore_pending_signal_chunks_collection']).document(doc).delete()


def push_signal_to_signals_queue(signal_id, paths, db):
    collection = default_args['firestore_signals_queue_collection']
    db.collection(collection).document(signal_id).set({
        "paths": paths
    })


with DAG(nameDAG,
         default_args=default_args,
         catchup=False,
         max_active_runs=3,
         schedule_interval=trigger_time) as dag:
    #############################################################

    t_begin = DummyOperator(task_id="begin")

    task_get_signals_from_datalake_and_push_to_queue = PythonOperator(
        task_id='task_get_signals_from_datalake_and_push_to_queue',
        provide_context=True,
        python_callable=python_get_signals_from_datalake_and_push_to_queue
        )

    task_launch_batch_dataflow = DataFlowPythonOperator(
        task_id='task_launch_batch_dataflow',
        py_file=f'{default_args["composer_resources_bucket"]}/pipelines/telemetry/batch_pipeline/batch_pipeline.py',
        gcp_conn_id='google_cloud_default',
        options={
            "job_name": 'telemetry-batch-from-composer',
            "time_table": f'tranxpert-mvp:{default_args["dataset"]}.time',
            "fft_table": f'tranxpert-mvp:{default_args["dataset"]}.fft',
            "psd_table": f'tranxpert-mvp:{default_args["dataset"]}.psd',
            "time_metrics_table": f'tranxpert-mvp:{default_args["dataset"]}.time_metrics',
            "fft_metrics_table": f'tranxpert-mvp:{default_args["dataset"]}.fft_metrics',
            "psd_metrics_table": f'tranxpert-mvp:{default_args["dataset"]}.psd_metrics',
            "model_signals_topic_name": default_args['model_signals_topic_name'],
            "setup_file": LOCAL_SETUP_FILE,
            "signals_queue_collection": default_args["firestore_signals_queue_collection"],
            "data_lake": default_args["data_lake"]
        },
        dataflow_default_options={
            "project": default_args['project_id'],
            "region": default_args["location"],
            "temp_location": 'gs://telemetry-pipeline-bucket',
        },
        dag=dag
    )

    t_end = DummyOperator(task_id="end")

    #############################################################
    t_begin >> task_get_signals_from_datalake_and_push_to_queue >> task_launch_batch_dataflow >> t_end
