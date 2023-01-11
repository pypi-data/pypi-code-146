import os
from typing import Any

import catboost  # pylint: disable=import-error
import cloudpickle
import pandas as pd
import scipy.sparse as sparse


class PredictProbaWrapper(object):

    def __init__(self, model: Any, transformer: Any):
        self.model = model
        self.transformer = transformer

    def predict(self, df):
        return pd.DataFrame(
            self.model.predict_proba(df), columns=self.model.classes_
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
    clf = catboost.CatBoostClassifier()
    clf.load_model(path, "cbm")

    path_to_transformer = os.path.join(parent_dir, "transformer.pkl")
    with open(path_to_transformer, "rb") as t:
        loaded_transformer = cloudpickle.load(t)
    return PredictProbaWrapper(clf, loaded_transformer)


def _load_pyfunc(path):
    return _load_model_from_local_file(path)
