import json
import base64
import requests
from datomizer import Datomizer
from datomizer.utils.constants import (MANAGEMENT_POST_ADD_FLOW, MANAGEMENT_GET_SCHEMA_DISCOVERY,
                                       MANAGEMENT_GET_SCHEMA_DISCOVERY_PROTO)
from datomizer.utils.general import ID
from datomizer.protos.autodiscoveryservice_pb2 import SchemaDiscoveryDTO


def create_flow_creation_request(datasource_id: int, sample_percent: int = 1, title: str = "new_flow") -> dict:
    return {
        "modelTrainingConfiguration": {
            "title": title,
            "dataSourceId": datasource_id,
            "sampleInputData": sample_percent,
            "privacyLevels": [-1]
        }
    }


def discover(datomizer: Datomizer,
             business_unit_id: str, project_id: str, datasource_id: str,
             sample_percent: int = 1, title: str = "new_flow") -> int:
    flow_creation_request = create_flow_creation_request(datasource_id, sample_percent, title)
    response_json = datomizer.get_response_json(requests.post,
                                                url=MANAGEMENT_POST_ADD_FLOW,
                                                url_params=[business_unit_id, project_id],
                                                headers={"Content-Type": "application/json"},
                                                data=json.dumps(flow_creation_request))
    return response_json[ID]


def get_schema_discovery(datomizer: Datomizer,
                         business_unit_id: str, project_id: str, flow_id: str) -> SchemaDiscoveryDTO:
    response_proto = datomizer.api_request(requests.get, headers={"Content-Type": "application/x-protobuf"},
                                           url=MANAGEMENT_GET_SCHEMA_DISCOVERY_PROTO,
                                           url_params=[business_unit_id, project_id, flow_id])
    return SchemaDiscoveryDTO().FromString(response_proto.content)


def put_schema_discovery(datomizer: Datomizer,
                         business_unit_id: str, project_id: str, flow_id: str,
                         schema: SchemaDiscoveryDTO) -> SchemaDiscoveryDTO:
    response_proto = datomizer.api_request(requests.put, headers={"Content-Type": "application/x-protobuf"},
                                           url=MANAGEMENT_GET_SCHEMA_DISCOVERY_PROTO,
                                           url_params=[business_unit_id, project_id, flow_id],
                                           data=schema.SerializeToString())
    return SchemaDiscoveryDTO().FromString(response_proto.content)
