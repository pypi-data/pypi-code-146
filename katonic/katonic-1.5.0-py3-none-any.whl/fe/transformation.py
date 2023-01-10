#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#
import logging
from typing import List
from typing import Tuple

import pandas as pd
import sklearn
from sklearn.preprocessing import StandardScaler

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


class Transformation:
    def __init__(self, input_data: pd.DataFrame):
        self.input_data = input_data

    def standard_scalar(
        self, column_list: List[str], with_mean: bool = True, with_std: bool = True
    ) -> Tuple[pd.DataFrame, sklearn.preprocessing._data.StandardScaler]:
        """
        Transforming features from standard scaling on training data
        Parameters:
            column_list: List of columns to be filled.
            with_mean: If True, center the data before scaling. This does not work (and will raise an exception)
                        when attempted on sparse matrices, because centering them entails building a dense matrix
                        which in common use cases is likely to be too large to fit in memory.
            with_std: If True, scale the data to unit variance (or equivalently, unit standard deviation).
        Return:
            [pd.DataFrame]: Return pandas dataframe with new transformed features created by standard scaling
            [sklearn.preprocessing._data.StandardScaler]: Standard Scalar model
        """
        try:
            if not isinstance(column_list, list):
                raise TypeError("column_list should be of list type")
            if not column_list:
                raise ValueError("column_list cannot be empty")

            logger.info("Started Standard-Scaling on training dataset")
            logger.info(f"Columns to do standard scaling: {column_list}")

            scaling_model = StandardScaler(with_mean=with_mean, with_std=with_std)
            scaling_model.fit(self.input_data[column_list])

            output_df = pd.DataFrame(
                scaling_model.transform(self.input_data[column_list]),
                columns=column_list,
            )

            logger.info("Ended Standard scaling")

            return output_df, scaling_model
        except Exception as e:
            raise e

    def standard_scalar_on_test(
        self,
        column_list: List[str],
        scalar_model: sklearn.preprocessing._data.StandardScaler,
    ) -> pd.DataFrame:
        """
        Transforming features from standard scalar on test data
        Parameters:
            column_list: List of columns to be filled.
            scalar_model: Standard Scalar model with which training data is scaled on
        Return:
            [pd.DataFrame]: Return pandas dataframe with new features created by standard scalar
        """
        if not isinstance(column_list, list):
            raise TypeError("column_list should be of list type")
        if not column_list:
            raise ValueError("column_list cannot be empty")

        if not isinstance(scalar_model, sklearn.preprocessing._data.StandardScaler):
            raise TypeError(
                "scalar_model should be of sklearn.preprocessing._data.StandardScaler type"
            )
        if not scalar_model:
            raise ValueError("one_hot_model cannot be empty")

        logger.info("Started standard feature scaling on test data")
        logger.info(f"Columns to transform using standard scalar: {column_list}")

        output_df = pd.DataFrame(
            scalar_model.transform(self.input_data[column_list]), columns=column_list
        )

        logger.info("Ended feature transformation using standard scalar")

        return output_df
