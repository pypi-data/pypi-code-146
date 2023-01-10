import io
from distutils.util import strtobool
from typing import Callable

import numpy as np
import pandas as pd
from lumipy.typing.sql_value_type import SqlValType
from pandas import DataFrame


def col_type_map(t: SqlValType) -> Callable:
    if t == SqlValType.Text:
        return lambda c: c.astype(pd.StringDtype())
    if t == SqlValType.Int or t == SqlValType.BigInt:
        return lambda c: c.astype(pd.Int64Dtype())
    if t == SqlValType.Double:
        return lambda c: c.astype(np.float64)
    if t == SqlValType.Boolean:
        return lambda c: c.astype(pd.BooleanDtype())
    if t == SqlValType.Decimal:
        return lambda c: c.astype(np.float64)
    if t == SqlValType.Date or t == SqlValType.DateTime:
        return lambda c: pd.to_datetime(c, errors='coerce')

    raise TypeError(f'Unrecognised data type in column conversion: {t.name}')


def scalar_type_map(t: SqlValType) -> Callable:
    if t == SqlValType.Int:
        return int
    if t == SqlValType.Double:
        return float
    if t == SqlValType.Text:
        return str
    if t == SqlValType.Boolean:
        return lambda v: bool(strtobool(str(v)))
    if t == SqlValType.Table:
        return lambda c: table_spec_to_df(c['metadata'], c['data'])
    if t == SqlValType.DateTime or t == SqlValType.Date:
        return lambda c: pd.to_datetime(c, errors='coerce')

    TypeError(f"Unsupported data type in scalar conversion: {t.name}.")


def table_spec_to_df(metadata, data, **read_csv_params) -> DataFrame:
    """Convert the table dictionary in a restriction table filter to a pandas DataFrame

    Args:
        metadata (List[Dict[str, str]]): a list of dictionaries containing column metadata.
        data (str): the CSV of the table to parse into a dataframe.

    Returns:
        DataFrame: the CSV data parsed as a dataframe

    """

    read_csv_params['encoding'] = 'utf-8'
    read_csv_params['skip_blank_lines'] = False
    read_csv_params['filepath_or_buffer'] = io.StringIO(data)

    df = pd.read_csv(**read_csv_params)

    for col in metadata:
        name, dtype = col['name'], SqlValType[col['type']]
        df[name] = col_type_map(dtype)(df[name])

    return df
