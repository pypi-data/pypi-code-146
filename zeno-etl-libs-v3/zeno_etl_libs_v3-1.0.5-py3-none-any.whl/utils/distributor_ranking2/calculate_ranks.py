import pandas as pd
import numpy as np
import math

from zeno_etl_libs.utils.distributor_ranking2.correction_flag import add_corr_flag


def calc_ranks_dc(features, weights_dc_drug_lvl, weights_dc_type_lvl, logger):

    # =========================== DRUG LEVEL RANKING ==========================

    logger.info("DC-drug level ranking starts")
    # select only relevant columns required for ranking
    rank_drug_lvl = features[
        ['partial_dc_id', 'partial_distributor_id', 'drug_id', 'margin',
         'wtd_ff', 'dist_type_portfolio_size', 'partial_distributor_credit_period',
         'request_volume_dc_dist']]

    # set significant digits for features with decimal points
    rank_drug_lvl["margin"] = np.round(rank_drug_lvl["margin"], 3)
    rank_drug_lvl["wtd_ff"] = np.round(rank_drug_lvl["wtd_ff"], 3)
    rank_drug_lvl["request_volume_dc_dist"] = np.round(
        rank_drug_lvl["request_volume_dc_dist"], 3)

    # rank each features
    rank_drug_lvl["rank_margin"] = \
        rank_drug_lvl.groupby(['partial_dc_id', 'drug_id'])['margin'].rank(
            method='dense', ascending=False)
    rank_drug_lvl["rank_ff"] = \
        rank_drug_lvl.groupby(['partial_dc_id', 'drug_id'])['wtd_ff'].rank(
            method='dense', ascending=False)
    rank_drug_lvl["rank_dist_type_portfolio_size"] = \
        rank_drug_lvl.groupby(['partial_dc_id', 'drug_id'])[
            'dist_type_portfolio_size'].rank(method='dense', ascending=False)
    rank_drug_lvl["rank_dc_dist_credit_period"] = \
        rank_drug_lvl.groupby(['partial_dc_id'])[
            'partial_distributor_credit_period'].rank(method='dense',
                                                      ascending=False)
    rank_drug_lvl['rank_dc_dist_volume'] = features.groupby(['partial_dc_id'])[
        'request_volume_dc_dist'].rank(method='dense', ascending=False)

    # primary ranking only based on margin & ff
    rank_drug_lvl["wtd_rank"] = (rank_drug_lvl["rank_margin"] *
                                 weights_dc_drug_lvl["margin"]) + \
                                (rank_drug_lvl["rank_ff"] *
                                 weights_dc_drug_lvl["ff"])
    rank_drug_lvl["wtd_rank"] = np.round(rank_drug_lvl["wtd_rank"], 1)

    # setting rules of ranking preference order in cases of ties
    group_cols = ["partial_dc_id", "drug_id"]
    group_col_sort_asc_order = [True, True]
    sort_columns = group_cols + ["wtd_rank", "rank_dc_dist_credit_period",
                                 "rank_dc_dist_volume",
                                 "rank_dist_type_portfolio_size"]
    sort_asc_order = group_col_sort_asc_order + [True, True, True, True]

    rank_drug_lvl = rank_drug_lvl.sort_values(
        sort_columns, ascending=sort_asc_order).reset_index(drop=True)
    rank_drug_lvl['index'] = rank_drug_lvl.index

    # final ranking based on preference order
    rank_drug_lvl["final_rank"] = \
        rank_drug_lvl.groupby(['partial_dc_id', 'drug_id'])['index'].rank(
            method='first', ascending=True)
    rank_drug_lvl.drop('index', axis=1, inplace=True)

    # ========================== D.TYPE LEVEL RANKING =========================

    logger.info("DC-drug-type level ranking starts")
    # select only relevant columns required for ranking
    rank_drug_type_lvl = features[
        ['partial_dc_id', 'partial_distributor_id', 'drug_id', 'drug_type',
         'margin', 'wtd_ff', 'dist_type_portfolio_size',
         'partial_distributor_credit_period', 'request_volume_dc_dist']]

    # group by dc-distributor-drug_type level and calculate features
    rank_drug_type_lvl = rank_drug_type_lvl.groupby(
        ["partial_dc_id", "partial_distributor_id", "drug_type"],
        as_index=False).agg({"margin": np.average, "wtd_ff": np.average,
                             "dist_type_portfolio_size": "first",
                             "partial_distributor_credit_period": "first",
                             "request_volume_dc_dist": "first"})

    # round features to 3 significant digits
    rank_drug_type_lvl["margin"] = np.round(rank_drug_type_lvl["margin"], 3)
    rank_drug_type_lvl["wtd_ff"] = np.round(rank_drug_type_lvl["wtd_ff"], 3)
    rank_drug_type_lvl["request_volume_dc_dist"] = np.round(
        rank_drug_type_lvl["request_volume_dc_dist"], 3)

    # rank each features
    rank_drug_type_lvl["rank_margin"] = \
        rank_drug_type_lvl.groupby(['partial_dc_id', 'drug_type'])['margin'].rank(
            method='dense', ascending=False)
    rank_drug_type_lvl["rank_ff"] = \
        rank_drug_type_lvl.groupby(['partial_dc_id', 'drug_type'])['wtd_ff'].rank(
            method='dense', ascending=False)
    rank_drug_type_lvl["rank_dist_type_portfolio_size"] = \
        rank_drug_type_lvl.groupby(['partial_dc_id', 'drug_type'])[
            'dist_type_portfolio_size'].rank(method='dense', ascending=False)
    rank_drug_type_lvl["rank_dc_dist_credit_period"] = \
        rank_drug_type_lvl.groupby(['partial_dc_id'])[
            'partial_distributor_credit_period'].rank(method='dense',
                                                      ascending=False)
    rank_drug_type_lvl['rank_dc_dist_volume'] = \
        rank_drug_type_lvl.groupby(['partial_dc_id'])[
            'request_volume_dc_dist'].rank(method='dense', ascending=False)

    # primary ranking only based on margin, ff & portfolio size
    rank_drug_type_lvl["wtd_rank"] = (rank_drug_type_lvl["rank_margin"] *
                                      weights_dc_type_lvl["margin"]) + \
                                     (rank_drug_type_lvl["rank_ff"] *
                                      weights_dc_type_lvl["ff"]) + \
                                     (rank_drug_type_lvl["rank_dist_type_portfolio_size"] *
                                      weights_dc_type_lvl["portfolio_size"])
    rank_drug_type_lvl["wtd_rank"] = np.round(rank_drug_type_lvl["wtd_rank"], 1)

    # setting rules of ranking preference order in cases of ties
    group_cols = ["partial_dc_id", "drug_type"]
    group_col_sort_asc_order = [True, True]
    sort_columns = group_cols + ["wtd_rank", "rank_dc_dist_credit_period",
                                 "rank_dc_dist_volume"]
    sort_asc_order = group_col_sort_asc_order + [True, True, True]

    rank_drug_type_lvl = rank_drug_type_lvl.sort_values(
        sort_columns, ascending=sort_asc_order).reset_index(drop=True)
    rank_drug_type_lvl['index'] = rank_drug_type_lvl.index

    # final ranking based on preference order
    rank_drug_type_lvl["final_rank"] = \
        rank_drug_type_lvl.groupby(['partial_dc_id', 'drug_type'])['index'].rank(
            method='first', ascending=True)
    rank_drug_type_lvl.drop('index', axis=1, inplace=True)

    # ================== DISQUALIFY POOR DC-DRUG-DISTRIBUTORS =================
    # For cases where a poor distributor in terms of wtd.ff and ff_requests
    # comes in rank 3 or higher => disqualify it. As a result the rank 3 slot
    # becomes vacant for the slot filling logic to assign another distributor
    # which will get a chance to fulfill the order. If the assigned distributor
    # performs good it will be better ranked in subsequent resets, else it will
    # also get disqualified in similar way in later resets. This will keep the
    # cycle to constantly look for better distributors. Else it might get locked
    # in a cycle of ranking the same poor distributor over and over again.
    disq_entries = rank_drug_lvl.merge(
        features[["partial_dc_id", "partial_distributor_id", "drug_id", "ff_requests"]],
        on=["partial_dc_id", "partial_distributor_id", "drug_id"], how="left")

    # disqualify condition
    disq_entries["disqualify"] = np.where(
        (disq_entries["final_rank"] >= 3) &
        ((disq_entries["ff_requests"] == 0) | (disq_entries["wtd_ff"] < 0.4)),
        1, 0)
    disq_entries = disq_entries.loc[(disq_entries["disqualify"] == 1)]
    disq_entries = disq_entries[["partial_dc_id", "partial_distributor_id",
                                 "drug_id", "disqualify"]]

    return rank_drug_lvl, rank_drug_type_lvl, disq_entries


