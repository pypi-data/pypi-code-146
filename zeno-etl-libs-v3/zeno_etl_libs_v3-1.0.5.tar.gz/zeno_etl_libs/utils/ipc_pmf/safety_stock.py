import pandas as pd
import numpy as np

from zeno_etl_libs.utils.ipc_pmf.lead_time import lead_time
from zeno_etl_libs.utils.ipc_pmf.heuristics.sl_heuristics import calculate_ss
from zeno_etl_libs.utils.ipc_pmf.heuristics.ss_doh_heuristics import ss_doh_min_cap, ss_doh_max_cap
from zeno_etl_libs.utils.ipc2.helpers.correction_flag import compare_df, \
    add_correction_flag
from zeno_etl_libs.utils.ipc2.heuristics.ipcv4_heuristics import v4_corrections


def safety_stock_calc(df_fcst_drug, store_id, reset_date,
                      v4_active_flag, drug_type_list_v4,
                      drug_sales_latest_12w, schema, db, logger):
    fcst_weeks = 4
    order_freq = 2

    # ========================= LEAD TIME CALCULATIONS =========================

    lt_drug, lt_store_mean, lt_store_std = lead_time(
        store_id, reset_date, db, schema, logger)

    safety_stock_df = df_fcst_drug.merge(
        lt_drug[['drug_id', 'lead_time_mean', 'lead_time_std']],
        how='left', on='drug_id')
    safety_stock_df['lead_time_mean'].fillna(lt_store_mean, inplace=True)
    safety_stock_df['lead_time_std'].fillna(lt_store_std, inplace=True)

    # ==================== SS, ROP, OUP CALCULATION BEGINS =====================

    # impute store_std for cases where store-drug std<1
    safety_stock_df['lead_time_std'] = np.where(
        safety_stock_df['lead_time_std'] < 1,
        lt_store_std, safety_stock_df['lead_time_std'])

    # calculate SS
    safety_stock_df = calculate_ss(safety_stock_df, fcst_weeks, logger)

    # MIN-SS-DOH CAPPING
    logger.info(f"DOH1 Correction starts")
    df_pre_corr = safety_stock_df.copy()
    safety_stock_df = ss_doh_min_cap(safety_stock_df)
    df_post_corr = safety_stock_df.copy()
    logger.info(f"Sum SS before: {df_pre_corr['safety_stock'].sum()}")
    logger.info(f"Sum SS after: {df_post_corr['safety_stock'].sum()}")

    corr_drug_lst = compare_df(df_pre_corr, df_post_corr, logger,
                               cols_to_compare=['safety_stock'])
    safety_stock_df = add_correction_flag(safety_stock_df, corr_drug_lst,
                                          'DOH1')

    # MAX-SS-DOH CAPPING
    logger.info(f"DOH2 Correction starts")
    df_pre_corr = safety_stock_df.copy()
    safety_stock_df = ss_doh_max_cap(safety_stock_df)
    df_post_corr = safety_stock_df.copy()
    logger.info(f"Sum SS before: {df_pre_corr['safety_stock'].sum()}")
    logger.info(f"Sum SS after: {df_post_corr['safety_stock'].sum()}")

    corr_drug_lst = compare_df(df_pre_corr, df_post_corr, logger,
                               cols_to_compare=['safety_stock'])
    safety_stock_df = add_correction_flag(safety_stock_df, corr_drug_lst,
                                          'DOH2')

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

    # ========== CORRECTION PLUGINS (REWORK SS,ROP,OUP BASED ON REQ) ===========

    final_ss_df = safety_stock_df.copy()

    if v4_active_flag == 'Y':
        logger.info("IPC V4 Correction starts")
        df_pre_corr = final_ss_df.copy()
        final_ss_df = v4_corrections(final_ss_df, drug_type_list_v4, db, schema)
        df_post_corr = final_ss_df.copy()
        logger.info(f"Sum OUP before: {df_pre_corr['order_upto_point'].sum()}")
        logger.info(f"Sum OUP after: {df_post_corr['order_upto_point'].sum()}")

        corr_drug_lst = compare_df(df_pre_corr, df_post_corr, logger)
        final_ss_df = add_correction_flag(final_ss_df, corr_drug_lst, 'V4')

    # correct cases where ROP=OUP
    df_pre_corr = final_ss_df.copy()
    final_ss_df['order_upto_point'] = np.where(
        ((final_ss_df['order_upto_point'] > 0) &
         (final_ss_df['reorder_point'] == final_ss_df['order_upto_point'])),
        final_ss_df['reorder_point'] + 1, final_ss_df['order_upto_point'])
    df_post_corr = final_ss_df.copy()
    corr_drug_lst = compare_df(df_pre_corr, df_post_corr, logger)
    final_ss_df = add_correction_flag(final_ss_df, corr_drug_lst, 'OUP_CORR1')

    # OUP < STD Qty, STD Qty correction
    df_pre_corr = final_ss_df.copy()
    final_ss_df = std_qty_oup(final_ss_df, schema, db)
    df_post_corr = final_ss_df.copy()
    corr_drug_lst = compare_df(df_pre_corr, df_post_corr, logger)
    final_ss_df = add_correction_flag(final_ss_df, corr_drug_lst, 'STD_CORR')

    # Min OUP=2 for recently sold
    df_pre_corr = final_ss_df.copy()
    final_ss_df = min_oup_recency(final_ss_df, drug_sales_latest_12w)
    df_post_corr = final_ss_df.copy()
    corr_drug_lst = compare_df(df_pre_corr, df_post_corr, logger)
    final_ss_df = add_correction_flag(final_ss_df, corr_drug_lst, 'OUP_CORR2')

    return final_ss_df


