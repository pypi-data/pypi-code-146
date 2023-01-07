"""
utility to reduce memory usage of pandas Series or DataFrame

this module adds a hug() method to both pandas.Series and pandas.DataFrame

it is recommend that you call convert_dtypes() before calling hug()

example -

S = pd.Series([2**8])
A = pd.Series([f'a{i}' for i in range(100)])
M = pd.Series([42])
E = pd.Series(['a', 'b', 'c'] * 15)
df = pd.DataFrame({'S': S, 'A': A, 'M': M, 'E': E})

df.info()

   <class 'pandas.core.frame.DataFrame'>
   RangeIndex: 100 entries, 0 to 99
   Data columns (total 4 columns):
    #   Column  Non-Null Count  Dtype
   ---  ------  --------------  -----
    0   S       1 non-null      float64
    1   A       100 non-null    object
    2   M       1 non-null      float64
    3   E       45 non-null     object
   dtypes: float64(2), object(2)
   memory usage: 3.2+ KB

df.convert_dtypes().hug().info()

   <class 'pandas.core.frame.DataFrame'>
   RangeIndex: 100 entries, 0 to 99
   Data columns (total 4 columns):
    #   Column  Non-Null Count  Dtype
   ---  ------  --------------  -----
    0   S       1 non-null      UInt16
    1   A       100 non-null    string
    2   M       1 non-null      UInt8
    3   E       45 non-null     category
   dtypes: UInt16(1), UInt8(1), category(1), string(1)
   memory usage: 1.6 KB
"""

import pandas as pd

from .core import (
    embrace_integer,
    embrace_string,
    embrace_series,
    embrace_dataframe,
    hug_dataframe,
    hug_series,
    golden_snub,
)

__version__ = "0.14.0"


__all__ = []


golden_snub()
