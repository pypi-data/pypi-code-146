# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
import os
import uuid
from typing import Any, Callable, Tuple

import pandas as pd
import dask
from azureml._tracing._tracer_factory import get_tracer
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared.constants import Tasks, RuleBasedValidation
from azureml.automl.runtime._data_preparation import data_preparation_utilities
from azureml.automl.runtime.experiment_store import ExperimentStore
from azureml.core import Run
from azureml.data import TabularDataset
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings
from azureml.train.automl.runtime._automl_job_phases import ExperimentPreparationPhase, PhaseUtil
from azureml.train.automl.runtime._automl_job_phases.distributed.constants import RowCountsForClassificationRegression
from azureml.train.automl.runtime._worker_initiator import EXPERIMENT_STATE_PLUGIN, get_worker_variables
from dask.distributed import get_worker
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)
tracer = get_tracer(__name__)


class ClassificationRegressionDistributedPreparationPhase:
    """AutoML job phase that prepares the data."""

    @staticmethod
    def run(workspace_getter: Callable[..., Any],
            current_run: Run,
            parent_run_id: str,
            automl_settings: AzureAutoMLSettings,
            training_dataset: TabularDataset,
            validation_dataset: TabularDataset) -> None:

            PhaseUtil.log_with_memory("Beginning distributed preparation")

            validation_split_required = not validation_dataset
            test_split_required = automl_settings.test_size > 0.0
            logger.info("Validation split required :{}\n"
                        "Test split required :{}".format(validation_split_required, test_split_required))

            if validation_split_required or test_split_required:
                training_ddf = training_dataset.to_dask_dataframe()
                prepared_data_dir = '{}_{}_prepared_{}'.format(current_run.experiment.name,
                                                               parent_run_id,
                                                               str(uuid.uuid4()))

                if validation_split_required:
                    validation_size_to_use = automl_settings.validation_size if automl_settings.validation_size > 0.0 \
                        else RuleBasedValidation.DEFAULT_TRAIN_VALIDATE_TEST_SIZE
                else:
                    validation_size_to_use = 0

                logger.info("Splitting dataset\n"
                            "Validation split size :{}\n"
                            "Test split size :{}".format(validation_size_to_use, automl_settings.test_size))
                split_distributed(training_ddf,
                                  prepared_data_dir,
                                  validation_size_to_use,
                                  automl_settings.test_size,
                                  automl_settings.task_type,
                                  automl_settings.label_column_name)

                PhaseUtil.log_with_memory("Ending distributed splitting")

                expr_store = ExperimentStore.get_instance()
                with logging_utilities.log_activity(logger=logger, activity_name='SavingPreparedTrainDataset'):
                    expr_store.data.partitioned.save_prepared_train_dataset(
                        workspace_getter(),
                        prepared_data_dir + "/train/*.parquet",
                        []
                    )
                training_dataset = expr_store.data.partitioned.get_prepared_train_dataset(workspace_getter())

                if validation_split_required:
                    with logging_utilities.log_activity(logger=logger,
                                                        activity_name='SavingPreparedValidationDataset'):
                        expr_store.data.partitioned.save_prepared_valid_dataset(
                            workspace_getter(),
                            prepared_data_dir + "/validation/*.parquet",
                            []
                        )
                        validation_dataset = expr_store.data.partitioned.get_prepared_valid_dataset(workspace_getter())

                if test_split_required:
                    with logging_utilities.log_activity(logger=logger, activity_name='SavingPreparedTestDataset'):
                        expr_store.data.partitioned.save_prepared_test_dataset(
                            workspace_getter(),
                            prepared_data_dir + "/test/*.parquet",
                            []
                        )

            with logging_utilities.log_activity(logger=logger, activity_name='ValidatingExperimentData'):
                validate_experiment_data(training_dataset, validation_dataset, automl_settings)

            PhaseUtil.log_with_memory("Ending distributed preparation")


def split_distributed(training_ddf: dask.dataframe,
                      prepared_data_dir: str,
                      validation_size: float,
                      test_size: float,
                      task_type: str,
                      label_column_name: str) -> None:

    # kick off splitting
    training_ddf.map_partitions(split_one_partition,
                                prepared_data_dir,
                                validation_size,
                                test_size,
                                task_type,
                                label_column_name,
                                meta=bool).compute()


def split_one_partition(train_df: pd.DataFrame,
                        prepared_data_dir: str,
                        validation_size: float,
                        test_size: float,
                        task_type: str,
                        label_column_name: str) -> bool:

    unique_task_id = f"split_one_partition - {str(uuid.uuid4())}"
    with logging_utilities.log_activity(logger=logger, activity_name=unique_task_id):
        worker = get_worker()
        experiment_state_plugin = worker.plugins[EXPERIMENT_STATE_PLUGIN]
        default_datastore_for_worker, workspace_for_worker, expr_store_for_worker = get_worker_variables(
            experiment_state_plugin.workspace_getter, experiment_state_plugin.parent_run_id)

        os.makedirs(prepared_data_dir, exist_ok=True)

        if train_df.empty:
            return False

        test_df = None
        validation_df = None

        if test_size > 0.0:
            train_df, test_df = split_dataframe(train_df, label_column_name, test_size, task_type)

        if validation_size > 0.0:
            train_df, validation_df = split_dataframe(train_df, label_column_name, validation_size, task_type)

        for prepared_data, split in \
                zip([train_df, validation_df, test_df], ['train', 'validation', 'test']):

            if prepared_data is not None:
                prepared_data.reset_index(inplace=True, drop=True)
                prepared_file_name = '{}-{}.parquet'.format(split, str(uuid.uuid4()))
                prepared_file_path = '{}/{}'.format(prepared_data_dir, prepared_file_name)
                prepared_data.to_parquet(prepared_file_path)

                # construct the path to which data will be written to on the default blob store
                target_path_array = [prepared_data_dir, split]
                target_path = '/'.join(target_path_array)

                # upload data to default store
                expr_store_for_worker.data.partitioned.write_file(prepared_file_path, target_path)

                logger.info("finished uploading split data for one {} partition".format(split))

        return True


def split_dataframe(df: pd.DataFrame,
                    label_column_name: str,
                    split_ratio: float,
                    task_type: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    split_succeeded = False
    try:
        if task_type == Tasks.CLASSIFICATION:
            # try splitting with stratification
            y = df[label_column_name]
            train_df, test_df = train_test_split(df, stratify=y, test_size=split_ratio)
            split_succeeded = True
    except Exception as e:
        logging_utilities.log_traceback(e, logger)
        logger.warning("Stratified split failed. Falling back to random.")

    if not split_succeeded:
        # try splitting without stratification
        train_df, test_df = train_test_split(df, test_size=split_ratio)

    return train_df, test_df


def validate_experiment_data(training_data, validation_data, automl_settings):
    raw_experiment_data = data_preparation_utilities._get_raw_experiment_data_from_training_data(
        training_data.take(RowCountsForClassificationRegression.ForValidation),
        automl_settings,
        validation_data.take(RowCountsForClassificationRegression.ForValidation))

    ExperimentPreparationPhase._validate_training_data(raw_experiment_data, automl_settings)
