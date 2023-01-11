# ============================ Imports ====================================
import base64
from txp.cloud import pull_current_configuration_from_firestore
from txp.common.utils.json_complex_encoder import ComplexEncoder
import google.cloud.firestore as firestore
from google.cloud import iot_v1
import json
from typing import List, Dict
from txp.cloud import settings
from txp.common.edge.common import PairedEdgesPayload, EdgeDescriptor, MachineMetadata
import sys


# =========================== Constant Data & helper functions ===============================
def _get_edges_from_db(
        db: firestore.Client, configuration_ref, edges_logical_ids: List[str]
):
    """Returns the Edges Documents from the Database that matches the logical ids
    passed in the edges_logical_ids

    Returns:
        The list of found Edges documents in Firestore.
    """
    edges_collection_name = settings.firestore.edges_collection
    configuration_reference_field_path = "configuration_ref"
    edges = (
        db.collection(edges_collection_name)
            .where(configuration_reference_field_path, "==", configuration_ref)
            .where("logical_id", "in", edges_logical_ids)
            .get()
    )
    return list(edges)


def _pull_machine(
        db: firestore.Client, configuration_ref, machine_id: str
):
    """Returns the Machine document associates with the virtual edge actuator
    declared in the logical configuration. """
    machines_collection_name = settings.firestore.machines_collection
    configuration_reference_field_path = "configuration_ref"
    machine_doc = (
        db.collection(machines_collection_name)
        .where(configuration_reference_field_path, "==", configuration_ref)
        .where("machine_id", "==", machine_id)
    ).get()

    if not machine_doc:
        return None

    return machine_doc[0]


def _add_edges_to_machines(
        db: firestore.Client,
        configuration_ref: firestore.DocumentReference,
        machines: List[MachineMetadata],
        edges_refs: Dict[str, firestore.DocumentReference]
):
    for machine in machines:
        machine_doc: firestore.DocumentSnapshot = _pull_machine(db, configuration_ref, machine.machine_id)
        if not machine_doc:
            print(
                f"Unexpected error: Machine document not found for {machine.machine_id}.",
                file=sys.stderr,
            )
            continue

        new_edges_for_machine = []
        for edge in machine.edges_ids:
            if edge in edges_refs:  # If not, then the edge already existed.
                new_edges_for_machine.append(edges_refs[edge])

        old_edges = machine_doc.get("associated_with_edges")
        new_edges = old_edges + new_edges_for_machine
        machine_doc.reference.update({
            "associated_with_edges": new_edges
        })

        print(f"Updated Machine document {machine_doc.id} with logical id {machine.machine_id}\n"
              f"New set of edges: {list(map(lambda edge_ref: edge_ref.get().get('logical_id'), new_edges ))}")


def _create_new_virtual_edges(
        db: firestore.Client, configuration_ref, device_kind_doc_ref,
        edge_descriptors: List[EdgeDescriptor]
):
    """Creates the New virtual Edges in Firestore."""
    edges_references: Dict[str, firestore.DocumentReference] = {}
    for edge_descriptor in edge_descriptors:
        parameters_dict = json.loads(
            json.dumps(edge_descriptor.edge_parameters, cls=ComplexEncoder)
        )
        document_dict = {
            "device_kind": edge_descriptor.device_kind,
            "configuration_ref": configuration_ref,
            "is_of_kind_ref": device_kind_doc_ref,
            "logical_id": edge_descriptor.logical_id,
            "parameters": parameters_dict,
            "type": edge_descriptor.device_type
        }
        edge_ref = db.collection(settings.firestore.edges_collection).add(
            document_dict
        )[1]
        edges_references[edge_descriptor.logical_id] = edge_ref
        print(f"Document created for virtual edge: {edge_descriptor.logical_id}")

    return edges_references


