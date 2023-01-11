import json
import requests
from datomizer import DatoMapper
from datomizer.helpers.wrapper.evaluation_wrapper import EvaluationWrapper
from datomizer.utils.constants import MANAGEMENT_PUT_TRAIN_FLOW, MANAGEMENT_GET_MODEL_EVALUATION
from datomizer.utils.general import ID, TRAIN_ITERATIONS


def create_train_request(epochs_gan=500, epochs_vae=300) -> dict:
    return {"sampleInputRatio": 1, "sampleOutputRatio": 1,
            "epochsGenerativeModel": epochs_gan, "epochsFeatureReduction": epochs_vae}


def train(dato_mapper: DatoMapper, epochs_gan=500, epochs_vae=300) -> int:
    dato_mapper.wait()
    response_json = dato_mapper.datomizer.get_response_json(requests.put,
                                                            url=MANAGEMENT_PUT_TRAIN_FLOW,
                                                            url_params=[dato_mapper.business_unit_id,
                                                                        dato_mapper.project_id,
                                                                        dato_mapper.flow_id],
                                                            headers={"Content-Type": "application/json"},
                                                            data=json.dumps(create_train_request(epochs_gan,
                                                                                                 epochs_vae)))
    return response_json


def get_evaluation(dato_mapper: DatoMapper, model_id: int = 0) -> str:
    response_json = dato_mapper.datomizer.get_response_json(requests.get,
                                                            url=MANAGEMENT_GET_MODEL_EVALUATION,
                                                            url_params=[dato_mapper.business_unit_id,
                                                                        dato_mapper.project_id,
                                                                        dato_mapper.flow_id,
                                                                        model_id])
    return EvaluationWrapper(response_json)


def get_train_iteration(dato_mapper: DatoMapper, train_id) -> dict:
    flow = dato_mapper.get_flow()
    iteration = [t for t in flow[TRAIN_ITERATIONS] if t[ID] == train_id][0]
    return iteration
