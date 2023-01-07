"""
This is an internal module, do not use it directly.
"""

from typing import Dict

import numpy as np
import pandas as pd
from pandas.api.types import is_integer_dtype, is_string_dtype


def embrace_integer(series: pd.Series) -> str:
    """
    Given a Series of integers, return the smallest type that will
    maintain information.
    """

    if not is_integer_dtype(series.dtype):
        raise TypeError(f"series type is {series.dtype}, expected an integer type")

    low = series.min()
    high = series.max()

    if low is not pd.NA and high is not pd.NA:
        known_types = [
            "uint8",
            "int8",
            "uint16",
            "int16",
            "uint32",
            "int32",
            "uint64",
            "int64",
        ]
        if series.isnull().any():
            known_types = [
                _type.replace("i", "I").replace("u", "U") for _type in known_types
            ]
        for _type in known_types:
            np_type = _type.lower()
            if np.iinfo(np_type).min <= low and high <= np.iinfo(np_type).max:
                return _type

    return series.dtype


def embrace_string(series: pd.Series) -> str:
    """
    Given a Series of strings, return the smallest type that will
    maintain information. Either 'string' or 'category'.
    """

    if not is_string_dtype(series.dtype):
        raise TypeError(f"series type is {series.dtype}, expected a string type")

    #
    # two approaches,
    #  0. convert and check memory savings -
    #   s.astype('category').memory_usage() // s.memory_usage()
    #  1. guess at savings based on counts and some tolerance -
    #   s.nunique() < len(s) * 0.42
    #
    # years of careful research says...
    #
    # (0) will give the right answer, at the cost of memory usage building the categorical,
    #     and we're assuming a memory constrained env
    # (1) will give a reasonable answer, at the cost of less memory usage building a set/map,
    #     and again we're assuming a memory constrained env
    #
    # len(set(s.values)) outperforms nunique() and often len(set(s))
    #
    # both can use a subset, e.g. s[:len(s)//10] or s.sample(frac=.1), but sample() is slower
    #
    # the tolerance when a category out performance is persnickety
    #

    return (
        "category"
        if len(set(series[: len(series) // 3])) < len(series) // 11
        else series.dtype
    )


def embrace_series(series: pd.Series, *, strings: bool = True) -> str:
    """
    Given a Series, return the smallest type that will maintain information.
    """

    if not hasattr(series, "dtype"):
        raise TypeError(f"{type(series)} is not Series-like, missing dtype attribute")

    if strings and is_string_dtype(series.dtype):
        return embrace_string(series)
    if is_integer_dtype(series.dtype):
        return embrace_integer(series)

    return series.dtype


def hug_series(series: pd.Series, *, strings: bool = True) -> pd.Series:
    """
    Given a Series, return a new Series with the smallest types that will maintain information.
    """

    if not hasattr(series, "astype"):
        raise TypeError(f"{type(series)} is not Series-like, missing astype attribute")

    return series.astype(embrace_series(series, strings=strings))


def embrace_dataframe(
    df: pd.DataFrame, *, strings: bool = True  # pylint: disable=C0103
) -> Dict[str, str]:
    """
    Given a DataFrame, return a dict of {col -> smallest type that will maintain information}.
    """

    if not hasattr(df, "columns"):
        raise TypeError(f"{type(df)} is not DataFrame-like, missing columns attribute")

    return {col: embrace_series(df[col], strings=strings) for col in df.columns}


def hug_dataframe(
    df: pd.DataFrame, *, strings: bool = True  # pylint: disable=C0103
) -> pd.DataFrame:
    """
    Given a DataFrame, return a new DataFrame with the smallest types that will
    maintain information.
    """

    if not hasattr(df, "columns"):
        raise TypeError(f"{type(df)} is not DataFrame-like, missing columns attribute")

    return df.astype(
        {col: embrace_series(df[col], strings=strings) for col in df.columns}
    )


def golden_snub():
    """
    Monkey patch Pandas' DataFrame and Series with a hug() method that returns
    a new object with reduced types.
    """

    pd.DataFrame.hug = hug_dataframe
    pd.Series.hug = hug_series
