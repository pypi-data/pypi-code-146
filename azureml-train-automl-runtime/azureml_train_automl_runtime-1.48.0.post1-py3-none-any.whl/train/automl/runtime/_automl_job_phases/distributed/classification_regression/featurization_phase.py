# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
import logging
import os
import uuid
from typing import Any, Callable, Dict, List, Optional, Tuple

import azureml.dataprep as dprep
import dask
import numpy as np
import pandas as pd
from azureml._tracing._tracer_factory import get_tracer
from azureml.automl.core import inference
from azureml.automl.core.constants import FeatureType
from azureml.automl.core.featurization import FeaturizationConfig
from azureml.automl.core.shared import constants, logging_utilities
from azureml.automl.runtime import data_cleaning
from azureml.automl.runtime import data_transformation
from azureml.automl.runtime._runtime_params import ExperimentControlSettings
from azureml.automl.runtime.data_transformation import _y_transform
from azureml.automl.runtime.distributed.utilities import to_dask_dataframe
from azureml.automl.runtime.experiment_store import ExperimentStore
from azureml.automl.runtime.faults_verifier import VerifierManager
from azureml.automl.runtime.featurization import DataTransformer
from azureml.automl.runtime.featurizer.transformer.featurization_utilities import get_prediction_transform_type, \
    skip_featurization
from azureml.automl.runtime.shared._dataset_binning import make_dataset_bins
from azureml.automl.runtime.shared.problem_info import ProblemInfo
from azureml.core import Run
from azureml.data import TabularDataset
from azureml.train.automl import _constants_azureml
from azureml.train.automl._azureautomlsettings import AzureAutoMLSettings
from azureml.train.automl.runtime._automl_job_phases.distributed.constants import RowCountsForClassificationRegression
from azureml.train.automl.runtime._automl_job_phases.utilities import PhaseUtil
from azureml.train.automl.runtime._worker_initiator import EXPERIMENT_STATE_PLUGIN, get_worker_variables
from dask.distributed import get_worker
from sklearn.base import TransformerMixin

logger = logging.getLogger(__name__)
tracer = get_tracer(__name__)


class _PartitionTransformResult(object):
    """
    Data class that captures the results of transforming one partition
    """
    def __init__(self,
                 rows_begin: int,
                 rows_end: int,
                 columns_begin: int,
                 columns_end: int) -> None:
        self.rows_begin = rows_begin
        self.rows_end = rows_end
        self.columns_begin = columns_begin
        self.columns_end = columns_end


class TransformResult(object):
    """
    Data class that captures the results of transforming all partitions
    """
    def __init__(self,
                 train_total_rows_begin: int,
                 train_total_rows_end: int,
                 train_total_columns_begin: int,
                 train_total_columns_end: int,
                 validation_total_rows_begin: int,
                 validation_total_rows_end: int,
                 validation_total_columns_begin: int,
                 validation_total_columns_end: int) -> None:
        self.train_total_rows_begin = train_total_rows_begin
        self.train_total_rows_end = train_total_rows_end
        self.train_total_columns_begin = train_total_columns_begin
        self.train_total_columns_end = train_total_columns_end
        self.validation_total_rows_begin = validation_total_rows_begin
        self.validation_total_rows_end = validation_total_rows_end,
        self.validation_total_columns_begin = validation_total_columns_begin,
        self.validation_total_columns_end = validation_total_columns_end


