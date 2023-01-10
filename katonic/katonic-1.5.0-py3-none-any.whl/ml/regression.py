#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#
"""
'lr' - Linear Regression
'lasso' - Lasso Regression
'ridge' - Ridge Regression
'en' - Elastic Net
'lar' - Least Angle Regression
'llar' - Lasso Least Angle Regression
'omp' - Orthogonal Matching Pursuit
'br' - Bayesian Ridge
'ard' - Automatic Relevance Determination
'par' - Passive Aggressive Regressor
'ransac' - Random Sample Consensus
'tr' - TheilSen Regressor
'huber' - Huber Regressor
'kr' - Kernel Ridge
'svm' - Support Vector Regression
'knn' - K Neighbors Regressor
'dt' - Decision Tree Regressor
'rf' - Random Forest Regressor
'et' - Extra Trees Regressor
'ada' - AdaBoost Regressor
'gbr' - Gradient Boosting Regressor
'mlp' - MLP Regressor
'xgboost' - Extreme Gradient Boosting
'lightgbm' - Light Gradient Boosting Machine
'catboost' - CatBoost Regressor
"""
import logging
import os
import traceback
import warnings
from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import Union

import mlflow.sklearn
import numpy as np
import pandas as pd
from katonic.ml.client import MLClient
from katonic.ml.hyperparameter_tuning import HyperParameterTune
from katonic.ml.util import add_doc
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score


logging.basicConfig(level=logging.WARN)

logger = logging.getLogger(__name__)
mlflow.set_tracking_uri(os.environ["MLFLOW_BASE_URL"])
client = mlflow.tracking.MlflowClient(os.environ["MLFLOW_BASE_URL"])

warnings.filterwarnings("ignore")


def input_validation(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
) -> None:
    """
    Args:
        X_train (pandas.DataFrame): Shape (n_samples, n_features), where n_samples is the number of samples and
            n_features is the number of features for train dataset.

        X_test (pandas.DataFrame): Shape (n_samples, n_features), where n_samples is the number of samples and
            n_features is the number of features for test dataset.

        y_train (pandas.Series): Shape (n_samples, 1), where n_samples is the number of samples for train dataset.

        y_test (pandas.Series): Shape (n_samples, 1), where n_samples is the number of samples for test dataset.
    """
    if not isinstance(X_train, (pd.DataFrame, np.ndarray)):
        raise TypeError(
            "X_train passed must be of type pandas.DataFrame or numpy.ndarray"
        )
    if X_train.shape[0] == 0:
        raise ValueError("X_train passed must be a positive dataframe")
    if not (isinstance(X_test, pd.DataFrame) or isinstance(X_train, np.ndarray)):
        raise TypeError(
            "X_test passed must be of type pandas.DataFrame or numpy.ndarray"
        )
    if X_test.shape[0] == 0:
        raise ValueError("X_test passed must be a positive dataframe")
    if not (isinstance(y_train, (pd.Series, pd.DataFrame, np.ndarray))):
        raise TypeError(
            "y_train passed must be of type pandas.Series,pandas.DataFrame,numpy.ndarray"
        )
    if y_train.shape[0] == 0:
        raise ValueError("y_train passed must be a positive Series")
    if not (isinstance(y_test, (pd.Series, pd.DataFrame, np.ndarray))):
        raise TypeError(
            "y_test passed must be of type pandas.Series,pandas.DataFrame,numpy.ndarray"
        )
    if y_test.shape[0] == 0:
        raise ValueError("y_test passed must be a positive Series")
    if X_train.shape[0] != len(y_train):
        raise ValueError(
            "Length of Train set and its respective Target variable should be of equal length"
        )
    if X_test.shape[0] != len(y_test):
        raise ValueError(
            "Length of Test set and its respective Target variable should be of equal length"
        )


