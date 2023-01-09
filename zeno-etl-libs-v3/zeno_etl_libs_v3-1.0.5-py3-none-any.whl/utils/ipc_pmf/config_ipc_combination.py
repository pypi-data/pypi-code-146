platform_prod = 0 

store_col = 'store_id'
drug_col = 'drug_id'
comb_col = 'comb_id'
date_col = 'date'
target_col = 'actual_demand'
key_col = 'ts_id'
eol_cutoff = 13
mature_cutoff = 52
forecast_horizon = 4

flag_weather = 0
flag_seasonality_index = {
    'ctb': 0,
    'lgbm': 0,
    'xgb': 0
}

flag_sample_weights = {
    'ctb': 0,
    'lgbm': 0,
    'xgb': 0
}

num_shift_lag = 3

lags = [1]

add_lags_diff_flag = 1
lags_diff = [(1, 2)]

add_monthly_lags_flag = 1
# monthly_lags = [1, 2, 3, 6, 12]
monthly_lags = [1, 2, 3, 6]

rolling_time_feat = {
    'lags': [5, 13, 26, 53],
    'agg_func_dict': {'min', 'max', 'mean', 'median', 'std'}
}

ewma_lags = [4, 8]

# trend_lags = [13, 26, 53]
trend_lags = [13, 26]

perc_noise = [0.2, 0.5, 0.1]

# fc_cols = ['preds_xgb_rf_target','preds_cb_target','preds_lgb','AE', 'croston_fcst']
# models = ['croston', 'prophet', 'ETS', 'MA', 'AE_ts', 'lgbm']

run_ml_flag = 1
runs_ts_flag = 1
run_ts_4w_agg_flag = 1
run_ml_4w_agg_flag = 0
models_un_agg = ['ETS_Auto', 'ETS_12w', 'MA', 'LGBM']
models_agg = ['ETS_4w_agg', 'LGBM_4w_agg']
local_testing = 0
models = ['LGBM']
default_model = 'LGBM'

# lgbm_params = {
# 'objective': 'regression_l1',
# 'learning_rate': 0.01,
# 'max_bin': 404,
# 'num_leaves': 1000,
# 'lambda_l1': 0.003657033571790936,
# 'lambda_l2': 1.203092568431234,
# 'cat_l2': 5.192935907692467,
# 'cat_smooth': 9.67794952387374,
# 'feature_fraction': 0.997997647335764,
# 'bagging_fraction': 0.9162909273820165,
# 'bagging_freq': 7,
# 'min_data_in_leaf': 33,
# 'min_child_samples': 5,
# 'metric': 'rmse',
# 'boosting_type': 'gbdt',
# 'max_depth': -1,
# 'random_state': 42,
# 'force_row_wise': True,
# 'verbose': -1,
# 'num_iterations': 1500
# }

# fc_cols = ['croston_fcst', 'ETS_fcst', 'ma_fcst','prophet_fcst', 'AE_ts_fcst']

# cols_rename = {
#     'preds_xgb_rf_target': 'fcst_1',
#     'preds_cb_target': 'fcst_2', 
#     'preds_lgb':'fcst_3',
#     'AE':'fcst_4',
#     'croston_fcst':'fcst_5'
# }

# cols_rename = {
#     'croston_fcst': 'fcst_1',
#     'ETS_fcst': 'fcst_2', 
#     'ma_fcst':'fcst_3',
#     'prophet_fcst':'fcst_4',
#     'AE_ts_fcst':'fcst_5'
# }

