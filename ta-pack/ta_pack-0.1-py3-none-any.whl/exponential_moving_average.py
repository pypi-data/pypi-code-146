import numpy as np
import pandas as pd


def exponential_moving_average(data, close_col_index, EMA_list, keep_na=True):
    """Takes input the OHLCV data, index of closing price and list of moving averages
    returns the dataframe with moving averages columns added """

    df = data.copy()
    ema_names = ['EMA_'+str(i) for i in EMA_list]
    close_col_name = df.columns[close_col_index]

    for i in range(len(EMA_list)):
        df[ema_names[i]] = df[close_col_name].ewm(span=EMA_list[i], min_periods=EMA_list[i]).mean()

    if not keep_na:
        df.dropna(inplace=True)

    return df
