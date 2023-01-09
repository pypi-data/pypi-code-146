import numpy as np


def add_corr_flag(df_base, df_pre, df_post, col_to_compare="col_name",
                  corr_flag="CORR", group_cols=None):

    if group_cols is None:
        group_cols = ["partial_dc_id", "drug_id"]
    df_pre = df_pre[group_cols + [col_to_compare]]
    df_post = df_post[group_cols + [col_to_compare]]

    df_comb = df_pre.merge(df_post, on=group_cols, how="outer",
                           suffixes=('_pre', '_post'))

    df_comb["changed"] = 'N'
    df_comb[col_to_compare + str('_pre')] = df_comb[col_to_compare + str('_pre')].fillna(0)
    df_comb[col_to_compare + str('_post')] = df_comb[col_to_compare + str('_post')].fillna(0)
    df_comb["changed"] = np.where(
        df_comb[col_to_compare + str('_pre')] != df_comb[col_to_compare + str('_post')],
        'Y', df_comb["changed"])

    # merge changed column entries with base df
    df_final = df_base.merge(df_comb[group_cols + ["changed"]], on=group_cols,
                             how="inner")

    # add correction flag to changed entries
    if "correction_flags" not in df_final.columns:
        df_final["correction_flags"] = ""
    df_final["correction_flags"] = df_final["correction_flags"].fillna("")

    df_final["correction_flags"] = np.where(
        (df_final["changed"] == 'Y') & (df_final["correction_flags"] != ""),
        df_final["correction_flags"] + '-' + corr_flag, df_final["correction_flags"])
    df_final["correction_flags"] = np.where(
        (df_final["changed"] == 'Y') & (df_final["correction_flags"] == ""),
        corr_flag, df_final["correction_flags"])

    df_final.drop("changed", axis=1, inplace=True)

    return df_final

