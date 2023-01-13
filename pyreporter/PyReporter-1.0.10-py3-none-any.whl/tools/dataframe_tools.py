import pandas as pd
import copy
import asyncio
from ..data_frames.cell import Cell
from typing import Any, Optional, Dict, Callable, List


# DataFrameTools: Useful tools for handling Panda Dataframes
class DataFrameTools():
    """
    Useful Tools for handling with `DataFrame`_
    """

    WIDTH_TOLERANCE = 4


    # remove_top_rows(no_of_rows): Removes the first 'no_of_rows' rows from 'df'
    # requires: no_of_rows >= 0
    @classmethod
    def remove_top_rows(cls, df: pd.DataFrame, no_of_rows: int) -> pd.DataFrame:
        """
        removes the top rows from the dataframe

        Parameters
        ----------
        df: `DataFrame`_
            The talbe being manipulated

        no_of_rows: :class:`int`
            The number of rows to be removed from the top

        Returns
        -------
        `DataFrame`_
            The resultant table with the top rows removed
        """
        return df.iloc[no_of_rows:]


    # ind_select_columns(df, start, end): Select a subset of columns from 'start'
    #   to 'end' from 'df'
    # requires: end >= start >= 0
    @classmethod
    def ind_select_columns(cls, df: pd.DataFrame, start: int, end: int) -> pd.DataFrame:
        """
        Selects a subset of columns from the table from 'start' to 'end'

        Requires: end >= start >= 0

        Parameters
        ----------
        df: `DataFrame`_
            The talbe being manipulated

        start: :class:`int`
            The left index of the column to start selecting

        end: :class:`int`
            The right index of the column to stop selecting

        Returns
        -------
        `DataFrame`_
            The resultant table with the selected columns
        """
        return df.iloc[: , start:end]


    # ind_subset(df, row_start, row_end, col_start, col_end): Selects a subset of the
    #   table from 'df'
    # requires: row_end >= row_start >= 0
    #           col_end >= col_start >= 0
    @classmethod
    def ind_subset(cls, df: pd.DataFrame, row_start: int, row_end: int, col_start: int, col_end: int) -> pd.DataFrame:
        """
        Selects a subset of the input source table

        Parameters
        ----------
        row_start: :class:`int`
            The top index position of the new table

        row_end: :class:`int`
            The bottom index position of the new table

        col_start: :class:`int`
            The left index position of the new table

        col_end: :class:`int`
            The right index position of the new table

        Returns
        -------
        `DataFrame`_
            The resultant subset of the original table
        """

        return df.iloc[row_start:row_end, col_start:col_end]


    # replace(df, lookup_df, df_key, lookup_df_key, desired_cols_dict): Replaces
    #   the values in the column 'df_key' from 'df' with values from the column
    #   'lookup_df_key' from 'lookup_df'
    # Note: the keys in 'desired_cols_dict' are column names from 'lookup_df'
    #           and the values in 'desired_cols_dict' are the column names from 'df'
    @classmethod
    def replace(cls, df: pd.DataFrame, lookup_df: pd.DataFrame, df_key: str,
                lookup_df_key: str, desired_cols_dict: Dict[str, str]) -> pd.DataFrame:
        """

        """

        df = df.join(lookup_df.set_index(lookup_df_key), on = df_key)

        # prepare the columns to remove in the joined table
        columns_to_remove = list(lookup_df.columns)
        columns_to_remove.remove(lookup_df_key)
        columns_to_remove = list(set(columns_to_remove) - set(desired_cols_dict.keys()))
        columns_to_remove = columns_to_remove + list(desired_cols_dict.values())

        # remove the extra columns
        df = df.drop(labels=columns_to_remove, axis=1)

        # rename the columns
        return df.rename(columns = desired_cols_dict)


    # sumproduct(df, col_lst, sum_col_name): Retreives the sumproduct of 'col_lst'
    #   from 'df'
    @classmethod
    def sumproduct(cls, df: pd.DataFrame, col_lst: List[Any], sum_col_name = "Product") -> float:
        # retrieve only the values portion of the dataframe
        product_df = df[col_lst]
        product_df = cls.celled_df_to_value_df(product_df)

        # compute the sumproduct
        product_df[sum_col_name]  = 1
        for col in col_lst:
            product_df[sum_col_name] = product_df[sum_col_name] * product_df[col]

        return product_df[sum_col_name].sum()


    # to_celled_df(cell): converts 'cell' to a 'Cell' object
    @classmethod
    def to_celled_df(cls, cell: Any):
        if (not isinstance(cell, Cell)):
            cell = Cell(cell)
        return cell


    # get_cell_value(cell): Retrives only the values portion of 'cell'
    @classmethod
    def get_cell_value(cls, cell):
        if (isinstance(cell, Cell)):
            cell = cell.value
        return cell


    # df_to_celled_df(df): Transforms 'df' to a dataframe with Cells
    @classmethod
    def df_to_celled_df(cls, df: pd.DataFrame) -> pd.DataFrame:
        return df.applymap(lambda cell: cls.to_celled_df(cell))


    # celled_df_to_display_df(df): Only extract the values to be displayed for 'df'
    @classmethod
    def celled_df_to_display_df(cls, df: pd.DataFrame) -> pd.DataFrame:
        return df.applymap(lambda cell: cell.get_display())


    # celled_df_to_value_df(df): Only extract the values portion of 'df'
    @classmethod
    def celled_df_to_value_df(cls, df: pd.DataFrame) -> pd.DataFrame:
        return df.applymap(lambda cell: cls.get_cell_value(cell))


    # print_celled_df(df): Prints a dataframe
    #  Note: all values in 'df' are a 'Cell' Object
    @classmethod
    def print_celled_df(cls, df: pd.DataFrame):
        temp_df = copy.deepcopy(df)
        cls.celled_df_to_df_val(temp_df)


    # ex_process_width(width): Process the width to be optimized for autofit in excel
    @classmethod
    def ex_process_width(cls, width: float) -> float:
        return width + cls.WIDTH_TOLERANCE


    # col_get_max_width(df): Retrieves the maximum string width of each column
    @classmethod
    def col_get_max_width(cls, df: pd.DataFrame, with_header: bool = False):
        autofitted_cols_lst = []

        for col in df:
            max_width = df[col].map(lambda cell: len(str(cell.value))).max()
            if (with_header):
                max_width = max(max_width, len(str(col)))

            max_width = cls.ex_process_width(max_width)

            autofitted_cols_lst.append(max_width)
        return autofitted_cols_lst
