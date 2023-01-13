#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#
import logging
import os
import traceback
import warnings
from typing import Any
from typing import Dict
from typing import Optional

import mlflow.sklearn
from katonic.log.client import MLClient


mlflow.set_tracking_uri(os.environ["MLFLOW_BASE_URL"])
client = mlflow.tracking.MlflowClient(os.environ["MLFLOW_BASE_URL"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

warnings.filterwarnings("ignore")


def misc_input_validation(
    model_name: str,
    model_type: str,
    model: Any,
    artifact_path: Optional[str],
    current_working_dir: Optional[str],
    metrics: Optional[Dict[Any, Any]],
) -> None:
    """
    Args:
        model_name (str): name of the model you want to validate.

        model_type (str): Type of model you want to validate. currently supporting are scikit-learn, xgboost, catboost, lightgbm, prophet, keras, custom-model
        Note: When you are validating/logging models supported by scikit-learn, please use scikit-learn as model_type

        model (Any): Object of model that you want to log/validate.

        artifact_path (Optional[str]): Location where you want to log the model.

        current_working_dir (Optional[str]): Loction of your current working directory.

        metrics (Optional[dict]): Dictionary of (metric_name, value) of the model you want to log.
    """
    if not model_name:
        raise ValueError("model_name cannot be null or empty string")
    if not isinstance(model_name, str):
        raise TypeError("model_type must be of type string.")

    if not model_type:
        raise ValueError("model_type cannot be null or empty string")
    if not isinstance(model_type, str):
        # TODO: prophet model logging will be supported only when there is stable fbprophet package installation will happen
        raise TypeError(
            """model_type must be of type string.
            Choose from currently supported models: ['scikit-learn', 'xgboost', 'catboost', 'lightgbm', 'prophet', 'keras', 'custom-model']"""
        )
    if model_type.lower() not in [
        "scikit-learn",
        "xgboost",
        "catboost",
        "lightgbm",
        "keras",
        "custom-model",
    ]:
        # TODO: prophet model logging will be supported only when there is stable fbprophet package installation will happen
        raise ValueError(
            "model_type must be from ['scikit-learn', 'xgboost', 'catboost', 'lightgbm', 'keras', 'prophet', 'custom-model']"
        )
    if not model:
        raise ValueError(
            "model cannot be empty. Pass the object of the model you want save"
        )

    if artifact_path and not isinstance(artifact_path, str):
        raise TypeError("artifact_path must be of type string ")

    if current_working_dir and not isinstance(current_working_dir, str):
        raise TypeError("current_working_dir must be of type string")
    if metrics and not isinstance(metrics, dict):
        raise TypeError(
            "Pass your metrics in dictionary format key: value as mertic_name: value"
        )


class LogModel(MLClient):
    def __init__(self, experiment_name: str):
        """
        Args:
            experiment_name (str): Name of the experiment for logging.
        """
        if not experiment_name:
            raise ValueError("experiment_name cannot be null or empty string")

        if not isinstance(experiment_name, str):
            raise ValueError("experiment_name must be string")

        super().__init__(experiment_name)

        self.model_name = ""
        self.artifact_path_name = "no_model_path"
        self.model_type = ""
        self.model = None
        self.current_working_dir = ""
        self.model_metrics: Dict[Any, Any] = {}
        self.experiment_name = experiment_name
        self.username = os.getenv("EXP_USER") or "default"
        self.model_uri = None

    def __log_model_metrics(self):
        """
        This function logs the model metrics.
        """
        logger.info(f"logged params: {self.model_metrics.keys()}")
        try:
            mlflow.log_metrics(self.model_metrics)
        except Exception:
            logger.warning("Couldn't perform log_metrics. Exception:")
            logger.warning(traceback.format_exc())

    def __log_keras_model(self) -> None:
        """
        This functions helps to save/log the keras models and also all the experimentation input, results from your current directory.
        Supporting models are tensorflow"s keras model.
        """
        with mlflow.start_run(run_name="keras-model"):
            mlflow.set_tag("mlflow.user", self.username)
            mlflow.keras.log_model(self.model, self.artifact_path_name)
            if self.current_working_dir:
                mlflow.log_artifact(self.current_working_dir, self.artifact_path_name)

            self.model_uri = mlflow.get_artifact_uri(self.artifact_path_name)
            if self.model_metrics:
                self.__log_model_metrics()

    def __log_catboost_model(self) -> None:
        """
        This functions helps to save/log the catboost model and also all the experimentation input, results from your current directory.
        """
        with mlflow.start_run(run_name="catboost-model"):
            mlflow.set_tag("mlflow.user", self.username)
            mlflow.catboost.log_model(self.model, self.artifact_path_name)
            if self.current_working_dir:
                mlflow.log_artifact(self.current_working_dir, self.artifact_path_name)
            self.model_uri = mlflow.get_artifact_uri(self.artifact_path_name)
            if self.model_metrics:
                self.__log_model_metrics()

    def __log_sklearn_model(self) -> None:
        """
        This functions helps to save/log the sklearn models and also all the experimentation input, results from your current directory.
        Supporting models are all scikit-learn models, xgboost, lightgbm.
        """
        with mlflow.start_run(run_name="scikit-learn-model"):
            mlflow.set_tag("mlflow.user", self.username)
            mlflow.sklearn.log_model(self.model, self.artifact_path_name)
            if self.current_working_dir:
                mlflow.log_artifact(self.current_working_dir, self.artifact_path_name)
            self.model_uri = mlflow.get_artifact_uri(self.artifact_path_name)
            if self.model_metrics:
                self.__log_model_metrics()

    def __log_custom_model(self) -> None:
        """
        This functions helps to save/log your custom models and also all the experimentation input, results from your current directory.
        """
        with mlflow.start_run(run_name="custom-model"):
            mlflow.set_tag("mlflow.user", self.username)
            mlflow.pyfunc.log_model(self.artifact_path_name, python_model=self.model)
            if self.current_working_dir:
                mlflow.log_artifact(self.current_working_dir, self.artifact_path_name)
            self.model_uri = mlflow.get_artifact_uri(self.artifact_path_name)
            if self.model_metrics:
                self.__log_model_metrics()

    def model_logging(
        self,
        model_name: str,
        model_type: str,
        model: Any,
        artifact_path: Optional[str] = None,
        current_working_dir: Optional[str] = None,
        metrics: Optional[Dict[Any, Any]] = None,
    ) -> None:
        """
        This function helps to log different types of user model.

        Args:
            model_name (str): name of the model you want to log. eg: linear_regression

            model_type (str): Type of model you want to save. currently supporting are scikit-learn, xgboost, catboost, lightgbm, prophet, keras, custom-model
            Note: When you are logging models supported by scikit-learn, please use scikit-learn as model_type

            model (Any): Object of model that you want to log.

            artifact_path (Optional[str]): Location where you want to log the model

            current_working_dir (Optional[str]): Loction of your current working directory.

            metrics (Optional[dict]): Dictionary of (metric_name, value) of the model you want to log.
        """
        # TODO: prophet model logging will be supported only when there is stable fbprophet package installation will happen
        self.reset()
        logger.info("Validation Start")
        misc_input_validation(
            model_name, model_type, model, artifact_path, current_working_dir, metrics
        )
        logger.info("Validation End")

        self.model_name = model_name

        if artifact_path:
            self.artifact_path_name = (
                f"{self.name}_{self.id}_{artifact_path}_{self.model_name}"
            )

        else:
            self.artifact_path_name = f"{self.name}_{self.id}_{self.model_name}"

        if metrics:
            self.model_metrics = metrics
        self.model_type = model_type
        self.model = model

        if current_working_dir:
            self.current_working_dir = current_working_dir

        if self.model_type.lower() in {
            "scikit-learn",
            "xgboost",
            "lightgbm",
            "prophet",
        }:
            # TODO: prophet model logging will be supported only when there is stable fbprophet package installation will happen
            logger.info(f"-----------{self.model_name}--------------")
            try:
                self.__log_sklearn_model()
                print(f"Model artifact logged to: {self.model_uri}")
            except Exception:
                logger.warning("Couldn't log the model. Exception:")
                logger.warning(traceback.format_exc())

        elif self.model_type.lower() == "keras":
            logger.info(f"-----------{self.model_name}--------------")
            try:
                self.__log_keras_model()
                print(f"Model artifact logged to: {self.model_uri}")
            except Exception:
                logger.warning("Couldn't log the model. Exception:")
                logger.warning(traceback.format_exc())

        elif self.model_type.lower() == "catboost":
            logger.info(f"-----------{self.model_name}--------------")
            try:
                self.__log_catboost_model()
                print(f"Model artifact logged to: {self.model_uri}")
            except Exception:
                logger.warning("Couldn't log the model. Exception:")
                logger.warning(traceback.format_exc())

        elif self.model_type.lower() == "custom-model":
            logger.info(f"-----------{self.model_name}--------------")
            try:
                self.__log_custom_model()
                print(f"Model artifact logged to: {self.model_uri}")
            except Exception:
                logger.warning("Couldn't log the model. Exception:")
                logger.warning(traceback.format_exc())

    def model_loading(self, model_location: str):
        """
        This function loads model from a run.

        Args:
            model_location (str): The location, in URI format, of the model.
        """
        try:
            return mlflow.pyfunc.load_model(model_location)
        except Exception:
            print(
                f"Could  not load the model, Make sure you saved it under the location {model_location}"
            )

    def reset(self):
        self.model_name = ""
        self.artifact_path_name = "no_model_path"
        self.model_type = ""
        self.model = None
        self.current_working_dir = ""
        self.model_uri = None
        self.model_metrics = {}
