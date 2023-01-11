"""
This module exports a function that can be deployed as a GCP Cloud function
capable of updating the TXP Firestore configuration based on the manual
configuration editable collection.

The Manual Configuration Editable collection is a special collection in our
Firestore database, that can be used to edit configurations using the Firestore
web console.

This is provided as a way to edit configuration while we develop a web client
to communicate with Firestore.

TODO: This script should disappear eventually. We should have a database initialization
    script stored somewhere.
"""

# =========================== Imports ===============================
import google.cloud.firestore as firestore
import txp.common.utils.firestore_utils
from txp.cloud import (
    pull_current_configuration_from_firestore
)
from txp.cloud import settings
import txp.common.configuration.config_version as txp_config_version
from typing import List, Dict, Union
import pytz
import datetime
import logging

log = logging.getLogger(__name__)

# =========================== Constant Data ===============================
manual_configuration_collection = (
    settings.firestore.manual_configuration_edit_collection
)
config_form_document = txp.common.utils.firestore_utils.config_form_document
machines_group_collection_name = settings.firestore.machines_group_collection
machines_collection_name = settings.firestore.machines_collection
gateways_collection_name = settings.firestore.gateways_collection
devices_collection_name = settings.firestore.devices_collection
edges_collection_name = settings.firestore.edges_collection
jobs_collections_name = settings.firestore.jobs_collection
configurations_collection_name = settings.firestore.configurations_collection
tenants_collection = txp.common.utils.firestore_utils.tenants_collection


# =========================== Helper Functions ===============================
def pull_docs_from_manual_form_collection(
        db: firestore.Client, configuration_document: str, subcollection: str, as_dict: bool = True
) -> Union[List[Dict], List[firestore.DocumentSnapshot]]:
    """Returns the Dict instances from the documents found in the
    collection for the manual configuration form collection"""
    documents_coll = (
        db.collection(manual_configuration_collection)
            .document(configuration_document)
            .collection(subcollection)
            .get()
    )

    documents_coll = list(filter(
        lambda doc: "template" not in doc.id, documents_coll
    ))

    if as_dict:
        documents_coll = list(map(
            lambda doc: doc.to_dict(), documents_coll
        ))

    return documents_coll


def _create_new_configuration(
        db: firestore.Client,
        tenant_reference: firestore.DocumentReference
) -> firestore.DocumentReference:
    """Creates a new entity (document) in the configurations root level collection.

    The configuration time is aware time for UTC zone.
    The configuration entity has a timestamp based on the Firestore server,
        in order to support queries by timestamp.

    Returns:
        The DocumentReference to the new configuration entity.
    """
    previous_configuration = pull_current_configuration_from_firestore(db, tenant_reference.get().get('tenant_id'))

    if (previous_configuration and
            previous_configuration.exists and
            'configuration_id' in previous_configuration.to_dict()):
        new_configuration_id = txp_config_version.get_next_normal_version(
            previous_configuration.to_dict()['configuration_id']
        )
    else:
        new_configuration_id = 1

    config_timestamp = datetime.datetime.now(pytz.timezone(settings.gateway.timezone)).replace(microsecond=0)
    ref = db.collection(configurations_collection_name).add(
        {
            "configuration_id": str(new_configuration_id),  # string to allow possible id generation in the future
            # TODO: Remove `since` key if nobody is using it. This is local time eventually turned into UTC by Firestore
            "since": config_timestamp,
            "server_timestamp": firestore.SERVER_TIMESTAMP,  # This will be UTC
            "tenant_ref": tenant_reference
        }
    )
    return ref[1]


def _create_jobs(
        db: firestore.Client, jobs: List[Dict], configuration_ref: firestore.DocumentReference
) -> Dict:
    """Creates the jobs in firestore from the manual form collection,
    and return the dict of Job Form ID to Document References"""
    return_dict = {}
    for job in jobs:
        job_dict = job.to_dict()
        job_dict["configuration_ref"] = configuration_ref
        result = db.collection(jobs_collections_name).add(job_dict)
        return_dict[job.id] = result[1]

    return return_dict


def _create_machines(
        db: firestore.Client,
        machines: List[Dict],
        edges_refs: Dict[str, firestore.DocumentReference],
        configuration_ref: firestore.DocumentReference
) -> Dict[str, firestore.DocumentReference]:
    """Creates the Machines entities in the DB based on the received dictionaries.

    It will create the references to the appropriates edges and gateway for each machine.

    Returns:
        Dict of machines IDs to the firestore DocumentReference's for those machines.
    """
    return_dict = {}
    for machine_dict in machines:
        # replace associated_with_edges with edges references
        edges_refs_for_machine = list(
            map(
                lambda edge_logical_id: edges_refs[edge_logical_id],
                machine_dict["associated_with_edges"],
            )
        )
        machine_dict["associated_with_edges"] = edges_refs_for_machine
        machine_dict["configuration_ref"] = configuration_ref

        # creates machine
        log.info(f"Creating Machine in Firestore: {machine_dict['machine_id']}")
        result = db.collection(machines_collection_name).add(machine_dict)
        return_dict[machine_dict["machine_id"]] = result[1]

    return return_dict


