#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#
"""
"rbfsvm" - SVM - Radial Kernel
"gpc" - Gaussian Process Classifier
"mlp" - MLP Classifier
"qda" - Quadratic Discriminant Analysis
"lda" - Linear Discriminant Analysis
"et" - Extra Trees Classifier
"""
import logging
import os
import traceback
import warnings
from typing import Any
from typing import Dict
from typing import Optional

import mlflow.sklearn
import numpy as np
import pandas as pd
from katonic.ml.client import MLClient
from katonic.ml.hyperparameter_tuning import HyperParameterTune
from katonic.ml.util import add_doc
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import log_loss
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score


mlflow.set_tracking_uri(os.environ["MLFLOW_BASE_URL"])
client = mlflow.tracking.MlflowClient(os.environ["MLFLOW_BASE_URL"])
logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

warnings.filterwarnings("ignore")


def input_validation(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    experiment_name: str,
    multiclass: bool,
    average: str,
) -> None:
    """
    Args:
        X_train (pandas.DataFrame): Shape (n_samples, n_features), where n_samples is the number of samples and
            n_features is the number of features for train dataset.

        X_test (pandas.DataFrame): Shape (n_samples, n_features), where n_samples is the number of samples and
            n_features is the number of features for test dataset.

        y_train (pandas.Series): Shape (n_samples, 1), where n_samples is the number of samples for train dataset.

        y_test (pandas.Series): Shape (n_samples, 1), where n_samples is the number of samples for test dataset.

        experiment_name (str): Name of the experiment for logging.

        multiclass (bool): True if data is multi class else False.

        average (string, [None, ``binary`` (default), ``micro``, ``macro``, ``samples``, ``weighted``]):
            This parameter is required for multiclass/multilabel targets.
            If None, the scores for each class are returned. Otherwise, this determines the type of averaging performed on the data.
    """

    if not (isinstance(X_train, (pd.Series, pd.DataFrame, np.ndarray))):
        raise TypeError("X_train passed must be of type pandas.DataFrame")
    if X_train.shape[0] == 0:
        raise ValueError("X_train passed must be a positive dataframe")
    if not (isinstance(X_test, (pd.Series, pd.DataFrame, np.ndarray))):
        raise TypeError("X_test passed must be of type pandas.DataFrame")
    if X_test.shape[0] == 0:
        raise ValueError("X_test passed must be a positive dataframe")
    if not (isinstance(y_train, (pd.Series, pd.DataFrame, np.ndarray))):
        raise TypeError(
            "y_train passed must be of type pandas.Series, pandas.DataFrame, numpy.ndarray"
        )
    if y_train.shape[0] == 0:
        raise ValueError("y_train passed must be a positive Series")
    if not (isinstance(y_test, (pd.Series, pd.DataFrame, np.ndarray))):
        raise TypeError(
            "y_test passed must be of type pandas.Series, pandas.DataFrame, numpy.ndarray"
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
    if not isinstance(experiment_name, str):
        raise ValueError("experiment_name must be string")
    if not experiment_name:
        raise ValueError("experiment_name cannot be null or empty string")
    if not isinstance(multiclass, bool):
        raise ValueError("multiclass must be boolean")
    if not isinstance(average, str):
        raise ValueError("average must be string")


class Classifier(MLClient):
    problem = "classification"
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
                    "n_estimators": {
                        "low": 80,
                        "high": 120,
                        "step": 10,
                        "type": "int"
                        },
                    "criterion":"gini",
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
                obj = Classifier(X_train, X_test, y_train, y_test, exp_name)
                obj.RandomForestClassifier(is_tune=True, n_trials=10, params=params)

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
        multiclass: bool = False,
        average: str = "binary",
    ):
        """
        A Classifier Object is used to define, create a classifier model.

        Args:
            X_train (pandas.DataFrame): Shape (n_samples, n_features), where n_samples is the number of samples and
                n_features is the number of features for train dataset.

            X_test (pandas.DataFrame): Shape (n_samples, n_features), where n_samples is the number of samples and
                n_features is the number of features for test dataset.

            y_train (pandas.Series): Shape (n_samples, 1), where n_samples is the number of samples for train dataset.

            y_test (pandas.Series): Shape (n_samples, 1), where n_samples is the number of samples for test dataset.

            experiment_name (str): Name of the experiment for logging.

            multiclass (bool): True if data is multi class else False.

            average (string, [None, ``binary`` (default), ``micro``, ``macro``, ``samples``, ``weighted``]):
                This parameter is required for multiclass/multilabel targets.
                If None, the scores for each class are returned. Otherwise, this determines the type of averaging performed on the data.
        """

        logger.info("Validation Start")
        input_validation(
            X_train, X_test, y_train, y_test, experiment_name, multiclass, average
        )
        logger.info("Validation End")

        super().__init__(experiment_name)

        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.multiclass = multiclass
        self.username = os.getenv("EXP_USER") or "default"
        self.average = average
        self.experiment_name = experiment_name
        logger.info("Classification successfully instantiated")

    def __str__(self):
        return f"Classfiaction models for experiment: Experiment Name is {self.name}, Experiment ID is {self.id}"

    def eval_metrics(self, actual, pred):
        """
        Calculates various evaluation parameters like accuracy_score, roc_auc_score, log_loss, recall_score, f1_score, precision_score
        for classification problem.

        Args:
            actual (pd.Dataframe): actual ``y`` value
            pred (pd.Dataframe): predicted ``y`` value

        Returns:
            (
                acc_score: Accuracy score,
                auc_roc: roc auc Score,
                log_los: log_loss,
                recall: recall,
                f1_scr: F1 Score,
                precision_scr: precision Score,
            )
        """
        logger.info("Calculating evaluation paramaters")
        """
        try:
            logger.info(f"classification Report")
            logger.info(classification_report(actual, pred))
        except:
            logger.error(f"classification_report calcuation raised an exception:")
            logger.error(traceback.format_exc())
        try:
            logger.info(f"Confusion Matrix")
            confusion_matrix = pd.crosstab(actual, pred, rownames=["Actual"], colnames=["Predicted"])
            logger.info(sn.heatmap(confusion_matrix, annot=True))
        except:
            logger.error(f"confusion matrix calcuation raised an exception:")
            logger.error(traceback.format_exc())
        """
        try:
            acc_score = accuracy_score(actual, pred)
        except Exception:
            logger.error("accuracy_score calcuation raised an exception:")
            logger.error(traceback.format_exc())
        try:
            recall = recall_score(actual, pred, average=self.average)
        except Exception:
            logger.error("recall_score calcuation raised an exception:")
            logger.error(traceback.format_exc())
        try:
            precision_scr = precision_score(actual, pred, average=self.average)
        except Exception:
            logger.error("precision_score calcuation raised an exception:")
            logger.error(traceback.format_exc())
        try:
            f1_scr = f1_score(actual, pred, average=self.average)
        except Exception:
            logger.error("f1_score calcuation raised an exception:")
            logger.error(traceback.format_exc())

        if self.multiclass:
            return acc_score, recall, f1_scr, precision_scr
        try:
            auc_roc = roc_auc_score(actual, pred)
        except Exception:
            logger.error("roc_auc_score calcuation raised an exception:")
            logger.error(traceback.format_exc())
        try:
            log_los = log_loss(actual, pred)
        except Exception:
            logger.error("log_loss calcuation raised an exception:")
            logger.error(traceback.format_exc())

        return acc_score, auc_roc, log_los, recall, f1_scr, precision_scr

    def model_fit_log(self, model, run_name: str) -> None:
        """
        Performs the model fitting and model prediction task. It calls the evaluation metrics function and logs the required metrics for the model.

        Args:
            model (Object): classification model object
            run_name (str): It register a model under ``run_name`` if one with the given name does not exist.
        """
        logger.info(f"Training the model {run_name}")
        try:
            model.fit(self.X_train, self.y_train)
        except Exception:
            logger.error(f"Fitting the model {model} raised an exception:")
            logger.error(traceback.format_exc())

        logger.info("Performing the prediction")

        try:
            y_pred = model.predict(self.X_test)
        except Exception:
            logger.error("Prediction process raised an exception:")
            logger.error(traceback.format_exc())

        if self.multiclass:

            (acc_score, recall, f1_scr, precision_scr) = self.eval_metrics(
                self.y_test, y_pred
            )

            metrics = {
                "accuracy_score": acc_score,
                "recall": recall,
                "f1_score": f1_scr,
                "precision_score": precision_scr,
            }
        else:

            (
                acc_score,
                auc_roc,
                log_los,
                recall,
                f1_scr,
                precision_scr,
            ) = self.eval_metrics(self.y_test, y_pred)

            metrics = {
                "accuracy_score": acc_score,
                "roc_auc_score": auc_roc,
                "log_loss": log_los,
                "recall": recall,
                "f1_score": f1_scr,
                "precision_score": precision_scr,
            }

        logger.info(f"logged params: {metrics.keys()}")
        try:
            mlflow.log_metrics(metrics)
        except Exception:
            logger.warning("Couldn't perform log_metrics. Exception:")
            logger.warning(traceback.format_exc())

        logger.info(f"log model {run_name}")
        try:
            mlflow.sklearn.log_model(model, run_name)
        except Exception:
            logger.warning("Couldn't log model. Exception:")
            logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def LogisticRegression(
        self,
        is_tune=False,
        params: Optional[Dict[Any, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for Logistic Regression model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
            for list of parameters that can be passed to model.
        """
        if params is None:
            params = {}
        logger.info("-----------Logistic Regression--------------")

        run_name = f"{self.name}_{self.id}_logistic_regression"

        with mlflow.start_run(run_name=run_name):
            from sklearn.linear_model import LogisticRegression

            try:
                mlflow.set_tag("mlflow.user", self.username)
                model = LogisticRegression(**kwargs)
                self.model_fit_log(model, run_name)
            except Exception:
                logger.warning("couldn't perform runs on model. Exception:")
                logger.warning(traceback.format_exc())

            if is_tune:
                logger.info("-------Tuning Logistic Regression------")
                new_run = f"{run_name}_tuned"
                try:
                    tuner = HyperParameterTune(
                        self.X_train,
                        self.X_test,
                        self.y_train,
                        self.y_test,
                        params,
                        self.experiment_name,
                        self.multiclass,
                        self.average,
                        problem=self.problem,
                        username=self.username,
                    )
                    tuner.tune(LogisticRegression, new_run, n_trials)
                except Exception:
                    logger.warning(
                        "couldn't perform hyperparameter tuning on model. Exception:"
                    )
                    logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def RandomForestClassifier(
        self,
        is_tune=False,
        params: Optional[Dict[Any, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for Random Forest Classifier model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
            for list of parameters that can be passed to model.
        """
        if params is None:
            params = {}
        logger.info("-----------Random Forest Classifier--------------")
        run_name = f"{self.name}_{self.id}_random_forest_classifier"

        with mlflow.start_run(run_name=run_name):
            from sklearn.ensemble import RandomForestClassifier

            try:
                mlflow.set_tag("mlflow.user", self.username)
                model = RandomForestClassifier(**kwargs)
                self.model_fit_log(model, run_name)
            except Exception:
                logger.warning("couldn't perform runs on model. Exception:")
                logger.warning(traceback.format_exc())

            if is_tune:
                logger.info("-------Tuning Random Forest Classifier------")
                new_run = f"{run_name}_tuned"
                try:
                    tuner = HyperParameterTune(
                        self.X_train,
                        self.X_test,
                        self.y_train,
                        self.y_test,
                        params,
                        self.experiment_name,
                        self.multiclass,
                        self.average,
                        problem=self.problem,
                    )
                    tuner.tune(RandomForestClassifier, new_run, n_trials)
                except Exception:
                    logger.warning(
                        "couldn't perform hyperparameter tuning on model. Exception:"
                    )
                    logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def AdaBoostClassifier(
        self,
        is_tune=False,
        params: Optional[Dict[Any, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for Ada Boost Classifier model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html
            for list of parameters that can be passed to model.
        """
        if params is None:
            params = {}
        logger.info("-----------Ada Boost Classifier--------------")

        run_name = f"{self.name}_{self.id}_ada_boost_classifier"

        with mlflow.start_run(run_name=run_name):
            from sklearn.ensemble import AdaBoostClassifier

            try:
                mlflow.set_tag("mlflow.user", self.username)
                model = AdaBoostClassifier(**kwargs)
                self.model_fit_log(model, run_name)
            except Exception:
                logger.warning("couldn't perform runs on model. Exception:")
                logger.warning(traceback.format_exc())

            if is_tune:
                logger.info("-------Tuning Ada Boost Classifier------")
                new_run = f"{run_name}_tuned"
                try:
                    tuner = HyperParameterTune(
                        self.X_train,
                        self.X_test,
                        self.y_train,
                        self.y_test,
                        params,
                        self.experiment_name,
                        self.multiclass,
                        self.average,
                        problem=self.problem,
                    )
                    tuner.tune(AdaBoostClassifier, new_run, n_trials)
                except Exception:
                    logger.warning(
                        "couldn't perform hyperparameter tuning on model. Exception:"
                    )
                    logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def GradientBoostingClassifier(
        self,
        is_tune=False,
        params: Optional[Dict[Any, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for Gradient Boosting Classifier model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html
            for list of parameters that can be passed to model.
        """
        logger.info("-----------Gradient Boosting Classifier--------------")
        run_name = f"{self.name}_{self.id}_gradient_boosting_classifier"

        with mlflow.start_run(run_name=run_name):
            from sklearn.ensemble import GradientBoostingClassifier

            try:
                mlflow.set_tag("mlflow.user", self.username)
                model = GradientBoostingClassifier(**kwargs)
                self.model_fit_log(model, run_name)
            except Exception:
                logger.warning("couldn't perform runs on model. Exception:")
                logger.warning(traceback.format_exc())

            if is_tune:
                logger.info("-------Tuning Gradient Boosting Classifier------")
                new_run = f"{run_name}_tuned"
                try:
                    tuner = HyperParameterTune(
                        self.X_train,
                        self.X_test,
                        self.y_train,
                        self.y_test,
                        params,
                        self.experiment_name,
                        self.multiclass,
                        self.average,
                        problem=self.problem,
                    )
                    tuner.tune(GradientBoostingClassifier, new_run, n_trials)
                except Exception:
                    logger.warning(
                        "couldn't perform hyperparameter tuning on model. Exception:"
                    )
                    logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def CatBoostClassifier(
        self,
        is_tune=False,
        params: Optional[Dict[Any, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for Cat Boost Classifier model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://catboost.ai/en/docs/concepts/python-usages-examples
            for list of parameters that can be passed to model.
        """
        logger.info("-----------Cat Boost Classifier--------------")

        run_name = f"{self.name}_{self.id}_cat_boost_classifier"

        with mlflow.start_run(run_name=run_name):
            from catboost import CatBoostClassifier

            try:
                mlflow.set_tag("mlflow.user", self.username)
                model = CatBoostClassifier(**kwargs)
                self.model_fit_log(model, run_name)
            except Exception:
                logger.warning("couldn't perform runs on model. Exception:")
                logger.warning(traceback.format_exc())

            if is_tune:
                logger.info("-------Tuning Cat Boost Classifier------")
                new_run = f"{run_name}_tuned"
                try:
                    tuner = HyperParameterTune(
                        self.X_train,
                        self.X_test,
                        self.y_train,
                        self.y_test,
                        params,
                        self.experiment_name,
                        self.multiclass,
                        self.average,
                        problem=self.problem,
                    )
                    tuner.tune(CatBoostClassifier, new_run, n_trials)
                except Exception:
                    logger.warning(
                        "couldn't perform hyperparameter tuning on model. Exception:"
                    )
                    logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def LGBMClassifier(
        self,
        is_tune=False,
        params: Optional[Dict[Any, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for LightGBM Classifier model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMClassifier.html
            for list of parameters that can be passed to model.
        """
        logger.info("-----------Light GBM Classifier--------------")

        run_name = f"{self.name}_{self.id}_lgbm_classifier"

        with mlflow.start_run(run_name=run_name):
            from lightgbm import LGBMClassifier

            try:
                mlflow.set_tag("mlflow.user", self.username)
                model = LGBMClassifier(**kwargs)
                self.model_fit_log(model, run_name)
            except Exception:
                logger.warning("couldn't perform runs on model. Exception:")
                logger.warning(traceback.format_exc())

            if is_tune:
                logger.info("-------Tuning Light GBM Classifier------")
                new_run = f"{run_name}_tuned"
                try:
                    tuner = HyperParameterTune(
                        self.X_train,
                        self.X_test,
                        self.y_train,
                        self.y_test,
                        params,
                        self.experiment_name,
                        self.multiclass,
                        self.average,
                        problem=self.problem,
                    )
                    tuner.tune(LGBMClassifier, new_run, n_trials)
                except Exception:
                    logger.warning(
                        "couldn't perform hyperparameter tuning on model. Exception:"
                    )
                    logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def XGBClassifier(
        self,
        is_tune=False,
        params: Optional[Dict[Any, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for XGBoost Classifier model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://xgboost.readthedocs.io/en/latest/python/python_api.html#xgboost.XGBClassifier
            for list of parameters that can be passed to model.
        """
        logger.info("-----------XG Boost Classifier--------------")

        run_name = f"{self.name}_{self.id}_xgb_classifier"

        with mlflow.start_run(run_name=run_name):
            from xgboost import XGBClassifier

            try:
                mlflow.set_tag("mlflow.user", self.username)
                model = XGBClassifier(**kwargs)
                self.model_fit_log(model, run_name)
            except Exception:
                logger.warning("couldn't perform runs on model. Exception:")
                logger.warning(traceback.format_exc())

            if is_tune:
                logger.info("-------Tuning XG Boost Classifier------")
                new_run = f"{run_name}_tuned"
                try:
                    tuner = HyperParameterTune(
                        self.X_train,
                        self.X_test,
                        self.y_train,
                        self.y_test,
                        params,
                        self.experiment_name,
                        self.multiclass,
                        self.average,
                        problem=self.problem,
                    )
                    tuner.tune(XGBClassifier, new_run, n_trials)
                except Exception:
                    logger.warning(
                        "couldn't perform hyperparameter tuning on model. Exception:"
                    )
                    logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def DecisionTreeClassifier(
        self,
        is_tune=False,
        params: Optional[Dict[Any, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for Decision Tree Classifier model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html
            for list of parameters that can be passed to model.
        """
        logger.info("-----------Decision Tree Classifier--------------")

        run_name = f"{self.name}_{self.id}_decision_tree_classifier"

        with mlflow.start_run(run_name=run_name):
            from sklearn.tree import DecisionTreeClassifier

            try:
                mlflow.set_tag("mlflow.user", self.username)
                model = DecisionTreeClassifier(**kwargs)
                self.model_fit_log(model, run_name)
            except Exception:
                logger.warning("couldn't perform runs on model. Exception:")
                logger.warning(traceback.format_exc())

            if is_tune:
                logger.info("-------Tuning Decision Tree Classifier------")
                new_run = f"{run_name}_tuned"
                try:
                    tuner = HyperParameterTune(
                        self.X_train,
                        self.X_test,
                        self.y_train,
                        self.y_test,
                        params,
                        self.experiment_name,
                        self.multiclass,
                        self.average,
                        problem=self.problem,
                    )
                    tuner.tune(DecisionTreeClassifier, new_run, n_trials)
                except Exception:
                    logger.warning(
                        "couldn't perform hyperparameter tuning on model. Exception:"
                    )
                    logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def SupportVectorClassifier(
        self,
        is_tune=False,
        params: Optional[Dict[Any, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for Support Vector Classifier model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://scikit-learn.org/stable/modules/svm.html
            for list of parameters that can be passed to model.
        """
        logger.info("-----------Support Vector Machine Classifier--------------")

        run_name = f"{self.name}_{self.id}_svm_classifier"

        with mlflow.start_run(run_name=run_name):
            from sklearn.svm import SVC

            try:
                mlflow.set_tag("mlflow.user", self.username)
                model = SVC(**kwargs)
                self.model_fit_log(model, run_name)
            except Exception:
                logger.warning("couldn't perform runs on model. Exception:")
                logger.warning(traceback.format_exc())

            if is_tune:
                logger.info("-------Tuning Support Vector Machine Classifier------")
                new_run = f"{run_name}_tuned"
                try:
                    tuner = HyperParameterTune(
                        self.X_train,
                        self.X_test,
                        self.y_train,
                        self.y_test,
                        params,
                        self.experiment_name,
                        self.multiclass,
                        self.average,
                        problem=self.problem,
                    )
                    tuner.tune(SVC, new_run, n_trials)
                except Exception:
                    logger.warning(
                        "couldn't perform hyperparameter tuning on model. Exception:"
                    )
                    logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def RidgeClassifier(
        self,
        is_tune=False,
        params: Optional[Dict[Any, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for Ridge Classifier model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeClassifier.html
            for list of parameters that can be passed to model.
        """
        logger.info("-----------Ridge Classifier--------------")

        run_name = f"{self.name}_{self.id}_ridge_classifier"

        with mlflow.start_run(run_name=run_name):
            from sklearn.linear_model import RidgeClassifier

            try:
                mlflow.set_tag("mlflow.user", self.username)
                model = RidgeClassifier(**kwargs)
                self.model_fit_log(model, run_name)
            except Exception:
                logger.warning("couldn't perform runs on model. Exception:")
                logger.warning(traceback.format_exc())

            if is_tune:
                logger.info("-------Tuning Ridge Classifier------")
                new_run = f"{run_name}_tuned"
                try:
                    tuner = HyperParameterTune(
                        self.X_train,
                        self.X_test,
                        self.y_train,
                        self.y_test,
                        params,
                        self.experiment_name,
                        self.multiclass,
                        self.average,
                        problem=self.problem,
                    )
                    tuner.tune(RidgeClassifier, new_run, n_trials)
                except Exception:
                    logger.warning(
                        "couldn't perform hyperparameter tuning on model. Exception:"
                    )
                    logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def KNeighborsClassifier(
        self,
        is_tune=False,
        params: Optional[Dict[Any, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for K Neighbors Classifier model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html
            for list of parameters that can be passed to model.
        """
        logger.info("-----------K Neighbors Classifier--------------")

        run_name = f"{self.name}_{self.id}_k_neighbors_classifier"

        with mlflow.start_run(run_name=run_name):
            from sklearn.neighbors import KNeighborsClassifier

            try:
                mlflow.set_tag("mlflow.user", self.username)
                model = KNeighborsClassifier(**kwargs)
                self.model_fit_log(model, run_name)
            except Exception:
                logger.warning("couldn't perform runs on model. Exception:")
                logger.warning(traceback.format_exc())

            if is_tune:
                logger.info("-------Tuning K Neighbors Classifier------")
                new_run = f"{run_name}_tuned"
                try:
                    tuner = HyperParameterTune(
                        self.X_train,
                        self.X_test,
                        self.y_train,
                        self.y_test,
                        params,
                        self.experiment_name,
                        self.multiclass,
                        self.average,
                        problem=self.problem,
                    )
                    tuner.tune(KNeighborsClassifier, new_run, n_trials)
                except Exception:
                    logger.warning(
                        "couldn't perform hyperparameter tuning on model. Exception:"
                    )
                    logger.warning(traceback.format_exc())

    @add_doc(hyperparameter_doc)
    def GaussianNB(
        self,
        is_tune=False,
        params: Optional[Dict[Any, Any]] = None,
        n_trials: int = 5,
        **kwargs,
    ) -> None:
        """
        This module performs experiments for Gaussian Naive Bayes Classifier model.

        Args:
            is_tune (bool, default=False): If True then Hyper Parameter Tuning will be done with the given params.

            params (Dict): Hyper Parameters for the Invoked Model.

            n_trials (int, default=5): number of iterations to run the tuning.

            **kwargs: List of parameters that will be passed to define the model.
            Refer: https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.GaussianNB.html
            for list of parameters that can be passed to model.
        """
        logger.info("-----------Gaussian Naive Bayes Classifier--------------")

        run_name = f"{self.name}_{self.id}_gaussian_NB_classifier"

        with mlflow.start_run(run_name=run_name):
            from sklearn.naive_bayes import GaussianNB

            try:
                mlflow.set_tag("mlflow.user", self.username)
                model = GaussianNB(**kwargs)
                self.model_fit_log(model, run_name)
            except Exception:
                logger.warning("couldn't perform runs on model. Exception:")
                logger.warning(traceback.format_exc())

            if is_tune:
                logger.info("-------Tuning Gaussian Naive Bayes Classifier------")
                new_run = f"{run_name}_tuned"
                try:
                    tuner = HyperParameterTune(
                        self.X_train,
                        self.X_test,
                        self.y_train,
                        self.y_test,
                        params,
                        self.experiment_name,
                        self.multiclass,
                        self.average,
                        problem=self.problem,
                    )
                    tuner.tune(GaussianNB, new_run, n_trials)
                except Exception:
                    logger.warning(
                        "couldn't perform hyperparameter tuning on model. Exception:"
                    )
                    logger.warning(traceback.format_exc())
