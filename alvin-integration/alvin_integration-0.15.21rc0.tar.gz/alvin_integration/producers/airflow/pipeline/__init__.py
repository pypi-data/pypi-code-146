import inspect
import os
import sys

from airflow import settings
from alvin_integration.helper import log_verbose


def create_alvin_dag_current():
    from alvin_integration.producers.airflow.pipeline import dag_metadata_current

    create_alvin_dag("alvin_metadata_dag.py", dag_metadata_current)


def create_alvin_dag_legacy():
    from alvin_integration.producers.airflow.pipeline import dag_metadata_legacy

    create_alvin_dag("alvin_metadata_dag.py", dag_metadata_legacy)


def create_alvin_dag(file_name, dag_module):

    log_verbose("Creating Alvin DAGs.....", True)
    dag_folder = settings.DAGS_FOLDER
    dag_source_code = inspect.getsource(sys.modules[dag_module.__name__])
    with open(os.path.join(dag_folder, file_name), "w") as file:
        file.write(dag_source_code)


def create_alvin_dag_google_composer():
    log_verbose(f"Importing dag metadata dependencies.....")

    from google.cloud import storage

    from alvin_integration.producers.airflow.config import GOOGLE_COMPOSER_BUCKET
    from alvin_integration.producers.airflow.pipeline import dag_metadata_current

    log_verbose(
        f"Creating Alvin DAGs on Google Composer path {GOOGLE_COMPOSER_BUCKET}....."
    )

    dag_source_code = inspect.getsource(sys.modules[dag_metadata_current.__name__])

    client = storage.Client()

    bucket = client.get_bucket(GOOGLE_COMPOSER_BUCKET)

    blob = bucket.blob("dags/alvin_metadata_dag.py")

    blob.upload_from_string(dag_source_code)