def _create_gateways(
        db: firestore.Client,
        gateways: List[Dict],
        created_machines: Dict[str, firestore.DocumentReference],
        created_jobs: Dict[str, firestore.DocumentReference],
        configuration_ref: firestore.DocumentReference,
) -> Dict[str, firestore.DocumentReference]:
    """Creates the new entities for the Gateways based on the received
    dictionaries.

    Returns:
        Returns a Dict of gateway IDs to the firestore DocumentReference for that
        gateway ID.
    """
    return_dict = {}
    for gateway_dict in gateways:
        log.info(f"Creating Gateway in Firestore: {gateway_dict['gateway_id']}")
        gateway_dict["configuration_ref"] = configuration_ref
        gateway_dict["has_job"] = created_jobs[gateway_dict["has_job"]]
        gateway_dict["machines"] = list(
            map(lambda machine: created_machines[machine], gateway_dict["machines"]))  # list(created_machines.values())
        result = db.collection(gateways_collection_name).add(gateway_dict)
        return_dict[gateway_dict["gateway_id"]] = result[1]

    return return_dict


# ======================== Main Function Body to export ============================================
def update_manual_configuration(request):
    """The cloud function body defined in this module, to be deployed
    as a GCP cloud function.

    This method will generate a manual configuration snapshot given the
    tenant-id and the manual configuration collection stored in firestore.

    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>

    Returns:
        200 OK status code if everything was successful.

    """
    print(request)
    request_json = request.get_json(silent=True)
    print(request_json)
    if request_json and 'tenant_id' in request_json:
        tenant_id = request_json['tenant_id']
        configuration_document = request_json['configuration_document']
        log.info(f"Tenant ID received: {tenant_id}")
        log.info(f"Configuration Document in {manual_configuration_collection}"
                 f" collection: {configuration_document}")
    else:
        raise ValueError("JSON is invalid, or missing a 'name' property")

    db = firestore.Client()
    log.info(f"Trying to find Tenant document for {tenant_id}...")

    # Pull the tenant Document
    tenant = db.collection(tenants_collection).where(
        'tenant_id', '==', tenant_id
    ).get()

    if not tenant:
        log.error(f"Tenant document was not found for {tenant_id}")
        return 404

    if len(tenant) > 1:
        log.warning(f"Multiple Tenants in the database with id: {tenant_id}.")

    tenant_ref = tenant[0].reference

    log.info(
        "Connection to Firestore established. Proceed to pulling entities from manual"
        f"configuration form {configuration_document}"
    )

    machines_groups: List[Dict] = pull_docs_from_manual_form_collection(
        db, configuration_document, machines_group_collection_name
    )

    if not machines_groups:
        log.error("No machines_groups documents found. Execution finished")
        return "Error: No machines_groups found\n", 500

    machines_groups

    machines: List[Dict] = pull_docs_from_manual_form_collection(
        db, configuration_document, machines_collection_name)

    if not machines:
        log.error("No machines documents found. Execution finished")
        return "Error: No machines found in database form\n", 500

    gateways: List[Dict] = pull_docs_from_manual_form_collection(
        db, configuration_document,gateways_collection_name)

    if not gateways:
        log.error("No gateways documents found. Execution finished")
        return "Error: No gateways found in database form\n", 500

    devices: List[Dict] = pull_docs_from_manual_form_collection(
        db, configuration_document, devices_collection_name)

    if not devices:
        log.error("No devices documents found. Execution finished")
        return "Error: No devices found in database form\n", 500

    edges: List[Dict] = pull_docs_from_manual_form_collection(
        db, configuration_document, edges_collection_name)

    if not edges:
        log.error("No edges documents found. Execution finished")
        return "Error: No edges found in database form\n", 500

    jobs = pull_docs_from_manual_form_collection(
        db, configuration_document, jobs_collections_name, as_dict=False)

    if not jobs:
        log.error("No jobs document found. Execution finished")
        return "Error: No job entity found in database form\n", 500

    log.info(
        "All the required entities were obtained from the manual configuration form document"
    )

    created_configuration_ref = _create_new_configuration(db, tenant_ref)

    created_devices = txp.common.utils.firestore_utils._create_devices(db, devices, created_configuration_ref)

    created_edges = txp.common.utils.firestore_utils._create_edges(db, edges, created_devices, created_configuration_ref)

    created_jobs = _create_jobs(db, jobs, created_configuration_ref)

    created_machines = _create_machines(db, machines, created_edges, created_configuration_ref)

    created_machines_groups = txp.common.utils.firestore_utils._create_machines_groups(
        db, machines_groups, created_machines, created_configuration_ref
    )

    created_gateways = _create_gateways(db, gateways, created_machines, created_jobs, created_configuration_ref)

    log.info("All the new entities were created for the new configuration snapshot")

    return "OK\n", 200


# ======================== Main program to debug locally ============================================
if __name__ == "__main__":
    from unittest.mock import Mock

    tenant_id = 'labshowroom-001'
    configuration_document = 'laboratorio_showroom_manual_script'
    data = {'tenant_id': tenant_id, 'configuration_document': configuration_document}
    req = Mock(get_json=Mock(return_value=data), args=data)
    update_manual_configuration(req)
