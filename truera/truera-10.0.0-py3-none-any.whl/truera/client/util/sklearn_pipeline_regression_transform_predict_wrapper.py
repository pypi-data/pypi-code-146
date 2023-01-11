import os
from typing import Any

import cloudpickle
import pandas as pd
import scipy.sparse as sparse


class PredictWrapper(object):

    def __init__(self, model: Any, transformer: Any):
        self.model = model
        self.transformer = transformer

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.model.predict(df).ravel()

    def transform(self, pre_transform_df: pd.DataFrame) -> pd.DataFrame:
        transformed_data = self.transformer.transform(pre_transform_df)
        if isinstance(transformed_data, pd.DataFrame):
            return transformed_data
        try:
            post_transform_features = self.transformer.get_feature_names_out()
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


def _load_model_from_local_file(path: str):
    parent_dir = os.path.dirname(path)
    with open(path, "rb") as f:
        loaded_model = cloudpickle.load(f)
    with open(os.path.join(parent_dir, "transformer.pkl"), "rb") as t:
        loaded_transformer = cloudpickle.load(t)
    return PredictWrapper(loaded_model, loaded_transformer)


def _load_pyfunc(path: str):
    return _load_model_from_local_file(path)
