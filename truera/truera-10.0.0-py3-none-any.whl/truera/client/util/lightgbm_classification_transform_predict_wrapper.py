from __future__ import annotations

from typing import Any, TYPE_CHECKING

import cloudpickle

if TYPE_CHECKING:
    from lightgbm import Booster

import os

import numpy as np
import pandas as pd
import scipy.sparse as sparse


def validate_lightgbm_booster_classifier(model: Booster) -> bool:
    if (not model.params) or ("objective" not in model.params
                             ) or (model.params["objective"] != "binary"):
        raise ValueError(
            "Booster objects do not output probability scores unless trained with `\"objective\": \"binary\"` so cannot be used for classification!"
        )


class PredictProbaWrapper(object):

    def __init__(self, model: Any, transformer: Any):
        from lightgbm import Booster
        from lightgbm import LGBMClassifier
        self.model = model
        self.transformer = transformer
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
    return PredictProbaWrapper(loaded_model, loaded_transformer)


def _load_pyfunc(path):
    return _load_model_from_local_file(path)
