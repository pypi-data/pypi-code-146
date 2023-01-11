import json
import requests

from datomizer import DatoMapper
from datomizer.utils.constants import MANAGEMENT_PUT_DATA_TUNER_TRAIN_GEN_FLOW, MANAGEMENT_PUT_DATA_TUNER_RULES_PATH
from datomizer.protos.datatunerservice_pb2 import DataTunerDTO


def create_data_tuner_request(rules_path: str) -> dict:
    return {"rulesPath": rules_path}


def tune(dato_mapper: DatoMapper, rules_path: str) -> int:
    dato_mapper.wait()
    response_json = dato_mapper.datomizer.get_response_json(requests.put,
                                                            url=MANAGEMENT_PUT_DATA_TUNER_TRAIN_GEN_FLOW,
                                                            url_params=[dato_mapper.business_unit_id,
                                                                        dato_mapper.project_id,
                                                                        dato_mapper.flow_id],
                                                            headers={"Content-Type": "application/json"},
                                                            data=json.dumps(create_data_tuner_request(rules_path)))
    return response_json


def put_rules(dato_mapper: DatoMapper, rules: DataTunerDTO):
    response = dato_mapper.datomizer.api_request(requests.put,
                                                 headers={"Content-Type": "application/x-protobuf"},
                                                 url=MANAGEMENT_PUT_DATA_TUNER_RULES_PATH,
                                                 url_params=[dato_mapper.business_unit_id,
                                                             dato_mapper.project_id,
                                                             dato_mapper.flow_id],
                                                 data=rules.SerializeToString())
    return response.text


def put_rules_and_tune(dato_mapper: DatoMapper, rules: DataTunerDTO):
    rules_path = put_rules(dato_mapper, rules)
    return tune(dato_mapper, rules_path)
