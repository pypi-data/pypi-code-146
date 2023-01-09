"""
all calculations for ranking (DC & Franchisee) happens within this module
"""

import pandas as pd

from zeno_etl_libs.utils.distributor_ranking2.pull_data import \
    pull_data_dc, pull_data_franchisee
from zeno_etl_libs.utils.distributor_ranking2.calculate_ranks import \
    calc_ranks_dc, get_final_ranks_dc, calc_ranks_franchisee, \
    get_final_ranks_franchisee
from zeno_etl_libs.utils.distributor_ranking2.preprocess_features import \
    preprocess_features_dc, preprocess_features_franchisee
from zeno_etl_libs.utils.distributor_ranking2.calculate_features import \
    calculate_features
from zeno_etl_libs.utils.distributor_ranking2.post_process_ranking import \
    post_process_ranking_dc, post_process_ranking_franchisee


def ranking_calc_dc(reset_date, time_interval_dc, as_ms_weights_dc_drug_lvl,
                    as_ms_weights_dc_type_lvl, pr_weights_dc_drug_lvl,
                    pr_weights_dc_type_lvl, logger, db, schema):

    # =============================== PULL DATA ===============================

    logger.info("Pulling data for DC")
    # add 7 days to time interval since we do not want to include last week's data.
    time_interval = time_interval_dc + 7

    df_features, df_distributors, df_dc_distributors_mapping, \
        df_distributor_drugs = pull_data_dc(
            reset_date, time_interval, db, schema)

    # ========================== DATA PRE-PROCESSING ==========================

    logger.info("Preprocessing data")
    df_features = preprocess_features_dc(df_features, df_dc_distributors_mapping,
                                         df_distributor_drugs)

    # add distributor name and distributor features here.
    df_features = pd.merge(df_features, df_distributors,
                           on=['partial_distributor_id', 'drug_type'],
                           how='left', validate='many_to_one')

    # ========================== FEATURE CALCULATION ==========================

    logger.info("Calculating features")
    features = calculate_features(df_features, reset_date, time_interval_dc,
                                  logger, group_cols=['partial_dc_id',
                                                      'partial_distributor_id',
                                                      'drug_id'])

    # add drug type column
    features = pd.merge(features,
                        df_features[['drug_id', 'drug_type']].drop_duplicates(),
                        on=['drug_id'], how='left', validate='many_to_one')

    # add dist info
    features = pd.merge(features, df_features[
        ['partial_distributor_id', 'partial_distributor_name',
         'partial_distributor_credit_period', 'drug_type',
         'dist_type_portfolio_size']].drop_duplicates(),
                        on=['partial_distributor_id', 'drug_type'], how='left',
                        validate='many_to_one')

    # add dc name
    features = pd.merge(features, df_features[
        ['partial_dc_id', 'dc_name']].dropna().drop_duplicates(),
                        on=['partial_dc_id'], validate='many_to_one', how='left')

    # add drug name
    features = pd.merge(features,
                        df_features[['drug_id', 'drug_name']].drop_duplicates(),
                        on=['drug_id'], validate='many_to_one', how='left')

    # ========================= CALCULATE RANKS AS/MS =========================

    logger.info("Ranking starts AS/MS")
    rank_drug_lvl, rank_drug_type_lvl, disq_entries = calc_ranks_dc(
        features, as_ms_weights_dc_drug_lvl, as_ms_weights_dc_type_lvl, logger)

    final_ranks = get_final_ranks_dc(
        rank_drug_lvl, rank_drug_type_lvl, disq_entries, features,
        df_distributor_drugs, df_distributors, df_dc_distributors_mapping,
        as_ms_weights_dc_drug_lvl, logger)

    # ====================== POST PROCESS RANK DFs AS/MS ======================

    logger.info("Post processing rank-DFs AS/MS")
    final_ranks_as_ms, ranked_features_as_ms = post_process_ranking_dc(
        features, rank_drug_lvl, rank_drug_type_lvl, final_ranks,
        as_ms_weights_dc_drug_lvl, as_ms_weights_dc_type_lvl)

    final_ranks_as_ms["request_type"] = "AS/MS"
    ranked_features_as_ms["request_type"] = "AS/MS"

    # ========================== CALCULATE RANKS PR ===========================

    logger.info("Ranking starts PR")
    rank_drug_lvl, rank_drug_type_lvl, disq_entries = calc_ranks_dc(
        features, pr_weights_dc_drug_lvl, pr_weights_dc_type_lvl, logger)

    final_ranks = get_final_ranks_dc(
        rank_drug_lvl, rank_drug_type_lvl, disq_entries, features,
        df_distributor_drugs, df_distributors, df_dc_distributors_mapping,
        pr_weights_dc_drug_lvl, logger)

    # ======================== POST PROCESS RANK DFs PR =======================

    logger.info("Post processing rank-DFs PR")
    final_ranks_pr, ranked_features_pr = post_process_ranking_dc(
        features, rank_drug_lvl, rank_drug_type_lvl, final_ranks,
        pr_weights_dc_drug_lvl, pr_weights_dc_type_lvl)

    final_ranks_pr["request_type"] = "PR"
    ranked_features_pr["request_type"] = "PR"

    # =========================== JOIN DFs AS/MS & PR =========================

    final_ranks = pd.concat([final_ranks_as_ms, final_ranks_pr], axis=0)
    ranked_features = pd.concat([ranked_features_as_ms, ranked_features_pr], axis=0)

    return ranked_features, final_ranks


