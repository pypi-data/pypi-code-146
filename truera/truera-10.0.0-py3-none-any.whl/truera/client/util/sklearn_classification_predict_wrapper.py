from typing import Any

import cloudpickle
import pandas as pd


class PredictProbaWrapper(object):

    def __init__(self, model: Any):
        self.model = model

    def predict(self, df):
        return pd.DataFrame(
            self.model.predict_proba(df), columns=self.model.classes_
        )

    def get_model(self):
        return self.model


def _load_model_from_local_file(path):
    with open(path, "rb") as f:
        return PredictProbaWrapper(cloudpickle.load(f))


def _load_pyfunc(path):
    return _load_model_from_local_file(path)