def transform_one_partition(df: pd.DataFrame,
                            X_transformer: Optional[DataTransformer],
                            y_transformer: Optional[TransformerMixin],
                            split: str,
                            featurized_data_dir: str,
                            label_column_name: str,
                            weight_column_name: Optional[str] = None,
                            featurization_config: Optional[FeaturizationConfig] = None) -> _PartitionTransformResult:

    unique_task_id = f"transform_one_partition - {str(uuid.uuid4())}"
    with logging_utilities.log_activity(logger=logger, activity_name=unique_task_id):
        worker = get_worker()
        experiment_state_plugin = worker.plugins[EXPERIMENT_STATE_PLUGIN]
        default_datastore_for_worker, workspace_for_worker, expr_store_for_worker = get_worker_variables(
            experiment_state_plugin.workspace_getter, experiment_state_plugin.parent_run_id)

        os.makedirs(featurized_data_dir, exist_ok=True)
        columns_to_drop = [label_column_name]

        if df.empty:
            return _PartitionTransformResult(0, 0, 0, 0)

        w = None
        if weight_column_name:
            columns_to_drop.append(weight_column_name)
            w = df[weight_column_name].values

        y = df[label_column_name].values
        X = df.drop(columns=columns_to_drop)

        X, y, w = data_cleaning._remove_nan_rows_in_X_y(X, y, w,
                                                        is_timeseries=False,
                                                        target_column=label_column_name,
                                                        featurization_config=featurization_config)
        if X.empty:
            # cleaning of data can result in zero rows
            return _PartitionTransformResult(df.shape[0], 0, df.shape[1], df.shape[1])

        y = pd.DataFrame(y, columns=[label_column_name])
        if w is not None:
            w = pd.DataFrame(w, columns=[weight_column_name])

        # transform X
        if X_transformer:
            transformed_X_array = X_transformer.transform(X)
            transformed_X = pd.DataFrame(transformed_X_array,
                                         columns=X_transformer.get_engineered_feature_names(),
                                         dtype=object)
        else:
            transformed_X = X

        # transform y
        if y_transformer:
            y_array = y_transformer.transform(y)
            transformed_y = pd.DataFrame(y_array, columns=[label_column_name])
            logger.info("finished transforming Y for one {} partition".format(split))
        else:
            transformed_y = y

        # join transformed dataframes
        dataframes_to_join = [transformed_X]
        if weight_column_name:
            dataframes_to_join.append(w)
        dataframes_to_join.append(transformed_y)
        transformed_data = pd.concat(dataframes_to_join, axis=1)

        transformed_data.reset_index(inplace=True, drop=True)
        featurized_file_name = '{}-{}.parquet'.format(split, str(uuid.uuid4()))
        featurized_file_path = '{}/{}'.format(featurized_data_dir, featurized_file_name)
        transformed_data.to_parquet(featurized_file_path)

        # construct the path to which data will be written to on the default blob store
        target_path_array = [featurized_data_dir, split]
        target_path = '/'.join(target_path_array)

        # upload data to default store
        expr_store_for_worker.data.partitioned.write_file(featurized_file_path, target_path)
        logger.info("Finished transforming and uploading one {} partition".format(split))

        return _PartitionTransformResult(df.shape[0],
                                         transformed_data.shape[0],
                                         df.shape[1],
                                         transformed_data.shape[1])


