import cloudpickle
import numpy as np
import pandas as pd
from xgboost import Booster
from xgboost import DMatrix
from xgboost import XGBClassifier


class PredictProbaWrapper(object):

    def __init__(self, model):
        self.model = model
        if isinstance(self.model, Booster):
            self.predict = lambda df: self.predict_booster(df)
        elif isinstance(self.model, XGBClassifier):
            self.predict = lambda df: self.predict_classifier(df)
        else:
            raise ValueError("Unknown XGBoost model type: " + type(self.model))

    def predict_classifier(self, df):
        return pd.DataFrame(
            self.model.predict_proba(df, validate_features=False),
            columns=self.model.classes_
        )

    def predict_booster(self, df):
        preds = self.model.predict(DMatrix(df.values), validate_features=False)
        return pd.DataFrame(
            data=np.column_stack([1 - preds, preds]), columns=[0, 1]
        )

    def get_model(self):
        return self.model


def _load_model_from_local_file(path):
    with open(path, "rb") as f:
        return PredictProbaWrapper(cloudpickle.load(f))


def _load_pyfunc(path):
    return _load_model_from_local_file(path)
