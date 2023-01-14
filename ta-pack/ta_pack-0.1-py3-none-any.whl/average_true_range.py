import numpy as np
import pandas as pd


def average_true_range(data,n=14,hlc_index=[1,2,3], keep_na=True):
    """Pass input OHLC data. It is a volatility indicator, take price data of high,low and close to calculate the average range
    for the asset prices """

    df = data.copy()
    high_col_name = df.columns[hlc_index[0]]
    low_col_name = df.columns[hlc_index[1]]
    close_col_name = df.columns[hlc_index[2]]

    df['H-L'] = df[high_col_name] - df[low_col_name]
    df['H-PC'] = abs(df[high_col_name] - df[close_col_name].shift(1))
    df['L-PC'] = abs(df[low_col_name] - df[close_col_name].shift(1))
    df['TR'] = df[['H-L','H-PC','L-PC']].max(axis=1, skipna=False)
    col_name_atr = 'ATR_' +str(n)
    df[col_name_atr] = df['TR'].ewm(com=n, min_periods=n).mean()

    data[col_name_atr] = df[col_name_atr]
    if not keep_na:
        data.dropna(inplace=True)
    
    return data