class ClassificationRegressionDistributedFeaturizationPhase:
    """AutoML distributed job phase that prepares the data."""

    @staticmethod
    def run(workspace_getter: Callable[..., Any],
            current_run: Run,
            parent_run_id: str,
            automl_settings: AzureAutoMLSettings,
            training_dataset: TabularDataset,
            validation_dataset: TabularDataset,
            verifier: VerifierManager) -> None:

        PhaseUtil.log_with_memory("Beginning distributed featurization")

        training_ddf = to_dask_dataframe(training_dataset._dataflow)
        validation_ddf = to_dask_dataframe(validation_dataset._dataflow)

        # step 1 - get suggestions for transformers
        with logging_utilities.log_activity(logger=logger, activity_name='suggest_transformers'):
            X_transformer, y_transformer = get_suggestions_and_fit_transformers(
                training_dataset,
                training_ddf,
                automl_settings.task_type,
                automl_settings.label_column_name,
                automl_settings.weight_column_name,
                automl_settings.featurization)

        # step 2 - kick of distributed featurization
        with logging_utilities.log_activity(logger=logger, activity_name='transform_data_distributed'):
            featurized_data_dir = '{}_{}_featurized_{}'.format(current_run.experiment.name,
                                                               parent_run_id,
                                                               str(uuid.uuid4()))
            transform_result = transform_data_distributed(training_ddf,
                                                          validation_ddf,
                                                          X_transformer,
                                                          y_transformer,
                                                          featurized_data_dir,
                                                          automl_settings.label_column_name,
                                                          automl_settings.weight_column_name,
                                                          automl_settings.featurization)
            PhaseUtil.log_with_memory("distributed transformation done.")

        # step 3 - Populate run and experiment store properties for use by training
        with logging_utilities.log_activity(logger=logger, activity_name='Save transformer, dataset, probleminfo'):
            expr_store = ExperimentStore.get_instance()

            # transformers. Both X and y transformers can be None
            transformers = {}  # type: Dict[str, TransformerMixin]
            transformers[constants.Transformers.X_TRANSFORMER] = X_transformer
            transformers[constants.Transformers.Y_TRANSFORMER] = y_transformer
            expr_store.transformers.set_transformers(transformers)

            unique_label_count = 0
            if automl_settings.task_type == constants.Tasks.CLASSIFICATION:
                assert y_transformer is not None
                unique_label_count = len(y_transformer.classes_)

            # problem info
            problem_info_dict = {"is_sparse": False,
                                 "subsampling": False,
                                 "dataset_classes": unique_label_count,
                                 "dataset_features": transform_result.train_total_columns_end,
                                 "dataset_samples": transform_result.train_total_rows_end}
            problem_info_str = json.dumps(problem_info_dict)
            current_run.add_properties({
                _constants_azureml.Properties.PROBLEM_INFO: problem_info_str
            })

            with logging_utilities.log_activity(logger=logger, activity_name='SavingFeaturizedTrainDataset'):
                expr_store.data.partitioned.save_featurized_train_dataset(
                    workspace_getter(),
                    featurized_data_dir + "/train/*.parquet",
                    []
                )

            with logging_utilities.log_activity(logger=logger, activity_name='SavingFeaturizedValidationDataset'):
                expr_store.data.partitioned.save_featurized_valid_dataset(
                    workspace_getter(),
                    featurized_data_dir + "/validation/*.parquet",
                    []
                )

            if verifier is not None and X_transformer is not None:
                verifier.update_data_verifier_for_missing_values(X_transformer)
                verifier.update_data_verifier_for_high_cardinal_features(X_transformer.stats_and_column_purposes)

            set_experiment_store_properties(
                expr_store,
                automl_settings,
                None if X_transformer is None else X_transformer._get_label_encoded_column_indexes(),
                transform_result.train_total_rows_end,
                transform_result.train_total_columns_end,
                unique_label_count,
                training_dataset._dataflow,
                validation_dataset._dataflow,
                expr_store.data.partitioned.get_featurized_train_dataset(workspace_getter())._dataflow,
                expr_store.data.partitioned.get_featurized_valid_dataset(workspace_getter())._dataflow)

            PhaseUtil.log_with_memory("Ending distributed featurization")


