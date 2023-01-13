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


class VariableCategorization:
    def __init__(self, df: pd.DataFrame):
        self.data = df

    def datatypes(self) -> Dict[str, str]:
        """
        Shape of the dataframe
        """
        return dict(self.data.dtypes)

    def is_DATE(self, column_name: str) -> bool:
        """
        Function returns true if the column in dataframe has date type
        Args:
            column_name ([string]): [name of the feature]
        Returns:
            [Boolean]: [return true is columns is date type otherwise false]
        """
        try:
            self.data[column_name][:10].astype("datetime64[ns]")
            return True
        except Exception:
            return False

    def is_sequence(self, column_name: str) -> bool:
        """
        Function check if the column has sequence values or not
        Args:
            column_name ([string]): [name of the feature]
        Returns:
            [Boolean]: [return true if unique values in column follow a sequence else false]
        """
        df_nonNull = pd.Series(self.data[column_name].dropna().sort_values().unique())

        if df_nonNull.diff().dropna().eq(1).all():
            return True
        return False

    def is_numeric(self, column_name: str) -> bool:
        """
        Function checks if the dataframe has numeric values
        Args:
            column_name ([string]): [name of the feature]
        Returns:
            [Boolean]: [return true if it is numeric]
        """
        try:
            unique_count_prob = (
                len(self.data[column_name].unique())
                / self.data[column_name].dropna().shape[0]
            )

            if unique_count_prob < 0.2 and self.is_sequence(column_name):
                return False
            return True
        except Exception as e:
            raise e

    def execute_variable_categization(
        self, datatype: Dict[str, str], column_name: str
    ) -> Tuple[str, List[str]]:
        """ "
        Functions that drives whole process
        Args:
            datatype ([dict]): [dictnory of columns and its datatypes]
            column_name ([string]): [name of the feature]
        Returns:
            [list]: [return list which has column_name, datatype and category]
        """

        if datatype[column_name] in ["boolean"]:
            cat = "CATEGORIC"
            return column_name, [str(datatype[column_name]), cat]

        if datatype[column_name] in ["timestamp", "date"]:
            cat = "DATE"
            return column_name, [str(datatype[column_name]), cat]

        if datatype[column_name] in [
            "short",
            "long",
            "int",
            "float",
            "double",
        ] and self.is_numeric(column_name):
            cat = "NUMERIC"
            return column_name, [str(datatype[column_name]), cat]

        if datatype[column_name] in ["string", "object"] and self.is_DATE(column_name):
            cat = "DATE"
            return column_name, [str(datatype[column_name]), cat]
        else:
            cat = "CATEGORIC"
            return column_name, [str(datatype[column_name]), cat]

    def attribute_categorization(
        self, id_column: str = "", label: str = ""
    ) -> Dict[str, List[str]]:
        """
        Function categorizes all coulmns in dataframe into ID, LABEL, DATE, NUMERIC, CATEGORIC
        Args:
            label ([String]): [label column name]
            id_column ([String]): ID column name]
        Returns:
            [DataFrame]: [return pandas DataFrame which has column_name, dataframe_name source_data_type and category]
        """
        if not isinstance(id_column, str):
            raise TypeError("id_column needs to be a string")
        if not isinstance(label, str):
            raise TypeError("label needs to be a string")
        categorized_dict = {}
        datatype = self.datatypes()

        df_columns = self.data.columns

        if id_column:
            categorized_dict[id_column] = [str(datatype[id_column]), "ID"]

        column_list = list(set(df_columns) - {id_column})

        if label != "":
            column_name, label_det = self.execute_variable_categization(datatype, label)
            if label_det[1] == "CATEGORIC":
                label_det[1] = "LABEL_CATEGORIC"
            if label_det[1] == "NUMERIC":
                label_det[1] = "LABEL_NUMERIC"
            categorized_dict[column_name] = label_det
            column_list.remove(label)

        for column_name in column_list:
            feat_name, dtypes = self.execute_variable_categization(
                datatype, column_name
            )
            categorized_dict[feat_name] = dtypes

        return categorized_dict
