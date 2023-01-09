"""
Hyper-parameter tuning with Optuna
"""

# Imports
import os
import random
from typing import List, Any, Union, Dict, Tuple
import pickle
from pathlib import Path
from tqdm.auto import tqdm
import numpy as np
import pandas as pd
import optuna
from optuna.samplers import TPESampler
from optuna.trial import FrozenTrial
from optuna.study import MaxTrialsCallback
from optuna.trial import TrialState
from sklearn.model_selection import StratifiedKFold, \
    StratifiedGroupKFold, KFold
from xgboost import XGBClassifier
from tensorflow.python.platform import build_info
from lightgbm.sklearn import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression, SGDClassifier, \
    RidgeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score, \
    fbeta_score, precision_score, recall_score

import logging
from colorlog import ColoredFormatter

LOG_LEVEL = logging.DEBUG
logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(
    '%(log_color)s[%(levelname).1s %(log_color)s%(asctime)s] - %(log_color)s%(name)s - '
    '%(message)s')
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(stream)

"""
Author: vickyparmar
File: tuners.py
Created on: 07-10-2022, Fri, 2:06:39

Last modified by: vickyparmar
Last modified on: 14-10-2022, Fri, 14:10:58
"""


# [  ] ToDo: CustomObjectiveFunction
# [  ] ToDo: CustomMetricsFunction
# [  ] ToDo: feature_map for SVC --> as separate objective functions-set
# [v] ToDo: modify suggest_categorical in dynamic space (temp-fix -> random.choice)
# [v] ToDo: Documentation including `Notes` and README.md
# [x] A function to read the csv and extract the parameters and return a dict
# [x] Add attributes to the list as well.
# [x] Rename 'values_*' to reflect the correct metrics
# [x] Check if objective function(s) exists
# [x] Loading objective functions
# [x] Calculate Metrics
# [x] Optimization Directions
# [x] Running Optuna Study and saving the results