def ranking_calc_franchisee(reset_date, time_interval_franchisee,
                            franchisee_stores, weights_franchisee_drug_lvl,
                            weights_franchisee_type_lvl, logger, db, schema):

    # =============================== PULL DATA ===============================

    logger.info("Pulling data for franchisee")
    # add 7 days to time interval since we do not want to include last week's data.
    time_interval = time_interval_franchisee + 7

    df_features, df_distributors, df_distributor_drugs = pull_data_franchisee(
                reset_date, time_interval, franchisee_stores, db, schema)

    # ========================== DATA PRE-PROCESSING ==========================

    logger.info("Preprocessing data")
    df_features = preprocess_features_franchisee(
        df_features, df_distributor_drugs, db, schema)

    # add distributor name and distributor features here.
    df_features = pd.merge(df_features, df_distributors,
                           on=['partial_distributor_id', 'drug_type'],
                           how='left', validate='many_to_one')

    # ========================== FEATURE CALCULATION ==========================

    logger.info("Calculating features")
    features = calculate_features(df_features, reset_date, time_interval_franchisee,
                                  logger, group_cols=['store_id',
                                                      'partial_distributor_id',
                                                      'drug_id'])

    # add drug type column
    features = pd.merge(features,
                        df_features[['drug_id', 'drug_type']].drop_duplicates(),
                        on=['drug_id'], how='left', validate='many_to_one')

    # add dist info
    features = pd.merge(features, df_features[
        ['partial_distributor_id', 'partial_distributor_name',
         'partial_distributor_credit_period', 'drug_type',
         'dist_type_portfolio_size']].drop_duplicates(),
                        on=['partial_distributor_id', 'drug_type'], how='left',
                        validate='many_to_one')

    # add store name and franchisee_id here.
    features = pd.merge(
        features, df_features[['store_id', 'store_name', 'franchisee_id']].dropna().drop_duplicates(),
        on=['store_id'], validate='many_to_one', how='left')

    # add drug name
    features = pd.merge(features,
                        df_features[['drug_id', 'drug_name']].drop_duplicates(),
                        on=['drug_id'], validate='many_to_one', how='left')

    # ============================ CALCULATE RANKS ============================

    logger.info("Ranking starts")
    rank_drug_lvl, rank_drug_type_lvl = calc_ranks_franchisee(
        features, weights_franchisee_drug_lvl, weights_franchisee_type_lvl,
        logger)

    final_ranks = get_final_ranks_franchisee(
        rank_drug_lvl, rank_drug_type_lvl, features, logger)

    # ========================= POST PROCESS RANK DFs =========================

    logger.info("Post processing rank-DFs")
    final_ranks, ranked_features = post_process_ranking_franchisee(
        features, rank_drug_lvl, rank_drug_type_lvl, final_ranks,
        weights_franchisee_drug_lvl, weights_franchisee_type_lvl)

    final_ranks["request_type"] = "ALL"
    ranked_features["request_type"] = "ALL"

    return ranked_features, final_ranks
