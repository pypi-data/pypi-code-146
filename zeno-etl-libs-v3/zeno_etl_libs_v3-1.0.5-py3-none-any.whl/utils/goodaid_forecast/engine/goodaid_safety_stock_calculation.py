"""
service level - 98%
safety stock = z-score * sqrt(std_lead_time^2 * avg_demand^2 +
                              avg_lead_time^2 * std_demand^2)
re-order point = safety stock + avg_lead_time_demand
"""

import numpy as np

from zeno_etl_libs.utils.ipc.lead_time import lead_time
from zeno_etl_libs.utils.ipc2.helpers.correction_flag import compare_df, \
    add_correction_flag
from zeno_etl_libs.utils.goodaid_forecast.engine.goodaid_calculate_ss import calculate_ss
from zeno_etl_libs.utils.goodaid_forecast.engine.config_goodaid import *


def safety_stock_calc(agg_fcst, cal_sales, store_id, reset_date,
                       schema, db, logger):
    fcst_weeks = 4
    order_freq = 4

    # ========================= LEAD TIME CALCULATIONS =========================

    lt_drug, lt_store_mean, lt_store_std = lead_time(
        store_id, cal_sales, reset_date, db, schema, logger)

    safety_stock_df = agg_fcst.merge(
        lt_drug[['drug_id', 'lead_time_mean', 'lead_time_std']],
        how='left', on='drug_id')
    safety_stock_df['lead_time_mean'].fillna(lt_store_mean, inplace=True)
    safety_stock_df['lead_time_mean'] = safety_stock_df['lead_time_mean'].apply(np.ceil)
    safety_stock_df['lead_time_std'].fillna(lt_store_std, inplace=True)

    # ==================== SS, ROP, OUP CALCULATION BEGINS =====================

    # impute store_std for cases where store-drug std<1
    safety_stock_df['lead_time_std'] = np.where(
        safety_stock_df['lead_time_std'] < 1,
        lt_store_std, safety_stock_df['lead_time_std'])

    # calculate SS
    safety_stock_df = calculate_ss(safety_stock_df, fcst_weeks, logger)

    safety_stock_df['safety_stock_without_correction'] = safety_stock_df['safety_stock']

    safety_stock_df_before = safety_stock_df
    # SS-DOH CAPPING #1
    logger.info(f"DOH1 (Upper Capping) Correction starts")
    df_pre_corr = safety_stock_df.copy()
    cap_doh = ss_upper_cap
    safety_stock_df['safety_stock_max'] = np.round((safety_stock_df['fcst'] / 28) * cap_doh)
    safety_stock_df['safety_stock'] = np.where(
        safety_stock_df['safety_stock'] > safety_stock_df['safety_stock_max'],
        safety_stock_df['safety_stock_max'], safety_stock_df['safety_stock'])
    safety_stock_df.drop('safety_stock_max', axis=1, inplace=True)
    df_post_corr = safety_stock_df.copy()
    logger.info(f"Sum SS before: {df_pre_corr['safety_stock'].sum()}")
    logger.info(f"Sum SS after: {df_post_corr['safety_stock'].sum()}")

    corr_drug_lst = compare_df(df_pre_corr, df_post_corr, logger,
                               cols_to_compare=['safety_stock'])
    safety_stock_df = add_correction_flag(safety_stock_df, corr_drug_lst, 'UDOH')

    # SS-DOH CAPPING #2
    logger.info(f"DOH2 (lower capping) Correction starts")
    df_pre_corr = safety_stock_df.copy()
    cap_doh = ss_lower_cap
    safety_stock_df['safety_stock_min'] = np.round((safety_stock_df['fcst'] / 28) * cap_doh)
    safety_stock_df['safety_stock'] = np.where(
        safety_stock_df['safety_stock'] < safety_stock_df['safety_stock_min'],
        safety_stock_df['safety_stock_min'], safety_stock_df['safety_stock'])
    safety_stock_df.drop('safety_stock_min', axis=1, inplace=True)
    df_post_corr = safety_stock_df.copy()
    logger.info(f"Sum SS before: {df_pre_corr['safety_stock'].sum()}")
    logger.info(f"Sum SS after: {df_post_corr['safety_stock'].sum()}")

    corr_drug_lst = compare_df(df_pre_corr, df_post_corr, logger,
                               cols_to_compare=['safety_stock'])
    safety_stock_df = add_correction_flag(safety_stock_df, corr_drug_lst, 'LDOH')

    # SS-DOH CAPPING #2
    logger.info(f"If WH assortment active then No drug should have 0 SS, entering harcoded value")
    df_pre_corr = safety_stock_df.copy()
    safety_stock_df['safety_stock'] = np.where(
        ((safety_stock_df['safety_stock'] < ss_harcoded)&(safety_stock_df['wh_assortment']=='Yes')),
        ss_harcoded, safety_stock_df['safety_stock'])
    df_post_corr = safety_stock_df.copy()
    logger.info(f"Sum SS before: {df_pre_corr['safety_stock'].sum()}")
    logger.info(f"Sum SS after: {df_post_corr['safety_stock'].sum()}")

    corr_drug_lst = compare_df(df_pre_corr, df_post_corr, logger,
                               cols_to_compare=['safety_stock'])
    safety_stock_df = add_correction_flag(safety_stock_df, corr_drug_lst, 'HDOH')

    # calculate ROP - add lead time demand to SS
    safety_stock_df['reorder_point'] = safety_stock_df.apply(
        lambda row: np.round(
            row['lead_time_mean'] * row['fcst'] / fcst_weeks / 7),
        axis=1) + safety_stock_df['safety_stock']

    # calculate OUP - add order_freq demand to ROP
    safety_stock_df['order_upto_point'] = (
            safety_stock_df['reorder_point'] +
            np.round(
                np.where(
                    # if rounding off give 0, increase it to 4-week forecast
                    (safety_stock_df['reorder_point'] +
                     safety_stock_df[
                         'fcst'] * order_freq / fcst_weeks / 7 < 0.5) &
                    (safety_stock_df['fcst'] > 0),
                    safety_stock_df['fcst'],
                    safety_stock_df['fcst'] * order_freq / fcst_weeks / 7))
            )

    # correction for negative forecast
    safety_stock_df['safety_stock'] = np.where(
        safety_stock_df['safety_stock'] < 0,
        0, safety_stock_df['safety_stock'])
    safety_stock_df['reorder_point'] = np.where(
        safety_stock_df['reorder_point'] < 0,
        0, safety_stock_df['reorder_point'])
    safety_stock_df['order_upto_point'] = np.where(
        safety_stock_df['order_upto_point'] < 0,
        0, safety_stock_df['order_upto_point'])

    # correction for OUP atleast 1 greater than ROP
    condition = [safety_stock_df['order_upto_point']==0,safety_stock_df['order_upto_point']>safety_stock_df['reorder_point'],safety_stock_df['order_upto_point']<=safety_stock_df['reorder_point']]
    choice = [safety_stock_df['order_upto_point'],safety_stock_df['order_upto_point'],safety_stock_df['order_upto_point']+1]
    safety_stock_df['order_upto_point'] = np.select(condition,choice)

    return safety_stock_df