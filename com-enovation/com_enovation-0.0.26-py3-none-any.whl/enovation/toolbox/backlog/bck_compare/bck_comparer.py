from inspect import stack
from logging import Logger, getLogger
from typing import Tuple

import numpy as np
from jsonschema import validate
from numpy import array
from pandas import DataFrame

from com.enovation.helper.pandas_dataframe_typer import PandasDataframeTyper


class BacklogComparer:
    _logger: Logger = getLogger(__name__)

    str__source_column_suffix: str = "_from"
    str__target_column_suffix: str = "_to"
    str__delta_column_suffix: str = "_delta"

    str__dict_columns__json_tag__key_columns: str = "key columns"
    str__dict_columns__json_tag__compared_columns: str = "compared columns"
    str__dict_columns__json_tag__type: str = "type"
    str__dict_columns__json_tag__compare_logic: str = "compare logic"
    str__dict_columns__json_tag__delta_type: str = "delta type"

    lst__dict_columns__json_tags: list[str] = [
        str__dict_columns__json_tag__key_columns,
        str__dict_columns__json_tag__compared_columns,
        str__dict_columns__json_tag__type
    ]

    def compare(
            self,
            df_src: DataFrame,
            df_tgt: DataFrame,
            dict_columns: dict
    ) -> DataFrame:
        """

        :param df_src:
        :param df_tgt:
        :param dict_columns: dictionary
        :return:
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        # From the dict_columns, we prepare the various sub-dictionaries/ lists
        dict_the_columns_types: dict[str]  # A dictionary to properly type the dataframes (both key and comparable col)
        lst_the_compared_columns: list[str]  # A list of the columns' labels to compare
        lst_the_key_columns: list[str]  # A list of the key columns' labels to merge dataframes
        dict_the_columns_comparison_logics: dict  # A dictionary to properly associate comparison functions to columns

        # First, we check the dict_columns. Exception will be thrown in case anything is incorrect
        self._check_parameter_dict_columns(
            df_src=df_src,
            df_tgt=df_tgt,
            dict_columns=dict_columns
        )

        # First, we process the dict_columns, and raise an exception should its format be incorrect
        dict_the_columns_types, lst_the_compared_columns, lst_the_key_columns, dict_the_columns_comparison_logics = \
            self._process_dict_columns(
                dict_columns=dict_columns
            )

        # We type and merge columns of interest from both dataframes into one single dataframe
        df_the_merged_dataframes: DataFrame = self._type_and_merge_data_frames(
            df_src=df_src,
            df_tgt=df_tgt,
            dict_columns_types=dict_the_columns_types,
            lst_compared_columns=lst_the_compared_columns,
            lst_key_columns=lst_the_key_columns
        )

        df_the_delta: DataFrame = self._reconcile(
            df=df_the_merged_dataframes,
            dict_columns_comparison_logics=dict_the_columns_comparison_logics
        )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")

        return df_the_delta

    def compare_into_excel(
            self,
            df_src: DataFrame,
            df_tgt: DataFrame,
            dict_columns: dict,
            str_path: str
    ):
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        df_the_results: DataFrame = self.compare(
            df_src=df_src,
            df_tgt=df_tgt,
            dict_columns=dict_columns
        )

        df_the_results.to_excel(str_path)

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")

    def _check_parameter_dict_columns(
            self,
            df_src: DataFrame,
            df_tgt: DataFrame,
            dict_columns: dict[str]
    ):
        """
        Function that check the parameter dict_columns provided as an input:
            - If parameter is correct, the function is returning (no value returned)
            - Otherwise, an exception is thrown.

        dict_columns should follow the following structure:
          {
            "key columns": {
              "the label of the key column": {
                "type": "the type of the key column, as defined in PandasDataframeTyper.lst__types",
              },
            },
            "compared columns": {
              "the label of the column to compare": {
                "type": "the type of the column to compare, as defined in PandasDataframeTyper.lst__types",
                "compare logic": "the function to compare",
                "delta type": "the type of the delta, as defined in PandasDataframeTyper.lst__types"
              }
            }
          }

        ---

        Business Rules:
            - BR_101: parameter "key columns" should exist
            - BR_102: parameter "key columns" should be a dictionary
            - BR_103: parameter "key columns" should contain at least one property
            - BR 104: parameter "key columns" should only contains keys among columns intersecting in both dataframes
            - BR_105: parameter "key columns" should contains records containing "type" key only
            - BR_106: parameter "key columns" should contains records containing "type" key
            - BR_107: parameter "key columns - type" should be among the ones defined in
              PandasDataframeTyper.lst__types

            - BR_201: parameter "compared columns" should exist
            - BR_202: parameter "compared columns" should be a dictionary
            - BR_203: parameter "compared columns" should contain at least one property
            - BR 204: parameter "compared columns" should only contains keys among columns intersecting in both dfs
            - BR_205: parameter "compared columns" should contains records containing "type" key only
            - BR_206: parameter "compared columns" should contains records containing "type" key
            - BR_207: parameter "compared columns - type" should be among the ones defined in
              PandasDataframeTyper.lst__types

            - BR_301: "key columns" and "compared columns" should be distinct. Aka no column should be listed as
              a key and a compared column at the same time

        :param df_tgt:
        :param df_src:
        :param dict_columns:
        :return: a tuple made of
          - dict_columns_types: the dictionary to type the dataframe (see PandasDataframeTyper)
          - lst_compared_columns: the list of columns to compare
          - lst_key_columns: the list of columns to be used as key to compare records across dataframes
        """

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        # First, we get the union of columns across both dataframes
        array_the_columns: array = np.intersect1d(df_src.columns, df_tgt.columns)

        dict_the_json_schema: dict = {

            "title": "id1",

            # Type dictionary
            "type": "object",

            # with properties
            "properties": {

                # "key columns"
                self.str__dict_columns__json_tag__key_columns: {

                    # of type dictionary
                    "type": "object",

                    # that contains at least one record
                    "minProperties": 1,

                    # among the following properties
                    "properties": {

                        # that could be any column in common across the 2 dataframes
                        i_col: {"$ref": "#/$defs/key_column"}
                        for i_col in array_the_columns
                    },

                    # we forbid any other property
                    "additionalProperties": False
                },

                # The second node is the compared columns
                self.str__dict_columns__json_tag__compared_columns: {

                    # of type dictionary
                    "type": "object",

                    # that contains at least one record
                    "minProperties": 1,

                    # among the following properties
                    "properties": {

                        # that could be any column in common across the 2 dataframes
                        i_col: {"$ref": "#/$defs/compared_column"}
                        for i_col in array_the_columns
                    },

                    # we forbid any other property
                    "additionalProperties": False
                },
            },

            # that requires properties
            "required": [
                self.str__dict_columns__json_tag__key_columns,
                self.str__dict_columns__json_tag__compared_columns
            ],

            "$defs": {

                # Sub-type "key_column"
                "key_column": {

                    # Type dictionary
                    "type": "object",

                    # with properties
                    "properties": {
                        # "type"
                        self.str__dict_columns__json_tag__type: {
                            # of type string
                            "type": "string",
                            # among predefined values
                            "enum": PandasDataframeTyper.lst__types
                        }
                    },

                    # we forbid any other property
                    "additionalProperties": False,

                    # that requires properties
                    "required": [
                        self.str__dict_columns__json_tag__type
                    ],
                },

                # Sub-type "compared_column"
                "compared_column": {

                    # Type dictionary
                    "type": "object",

                    # with properties
                    "properties": {
                        # "type"
                        self.str__dict_columns__json_tag__type: {
                            # of type string
                            "type": "string",
                            # among predefined values
                            "enum": PandasDataframeTyper.lst__types
                        },
                        # compare logic
                        self.str__dict_columns__json_tag__compare_logic: {
                            # of type string
                            "type": "string",
                        },
                        # delta type
                        self.str__dict_columns__json_tag__delta_type: {
                            # of type string
                            "type": "string",
                        }

                    },

                    # we forbid any other property
                    "additionalProperties": False,

                    # that requires properties
                    "required": [
                        self.str__dict_columns__json_tag__type,
                        # self.str__dict_columns__json_tag__compare_logic -> If not set, we test equality using "=="
                        # self.str__dict_columns__json_tag__delta_type -> If not set, we use the column type
                    ],
                }
            },
        }

        self._logger.debug(f"_check_parameter_dict_columns relies on a jsonschema which is:\n{dict_the_json_schema}")

        # Additional check: BR_301:
        # "key columns" and "compared columns" should be distinct. Aka no column should be listed as a key and a
        # compared column at the same time
        lst_intersecting_columns: list[str] = [
            i_key
            for i_key in (
                    dict_columns[self.str__dict_columns__json_tag__key_columns].keys()
                    & dict_columns[self.str__dict_columns__json_tag__compared_columns].keys()
            )
        ]

        if len(lst_intersecting_columns) > 0:
            raise Exception(
                f"the parameter dict_columns contains columns defined as both a key and a compared column, while these "
                f"universes should not intersect.\n"
                f"\t Faulty columns: {','.join(lst_intersecting_columns)}"
            )

        validate(
            instance=dict_columns,
            schema=dict_the_json_schema
        )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")

    def _process_dict_columns(
            self,
            dict_columns: dict[str]
    ) -> Tuple[
        dict[str],  # dict_columns_types: the dictionary to properly type the dataframes (both key and comparable col)
        list[str],  # the list of the columns' labels to compare
        list[str],  # the list of the key columns' labels to merge dataframes
        dict        # the dictionary to properly associate comparison functions to columns
    ]:
        """
        Function that process the dict_columns provided as an input, and return the various lists and dictionaries
        later used in the logic

        Assumption: dict_columns were previously checked (through function _check_parameter_dict_columns

        :param dict_columns:
        :return: a tuple made of
          - dict_columns_types: the dictionary to properly type the dataframes (both key and comparable col)
            (see PandasDataframeTyper)
          - lst_compared_columns: the list of the columns' labels to compare
          - lst_key_columns: the list of the key columns' labels to merge dataframes
          - dict_columns_comparison_logics: the dictionary to properly associate comparison functions to columns
        """

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        # #############################################################################################################
        # 1. We prepare the dictionary used to type the dataframes
        dict_return_columns_types: dict[str] = {
            i_key: i_val[self.str__dict_columns__json_tag__type]
            for i_key, i_val in dict_columns[self.str__dict_columns__json_tag__key_columns].items()
        }
        dict_return_columns_types.update(
            {
                i_key: i_val[self.str__dict_columns__json_tag__type]
                for i_key, i_val in dict_columns[self.str__dict_columns__json_tag__compared_columns].items()
            }
        )

        # #############################################################################################################
        # 2. We prepare the list of columns to compare. Other columns will be discarded
        lst_return_comparable_columns: list[str] = [
            i_key
            for i_key in dict_columns[self.str__dict_columns__json_tag__compared_columns]
        ]

        # #############################################################################################################
        # 3. We prepare the list of key columns to merge dataframes.
        lst_return_key_columns: list[str] = [
            i_key
            for i_key in dict_columns[self.str__dict_columns__json_tag__key_columns]
        ]

        # #############################################################################################################
        # 4. We prepare the dictionary with the comparison logics as functions
        dict_columns_comparison_logics: dict = {
            i_key:
                f"("
                f"  ("
                f"    row['{i_key + self.str__source_column_suffix}'].isnull() "
                f"    & row['{i_key + self.str__target_column_suffix}'].isnull()"
                f"  )"
                f"  | ("
                f"    row['{i_key + self.str__source_column_suffix}'] "
                f"    == row['{i_key + self.str__target_column_suffix}']"
                f"  )"
                f")"
                if self.str__dict_columns__json_tag__compare_logic not in i_value
                else
                f"("
                f"  ("
                f"    row['{i_key + self.str__source_column_suffix}'].isnull() "
                f"    & row['{i_key + self.str__target_column_suffix}'].isnull()"
                f"  )"
                f"  | ("
                + i_value[self.str__dict_columns__json_tag__compare_logic].replace(
                        "src",
                        f"row['{i_key + self.str__source_column_suffix}']"
                ).replace(
                    "tgt",
                    f"row['{i_key + self.str__target_column_suffix}']"
                ) +
                f"  )"
                f")"

            for i_key, i_value in dict_columns[self.str__dict_columns__json_tag__compared_columns].items()
        }

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")

        return \
            dict_return_columns_types, \
            lst_return_comparable_columns, \
            lst_return_key_columns, \
            dict_columns_comparison_logics

    def _type_and_merge_data_frames(
            self,
            df_src: DataFrame,
            df_tgt: DataFrame,
            dict_columns_types: dict,
            lst_key_columns: list[str],
            lst_compared_columns: list[str],
    ) -> DataFrame:
        """
        Dataframes received as inputs comply to the following:
        - Columns are properly typed
        - Only columns to compare are there.

        :param df_src:
        :param df_tgt:
        :param lst_key_columns:
        :param lst_compared_columns:
        :return:
        """
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        # We filter out the useless columns
        df_the_filtered_src: DataFrame = df_src[lst_key_columns + lst_compared_columns]
        df_the_filtered_tgt: DataFrame = df_tgt[lst_key_columns + lst_compared_columns]

        # We type the columns
        df_the_typed_src: DataFrame = PandasDataframeTyper().type(
            df_to_type=df_the_filtered_src.copy(),
            dict_columns_to_type=dict_columns_types,
            b_strict=True
        )
        df_the_typed_tgt: DataFrame = PandasDataframeTyper().type(
            df_to_type=df_the_filtered_tgt.copy(),
            dict_columns_to_type=dict_columns_types,
            b_strict=True
        )

        # We merge
        df_the_return: DataFrame = df_the_typed_tgt.merge(
            right=df_the_typed_src,
            on=lst_key_columns,
            suffixes=(
                self.str__target_column_suffix,
                self.str__source_column_suffix,
            )
        )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")
        return df_the_return

    def _reconcile(
            self,
            df: DataFrame,
            dict_columns_comparison_logics: dict
    ) -> DataFrame:
        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is called")

        df_the_return: DataFrame = df

        for i_column_label, i_logic in dict_columns_comparison_logics.items():
            df_the_return = df_the_return.assign(
                **{
                    i_column_label + self.str__delta_column_suffix: lambda row: eval(i_logic)
                }
            )

        self._logger.debug(f"Function '{stack()[0].filename} - {stack()[0].function}' is returning")
        return df_the_return