# class TuneClassifier
class TuneClassifier:
    """
                Performing a hyperparameter search for
                different classifiers using
                `OPTUNA
                <https://github.com/optuna/optuna>`_.
                For a detailed example on how to use
                TuneClassifier, check `this
                <__init__.py>`_ out.

                Parameters
                ----------
                x: Union[pd.DataFrame, pd.Series]
                    input data
                y: Union[pd.DataFrame, pd.Series]
                    target data
                objective: Union[str, List]
                    objective function (Classifier to use)
                save_loc: Union[str, Path]
                    location to save the end results
                metrics: Union[str, List]
                    metrics to optimize
                metrics_directions: Union[str, List]
                    direction to optimize the metrics
                    (maximize or minimize)
                cv: Union[int, Any]
                    either an integer for StratifiedKFold
                    or StratifiedGroupKFold or any
                    cv method that has split(X,y,groups)
                group_col: str
                    name of the group column in case of
                    StratifiedGroupKFold or similar
                random_state: int
                    random initializing state for
                    reproducibility

                Attributes
                ----------
                trials_df: pd.DataFrame
                    a DataFrame for all trials (in case of
                    single objective)
                best_trial: FrozenTrial
                    a trial with all its attributes (single
                    objective)
                multi_trials_df: pd.DataFrame
                    a DataFrame for all trials (in case of
                    multiple objectives concatinated
                    below one another)
                best_trials: Dict
                    a dictionary of trials with all their
                    attributes (multiple objectives)

                Methods
                -------
                tune(optimization_config: Dict | None,
                max_trials_callback: int)
                    takes in the configuration for
                    study.optimize(objective,
                    optimization_config) and tunes the
                    objective function.
                    `optimization_config` must be a Dict
                    and the allowed parameters can be
                    found `here
                    <https://optuna.readthedocs.io/en/
                    stable/reference/generated/optuna.
                    study.Study.html#
                    optuna.study.Study.optimize>`_

                Raises
                ------
                ValueError
                    Raised when length of `metrics`
                    do not match the length of
                     `metrics_directions`
                TypeError
                    Raised when either objective or
                    metrics contains an unsupported type

                See Also
                --------
                othermodule: Other module to see.

                Notes
                -----
                In progres...

                Examples
                --------
                >>> objective = 'lr'
                >>> metrics = 'roc_auc_score'
                >>> direction = 'maximize'
                >>> cv = KFold(n_splits=3,
                                         shuffle=True,
                                         random_state=99)
                >>> optimization_config = {
                            'n_trials': 5,
                            'timeout': 3600
                        }
                >>> max_trials_callback = 5
                >>> x = pd.DataFrame() # your df
                >>> y = pd.DataFrame() # your target
                >>> tuner = TuneClassifier(x, y,
                                                     objective],
                                                     'tmp/data',
                                                     metrics,
                                                     direction,
                                                     cv,
                                                     42)
                >>> tuner.tune(optimization_config,
                                        max_trials_callback)
                """

    # noinspection PyTypeChecker
    def __init__(self, x: Union[pd.DataFrame, pd.Series],
                 y: Union[pd.DataFrame, pd.Series],
                 objective: Union[str, List],
                 save_loc: Union[str, Path],
                 metrics: Union[str, List] = 'roc_auc',
                 metrics_directions: Union[str, List] = 'maximize',
                 cv: Union[int, Any] = 5, group_col: str = None,
                 random_state: int = None):
        self.objectives, self.metrics = self.integrity_check(objective,
                                                             metrics)
        logger.info(f"Objective functions: {self.objectives}")
        logger.info(f"Metrics: {self.metrics}")
        self.directions = metrics_directions
        if isinstance(self.directions, List):
            # noinspection PyTypeChecker
            if len(metrics_directions) != len(self.metrics):
                logger.error(
                    f"Length missmatch. If you provided the same lengths for `metrics` and `metrics_directions`,"
                    f"check if there are duplicates in `metrics`. Duplicates are removed as a part of integrity check."
                    f"Hence, it can lead to a length missmatch.")
                raise ValueError(
                    f"`metrics` and `metrics_directions` must have the same length."
                )
        # noinspection PyTypeChecker
        self.x, self.y = x, y
        self.unique_length = self.y.nunique()
        self.objective_fn = None
        # noinspection PyTypeChecker
        self.save_loc = Path(save_loc)
        self.random_state = random_state
        self.cv = cv
        self.group_col = group_col
        self.cuda_build = build_info.build_info['is_cuda_build']
        self.rf_params = []
        self.lr_params = []
        self.svm_params = []
        self.xgb_params = []
        self.dt_params = []
        self.cat_params = []
        self.lgbm_params = []
        self.sgd_params = []
        self.gnb_params = []
        self.ridge_params = []
        self.trials_df = pd.DataFrame()
        self.best_trial = None
        self.multi_trials_df = pd.DataFrame()
        self.best_trials = {}
        # noinspection PyBroadException
        try:
            self.terminal_size = os.get_terminal_size().columns
        except Exception:
            self.terminal_size = 100

    # Create and run Optuna Study
    def create_study_run(self, objective: Any, max_trials_callback: int,
                         direct: Union[str, List[str]],
                         **kwargs) -> Tuple[pd.DataFrame, Union[FrozenTrial, List]]:
        """
        Creating an Optuna.study.Study and
        running study.optimize(*).

        Parameters
        ----------
        objective: Any
            Objective function. A callable function
            that takes in `optuna.trial.Trial` as input
            and returns either a float or multiple
            float values (usually scores or losses) to
            be optimized.
        max_trials_callback: int
            When running multiple studies, this will
            be the total number of trials for all
            the studies combined.
        direct: Union[str, List[str]]
            Direction(s) in which the score(s)/loss(es)
            will be optimized
        kwargs: Dict
            Configuration parameters for `optuna.
            study.Study.optimize`

        Returns
        -------
        tuple: Tuple[pd.DataFrame, Union[FrozenTrial, List]]
            Returns a tuple containing a DataFrame
            with all trials and a FrozenTrial containing
            all trial parameters.
        """
        print('='*self.terminal_size)
        sampler = TPESampler(seed=self.random_state,
                             n_startup_trials=2, multivariate=True,
                             group=True)
        if isinstance(direct, str):
            study = optuna.create_study(direction=direct,
                                        pruner=optuna.pruners.MedianPruner(),
                                        sampler=sampler,
                                        study_name=f"{objective.__name__}")
        else:
            study = optuna.create_study(directions=direct,
                                        pruner=optuna.pruners.MedianPruner(),
                                        sampler=sampler,
                                        study_name=f"{objective.__name__}")
        optuna.logging.enable_default_handler()
        max_trials_callback = MaxTrialsCallback(max_trials_callback,
                                                states=(
                                                    TrialState.COMPLETE,))
        study.optimize(objective, callbacks=[max_trials_callback],
                       **kwargs)
        trials_df = study.trials_dataframe()
        if isinstance(direct, List):
            best_trial = study.best_trials
        else:
            best_trial = study.best_trial
        return trials_df, best_trial

    # Running one or multiple objectives
    def tune(self, optimization_config: Dict = None,
             max_trials_callback: int = 1000):
        """
        Taking the given parameters and tuning
        the objective function(s).

        Parameters
        ----------
        optimization_config: Dict | None
            Configuration parameters for optuna.
            study.Study.optimize. Default: None
            i.e. optimization_config = {
                'n_trials': 1000,
                'timeout': 3600
            }
        max_trials_callback: int
            When running multiple studies, this will
            be the total number of trials for all
            the studies combined. Default: 1000

        Returns
        -------
        None
        """
        # Loading objective functions
        self.load_objective_functions()
        # Optimization config
        if optimization_config is None:
            optimization_config = {
                'n_trials': 1000,
                'timeout': 3600
            }
        # Running the study
        if isinstance(self.objective_fn, list):
            best_trials = {}
            for objective in tqdm(self.objective_fn,
                                  desc="Running multiple objective functions",
                                  total=len(self.objective_fn)):
                trials_df, best_trial = self.create_study_run(objective,
                                                              max_trials_callback,
                                                              self.directions,
                                                              **optimization_config)

                self.best_trials[objective.__name__] = best_trials

                trials_df['objective'] = objective.__name__
                if isinstance(self.metrics, List):
                    values = [c for c in trials_df.columns if 'value' in c]
                    new_cols = dict(zip(values, self.metrics))
                    trials_df.rename(columns=new_cols, inplace=True)
                    final_cols = self.metrics.copy()
                    final_cols.append('objective')
                else:
                    trials_df.rename(columns={'value': self.metrics}, inplace=True)
                    final_cols = [self.metrics, 'objective']

                self.multi_trials_df = pd.concat(
                    [self.multi_trials_df, trials_df[final_cols]],
                    axis=0)

                entire_df = self.create_results_df(objective, trials_df)
                save_loc = self.save_loc / f"{objective.__name__}"
                save_loc.mkdir(parents=True, exist_ok=True)

                entire_df.to_csv(f"{save_loc}/trials_df.csv", index=False)

                # with open(f"{save_loc}/best_trial.pickle",
                #           'wb') as pickle_file:
                #     pickle.dump(best_trial, pickle_file)

                logger.info(
                    f"\nA DataFrame containing information on all trials and a pickle file with best_trial are"
                    f"saved at {save_loc}\n")

                best_trials[f"{objective.__name__}"] = best_trial

            print("-" * self.terminal_size)
            logger.info(
                f"\nHere are the best trials for all your objective functions:\n")
            for o, t in best_trials.items():
                print("-" * self.terminal_size)
                if isinstance(self.metrics, List):
                    for m in t:
                        print(
                            f"Objective: {o}: best_trial_{t.index(m)}")
                        logger.info(f"\n{m}\n")
                else:
                    print(f"Objective: {o}: ")
                    logger.info(f"\n{t}\n")

        else:
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

    # Importing the objective functions from objective scripts and passing them on to the _tune
    def load_objective_functions(self):
        """
        Mapping user keywords for objectives with
        predefined objective functions. Class
        attribute objective_fn is updated accordingly

        Returns
        -------
        None
        """
        function_map = {
            'lr': self.lr_objective,
            'svm': self.svm_objective,
            'xgb': self.xgb_objective,
            'rf': self.rf_objective,
            'dt': self.dt_objective,
            'cat': self.cat_objective,
            'lgbm': self.lgbm_objective,
            'sgd': self.sgd_objective,
            # 'ridge': self.ridge_objective,
            'gnb': self.gnb_objective
        }
        if isinstance(self.objectives, str):
            self.objective_fn = function_map[self.objectives]
        else:
            self.objective_fn = []
            for obj in self.objectives:
                self.objective_fn.append(function_map[obj])

    # Method to calculate the specified score
    def calculate_metrics(self, estimator: Any,
                          x: Union[pd.DataFrame, pd.Series, np.ndarray],
                          y: Union[
                              pd.DataFrame, pd.Series, np.ndarray]) -> \
            Union[float, List[float]]:
        """
        Calculating score(s) / loss(es) and returning
        what the user asked for with a trained
        estimator, input data, and ground truth.

        Parameters
        ----------
        estimator: Any
            a trained or fitted estimator
        x: Union[pd.DataFrame, pd.Series,
                np.ndarray]
            input_data
        y: Union[pd.DataFrame, pd.Series,
                np.ndarray]
            target data

        Returns
        -------
        metrics: Union[float, List[float]]
            score(s) / loss(es) specified by the user
        """
        roc_auc = self.get_roc_auc(estimator, x, y)
        predictions = estimator.predict(x)
        accuracy = accuracy_score(y_true=y, y_pred=predictions)
        f1 = f1_score(y_true=y, y_pred=predictions)
        fbeta = fbeta_score(y_true=y, y_pred=predictions, beta=0.5)
        precision = precision_score(y_true=y, y_pred=predictions)
        recall = recall_score(y_true=y, y_pred=predictions)
        # Metrics mapping
        metrics_map = {
            'roc_auc_score': roc_auc,
            'accuracy_score': accuracy,
            'f1_score': f1,
            'fbeta_score': fbeta,
            'precision_score': precision,
            'recall_score': recall
        }
        if isinstance(self.metrics, str):
            return metrics_map[self.metrics]
        return [metrics_map[m] for m in self.metrics]

    # Calculate scores with CV
    def get_scores(self, estimator: Any) -> List:
        """
        Takes in an estimator, performs
        cross-validation and returns the
        score(s) / loss(es)

        Parameters
        ----------
        estimator: Any
            any estimator that has a .fit, .predict,
            and .predict_proba methods.

        Returns
        -------
        metrics: List
            returns the user specified metrics
        """
        scores = []
        if self.group_col is not None:
            if isinstance(self.cv, int):
                cv = StratifiedGroupKFold(n_splits=self.cv,
                                          random_state=self.random_state,
                                          shuffle=True)
            else:
                cv = self.cv
            for train, val in cv.split(self.x, self.y,
                                       self.x[self.group_col]):
                x_train, y_train = self.x.loc[train], self.y.loc[train]
                x_val, y_val = self.x.loc[val], self.y.loc[val]
                estimator.fit(x_train, y_train)
                scores.append(
                    self.calculate_metrics(estimator=estimator, x=x_val,
                                           y=y_val))
        else:
            if isinstance(self.cv, int):
                cv = StratifiedKFold(n_splits=self.cv,
                                     random_state=self.random_state,
                                     shuffle=True)
            else:
                cv = self.cv
            for train, val in cv.split(self.x, self.y):
                x_train, y_train = self.x.loc[train], self.y.loc[train]
                x_val, y_val = self.x.loc[val], self.y.loc[val]
                estimator.fit(x_train, y_train)
                scores.append(
                    self.calculate_metrics(estimator=estimator, x=x_val,
                                           y=y_val))
        return scores

    # LogisticRegression
    def lr_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
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
            'penalty': trial.suggest_categorical('penalty', ['l1', 'l2',
                                                             'elasticnet']),
            'C': trial.suggest_float('C', 0.1, 5.0)
        }
        # Selecting 'SOLVER' parameter based on labels and penalties
        if self.unique_length > 2:
            if params['penalty'] == 'l1':
                params['solver'] = random.choice(['liblinear', 'saga'])
            elif params['penalty'] == 'l2':
                params['solver'] = random.choice(
                    ['newton-cg', 'sag', 'saga', 'lbfgs'])
            else:
                params['solver'] = 'saga'
        else:
            if params['penalty'] == 'l1':
                params['solver'] = random.choice(['liblinear', 'saga'])
            elif params['penalty'] == 'l2':
                params['solver'] = random.choice(
                    ['newton-cg', 'sag', 'saga', 'lbfgs', 'liblinear'])
            else:
                params['solver'] = 'saga'
        # Specifying 'L1_Ratio' parameter only if 'ELASTICNET' is used as penalty
        if params['penalty'] == 'elasticnet':
            params['l1_ratio'] = trial.suggest_float('l1_ratio', 0.1,
                                                     0.9)

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

    # SVMClassifier
    def svm_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for SupportVectorMachine
        - SVC classifier.

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
            'kernel': trial.suggest_categorical('kernel',
                                                ['linear', 'poly',
                                                 'rbf', 'sigmoid']),
            'probability': True,
        }
        # Selecting degree
        if params['kernel'] == 'poly':
            params['degree'] = trial.suggest_int('degree', 2, 7)
        if params['kernel'] in ['rbf', 'poly', 'sigmoid']:
            params['gamma'] = random.choice(['scale', 'auto'])
        else:
            params['gamma'] = 'auto'
        if params['kernel'] in ['poly', 'sigmoid']:
            params['coef0'] = trial.suggest_float('coef0', 0.0, 1.0)

        # Classifier
        svc = SVC(**params)
        scores = self.get_scores(estimator=svc)
        self.svm_params.append(svc.get_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    # XGBoost
    def xgb_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for XGBoost.

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
            'use_label_encoder': False,
            'random_state': self.random_state,
            'n_estimators': trial.suggest_int('n_estimators', 100, 1000, 50),
            'max_depth': trial.suggest_int('max_depth', 2, 9),
            'learning_rate': trial.suggest_float('learning_rate', 1e-5, 0.1),
            'booster': trial.suggest_categorical('booster', ['gbtree', 'gblinear', 'dart']),
            'reg_alpha': trial.suggest_float('reg_alpha', 0, 1),
            'reg_lambda': trial.suggest_float('reg_lambda', 0, 1)
        }
        # Enabling 'gpu_hist' if 'CUDA' is available
        if self.cuda_build:
            params['tree_method'] = trial.suggest_categorical(
                'tree_method', ['approx', 'gpu_hist'])
        else:
            params['tree_method'] = trial.suggest_categorical(
                'tree_method', ['approx', 'hist'])
        # Checking for categorical columns and finding minimum number of categories to onehot and maximum
        cat_cols = self.x.select_dtypes('category').columns.tolist()
        if len(cat_cols) >= 1:
            max_ohc = sum([self.x[c].nunique() for c in cat_cols])
            min_ohc = min(10, min([self.x[c].nunique() for c in cat_cols]))
            params['enable_categorical'] = True
            params['max_cat_to_onehot'] = trial.suggest_int('max_cat_to_onehot',
                                                            min_ohc, max_ohc)

            logger.warning(f"Found categorical_columns:\n{cat_cols}")
            logger.warning(
                f"Enabling OneHotEncoding with different number of one hot features."
                f"Minimum {min_ohc} features, Maximum {max_ohc}")

        # Classifier
        xgb = XGBClassifier(**params)
        scores = self.get_scores(estimator=xgb)
        self.xgb_params.append(xgb.get_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    # RandomForest
    def rf_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for RandomForest

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
            'n_estimators': trial.suggest_int('n_estimators', 100, 1000, 50),
            'max_depth': trial.suggest_int('max_depth', 2, 9),
            'criterion': trial.suggest_categorical('criterion', ['gini', 'entropy', 'log_loss']),
            'min_samples_split': trial.suggest_float('min_samples_split', 0.0, 0.3),
            'min_samples_leaf': trial.suggest_float('min_samples_leaf', 0.0, 0.15),
            'max_features': 'sqrt',
            'bootstrap': trial.suggest_categorical('bootstrap', [True, False]),
            'class_weight': 'balanced',
            'ccp_alpha': trial.suggest_float('ccp_alpha', 1e-3, 0.5)
        }
        # OutOfBag sample
        if params['bootstrap']:
            params['oob_score'] = True
            params['class_weight'] = 'balanced_subsample'
            params['max_samples'] = 0.85

        # Classifier
        rf = RandomForestClassifier(**params)
        scores = self.get_scores(estimator=rf)
        self.rf_params.append(rf.get_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    # DecisionTrees
    def dt_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for DecisionTrees.

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
            'max_depth': trial.suggest_int('max_depth', 2, 9),
            'criterion': trial.suggest_categorical('criterion',
                                                   ['gini', 'entropy',
                                                    'log_loss']),
            'splitter': trial.suggest_categorical('splitter',
                                                  ['best', 'random']),
            'min_samples_split': trial.suggest_float(
                'min_samples_split', 0.0, 0.3),
            'min_samples_leaf': trial.suggest_float('min_samples_leaf',
                                                    0.0, 0.15),
            'max_features': 'sqrt',
            'class_weight': 'balanced',
            'ccp_alpha': trial.suggest_float('ccp_alpha', 1e-3, 0.5),
        }
        # Classifier
        dt = DecisionTreeClassifier(**params)
        scores = self.get_scores(estimator=dt)
        self.dt_params.append(dt.get_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    # CatBoost
    def cat_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for CATBoost.

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
            'verbose': False,
            'random_seed': self.random_state,
            'iterations': trial.suggest_int('n_estimators', 100, 1000,
                                            step=50),
            'learning_rate': trial.suggest_float('learning_rate', 0.01,
                                                 1.),
            'l2_leaf_reg': trial.suggest_float('l2_leaf_reg', 0.1, 10.),
            'use_best_model': False,
            'max_depth': trial.suggest_int('max_depth', 2, 9),
            'grow_policy': trial.suggest_categorical('grow_policy',
                                                     ['SymmetricTree',
                                                      'Depthwise',
                                                      'Lossguide'])
        }
        # Checking for categorical columns and finding minimum number of categories to onehot and maximum
        cat_cols = self.x.select_dtypes('category').columns.tolist()
        if len(cat_cols) >= 1:
            max_ohc = sum([self.x[c].nunique() for c in cat_cols])
            min_ohc = min(10,
                          min([self.x[c].nunique() for c in cat_cols]))
            params['cat_features'] = np.array(cat_cols)
            params['one_hot_max_size'] = trial.suggest_int(
                'max_cat_to_onehot', min_ohc, max_ohc)

            logger.warning(f"Found categorical_columns:\n{cat_cols}")
            logger.warning(
                f"Enabling OneHotEncoding with different number of one hot features."
                f"Minimum {min_ohc} features, Maximum {max_ohc}")
        # Score-Function
        if self.cuda_build:
            if params['grow_policy'] == 'Lossguide':
                params['score_function'] = random.choice(
                    ['L2', 'NewtonL2'])
            else:
                params['score_function'] = random.choice(
                    ['Cosine', 'L2', 'NewtonL2', 'NewtonCosine'])
        else:
            if params['grow_policy'] == 'Lossguide':
                params['score_function'] = random.choice(['L2'])
            else:
                params['score_function'] = random.choice(
                    ['Cosine', 'L2'])
        # Classifier
        cat = CatBoostClassifier(**params)
        scores = self.get_scores(estimator=cat)
        self.cat_params.append(cat.get_all_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    # LightGBM
    def lgbm_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for LightGBM.

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
            'importance_type': 'gain',
            'boosting_type': trial.suggest_categorical('boosting_type',
                                                       ['rf', 'gbdt',
                                                        'dart',
                                                        'goss']),
            'num_leaves': trial.suggest_int('num_leaves', 2, 100, 2),
            'max_depth': trial.suggest_int('max_depth', 2, 9),
            'learning_rate': trial.suggest_float('learning_rate', 1e-5,
                                                 0.1),
            'n_estimators': trial.suggest_int('n_estimators', 100,
                                              1000),
            'reg_alpha': trial.suggest_float('reg_alpha', 0, 1),
            'reg_lambda': trial.suggest_float('reg_lambda', 0, 1)
        }
        if params['boosting_type'] != 'goss':
            params['subsample'] = 0.9
            params['subsample_freq'] = int(params['n_estimators'] / 2)
        unique_labels = self.y.unique()
        value_counts = self.y.value_counts()
        if self.unique_length == 2:
            ratio = value_counts.iloc[0] / self.y.shape[0]
            if 0.49 <= ratio <= 0.51:
                params['is_unbalanced'] = False
            else:
                params['is_unbalanced'] = True
        else:
            balanced = self.y.shape[0] / self.unique_length
            lower = balanced - 0.1
            higher = balanced + 0.1
            for ul in unique_labels:
                ratio = value_counts[ul] / self.y.shape[0]
                if lower > ratio > higher:
                    params['is_unbalanced'] = True
                    break
                else:
                    params['is_unbalanced'] = False
        # Classifier
        lgbm = LGBMClassifier(**params)
        scores = self.get_scores(estimator=lgbm)
        self.lgbm_params.append(lgbm.get_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    # SGDClassifier
    def sgd_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for SGD -
        StochasticGradientDescent

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
            'loss': trial.suggest_categorical('loss',
                                              ['hinge', 'log_loss',
                                               'modified_huber',
                                               'squared_hinge',
                                               'perceptron']),
            'penalty': trial.suggest_categorical('penalty', ['l1', 'l2',
                                                             'elasticnet']),
            'alpha': trial.suggest_float('alpha', 1e-3, 1),
            'learning_rate': trial.suggest_categorical('learning_rate',
                                                       ['optimal',
                                                        'adaptive',
                                                        'constant',
                                                        'invscaling']),
            'early_stopping': True
        }
        # ETA0 and POWER_T
        if params['learning_rate'] == 'constant':
            params['eta0'] = 0.01
        else:
            params['eta0'] = 0.1
        if params['learning_rate'] == 'invscaling':
            params['power_t'] = trial.suggest_float('power_t', -1.0,
                                                    1.0)

        # Classifier
        sgd = SGDClassifier(**params)
        scores = self.get_scores(estimator=sgd)
        self.sgd_params.append(sgd.get_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    # RidgeClassifier
    def ridge_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for RidgeClassifier.

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
            'alpha': trial.suggest_float('alpha', 0.01, 1),
            'solver': trial.suggest_categorical('solver',
                                                ['auto', 'svd',
                                                 'cholesky', 'lsqr',
                                                 'sparse_cg', 'sag',
                                                 'saga', 'lbfgs']),
            'class_weight': 'balanced'
        }
        # Positive coefficients
        if params['solver'] == 'lbfgs':
            params['positive'] = True

        # Classifier
        ridge = RidgeClassifier(**params)
        scores = self.get_scores(estimator=ridge)
        self.ridge_params.append(ridge.get_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    # GaussianNB
    def gnb_objective(self, trial: optuna.trial.Trial) -> Union[float, List[float]]:
        """
        Objective function for GaussianNB.

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
            'var_smoothing': trial.suggest_float('var_smoothing', 1e-10,
                                                 0.1, )
        }
        # Classifier
        gnb = GaussianNB(**params)
        scores = self.get_scores(estimator=gnb)
        self.gnb_params.append(gnb.get_params())
        if isinstance(self.metrics, List):
            mean_score = np.mean(scores, axis=0).tolist()
        else:
            mean_score = np.mean(scores)
        # noinspection PyTypeChecker
        return mean_score

    # Checking the inputs
    @staticmethod
    def verify_input(objective: Union[str, List], metrics: Union[str, List]) -> None:
        """
        Verifying whether the given inputs are in
        predefined inputs.

        Parameters
        ----------
        objective: Union[str, List]
            objective functions to check
        metrics: Union[str, List]
            metrics to check

        Returns
        -------
        None
        """
        predefined_functions = ['lr', 'svm', 'xgb', 'rf', 'dt', 'cat',
                                'lgbm', 'sgd', 'gnb']  # 'ridge'
        predefined_metrics = ['roc_auc_score', 'accuracy_score',
                              'f1_score', 'fbeta_score',
                              'precision_score', 'recall_score']

        if isinstance(objective, str):
            if objective in predefined_functions:
                # logger.info(f"Found only one objective function to optimize.")
                pass
            else:
                logger.error(
                    f"Provided objective function not supported.")
                raise ValueError(
                    f" Please choose one or more from the predefined list: \n {predefined_functions}"
                )
        elif isinstance(objective, List):
            if set(objective).issubset(set(predefined_functions)):
                # logger.info(f"Multiple objective functions found.")
                pass
            else:
                logger.error(
                    f"One or more objective functions provided, are not supported.")
                raise ValueError(
                    f" Please choose one or more from the predefined list: \n {predefined_functions}"
                )

        if isinstance(metrics, str):
            if metrics in predefined_metrics:
                # logger.info(f"Found only one metrics to optimize.")
                pass
            else:
                logger.error(f"Provided metrics not supported.")
                raise ValueError(
                    f" Please choose one or more from the predefined list: \n {predefined_functions}"
                )
        elif isinstance(metrics, List):
            if set(metrics).issubset(set(predefined_metrics)):
                # logger.info(f"Multiple metrics found.")
                pass
            else:
                logger.error(
                    f"One or more metrics provided, are not supported.")
                raise ValueError(
                    f" Please choose one or more from the predefined list: \n {predefined_functions}"
                )

    # Instance checker
    @staticmethod
    def verify_input_types(objective: Union[str, List], metrics: Union[str, List]) -> None:
        """
        Verifying whether the given inputs are of the
        correct type

        Parameters
        ----------
        objective: Union[str, List]
            objective functions to check
        metrics: Union[str, List]
            metrics to check

        Returns
        -------
        None
        """
        if isinstance(objective, str):
            logger.info(
                f"Found only one objective function to optimize.")
        elif isinstance(objective, List):
            passed = 0
            for obj in objective:
                if isinstance(obj, str):
                    passed += 1
                else:
                    logger.error(
                        f"Currently the parameter `objective` only supports str or List[str].")
                    raise TypeError(
                        f"One or more elements of your list has type: {type(obj)}"
                    )
            if len(objective) == passed:
                logger.info(f"Found multiple objectives.")
        else:
            logger.error(
                f"Currently the parameter `objective` only supports str or List[str].")
            raise TypeError(
                f"You passed in {type(objective)}"
            )

        if isinstance(metrics, str):
            logger.info(f"Found only one metric to optimize.")
        elif isinstance(metrics, List):
            for met in metrics:
                if isinstance(met, str):
                    pass
                else:
                    logger.error(
                        f"Currently the parameter `metrics` only supports str or List[str].")
                    raise TypeError(
                        f"One or more elements of your list has type: {type(met)}"
                    )
            logger.info(f"Found multiple metrics.")
        else:
            logger.error(
                f"Currently the parameter `metrics` only supports str or List[str].")
            raise TypeError(
                f"You passed in {type(metrics)}"
            )

    # Checking integrity of the inputs
    def integrity_check(self, objective: Union[str, List],
                        metrics: Union[str, List]) -> Tuple[Union[str, List[str]], Union[str, List[str]]]:
        """
        Checking the integrity of the inputs.
        Specifically, objective and metrics.

        Parameters
        ----------
        objective: Union[str, List]
            objective functions to check
        metrics: Union[str, List]
            metrics to check

        Returns
        -------
        tuple: Tuple[Union[str, List[str]],
                    Union[str, List[str]]]
            a tuple of clean objective functions and
            metrics
        """
        logger.info(f"PERFORMING INPUT INTEGRITY CHECK...")
        self.verify_input_types(objective, metrics)
        self.verify_input(objective, metrics)
        new_objective, new_metrics = objective, metrics
        if isinstance(objective, List):
            new_objective = list(set(objective))
            if len(new_objective) == 1:
                new_objective = new_objective[0]
            if len(set(objective)) != len(objective):
                logger.warning(
                    f"Duplicated objective functions found. Each function will only be calculated once.")
        if isinstance(metrics, List):
            new_metrics = list(set(metrics))
            if len(new_metrics) == 1:
                new_metrics = objective[0]
            if len(set(objective)) != len(objective):
                logger.warning(
                    f"Duplicated metrics found. Each metric will only be calculated once.")
        logger.info(f"INTEGRITY CHECK SUCCESSFUL...")
        return new_objective, new_metrics

    # Checking if roc_auc_score is available
    @staticmethod
    def get_roc_auc(estimator: Any,
                    x: Union[pd.DataFrame, pd.Series, np.ndarray],
                    y: Union[
                        pd.DataFrame, pd.Series, np.ndarray]) -> float:
        """
        Checking if the estimator supports
        `predict_proba`. If not, `np.nan` is
        returned as probability.

        Parameters
        ----------
        estimator: Any
            a trained or fitted estimator
        x: Union[pd.DataFrame, pd.Series,
                np.ndarray]
            input_data
        y: Union[pd.DataFrame, pd.Series,
                np.ndarray]
            target data

        Returns
        -------
        roc_auc: float
            roc_auc_score for the estimator
        """
        # if estimator.__class__ == RidgeClassifier:
        #     logger.warning(f"ROC_AUC_SCORE not available for RidgeClassifier.")
        #     roc_auc = np.nan
        if estimator.__class__ == SGDClassifier:
            params = estimator.get_params()
            if params['loss'] not in ['log_loss', 'modified_huber']:
                roc_auc = np.nan
                logger.warning(
                    f"For SGDClassifier, probability estimates are only available when `loss` parameter"
                    f"is either 'log_loss' or 'modified_huber'")
            else:
                probabilities = estimator.predict_proba(x)
                roc_auc = roc_auc_score(y_true=y,
                                        y_score=probabilities[:, 1])
        else:
            probabilities = estimator.predict_proba(x)
            roc_auc = roc_auc_score(y_true=y,
                                    y_score=probabilities[:, 1])

        return roc_auc

    # Creating a params DataFrame
    def create_results_df(self, objective_fn: Any,
                          trials_df: pd.DataFrame) -> pd.DataFrame:
        """
        Creating a DataFrame with all params for the
        estimator

        Parameters
        ----------
        objective_fn: Any
            objective function running
        trials_df: pd.DataFrane
            trials_df received from Optuna

        Returns
        -------
        results_df: pd.DataFrame
            a resulting df with all estimator as well as
            trial parameters
        """
        name = objective_fn.__name__
        if 'rf' in name:
            rf_df = pd.DataFrame(self.rf_params)
            new_cols = [f"params_{c}" for c in rf_df.columns]
            rf_df.columns = new_cols
            params_cols = [col for col in trials_df.columns if col.startswith('params')]
            trials_df.drop(params_cols, axis=1, inplace=True)
            rf_df = pd.concat([trials_df, rf_df], axis=1)
            return rf_df
        elif 'lr' in name:
            lr_df = pd.DataFrame(self.lr_params)
            new_cols = [f"params_{c}" for c in lr_df.columns]
            lr_df.columns = new_cols
            params_cols = [col for col in trials_df.columns if col.startswith('params')]
            trials_df.drop(params_cols, axis=1, inplace=True)
            lr_df = pd.concat([trials_df, lr_df], axis=1)
            return lr_df
        elif 'svm' in name:
            svm_df = pd.DataFrame(self.svm_params)
            new_cols = [f"params_{c}" for c in svm_df.columns]
            svm_df.columns = new_cols
            params_cols = [col for col in trials_df.columns if col.startswith('params')]
            trials_df.drop(params_cols, axis=1, inplace=True)
            svm_df = pd.concat([trials_df, svm_df], axis=1)
            return svm_df
        elif 'xgb' in name:
            xgb_df = pd.DataFrame(self.xgb_params)
            new_cols = [f"params_{c}" for c in xgb_df.columns]
            xgb_df.columns = new_cols
            params_cols = [col for col in trials_df.columns if col.startswith('params')]
            trials_df.drop(params_cols, axis=1, inplace=True)
            xgb_df = pd.concat([trials_df, xgb_df], axis=1)
            return xgb_df
        elif 'dt' in name:
            dt_df = pd.DataFrame(self.dt_params)
            new_cols = [f"params_{c}" for c in dt_df.columns]
            dt_df.columns = new_cols
            params_cols = [col for col in trials_df.columns if col.startswith('params')]
            trials_df.drop(params_cols, axis=1, inplace=True)
            dt_df = pd.concat([trials_df, dt_df], axis=1)
            return dt_df
        elif 'cat' in name:
            cat_df = pd.DataFrame(self.cat_params)
            new_cols = [f"params_{c}" for c in cat_df.columns]
            cat_df.columns = new_cols
            params_cols = [col for col in trials_df.columns if col.startswith('params')]
            trials_df.drop(params_cols, axis=1, inplace=True)
            cat_df = pd.concat([trials_df, cat_df], axis=1)
            return cat_df
        elif 'lgbm' in name:
            lgbm_df = pd.DataFrame(self.lgbm_params)
            new_cols = [f"params_{c}" for c in lgbm_df.columns]
            lgbm_df.columns = new_cols
            params_cols = [col for col in trials_df.columns if col.startswith('params')]
            trials_df.drop(params_cols, axis=1, inplace=True)
            lgbm_df = pd.concat([trials_df, lgbm_df], axis=1)
            return lgbm_df
        elif 'sgd' in name:
            sgd_df = pd.DataFrame(self.sgd_params)
            new_cols = [f"params_{c}" for c in sgd_df.columns]
            sgd_df.columns = new_cols
            params_cols = [col for col in trials_df.columns if col.startswith('params')]
            trials_df.drop(params_cols, axis=1, inplace=True)
            sgd_df = pd.concat([trials_df, sgd_df], axis=1)
            return sgd_df
        elif 'gnb' in name:
            gnb_df = pd.DataFrame(self.gnb_params)
            new_cols = [f"params_{c}" for c in gnb_df.columns]
            gnb_df.columns = new_cols
            params_cols = [col for col in trials_df.columns if col.startswith('params')]
            trials_df.drop(params_cols, axis=1, inplace=True)
            gnb_df = pd.concat([trials_df, gnb_df], axis=1)
            return gnb_df
        else:
            return trials_df


# class ParamsLoader
class ParamsLoader:
    """
                    Loading the parameters from a csv
                    file generated by `TuneClassifier
                    <TuneClassifier>`_

                    Parameters
                    ----------
                    params_csv: Union[str, List]
                        path to params.csv file
                    column_name: str
                        this parameter checks the
                        `fetch_max` argument and
                        extracts the maximum from this
                        column
                    index_id: int
                        if column_name is none, it will
                        use index id. Usefull when you
                        have multiple metrics and want to
                        do a trade-off
                    save_loc: Union[str, Path]
                        location to save the params.
                        If None, file will not be saved.
                    fetch_max: bool
                        if True, it will look for the
                        maximum value in the `column_
                        name` column. When used with
                        `index_id`, this parameter has no
                        effect.

                    Methods
                    -------
                    load_params()
                        loads only the non-null parameters
                        from the csv file and returns a
                        dictionary

                    Raises
                    ------
                    AttributeError
                        Raised when both `column_name`
                        and `index_id` are provided at the
                        same time

                    Examples
                    --------
                    >>> pl = ParamsLoader('params.csv',
                                                    'col1',
                                                    save_loc='.',
                                                    fetch_max=True)
                    >>> params = pl.load_params()
                    """

    # noinspection PyTypeChecker
    def __init__(self, params_csv: Union[str, Path], column_name: str = None,
                 index_id: int = None, save_loc: Union[str, Path] = None,
                 fetch_max: bool = True):
        if column_name is not None and index_id is not None:
            logger.error(f"Invalid input.")
            raise AttributeError(
                f"`column_name` and `index_id` cannot be provided at the same time"
            )
        self.df = pd.read_csv(params_csv)
        self.column_name = column_name
        self.index_id = index_id
        self.save_loc = save_loc
        self.fetch_max = fetch_max
        self.cols_to_extract = [c for c in self.df.columns if c.startswith('params_')]

    # Loading the params given a column name
    def load_via_column(self) -> Dict:
        """
        Loading params given a column name.

        Returns
        -------
        parameters: Dict
            non-null parameters as a dictionary
        """
        if self.fetch_max:
            value = max(self.df[self.column_name])
        else:
            value = min(self.df[self.column_name])
        params = self.df[self.df[self.column_name] == value]
        params = params[self.cols_to_extract]
        params.dropna(axis=1, inplace=True)
        new_cols = [c.replace('params_', '') for c in params.columns]
        params.columns = new_cols
        params.reset_index(inplace=True, drop=True)
        params = params.loc[0].to_dict()
        return params

    # Loading the params given an index
    def load_via_index(self) -> Dict:
        """
        Loading params given an index id.

        Returns
        -------
        parameters: Dict
            non-null parameters as a dictionary
        """
        params = self.df.loc[self.index_id]
        params = params[self.cols_to_extract]
        params.dropna(inplace=True)
        params = params.to_dict()
        return params

    # Loading and saving the params
    def load_params(self):
        """
        User function for loading the params.

        Returns
        -------
        parameters: Dict
            non-null parameters as a dictionary
        """
        if self.column_name is None:
            params = self.load_via_index()
        else:
            params = self.load_via_column()

        if self.save_loc is not None:
            # noinspection PyTypeChecker
            Path(self.save_loc).mkdir(parents=True, exist_ok=True)
            with open(f"{self.save_loc}/params.pkl", 'wb') as pf:
                pickle.dump(params, pf)

        return params



