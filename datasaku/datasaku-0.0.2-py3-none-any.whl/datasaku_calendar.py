"""
date manipulation module
based on https://pandas.pydata.org/docs/user_guide/timeseries.html#timeseries-offset-aliases #
"""

import pandas as pd

def date_to_seq(start_date_def, end_date_def, sequence_def):
    """date to sequence converter"""
    seq = pd.date_range(start_date_def, end_date_def, freq = sequence_def)
    seq = pd.Series(seq.format()).tolist()
    return seq

def date_is_weekend(df_col_def):
    """weekend flag"""
    is_weekend = df_col_def.dt.dayofweek > 4
    return is_weekend