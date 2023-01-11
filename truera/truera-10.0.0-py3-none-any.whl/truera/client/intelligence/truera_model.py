import pandas as pd
import scipy.sparse as sparse


class TruEraPredFuncModel(object):

    def __init__(self, pred_func) -> None:
        self.predict = pred_func


class TruEraTransformPredFuncModel(object):

    def __init__(self, pred_func, transformer) -> None:
        self.predict = pred_func
        self.transformer = transformer

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
