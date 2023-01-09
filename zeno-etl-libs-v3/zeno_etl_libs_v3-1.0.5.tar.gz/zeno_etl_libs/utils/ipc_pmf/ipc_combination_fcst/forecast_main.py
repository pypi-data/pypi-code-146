import pandas as pd
import numpy as np
import datetime as dt
import time
from dateutil.relativedelta import relativedelta

from zeno_etl_libs.utils.ipc2.engine.data_load import LoadData
from zeno_etl_libs.utils.ipc2.engine.forecast import Forecast
from zeno_etl_libs.utils.ipc2.engine.feat_engg import Feature_Engg

from zeno_etl_libs.utils.ipc_pmf.ipc_combination_fcst.engine.data_pre_process import PreprocessData
from zeno_etl_libs.utils.ipc_pmf.ipc_combination_fcst.engine.segmentation import Segmentation
from zeno_etl_libs.utils.ipc_pmf.ipc_combination_fcst.engine.ts_fcst import TS_forecast

from zeno_etl_libs.utils.ipc_pmf.config_ipc_combination import *


def ipc_comb_forecast(store_id, reset_date, type_list, schema, db, logger):
    store_id_list = ("({})").format(store_id)  # for sql pass
    last_date = dt.date(day=1, month=4, year=2019)  # max history
    load_max_date = pd.to_datetime(reset_date).date() - dt.timedelta(
        days=pd.to_datetime(reset_date).dayofweek + 1)

    # define empty variables in case of fail
    weekly_fcst = pd.DataFrame()
    ts_fcst = pd.DataFrame()
    ts_fcst_cols = []

    logger.info("Data Loading Started...")
    data_load_obj = LoadData()

    (
        drug_list,
        sales_history,
        cfr_pr,
        calendar,
        first_bill_date,
        drug_sp
    ) = data_load_obj.load_all_input(
        type_list=type_list,
        store_id_list=store_id_list,
        last_date=last_date,
        reset_date=reset_date,
        load_max_date=load_max_date,
        schema=schema,
        db=db
    )

    # consider only drugs in specified type
    drug_list = drug_list["drug_id"].unique().tolist()
    sales_history = sales_history.loc[sales_history[drug_col].isin(drug_list)]
    cfr_pr = cfr_pr.loc[cfr_pr[drug_col].isin(drug_list)]

    # ========================================================================
    # AGGREGATE DRUG-LEVEL DEMAND TO COMBINATION LEVEL DEMAND
    # ========================================================================
    sales_history, cfr_pr, comb_list = drugs_to_comb_gps(sales_history, cfr_pr,
                                                         schema, db)
    # ========================================================================

    logger.info("Data Pre Processing Started...")
    data_prep_obj = PreprocessData()

    (
        comb_sales_4w_wtd,
        comb_sales_latest_12w,
        train_4w_agg_vald_max_date,
        sales_pred_4w_agg_vald,
        train_vald_max_date,
        sales_pred_vald,
        sales_4w_agg,
        sales_pred_4w_agg,
        sales,
        sales_pred,
        cal_sales,
        sales_daily
    ) = data_prep_obj.preprocess_all(
        sales=sales_history,
        comb_list=comb_list,
        cfr_pr=cfr_pr,
        calendar=calendar,
        first_bill_date=first_bill_date,
        last_date=last_date
    )

    train_max_date = sales[date_col].max()
    end_date = sales_pred[date_col].max()

    logger.info("Segmentation Started...")
    seg_obj = Segmentation()

    seg_df = seg_obj.get_weekly_segmentation(
        df=sales.copy(deep=True),
        df_sales_daily=sales_daily.copy(deep=True),
        train_max_date=train_max_date,
        end_date=end_date
    )

    seg_df['reset_date'] = str(reset_date)

    # ========================================================================
    # VALIDATION AND BEST MODEL FOR BUCKET SELECTION
    # ========================================================================
    # Find validation period actual demand
    valid_start_date = train_max_date - relativedelta(weeks=4)
    valid_period_demand = sales.loc[sales[date_col] > valid_start_date]
    valid_period_demand = valid_period_demand.groupby(key_col, as_index=False).agg({target_col: "sum"})

    min_history_date_validation = valid_start_date - relativedelta(weeks=4)
    df_min_date = sales_pred_vald.groupby(key_col, as_index=False).agg({date_col: 'min'})
    df_min_date['min_allowed_date'] = min_history_date_validation
    ts_ids_to_drop = df_min_date.loc[df_min_date['min_allowed_date']<df_min_date[date_col]][key_col].tolist()

    # Perform Un-Aggregated TS Forecast
    merged_df1 = pd.merge(sales_pred_vald, seg_df, how='left', on=['ts_id'])
    merged_df1 = merged_df1[merged_df1['PLC Status L1'].isin(['Mature', 'New Product'])]
    merged_df1 = merged_df1[~merged_df1['ts_id'].isin(ts_ids_to_drop)]

    # calculate bucket wise wmape
    valid_wmape = {'Model': []}
    for bucket in ['AW', 'AX', 'AY', 'AZ', 'BW', 'BX', 'BY', 'BZ',
                   'CW', 'CX', 'CY', 'CZ', 'DW', 'DX', 'DY', 'DZ']:
        valid_wmape[bucket] = []

    if runs_ts_flag == 1:
        ts_fcst_obj = TS_forecast()
        ts_fcst, ts_fcst_cols = ts_fcst_obj.apply_ts_forecast(
            df=merged_df1.copy(),
            train_max_date=train_vald_max_date,
            forecast_start=train_vald_max_date + relativedelta(weeks=1))

        for model in ts_fcst_cols:
            df_model = ts_fcst[[key_col, 'Mixed', model]]
            df_model = df_model.groupby(key_col, as_index=False).agg({'Mixed': 'first', model: 'sum'})
            df_model = df_model.merge(valid_period_demand, on=key_col, how='left')
            df_model['error'] = df_model[model] - df_model[target_col]
            df_model['abs_error'] = abs(df_model['error'])
            df_bucket_wmape = df_model.groupby('Mixed', as_index=False).agg({'abs_error': 'sum', target_col: 'sum'})
            df_bucket_wmape['wmape'] = df_bucket_wmape['abs_error']/df_bucket_wmape[target_col]

            valid_wmape['Model'].append(model)
            for bucket in ['AW', 'AX', 'AY', 'AZ', 'BW', 'BX', 'BY', 'BZ',
                           'CW', 'CX', 'CY', 'CZ', 'DW', 'DX', 'DY', 'DZ']:
                try:
                    wmape = df_bucket_wmape.loc[df_bucket_wmape['Mixed'] == bucket]['wmape'].values[0]
                except:
                    wmape = np.inf
                valid_wmape[bucket].append(wmape)

    if run_ml_flag == 1:
        forecast_start = train_vald_max_date + relativedelta(weeks=1)
        weekly_fcst = run_LGBM(merged_df1, train_vald_max_date, forecast_start, logger, is_validation=True)
        lgbm_fcst = weekly_fcst.groupby(key_col, as_index=False).agg({'preds_lgb': 'sum'})

        df_model = lgbm_fcst.merge(valid_period_demand, on=key_col, how='left')
        df_model = df_model.merge(seg_df[[key_col, 'Mixed']], how='left', on='ts_id')
        df_model['error'] = df_model['preds_lgb'] - df_model[target_col]
        df_model['abs_error'] = abs(df_model['error'])
        df_bucket_wmape = df_model.groupby('Mixed', as_index=False).agg(
            {'abs_error': 'sum', target_col: 'sum'})
        df_bucket_wmape['wmape'] = df_bucket_wmape['abs_error'] / df_bucket_wmape[target_col]

        valid_wmape['Model'].append('LGBM')
        for bucket in ['AW', 'AX', 'AY', 'AZ', 'BW', 'BX', 'BY', 'BZ',
                       'CW', 'CX', 'CY', 'CZ', 'DW', 'DX', 'DY', 'DZ']:
            try:
                wmape = df_bucket_wmape.loc[df_bucket_wmape['Mixed'] == bucket]['wmape'].values[0]
            except:
                wmape = np.inf
            valid_wmape[bucket].append(wmape)

    # Perform Aggregated TS Forecast
    merged_df1 = pd.merge(sales_pred_4w_agg_vald, seg_df, how='left', on=['ts_id'])
    merged_df1 = merged_df1[merged_df1['PLC Status L1'].isin(['Mature', 'New Product'])]
    merged_df1 = merged_df1[~merged_df1['ts_id'].isin(ts_ids_to_drop)]
    if run_ts_4w_agg_flag == 1:
        ts_fcst_obj = TS_forecast()
        ts_fcst, ts_fcst_cols = ts_fcst_obj.apply_ts_forecast_agg(
            df=merged_df1.copy(),
            train_max_date=train_4w_agg_vald_max_date,
            forecast_start=train_4w_agg_vald_max_date + relativedelta(weeks=1))

        for model in ts_fcst_cols:
            df_model = ts_fcst[[key_col, 'Mixed', model]]
            df_model = df_model.groupby(key_col, as_index=False).agg(
                {'Mixed': 'first', model: 'sum'})
            df_model = df_model.merge(valid_period_demand, on=key_col,
                                      how='left')
            df_model['error'] = df_model[model] - df_model[target_col]
            df_model['abs_error'] = abs(df_model['error'])
            df_bucket_wmape = df_model.groupby('Mixed', as_index=False).agg(
                {'abs_error': 'sum', target_col: 'sum'})
            df_bucket_wmape['wmape'] = df_bucket_wmape['abs_error'] / df_bucket_wmape[target_col]

            valid_wmape['Model'].append(model)
            for bucket in ['AW', 'AX', 'AY', 'AZ', 'BW', 'BX', 'BY', 'BZ',
                           'CW', 'CX', 'CY', 'CZ', 'DW', 'DX', 'DY', 'DZ']:
                try:
                    wmape = df_bucket_wmape.loc[df_bucket_wmape['Mixed'] == bucket]['wmape'].values[0]
                except:
                    wmape = np.inf
                valid_wmape[bucket].append(wmape)

    if run_ml_4w_agg_flag == 1:
        forecast_start = train_4w_agg_vald_max_date + relativedelta(weeks=4)
        weekly_fcst = run_LGBM(merged_df1, train_4w_agg_vald_max_date, forecast_start,
                               logger, is_validation=True, agg_4w=True)
        lgbm_fcst = weekly_fcst.groupby(key_col, as_index=False).agg(
            {'preds_lgb': 'sum'})

        df_model = lgbm_fcst.merge(valid_period_demand, on=key_col, how='left')
        df_model = df_model.merge(seg_df[[key_col, 'Mixed']], how='left',
                                  on='ts_id')
        df_model['error'] = df_model['preds_lgb'] - df_model[target_col]
        df_model['abs_error'] = abs(df_model['error'])
        df_bucket_wmape = df_model.groupby('Mixed', as_index=False).agg(
            {'abs_error': 'sum', target_col: 'sum'})
        df_bucket_wmape['wmape'] = df_bucket_wmape['abs_error'] / \
                                   df_bucket_wmape[target_col]

        valid_wmape['Model'].append('LGBM_4w_agg')
        for bucket in ['AW', 'AX', 'AY', 'AZ', 'BW', 'BX', 'BY', 'BZ',
                       'CW', 'CX', 'CY', 'CZ', 'DW', 'DX', 'DY', 'DZ']:
            try:
                wmape = df_bucket_wmape.loc[df_bucket_wmape['Mixed'] == bucket][
                    'wmape'].values[0]
            except:
                wmape = np.inf
            valid_wmape[bucket].append(wmape)

    # ========================================================================
    # Choose best model based on lowest wmape
    # ========================================================================
    best_bucket_model = {}
    for bucket in ['AW', 'AX', 'AY', 'AZ', 'BW', 'BX', 'BY', 'BZ',
                   'CW', 'CX', 'CY', 'CZ', 'DW', 'DX', 'DY', 'DZ']:
        min_wmape = min(valid_wmape[bucket])
        if min_wmape != np.inf:
            best_bucket_model[bucket] = valid_wmape['Model'][valid_wmape[bucket].index(min_wmape)]
        else:
            best_bucket_model[bucket] = default_model # default

    # ========================================================================
    # TRAINING AND FINAL FORECAST
    # ========================================================================
    # Perform Un-Aggregated TS Forecast
    merged_df1 = pd.merge(sales_pred, seg_df, how='left', on=['ts_id'])
    merged_df1 = merged_df1[merged_df1['PLC Status L1'].isin(['Mature', 'New Product'])]

    if runs_ts_flag == 1:
        ts_fcst_obj = TS_forecast()
        ts_fcst, ts_fcst_cols = ts_fcst_obj.apply_ts_forecast(
            df=merged_df1.copy(),
            train_max_date=train_max_date,
            forecast_start=train_max_date + relativedelta(weeks=2))

    final_fcst = pd.DataFrame()
    for model_fcst in ts_fcst_cols:
        df_model_fcst = ts_fcst.groupby(key_col, as_index=False).agg({model_fcst: 'sum'})
        df_model_fcst.rename({model_fcst: 'fcst'}, axis=1, inplace=True)
        df_model_fcst['model'] = model_fcst
        final_fcst = final_fcst.append(df_model_fcst)

    if run_ml_flag == 1:
        forecast_start = train_max_date + relativedelta(weeks=2)
        weekly_fcst = run_LGBM(merged_df1, train_max_date, forecast_start, logger, is_validation=False)
        lgbm_fcst = weekly_fcst.groupby(key_col, as_index=False).agg({'preds_lgb': 'sum'})
        lgbm_fcst.rename({'preds_lgb': 'fcst'}, axis=1, inplace=True)
        lgbm_fcst['model'] = 'LGBM'
        final_fcst = final_fcst.append(lgbm_fcst)

    # Perform Aggregated TS Forecast
    merged_df1 = pd.merge(sales_pred_4w_agg, seg_df, how='left', on=['ts_id'])
    merged_df1 = merged_df1[merged_df1['PLC Status L1'].isin(['Mature', 'New Product'])]
    if run_ts_4w_agg_flag == 1:
        ts_fcst_obj = TS_forecast()
        ts_fcst, ts_fcst_cols = ts_fcst_obj.apply_ts_forecast_agg(
            df=merged_df1.copy(),
            train_max_date=train_max_date,
            forecast_start=train_max_date + relativedelta(weeks=2))
        for model_fcst in ts_fcst_cols:
            df_model_fcst = ts_fcst.groupby(key_col, as_index=False).agg(
                {model_fcst: 'sum'})
            df_model_fcst.rename({model_fcst: 'fcst'}, axis=1, inplace=True)
            df_model_fcst['model'] = model_fcst
            final_fcst = final_fcst.append(df_model_fcst)

    if run_ml_4w_agg_flag == 1:
        forecast_start = train_max_date + relativedelta(weeks=2)
        weekly_fcst = run_LGBM(merged_df1, train_max_date, forecast_start,
                               logger, is_validation=False, agg_4w=True)
        lgbm_fcst = weekly_fcst.groupby(key_col, as_index=False).agg(
            {'preds_lgb': 'sum'})
        lgbm_fcst.rename({'preds_lgb': 'fcst'}, axis=1, inplace=True)
        lgbm_fcst['model'] = 'LGBM_4w_agg'
        final_fcst = final_fcst.append(lgbm_fcst)

    final_fcst = final_fcst.merge(seg_df[[key_col, 'Mixed']], on=key_col, how='left')
    final_fcst.rename({'Mixed': 'bucket'}, axis=1, inplace=True)

    # Choose buckets forecast of best models as final forecast
    final_selected_fcst = pd.DataFrame()
    for bucket in best_bucket_model.keys():
        df_selected = final_fcst.loc[(final_fcst['bucket'] == bucket) &
                                     (final_fcst['model'] == best_bucket_model[bucket])]
        final_selected_fcst = final_selected_fcst.append(df_selected)

    # add comb rejected due to recent sales
    list_all_comb = final_fcst[key_col].unique().tolist()
    list_all_final_comb = final_selected_fcst[key_col].unique().tolist()
    list_comb_rejects = list(set(list_all_comb)-set(list_all_final_comb))
    comb_fcst_to_add = final_fcst.loc[(final_fcst[key_col].isin(list_comb_rejects))
                                      & (final_fcst["model"] == default_model)]
    final_selected_fcst = final_selected_fcst.append(comb_fcst_to_add)

    final_selected_fcst = final_selected_fcst.merge(seg_df[[key_col, 'std']],
                                                    on=key_col, how='left')
    final_selected_fcst[[store_col, comb_col]] = final_selected_fcst['ts_id'].str.split('_', expand=True)
    final_selected_fcst[store_col] = final_selected_fcst[store_col].astype(int)

    model_name_map = {'preds_ETS_12w': 'ETS_12w', 'preds_ma': 'MA',
                      'preds_ETS_auto': 'ETS_auto',
                      'preds_ETS_4w_auto': 'ETS_4w_auto'}
    final_selected_fcst["model"] = final_selected_fcst["model"].map(
        model_name_map).fillna(final_selected_fcst["model"])

    return final_selected_fcst, seg_df, comb_sales_latest_12w, comb_sales_4w_wtd


