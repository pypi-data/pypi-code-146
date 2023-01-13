"""Data pre-processing for ML"""
import pandas as pd
import numpy as np
from typing import List


def perform_binning_quantile(
   column: pd.Series, quantile: float = 0.5, bin_name: str = "Other"
) -> pd.DataFrame:
    """Bin low frequency values by quantile threshold.

    Args:
        column (pd.Series): Column to bin.
        quantile (float, optional): Quantile threshold. Defaults to 0.5.
        bin_name (str, optional): Name for bin. Defaults to "Other".

    Returns:
        pd.DataFrame: Value counts of dataframe.
    """
    column = column.copy(deep=True)
    counts = column.value_counts()
    for group in counts[counts < counts.quantile(quantile)].index:
        column = column.replace(group, bin_name)
    return column


def perform_binning_scalar(
    column: pd.Series, value: int = 2, bin_name: str = "Other"
) -> pd.DataFrame:
    """Bin low frequency values by a scalar value threshold.

    Args:
        column (pd.Series): Column to bin.
        value (int, optional): Scalar value threshold. Defaults to 2.
        bin_name (str, optional): Name for bin. Defaults to "Other".

    Returns:
        pd.DataFrame: Value counts of dataframe.
    """
    column = column.copy(deep=True)
    counts = column.value_counts()
    for group in counts[counts < value].index:
        column = column.replace(group, bin_name)
    return column


def perform_frequency_split_quantile(
    column: pd.Series, quantile: int = 0.5
) -> List[pd.Series]:
    """Split the value counts of the data in two frequency bins, low and high, based on quantile.

    Args:
        column (pd.Series): Column to split.
        quantile (int, optional): Quantile threshold. Defaults to 0.5.

    Returns:
        Tuple[pd.Series, pd.Series]: low_frequency, high_frequency
    """
    counts = column.value_counts()
    return [
        counts[counts < counts.quantile(quantile)],
        counts[counts >= counts.quantile(quantile)],
    ]


def perform_frequency_split_scalar(
    column: pd.Series, value: int = 2
) -> List[pd.Series]:
    """Split the value counts of the data in two frequency bins, low and high, based on scalar value.

    Args:
        column (pd.Series): Column to split.
        value (int, optional): Scalar threshold. Defaults to 2.

    Returns:
        Tuple[pd.Series, pd.Series]: low_frequency, high_frequency
    """
    counts = column.value_counts()
    return [counts[counts < value], counts[counts >= value]]


def perform_matrix_encoding(column: pd.Series, group_by: pd.Series, append_name: bool = True) -> pd.DataFrame:
    """Returns encoded values as a matrix of columns with binary values.

    Args:
        column (pd.Series): Column to perform the matrix on.
        group_by (pd.Series): Column to group_by, like id.

    Returns:
        pd.DataFrame: group_by column with matrix.
    """
    name = f"{column.name}_" if append_name else ""
    return (
        pd.DataFrame(
            {
                group_by.name: group_by.values,
                **{
                    f"{name}{value}": np.where(column == value, 1, 0)
                    for value in column.values
                },
            },
            index=column.index,
        )
        .groupby([group_by.name])
        .sum()
        .reset_index()
    )
