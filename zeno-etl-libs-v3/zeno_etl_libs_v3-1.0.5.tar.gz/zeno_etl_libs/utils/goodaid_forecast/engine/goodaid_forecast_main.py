import os
import sys
import argparse

sys.path.append('../../../..')

import pandas as pd
import numpy as np
import datetime as dt

from zeno_etl_libs.utils.goodaid_forecast.engine.config_goodaid import *
from zeno_etl_libs.utils.goodaid_forecast.engine.goodaid_data_load import GoodaidloadData,Goodaid_data_additional_processing,b2_goodaid_load_data
from zeno_etl_libs.utils.goodaid_forecast.engine.goodaid_ts_forecast import *
from zeno_etl_libs.utils.goodaid_forecast.engine.goodaid_data_pre_process import PreprocessData
from zeno_etl_libs.utils.ipc2.engine.segmentation import Segmentation
from dateutil.relativedelta import relativedelta


def drugs_to_comp_gp(sales, sales_pred,  similar_drug_mapping):
    # ================== aggregate drug_id to composition_id ==================
    # df to change sales_pred, sales, sales_daily

    df_drug_comp_hash = similar_drug_mapping.copy(deep = True)
    df_drug_comp_hash.rename(columns = {'group':'comp_gp_hash'},inplace = True)

    sales_pred["drug_id"] = sales_pred["drug_id"].astype(float)
    sales_pred1 = sales_pred.merge(df_drug_comp_hash, on="drug_id", how="left")
    drug_reject = sales_pred1.loc[sales_pred1["comp_gp_hash"].isnull()][
        "drug_id"].unique().tolist()
    drug_accept = sales_pred1.loc[~sales_pred1["comp_gp_hash"].isnull()][
        "drug_id"].unique().tolist()
    sales_pred1 = sales_pred1.dropna()
    sales_pred1 = sales_pred1.groupby(["store_id", "comp_gp_hash", "date"],
                                      as_index=False).agg(
        {"actual_demand": "sum"})
    sales_pred1.rename({"comp_gp_hash": "drug_id"}, axis=1, inplace=True)
    sales_pred1['ts_id'] = (
            sales_pred1[store_col].astype(int).astype(str)
            + '_'
            + sales_pred1[drug_col].astype(str)
    )

    sales1 = sales.merge(df_drug_comp_hash, on="drug_id", how="left")
    sales1 = sales1.groupby(["store_id", "comp_gp_hash", "date"],
                            as_index=False).agg({"actual_demand": "sum"})
    sales1.rename({"comp_gp_hash": "drug_id"}, axis=1, inplace=True)
    sales1['ts_id'] = (
            sales1[store_col].astype(int).astype(str)
            + '_'
            + sales1[drug_col].astype(str)
    )

    return sales1, sales_pred1


