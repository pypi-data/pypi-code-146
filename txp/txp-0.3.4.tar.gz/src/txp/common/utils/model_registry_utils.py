import google.cloud.firestore as firestore
import txp.common.utils.firestore_utils
from google.cloud import firestore as firestore
from txp.common.config import settings
import logging
from datetime import datetime, timezone
import json

from txp.common.utils.firestore_utils import configuration_reference_field_path, machines_collection_name, \
    pull_current_configuration_from_firestore
from txp.common.ml.models import ModelStateValue, ModelRegistry

configurations_collection_name = settings.firestore.configurations_collection
tenants_collection_name = txp.common.utils.firestore_utils.tenants_collection
configuration_reference_field_path = "configuration_ref"
configuration_id_field = "configuration_id"
log = logging.getLogger(__name__)
edges_collection_name = settings.firestore.edges_collection
machines_collection_name = settings.firestore.machines_collection


def insert_ml_model(db: firestore.Client, model_registry, model_registry_name, collection_name):
    db.collection(collection_name).document(model_registry.metadata.tenant_id). \
        collection(model_registry.metadata.machine_id).document(model_registry.metadata.task_id).collection("models"). \
        document(model_registry_name).set(json.loads(model_registry.json()))


def get_model_registry_doc_ref(db: firestore.Client, tenant_id, machine_id, task_id, model_registry_name,
                               collection_name):
    return db.collection(collection_name).document(tenant_id).collection(machine_id). \
        document(task_id).collection("models").document(model_registry_name)


def set_ml_model_feedback_and_status(db: firestore.Client, tenant_id, machine_id, task_id, model_registry_name,
                                     model_feedback, status, collection_name):
    doc_ref = get_model_registry_doc_ref(db, tenant_id, machine_id, task_id, model_registry_name, collection_name)
    if not doc_ref.get().exists:
        return False
    doc_ref.update({
        "state.value": status,
        "metadata.feedback": json.loads(model_feedback.json())
    })
    return True


def set_error_ml_model(db: firestore.Client, tenant_id, machine_id, task_id, model_registry_name, model_feedback,
                       collection_name):
    return set_ml_model_feedback_and_status(db, tenant_id, machine_id, task_id, model_registry_name, model_feedback,
                                            ModelStateValue.ERROR.value, collection_name)


def acknowledge_ml_model(db: firestore.Client, tenant_id, machine_id, task_id, model_registry_name, model_feedback,
                         collection_name):
    return set_ml_model_feedback_and_status(db, tenant_id, machine_id, task_id, model_registry_name, model_feedback,
                                            ModelStateValue.ACKNOWLEDGE.value, collection_name)


def get_ml_model(db: firestore.Client, tenant_id, machine_id, task_id, model_registry_name, collection_name) -> \
        ModelRegistry:
    doc_ref = get_model_registry_doc_ref(db, tenant_id, machine_id, task_id, model_registry_name, collection_name).get()

    if not doc_ref.exists:
        return None
    try:
        return ModelRegistry(**doc_ref.to_dict())
    except Exception as e:
        log.error(f"Error trying to create ModelRegistry instance based on dict: {e}")
        return None


def set_is_pre_annotating_ml_model(db: firestore.Client, tenant_id, machine_id, task_id, is_pre_annotating,
                                   collection_name):
    doc_ref = get_active_ml_model_doc_ref(db, tenant_id, machine_id, task_id, collection_name)
    if not doc_ref.get().exists:
        return False
    doc_ref.update({
        "state.is_pre_annotating": is_pre_annotating
    })
    return True


def publish_ml_model(db: firestore.Client, tenant_id, machine_id, task_id, model_registry_name, collection_name):
    doc_ref = get_model_registry_doc_ref(db, tenant_id, machine_id, task_id, model_registry_name, collection_name)
    if not doc_ref.get().exists or doc_ref.get().to_dict()['state']['value'] == ModelStateValue.ACTIVE.value:
        return False
    doc_ref.update({
        "state.publishment_date": get_current_utc_datetime_str(),
        "state.deprecation_date": "",
        "state.value": ModelStateValue.ACTIVE.value
    })
    return True


