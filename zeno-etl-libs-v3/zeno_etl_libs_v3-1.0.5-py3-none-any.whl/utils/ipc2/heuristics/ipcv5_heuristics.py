"""
rework ROP and OUP based on drug-std-qty
"""

from zeno_etl_libs.helper.aws.s3 import S3
import pandas as pd
import numpy as np


def v5_corrections(safety_stock_df, db, schema, logger):
    # ======================= DEFINE BUCKETS TO CORRECT ========================
    corr_buckets = ['AW', 'AX', 'AY', 'BX', 'BY']
    # ==========================================================================

    logger.info("Reading STD-Qty for all drugs")
    # get drug-std_qty data (TO CHANGE READ IF LIVE FOR ALL STORES)
    s3 = S3()
    file_path = s3.download_file_from_s3('STD_QTY_IPC/df_std_qty.csv')
    df_std_qty = pd.read_csv(file_path)

    logger.info("Define Max-STD-Qty for all drugs based on confidence")
    for index, row in df_std_qty.iterrows():
        if row["std_qty_3_cf"] == 'H':
            max_std_qty = row["std_qty_3"]
        elif row["std_qty_2_cf"] in ['H', 'M']:
            max_std_qty = row["std_qty_2"]
        else:
            max_std_qty = row["std_qty"]

        df_std_qty.loc[index, "max_std_qty"] = max_std_qty

    # merge std and max.std to base df
    safety_stock_df = safety_stock_df.merge(
        df_std_qty[["drug_id", "std_qty", "max_std_qty"]], on="drug_id", how="left")
    safety_stock_df["std_qty"] = safety_stock_df["std_qty"].fillna(1)
    safety_stock_df["max_std_qty"] = safety_stock_df["max_std_qty"].fillna(1)

    # drugs to correct and not correct
    df_to_corr = safety_stock_df.loc[
        safety_stock_df["bucket"].isin(corr_buckets)]
    df_not_to_corr = safety_stock_df.loc[
        ~safety_stock_df["bucket"].isin(corr_buckets)]
    logger.info(f"Num drugs considered for correction {df_to_corr.shape[0]}")
    logger.info(f"Num drugs not considered for correction {df_not_to_corr.shape[0]}")

    logger.info("Correction logic starts")
    for index, row in df_to_corr.iterrows():
        fcst = row["fcst"]
        rop = row["reorder_point"]
        oup = row["order_upto_point"]
        std = row["std_qty"]
        max_std = row["max_std_qty"]

        new_rop = std_round(rop, std=max_std)
        if (new_rop != 0) & (new_rop / rop >= 2):
            new_rop = std_round(rop, std=std)
            if (new_rop / rop >= 2) & (new_rop > fcst):
                new_rop = rop  # no correction

        if (new_rop == 0) & (oup > 0):
            new_oup = std
        else:
            new_oup = std_round(oup, std=max_std)

        if (new_oup <= new_rop) & (new_oup != 0):
            new_oup = std_round(new_rop + 1, std=max_std)

        df_to_corr.loc[index, "reorder_point"] = new_rop
        df_to_corr.loc[index, "order_upto_point"] = new_oup

    corr_safety_stock_df = pd.concat([df_to_corr, df_not_to_corr])
    corr_safety_stock_df.drop(columns=["std_qty", "max_std_qty"],
                              axis=1, inplace=True)

    return corr_safety_stock_df


def std_round(x, std):
    """
    round x to the closest higher multiple of std-qty
    """
    return std * np.ceil(x/std)