def goodaid_ipc_forecast(store_id, reset_date, type_list, schema, db, logger):
    store_id_list = ("({})").format(store_id)  # for sql pass
    last_date = dt.date(day=1, month=8, year=2021)  # max history #baseline
    # last_date = pd.to_datetime(reset_date).date() - dt.timedelta(weeks=26) # capping sales history to 6 months
    # last_date = pd.to_datetime(reset_date).date() - dt.timedelta(weeks=52) # capping sales history to 12 months
    load_max_date = pd.to_datetime(reset_date).date() - dt.timedelta(days = pd.to_datetime(reset_date).dayofweek+1)
    # define empty variables in case of fail
    weekly_fcst = pd.DataFrame()
    ts_fcst = pd.DataFrame()
    ts_fcst_cols = []

    # Load Data

    logger.info("Data Loading Started...")
    data_load_obj = GoodaidloadData()

    (
        drug_list,
        sales_history,
        cfr_pr,
        calendar,
        first_bill_date,
        first_store_drug_bill_date,
        wh_goodaid_assortment,
        similar_drug_mapping,
        sales_history_add
    ) = data_load_obj.load_all_input(
        type_list=type_list,
        store_id_list=store_id_list,
        last_date=last_date,
        reset_date=reset_date,
        schema=schema,
        db=db
    )

    # PreProcess Data
    logger.info("Data Pre Processing Started...")
    data_prep_obj = PreprocessData()

    (
        sales,
        sales_pred,
        cal_sales,
        sales_daily
    ) = data_prep_obj.preprocess_all(
        sales=sales_history,
        drug_list=drug_list,
        cfr_pr=cfr_pr,
        calendar=calendar,
        first_bill_date=first_bill_date,
        last_date=last_date
    )

    train_max_date = sales[date_col].max()
    end_date = sales_pred[date_col].max()


    #Extra PreProcessing
    logger.info("Goodaid Specific Extra processing Started...")
    gdad_ep_obj = Goodaid_data_additional_processing()

    sales,sales_pred = gdad_ep_obj.goodaid_extra_processing_all(first_store_drug_bill_date=first_store_drug_bill_date,
                                                                sales_pred=sales_pred,
                                                                sales = sales,
                                                                reset_date=reset_date,
                                                                first_bill_date=first_bill_date,
                                                                wh_goodaid_assortment=wh_goodaid_assortment
                                                                )

    #Segmentation
    logger.info("Segmentation Started...")
    seg_obj = Segmentation()
    seg_df, drug_class = seg_obj.get_weekly_segmentation(
        df=sales.copy(deep=True),
        df_sales_daily=sales_daily.copy(deep=True),
        train_max_date=train_max_date,
        end_date=end_date
    )
    seg_df['reset_date'] = str(reset_date)

    merged_df1 = sales_pred


    # Forecasting
    ts_fcst_obj = Goodaid_tS_forecast()
    ts_fcst, ts_fcst_cols = ts_fcst_obj.apply_ts_forecast(
        df=merged_df1.copy(),
        train_max_date=train_max_date,
        forecast_start=train_max_date + relativedelta(weeks=2))

    logger.info("Forecast Completed...")


    # Composition/Similar drug Level Forecasting for B2 Bucket

    data_load_obj_new = b2_goodaid_load_data()
    (
        drug_list_comp,
        sales_history_comp,
        cfr_pr_comp,
        calendar_comp,
        drug_info_comp,
        group_info_comp
    ) = data_load_obj_new.load_all_input(
        type_list=type_list,
        store_id_list=store_id_list,
        sales_pred=sales_pred,
        similar_drug_mapping = similar_drug_mapping,
        last_date=last_date,
        reset_date=reset_date,
        schema=schema,
        db=db
    )

    logger.info("date fetched...")

    (
        sales_comp,
        sales_pred_comp,
        cal_sales_comp,
        sales_daily_comp
    ) = data_prep_obj.preprocess_all(
        sales=sales_history_comp,
        drug_list=drug_list_comp,
        cfr_pr=cfr_pr_comp,
        calendar=calendar_comp,
        first_bill_date=first_bill_date,
        last_date=last_date
    )

    logger.info("data preprocess part 1...")

    sales1, sales_pred1= drugs_to_comp_gp(sales_comp, sales_pred_comp, similar_drug_mapping)

    logger.info("data preprocess part 2...")

    train_max_date = sales1[date_col].max()
    end_date = sales_pred1[date_col].max()
    merged_df2 = sales_pred1

    ts_fcst_obj = Goodaid_tS_forecast()
    ts_fcst2, ts_fcst_cols2 = ts_fcst_obj.apply_ts_forecast(
        df=merged_df2.copy(),
        train_max_date=train_max_date,
        forecast_start=train_max_date + relativedelta(weeks=2))

    logger.info("forecast 2 completed...")

    ts_fcst2 = ts_fcst2.drop_duplicates(
      subset = ['ts_id', 'date'],
      keep = 'last')

    ts_fcst2.drop(['store_id', 'drug_id', 'actual_demand',], axis=1, inplace=True)

    weekly_fcst = ts_fcst.copy(deep=True)
    weekly_fcst['reset_date'] = reset_date

    weekly_fcst.drop_duplicates(inplace=True)
    weekly_fcst['model'] = 'AvgTS'
    weekly_fcst[[store_col, drug_col]] = weekly_fcst[key_col].str.split('_',
                                                                        expand=True)
    weekly_fcst.rename(columns={'preds_AE_ts': 'fcst'}, inplace=True)
    weekly_fcst = pd.merge(weekly_fcst, seg_df[['ts_id', 'std', 'Mixed']],
                           how='left', on=['ts_id'])
    weekly_fcst.rename(columns={'Mixed': 'bucket'}, inplace=True)

    weekly_fcst = weekly_fcst[
        ['store_id', 'drug_id', 'model', 'date', 'fcst', 'std', 'bucket','age_bucket', 'wh_assortment']]
    fc_cols = [i for i in weekly_fcst.columns if i.startswith('preds_')]
    weekly_fcst['std'].fillna(seg_df['std'].mean(), inplace=True)

    agg_fcst = weekly_fcst.groupby(
        ['model', 'store_id', 'drug_id', 'bucket']). \
        agg({'fcst': 'sum', 'std': 'mean', 'age_bucket':'first', 'wh_assortment':'first'}).reset_index()

    agg_fcst['drug_id'] = agg_fcst['drug_id'].astype(int)

    weekly_fcst2 = ts_fcst2.copy(deep=True)
    weekly_fcst2['reset_date'] = reset_date

    weekly_fcst2.drop_duplicates(inplace=True)
    weekly_fcst2['model'] = 'AvgTS'
    weekly_fcst2[[store_col, drug_col]] = weekly_fcst2[key_col].str.split('_',
                                                                        expand=True)
    weekly_fcst2.rename(columns={'preds_AE_ts': 'fcst'}, inplace=True)

    weekly_fcst2 = weekly_fcst2[
        ['store_id', 'drug_id', 'model', 'date', 'fcst']]

    agg_fcst2 = weekly_fcst2.groupby(
        ['model', 'store_id', 'drug_id']). \
        agg({'fcst': 'sum'}).reset_index()

    agg_fcst2.rename(columns={'drug_id':'group'},inplace=True)

    agg_fcst2['age_bucket'] = 'B2'

    agg_fcst2.drop(['model'], axis=1, inplace=True)

    agg_fcst = agg_fcst.merge(similar_drug_mapping[['drug_id','group']],on = 'drug_id',how='left')

    suffix_for_similar_drugs = '_sdlf'

    agg_fcst = agg_fcst.merge(agg_fcst2, on = ['store_id','group','age_bucket'],how='left',suffixes=('', suffix_for_similar_drugs))

    agg_fcst.drop(['group'], axis=1, inplace=True)

    agg_fcst['store_id'] = agg_fcst['store_id'].astype(int)

    col = 'fcst'

    condition = [agg_fcst[col + suffix_for_similar_drugs].isna(),
                 agg_fcst[col] >= (agg_fcst[col + suffix_for_similar_drugs]) * generic_share_in_first_3_months,
                 agg_fcst[col] <  (agg_fcst[col + suffix_for_similar_drugs]) * generic_share_in_first_3_months]
    choice = [agg_fcst[col], agg_fcst[col], (agg_fcst[col + suffix_for_similar_drugs]) * generic_share_in_first_3_months]
    choice2 = ['individual','individual','composition']
    agg_fcst[col + '_ol'] = agg_fcst[col]
    agg_fcst[col] = np.select(condition, choice)
    agg_fcst['fcst_level'] = np.select(condition, choice2,default='individual')

    return agg_fcst, cal_sales, weekly_fcst, seg_df, drug_class


