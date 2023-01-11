"""
This module exports the GCP Cloud function to update the Cloud IoT Core Gateway devices
based on the Firestore project configuration, specifically the most recent one.
"""

# =========================== Imports ===============================
import txp.common.utils.firestore_utils
from txp.cloud import settings
from txp.common.utils.json_complex_encoder import ComplexEncoder
from txp.common.configuration import GatewayConfig
from txp.common.configuration import JobConfig
from txp.cloud import (
    pull_docs_from_collection_associated_with_configuration
)
from txp.common.edge import EdgeDescriptor, MachineMetadata
import google.cloud.firestore as firestore
from typing import Dict, List
from google.cloud import iot_v1
import json
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

configuration_reference_field_path = "configuration_ref"


def _get_edges_descriptor(
        devices_docs: List[firestore.DocumentSnapshot], edges_docs: List[firestore.DocumentSnapshot]
) -> List[EdgeDescriptor]:
    """Utilitary function to build the EdgeDesctiptor's instance for the Gateway IoT Configuration"""
    device_dict: Dict[str, firestore.DocumentReference] = {}
    for device in devices_docs:
        device_dict[device.to_dict()["kind"]] = device.to_dict()

    edges_descriptors: List[EdgeDescriptor] = []
    for edge in edges_docs:
        try:
            device_kind = edge.to_dict()["device_kind"]
            device = device_dict[device_kind]
            if "type" in edge.to_dict():
                device_type = edge.get("type")
            elif "device_type" in edge.to_dict():
                device_type = edge.get("device_type")
            else:
                device_type = device["type"]

            edge_parameters: Dict = {**device["parameters"], **edge.to_dict()["parameters"]}
            edge_perceptions: Dict = device["perceptions"]
            edge_descriptor = EdgeDescriptor(
                edge.to_dict()["logical_id"], device_kind, device_type, edge_parameters, edge_perceptions
            )
            edges_descriptors.append(edge_descriptor)
            print(f"Successfully built the Edge {edge.id}: {edge_descriptor.logical_id} with type: {edge_descriptor.device_type}")
        except:
            edges_descriptors.append(None)

    return edges_descriptors


def _update_gateway_configuration(
        iot: iot_v1.DeviceManagerClient,
        configuration_id: int,
        job: JobConfig,
        gateway_config: GatewayConfig,
        machines: List[MachineMetadata],
        edges: List[EdgeDescriptor]
) -> None:
    """Updates the configuration of the Gateway in the IoT Core service."""
    device_path = iot.device_path(
        gateway_config.project_id,
        gateway_config.cloud_region,
        gateway_config.registry_id,
        gateway_config.gateway_id
    )

    data = json.dumps(
        {
            "configuration_id": configuration_id,
            "job": job,
            "gateway": gateway_config,
            "machines": machines,
            "edges": edges
        },
        cls=ComplexEncoder, indent=4
    ).encode()

    data

    iot.modify_cloud_to_device_config(
        request={
            "name": device_path,
            "binary_data": data,
            "version_to_update": 0
            # https://googleapis.dev/python/cloudiot/latest/iot_v1/types.html#google.cloud.iot_v1.types.ModifyCloudToDeviceConfigRequest.version_to_update
        }
    )


def _extract_edges_ids_from_machine(machine_doc: firestore.DocumentSnapshot):
    edges_ids: List[str] = []
    for edge_doc_ref in machine_doc.get("associated_with_edges"):
        edges_ids.append(edge_doc_ref.get().get('logical_id'))
    return edges_ids


# ======================== Main Function Body to export ============================================
def update_iot_gateways_conf(data, context):
    """The cloud function body defined in this module, to be deployed as a GCP cloud function.

    Documentation reference for the received arguments as result of a Firestore trigger:
        https://cloud.google.com/functions/docs/calling/cloud-firestore#event_structure
    """
    db = firestore.Client()

    log.info("Connection to Firestore established.")

    gateway_document_name = data["value"]["name"]  # This keys are guaranteed by Firestore trigger payload
    gateway_document: firestore.DocumentSnapshot = db.document(gateway_document_name).get()
    job_document: firestore.DocumentSnapshot = gateway_document.get("has_job").get()

    machines: List[firestore.DocumentSnapshot] = list(map(
        lambda machine_doc_ref: machine_doc_ref.get(),
        gateway_document.get('machines')
    ))

    edges: List[firestore.DocumentSnapshot] = []

    for machine in machines:
        edges = edges + (list(map(
            lambda edge_doc_ref: edge_doc_ref.get(),
            machine.get("associated_with_edges")
        )))

    edges = list(set(edges))

    configuration = gateway_document.get('configuration_ref')

    if not configuration:
        log.error(f"No Configuration reference document was found in "
                  f"the Gateway {gateway_document.get('gateway_id')}")
        return 1

    tenant_doc_ref = configuration.get().get('tenant_ref')
    tenant_id = tenant_doc_ref.get().get('tenant_id')

    log.info(f'Tenant ID found for Gateway update: {tenant_id}')

    devices_documents = pull_docs_from_collection_associated_with_configuration(
        db, devices_collection_name, configuration
    )

    # Build TXP objects instances.
    configuration_id = configuration.get().to_dict().get('configuration_id', None)
    if not configuration_id:
        log.error("Configuration obtained from firestore does not have the expected configuration_id field.")
        return 1

    configuration_id = configuration_id

    machines_ids: List[str] = list(map(
        lambda machine_doc: machine_doc.to_dict()['machine_id'], machines
    ))

    gateway_config: GatewayConfig = GatewayConfig.build_from_dict(
        {**gateway_document.to_dict(), **{"machines_ids": machines_ids}}
    )

    job_config: JobConfig = JobConfig.build_from_dict(job_document.to_dict())
    if not job_config:
        log.error("The JOB obtained from Firestore could not be parsed")
        return 1

    if gateway_config is None:
        log.error("Gateway configurations obtained from Firestore could not be parsed")
        return 1

    machines_metadata: List[MachineMetadata] = list(map(
        lambda machine_document: MachineMetadata.build_from_dict(
            {**machine_document.to_dict(), **{"edges_ids": _extract_edges_ids_from_machine(machine_document)}}
        ),
        machines
    ))

    for machine in machines_metadata:
        if machine is None:
            log.error("MachinesMetadata configurations obtained from Firestore could not be parsed")
            return 1

    edges_descriptors: List[EdgeDescriptor] = _get_edges_descriptor(devices_documents, edges)

    for edge_descriptor in edges_descriptors:
        if edge_descriptor is None:
            log.error("EdgeDescriptor configurations obtained from Firestore could not be parsed")
            return 1

    iot = iot_v1.DeviceManagerClient()

    _update_gateway_configuration(
        iot,
        configuration_id,
        job_config,
        gateway_config,
        machines_metadata,
        edges_descriptors
    )

    print(f"Successfully updated the Gateway: {gateway_config.gateway_id} in IoT")


# ======================== Main to debug locally ============================================
if __name__ == '__main__':
    # debug using the GAO standalone-arm gateway
    update_iot_gateways_conf(
        {
            'value': {
                'name': 'gateways/6QQ6anowueUC25seUfnS'
            }
        },
        {})