def _create_iot_device(
    project_id, cloud_region, registry_id, device_id
):
    """Create a device to bind to a gateway if it does not exist."""
    client = iot_v1.DeviceManagerClient()
    exists = False
    parent = client.registry_path(project_id, cloud_region, registry_id)
    devices = list(client.list_devices(request={"parent": parent}))

    for device in devices:
        if device.id == device_id:
            exists = True

    # Create the device
    device_template = {
        "id": device_id,
        "gateway_config": {
            "gateway_type": iot_v1.GatewayType.NON_GATEWAY,
            "gateway_auth_method": iot_v1.GatewayAuthMethod.ASSOCIATION_ONLY,
        },
    }

    if not exists:
        res = client.create_device(
            request={"parent": parent, "device": device_template}
        )
        print("Created Device {}".format(res))
    else:
        print("Device exists, skipping")


def _bind_device_to_gateway(
    project_id, cloud_region, registry_id, device_id, gateway_id
):
    """Binds a device to a gateway."""
    client = iot_v1.DeviceManagerClient()

    _create_iot_device(
        project_id, cloud_region, registry_id, device_id
    )

    parent = client.registry_path(project_id, cloud_region, registry_id)

    res = client.bind_device_to_gateway(
        request={"parent": parent, "gateway_id": gateway_id, "device_id": device_id}
    )

    print(f"Device Bound in IoT {res}")


def _get_iot_gateway_configuration(
        gateway_id: str,
        registry_id: str,
        project_id: str,
        cloud_region: str,
) -> Dict:
    """Returns the Gateway configuration in a dict"""
    iot_client = iot_v1.DeviceManagerClient()
    device_path = iot_client.device_path(project_id, cloud_region, registry_id, gateway_id)

    gateway_device: iot_v1.Device = iot_client.get_device(request={"name": device_path})
    current_config: iot_v1.DeviceConfig = gateway_device.config
    config_json: dict = json.loads(
        current_config.binary_data.decode()
    )
    return config_json


def _update_gateway_configuration(
    gateway_id: str,
    registry_id: str,
    project_id: str,
    cloud_region: str,
    configuration: Dict
) -> None:
    iot_client = iot_v1.DeviceManagerClient()
    device_path = iot_client.device_path(
        project_id,
        cloud_region,
        registry_id,
        gateway_id
    )
    data = json.dumps(
        configuration,
        indent=4
    ).encode()

    iot_client.modify_cloud_to_device_config(
        request={
            "name": device_path,
            "binary_data": data,
            "version_to_update": 0
            # https://googleapis.dev/python/cloudiot/latest/iot_v1/types.html#google.cloud.iot_v1.types.ModifyCloudToDeviceConfigRequest.version_to_update
        }
    )

    print(f"Successfully updated Cloud IoT config for Gateway: {gateway_id}")


