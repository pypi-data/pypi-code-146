import os

import cloudpickle

from truera.client.intelligence.truera_model import \
    TruEraTransformPredFuncModel


def _load_model_from_local_file(path):
    parent_dir = os.path.dirname(path)
    with open(path, "rb") as f:
        loaded_model = cloudpickle.load(f)

    path_to_transformer = os.path.join(parent_dir, "transformer.pkl")
    with open(path_to_transformer, "rb") as t:
        loaded_transformer = cloudpickle.load(t)
    return TruEraTransformPredFuncModel(loaded_model, loaded_transformer)


def _load_pyfunc(path):
    return _load_model_from_local_file(path)
