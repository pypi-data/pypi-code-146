from typing import Union

import pandas as pd


def is_number(s: Union[float, int, str, bool]) -> bool:
    """Utility function to check if a string is a number
    Args:
        s (unknown): the variable to check

    Returns:
        bool: True if the variable is a number, False otherwise
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def format_number(x: Union[float, int]) -> str:
    """
    Utility function to format a number to a string with
    thousands separators and decimals according
    to Bergens Tidende's format.

    Args:
        x (number): the number to format

    Returns:
        str: the formatted number as a string
    """
    num_str = str(x)
    decimal_mark_in = "."
    decimal_mark_out = ","
    thousands_delimiter = "."

    sign = ""
    fraction = ""

    # If num_str is signed, store the sign and remove it.
    if num_str[0] == "+" or num_str[0] == "-":
        sign = num_str[0]
        num_str = num_str[1:]

    # If num_str has a decimal mark, store the fraction and remove it.
    # Note that find() will return -1 if the substring is not found.
    dec_mark_pos = num_str.find(decimal_mark_in)
    if dec_mark_pos >= 0:
        fraction = decimal_mark_out + num_str[dec_mark_pos + 1 :]
        num_str = num_str[:dec_mark_pos]

    if is_number(num_str) and len(num_str) >= 5:
        # Work backwards through num_str inserting a separator after every 3rd digit.
        i = len(num_str) - 3
        while i > 0:
            num_str = num_str[:i] + thousands_delimiter + num_str[i:]
            i -= 3

    # Build and return the final string.
    return sign + num_str + fraction


def format_number_column(  # type: ignore[no-any-unimported]
    _df: pd.DataFrame, column_name: str
) -> pd.DataFrame:
    """
      Utility function to format a column of numbers to a string with
      thousands separators and decimals according to Bergens Tidende's format.

      The formatted colmun will be addeed with at _fmt suffix.

    Args:
        _df (_type_): the dataframe to format
        column_name (_type_): the name of the column to format
    Returns:
      dataframe: the dataframe with the formatted column
    """
    _df[f"{column_name}__fmt"] = _df[column_name].apply(lambda x: format_number(x))
    return _df
