#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#
import logging
from typing import List
from typing import Tuple

import pandas as pd
from sklearn.preprocessing import OneHotEncoder

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


class CreateFeatures:
    def __init__(self, input_data: pd.DataFrame):
        self.input_data = input_data

    def one_hot_encode(
        self,
        column_list: List[str],
        max_categories=None,
        min_frequency=None,
    ) -> Tuple[pd.DataFrame, OneHotEncoder]:
        """
        Create new features from one hot encode on training data
        Parameters:
            column_list: List of columns to perform one-hot encoding.
            max_categories: Specifies an upper limit to the number of output features for each input feature when considering infrequent categories.
            min_frequency: Specifies the minimum frequency below which a category will be considered infrequent.
        Return:
            [pd.DataFrame]: Return pandas dataframe with new features created by one-hot encode
            [sklearn.preprocessing._encoders.OneHotEncoder]: One-hot encode model
        """
        if not isinstance(column_list, list):
            raise TypeError("column_list should be of list type")
        if not column_list:
            raise ValueError("column_list cannot be empty")

        if max_categories and not isinstance(max_categories, int):
            raise TypeError("max_categories should be of int type")

        if min_frequency and not isinstance(min_frequency, (int, float)):
            raise ValueError("min_frequency should be of int/float type")

        logger.info("Started One-hot-encoding on training dataset")
        logger.info(f"Columns to do one-hot encode: {column_list}")

        enc_model = OneHotEncoder(
            handle_unknown="ignore",
            max_categories=max_categories,
            min_frequency=min_frequency,
        )
        enc_model.fit(self.input_data[column_list])

        output_df = pd.DataFrame(
            enc_model.transform(self.input_data[column_list]).toarray(),
            columns=enc_model.get_feature_names_out(column_list),
        )

        logger.info(f"Columns created in one-hot encoding: {output_df.columns}")

        logger.info("Ended One-hot encoding")

        return output_df, enc_model

    def one_hot_encode_on_test(
        self, column_list: List[str], one_hot_model: OneHotEncoder
    ) -> pd.DataFrame:
        """
        Create new features from one hot encode on test data
        Parameters:
            column_list: List of columns to be filled.
            one_hot_model: One-hot encode model with which training data is encoded
        Return:
            [pd.DataFrame]: Return pandas dataframe with new features created by one-hot encode
        """
        if not isinstance(column_list, list):
            raise TypeError("column_list should be of dictionary type")
        if not column_list:
            raise ValueError("column_list cannot be empty")

        if not isinstance(one_hot_model, OneHotEncoder):
            raise TypeError(
                "one_hot_model should be of sklearn.preprocessing._encoders.OneHotEncoder type"
            )
        if not one_hot_model:
            raise ValueError("one_hot_model cannot be empty")

        one_hot_column_list = one_hot_model.feature_names_in_.tolist()
        for item in column_list:
            if item not in one_hot_column_list:
                raise KeyError(f"{item} not in index")

        logger.info("Started one-hot encode feature creation on test data")
        logger.info(f"Columns to create new features using one-hot: {column_list}")

        output_df = pd.DataFrame(
            one_hot_model.transform(self.input_data[column_list]).toarray(),
            columns=one_hot_model.get_feature_names_out(column_list),
        )

        logger.info(f"Columns created in one-hot encoding: {output_df.columns}")

        logger.info("Ended One-hot encoding")

        return output_df
