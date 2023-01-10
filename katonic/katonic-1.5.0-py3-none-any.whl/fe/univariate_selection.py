#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#
import logging
from typing import List

import pandas as pd

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


class UnivariateSelection:
    def __init__(self, input_data: pd.DataFrame, target_column: pd.Series):
        self.input_data = input_data
        self.target_column = target_column

    def non_null_columns(self) -> pd.DataFrame:
        filtered_data = self.input_data.dropna(axis=1)
        dropped_cols = set(filtered_data.columns.to_list()) ^ set(
            self.input_data.columns.to_list()
        )
        logger.info(f"Dropped columns are: {dropped_cols}")
        return filtered_data

    def non_constant_columns(self, column_list: List[str], threshold: float = 0.1):
        non_zero_variance_column_list = []
        std_dict = self.input_data[column_list].std()
        non_zero_variance_column_list = [
            column
            for column, std in std_dict.items()
            if std and float(std) * 2 > threshold
        ]
        logger.info(f"Non constant columns are: {non_zero_variance_column_list}")
        return non_zero_variance_column_list
