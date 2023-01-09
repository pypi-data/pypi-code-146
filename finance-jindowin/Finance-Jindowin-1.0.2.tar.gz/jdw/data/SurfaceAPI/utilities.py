# -*- coding: utf-8 -*-
import pdb
import numpy as np
import pandas as pd


def create_stats(df, horizon, offset, no_code=False):
    df["trade_date"] = pd.to_datetime(df["trade_date"])
    df.set_index("trade_date", inplace=True)
    df["nxt1_ret"] = np.log(1. + df["chgPct"])
    if not no_code:
        # horizon通过累计涨跌幅计算累计收益率，+1表示到第二天
        # offset 表示向前偏移，即offset + 1 对应当期，默认+1表示将第二天涨跌幅对应当期
        df = df.groupby("code").rolling(window=horizon + 1)['nxt1_ret'].sum() \
            .groupby(level=0).shift(-(horizon + offset + 1)).dropna().reset_index()
    else:
        df = df.rolling(window=horizon + 1)['nxt1_ret'].sum().shift(
            -(horizon + offset + 1)).dropna().reset_index()
    return df