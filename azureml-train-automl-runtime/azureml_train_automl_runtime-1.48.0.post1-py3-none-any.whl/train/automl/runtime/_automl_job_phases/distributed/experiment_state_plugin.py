# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Plugin for experiment state for distributed run."""
from typing import Any, Callable

from dask.distributed import WorkerPlugin

from azureml.data import TabularDataset
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings


class ExperimentStatePlugin(WorkerPlugin):
    def __init__(self, workspace_getter: Callable[..., Any],
                 parent_run_id: str,
                 training_dataset: TabularDataset,
                 validation_dataset: TabularDataset,
                 automl_settings: AzureAutoMLSettings):
        self.workspace_getter = workspace_getter
        self.parent_run_id = parent_run_id
        self.training_dataset = TabularDataset._create(training_dataset._dataflow,
                                                       training_dataset._properties,
                                                       telemetry_info=training_dataset._telemetry_info)
        self.validation_dataset = TabularDataset._create(validation_dataset._dataflow,
                                                         validation_dataset._properties,
                                                         telemetry_info=validation_dataset._telemetry_info)\
            if validation_dataset is not None else None
        self.automl_settings = automl_settings
