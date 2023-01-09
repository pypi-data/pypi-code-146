"""
A custom tuner class
"""
# Imports
import os
import sys
from typing import List, Union, Any, Dict
from pathlib import Path
import optuna
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
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

cwd = os.getcwd()
sys.path.append(cwd)

from core_of_theaisphere.tuning.tuners import ClassificationTuner


class CustomTuner(ClassificationTuner):
    def __init__(self, x: Union[pd.DataFrame, pd.Series],
                 y: Union[pd.DataFrame, pd.Series],
                 objective: Union[str, List],
                 save_loc: Union[str, Path],
                 metrics: Union[str, List] = 'roc_auc',
                 metrics_directions: Union[str, List] = 'maximize',
                 cv: Union[int, Any] = 5, group_col: str = None,
                 random_state: int = None):
        super().__init__(x, y, objective, save_loc, metrics, metrics_directions, cv, group_col, random_state)

    def custom_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for LogisticRegression

        Parameters
        ----------
        trial: optuna.trial.Trial
            a trial from optuna

        Returns
        -------
        metrics: Union[float, List[float]]
            metrics specified by the user
        """
        params = {
            'random_state': self.random_state,
            'max_iter': trial.suggest_int('max_iter', 100, 1000),
            'penalty': trial.suggest_categorical('penalty', ['l2', 'none']),
            'C': trial.suggest_float('C', 0.1, 5.0)
        }

        # Classifier
        lr = LogisticRegression(**params)
        scores = self.get_scores(estimator=lr)
        self.lr_params.append(lr.get_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    def custom_tune(self, optimization_config: Dict = None,
                    max_trials_callback: int = 1000):
        if self.objectives == 'custom':
            self.objective_fn = self.custom_objective
        else:
            self.load_objective_functions()

        # Optimization config
        if optimization_config is None:
            optimization_config = {
                'n_trials': 1000,
                'timeout': 3600
            }
        # Running the study
        trials_df, best_trial = self.create_study_run(
            self.objective_fn, max_trials_callback, self.directions,
            **optimization_config)
        trials_df['objective'] = self.objective_fn.__name__
        if isinstance(self.metrics, List):
            values = [c for c in trials_df.columns if 'value' in c]
            new_cols = dict(zip(values, self.metrics))
            trials_df.rename(columns=new_cols, inplace=True)
        else:
            trials_df.rename(columns={'value': self.metrics}, inplace=True)

        entire_df = self.create_results_df(self.objective_fn, trials_df)

        save_loc = self.save_loc / f"{self.objective_fn.__name__}"
        save_loc.mkdir(parents=True, exist_ok=True)
        entire_df.to_csv(f"{save_loc}/trials_df.csv", index=False)

        # with open(f"{save_loc}/best_trial.pickle",
        #           'wb') as pickle_file:
        #     pickle.dump(best_trial, pickle_file)

        logger.info(
            f"A DataFrame containing information on all trials and a pickle file with best_trial are "
            f"saved at -> '{save_loc}'")
        print("-" * self.terminal_size)

        if isinstance(self.metrics, List):
            for trial in best_trial:
                print(
                    f"Objective: {self.objective_fn.__name__}: best_trial_{best_trial.index(trial)}")
                logger.info(f"\n{trial}")
        else:
            print(f"Objective: {self.objective_fn.__name__}:")
            logger.info(f"\n{best_trial}\n")

        self.trials_df = entire_df
        self.best_trial = best_trial


# objectives_ex = 'custom'
# metrics_ex = ['roc_auc_score', 'accuracy_score', 'f1_score', 'fbeta_score', 'precision_score', 'recall_score']
# metrics_directions_ex = ['maximize', 'maximize', 'maximize', 'maximize', 'maximize', 'maximize']
# cv_ex = KFold(n_splits=3, shuffle=True, random_state=99)
#
# optimization_config_ex = {
#     'n_trials': 5,
#     'timeout': 3600
# }
# max_trials_callback_ex = 5

# # DF
# df = pd.read_csv("/Users/vickyparmar/data/kaggle/ds-salaries/train.csv")
# y_ex = pd.Series(np.where(df.salary_in_usd <= 10000, 0, 1), name='target')
# X_ex = df.drop(['salary_in_usd'], axis=1, inplace=False)
#
# cat_cols = ['employment_type', 'job_title', 'employee_residence', 'company_location',
#             'company_size']
# for col in cat_cols:
#     X_ex[col] = X_ex[col].astype('category')
#
# X_ex.drop(cat_cols, axis=1, inplace=True)
# ss = MinMaxScaler()
# X_ss = pd.DataFrame(ss.fit_transform(X_ex), columns=X_ex.columns)

# tuner = CustomTuner(x=X_ss, y=y_ex, objective=objectives_ex, save_loc='tmp/data', metrics=metrics_ex,
#                     metrics_directions=metrics_directions_ex, cv=cv_ex, random_state=99)
# # print(f"Instance successfully created.")
# tuner.custom_tune(optimization_config=optimization_config_ex, max_trials_callback=max_trials_callback_ex)
# print(tuner.multi_trials_df.head())
# print(tuner.multi_trials_df.shape)
# print(tuner.trials_df.head())
# print(tuner.trials_df.shape)
