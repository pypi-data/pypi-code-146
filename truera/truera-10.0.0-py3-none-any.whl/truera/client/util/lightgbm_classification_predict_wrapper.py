from __future__ import annotations

from typing import TYPE_CHECKING

import cloudpickle

if TYPE_CHECKING:
    from lightgbm import Booster

import numpy as np
import pandas as pd


def validate_lightgbm_booster_classifier(model: Booster) -> bool:
    if (not model.params) or ("objective" not in model.params
                             ) or (model.params["objective"] != "binary"):
        raise ValueError(
            "Booster objects do not output probability scores unless trained with `\"objective\": \"binary\"` so cannot be used for classification!"
        )


class PredictProbaWrapper(object):

    def __init__(self, model):
        from lightgbm import Booster
        from lightgbm import LGBMClassifier
        self.model = model
        if isinstance(self.model, Booster):
            validate_lightgbm_booster_classifier(self.model)
            self.predict = lambda df: self.predict_booster(df)
        elif isinstance(self.model, LGBMClassifier):
            self.predict = lambda df: self.predict_classifier(df)
        else:
            raise ValueError("Unknown lightgbm model type: " + type(self.model))

    def predict_booster(self, df: pd.DataFrame):
        preds = self.model.predict(df)
        return pd.DataFrame(
            data=np.column_stack([1 - preds, preds]), columns=[0, 1]
        )

    def predict_classifier(self, df: pd.DataFrame):
        return pd.DataFrame(
            self.model.predict_proba(df, validate_features=False),
            columns=self.model.classes_
        )

    def get_model(self):
        return self.model


def _load_model_from_local_file(path):
    with open(path, "rb") as f:
        return PredictProbaWrapper(cloudpickle.load(f))


def _load_pyfunc(path):
    return _load_model_from_local_file(path)