def update_paired_devices(event, context):
    """This function is the function body deployed to run in the cloud functions
    runtime.

    A detailed page with all the context can be found here:
        https://cloud.google.com/functions/docs/calling/pubsub
    """
    if "data" in event:
        # ================== Parses event received data====================================
        state_data = base64.b64decode(event["data"]).decode()
        attributes = event.get("attributes", None)
        if not attributes:
            print("Unexpected error: No attributes received in event.", file=sys.stderr)
            exit(1)

        json_data = json.loads(state_data, strict=False)
        print(f"Received JSON data: {json_data}")

        payload: PairedEdgesPayload = PairedEdgesPayload.build_from_dict(json_data)
        if not payload:
            print(
                "Unexpected error: could not parse PairedEdgesPayload in event.",
                file=sys.stderr,
            )
            exit(1)

        # ================== Pulls configuration documents from DB====================================
        # In this point, we'll pull from Firestore the existing EdgeDescriptors.
        # Non-virtual Edges will be there, those need to be updated.
        # Virtual Edges will not be found, those need to be created.
        db = firestore.Client()

        current_configuration = pull_current_configuration_from_firestore(db, payload.tenant_id)
        if not current_configuration:
            print(
                "Unexpected error: No current configuration found in database",
                file=sys.stderr,
            )
            exit(1)

        edges_ids = list(
            map(lambda edge_descriptor: edge_descriptor.logical_id, payload.devices)
        )

        edges_documents: List[firestore.DocumentSnapshot] = _get_edges_from_db(
            db, current_configuration.reference, edges_ids
        )

        if not edges_documents:
            print(
                "Unexpected error: No edges found in configuration for the received edges logical_ids."
            )
            exit(1)

        # ================== Builds associative tables====================================
        edges_documents_table: Dict = dict(
            map(
                lambda edge_doc: (edge_doc.to_dict()["logical_id"], edge_doc),
                edges_documents,
            )
        )

        # ================== Update Firestore documents ==================================
        not_found_edges: List[EdgeDescriptor] = []
        actuator_edge_descriptor_doc: firestore.DocumentSnapshot = None
        for edge_descriptor in payload.devices:
            if edge_descriptor.logical_id in edges_documents_table:
                document = edges_documents_table[edge_descriptor.logical_id]
                parameters_dump = json.dumps(edge_descriptor.edge_parameters, cls=ComplexEncoder)
                document.reference.update({"parameters": json.loads(parameters_dump)})
                print(
                    f"Updated Edge in database: {edge_descriptor.logical_id}. Document ID: {document.id}"
                )
                if edge_descriptor.is_actuator_device():
                    actuator_edge_descriptor_doc = document
            else:
                not_found_edges.append(edge_descriptor)

        print("All existing Edges were updated")

        if not_found_edges:
            print(f"Not found virtual edges will be created")

            if not actuator_edge_descriptor_doc:
                print("Virtual Edges received, but the parent EdgeDescriptor for the actuator"
                      "was not found.", file=sys.stderr)
                db.close()
                exit(1)

            else:
                # TODO: Handle Errors with Firestore.
                created_edges = _create_new_virtual_edges(db, current_configuration.reference,
                                          actuator_edge_descriptor_doc.get("is_of_kind_ref"),
                                          not_found_edges)

                _add_edges_to_machines(db, current_configuration.reference, payload.machines, created_edges)

        db.close()

        # ================= Gateway IoT Device Configuration =============================
        gateway_id: str = attributes['deviceNumId']
        registry_id: str = attributes['deviceRegistryId']
        cloud_region: str = attributes['deviceRegistryLocation']
        project_id: str = attributes['projectId']

        gateway_conf_dict: Dict = _get_iot_gateway_configuration(gateway_id,
                                                                 registry_id,
                                                                 project_id,
                                                                 cloud_region)

        edges_descriptors_json = list(map(lambda edge_desc: json.dumps(
            edge_desc, cls=ComplexEncoder, indent=4
        ), payload.devices))

        edges_descriptors_json = list(map(lambda edge_des_dumped: json.loads(
            edge_des_dumped
        ), edges_descriptors_json))

        gateway_conf_dict.update({
            'edges': edges_descriptors_json
        })

        machines_metadata_jsons = list(map(
            lambda machine_metadata: json.dumps(
                machine_metadata, cls=ComplexEncoder, indent=4
            ), payload.machines
        ))

        machines_metadata_jsons = list(map(
            lambda machine_dumped: json.loads(machine_dumped),
            machines_metadata_jsons
        ))

        gateway_conf_dict["machines"] = machines_metadata_jsons

        # Bind and create new devices
        for edge_descriptor in not_found_edges:
            _bind_device_to_gateway(project_id, cloud_region, registry_id,
                                    edge_descriptor.logical_id, gateway_id)

        _update_gateway_configuration(
            gateway_id, registry_id,
            project_id, cloud_region, gateway_conf_dict
        )

        db.close()
    else:
        print("Unexpected error: No data received in event.", file=sys.stderr)