def get_final_ranks_dc(rank_drug_lvl, rank_drug_type_lvl, disq_entries,
                       features, df_distributor_drugs, df_distributors,
                       df_dc_distributors_mapping, weights_dc_drug_lvl, logger):
    """
    get final ranking format and apply slot filling logic to rank slots
    which are empty.
    """

    final_ranks = rank_drug_lvl[["partial_dc_id", "drug_id"]].drop_duplicates()
    final_ranks = final_ranks.merge(
        features[["drug_id", "drug_type"]].drop_duplicates(), on="drug_id",
        how="left")

    # remove disqualified entries
    rank_drug_lvl = rank_drug_lvl.merge(
        disq_entries, on=["partial_dc_id", "partial_distributor_id", "drug_id"],
        how="left")
    rank_drug_lvl = rank_drug_lvl.loc[rank_drug_lvl["disqualify"] != 1]

    logger.info("Creating final df format")
    # make final ranking df
    for rank in [1, 2, 3]:
        df_rank = rank_drug_lvl.loc[rank_drug_lvl["final_rank"] == rank]
        df_rank = df_rank[
            ["partial_dc_id", "drug_id", "partial_distributor_id"]]
        df_rank.rename({"partial_distributor_id": f"distributor_rank_{rank}"},
                       axis=1, inplace=True)
        final_ranks = final_ranks.merge(df_rank,
                                        on=["partial_dc_id", "drug_id"],
                                        how="left")
        final_ranks[f"distributor_rank_{rank}"] = final_ranks[
            f"distributor_rank_{rank}"].astype(float)

    # ================== FILL MISSING RANK SLOTS DC-DRUG LVL ==================

    # get all dc-drug with missing slots
    logger.info("Get allowable dc-drug-distributors to fill slots")
    missing_rank_dc_drugs = final_ranks.loc[
        (final_ranks["distributor_rank_2"].isna()) | (final_ranks["distributor_rank_3"].isna())]
    missing_rank_dc_drugs = missing_rank_dc_drugs[["partial_dc_id", "drug_id", "drug_type"]]

    # list all missing drugs
    list_missing_rank_drugs = list(missing_rank_dc_drugs["drug_id"].unique())

    # get all distributors with missing drugs in their portfolio
    select_distributor_drugs = df_distributor_drugs.loc[
        df_distributor_drugs["drug_id"].isin(list_missing_rank_drugs)]

    # assign it to all dc
    available_mappings = missing_rank_dc_drugs.merge(select_distributor_drugs,
                                                     on="drug_id", how="left")

    # merge distributor details
    available_mappings = available_mappings.merge(
        df_distributors[["partial_distributor_id", "partial_distributor_credit_period"]].drop_duplicates(),
        on="partial_distributor_id", how="left")

    # calculate features on drug_type level for dc-distributors (margin & ff)
    distributor_type_lvl_features = features.groupby(
        ["partial_dc_id", "partial_distributor_id", "drug_type"],
        as_index=False).agg({"margin": np.average, "wtd_ff": np.average,
                             "request_volume_dc_dist": "first"})
    available_mappings = available_mappings.merge(
        distributor_type_lvl_features, on=["partial_dc_id",
                                           "partial_distributor_id",
                                           "drug_type"], how="left")

    # fill na and set significant digits
    available_mappings["margin"] = available_mappings["margin"].fillna(0)
    available_mappings["wtd_ff"] = available_mappings["wtd_ff"].fillna(0)
    available_mappings["request_volume_dc_dist"] = available_mappings[
        "request_volume_dc_dist"].fillna(0)
    available_mappings["margin"] = np.round(available_mappings["margin"], 3)
    available_mappings["wtd_ff"] = np.round(available_mappings["wtd_ff"], 3)
    available_mappings["request_volume_dc_dist"] = np.round(
        available_mappings["request_volume_dc_dist"], 3)

    # remove inactive dc-distributors
    available_mappings = available_mappings.merge(
        df_dc_distributors_mapping, on=["partial_dc_id", "partial_distributor_id"],
        how="inner")

    # remove disqualified entries
    available_mappings = available_mappings.merge(
        disq_entries, on=["partial_dc_id", "partial_distributor_id", "drug_id"],
        how="left")
    available_mappings = available_mappings.loc[available_mappings["disqualify"] != 1]

    # ranking distributors based on dc-drug level logic
    logger.info("Ranking allowable dc-drug-distributors")
    available_mapping_ranked = available_mappings.copy()
    available_mapping_ranked["rank_margin"] = \
        available_mapping_ranked.groupby(['partial_dc_id', 'drug_id'])[
            'margin'].rank(method='dense', ascending=False)
    available_mapping_ranked["rank_ff"] = \
        available_mapping_ranked.groupby(['partial_dc_id', 'drug_id'])[
            'wtd_ff'].rank(method='dense', ascending=False)
    available_mapping_ranked["rank_dc_dist_credit_period"] = \
        available_mapping_ranked.groupby(['partial_dc_id'])[
            'partial_distributor_credit_period'].rank(method='dense',
                                                      ascending=False)
    available_mapping_ranked['rank_dc_dist_volume'] = \
        available_mapping_ranked.groupby(['partial_dc_id'])[
            'request_volume_dc_dist'].rank(method='dense', ascending=False)

    # calculate wtd.ranks
    available_mapping_ranked["wtd_rank"] = (available_mapping_ranked["rank_margin"] *
                                            weights_dc_drug_lvl["margin"]) + \
                                           (available_mapping_ranked["rank_ff"] *
                                            weights_dc_drug_lvl["ff"])
    available_mapping_ranked["wtd_rank"] = np.round(
        available_mapping_ranked["wtd_rank"], 1)

    # set sorting order
    group_cols = ["partial_dc_id", "drug_id"]
    group_col_sort_asc_order = [True, True]
    sort_columns = group_cols + ["wtd_rank", "rank_dc_dist_credit_period",
                                 "rank_dc_dist_volume"]
    sort_asc_order = group_col_sort_asc_order + [True, True, True]

    available_mapping_ranked = available_mapping_ranked.sort_values(
        sort_columns, ascending=sort_asc_order).reset_index(drop=True)
    available_mapping_ranked['index'] = available_mapping_ranked.index

    # get final ranks
    available_mapping_ranked["final_rank"] = \
        available_mapping_ranked.groupby(['partial_dc_id', 'drug_id'])[
            'index'].rank(method='first', ascending=True)
    available_mapping_ranked.drop('index', axis=1, inplace=True)

    pre_corr = final_ranks.copy()  # to compare pre-post correction

    # adding auxiliary ranking to empty slot dc-drugs
    logger.info("Filling empty rank slots with ranked distributors")
    for rank in [1, 2, 3]:
        df_rank = available_mapping_ranked.loc[
            available_mapping_ranked["final_rank"] == rank]
        df_rank = df_rank[
            ["partial_dc_id", "drug_id", "partial_distributor_id"]]
        df_rank.rename(
            {"partial_distributor_id": f"aux_distributor_rank_{rank}"}, axis=1,
            inplace=True)
        final_ranks = final_ranks.merge(df_rank,
                                        on=["partial_dc_id", "drug_id"],
                                        how="left")
        final_ranks[f"aux_distributor_rank_{rank}"] = final_ranks[
            f"aux_distributor_rank_{rank}"].astype(float)

    for index, row in final_ranks.iterrows():
        # if rank 2 empty and aux_rank present
        if math.isnan(row["distributor_rank_2"]) & \
                (not math.isnan(row["aux_distributor_rank_1"])):
            if row["aux_distributor_rank_1"] != row["distributor_rank_1"]:
                final_ranks.loc[index, "distributor_rank_2"] = row[
                    "aux_distributor_rank_1"]
            elif not math.isnan(row["aux_distributor_rank_2"]):
                final_ranks.loc[index, "distributor_rank_2"] = row[
                    "aux_distributor_rank_2"]

    for index, row in final_ranks.iterrows():
        # if rank 1 & 2 filled, rank 3 empty and aux_ranks present
        if (not math.isnan(row["distributor_rank_1"])) & \
                (not math.isnan(row["distributor_rank_2"])) & \
                (math.isnan(row["distributor_rank_3"])):
            if (not math.isnan(row["aux_distributor_rank_1"])) & \
                    (row["aux_distributor_rank_1"] != row["distributor_rank_1"]) & \
                    (row["aux_distributor_rank_1"] != row["distributor_rank_2"]):
                final_ranks.loc[index, "distributor_rank_3"] = row[
                    "aux_distributor_rank_1"]
            elif (not math.isnan(row["aux_distributor_rank_2"])) & \
                    (row["aux_distributor_rank_2"] != row["distributor_rank_1"]) & \
                    (row["aux_distributor_rank_2"] != row["distributor_rank_2"]):
                final_ranks.loc[index, "distributor_rank_3"] = row[
                    "aux_distributor_rank_2"]
            elif (not math.isnan(row["aux_distributor_rank_3"])) & \
                    (row["aux_distributor_rank_3"] != row["distributor_rank_1"]) & \
                    (row["aux_distributor_rank_3"] != row["distributor_rank_2"]):
                final_ranks.loc[index, "distributor_rank_3"] = row[
                    "aux_distributor_rank_3"]

    final_ranks = final_ranks.drop(
        ["aux_distributor_rank_1", "aux_distributor_rank_2",
         "aux_distributor_rank_3"], axis=1)

    post_corr = final_ranks.copy()  # to compare pre-post correction

    # add correction flags where rank2 & rank3 slot filling took place
    logger.info("Adding correction flags for filled rank slots")
    final_ranks = add_corr_flag(final_ranks, pre_corr, post_corr,
                                col_to_compare="distributor_rank_2",
                                corr_flag="R2F",
                                group_cols=["partial_dc_id", "drug_id"])
    final_ranks = add_corr_flag(final_ranks, pre_corr, post_corr,
                                col_to_compare="distributor_rank_3",
                                corr_flag="R3F",
                                group_cols=["partial_dc_id", "drug_id"])

    # ================== COMBINE DC-DRUG LVL & DC-TYPE LVL  ===================

    # add dc-drug-type level ranking
    logger.info("Adding dc-drug-type level ranking to final df")
    final_ranks_type_lvl = rank_drug_type_lvl[
        ["partial_dc_id", "drug_type"]].drop_duplicates()

    # create dc-type level final ranking format
    for rank in [1, 2, 3]:
        df_rank = rank_drug_type_lvl.loc[
            rank_drug_type_lvl["final_rank"] == rank]
        df_rank = df_rank[
            ["partial_dc_id", "drug_type", "partial_distributor_id"]]
        df_rank.rename({"partial_distributor_id": f"distributor_rank_{rank}"},
                       axis=1, inplace=True)
        final_ranks_type_lvl = final_ranks_type_lvl.merge(df_rank,
                                                          on=["partial_dc_id",
                                                              "drug_type"],
                                                          how="left")
        final_ranks_type_lvl[f"distributor_rank_{rank}"] = final_ranks_type_lvl[
            f"distributor_rank_{rank}"].astype(float)

    # combine dc-drug lvl and dc-drug-type lvl
    final_ranks = pd.concat([final_ranks, final_ranks_type_lvl], axis=0)
    final_ranks["correction_flags"] = final_ranks["correction_flags"].fillna("")

    return final_ranks


