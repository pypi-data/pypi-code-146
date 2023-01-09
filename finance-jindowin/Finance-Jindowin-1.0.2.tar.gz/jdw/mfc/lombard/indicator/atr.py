# -*- encoding:utf-8 -*-
import numpy as np
import pandas as pd
from jdw.mfc.lombard.indicator.base import pd_ewm_mean


def _calc_atr_from_pd(high, low, close, time_period=14):
    """
    通过atr公式手动计算atr
    :param high: 最高价格序列，pd.Series或者np.array
    :param low: 最低价格序列，pd.Series或者np.array
    :param close: 收盘价格序列，pd.Series或者np.array
    :param time_period: atr的N值默认值14，int
    :return: atr值序列，np.array对象
    """
    if isinstance(close, pd.Series):
        # shift(1)构成昨天收盘价格序列
        pre_close = close.shift(1).values
    else:
        from scipy.ndimage.interpolation import shift
        # 也可以暂时转换为pd.Series进行shift
        pre_close = shift(close, 1)
    pre_close[0] = pre_close[1]

    if isinstance(high, pd.Series):
        high = high.values
    if isinstance(low, pd.Series):
        low = low.values

    # ∣最高价 - 最低价∣
    tr_hl = np.abs(high - low)
    # ∣最高价 - 昨收∣
    tr_hc = np.abs(high - pre_close)
    # ∣昨收 - 最低价∣
    tr_cl = np.abs(pre_close - low)
    # TR =∣最高价 - 最低价∣，∣最高价 - 昨收∣，∣昨收 - 最低价∣中的最大值
    tr = np.maximum(np.maximum(tr_hl, tr_hc), tr_cl)
    # （ATR）= MA(TR, N)（TR的N日简单移动平均）, 这里没有完全按照标准公式使用简单移动平均，使用了pd_ewm_mean，即加权移动平均
    atr = pd_ewm_mean(pd.Series(tr), span=time_period, min_periods=1)
    # 返回atr值序列，np.array对象
    return atr.values


calc_atr = _calc_atr_from_pd


def atr14(high, low, close):
    """
    通过high, low, close计算atr14序列值
    :param high: 最高价格序列，pd.Series或者np.array
    :param low: 最低价格序列，pd.Series或者np.array
    :param close: 收盘价格序列，pd.Series或者np.array
    :return: atr值序列，np.array对象
    """
    atr = calc_atr(high, low, close, 14)
    return atr


def atr21(high, low, close):
    """
    通过high, low, close计算atr21序列值
    :param high: 最高价格序列，pd.Series或者np.array
    :param low: 最低价格序列，pd.Series或者np.array
    :param close: 收盘价格序列，pd.Series或者np.array
    :return: atr值序列，np.array对象
    """
    atr = calc_atr(high, low, close, 21)
    return atr