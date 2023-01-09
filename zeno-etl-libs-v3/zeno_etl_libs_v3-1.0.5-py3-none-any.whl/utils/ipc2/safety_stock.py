"""
service level - 95%
safety stock = z-score * sqrt(std_lead_time^2 * avg_demand^2 +
                              avg_lead_time^2 * std_demand^2)
re-order point = safety stock + avg_lead_time_demand
"""

import numpy as np

from zeno_etl_libs.utils.ipc.lead_time import lead_time
from zeno_etl_libs.utils.ipc2.helpers.correction_flag import compare_df, \
    add_correction_flag
from zeno_etl_libs.utils.ipc2.heuristics.sl_heuristics import calculate_ss
from zeno_etl_libs.utils.ipc2.heuristics.doh_heuristics import ss_doh_wh_cap, \
    ss_doh_non_wh_cap
from zeno_etl_libs.utils.ipc2.heuristics.ipcv3_heuristics import v3_corrections
from zeno_etl_libs.utils.ipc2.heuristics.ipcv4_heuristics import v4_corrections
from zeno_etl_libs.utils.ipc2.heuristics.ipcv5_heuristics import v5_corrections
from zeno_etl_libs.utils.ipc2.heuristics.ipcv3N_heuristics import v3N_corrections


def safety_stock_calc(agg_fcst, cal_sales, store_id, reset_date, v3_active_flag,
                      corrections_selling_probability_cutoff,
                      corrections_cumulative_probability_cutoff,
                      v4_active_flag, drug_type_list_v4, v5_active_flag,
                      open_po_turbhe_active, schema, db, logger):
    fcst_weeks = 4
    order_freq = 4
    review_period = 2

    # ================== TEMPORARY FOR OPEN-PO TURBHE STORES ===================

    if open_po_turbhe_active == 'Y':
        q_turbhe_stores = f"""
                select distinct "store-id" 
                from "{schema}"."store-dc-mapping" sdm 
                left join "{schema}".stores s on s.id =sdm."store-id" 
                where "forward-dc-id" = 169
                and s."franchisee-id" = 1 
                and name <> 'Zippin Central'
                and "is-active" = 1
                and "opened-at" != '0101-01-01 00:00:00'
                """
        df_turbhe_stores = db.get_df(q_turbhe_stores)
        turbhe_stores = df_turbhe_stores["store-id"].tolist()

        # add store_id 2 & 264 (mulund east and mulund west sarvodaya)
        turbhe_stores += [2, 264]

        if store_id in turbhe_stores:
            order_freq = 3

    # ========================= LEAD TIME CALCULATIONS =========================

    lt_drug, lt_store_mean, lt_store_std = lead_time(
        store_id, cal_sales, reset_date, db, schema, logger)

    safety_stock_df = agg_fcst.merge(
        lt_drug[['drug_id', 'lead_time_mean', 'lead_time_std']],
        how='left', on='drug_id')
    safety_stock_df['lead_time_mean'].fillna(lt_store_mean, inplace=True)
    safety_stock_df['lead_time_std'].fillna(lt_store_std, inplace=True)

    # ==================== SS, ROP, OUP CALCULATION BEGINS =====================

    # impute store_std for cases where store-drug std<1
    # safety_stock_df['lead_time_std'] = np.where(
    #     safety_stock_df['lead_time_std'] < 1,
    #     lt_store_std, safety_stock_df['lead_time_std'])

    # calculate SS
    safety_stock_df = calculate_ss(safety_stock_df, fcst_weeks, logger)

    # # SS-DOH CAPPING #1
    # logger.info(f"DOH1 (SS-WH-DOH) Correction starts")
    # df_pre_corr = safety_stock_df.copy()
    # safety_stock_df = ss_doh_wh_cap(safety_stock_df, schema, db)
    # df_post_corr = safety_stock_df.copy()
    # logger.info(f"Sum SS before: {df_pre_corr['safety_stock'].sum()}")
    # logger.info(f"Sum SS after: {df_post_corr['safety_stock'].sum()}")
    #
    # corr_drug_lst = compare_df(df_pre_corr, df_post_corr, logger,
    #                            cols_to_compare=['safety_stock'])
    # safety_stock_df = add_correction_flag(safety_stock_df, corr_drug_lst, 'DOH1')
    #
    # # SS-DOH CAPPING #2
    # logger.info(f"DOH2 (SS-Non-WH-DOH) Correction starts")
    # df_pre_corr = safety_stock_df.copy()
    # safety_stock_df = ss_doh_non_wh_cap(safety_stock_df, schema, db)
    # df_post_corr = safety_stock_df.copy()
    # logger.info(f"Sum SS before: {df_pre_corr['safety_stock'].sum()}")
    # logger.info(f"Sum SS after: {df_post_corr['safety_stock'].sum()}")
    #
    # corr_drug_lst = compare_df(df_pre_corr, df_post_corr, logger,
    #                            cols_to_compare=['safety_stock'])
    # safety_stock_df = add_correction_flag(safety_stock_df, corr_drug_lst, 'DOH2')

    # calculate ROP - add lead time demand to SS
    safety_stock_df['reorder_point'] = safety_stock_df.apply(
        lambda row: np.round(
            (row['lead_time_mean'] + review_period) * row['fcst'] / fcst_weeks / 7),
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

    # ========== CORRECTION PLUGINS (REWORK SS,ROP,OUP BASED ON REQ) ===========

    final_ss_df = safety_stock_df.copy()

    # if v3_active_flag == 'Y':
    #     logger.info("IPC V3 Correction starts")
    #     df_pre_corr = final_ss_df.copy()
    #     final_ss_df = v3_corrections(final_ss_df, store_id,
    #                                  corrections_selling_probability_cutoff,
    #                                  corrections_cumulative_probability_cutoff,
    #                                  schema, db, logger)
    #     df_post_corr = final_ss_df.copy()
    #     logger.info(f"Sum OUP before: {df_pre_corr['order_upto_point'].sum()}")
    #     logger.info(f"Sum OUP after: {df_post_corr['order_upto_point'].sum()}")

    #     corr_drug_lst = compare_df(df_pre_corr, df_post_corr, logger)
    #     final_ss_df = add_correction_flag(final_ss_df, corr_drug_lst, 'V3')

    if v3_active_flag == 'Y':
        logger.info("IPC V3N Correction starts")
        df_pre_corr = final_ss_df.copy()
        final_ss_df = v3N_corrections(final_ss_df, store_id,
                                     reset_date,
                                     schema, db, logger)
        df_post_corr = final_ss_df.copy()
        logger.info(f"Sum OUP before: {df_pre_corr['order_upto_point'].sum()}")
        logger.info(f"Sum OUP after: {df_post_corr['order_upto_point'].sum()}")

        corr_drug_lst = compare_df(df_pre_corr, df_post_corr, logger)
        final_ss_df = add_correction_flag(final_ss_df, corr_drug_lst, 'V3N')

    if v4_active_flag == 'Y':
        logger.info("IPC V4 Correction starts")
        df_pre_corr = final_ss_df.copy()
        final_ss_df = v4_corrections(final_ss_df, drug_type_list_v4, db, schema)
        df_post_corr = final_ss_df.copy()
        logger.info(f"Sum OUP before: {df_pre_corr['order_upto_point'].sum()}")
        logger.info(f"Sum OUP after: {df_post_corr['order_upto_point'].sum()}")

        corr_drug_lst = compare_df(df_pre_corr, df_post_corr, logger)
        final_ss_df = add_correction_flag(final_ss_df, corr_drug_lst, 'V4')

    # currently v5 only active for pilot stores
    if (v5_active_flag == 'Y') & (store_id in [51, 134, 83]):
        logger.info("IPC V5 STD-Qty Correction starts")
        df_pre_corr = final_ss_df.copy()
        final_ss_df = v5_corrections(final_ss_df, db, schema, logger)
        df_post_corr = final_ss_df.copy()
        logger.info(f"Sum OUP before: {df_pre_corr['order_upto_point'].sum()}")
        logger.info(f"Sum OUP after: {df_post_corr['order_upto_point'].sum()}")

        corr_drug_lst = compare_df(df_pre_corr, df_post_corr, logger)
        final_ss_df = add_correction_flag(final_ss_df, corr_drug_lst, 'V5')

    # correct cases where ROP=OUP
    df_pre_corr = final_ss_df.copy()
    final_ss_df['order_upto_point'] = np.where(
        ((final_ss_df['order_upto_point'] > 0) &
         (final_ss_df['reorder_point'] == final_ss_df['order_upto_point'])),
        final_ss_df['reorder_point'] + 1, final_ss_df['order_upto_point'])
    df_post_corr = final_ss_df.copy()
    corr_drug_lst = compare_df(df_pre_corr, df_post_corr, logger)
    final_ss_df = add_correction_flag(final_ss_df, corr_drug_lst, 'OUP_CORR')

    return final_ss_df
