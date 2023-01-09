import numpy as np

from zeno_etl_libs.utils.ipc_pmf.correction_flag import compare_df, \
    add_correction_flag, compare_df_comb, add_correction_flag_comb


def fcst_correction(fcst_df_comb_lvl, comb_sales_latest_12w,
                    fcst_df_drug_lvl, drug_sales_latest_12w,
                    drug_sales_latest_4w, comb_sales_4w_wtd,
                    drug_sales_4w_wtd, logger):
    comb_sales_latest_12w['latest_28d_demand'] = np.round(
        comb_sales_latest_12w['actual_demand'] / 3)
    drug_sales_latest_12w['latest_28d_demand'] = np.round(
        drug_sales_latest_12w['actual_demand'] / 3)

    fcst_df_comb_lvl['fcst'] = np.round(fcst_df_comb_lvl['fcst'])
    fcst_df_comb_lvl = fcst_df_comb_lvl.merge(
        comb_sales_latest_12w[['comb_id', 'latest_28d_demand']],
        on='comb_id', how='left')


    fcst_df_drug_lvl['drug_id'] = fcst_df_drug_lvl['drug_id'].astype(int)
    fcst_df_drug_lvl['fcst'] = np.round(fcst_df_drug_lvl['fcst'])
    fcst_df_drug_lvl = fcst_df_drug_lvl.merge(
        drug_sales_latest_12w[['drug_id', 'latest_28d_demand']],
        on='drug_id', how='left')

    logger.info(f"Combination Fcst Recency Correction starts")
    df_pre_corr = fcst_df_comb_lvl.copy()
    fcst_df_comb_lvl['fcst'] = np.where(fcst_df_comb_lvl['fcst'] == 0,
                                        fcst_df_comb_lvl['latest_28d_demand'],
                                        fcst_df_comb_lvl['fcst'])
    df_post_corr = fcst_df_comb_lvl.copy()
    logger.info(f"Sum Fcst before: {df_pre_corr['fcst'].sum()}")
    logger.info(f"Sum Fcst after: {df_post_corr['fcst'].sum()}")

    corr_comb_lst = compare_df_comb(df_pre_corr, df_post_corr, logger,
                                    cols_to_compare=['fcst'])
    fcst_df_comb_lvl = add_correction_flag_comb(fcst_df_comb_lvl, corr_comb_lst,
                                                'REC_CORR1')

    logger.info(f"Drug Fcst Recency Correction 1 starts")
    df_pre_corr = fcst_df_drug_lvl.copy()
    fcst_df_drug_lvl['fcst'] = np.where(fcst_df_drug_lvl['fcst'] == 0,
                                        fcst_df_drug_lvl['latest_28d_demand'],
                                        fcst_df_drug_lvl['fcst'])
    df_post_corr = fcst_df_drug_lvl.copy()
    logger.info(f"Sum Fcst before: {fcst_df_drug_lvl['fcst'].sum()}")
    logger.info(f"Sum Fcst after: {fcst_df_drug_lvl['fcst'].sum()}")

    corr_drug_lst = compare_df(df_pre_corr, df_post_corr, logger,
                               cols_to_compare=['fcst'])
    fcst_df_drug_lvl = add_correction_flag(fcst_df_drug_lvl, corr_drug_lst,
                                           'REC_CORR1')

    fcst_df_comb_lvl.drop('latest_28d_demand', axis=1, inplace=True)
    fcst_df_drug_lvl.drop('latest_28d_demand', axis=1, inplace=True)

    # add drugs with recent sales
    forecasted_drug_list = fcst_df_drug_lvl['drug_id'].tolist()
    df_add1 = drug_sales_latest_12w.loc[~drug_sales_latest_12w['drug_id'].isin(forecasted_drug_list)]
    df_add2 = drug_sales_latest_4w.loc[~drug_sales_latest_4w['drug_id'].isin(forecasted_drug_list)]
    df_add1.rename({'latest_28d_demand': 'fcst'}, axis=1, inplace=True)
    df_add1.drop('actual_demand', axis=1, inplace=True)
    df_add2.rename({'actual_demand': 'fcst'}, axis=1, inplace=True)
    df_add = df_add1.append(df_add2)
    df_add = df_add.loc[df_add['fcst'] > 0]
    if df_add.shape[0] > 0:
        df_add['model'] = 'NA'
        df_add['bucket'] = 'NA'
        df_add['std'] = 0
        df_add['correction_flags'] = ""
        df_add['ts_id'] = (
                df_add['store_id'].astype(int).astype(str)
                + '_'
                + df_add['drug_id'].astype(int).astype(str)
        )

        logger.info(f"Drug Fcst Recency Correction 2 starts")
        df_pre_corr = fcst_df_drug_lvl.copy()
        fcst_df_drug_lvl = fcst_df_drug_lvl.append(df_add[fcst_df_drug_lvl.columns])
        df_post_corr = fcst_df_drug_lvl.copy()

        logger.info(f"Sum Fcst before: {fcst_df_drug_lvl['fcst'].sum()}")
        logger.info(f"Sum Fcst after: {fcst_df_drug_lvl['fcst'].sum()}")

        corr_drug_lst = compare_df(df_pre_corr, df_post_corr, logger,
                                   cols_to_compare=['fcst'])
        fcst_df_drug_lvl = add_correction_flag(fcst_df_drug_lvl, corr_drug_lst,
                                               'REC_CORR2')

    fcst_df_comb_lvl['fcst'] = np.where(fcst_df_comb_lvl['fcst'] < 0, 0,
                                        fcst_df_comb_lvl['fcst'])
    fcst_df_drug_lvl['fcst'] = np.where(fcst_df_drug_lvl['fcst'] < 0, 0,
                                        fcst_df_drug_lvl['fcst'])

    # fcst 4 week weighted replace
    logger.info(f"Comb Fcst Recency Correction 3 starts")
    df_pre_corr = fcst_df_comb_lvl.copy()
    fcst_df_comb_lvl = fcst_df_comb_lvl.merge(comb_sales_4w_wtd, on=['store_id', 'comb_id'],
                                              how='left')
    fcst_df_comb_lvl['fcst'] = np.where(fcst_df_comb_lvl['fcst'] < fcst_df_comb_lvl['wtd_demand'],
                                fcst_df_comb_lvl['wtd_demand'], fcst_df_comb_lvl['fcst'])
    df_post_corr = fcst_df_comb_lvl.copy()

    logger.info(f"Sum Fcst before: {df_pre_corr['fcst'].sum()}")
    logger.info(f"Sum Fcst after: {df_post_corr['fcst'].sum()}")

    corr_comb_lst = compare_df_comb(df_pre_corr, df_post_corr, logger,
                               cols_to_compare=['fcst'])
    fcst_df_comb_lvl = add_correction_flag_comb(fcst_df_comb_lvl, corr_comb_lst,
                                           'REC_CORR3')

    logger.info(f"Drug Fcst Recency Correction 3 starts")
    df_pre_corr = fcst_df_drug_lvl.copy()
    fcst_df_drug_lvl = fcst_df_drug_lvl.merge(drug_sales_4w_wtd, on=['store_id', 'drug_id'],
                                              how='left')
    fcst_df_drug_lvl['fcst'] = np.where(fcst_df_drug_lvl['fcst'] < fcst_df_drug_lvl['wtd_demand'],
                                fcst_df_drug_lvl['wtd_demand'], fcst_df_drug_lvl['fcst'])

    df_post_corr = fcst_df_drug_lvl.copy()
    logger.info(f"Sum Fcst before: {df_pre_corr['fcst'].sum()}")
    logger.info(f"Sum Fcst after: {df_post_corr['fcst'].sum()}")

    corr_drug_lst = compare_df(df_pre_corr, df_post_corr, logger,
                               cols_to_compare=['fcst'])
    fcst_df_drug_lvl = add_correction_flag(fcst_df_drug_lvl, corr_drug_lst,
                                           'REC_CORR3')

    fcst_df_comb_lvl.drop('wtd_demand', axis=1, inplace=True)
    fcst_df_drug_lvl.drop('wtd_demand', axis=1, inplace=True)

    return fcst_df_comb_lvl, fcst_df_drug_lvl
