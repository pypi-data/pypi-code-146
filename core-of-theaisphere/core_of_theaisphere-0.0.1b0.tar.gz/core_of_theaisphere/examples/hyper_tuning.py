"""
An example of how to use tuning module.
"""
# Imports
import os
import sys

cwd = os.getcwd()
sys.path.append(cwd)
import pandas as pd
import numpy as np
from core_of_theaisphere.tuning.tuners import ClassificationTuner, ParamsLoader, RegressionTuner
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import logging
from colorlog import ColoredFormatter

LOG_LEVEL = logging.DEBUG
logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter('%(log_color)s[%(levelname).1s %(log_color)s%(asctime)s] - %(log_color)s%(name)s - '
                             '%(reset)s%(message)s')
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(stream)

"""
Author: vickyparmar
File: hyper_tuning.py
Created on: 11-10-2022, Tue, 16:20:28

Last modified by: vickyparmar
Last modified on: 04-11-2022, Fri, 15:43:17
"""

# DF
df = pd.read_csv("/Users/vickyparmar/data/kaggle/ds-salaries/train.csv")
y = pd.Series(np.where(df.salary_in_usd <= 10000, 0, 1), name='target')
X = df.drop(['salary_in_usd'], axis=1, inplace=False)

cat_cols = ['employment_type', 'job_title', 'employee_residence', 'company_location',
            'company_size']
for col in cat_cols:
    X[col] = X[col].astype('category')

X.drop(cat_cols, axis=1, inplace=True)
ss = MinMaxScaler()
X_ss = pd.DataFrame(ss.fit_transform(X), columns=X.columns)

# Classification
objectives = ['lr', 'svm', 'xgb', 'rf', 'dt', 'cat', 'lgbm', 'sgd', 'gnb']
metrics = ['roc_auc_score', 'accuracy_score', 'f1_score', 'fbeta_score', 'precision_score', 'recall_score']
metrics_directions = ['maximize', 'maximize', 'maximize', 'maximize', 'maximize', 'maximize']
cv = KFold(n_splits=3, shuffle=True, random_state=99)

optimization_config = {
    'n_trials': 5,
    'timeout': 3600
}
max_trials_callback = 5

clf_tuner = ClassificationTuner(x=X_ss, y=y, objective=objectives, save_loc='tmp/data', metrics=metrics[:2],
                                metrics_directions=metrics_directions[:2], cv=cv, random_state=99)
# print(f"Instance successfully created.")
clf_tuner.tune_classifier(optimization_config=optimization_config, max_trials_callback=max_trials_callback)
logger.info(f"\n{clf_tuner.multi_trials_df.head()}")
logger.info(f"\n{clf_tuner.multi_trials_df.shape}")
logger.info(f"\n{clf_tuner.trials_df.head()}")
logger.info(f"\n{clf_tuner.trials_df.shape}")

# Regression
# objectives = ['ard']
# metrics = ['mse', 'mae', 'rmse', 'msle', 'r2', 'mape', 'smape']
# metrics_directions = ['minimize', 'minimize', 'minimize', 'minimize', 'minimize', 'minimize', 'minimize']
# cv = KFold(n_splits=3, shuffle=True, random_state=99)
#
# optimization_config = {
#     'n_trials': 5,
#     'timeout': 3600
# }
# max_trials_callback = 5
#
# reg_tuner = RegressionTuner(x=X_ss, y=y, objective=objectives, save_loc='tmp/data', metrics=metrics,
#                             metrics_directions=metrics_directions, cv=cv, random_state=99)
# # print(f"Instance successfully created.")
# reg_tuner.tune_regressor(optimization_config=optimization_config, max_trials_callback=max_trials_callback)
# logger.info(f"\n{reg_tuner.multi_trials_df.head()}")
# logger.info(f"\n{reg_tuner.multi_trials_df.shape}")
# logger.info(f"\n{reg_tuner.trials_df.head()}")
# logger.info(f"\n{reg_tuner.trials_df.shape}")

# Loading params
# pl = ParamsLoader(params_csv="tmp/data/rf_objective/trials_df.csv",
#                   column_name='roc_auc_score', save_loc="tmp/data/",
#                   fetch='max')
# # pl = ParamsLoader(params_csv="tmp/data/multi_trials_df.csv",
# #                   index_id=10, save_loc="tmp/data/")
# params = pl.load_params()
# logger.info(f"Params: \n{params}")
