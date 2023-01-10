"""
  Collection of utility functions to do with datetime for faster analysis
"""

from typing import Optional

import pandas as pd


def add_ymd(  # type: ignore[no-any-unimported]
    _df: pd.DataFrame, date_column: str
) -> pd.DataFrame:
    """Utility function to split a date column into year, month and day

    Args:
        __df (dataframe): The dataframe to split
        date_column (datetime): The column to split

    Returns:
        dataframe: The dataframe with the split columns
    """

    _df["year"] = _df[date_column].dt.year.fillna(0).astype("int")
    _df["month"] = _df[date_column].dt.month.fillna(0).astype("int")
    _df["day"] = _df[date_column].dt.day.fillna(0).astype("int")

    return _df


def add_hms(  # type: ignore[no-any-unimported]
    _df: pd.DataFrame, date_column: str
) -> pd.DataFrame:
    """Utility function to split a date column into hour, minute and second

    Args:
        __df (dataframe): The dataframe to split
        date_column (datetime): The column to split

    Returns:
        dataframe: The dataframe with the split columns
    """

    _df["hour"] = _df[date_column].dt.hour.fillna(0).astype("int")
    _df["minute"] = _df[date_column].dt.minute.fillna(0).astype("int")
    _df["second"] = _df[date_column].dt.second.fillna(0).astype("int")

    return _df


def add_month_name(  # type: ignore[no-any-unimported]
    _df: pd.DataFrame, date_column: str, locale: Optional[str] = "no_NO"
) -> pd.DataFrame:
    """
    Utility function to add the month name to a dataframe

    Args:
        _df (dataframe): the dataframe to add the month name to
        date_column (datetime): The column with the date
        locale (str, optional): Locale to use, defualts to no_NO.

    Returns:
        dataframe: the dataframe with the month name added
    """

    _df["month_name"] = _df[date_column].dt.month_name(locale=locale).fillna("")

    return _df


def add_week_day(  # type: ignore[no-any-unimported]
    _df: pd.DataFrame, date_column: str
) -> pd.DataFrame:
    """Utility function to add the week day to a dataframe

    Args:
        _df (dataframe): the dataframe to add the week day to
        date_column (datetime): The column with the date

    Returns:
        dataframe: the dataframe with the week day added
    """

    _df["week_day"] = _df[date_column].dt.dayofweek.fillna(-1).astype("int")

    return _df


def add_week_number(  # type: ignore[no-any-unimported]
    _df: pd.DataFrame, date_column: str
) -> pd.DataFrame:
    """Utility function to add the week number to a dataframe

    Args:
        _df (dataframe): the dataframe to add the week number to
        date_column (datetime): The column with the date

    Returns:
        dataframe: the dataframe with the week number added
    """

    _df["week_number"] = _df[date_column].dt.week.fillna(0).astype("int")

    return _df


def add_week_day_name(  # type: ignore[no-any-unimported]
    _df: pd.DataFrame,
    date_column: str,
    locale: Optional[str] = "no_NO",
    nynorsk: Optional[bool] = False,
) -> pd.DataFrame:
    """Utility function to add the week day name to a dataframe

    Args:
        _df (dataframe): the dataframe to add the week day name to
        date_column (datetime): The column with the date
        locale (str, optional): Locale to use, defualts to no_NO.
        nynorsk (bool, optional): Use nynorsk instead of bokmål
        if locale set to no_NO. Defaults to False.

    Returns:
        dataframe: the dataframe with the week day name added
    """

    _df["week_day_name"] = _df[date_column].dt.day_name(locale=locale).fillna("")

    if locale == "no_NO" and nynorsk:
        nynorsk_week_days = {
            "Mandag": "Måndag",
            "Tirsdag": "Tysdag",
            "Lørdag": "Laurdag",
            "Søndag": "Sundag",
        }
        _df = _df.replace({"week_day_name": nynorsk_week_days})

    return _df