def get_active_ml_model_doc_ref(db: firestore.Client, tenant_id, machine_id, task_id,
                                collection_name):
    documents = db.collection(collection_name).document(tenant_id).collection(machine_id). \
        document(task_id).collection("models"). \
        where("state.value", "==", ModelStateValue.ACTIVE.value).get()

    if not documents:
        return None
    doc = documents[0]
    doc_ref = doc.reference
    return doc_ref


def deprecate_active_ml_model(db: firestore.Client, tenant_id, machine_id, task_id,
                              collection_name):
    doc_ref = get_active_ml_model_doc_ref(db, tenant_id, machine_id, task_id, collection_name)
    if doc_ref is None:
        return None
    doc_ref.update({
        "state.deprecation_date": get_current_utc_datetime_str(),
        "state.value": ModelStateValue.OLD.value
    })

    return doc_ref.get().to_dict()


def get_all_model_registries(db: firestore.Client, tenant_id, machine_id, task_id, collection_name):
    documents = db.collection(collection_name).document(tenant_id).collection(machine_id). \
        document(task_id).collection("models").get()
    models = []
    for doc in documents:
        models.append(doc.to_dict())
    return models


def get_gcs_dataset_prefix(dataset_name, dataset_versions):
    dataset_versions.sort()
    suffix = ""
    for i, tag in enumerate(dataset_versions):
        suffix += tag
        if i + 1 < len(dataset_versions):
            suffix += "_"
    return f"{dataset_name}_{suffix}"


def get_gcs_task_bucket_path(tenant_id, machine_id, task_id):
    return f"{tenant_id}/{machine_id}/{task_id}"


def get_gcs_dataset_file_name(task_path, dataset_name, table, dataset_versions):
    return f"{task_path}/{get_gcs_dataset_prefix(dataset_name, dataset_versions)}/{table}.gzip"


def get_current_utc_datetime_str():
    return datetime.now(timezone.utc).strftime(settings.time.datetime_zoned_format)


def get_gcs_model_file_name(dataset_name, dataset_versions):
    return f"{get_gcs_dataset_prefix(dataset_name, dataset_versions)}.joblib"


def update_model_in_task(db: firestore.Client, tenant_id, machine_id, task_id, model_path, parameters):
    configuration = pull_current_configuration_from_firestore(db, tenant_id)
    documents = db.collection(machines_collection_name). \
        where(configuration_reference_field_path, "==", configuration.reference). \
        where("machine_id", "==", machine_id).get()
    if len(documents) != 1:
        print(f"Machine not found {machine_id}")
        return False
    document = documents[0]
    tasks = document.get("tasks")
    if task_id not in tasks:
        print(f"Task not found {task_id}")
        return False
    document_ref = document.reference
    path = f"tasks.{task_id}.task_data"
    document_ref.update({path: model_path})

    # Update parameters
    params_path = f"tasks.{task_id}.parameters"
    document_ref.update({params_path: parameters})

    return True


def get_pubsub_ml_event_log(message):
    return f"edge_logical_id: {message['edge_logical_id']}, " \
           f"perception_name: {message['perception_name']}, " \
           f"tenant_id: {message['tenant_id']}, " \
           f"table_id: {message['table_id']}," \
           f"observation_timestamp: {message['observation_timestamp']}"


def get_ml_event_log(event):
    return f"event: {event['event']}, " \
           f"task_id: {event['task_id']}" \
           f"asset_id: {event['asset_id']}, " \
           f"tenant_id: {event['tenant_id']}, " \
           f"event_id: {event['event_id']}," \
           f"observation_timestamp: {event['observation_timestamp']}"