def std_qty_oup(df, schema, db):
    list_drugs = df['drug_id'].tolist()
    if list_drugs:
        str_drugs = str(list_drugs).replace('[', '(').replace(']', ')')
    else:
        str_drugs = '(0)'
    q_std_qty = f"""
        select "drug-id" , "std-qty"
        from "{schema}"."drug-std-info" dsi
        where "drug-id" in {str_drugs}
        """
    df_std_qty = db.get_df(q_std_qty)
    df_std_qty.columns = [c.replace('-', '_') for c in df_std_qty.columns]

    df = df.merge(df_std_qty, on='drug_id', how='left')
    df['std_qty'] = df['std_qty'].fillna(1)

    df_to_corr = df.loc[df['order_upto_point'] < df['std_qty']]
    df_not_to_corr = df.loc[~(df['order_upto_point'] < df['std_qty'])]

    df_to_corr['order_upto_point'] = df_to_corr['std_qty']
    df_to_corr['reorder_point'] = np.where(df_to_corr['order_upto_point'] > 1, round(df_to_corr['std_qty'] / 2), 0)

    df = df_not_to_corr.append(df_to_corr)
    df.drop('std_qty', axis=1, inplace=True)

    return df


def min_oup_recency(df, drug_sales_latest_12w):
    drug_sales_latest_12w['latest_28d_demand'] = np.round(
        drug_sales_latest_12w['actual_demand'] / 3)
    df = df.merge(drug_sales_latest_12w[['drug_id', 'latest_28d_demand']],
        on='drug_id', how='left')

    df_to_corr = df.loc[(df['order_upto_point'] == 1) & (df['fcst'] > 0) &
                        (df['latest_28d_demand'] > 0)]
    df_not_to_corr = df.loc[~((df['order_upto_point'] == 1) & (df['fcst'] > 0) &
                              (df['latest_28d_demand'] > 0))]

    df_to_corr['order_upto_point'] = 2
    df_to_corr['reorder_point'] = 1

    df = df_not_to_corr.append(df_to_corr)
    df.drop('latest_28d_demand', axis=1, inplace=True)

    return df