def transform_data_distributed(training_ddf: dask.dataframe,
                               validation_ddf: dask.dataframe,
                               X_transformer: Optional[DataTransformer],
                               y_transformer: Optional[TransformerMixin],
                               featurized_data_dir: str,
                               label_column_name: str,
                               weight_column_name: Optional[str] = None,
                               featurization_config: Optional[FeaturizationConfig] = None) -> TransformResult:

    # kick off distributed transformation using the fitted transformer
    train_transform_result = training_ddf.map_partitions(transform_one_partition,
                                                         X_transformer,
                                                         y_transformer,
                                                         'train',
                                                         featurized_data_dir,
                                                         label_column_name,
                                                         weight_column_name,
                                                         featurization_config,
                                                         meta=_PartitionTransformResult).compute()

    validation_transform_result = validation_ddf.map_partitions(transform_one_partition,
                                                                X_transformer,
                                                                y_transformer,
                                                                'validation',
                                                                featurized_data_dir,
                                                                label_column_name,
                                                                weight_column_name,
                                                                featurization_config,
                                                                meta=_PartitionTransformResult).compute()
    transform_result = TransformResult(sum([p.rows_begin for p in train_transform_result]),
                                       sum([p.rows_end for p in train_transform_result]),
                                       train_transform_result[0].columns_begin,
                                       train_transform_result[0].columns_end,
                                       sum([p.rows_begin for p in validation_transform_result]),
                                       sum([p.rows_end for p in validation_transform_result]),
                                       validation_transform_result[0].columns_begin,
                                       validation_transform_result[0].columns_end)

    logger.info("Featurization summary below")
    logger.info(json.dumps(transform_result.__dict__))
    logger.info("dask partitions for train {}".format(len(train_transform_result)))
    logger.info("dask partitions for validation {}".format(len(validation_transform_result)))

    return transform_result


