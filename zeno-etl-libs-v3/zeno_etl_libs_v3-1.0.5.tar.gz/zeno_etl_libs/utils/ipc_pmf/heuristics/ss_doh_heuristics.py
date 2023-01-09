"""
Capping on SS-DOH, Logic:
* Min SS-DOH = 5 days
* Max SS-DOH = 14 days
"""
import pandas as pd
import numpy as np


def ss_doh_min_cap(safety_stock_df, cap_doh=5):
    safety_stock_df['safety_stock_min'] = np.round(
        (safety_stock_df['fcst'] / 28) * cap_doh)

    safety_stock_df['safety_stock'] = np.where(
        safety_stock_df['safety_stock'] < safety_stock_df['safety_stock_min'],
        safety_stock_df['safety_stock_min'], safety_stock_df['safety_stock'])

    return safety_stock_df


def ss_doh_max_cap(safety_stock_df, cap_doh=14):
    safety_stock_df['safety_stock_max'] = np.round(
        (safety_stock_df['fcst'] / 28) * cap_doh)

    safety_stock_df['safety_stock'] = np.where(
        safety_stock_df['safety_stock'] > safety_stock_df['safety_stock_max'],
        safety_stock_df['safety_stock_max'], safety_stock_df['safety_stock'])

    return safety_stock_df
