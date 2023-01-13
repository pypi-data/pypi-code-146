#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#
import logging
import os
from typing import Any
from typing import List

import joblib
import mlflow
from katonic.version import get_version


mlflow.set_tracking_uri(os.environ["MLFLOW_BASE_URL"])
client = mlflow.tracking.MlflowClient(os.environ["MLFLOW_BASE_URL"])
logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


def set_exp(exp_name: str) -> Any:
    """
    Set given experiment as active experiment. If experiment does not exist, create an experiment with provided name.

    Args:
        exp_name (str): Case sensitive name of an experiment to be activated.
    """
    return mlflow.set_experiment(exp_name)


class MLClient:
    """
    A MLClient Object is used to define, create a experiment.

    Args:
        exp_name (str): Case sensitive name of an experiment to be activated.
    """

    def __init__(self, exp_name: str):

        if not isinstance(exp_name, str):
            raise ValueError("exp_name must be string")
        if not exp_name:
            raise ValueError("exp_name cannot be null or empty string")

        set_exp(exp_name)

        exp_details = mlflow.get_experiment_by_name(exp_name)
        self.name = exp_details.name
        self.location = exp_details.artifact_location
        self.id = exp_details.experiment_id
        self.stage = exp_details.lifecycle_stage
        self.tag = exp_details.tags
        logger.info("MLClient successfully instantiated")

    def search_runs(self, exp_id: str):
        """
        This function search runs and return dataframe of runs. It takes exp_id as input
        and returns the list of experiment ids.

        Args:
            exp_id (List[str]): List of experiment IDs. None will default to the active experiment

        Returns:
            A list of experiment ids
        """
        try:
            df = mlflow.search_runs(experiment_ids=exp_id)
            df.columns = df.columns.str.replace("tags.mlflow.runName", "run_name")
            exclude_cols = [
                "tags.mlflow.source.type",
                "tags.mlflow.user",
                "tags.mlflow.source.name",
            ]
            df = df[df.columns.difference(exclude_cols)]
            return df
        except Exception:
            print(f"Experiment id {exp_id} does not exists")

    def register_model(self, model_name: str, run_id: str) -> Any:
        """
        This function register the given model in model registry and create a new version of it (if not registered).

        Args:
            model_name (str): name of the model.
            run_id (str): experiment id.

        Returns:
            A single ModelVersion object.
        """
        try:
            client.create_registered_model(model_name)
            result = client.create_model_version(
                name=model_name,
                source=f"{self.location}/{run_id}/artifacts/{model_name}",
                run_id=run_id,
            )
            return result.to_proto()
        except Exception:
            print(f"Could not register the model {model_name} with run_id {run_id}")

    def change_stage(self, model_name: str, ver_list: List[str], stage: str) -> Any:
        """
        This function changes stage of model. (Staging, Production or Archived).

        Args:
            model_name (str): name of the model.
            ver_list (List[str]): version list of the model.
            stage (str): Staging, Production and archived.
        """
        try:
            list(
                map(
                    lambda x: client.transition_model_version_stage(  # type: ignore
                        name=model_name, version=x, stage=stage
                    ),
                    ver_list,
                )
            )
        except Exception:
            print(
                f"Could not change the stage of model {model_name} for versions {ver_list} "
            )

    def model_versions(self, model_name: str) -> Any:
        """
        This function returns the model versions if match with filter string.

        Args:
            model_name (str): Name of the model taken as input string.
        """
        try:
            filter_string = f"name='{model_name}'"
            results = client.search_model_versions(filter_string)
        except Exception:
            print(
                f"Could not get the versions of model {model_name}. Try another name "
            )
        return list(map(lambda x: x.version, results))  # type: ignore

    def log_data(self, prun_id: str, data_obj, location: str) -> None:
        """
        This function stores joblib objects in model artifact.

        Args:
            prun_id (str): run_id of experiment.
            data_obj (Any): class object of any transformation function.
            location (str): location where the artifact will be logged.
        """
        joblib.dump(data_obj, location)
        with mlflow.start_run(run_id=prun_id):
            mlflow.log_artifact(location, artifact_path=f"model/{location}/")

    def delete_model_version(self, model_name: str, ver_list: List[str]) -> Any:
        """
        This function deletes model versions.

        Args:
            model_name (str) : name of the model
            ver_list (List[str]): list of all it"s versions.
        """
        try:
            list(
                map(
                    lambda version: client.delete_model_version(  # type: ignore
                        name=model_name, version=version
                    ),
                    ver_list,
                )
            )
        except Exception:
            print(
                f"Could not delete the respective versions {ver_list} of model {model_name}. Make sure the versions or model exists"
            )

    def delete_reg_model(self, model_name: str):
        """
        This function deletes registered model with all its version.

        Args:
            model_name (str): Name of the registered model to update.
        """
        try:
            return client.delete_registered_model(name=model_name)
        except Exception:
            print(
                f"Could not delete the registered model {model_name}. Make sure the model is registered"
            )

    def delete_run_by_id(self, run_ids: List[Any]) -> Any:
        """
        delete runs with the specific run_ids.

        Args:
            run_ids (List): The unique run ids to delete.
        """
        try:
            list(map(lambda run: client.delete_run(run_id=run), run_ids))  # type: ignore
            return f"{run_ids} runids successfully deleted"
        except Exception:
            print(f"Could not delete run_ids {run_ids}. Make sure they exits")

    def load_model(self, location):
        """
        Load a scikit-learn model from a local file or a run.

        Args:
            location: The location, in URI format, of the model, for example:

                        - ``/Users/me/path/to/local/model``
                        - ``relative/path/to/local/model``
                        - ``s3://my_bucket/path/to/model``
                        - ``runs:/<run_id>/run-relative/path/to/model``
                        - ``models:/<model_name>/<model_version>``
                        - ``models:/<model_name>/<stage>``

        Returns:
            A scikit-learn model.
        """
        try:
            return mlflow.sklearn.load_model(location)
        except Exception:
            print(
                f"Could  not load the model, Make sure you saved it under the location {location}"
            )

    def version(self) -> str:
        """Returns the version of the current Katonic SDK."""
        return get_version()  # type: ignore
