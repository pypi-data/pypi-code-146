import pandas as pd
import numpy as np


def post_process_ranking_dc(features, rank_drug_lvl, rank_drug_type_lvl,
                            final_ranks, weights_dc_drug_lvl, weights_dc_type_lvl):

    # add drug_id dummy column in type lvl
    rank_drug_type_lvl["drug_id"] = np.nan

    # add weights column
    rank_drug_type_lvl["weights"] = str(weights_dc_type_lvl)
    rank_drug_lvl["weights"] = str(weights_dc_drug_lvl)

    # additional details to be added
    drugs_info = features[["drug_id", "drug_type", "drug_name"]].drop_duplicates()
    dc_info = features[["partial_dc_id", "dc_name"]].drop_duplicates()
    distributor_info = features[["partial_distributor_id", "partial_distributor_name"]].drop_duplicates()

    # adding details into drug_lvl_df
    rank_drug_lvl = rank_drug_lvl.merge(drugs_info, on="drug_id", how="left")
    rank_drug_lvl = rank_drug_lvl.merge(dc_info, on="partial_dc_id", how="left")
    rank_drug_lvl = rank_drug_lvl.merge(
        distributor_info, on="partial_distributor_id", how="left")

    # adding details into drug_type_lvl_df
    rank_drug_type_lvl = rank_drug_type_lvl.merge(dc_info,
                                                  on="partial_dc_id", how="left")
    rank_drug_type_lvl = rank_drug_type_lvl.merge(
        distributor_info, on="partial_distributor_id", how="left")

    # combine drug_lvl and drug_type_lvl df
    ranked_features = pd.concat([rank_drug_lvl, rank_drug_type_lvl], axis=0)

    # add details into final_ranks df
    final_ranks = final_ranks.merge(dc_info, on="partial_dc_id", how="left")
    final_ranks = final_ranks.merge(drugs_info[["drug_id", "drug_name"]], on="drug_id", how="left")

    # add columns for franchisee rank addition because
    # both dc & franchisee features/ranks needs to be written to same table.
    final_ranks["franchisee_id"] = 1  # zippin id
    final_ranks["store_id"] = np.nan
    final_ranks["store_name"] = ""

    ranked_features["franchisee_id"] = 1  # zippin id
    ranked_features["store_id"] = np.nan
    ranked_features["store_name"] = ""
    ranked_features["request_volume_store_dist"] = np.nan
    ranked_features["rank_store_dist_credit_period"] = np.nan
    ranked_features["rank_store_dist_volume"] = np.nan

    return final_ranks, ranked_features


def post_process_ranking_franchisee(features, rank_drug_lvl, rank_drug_type_lvl,
                                    final_ranks, weights_franchisee_drug_lvl,
                                    weights_franchisee_type_lvl):

    # add drug_id dummy column in type lvl
    rank_drug_type_lvl["drug_id"] = np.nan

    # add weights column
    rank_drug_type_lvl["weights"] = str(weights_franchisee_type_lvl)
    rank_drug_lvl["weights"] = str(weights_franchisee_drug_lvl)

    # additional details to be added
    drugs_info = features[["drug_id", "drug_type", "drug_name"]].drop_duplicates()
    store_info = features[["store_id", "store_name", "franchisee_id"]].drop_duplicates()
    distributor_info = features[["partial_distributor_id",
                                 "partial_distributor_name"]].drop_duplicates()

    # adding details into drug_lvl_df
    rank_drug_lvl = rank_drug_lvl.merge(drugs_info, on="drug_id", how="left")
    rank_drug_lvl = rank_drug_lvl.merge(store_info, on="store_id", how="left")
    rank_drug_lvl = rank_drug_lvl.merge(
        distributor_info, on="partial_distributor_id", how="left")

    # adding details into drug_type_lvl_df
    rank_drug_type_lvl = rank_drug_type_lvl.merge(store_info,
                                                  on="store_id",
                                                  how="left")
    rank_drug_type_lvl = rank_drug_type_lvl.merge(
        distributor_info, on="partial_distributor_id", how="left")

    # combine drug_lvl and drug_type_lvl df
    ranked_features = pd.concat([rank_drug_lvl, rank_drug_type_lvl], axis=0)

    # add details into final_ranks df
    final_ranks = final_ranks.merge(store_info, on="store_id", how="left")
    final_ranks = final_ranks.merge(drugs_info[["drug_id", "drug_name"]],
                                    on="drug_id", how="left")

    # add columns for dc rank addition because
    # both dc & franchisee features/ranks needs to be written to same table.
    final_ranks["partial_dc_id"] = np.nan
    final_ranks["dc_name"] = ""
    final_ranks["correction_flags"] = ""

    ranked_features["partial_dc_id"] = np.nan
    ranked_features["dc_name"] = ""
    ranked_features["request_volume_dc_dist"] = np.nan
    ranked_features["rank_dc_dist_credit_period"] = np.nan
    ranked_features["rank_dc_dist_volume"] = np.nan

    return final_ranks, ranked_features