def get_suggestions_and_fit_transformers(
        training_dataset: TabularDataset,
        training_ddf: dask.dataframe,
        task_type: str,
        label_column_name: str,
        weight_column_name: str,
        featurization_config: FeaturizationConfig) -> Tuple[Optional[DataTransformer], Optional[TransformerMixin]]:

    # We combine all distributed operations. This is required to let DASK achieve highest performance
    distributed_operations = []
    X_transformer = None
    y_transformer = None

    columns_to_drop = [label_column_name]
    if weight_column_name is not None:
        columns_to_drop.append(weight_column_name)

    sampled_training_df = training_dataset\
        .take(RowCountsForClassificationRegression.ForSuggestion)\
        .to_pandas_dataframe()
    subsampled_X = sampled_training_df.drop(columns=columns_to_drop)
    subsampled_y = sampled_training_df[label_column_name]

    if not skip_featurization(featurization_config, False):
        X_transformer = data_transformation._suggest_featurizers_and_create_datatransformer(
            task=task_type,
            X=subsampled_X,
            y=subsampled_y,
            enable_feature_sweeping=False,
            is_cross_validation=False,
            for_distributed_featurization=True
        )

        # 2 important things here
        # this fit_transform is fake - we do it just to make things work for subsequent workflows.
        # Some fitted featurizers learnt values will be overwritten later in the workflow
        # Transform is required to make engineered feature names work
        X_transformer.fit_transform(subsampled_X.head(RowCountsForClassificationRegression.ForFakeFitTransform),
                                    subsampled_y.head(RowCountsForClassificationRegression.ForFakeFitTransform))

        assert X_transformer.stats_and_column_purposes is not None
        for stat, cp, c in X_transformer.stats_and_column_purposes:
            if cp == FeatureType.Categorical or cp == FeatureType.CategoricalHash:
                # astype('category') handles the case where numerical column is deduced to be a categorical
                ddf_c = training_ddf[c].astype('category')
                distributed_operations.append(ddf_c.unique())
                distributed_operations.append(ddf_c.describe())
            elif cp == FeatureType.Numeric:
                tr_map = next(tr_map for tr_map in X_transformer.transformer_and_mapper_list
                              if c == tr_map.mapper.built_features[0][0][0])
                if tr_map.transformers[0].strategy == 'mean' or tr_map.transformers[0].strategy == 'median':
                    distributed_operations.append(training_ddf[c].describe())
                elif tr_map.transformers[0].stretegy == 'most_frequent':
                    distributed_operations.append(training_ddf[c].mode(dropna=True))

    # We do 2 things irrespective of featurization is turned on or off
    # 1. drop NA labels (done as part of data cleaning)
    # 2. Build a y transformer
    pred_transform_type = get_prediction_transform_type(featurization_config)
    y_transformer, _, _ = _y_transform(subsampled_y[~pd.isna(subsampled_y)], None, task_type, pred_transform_type)
    if task_type == constants.Tasks.CLASSIFICATION:
        assert y_transformer is not None
        distributed_operations.append(training_ddf[label_column_name].unique())

    if distributed_operations:
        all_statistics = dask.compute(*distributed_operations)  # type: List[Any]

        # We calculate statistics in distributed manner so we can overwrite fitted featurizers with values we learnt
        # Dask returns results in the same order that we requested it to
        # Hence we traverse the results in the same order
        # Note that the for loops above and below match exactly and it is required to traverse things in order
        stat_index = 0
        if X_transformer:

            assert X_transformer.stats_and_column_purposes is not None
            for stat, cp, c in X_transformer.stats_and_column_purposes:
                if cp == FeatureType.Categorical or cp == FeatureType.CategoricalHash:
                    tr_map = next(tr_map for tr_map in X_transformer.transformer_and_mapper_list
                                  if c == tr_map.mapper.built_features[0][0])

                    logger.info('overwriting label encoder with classes that we learnt')
                    unique_classes = all_statistics[stat_index]
                    unique_classes = unique_classes[~pd.isna(unique_classes)]
                    tr_map.transformers[2]._label_encoder.classes_ = np.sort(np.asarray(unique_classes).astype(str))
                    stat_index = stat_index + 1

                    logger.info('overwriting categorical imputer with mode value that we learnt')
                    tr_map.transformers[0]._fill = all_statistics[stat_index].top
                    stat_index = stat_index + 1

                elif cp == FeatureType.Numeric:
                    tr_map = next(tr_map for tr_map in X_transformer.transformer_and_mapper_list
                                  if c == tr_map.mapper.built_features[0][0][0])

                    if tr_map.transformers[0].strategy == 'mean':
                        logger.info('overwriting numerical imputer with mean value that we learnt')
                        tr_map.transformers[0].statistics_ = np.asarray([all_statistics[stat_index]['mean']])
                        stat_index = stat_index + 1

                    elif tr_map.transformers[0].strategy == 'median':
                        logger.info('overwriting numerical imputer with median value that we learnt')
                        tr_map.transformers[0].statistics_ = np.asarray([all_statistics[stat_index]['50%']])
                        stat_index = stat_index + 1

                    elif tr_map.transformers[0].stretegy == 'most_frequent':
                        logger.info('overwriting numerical imputer with mode value that we learnt')
                        tr_map.transformers[0].statistics_ = np.asarray([all_statistics[stat_index][0]])
                        stat_index = stat_index + 1

        if task_type == constants.Tasks.CLASSIFICATION:
            assert y_transformer is not None
            logger.info('Write y transformer with classes that we learnt')
            unique_classes = all_statistics[stat_index]
            unique_classes = unique_classes[~pd.isna(unique_classes)]
            y_transformer.classes_ = np.sort(np.asarray(unique_classes))

    logger.info("Finished suggesting transformers for X and y")
    return X_transformer, y_transformer


