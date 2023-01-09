"""
Features for distributor ranking 2.0
1. Margin
2. Weighted Fulfillment
"""

from functools import reduce

import numpy as np
import pandas as pd
import datetime as dt


def calculate_features(df_features, reset_date, time_interval, logger, group_cols):
    """
    DC-LEVEL: group_cols=['partial_dc_id','partial_distributor_id', 'drug_id']
    FRANCHISEE-LEVEL: group_cols=['store_id','partial_distributor_id', 'drug_id']
    """

    dfx = df_features[df_features['invoice_count'] != 0]

    # ========================== MARGIN CALCULATION ==========================

    # (follows same logic as in distributor ranking 1.0)
    logger.info("Calculating margin")
    df_margin = dfx.copy()

    df_margin['margin'] = (df_margin['mrp'] -
                           df_margin['distributor_rate']) / df_margin[
                              'mrp']

    df_margin = df_margin.groupby(group_cols).agg(
        margin=('margin', 'mean')).reset_index()

    # sanity check
    assert df_margin.shape[0] == dfx[group_cols].drop_duplicates().shape[0]

    # ====================== WTD.FULFILLMENT CALCULATION ======================

    logger.info("Calculating wtd.ff")
    # get length of 3 period split
    period_length = round(time_interval / 3)

    # p1 : t-1 (latest period)
    # p2 : t-2 period
    # p3 : t-3 period

    p1_end = pd.Timestamp(reset_date - dt.timedelta(6))
    p1_start = p1_end - dt.timedelta(period_length)
    p2_end = p1_start
    p2_start = p2_end - dt.timedelta(period_length)
    p3_end = p2_start
    p3_start = p3_end - dt.timedelta(period_length + 1)

    df_ff_1 = ff_calc(dfx, group_cols, p_start=p1_start, p_end=p1_end, period_flag="p1")
    df_ff_2 = ff_calc(dfx, group_cols, p_start=p2_start, p_end=p2_end, period_flag="p2")
    df_ff_3 = ff_calc(dfx, group_cols, p_start=p3_start, p_end=p3_end, period_flag="p3")

    df_ff_comb = pd.concat([df_ff_1, df_ff_2, df_ff_3], axis=0)

    # count cases where all 3 or 2 or 1 periods data present
    df_ff_period_cnt = df_ff_comb.groupby(group_cols, as_index=False).agg(
        {"period_flag": "count"})
    df_ff_period_cnt.rename({"period_flag": "period_count"}, axis=1,
                            inplace=True)

    # Cases with 3 periods present
    # weighted by 0.5, 0.3, 0.2 for p1, p2, p3 respectively
    df_3p = df_ff_period_cnt.loc[df_ff_period_cnt["period_count"] == 3][
        group_cols]
    df_ff_comb_3p = df_ff_comb.merge(df_3p, on=group_cols, how="inner")
    df_ff_comb_3p['period'] = np.tile(np.arange(1, 4), len(df_ff_comb_3p))[
                              :len(df_ff_comb_3p)]

    df_ff_comb_3p['weights'] = np.where(df_ff_comb_3p['period'] == 1, 0.5, 0)
    df_ff_comb_3p['weights'] = np.where(df_ff_comb_3p['period'] == 2, 0.3,
                                        df_ff_comb_3p['weights'])
    df_ff_comb_3p['weights'] = np.where(df_ff_comb_3p['period'] == 3, 0.2,
                                        df_ff_comb_3p['weights'])

    df_ff_comb_3p["wtd_ff"] = df_ff_comb_3p["ff"] * df_ff_comb_3p["weights"]

    df_ff_comb_3p = df_ff_comb_3p.groupby(group_cols, as_index=False).agg(
        {"wtd_ff": "sum"})

    # Cases with 2 periods present
    # weighted by 0.6, 0.4 for latest, early respectively
    df_2p = df_ff_period_cnt.loc[df_ff_period_cnt["period_count"] == 2][
        group_cols]
    df_ff_comb_2p = df_ff_comb.merge(df_2p, on=group_cols, how="inner")
    df_ff_comb_2p['period'] = np.tile(np.arange(1, 3), len(df_ff_comb_2p))[
                              :len(df_ff_comb_2p)]

    df_ff_comb_2p['weights'] = np.where(df_ff_comb_2p['period'] == 1, 0.6, 0)
    df_ff_comb_2p['weights'] = np.where(df_ff_comb_2p['period'] == 2, 0.4,
                                        df_ff_comb_2p['weights'])

    df_ff_comb_2p["wtd_ff"] = df_ff_comb_2p["ff"] * df_ff_comb_2p["weights"]

    df_ff_comb_2p = df_ff_comb_2p.groupby(group_cols, as_index=False).agg(
        {"wtd_ff": "sum"})

    # Cases with 1 period present
    # weighted by 1 for whatever period present
    df_1p = df_ff_period_cnt.loc[df_ff_period_cnt["period_count"] == 1][
        group_cols]
    df_ff_comb_1p = df_ff_comb.merge(df_1p, on=group_cols, how="inner")

    df_ff_comb_1p = df_ff_comb_1p[group_cols + ["ff"]]
    df_ff_comb_1p.rename({"ff": "wtd_ff"}, axis=1, inplace=True)

    # combine all
    df_ff_comb = pd.concat([df_ff_comb_3p, df_ff_comb_2p, df_ff_comb_1p],
                           axis=0)

    # ======================== DIST VOLUME CALCULATION ========================

    if group_cols[0] == "partial_dc_id":
        base_lvl = 'dc'
    else:
        base_lvl = 'store'

    logger.info(f"Calculating {base_lvl}-distributor volume")
    df_vol = df_features.groupby(group_cols).agg(
        total_lost=('is_lost', 'sum'),
        total_requests=('is_lost', 'count')).reset_index()
    df_vol["ff_requests"] = df_vol["total_requests"] - df_vol["total_lost"]
    df_vol["ff_requests"] = np.where(df_vol["ff_requests"] < 0, 0,
                                     df_vol["ff_requests"])

    df_vol.drop(["total_lost", "total_requests"], axis=1, inplace=True)

    if base_lvl == 'dc':
        # calculate request volume dc
        request_volume_dc = df_vol.groupby("partial_dc_id", as_index=False).agg(
            total_requests_dc=("ff_requests", "sum"))
        request_volume_dc_dist = df_vol.groupby(
            ["partial_dc_id", "partial_distributor_id"], as_index=False).agg(
            total_requests_dc_dist=("ff_requests", "sum"))

        df_vol = df_vol.merge(request_volume_dc_dist,
                              on=["partial_dc_id", "partial_distributor_id"],
                              how="left")
        df_vol = df_vol.merge(request_volume_dc, on="partial_dc_id", how="left")

        df_vol["request_volume_dc_dist"] = df_vol["total_requests_dc_dist"] / \
                                           df_vol["total_requests_dc"]

        df_vol.drop(["total_requests_dc_dist", "total_requests_dc"], axis=1,
                    inplace=True)

    else:
        # calculate request volume store (franchisee)
        request_volume_store = df_vol.groupby("store_id", as_index=False).agg(
            total_requests_store=("ff_requests", "sum"))
        request_volume_store_dist = df_vol.groupby(
            ["store_id", "partial_distributor_id"], as_index=False).agg(
            total_requests_store_dist=("ff_requests", "sum"))

        df_vol = df_vol.merge(request_volume_store_dist,
                              on=["store_id", "partial_distributor_id"],
                              how="left")
        df_vol = df_vol.merge(request_volume_store, on="store_id", how="left")

        df_vol["request_volume_store_dist"] = df_vol["total_requests_store_dist"] / \
                                           df_vol["total_requests_store"]

        df_vol.drop(["total_requests_store_dist", "total_requests_store"], axis=1,
                    inplace=True)

    # =========================== COMPILE FEATURES ===========================

    logger.info("Compiling all features")
    meg_list = [df_margin, df_ff_comb, df_vol]

    features = reduce(
        lambda left, right: pd.merge(left, right,
                                     on=group_cols,
                                     how='outer'), meg_list)

    # rounding off to 3 significant digits
    features["margin"] = np.round(features["margin"], 3)
    features["wtd_ff"] = np.round(features["wtd_ff"], 3)
    features[f"request_volume_{base_lvl}_dist"] = np.round(
        features[f"request_volume_{base_lvl}_dist"], 3)

    return features