def run_LGBM(merged_df1, train_max_date, forecast_start, logger, is_validation=False, agg_4w=False):
    start_time = time.time()

    merged_df1['All'] = 'All'
    slice_col = 'All'
    forecast_volume = merged_df1[merged_df1[date_col] > train_max_date][
        target_col].sum()
    assert forecast_volume == 0
    logger.info(
        "forecast start {} total volume: {}".format(forecast_start,
                                                    forecast_volume)
    )

    forecast_df = pd.DataFrame()
    validation_df = pd.DataFrame()
    weekly_fcst = pd.DataFrame()

    if agg_4w:
        end_range = 2
    else:
        end_range = 5

    for i in range(1, end_range):

        if is_validation:
            num_shift_lags = i
        else:
            num_shift_lags = i + 1

        # for group_name in merged_df1[slice_col].dropna.unique():
        # slice_col = 'Mixed'
        # for groups in [['AW', 'BW', 'CW', 'DW'], ['AX', 'BX', 'CX', 'DX'], ['AY', 'BY', 'CY', 'DY'], ['AZ', 'BZ', 'CZ', 'DZ']]:
        for groups in ['All']:
            logger.info('Group: {}'.format(groups))
            logger.info("Feature Engineering Started...")
            feat_df = pd.DataFrame()
            for one_df in [merged_df1]:
                feat_engg_obj = Feature_Engg()
                one_feat_df = feat_engg_obj.feat_agg(
                    one_df[
                        one_df[slice_col] == groups
                        ].drop(slice_col, axis=1).copy(deep=True),
                    train_max_date=train_max_date,
                    num_shift_lag=num_shift_lags
                )
                feat_df = pd.concat([one_feat_df, feat_df])

            if pd.DataFrame(feat_df).empty:
                continue

            logger.info(
                "Forecasting Started for {}...".format(forecast_start))
            forecast_obj = Forecast()
            fcst_df, val_df, Feature_Imp_all = forecast_obj.get_STM_forecast(
                feat_df.copy(deep=True),
                forecast_start=forecast_start,
                num_shift_lags=num_shift_lags
            )
            forecast_df = pd.concat([forecast_df, fcst_df], axis=0)
            validation_df = pd.concat([validation_df, val_df])
            ml_fc_cols = [i for i in forecast_df.columns if
                          i.startswith('preds_')]
            # forecast_df['AE'] = forecast_df[ml_fc_cols].mean(axis=1)

        end_time = time.time()
        logger.info(
            "total time for {} forecast: {}"
                .format(forecast_start, end_time - start_time)
        )

        forecast_start = forecast_start + relativedelta(weeks=1)

        # weekly_fcst = pd.concat([weekly_fcst, forecast_df])

    return forecast_df


def drugs_to_comb_gps(sales_history, cfr_pr, schema, db):
    """map all drugs to its combination groups"""
    q_drug_comp_hash = f"""
              select "drug-id" as drug_id, "group" as comb_id
              from "{schema}"."drug-substitution-mapping" dsm
              """
    df_drug_comb = db.get_df(q_drug_comp_hash)
    sales_history = sales_history.merge(df_drug_comb, on="drug_id", how="left")
    sales_history = sales_history.groupby(["store_id", "comb_id", "sales_date"],
                                            as_index=False).agg({"net_sales_quantity": "sum"})

    cfr_pr = cfr_pr.merge(df_drug_comb, on="drug_id", how="left")
    cfr_pr = cfr_pr.groupby(["store_id", "comb_id", "shortbook_date"],
                            as_index=False).agg({"loss_quantity": "sum"})

    comb_list = df_drug_comb[comb_col].unique().tolist()

    return sales_history, cfr_pr, comb_list
