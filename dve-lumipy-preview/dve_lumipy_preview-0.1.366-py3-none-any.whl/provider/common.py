import numpy as np
import pandas as pd
from pandas import CategoricalDtype, Series
from termcolor import colored

from lumipy.common.string_utils import indent_str
from lumipy.typing.sql_value_type import SqlValType


def cyan_print(s):
    print(colored(s, color='cyan'))


def red_print(s):
    print(colored(s, color='red'))


def infer_datatype(col: Series) -> SqlValType:
    """Map the type of pandas Series to its corresponding SQL column type.

    Args:
        col (Series): the input series to infer the type of.

    Returns:
        SqlValType: the SQL column type.
    """
    pd_dtype = col.dtype

    if pd_dtype == int:
        return SqlValType.Int
    elif pd_dtype == float:
        return SqlValType.Double
    elif pd_dtype == bool:
        return SqlValType.Boolean
    elif isinstance(pd_dtype, CategoricalDtype):
        return SqlValType.Text
    elif isinstance(pd_dtype, pd.core.dtypes.dtypes.DatetimeTZDtype):
        return SqlValType.DateTime
    elif np.issubdtype(pd_dtype, np.datetime64):
        raise ValueError(
            f"The pandas DataFrame column '{col.name}' used to build the provider was not tz-aware. "
            f"Datetime values in pandas providers must be tz-aware.\n"
            "  Consider using the following (e.g. for the UTC timezone)\n"
            "    df['column'] = df['column'].dt.tz_localize(tz='utc')\n"
            "  to convert an existing DataFrame datetime column."
        )
    else:
        return SqlValType.Text


def df_summary_str(d):
    mem_use = pd.DataFrame.memory_usage(d, deep=True)
    max_col_len = max(len(k) for k in mem_use.keys())
    divider = '―' * (max_col_len + 11)

    def format_size(x):

        units = [['TB😱', 1e12], ['GB', 1e9], ['MB', 1e6], ['KB', 1e3], ['B ', 1e0]]

        for upper, lower in zip(units[:-1], units[1:]):
            if upper[1] > x >= lower[1]:
                vstr = f'{x / lower[1]:6.1f}'
                return f'{vstr:6} {lower[0]}'

    strs = [divider]
    for k, v in mem_use.items():
        strs.append(f'{k:{max_col_len}}  {format_size(v)}')

    strs.append(divider)
    strs.append(f'{"Total":{max_col_len}}  {format_size(mem_use.sum())}')
    strs.append(divider)

    table_str = '\n'.join(map(lambda x: f'│ {x} │', strs))

    return '\n'.join([
        '\n',
        'DataFrame Stats',
        f'    Number of rows: {d.shape[0]}',
        f'    Number of cols: {d.shape[1]}',
        '    Memory Usage:',
        f'{indent_str(table_str, 6)}',
        '',
    ])


def clean_colname(c_str):
    return str(c_str).replace('.', '_').replace("'", "").strip().strip('_')