class Regressor(MLClient):
    problem = "regression"
    hyperparameter_doc = """
        is_tune: bool, Default: False
            This decides whether to tune the model or not
        params: dict, Default: Empty dictionary
            Parameters on the model needs to be tuned.
        n_trials: int, Default: 5
            The number of trials/iteration to run the hyperparameter tuning function before finalizing
        [refer]: https://optuna.readthedocs.io/en/stable/reference/generated/optuna.study.Study.html#optuna.study.Study.optimize
            for n_trials

        Available datatypes for params are:
        [int, float, categorical, uniform, loguniform, discrete_uniform]
        [refer]: https://optuna.readthedocs.io/en/stable/reference/generated/optuna.trial.Trial.html#optuna.trial.Trial
            for reading about datatypes
        Dictionary for params need to be as following structure:
            params = {
                "parameter1": {
                    "low": 10,
                    "high": 50,
                    "step": 5,   // Default: 1
                    "type": "int"
                    },
                "parameter2":{
                    "values": ["option 1", "option 2"],
                    "type": "categorical"
                    },
                "parameter3": {
                    "low": 0.5,
                    "high": 1.0,
                    "step": 0.1,   // Default: 0.1
                    "log": False,  // Default: False
                    "type": "float"
                    },
                "parameter4":{
                    "low": 1.0,
                    "high": 2.0,
                    "type": "uniform"
                    },
                "parameter5":{
                    "low": 1.0,
                    "high": 2.0,
                    "type": "loguniform"
                    },
                "parameter6":{
                    "low": 1.0,
                    "high": 2.0,
                    "q": 0.1,     // Default: 0.1
                    "type": "discrete_uniform"
                    },
                "parameter7": 30,
                "parameter9: 0.8,
                "parameter10": "some param"
            }

            Example:
                params = {
                    "n_estimators": 80,
                    "criterion":{
                        "values": ["mse", "mae"],
                        "type": "categorical"
                        },
                    "min_samples_split": {
                        "low": 2,
                        "high": 5,
                        "type": "int"
                        },
                    "min_samples_leaf":{
                        "low": 1,
                        "high": 5,
                        "type": "int"
                        }
                    }
                obj = Regressor(X_train, X_test, y_train, y_test, exp_name)
                obj.RandomForestRegressor(is_tune=True, n_trials=10, params=params)

            Returns:
                None
            """

    def __init__(
        self,
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        y_train: pd.Series,
        y_test: pd.Series,
        experiment_name: str,
    ):
        """
        A Regressor Object is used to define, create a regressor model.

        Args:
            X_train (pandas.DataFrame): Shape (n_samples, n_features), where n_samples is the number of samples and
                n_features is the number of features for train dataset.

            X_test (pandas.DataFrame): Shape (n_samples, n_features), where n_samples is the number of samples and
                n_features is the number of features for test dataset.

            y_train (pandas.Series): Shape (n_samples, 1), where n_samples is the number of samples for train dataset.

            y_test (pandas.Series): Shape (n_samples, 1), where n_samples is the number of samples for test dataset.

            experiment_name (str): Name of the experiment for logging.
        """
        logger.info("Validation Start")
        input_validation(X_train, X_test, y_train, y_test)
        logger.info("Validation End")

        super().__init__(experiment_name)

        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.username = os.getenv("EXP_USER") or "default"
        self.experiment_name = experiment_name
        logger.info("Regression successfully instantiated")

    def __str__(self):
        return f"Regression models for experiment: Experiment Name is {self.name}, Experiment ID is {self.id}"

    def eval_metrics(
        self,
        actual: Union[pd.Series, pd.DataFrame, np.ndarray],
        pred: Union[pd.Series, pd.DataFrame, np.ndarray],
    ) -> Tuple[Any, Any, Any, Any, float]:
        """
        Calculates various evaluation parameters like mse, rmse, mae rmsle for regression problem.

        Args:
            actual (pandas.Series or pandas.DataFrame, or numpy array): actual ``testing`` data
            pred (pandas.Series or pandas.DataFrame, or numpy array): predicted ``testing`` data

        Returns:
            (
                mse: mean square error,
                rmse: root mean square error,
                rmsle: root mean square log error,
                mae: mean absolute error,
                r2: r-2 score,
            )
        """
        logger.info("Calculating evaluation paramaters")
        try:
            mse = mean_squared_error(actual, pred)
        except Exception:
            logger.error("mean_squared_error calcuation raised an exception:")
            logger.error(traceback.format_exc())
        try:
            rmse = np.sqrt(mse)
        except Exception:
            logger.error("root_mean_squared_error calcuation raised an exception:")
            logger.error(traceback.format_exc())
        try:
            rmsle = np.log(rmse)
        except Exception:
            logger.error("root_mean_squared_log_error calcuation raised an exception:")
            logger.error(traceback.format_exc())
        try:
            mae = mean_absolute_error(actual, pred)
        except Exception:
            logger.error("mean_absolute_error calcuation raised an exception:")
            logger.error(traceback.format_exc())
        try:
            r2 = r2_score(actual, pred)
        except Exception:
            logger.error("r2 score calcuation raised an exception:")
            logger.error(traceback.format_exc())

        return mse, rmse, rmsle, mae, r2

    def model_fit_log(self, model: Any, run_name: str) -> None:
        """
        Performs the model fitting and model prediction task. It calls the evaluation metrics function and logs the required metrics for the model.

        Args:
            model (Object) : regression model object
            run_name (str): It register a model under ``run_name`` if one with the given name does not exist.
        """
        logger.info("Training the model")
        try:
            model.fit(self.X_train, self.y_train)
        except Exception:
            logger.error(f"Fitting the model {run_name} raised an exception:")
            logger.error(traceback.format_exc())

        logger.info("Performing the prediction")

        try:
            y_pred = model.predict(self.X_test)
        except Exception:
            logger.error("Prediction process raised an exception:")
            logger.error(traceback.format_exc())

        (mse, rmse, rmsle, mae, r2) = self.eval_metrics(self.y_test, y_pred)

        metrics = {"MSE": mse, "RMSE": rmse, "RMSLE": rmsle, "MAE": mae, "R2": r2}

        logger.info(f"logged params: {metrics.keys()}")
        try:
            mlflow.log_metrics(metrics)
        except Exception:
            logger.warning("Couldn't log metrics. Exception:")
            logger.warning(traceback.format_exc())
        logger.info(f"logging model {run_name}")
        try:
            mlflow.sklearn.log_model(model, run_name)
        except Exception:
            logger.warning("Couldn't log model. Exception:")
            logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def LinearRegression(
        self,
        is_tune=False,
        params: Optional[Dict[str, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for Linear Regression model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
            for list of parameters that can be passed to model.
        """
        if params is None:
            params = {}
        logger.info("-----------Linear Regression----------------")

        from sklearn.linear_model import LinearRegression

        run_name = f"{self.name}_{self.id}_Linear_regression"
        try:
            with mlflow.start_run(run_name=run_name):
                mlflow.set_tag("mlflow.user", self.username)
                model = LinearRegression(**kwargs)
                self.model_fit_log(model, run_name)

                if is_tune:
                    logger.info("-------Tuning Linear Regression------")
                    new_run = run_name + "_tuned"
                    try:
                        tuner = HyperParameterTune(
                            self.X_train,
                            self.X_test,
                            self.y_train,
                            self.y_test,
                            params,
                            self.experiment_name,
                            problem=self.problem,
                        )
                        tuner.tune(LinearRegression, new_run, n_trials)
                    except Exception:
                        logger.warning(
                            "Couldn't perform hyperparameter tuning on model. Exception:"
                        )
                        logger.warning(traceback.format_exc())
        except Exception:
            logger.warning("Couldn't perform runs on model. Exception:")
            logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def RidgeRegression(
        self,
        is_tune=False,
        params: Optional[Dict[str, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for Ridge Regression model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html
            for list of parameters that can be passed to model.
        """
        if params is None:
            params = {}
        logger.info("-----------Ridge Regression----------------")

        from sklearn.linear_model import Ridge

        run_name = f"{self.name}_{self.id}_Ridge_regression"
        try:
            with mlflow.start_run(run_name=run_name):
                mlflow.set_tag("mlflow.user", self.username)
                model = Ridge(**kwargs)
                self.model_fit_log(model, run_name)

                if is_tune:
                    logger.info("-------Tuning Ridge Regression------")
                    new_run = run_name + "_tuned"
                    try:
                        tuner = HyperParameterTune(
                            self.X_train,
                            self.X_test,
                            self.y_train,
                            self.y_test,
                            params,
                            self.experiment_name,
                            problem=self.problem,
                        )
                        tuner.tune(Ridge, new_run, n_trials)
                    except Exception:
                        logger.warning(
                            "Couldn't perform hyperparameter tuning on model. Exception:"
                        )
                        logger.warning(traceback.format_exc())
        except Exception:
            logger.warning("Couldn't perform runs on model. Exception:")
            logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def LassoRegression(
        self,
        is_tune=False,
        params: Optional[Dict[str, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for Ridge Regression model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html
            for list of parameters that can be passed to model.
        """
        if params is None:
            params = {}
        logger.info("-----------Lasso Regression----------------")

        from sklearn.linear_model import Lasso

        run_name = f"{self.name}_{self.id}_Lasso_regression"
        try:
            with mlflow.start_run(run_name=run_name):
                mlflow.set_tag("mlflow.user", self.username)
                model = Lasso(**kwargs)
                self.model_fit_log(model, run_name)

                if is_tune:
                    logger.info("-------Tuning Lasso Regression------")
                    new_run = run_name + "_tuned"
                    try:
                        tuner = HyperParameterTune(
                            self.X_train,
                            self.X_test,
                            self.y_train,
                            self.y_test,
                            params,
                            self.experiment_name,
                            problem=self.problem,
                        )
                        tuner.tune(Lasso, new_run, n_trials)
                    except Exception:
                        logger.warning(
                            "Couldn't perform hyperparameter tuning on model. Exception:"
                        )
                        logger.warning(traceback.format_exc())
        except Exception:
            logger.warning("Couldn't perform runs on model. Exception:")
            logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def ElasticNet(
        self,
        is_tune=False,
        params: Optional[Dict[str, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for Ridge Regression model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNet.html
            for list of parameters that can be passed to model.
        """
        if params is None:
            params = {}
        logger.info("-----------Elasticnet Regression----------------")

        from sklearn.linear_model import ElasticNet

        run_name = f"{self.name}_{self.id}_ElasticNet_regression"
        try:
            with mlflow.start_run(run_name=run_name):
                mlflow.set_tag("mlflow.user", self.username)
                model = ElasticNet(**kwargs)
                self.model_fit_log(model, run_name)

                if is_tune:
                    logger.info("-------Tuning Elasticnet Regression------")
                    new_run = run_name + "_tuned"
                    try:
                        tuner = HyperParameterTune(
                            self.X_train,
                            self.X_test,
                            self.y_train,
                            self.y_test,
                            params,
                            self.experiment_name,
                            problem=self.problem,
                        )
                        tuner.tune(ElasticNet, new_run, n_trials)
                    except Exception:
                        logger.warning(
                            "Couldn't perform hyperparameter tuning on model. Exception:"
                        )
                        logger.warning(traceback.format_exc())
        except Exception:
            logger.warning("Couldn't perform runs on model. Exception:")
            logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def SupportVectorRegressor(
        self,
        is_tune=False,
        params: Optional[Dict[str, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for Support Vector Regression model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://scikit-learn.org/stable/modules/svm.html
            for list of parameters that can be passed to model.
        """
        if params is None:
            params = {}
        logger.info("-----------Support Vector Regression----------------")

        from sklearn.svm import SVR

        run_name = f"{self.name}_{self.id}_SupportVector_regression"
        try:
            with mlflow.start_run(run_name=run_name):
                mlflow.set_tag("mlflow.user", self.username)
                model = SVR(**kwargs)
                self.model_fit_log(model, run_name)

                if is_tune:
                    logger.info("-------Tuning Support Vector Regression------")
                    new_run = run_name + "_tuned"
                    try:
                        tuner = HyperParameterTune(
                            self.X_train,
                            self.X_test,
                            self.y_train,
                            self.y_test,
                            params,
                            self.experiment_name,
                            problem=self.problem,
                        )
                        tuner.tune(SVR, new_run, n_trials)
                    except Exception:
                        logger.warning(
                            "Couldn't perform hyperparameter tuning on model. Exception:"
                        )
                        logger.warning(traceback.format_exc())
        except Exception:
            logger.warning("Couldn't perform runs on model. Exception:")
            logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def KNNRegressor(
        self,
        is_tune=False,
        params: Optional[Dict[str, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for KNN Regression model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsRegressor.html
            for list of parameters that can be passed to model.
        """
        if params is None:
            params = {}
        logger.info("-----------KNN Regression----------------")

        from sklearn.neighbors import KNeighborsRegressor

        run_name = f"{self.name}_{self.id}_KNN_regression"
        try:
            with mlflow.start_run(run_name=run_name):
                mlflow.set_tag("mlflow.user", self.username)
                model = KNeighborsRegressor(**kwargs)
                self.model_fit_log(model, run_name)

                if is_tune:
                    logger.info("-------Tuning KNN Regression------")
                    new_run = run_name + "_tuned"
                    try:
                        tuner = HyperParameterTune(
                            self.X_train,
                            self.X_test,
                            self.y_train,
                            self.y_test,
                            params,
                            self.experiment_name,
                            problem=self.problem,
                        )
                        tuner.tune(KNeighborsRegressor, new_run, n_trials)
                    except Exception:
                        logger.warning(
                            "Couldn't perform hyperparameter tuning on model. Exception:"
                        )
                        logger.warning(traceback.format_exc())
        except Exception:
            logger.warning("Couldn't perform runs on model. Exception:")
            logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def RandomForestRegressor(
        self,
        is_tune=False,
        params: Optional[Dict[str, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for Random Forest Regression model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html
            for list of parameters that can be passed to model.
        """
        if params is None:
            params = {}
        logger.info("-----------Random Forest Regression----------------")

        from sklearn.ensemble import RandomForestRegressor

        run_name = f"{self.name}_{self.id}_RandomForest_regression"
        try:
            with mlflow.start_run(run_name=run_name):
                mlflow.set_tag("mlflow.user", self.username)
                model = RandomForestRegressor(**kwargs)
                self.model_fit_log(model, run_name)

                if is_tune:
                    logger.info("-------Tuning Random Forest Regression------")
                    new_run = run_name + "_tuned"
                    try:
                        tuner = HyperParameterTune(
                            self.X_train,
                            self.X_test,
                            self.y_train,
                            self.y_test,
                            params,
                            self.experiment_name,
                            problem=self.problem,
                        )
                        tuner.tune(RandomForestRegressor, new_run, n_trials)
                    except Exception:
                        logger.warning(
                            "Couldn't perform hyperparameter tuning on model. Exception:"
                        )
                        logger.warning(traceback.format_exc())
        except Exception:
            logger.warning("Couldn't perform runs on model. Exception:")
            logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def XGBRegressor(
        self,
        is_tune=False,
        params: Optional[Dict[str, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for XGBoost Regression model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://xgboost.readthedocs.io/en/latest/python/python_api.html#module-xgboost.sklearn
            for list of parameters that can be passed to model.
        """
        if params is None:
            params = {}
        logger.info("-----------XGBoost Regression----------------")

        from xgboost import XGBRegressor

        run_name = f"{self.name}_{self.id}_XGBoost_regression"
        try:
            with mlflow.start_run(run_name=run_name):
                mlflow.set_tag("mlflow.user", self.username)
                model = XGBRegressor(**kwargs)
                self.model_fit_log(model, run_name)

                if is_tune:
                    logger.info("-------Tuning XGBoost Regression------")
                    new_run = run_name + "_tuned"
                    try:
                        tuner = HyperParameterTune(
                            self.X_train,
                            self.X_test,
                            self.y_train,
                            self.y_test,
                            params,
                            self.experiment_name,
                            problem=self.problem,
                        )
                        tuner.tune(XGBRegressor, new_run, n_trials)
                    except Exception:
                        logger.warning(
                            "Couldn't perform hyperparameter tuning on model. Exception:"
                        )
                        logger.warning(traceback.format_exc())
        except Exception:
            logger.warning("Couldn't perform runs on model. Exception:")
            logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def CatBoostRegressor(
        self,
        is_tune=False,
        params: Optional[Dict[str, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for XGBoost Regression model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://catboost.ai/en/docs/concepts/python-reference_catboostregressor
            for list of parameters that can be passed to model.
        """
        if params is None:
            params = {}
        logger.info("-----------Catboost Regression----------------")

        from catboost import CatBoostRegressor

        run_name = f"{self.name}_{self.id}_CatBoost_regression"
        try:
            with mlflow.start_run(run_name=run_name):
                mlflow.set_tag("mlflow.user", self.username)
                model = CatBoostRegressor(**kwargs)
                self.model_fit_log(model, run_name)

                if is_tune:
                    logger.info("-------Tuning Catboost Regression------")
                    new_run = run_name + "_tuned"
                    try:
                        tuner = HyperParameterTune(
                            self.X_train,
                            self.X_test,
                            self.y_train,
                            self.y_test,
                            params,
                            self.experiment_name,
                            problem=self.problem,
                        )
                        tuner.tune(CatBoostRegressor, new_run, n_trials)
                    except Exception:
                        logger.warning(
                            "Couldn't perform hyperparameter tuning on model. Exception:"
                        )
                        logger.warning(traceback.format_exc())
        except Exception:
            logger.warning("Couldn't perform runs on model. Exception:")
            logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def LGBMRegressor(
        self,
        is_tune=False,
        params: Optional[Dict[str, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for LGBM Regression model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMRegressor.html
            for list of parameters that can be passed to model.
        """
        if params is None:
            params = {}
        logger.info("-----------LightGBM Regression----------------")

        from lightgbm import LGBMRegressor

        run_name = f"{self.name}_{self.id}_LGBM_regression"
        try:
            with mlflow.start_run(run_name=run_name):
                mlflow.set_tag("mlflow.user", self.username)
                model = LGBMRegressor(**kwargs)
                self.model_fit_log(model, run_name)

                if is_tune:
                    logger.info("-------Tuning LightGBM Regression------")
                    new_run = run_name + "_tuned"
                    try:
                        tuner = HyperParameterTune(
                            self.X_train,
                            self.X_test,
                            self.y_train,
                            self.y_test,
                            params,
                            self.experiment_name,
                            problem=self.problem,
                        )
                        tuner.tune(LGBMRegressor, new_run, n_trials)
                    except Exception:
                        logger.warning(
                            "Couldn't perform hyperparameter tuning on model. Exception:"
                        )
                        logger.warning(traceback.format_exc())
        except Exception:
            logger.warning("Couldn't perform runs on model. Exception:")
            logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def GradientBoostingRegressor(
        self,
        is_tune=False,
        params: Optional[Dict[str, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for Gradient Boosting Regression model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html
            for list of parameters that can be passed to model.
        """
        if params is None:
            params = {}
        logger.info("-----------GradientBoost Regression----------------")

        from sklearn.ensemble import GradientBoostingRegressor

        run_name = f"{self.name}_{self.id}_GB_regression"
        try:
            with mlflow.start_run(run_name=run_name):
                mlflow.set_tag("mlflow.user", self.username)
                model = GradientBoostingRegressor(**kwargs)
                self.model_fit_log(model, run_name)

                if is_tune:
                    logger.info("-------Tuning GradientBoost Regression------")
                    new_run = run_name + "_tuned"
                    try:
                        tuner = HyperParameterTune(
                            self.X_train,
                            self.X_test,
                            self.y_train,
                            self.y_test,
                            params,
                            self.experiment_name,
                            problem=self.problem,
                        )
                        tuner.tune(GradientBoostingRegressor, new_run, n_trials)
                    except Exception:
                        logger.warning(
                            "Couldn't perform hyperparameter tuning on model. Exception:"
                        )
                        logger.warning(traceback.format_exc())
        except Exception:
            logger.warning("Couldn't perform runs on model. Exception:")
            logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def AdaBoostRegressor(
        self,
        is_tune=False,
        params: Optional[Dict[str, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for AdaBoost Regression model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostRegressor.html
            for list of parameters that can be passed to model.
        """
        if params is None:
            params = {}
        logger.info("-----------AdaBoost Regression----------------")

        from sklearn.ensemble import AdaBoostRegressor

        run_name = f"{self.name}_{self.id}_Adaboost_regression"
        try:
            with mlflow.start_run(run_name=run_name):
                mlflow.set_tag("mlflow.user", self.username)
                model = AdaBoostRegressor(**kwargs)
                self.model_fit_log(model, run_name)

                if is_tune:
                    logger.info("-------Tuning AdaBoost Regression------")
                    new_run = run_name + "_tuned"
                    try:
                        tuner = HyperParameterTune(
                            self.X_train,
                            self.X_test,
                            self.y_train,
                            self.y_test,
                            params,
                            self.experiment_name,
                            problem=self.problem,
                        )
                        tuner.tune(AdaBoostRegressor, new_run, n_trials)
                    except Exception:
                        logger.warning(
                            "Couldn't perform hyperparameter tuning on model. Exception:"
                        )
                        logger.warning(traceback.format_exc())
        except Exception:
            logger.warning("Couldn't perform runs on model. Exception:")
            logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def DecisionTreeRegressor(
        self,
        is_tune=False,
        params: Optional[Dict[str, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for DecisionTree Regression model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html
            for list of parameters that can be passed to model.
        """
        if params is None:
            params = {}
        logger.info("-----------DecisionTree Regression----------------")

        from sklearn.tree import DecisionTreeRegressor

        run_name = f"{self.name}_{self.id}_DecisionTree_regression"
        try:
            with mlflow.start_run(run_name=run_name):
                mlflow.set_tag("mlflow.user", self.username)
                model = DecisionTreeRegressor(**kwargs)
                self.model_fit_log(model, run_name)

                if is_tune:
                    logger.info("-------Tuning DecisionTree Regression------")
                    new_run = run_name + "_tuned"
                    try:
                        tuner = HyperParameterTune(
                            self.X_train,
                            self.X_test,
                            self.y_train,
                            self.y_test,
                            params,
                            self.experiment_name,
                            problem=self.problem,
                        )
                        tuner.tune(DecisionTreeRegressor, new_run, n_trials)
                    except Exception:
                        logger.warning(
                            "Couldn't perform hyperparameter tuning on model. Exception:"
                        )
                        logger.warning(traceback.format_exc())
        except Exception:
            logger.warning("Couldn't perform runs on model. Exception:")
            logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def ExtraTreeRegressor(
        self,
        is_tune=False,
        params: Optional[Dict[str, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for ExtraTree Regression model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesRegressor.html
            for list of parameters that can be passed to model.
        """
        if params is None:
            params = {}
        logger.info("-----------ExtraTree Regression----------------")

        from sklearn.ensemble import ExtraTreesRegressor

        run_name = f"{self.name}_{self.id}_ExtraTree_regression"
        try:
            with mlflow.start_run(run_name=run_name):
                mlflow.set_tag("mlflow.user", self.username)
                model = ExtraTreesRegressor(**kwargs)
                self.model_fit_log(model, run_name)

                if is_tune:
                    logger.info("-------Tuning ExtraTree Regression------")
                    new_run = run_name + "_tuned"
                    try:
                        tuner = HyperParameterTune(
                            self.X_train,
                            self.X_test,
                            self.y_train,
                            self.y_test,
                            params,
                            self.experiment_name,
                            problem=self.problem,
                        )
                        tuner.tune(ExtraTreesRegressor, new_run, n_trials)
                    except Exception:
                        logger.warning(
                            "Couldn't perform hyperparameter tuning on model. Exception:"
                        )
                        logger.warning(traceback.format_exc())
        except Exception:
            logger.warning("Couldn't perform runs on model. Exception:")
            logger.warning(traceback.format_exc())