def set_experiment_store_properties(expr_store: ExperimentStore,
                                    automl_settings: AzureAutoMLSettings,
                                    label_encoded_column_indexes: Optional[List[int]],
                                    featurized_train_row_count: int,
                                    featurized_train_column_count: int,
                                    unique_label_count: int,
                                    raw_dataset: dprep.Dataflow,
                                    raw_validation_dataset: dprep.Dataflow,
                                    featurized_train_dataset: dprep.Dataflow,
                                    featurized_validation_dataset: dprep.Dataflow) -> None:

    # Step 1 -- Write lazy data section of experiment store
    logger.info("Writing experiment store with lazy featurized training and validation dataset")
    expr_store.data.lazy.set_training_dataset(
        featurized_train_dataset,
        automl_settings.label_column_name,
        automl_settings.weight_column_name,
    )
    expr_store.data.lazy.set_validation_dataset(featurized_validation_dataset)

    # Step 2 -- Write materialized data section of experiment store
    control_settings = ExperimentControlSettings(automl_settings)

    logger.info("Writing experiment store with materialized/subsampled raw train and valid dataset")
    X_raw, y_raw, w_raw = get_meterialized_xyw(
        raw_dataset,
        automl_settings.label_column_name,
        automl_settings.weight_column_name,
        automl_settings.featurization)
    X_valid_raw, y_valid_raw, w_valid_raw = get_meterialized_xyw(
        raw_validation_dataset,
        automl_settings.label_column_name,
        automl_settings.weight_column_name,
        automl_settings.featurization)
    expr_store.data.materialized.set_raw(X_raw, y_raw, X_valid_raw, y_valid_raw)

    logger.info("Writing experiment store with materialized/subsampled featurized training/validation dataset")
    X_featurized, y_featurized, w_featurized = get_meterialized_xyw(
        featurized_train_dataset,
        automl_settings.label_column_name,
        automl_settings.weight_column_name,
        automl_settings.featurization)
    X_valid_featurized, y_valid_featurized, w_valid_featurized = get_meterialized_xyw(
        featurized_validation_dataset,
        automl_settings.label_column_name,
        automl_settings.weight_column_name,
        automl_settings.featurization)
    expr_store.data.materialized.set_train(X_featurized,
                                           y_featurized,
                                           w_featurized,
                                           automl_settings.featurization)
    expr_store.data.materialized.set_valid(X_valid_featurized,
                                           y_valid_featurized,
                                           w_valid_featurized,
                                           automl_settings.featurization)

    # Step 3 -- Write metadata section of experiment store
    logger.info("Writing experiment store's metadata section")
    if automl_settings.task_type == constants.Tasks.CLASSIFICATION:
        expr_store.metadata.classification.class_labels = np.asarray(range(0, unique_label_count))
    else:
        y_valid_dflow = featurized_validation_dataset.keep_columns([automl_settings.label_column_name])
        y_valid_np = y_valid_dflow.to_pandas_dataframe().iloc[:, 0].values
        expr_store.metadata.regression.bin_info = make_dataset_bins(y_valid_np.shape[0], y_valid_np)

    expr_store.metadata.training_type = constants.TrainingType.TrainAndValidation
    expr_store.metadata.X_raw_column_names = X_raw.head(1).columns.tolist()
    expr_store.metadata.raw_data_snapshot_str = data_transformation._get_data_snapshot(data=X_raw)
    expr_store.metadata.output_snapshot_str = data_transformation._get_output_snapshot(y=y_raw)
    expr_store.metadata.raw_data_type = inference.PandasParameterType

    expr_store.metadata.problem_info = ProblemInfo(
        dataset_samples=featurized_train_row_count,
        dataset_features=featurized_train_column_count,
        dataset_classes=unique_label_count,
        is_sparse=False,
        label_column_name=automl_settings.label_column_name,
        weight_column_name=automl_settings.weight_column_name,
        label_encoded_column_indexes=label_encoded_column_indexes,
        use_distributed=True)


def get_meterialized_xyw(dataset, label_column_name, weight_column_name, featurization_config):
    columns_to_drop = [label_column_name]
    if weight_column_name is not None:
        columns_to_drop.append(weight_column_name)

    dataset_df = dataset.take(RowCountsForClassificationRegression.ForPostFeaturizationSteps).\
        to_pandas_dataframe(extended_types=False)
    X = dataset_df.drop(columns=columns_to_drop)
    y = dataset_df[label_column_name].values
    w = None
    if weight_column_name:
        w = dataset_df[weight_column_name].values

    logger.info("Subsample size before cleaning {}".format(X.shape[0]))
    X, y, w = data_cleaning._remove_nan_rows_in_X_y(X, y, w,
                                                    is_timeseries=False,
                                                    target_column=label_column_name,
                                                    featurization_config=featurization_config)
    logger.info("Subsample size after cleaning {}".format(X.shape[0]))

    return X, y, w
