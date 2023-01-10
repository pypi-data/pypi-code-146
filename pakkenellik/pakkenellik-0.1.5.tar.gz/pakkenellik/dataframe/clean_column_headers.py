import string
import unicodedata
from typing import List

import pandas as pd

valid_filename_chars = "_ %s%s" % (string.ascii_letters, string.digits)
char_limit = 255


def clean_column_header(column_header: str, whitelist: str, replace: List[str]) -> str:
    """Clean a single string for annoying characters

    Args:
        column_header (str): the string to clean
        whitelist (str): valid characters to use in the header, defaults to underscore,
        ascii letters and digits
        replace (List[str]): What other characters should be replaced?

    Returns:
        str : cleaned string
    """
    # lower case and trim
    column_header = column_header.strip().lower()
    column_header = (
        column_header.replace("æ", "ae").replace("ø", "o").replace("å", "aa")
    )

    # replace spaces
    for r in replace:
        column_header = column_header.replace(r, "_")

    # keep only valid ascii chars
    cleaned_column_header = (
        unicodedata.normalize("NFKD", column_header).encode("ASCII", "ignore").decode()
    )

    # keep only whitelisted chars
    cleaned_column_header = "".join(c for c in cleaned_column_header if c in whitelist)
    return cleaned_column_header[:char_limit]


def clean_column_headers(  # type: ignore[no-any-unimported]
    _df: pd.DataFrame,
    whitelist: str = valid_filename_chars,
    replace: List[str] = [" ", "-"],
) -> pd.DataFrame:
    """Makes column headers usable in pandas

    Args:
        _df (Dataframe): The Dataframe with the columns you wish to fix
        whitelist (str, optional): valid characters to use in the header, defaults
                                   to underscore, ascii letters and digits
        replace (array, optional): What other characters should be replaced?
                                   Defaults to [" ", "-"].

    Returns:
        Dataframe: A dataframe with cleaned column headers
    """
    _df.columns = [clean_column_header(c, whitelist, replace) for c in _df.columns]
    return _df