def calc_ranks_franchisee(features, weights_franchisee_drug_lvl,
                          weights_franchisee_type_lvl, logger):

    # =========================== DRUG LEVEL RANKING ==========================

    logger.info("Franchisee-store-drug level ranking starts")
    # select only relevant columns required for ranking
    rank_drug_lvl = features[
        ['store_id', 'partial_distributor_id', 'drug_id', 'margin',
         'wtd_ff', 'dist_type_portfolio_size', 'partial_distributor_credit_period',
         'request_volume_store_dist']]

    # set significant digits for features with decimal points
    rank_drug_lvl["margin"] = np.round(rank_drug_lvl["margin"], 3)
    rank_drug_lvl["wtd_ff"] = np.round(rank_drug_lvl["wtd_ff"], 3)
    rank_drug_lvl["request_volume_store_dist"] = np.round(
        rank_drug_lvl["request_volume_store_dist"], 3)

    # rank each features
    rank_drug_lvl["rank_margin"] = \
        rank_drug_lvl.groupby(['store_id', 'drug_id'])['margin'].rank(
            method='dense', ascending=False)
    rank_drug_lvl["rank_ff"] = \
        rank_drug_lvl.groupby(['store_id', 'drug_id'])['wtd_ff'].rank(
            method='dense', ascending=False)
    rank_drug_lvl["rank_dist_type_portfolio_size"] = \
        rank_drug_lvl.groupby(['store_id', 'drug_id'])[
            'dist_type_portfolio_size'].rank(method='dense', ascending=False)
    rank_drug_lvl["rank_store_dist_credit_period"] = \
        rank_drug_lvl.groupby(['store_id'])[
            'partial_distributor_credit_period'].rank(method='dense',
                                                      ascending=False)
    rank_drug_lvl['rank_store_dist_volume'] = features.groupby(['store_id'])[
        'request_volume_store_dist'].rank(method='dense', ascending=False)

    # primary ranking only based on margin & ff
    rank_drug_lvl["wtd_rank"] = (rank_drug_lvl["rank_margin"] *
                                 weights_franchisee_drug_lvl["margin"]) + \
                                (rank_drug_lvl["rank_ff"] *
                                 weights_franchisee_drug_lvl["ff"])
    rank_drug_lvl["wtd_rank"] = np.round(rank_drug_lvl["wtd_rank"], 1)

    # setting rules of ranking preference order in cases of ties
    group_cols = ["store_id", "drug_id"]
    group_col_sort_asc_order = [True, True]
    sort_columns = group_cols + ["wtd_rank", "rank_store_dist_credit_period",
                                 "rank_store_dist_volume",
                                 "rank_dist_type_portfolio_size"]
    sort_asc_order = group_col_sort_asc_order + [True, True, True, True]

    rank_drug_lvl = rank_drug_lvl.sort_values(
        sort_columns, ascending=sort_asc_order).reset_index(drop=True)
    rank_drug_lvl['index'] = rank_drug_lvl.index

    # final ranking based on preference order
    rank_drug_lvl["final_rank"] = \
        rank_drug_lvl.groupby(['store_id', 'drug_id'])['index'].rank(
            method='first', ascending=True)
    rank_drug_lvl.drop('index', axis=1, inplace=True)

    # ========================== D.TYPE LEVEL RANKING =========================

    logger.info("Franchisee-drug-type level ranking starts")
    # select only relevant columns required for ranking
    rank_drug_type_lvl = features[
        ['store_id', 'partial_distributor_id', 'drug_id', 'drug_type',
         'margin', 'wtd_ff', 'dist_type_portfolio_size',
         'partial_distributor_credit_period', 'request_volume_store_dist']]

    # group by dc-distributor-drug_type level and calculate features
    rank_drug_type_lvl = rank_drug_type_lvl.groupby(
        ["store_id", "partial_distributor_id", "drug_type"],
        as_index=False).agg({"margin": np.average, "wtd_ff": np.average,
                             "dist_type_portfolio_size": "first",
                             "partial_distributor_credit_period": "first",
                             "request_volume_store_dist": "first"})

    # round features to 3 significant digits
    rank_drug_type_lvl["margin"] = np.round(rank_drug_type_lvl["margin"], 3)
    rank_drug_type_lvl["wtd_ff"] = np.round(rank_drug_type_lvl["wtd_ff"], 3)
    rank_drug_type_lvl["request_volume_store_dist"] = np.round(
        rank_drug_type_lvl["request_volume_store_dist"], 3)

    # rank each features
    rank_drug_type_lvl["rank_margin"] = \
        rank_drug_type_lvl.groupby(['store_id', 'drug_type'])['margin'].rank(
            method='dense', ascending=False)
    rank_drug_type_lvl["rank_ff"] = \
        rank_drug_type_lvl.groupby(['store_id', 'drug_type'])['wtd_ff'].rank(
            method='dense', ascending=False)
    rank_drug_type_lvl["rank_dist_type_portfolio_size"] = \
        rank_drug_type_lvl.groupby(['store_id', 'drug_type'])[
            'dist_type_portfolio_size'].rank(method='dense', ascending=False)
    rank_drug_type_lvl["rank_store_dist_credit_period"] = \
        rank_drug_type_lvl.groupby(['store_id'])[
            'partial_distributor_credit_period'].rank(method='dense',
                                                      ascending=False)
    rank_drug_type_lvl['rank_store_dist_volume'] = \
        rank_drug_type_lvl.groupby(['store_id'])[
            'request_volume_store_dist'].rank(method='dense', ascending=False)

    # primary ranking only based on margin, ff & portfolio size
    rank_drug_type_lvl["wtd_rank"] = (rank_drug_type_lvl["rank_margin"] *
                                      weights_franchisee_type_lvl["margin"]) + \
                                     (rank_drug_type_lvl["rank_ff"] *
                                      weights_franchisee_type_lvl["ff"]) + \
                                     (rank_drug_type_lvl["rank_dist_type_portfolio_size"] *
                                      weights_franchisee_type_lvl["portfolio_size"])
    rank_drug_type_lvl["wtd_rank"] = np.round(rank_drug_type_lvl["wtd_rank"], 1)

    # setting rules of ranking preference order in cases of ties
    group_cols = ["store_id", "drug_type"]
    group_col_sort_asc_order = [True, True]
    sort_columns = group_cols + ["wtd_rank", "rank_store_dist_credit_period",
                                 "rank_store_dist_volume"]
    sort_asc_order = group_col_sort_asc_order + [True, True, True]

    rank_drug_type_lvl = rank_drug_type_lvl.sort_values(
        sort_columns, ascending=sort_asc_order).reset_index(drop=True)
    rank_drug_type_lvl['index'] = rank_drug_type_lvl.index

    # final ranking based on preference order
    rank_drug_type_lvl["final_rank"] = \
        rank_drug_type_lvl.groupby(['store_id', 'drug_type'])['index'].rank(
            method='first', ascending=True)
    rank_drug_type_lvl.drop('index', axis=1, inplace=True)

    return rank_drug_lvl, rank_drug_type_lvl