def ff_calc(dfx, group_cols, p_start=None, p_end=None, period_flag="None"):
    """
    Base FF calculation same as in distributor ranking 1.0
    """
    # split base data by period
    dfx = dfx.loc[
        (dfx["original_created_at"] > p_start) &
        (dfx["original_created_at"] < p_end)]

    df_sorted = dfx.groupby(['short_book_1_id'], as_index=False).apply(
        lambda x: x.sort_values(by=['partial_invoiced_at']))

    # for multiple invoices, calculate cumulative fulfilled quantities
    df_sorted = df_sorted.groupby(['short_book_1_id']).apply(
        lambda x: x['partial_quantity'].cumsum()).reset_index().rename(
        columns={'partial_quantity': 'cum_partial_quantity'})

    df_sorted = df_sorted.set_index('level_1')

    df_fulfillment = pd.merge(df_sorted, dfx, left_index=True,
                              right_index=True, how='left', suffixes=('', '_y'))
    assert df_fulfillment['short_book_1_id'].equals(
        df_fulfillment['short_book_1_id_y'])

    df_fulfillment = df_fulfillment[
        ['short_book_1_id'] + group_cols + ['original_order', 'partial_quantity',
         'cum_partial_quantity']]

    # cum required quantity is quantity left after subtracting cum quantity from all previous invoices.
    df_fulfillment['cum_required_quantity'] = df_fulfillment['original_order'] - \
        df_fulfillment['cum_partial_quantity']

    # the real required quantity while placing an order is quantity
    # unfulfilled by the previours invoice. Hence shifted by 1
    df_fulfillment['actual_required'] = df_fulfillment.groupby(
        ['short_book_1_id']).shift(1)['cum_required_quantity']

    # fill single invoices with the original order
    df_fulfillment['actual_required'] = df_fulfillment['actual_required'].fillna(
        df_fulfillment['original_order'])

    # put actual required = 0 when ordered exceeds required.
    df_fulfillment.loc[df_fulfillment['actual_required']
                       < 0, 'actual_required'] = 0

    df_fulfillment['redundant_order_flag'] = np.where(
        df_fulfillment['actual_required'] == 0, 1, 0)

    df_fulfillment = df_fulfillment[['short_book_1_id'] + group_cols +
                                    ['original_order', 'partial_quantity',
                                     'actual_required', 'redundant_order_flag']]

    df_fulfillment['ff'] = df_fulfillment['partial_quantity'] / \
        df_fulfillment['actual_required']

    # for those quantities where nothing was required and still order placed, take them as 0.
    df_fulfillment.loc[(df_fulfillment['actual_required'] == 0) & (
        df_fulfillment['partial_quantity'] > 0), 'ff'] = 1

    df_fulfillment.loc[(df_fulfillment['ff'] > 1), 'ff'] = 1

    # removed redundant orders here.
    df_ff = df_fulfillment[df_fulfillment['redundant_order_flag'] != 1].groupby(
        group_cols).agg(ff=('ff', 'mean')).reset_index()

    # add period_flag
    df_ff["period_flag"] = period_flag

    return df_ff
