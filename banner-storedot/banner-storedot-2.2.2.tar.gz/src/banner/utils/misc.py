from collections.abc import Iterable
from re import split
from typing import Union
from numbers import Number
from hashlib import md5
from pandas import DataFrame

def is_non_string_iterable(value):
    return isinstance(value, Iterable) and not isinstance(value, str)

def to_sql_range(values:Union[Number, Iterable], column: str, table:str = '', op='IN'):
    if not isinstance(values, Iterable):
        values = [values]
    
    __left_bracket, __join_by, __right_bracket = ('"', '|', '"') if op.lower() == 'regexp' else ('(', ', ', ')')

    __values = __join_by.join([str(value) for value in values])

    _column = f'{table}.{column}' if table else column

    return f'{_column} {op} {__left_bracket}{__values}{__right_bracket}'

def digested_key(func: callable, *args, **kwargs):
    key = f'{func.__name__}-{"_".join(str(arg) for arg in args).strip()}'

    if kwargs:
        _kwargs = "_".join(
            [f'{key}:{str(value).strip()}' for key, value in kwargs.items() if type(value) not in (DataFrame, )]
        )
        key += f'-{_kwargs}'

    if len(key) > 300:
        key = md5(key.encode('utf-8')).hexdigest()
    
    return key

def key_value_to_string(key, val, sep='='):
    return f'{str(key)}{sep}{repr(val)}'

def to_list(items: str, delimiter=','):
    delimiter = f' {delimiter} |{delimiter} | {delimiter}|{delimiter}'

    return list(
        map(
            str.strip,
            filter(
                None, 
                split(
                    ' , |, | ,|,',
                    items
                )
            )
        )
    )

def query_df_by_dict(df: DataFrame, query: dict):
    _query = ' & '.join([f'{key}=={value}' for key, value in query.items()])

    return df.query(_query)
