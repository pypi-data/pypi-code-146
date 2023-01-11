from __future__ import annotations

from typing import Union

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression

_VALID_MODEL_OUTPUT_TYPES = ["binary_classification", "regression"]


class QiiScaler:

    def __init__(
        self,
        random_state: int = None,
        model_output_type: str = "binary_classification"
    ) -> None:
        """Scaler using QIIs.

        Args:
            random_state (int, optional): Random seed. Defaults to None.
            model_output_type (str, optional): [description]. One of ["binary_classification", "regression"]. Defaults to "binary_classification".
        """
        assert model_output_type in _VALID_MODEL_OUTPUT_TYPES
        self._random_state = random_state
        self._model_output_type = model_output_type

    def fit(
        self, xs: Union[pd.DataFrame, np.ndarray], ys: Union[pd.DataFrame,
                                                             np.ndarray]
    ) -> QiiScaler:
        """Fits this scaler.

        Args:
            xs (Union[pd.DataFrame, np.ndarray]): x-values to scale with.
            ys (Union[pd.DataFrame, np.ndarray]): y-values to scale with. Note that these are necessary.

        Returns:
            QiiScaler: The QiiScaler instance (used for chaining).
        """
        if self._model_output_type == "binary_classification":
            # TODO(davidkurokawa): For some reason, pylint complains about random_state and max_iter.
            # pylint: disable=unexpected-keyword-arg
            model = LogisticRegression(
                random_state=self._random_state, max_iter=1000
            )
        elif self._model_output_type == "regression":
            # TODO(davidkurokawa): For some reason, pylint complains about random_state and max_iter.
            # pylint: disable=unexpected-keyword-arg
            model = LinearRegression(
                random_state=self._random_state, max_iter=1000
            )
        else:
            assert self._model_output_type in _VALID_MODEL_OUTPUT_TYPES
        model.fit(xs, ys)
        self._coeffs = model.coef_
        self._mean_xs = np.mean(xs, axis=0)
        return self

    def transform(
        self, xs: Union[pd.DataFrame, np.ndarray]
    ) -> Union[pd.DataFrame, np.ndarray]:
        """Applies scaler to data. Must have called `fit` first.

        Args:
            xs (Union[pd.DataFrame, np.ndarray]): Data to transform.

        Returns:
            Union[pd.DataFrame, np.ndarray]: Transformed data.
        """
        return self._coeffs * (xs - self._mean_xs)