def get_final_ranks_franchisee(rank_drug_lvl, rank_drug_type_lvl, features,
                               logger):
    """
    get final ranking format. no slot filling logic for franchisee stores.
    """

    final_ranks = rank_drug_lvl[["store_id", "drug_id"]].drop_duplicates()
    final_ranks = final_ranks.merge(
        features[["drug_id", "drug_type"]].drop_duplicates(), on="drug_id",
        how="left")

    logger.info("Creating final df format")
    # make final ranking df
    for rank in [1, 2, 3]:
        df_rank = rank_drug_lvl.loc[rank_drug_lvl["final_rank"] == rank]
        df_rank = df_rank[
            ["store_id", "drug_id", "partial_distributor_id"]]
        df_rank.rename({"partial_distributor_id": f"distributor_rank_{rank}"},
                       axis=1, inplace=True)
        final_ranks = final_ranks.merge(df_rank,
                                        on=["store_id", "drug_id"],
                                        how="left")
        final_ranks[f"distributor_rank_{rank}"] = final_ranks[
            f"distributor_rank_{rank}"].astype(float)

    # add franchisee-store-drug-type level ranking
    logger.info("Adding franchisee-store-drug-typ level ranking to final df")
    final_ranks_type_lvl = rank_drug_type_lvl[
        ["store_id", "drug_type"]].drop_duplicates()

    # create store-type level final ranking format
    for rank in [1, 2, 3]:
        df_rank = rank_drug_type_lvl.loc[
            rank_drug_type_lvl["final_rank"] == rank]
        df_rank = df_rank[
            ["store_id", "drug_type", "partial_distributor_id"]]
        df_rank.rename({"partial_distributor_id": f"distributor_rank_{rank}"},
                       axis=1, inplace=True)
        final_ranks_type_lvl = final_ranks_type_lvl.merge(df_rank,
                                                          on=["store_id",
                                                              "drug_type"],
                                                          how="left")
        final_ranks_type_lvl[f"distributor_rank_{rank}"] = final_ranks_type_lvl[
            f"distributor_rank_{rank}"].astype(float)

    # combine store-drug lvl and store-drug-type lvl
    final_ranks = pd.concat([final_ranks, final_ranks_type_lvl], axis=0)

    return final_ranks
