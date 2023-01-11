import os
from typing import Any

import cloudpickle
import pandas as pd
import scipy.sparse as sparse
from xgboost import Booster
from xgboost import DMatrix
from xgboost import XGBRegressor


class PredictWrapper(object):

    def __init__(self, model: Any, transformer: Any):
        self.model = model
        self.transformer = transformer
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

    def transform(self, pre_transform_df: pd.DataFrame) -> pd.DataFrame:
        if callable(self.transformer):
            transformed_data = self.transformer(pre_transform_df)
            if isinstance(transformed_data, pd.DataFrame):
                return transformed_data
            else:
                raise AssertionError(
                    "Expected transform function to output a DataFrame!"
                )
        else:
            # This part will handle sklearn transform objects.
            # Refer to `https://scikit-learn.org/stable/modules/preprocessing.html` to check which transforms are supported.
            transformed_data = self.transformer.transform(pre_transform_df)
            if isinstance(transformed_data, pd.DataFrame):
                return transformed_data
            try:
                post_transform_features = self.transformer.get_feature_names_out(
                )
            except:
                raise AssertionError(
                    "Expected transform object to output a DataFrame or implement the `get_feature_names_out()` function to retrieve post features!"
                )
            if isinstance(transformed_data, sparse.csr_matrix):
                return pd.DataFrame.sparse.from_spmatrix(
                    transformed_data, columns=post_transform_features
                )
            else:
                return pd.DataFrame(
                    transformed_data, columns=post_transform_features
                )

    def get_model(self):
        return self.model


def _load_model_from_local_file(path):
    parent_dir = os.path.dirname(path)
    with open(path, "rb") as f:
        loaded_model = cloudpickle.load(f)

    path_to_transformer = os.path.join(parent_dir, "transformer.pkl")
    with open(path_to_transformer, "rb") as t:
        loaded_transformer = cloudpickle.load(t)
    return PredictWrapper(loaded_model, loaded_transformer)


def _load_pyfunc(path):
    return _load_model_from_local_file(path)
