import cloudpickle
import pandas as pd
from xgboost import Booster
from xgboost import DMatrix
from xgboost import XGBRegressor


class PredictWrapper(object):

    def __init__(self, model):
        self.model = model
        if isinstance(self.model, Booster):
            self.predict = lambda df: self.predict_booster(df)
        elif isinstance(self.model, XGBRegressor):
            self.predict = lambda df: self.predict_regressor(df)
        else:
            raise ValueError("Unknown XGBoost model type: " + type(self.model))

    def predict_regressor(self, df):
        return self.model.predict(df, validate_features=False)

    def predict_booster(self, df):
        return pd.Series(
            self.model.predict(DMatrix(df.values), validate_features=False),
            name="Result"
        )

    def get_model(self):
        return self.model


def _load_model_from_local_file(path):
    with open(path, "rb") as f:
        return PredictWrapper(cloudpickle.load(f))


def _load_pyfunc(path):
    return _load_model_from_local_file(path)
