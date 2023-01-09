import os
from typing import List

import requests
from alvin_integration.helper import log_verbose
from sqlalchemy.orm.session import Session

from alvin_integration.producers.airflow.config import (
    ALVIN_BACKEND_API_KEY,
    ALVIN_BACKEND_API_URL,
)

ALVIN_PLATFORM_ID = os.getenv("ALVIN_PLATFORM_ID")


def get_airflow_version():
    import airflow

    return airflow.__version__


def get_dag_source_code(dag_location):
    if dag_location:
        with open(dag_location, "r") as f:
            content = f.read()
        return content


def extract_dag_metadata(session: Session):
    from airflow.models.dag import DagModel
    from airflow.serialization.serialized_objects import SerializedDAG

    alvin_backend_metadata_url = f"{ALVIN_BACKEND_API_URL}/api/v1/metadata"
    entities = []
    all_dags_models: List[DagModel] = DagModel().get_all_dagmodels(session)

    for dag_model in all_dags_models:
        if not hasattr(dag_model.serialized_dag, "dag"):
            continue

        dag = dag_model.serialized_dag.dag
        dag_metadata = SerializedDAG.to_dict(dag)

        enrich_dag_metadata(dag_metadata, dag_model, dag)
        entities.append(dag_metadata["dag"])
    payload = {
        "alvin_platform_id": ALVIN_PLATFORM_ID,
        "facets": {
            "airflow_version": get_airflow_version(),
            "platform_type": "AIRFLOW",
        },
        "entities": entities,
    }
    requests.post(
        alvin_backend_metadata_url,
        json=payload,
        headers={"X-API-KEY": ALVIN_BACKEND_API_KEY},
    )
    log_verbose(f"Metadata extracted: {payload}")


def enrich_dag_metadata(dag_metadata, dag_model, dag):
    "Adds metadata fields to dag metadata"

    dag_metadata["dag"]["source_code"] = get_dag_source_code(
            dag_metadata["dag"].get("fileloc")
        )
    dag_metadata["dag"]["is_active"] = dag_model.is_active
    dag_metadata["dag"]["leaves"] = [task.task_id for task in dag.leaves]
    dag_metadata["dag"]["roots"] = [task.task_id for task in dag.roots]
    for task in dag_metadata["dag"].get("tasks", []):
        task_instance = dag.task_dict.get(task["task_id"])
        task["_upstream_task_ids"] = list(task_instance.upstream_task_ids) if task_instance else []
        task["operator_type"] = task_instance.task_type if task_instance else task.get("_task_type")
