#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#
import os

import mlflow
import pandas as pd


mlflow.set_tracking_uri(os.environ["MLFLOW_BASE_URL"])
client = mlflow.tracking.MlflowClient(os.environ["MLFLOW_BASE_URL"])


def get_exp(exp_name: str):
    """
    Retrieve an experiment by experiment name from the backend store.

    Args:
        exp_name (str): The case senstive experiment name.
    """
    mlflow.set_experiment(exp_name)
    exp_details = mlflow.get_experiment_by_name(exp_name)
    result = {
        "experiment_name": exp_details.name,
        "location": exp_details.artifact_location,
        "experiment_id": exp_details.experiment_id,
        "experiment_stage": exp_details.lifecycle_stage,
        "tags": exp_details.tags,
    }

    return pd.DataFrame.from_dict(result, orient="index", columns=["parameters"])


def previous_version(model_name: str):
    """
    Return list of all previous versions.

    Args:
        model_name (str): name of the model.
    """
    filter_string = f"name='{model_name}'"
    all_versions = [
        int(dict(x)["version"]) for x in client.search_model_versions(filter_string)
    ]

    all_versions.sort()
    # previous_versions
    return list(map(lambda x: str(x), all_versions))[:-1]


# A decorator function to alter doc strings
def add_doc(value):
    def _doc(func):
        func.__doc__ = func.__doc__ + value
        return func

    return _doc
