#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#
import logging
from typing import Dict
from typing import List
from typing import Tuple

import pandas as pd

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


class FillMissingValues:
    def __init__(self, input_data: pd.DataFrame):
        self.input_data = input_data
        self.central_tendancy_meta: Dict[str, int] = {}

    def get_aggr(self, col: pd.Series, aggr_func: str) -> pd.Series:
        aggr_value = col.aggregate(func=aggr_func)
        if aggr_func == "mode":
            aggr_value = aggr_value[0]

        column_name = col.name

        logger.info(
            f"{column_name} has {self.input_data[column_name].isna().sum()} missing values"
        )

        self.central_tendancy_meta[column_name] = aggr_value

        logger.info(f"{aggr_func} for the {column_name} is {aggr_value}")

        try:
            return col.fillna(aggr_value)
        except Exception as e:
            logger.error(f"Something went wrong while filling missing values: {str(e)}")
            raise (
                Exception("Error: Something went wrong while filling missing values")
            )

    def fill_with_central_tendancy(
        self, column_list: List[str], aggr_func: str
    ) -> Tuple[pd.DataFrame, Dict[str, int]]:
        """
        Fill missing value category with measure of Cental Tendancy i.e., mean/median/mode
        Parameters:
            column_list: List of columns to be filled.
            aggr_func: Aggregate Function mean/median/mode

        Return:
            [pd.DataFrame]: Return pandas dataframe with columns filled
            [dict]: Return a dictionary which has two keys data and transformation
            Example : {
                "column_name" : x
                "column_name" : x
            }
        """
        if not isinstance(column_list, list):
            raise TypeError("column_list should be of list type")
        if not column_list:
            raise ValueError("column_list cannot be empty")

        if not isinstance(aggr_func, str):
            raise TypeError("aggr_func should be of string type")
        if not aggr_func:
            raise ValueError("aggr_func cannot be empty")
        if aggr_func not in ["mean", "median", "mode"]:
            raise ValueError("aggr_func should be one of mean/median/mode")

        logger.info("Started fill missing value")
        logger.info(f"Columns to fill with {aggr_func}: {column_list}")

        output_df = pd.DataFrame()

        output_df[column_list] = self.input_data[column_list].apply(
            lambda x: self.get_aggr(x, aggr_func)
        )

        logger.info(f"Ended filling missing values with {aggr_func}")

        return output_df, self.central_tendancy_meta

    def fill_with_central_tendancy_on_test(
        self, column_list: List[str], meta_dict: Dict[str, str]
    ) -> pd.DataFrame:
        """
        Fill missing value with mean/median/mode impute for test dataset
        Parameters:
            column_list: List of columns to be filled.
            meta_dict: model meta with which the data has to be filled
        Return:
            [pd.DataFrame]: Return pandas dataframe with columns filled
        """
        if not isinstance(column_list, list):
            raise TypeError("column_list should be of list type")
        if not column_list:
            raise ValueError("column_list cannot be empty")

        if not isinstance(meta_dict, dict):
            raise TypeError("meta_dict should be of list type")
        if not meta_dict:
            raise ValueError("meta_dict cannot be empty")

        logger.info("Started fill missing value with on test data")
        logger.info(f"Columns to fill: {column_list}")
        logger.info(
            f"The data has {self.input_data[column_list].isna().sum()} missing values"
        )

        output_df = pd.DataFrame()

        output_df[column_list] = self.input_data[column_list].apply(
            lambda x: x.fillna(meta_dict[x.name])
        )

        logger.info("Ended filling missing values on test data")

        return output_df

    def sort_dataframe(self, sort_columns: List[str]) -> None:
        """
        Sort dataframe by a specified column
        Args:
            column: The columns list to sort the dataframe with
        """
        try:
            if not isinstance(sort_columns, list):
                raise TypeError("sort_columns should be of list type")
            if not sort_columns:
                raise ValueError("sort_columns cannot be empty")
            logger.info(f"Sorting dataframe with {sort_columns}..")
            self.input_data = self.input_data.sort_values(by=sort_columns)
            logger.info("Dataframe sorted successfully")
        except Exception as e:
            raise e

    def forward_backward_fill(
        self, column_list: List[str], fill_func: str
    ) -> pd.DataFrame:
        """
        Forward and backward fill missing value
        Parameters:
            column_list: List of columns to be filled.
            fill_func: Fill functions ffill/bfill

        Return:
            [pd.DataFrame]: Return pandas dataframe with columns filled

        """
        if not isinstance(column_list, list):
            raise TypeError("column_list should be of list type")
        if not column_list:
            raise ValueError("column_list cannot be empty")

        if not isinstance(fill_func, str):
            raise TypeError("fill_func should be of string type")
        if not fill_func:
            raise ValueError("fill_func cannot be empty")
        if fill_func not in ["ffill", "bfill"]:
            raise ValueError("fill_func should be one of ffill/bfill")
        if fill_func == "ffill":
            main_fill = fill_func
            sub_fill = "bfill"
            method = "forward fill"
        else:
            main_fill = fill_func
            sub_fill = "ffill"
            method = "backward fill"
        logger.info(f"Started {method} missing value")
        logger.info(f"Columns to fill: {column_list}")
        logger.info(
            f"The data has {self.input_data[column_list].isna().sum()} missing values"
        )
        output_df = pd.DataFrame()
        output_df[column_list] = self.input_data[column_list].apply(
            lambda x: x.fillna(method=main_fill).fillna(method=sub_fill)
        )
        logger.info(f"Ended filling missing values with {method}")
        return output_df

    def fill_new_category(
        self, column_list: List[str], fill_value: str
    ) -> pd.DataFrame:
        """
        Fill the missing values with a string value
        Args::
            column_list: List of columns to be filled.
            fill_value: The value to fill the columns with

        Return:
            [pd.DataFrame]: Return pandas dataframe with columns filled

        """
        try:
            if not isinstance(column_list, list):
                raise TypeError("column_list should be of list type")
            if not column_list:
                raise ValueError("column_list cannot be empty")

            if not isinstance(fill_value, str):
                raise TypeError("fill_value should be of string type")
            if not fill_value:
                raise ValueError("fill_value cannot be empty")

            logger.info("Started fill with value imputer")
            logger.info(f"Columns to fill: {column_list}")
            logger.info(
                f"The data has {self.input_data[column_list].isna().sum()} missing values"
            )
            logger.info(f"Filling columns with new category: {fill_value}")
            output_df = pd.DataFrame()
            output_df[column_list] = self.input_data[column_list].apply(
                lambda x: x.fillna(fill_value)
            )
            return output_df
        except Exception as e:
            raise e

    def fill_with_zero(self, column_list: List[str]) -> pd.DataFrame:
        """
        Fill the missing values with zero
        Args::
            column_list: List of columns to be filled.
        Return:
            [pd.DataFrame]: Return pandas dataframe with columns filled

        """
        try:
            if not isinstance(column_list, list):
                raise TypeError("column_list should be of dictionary type")
            if not column_list:
                raise ValueError("column_list cannot be empty")
            logger.info("Started fill with zero imputer")
            logger.info(f"Columns to fill: {column_list}")
            logger.info(
                f"The data has {self.input_data[column_list].isna().sum()} missing values"
            )
            logger.info("Filling columns with zero")
            output_df = pd.DataFrame()
            output_df[column_list] = self.input_data[column_list].fillna(0)
            return output_df
        except Exception as e:
            raise e
