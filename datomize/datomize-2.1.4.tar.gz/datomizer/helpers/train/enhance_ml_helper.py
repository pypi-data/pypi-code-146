import json
import requests
from datomizer import DatoMapper
from datomizer.utils.constants import MANAGEMENT_PUT_ENHANCE_ML_TRAIN_GEN_FLOW
from datomizer.utils.general import TRAIN_ITERATIONS, ENHANCE_ML_TARGET_TABLE, ENHANCE_ML_TARGET_COLUMN
from datomizer.utils.enhance_ml import Algorithms, Metrics, map_enum_list

DEFAULT_ALGORITHMS = [Algorithms.RANDOM_FOREST,
                      Algorithms.GBM,
                      Algorithms.KNN,
                      Algorithms.LR,
                      Algorithms.LGBM,
                      Algorithms.XGBOOST]
DEFAULT_METRICS = [Metrics.F1,
                   Metrics.PR_AUC]


def create_enhance_ml_request(target_table, target_column,
                              metric_list=[], algorithm_list=[]) -> dict:
    if not metric_list:
        metric_list = DEFAULT_METRICS
    if not algorithm_list:
        algorithm_list = DEFAULT_ALGORITHMS

    metric_list = map_enum_list(metric_list)
    algorithm_list = map_enum_list(algorithm_list)

    return {"tableName": target_table, "targetColumn": target_column,
            "metricList": metric_list, "algorithmList": algorithm_list}


def enhance_ml_generate(dato_mapper: DatoMapper, target_table, target_column, metric_list=[], algorithm_list=[]) -> int:
    dato_mapper.wait()
    response_json = dato_mapper.datomizer.get_response_json(requests.put,
                                                            url=MANAGEMENT_PUT_ENHANCE_ML_TRAIN_GEN_FLOW,
                                                            url_params=[dato_mapper.business_unit_id,
                                                                        dato_mapper.project_id,
                                                                        dato_mapper.flow_id],
                                                            headers={"Content-Type": "application/json"},
                                                            data=json.dumps(create_enhance_ml_request(target_table,
                                                                                                      target_column,
                                                                                                      metric_list,
                                                                                                      algorithm_list)))
    return response_json


def get_train_iteration_by_target(dato_mapper: DatoMapper, target_table, target_column) -> dict:
    flow = dato_mapper.get_flow()
    iteration = [t for t in flow[TRAIN_ITERATIONS]
                 if t[ENHANCE_ML_TARGET_TABLE] == target_table
                 and t[ENHANCE_ML_TARGET_COLUMN == target_column]][0]
    return iteration
