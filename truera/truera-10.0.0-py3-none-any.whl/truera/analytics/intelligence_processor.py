from __future__ import annotations

import logging
from typing import Mapping, NamedTuple, Optional, Sequence, Tuple

import pandas as pd
from scipy.special import expit as scipy_expit
from scipy.special import logit as scipy_logit

from truera.aiq.artifact_metadata_client import AIQArtifactMetadataClient
from truera.aiq.realized_background_data_split_info import \
    RealizedBackgroundDataSplitInfo
from truera.analytics.dataset import Dataset
from truera.analytics.loader.explanation_config_loader import \
    ExplanationConfigLoader
from truera.analytics.loader.metric_config_loader import MetricConfigLoader
from truera.analytics.model_wrapper import ModelWrapper
from truera.analytics.pending_operations_or import PendingOperationsOr
from truera.authn.usercontext import RequestContext
from truera.caching import util as caching_util
from truera.caching.explanation_cache_manager import ExplanationCacheManager
from truera.caching.model_prediction_cache_manager import \
    ModelPredictionCacheManager
from truera.modelrunner.client.models.system_columns import SystemColumns
from truera.protobuf.aiq.cache_pb2 import \
    ExplanationCacheMetadata  # pylint: disable=no-name-in-module
from truera.protobuf.aiq.cache_pb2 import \
    ModelPredictionCacheMetadata  # pylint: disable=no-name-in-module
from truera.protobuf.public.modelrunner.cache_entries_pb2 import \
    PartialDependenceCache  # pylint: disable=no-name-in-module
from truera.protobuf.public.qoi_pb2 import \
    ExplanationAlgorithmType  # pylint: disable=no-name-in-module
from truera.public import feature_influence_constants as fi_constants
from truera.utils import aiq_proto
from truera.utils.config_util import get_config_value
from truera.utils.numeric_table_cache import NumericTableCache
from truera.utils.truera_status import TruEraInternalError
from truera.utils.truera_status import TruEraInvalidArgumentError
from truera.utils.truera_status import TruEraInvalidConfigError
from truera.utils.truera_status import TruEraNotFoundError
from truera.utils.truera_status import TruEraPredictionUnavailableError


class ModelScoreTypeTuple(NamedTuple):
    model_id: str
    split_id: str
    score_type: str

    def __post_init__(self):
        assert self.model_id, "model_id cannot be None"
        assert self.split_id, "split_id cannot be None"


class CacheKey(NamedTuple):
    #TODO(AB#6237): Include background data num_samples in cache key.
    model_id: str
    split_id: str
    background_data_split_id: str
    background_data_split_index: Optional[int]
    background_data_split_filter_expression: Optional[str]
    score_type: str
    explanation_algorithm_type: Optional[
        ExplanationCacheMetadata.ExplanationCacheType
    ]  # can be None for PDPs if explicitly provided.

    def __post_init__(self):
        assert self.model_id, "model_id cannot be None"
        assert self.split_id, "split_id cannot be None"
        assert self.background_data_split_id, "background_data_split_id cannot be None"
        assert self.score_type, "score_type cannot be None"


class IntelligenceProcessor(object):
    """Analytics processor for models and datasets.
    """

    def __init__(
        self,
        project_id: str = None,
        server_config=None,
        analytics_config_loader: ExplanationConfigLoader = None,
        metric_config_loader: MetricConfigLoader = None,
        artifact_metadata_client: AIQArtifactMetadataClient = None,
        explanation_cache_manager: ExplanationCacheManager = None,
        model_prediction_cache_manager: ModelPredictionCacheManager = None
    ):
        self.logger = logging.getLogger(__name__)
        self.project_id = project_id or "project"

        self.feature_influence_caches: Mapping[CacheKey, NumericTableCache] = {}
        self.partial_dependence_plot_caches: Mapping[PartialDependenceCache
                                                    ] = {}
        self.model_prediction_caches: Mapping[ModelScoreTypeTuple,
                                              NumericTableCache] = {}
        self.explanation_cache_manager = explanation_cache_manager
        self.model_prediction_cache_manager = model_prediction_cache_manager

        self.datasets: Mapping[str, Dataset] = {}
        self.models: Mapping[str, ModelWrapper] = {}
        self.analytics_config_loader = analytics_config_loader
        self.metric_config_loader = metric_config_loader

        self.server_config = server_config
        self.artifact_metadata_client = artifact_metadata_client

    def get_model_keys(self):
        return self.models.keys()

    def get_dataset_keys(self):
        return self.datasets.keys()

    def get_dataset_by_id(self, dataset_id) -> Dataset:
        if dataset_id not in self.datasets:
            raise TruEraNotFoundError(
                f"Data collection {dataset_id} does not exist in project_id {self.project_id}\n"
                f"Available data collections: {list(self.datasets.keys())}"
            )
        return self.datasets[dataset_id]

    def get_dataset_id(self, model_id) -> str:
        return self.get_model(model_id).get_dataset_id()

    def get_dataset(self, model_id) -> Optional[Dataset]:
        dataset_id = self.get_dataset_id(model_id)
        if dataset_id:
            return self.get_dataset_by_id(dataset_id)
        return None

    def get_model(self, model_id) -> ModelWrapper:
        return self.models[model_id]

    def add_dataset(self, dataset_id: str, dataset: Dataset):
        self.datasets[dataset_id] = dataset

    def add_model(self, model_id, model_wrapper):
        self.models[model_id] = model_wrapper

    def remove_dataset(self, dataset_id):
        return self.datasets.pop(dataset_id, None)

    def get_default_split_id_for_model(
        self, request_context: RequestContext, model_id: str
    ):
        split_id = self.artifact_metadata_client.get_default_base_split_id_for_model(
            request_context,
            self.project_id,
            model_id,
            infer_base_split_if_not_set=True
        )
        if split_id:
            return split_id
        raise TruEraNotFoundError("No default split!")

    def get_default_split_id(
        self,
        request_context: RequestContext,
        data_collection_id: str,
        throw_exception_if_not_found: bool = True
    ) -> Optional[str]:
        split_id = self.artifact_metadata_client.get_default_base_split_id(
            request_context,
            self.project_id,
            data_collection_id,
            infer_base_split_if_not_set=True
        )
        if split_id or not throw_exception_if_not_found:
            return split_id
        raise TruEraNotFoundError("No default split!")

    def _get_default_score_type(self, model_id):
        if self.get_model(model_id).is_regression:
            return fi_constants.PREDICTOR_SCORE_TYPE_REGRESSION
        return fi_constants.PREDICTOR_SCORE_TYPE_LOGITS

    def _validate_score_type(self, dataset, split_id, model_id, score_type):
        is_regression = self.get_model(model_id).is_regression
        if is_regression != (
            score_type in fi_constants.ALL_REGRESSION_SCORE_TYPES
        ):
            model_type_str = "regression" if is_regression else "classification"
            raise TruEraInvalidArgumentError(
                f"Score type {score_type} is not supported for {model_type_str} models."
            )
        if not dataset.get_split(
            split_id
        ).has_labels and score_type in fi_constants.MODEL_ERROR_SCORE_TYPES:
            raise TruEraInvalidConfigError(
                "Feature influences for error score types require splits with labels. Provided split: {split_id}."
            )

    def _score_type_is_derivable_from(
        self, target_score_type, source_score_type
    ):
        return (
            get_config_value(
                self.server_config, "intelligence",
                "enable_score_type_conversion"
            ) and (
                (
                    target_score_type
                    == fi_constants.PREDICTOR_SCORE_TYPE_LOGITS and
                    source_score_type
                    == fi_constants.PREDICTOR_SCORE_TYPE_PROBITS
                ) or (
                    target_score_type
                    == fi_constants.PREDICTOR_SCORE_TYPE_PROBITS and
                    source_score_type
                    == fi_constants.PREDICTOR_SCORE_TYPE_LOGITS
                )
            )
        )

    def _convert_score_type(
        self, target_score_type, source_score_type, prediction_values
    ):
        if not self._score_type_is_derivable_from(
            target_score_type, source_score_type
        ):
            raise TruEraInvalidArgumentError(
                f"Source score type {source_score_type} cannot be safely converted into target score type {target_score_type}"
            )
        if (
            target_score_type == fi_constants.PREDICTOR_SCORE_TYPE_LOGITS and
            source_score_type == fi_constants.PREDICTOR_SCORE_TYPE_PROBITS
        ):
            return scipy_logit(prediction_values)
        elif (
            target_score_type == fi_constants.PREDICTOR_SCORE_TYPE_PROBITS and
            source_score_type == fi_constants.PREDICTOR_SCORE_TYPE_LOGITS
        ):
            return scipy_expit(prediction_values)
        return prediction_values

    def get_prediction_score(
        self,
        request_context: RequestContext,
        model_id: str,
        score_type_str: str,
        index: int,
        split_id: Optional[str] = None,
        include_system_data: bool = False
    ) -> pd.DataFrame:
        metric_config = self.metric_config_loader.fetch_config(
            request_context, self.project_id
        )
        split_id = split_id or self.get_default_split_id_for_model(
            request_context, model_id
        )
        score_type_str = score_type_str or self._get_default_score_type(
            model_id
        )
        default_score_type_str = aiq_proto.GetScoreTypeFromQuantityOfInterest(
            metric_config.score_type
        )
        if self._score_type_is_derivable_from(
            score_type_str, default_score_type_str
        ):
            default_score = self.get_prediction_score(
                request_context,
                model_id,
                default_score_type_str,
                index,
                split_id,
                include_system_data=include_system_data
            )
            default_score.loc[:, aiq_proto.PREDICTION_CACHE_COLUMN
                             ] = self._convert_score_type(
                                 score_type_str, default_score_type_str,
                                 default_score.loc[:, aiq_proto.
                                                   PREDICTION_CACHE_COLUMN]
                             )
            return default_score

        if score_type_str == fi_constants.PREDICTOR_SCORE_TYPE_CLASSIFICATION:
            # trigger computations on probits which can be thresholded to get classification decisions
            if default_score_type_str == fi_constants.PREDICTOR_SCORE_TYPE_CLASSIFICATION:
                default_score_type_str = fi_constants.PREDICTOR_SCORE_TYPE_PROBITS
            default_score = self.get_prediction_score(
                request_context,
                model_id,
                default_score_type_str,
                index,
                split_id,
                include_system_data=include_system_data
            )
            default_score.loc[:, aiq_proto.PREDICTION_CACHE_COLUMN
                             ] = self.artifact_metadata_client.get_classification_scores_for_model(
                                 request_context, self.project_id, model_id,
                                 metric_config.score_type,
                                 default_score[aiq_proto.PREDICTION_CACHE_COLUMN
                                              ].to_numpy()
                             ).astype(float)
            return default_score
        cache_key = ModelScoreTypeTuple(model_id, split_id, score_type_str)
        # TODO(AB#176) Not multi-thread safe
        if cache_key not in self.model_prediction_caches:
            # Cache needs to be loaded if using a virtual model
            self._load_model_prediction_cache(
                model_id, split_id, score_type_str, request_context
            )
        if cache_key in self.model_prediction_caches:
            cache = self.model_prediction_caches[cache_key]
            if cache.contains_index(index):
                return cache.get_value(
                    index, include_system_data=include_system_data
                ).to_frame().T
        model = self.models[model_id]
        split = self.get_dataset(model_id).get_split(split_id)
        input_data = split.processed_or_preprocessed_data_with_system_data.iloc[
            index:(index + 1)]
        system_columns = None
        if split.system_column_names:
            system_columns = SystemColumns(
                id_column_name=split.unique_id_column_name,
                timestamp_column_name=split.timestamp_column_name
            )

        prediction_df = model.compute_prediction_score_remote_proba(
            request_context,
            score_type_str,
            input_data,
            system_columns,
            include_system_data=include_system_data
        )
        prediction_df.index = input_data.index
        prediction_df.rename(
            columns={'Result': aiq_proto.PREDICTION_CACHE_COLUMN}, inplace=True
        )
        return prediction_df

    def get_prediction_scores(
        self,
        request_context: RequestContext,
        model_id: str,
        score_type: Optional[str] = None,
        split_id: Optional[str] = None,
        start: int = 0,
        stop: Optional[int] = None,
        readonly: bool = False,
        include_system_data: bool = False
    ) -> PendingOperationsOr[pd.DataFrame]:
        score_type = score_type or self._get_default_score_type(model_id)
        metric_config = self.metric_config_loader.fetch_config(
            request_context, self.project_id
        )
        default_score_type = aiq_proto.GetScoreTypeFromQuantityOfInterest(
            metric_config.score_type
        )
        if self._score_type_is_derivable_from(score_type, default_score_type):
            raw_predictions_or_operations = self.get_prediction_scores(
                request_context,
                model_id,
                default_score_type,
                split_id,
                start,
                stop,
                readonly=readonly,
                include_system_data=include_system_data
            )
            if raw_predictions_or_operations.is_operations:
                return raw_predictions_or_operations
            preds = raw_predictions_or_operations.value
            preds.loc[:, aiq_proto.
                      PREDICTION_CACHE_COLUMN] = self._convert_score_type(
                          score_type, default_score_type,
                          preds[aiq_proto.PREDICTION_CACHE_COLUMN].to_numpy()
                      )
            return PendingOperationsOr.from_value(preds)

        if score_type == fi_constants.PREDICTOR_SCORE_TYPE_CLASSIFICATION:
            # trigger computations on probits which can be thresholded to get classification decisions
            if default_score_type == fi_constants.PREDICTOR_SCORE_TYPE_CLASSIFICATION:
                default_score_type = fi_constants.PREDICTOR_SCORE_TYPE_PROBITS

            raw_predictions_or_operations = self.get_prediction_scores(
                request_context,
                model_id,
                default_score_type,
                split_id,
                start,
                stop,
                readonly=readonly,
                include_system_data=include_system_data
            )
            if raw_predictions_or_operations.is_operations:
                return raw_predictions_or_operations
            classifications = raw_predictions_or_operations.value
            classifications.loc[:, aiq_proto.PREDICTION_CACHE_COLUMN
                               ] = self.artifact_metadata_client.get_classification_scores_for_model(
                                   request_context, self.project_id, model_id,
                                   metric_config.score_type, classifications[
                                       aiq_proto.PREDICTION_CACHE_COLUMN
                                   ].to_numpy()
                               ).astype(float)
            return PendingOperationsOr.from_value(classifications)

        split_id = split_id or self.get_default_split_id_for_model(
            request_context, model_id
        )
        cache_key = ModelScoreTypeTuple(model_id, split_id, score_type)
        pending_operation_ids = self._build_model_prediction_cache(
            request_context, stop, model_id, split_id, score_type, readonly
        )
        if pending_operation_ids:
            return PendingOperationsOr.from_operations(pending_operation_ids)
        if cache_key in self.model_prediction_caches:
            cache = self.model_prediction_caches[cache_key]
            if cache.contains_index_range(start, stop):
                predictions = cache.get_values_df(
                    start, stop, include_system_data=include_system_data
                )
                return PendingOperationsOr.from_value(predictions)
        else:
            cache_keys = [
                ModelScoreTypeTuple(model_id, split_id, temp_score_type)
                for temp_score_type in [
                    fi_constants.PREDICTOR_SCORE_TYPE_LOGITS,
                    fi_constants.PREDICTOR_SCORE_TYPE_LOGITS_UNNORM,
                    fi_constants.PREDICTOR_SCORE_TYPE_PROBITS,
                    fi_constants.PREDICTOR_SCORE_TYPE_CLASSIFICATION,
                    fi_constants.PREDICTOR_SCORE_TYPE_LOG_LOSS,
                    fi_constants.PREDICTOR_SCORE_TYPE_MAE_CLASSIFICATION,
                ]
            ]
            for ck in cache_keys:
                if ck in self.model_prediction_caches:
                    self.logger.info(
                        f"Found existing cache with type {ck.score_type} for model: {model_id} \
                            split: {split_id} but did not convert it because project uses {default_score_type}"
                    )

        if not readonly:
            raise TruEraInternalError(
                "Internal error: Prediction cache values not available."
            )
        raise TruEraPredictionUnavailableError(
            "Requested prediction caches not available."
        )

    def _get_fi_algorithm_types_to_query(self, use_shap: bool):
        # NB: this is ordered. If we get a cache hit on an earlier FI algo type, we will return.
        return [
            ExplanationCacheMetadata.ExplanationCacheType.
            FEATURE_INFLUENCE_TREE_SHAP_INTERVENTIONAL,
            ExplanationCacheMetadata.ExplanationCacheType.
            FEATURE_INFLUENCE_KERNEL_SHAP, ExplanationCacheMetadata.
            ExplanationCacheType.FEATURE_INFLUENCE_TREE_SHAP_PATH_DEPENDENT
        ] if use_shap else [
            ExplanationCacheMetadata.ExplanationCacheType.FEATURE_INFLUENCE
        ]

    def _map_fi_algorithm_cache_to_client_proto(
        self, cache_proto: ExplanationCacheMetadata.ExplanationCacheType
    ):
        return {
            ExplanationCacheMetadata.ExplanationCacheType.FEATURE_INFLUENCE:
                ExplanationAlgorithmType.TRUERA_QII,
            ExplanationCacheMetadata.ExplanationCacheType.FEATURE_INFLUENCE_KERNEL_SHAP:
                ExplanationAlgorithmType.KERNEL_SHAP,
            ExplanationCacheMetadata.ExplanationCacheType.FEATURE_INFLUENCE_TREE_SHAP_INTERVENTIONAL:
                ExplanationAlgorithmType.TREE_SHAP_INTERVENTIONAL,
            ExplanationCacheMetadata.ExplanationCacheType.FEATURE_INFLUENCE_TREE_SHAP_PATH_DEPENDENT:
                ExplanationAlgorithmType.TREE_SHAP_PATH_DEPENDENT,
            ExplanationCacheMetadata.ExplanationCacheType.FEATURE_INFLUENCE_INTEGRATED_GRADIENTS:
                ExplanationAlgorithmType.INTEGRATED_GRADIENTS,
        }[cache_proto]

    def get_inf(
        self,
        request_context: RequestContext,
        model_id: str,
        split_id: Optional[str] = None,
        index: int = 0,
        realized_background_data_split_info:
        RealizedBackgroundDataSplitInfo = None,
        score_type: Optional[str] = None,
        include_system_data: bool = False
    ) -> PendingOperationsOr[Tuple[pd.DataFrame, ExplanationAlgorithmType]]:
        if realized_background_data_split_info is None:
            realized_background_data_split_info = RealizedBackgroundDataSplitInfo(
                request_context, intelligence_processor=self, model_id=model_id
            )
        score_type = score_type or self._get_default_score_type(model_id)
        split_id = split_id or self.get_default_split_id_for_model(
            request_context, model_id
        )
        split_obj = self.get_dataset(model_id).get_split(split_id)
        use_shap = self.artifact_metadata_client.is_shap_algorithm_type(
            request_context, self.project_id
        )
        # cache hit
        for explanation_algorithm_type in self._get_fi_algorithm_types_to_query(
            use_shap
        ):
            cache_key = CacheKey(
                model_id=model_id,
                split_id=split_id,
                background_data_split_id=realized_background_data_split_info.id,
                background_data_split_index=realized_background_data_split_info.
                index,
                background_data_split_filter_expression=str(
                    realized_background_data_split_info.filter_expression
                ),
                score_type=score_type,
                explanation_algorithm_type=explanation_algorithm_type
            )
            if cache_key in self.feature_influence_caches:
                feature_influence_cache = self.feature_influence_caches[
                    cache_key]
                if feature_influence_cache.contains_index(index):
                    if score_type in fi_constants.MODEL_ERROR_SCORE_TYPES and feature_influence_cache.get_updated_on(
                    ) < split_obj.updated_on:
                        del self.feature_influence_caches[cache_key]
                    else:
                        return PendingOperationsOr.from_value(
                            (
                                feature_influence_cache.get_value(
                                    index,
                                    include_system_data=include_system_data
                                ).to_frame().T,
                                self._map_fi_algorithm_cache_to_client_proto(
                                    cache_key.explanation_algorithm_type
                                )
                            )
                        )

        # cache miss
        if use_shap:  # cannot trigger MRs for SHAP infs.
            raise TruEraNotFoundError(
                "Requested feature influences are not precomputed. New feature influences can only be generated if the project's influence algorithm is set to truera-qii!"
            )

        return PendingOperationsOr.from_value(
            (
                self._compute_feature_influence_remote(
                    request_context,
                    model_id,
                    split_id,
                    score_type,
                    index,
                    index + 1,
                    realized_background_data_split_info,
                    include_system_data=include_system_data
                ), ExplanationAlgorithmType.TRUERA_QII
            )
        )

    def get_infs(
        self,
        request_context: RequestContext,
        model_id: str,
        split_id: Optional[str] = None,
        n: int = 1000,
        realized_background_data_split_info:
        RealizedBackgroundDataSplitInfo = None,
        score_type: Optional[str] = None,
        include_system_data: bool = False
    ) -> PendingOperationsOr[Tuple[pd.DataFrame, ExplanationAlgorithmType]]:
        if realized_background_data_split_info is None:
            realized_background_data_split_info = RealizedBackgroundDataSplitInfo(
                request_context, intelligence_processor=self, model_id=model_id
            )
        score_type = score_type or self._get_default_score_type(model_id)
        split_id = split_id or self.get_default_split_id_for_model(
            request_context, model_id
        )
        n = min(n, self.get_dataset(model_id).get_split(split_id).num_inputs)

        pending_operation_ids, cache_key = self._build_fi_cache(
            request_context, n, model_id, split_id,
            realized_background_data_split_info, score_type
        )
        if pending_operation_ids:
            return PendingOperationsOr.from_operations(pending_operation_ids)
        return PendingOperationsOr.from_value(
            (
                self.feature_influence_caches[cache_key].get_values_df(
                    0, n, include_system_data=include_system_data
                ),
                self._map_fi_algorithm_cache_to_client_proto(
                    cache_key.explanation_algorithm_type
                )
            )
        )

    def get_pdp(
        self,
        request_context: RequestContext,
        model_id: str,
        realized_background_data_split_info:
        RealizedBackgroundDataSplitInfo = None,
        score_type: Optional[str] = None
    ) -> PendingOperationsOr[PartialDependenceCache]:
        if realized_background_data_split_info is None:
            realized_background_data_split_info = RealizedBackgroundDataSplitInfo(
                request_context, intelligence_processor=self, model_id=model_id
            )
        score_type = score_type or self._get_default_score_type(model_id)
        if score_type in fi_constants.MODEL_ERROR_SCORE_TYPES:
            raise TruEraInvalidArgumentError(
                "Partial Dependence Plots are not supported for error score types."
            )

        cache_key = CacheKey(
            model_id,
            "NA",
            realized_background_data_split_info.id,
            realized_background_data_split_info.index,
            str(realized_background_data_split_info.filter_expression),
            score_type,
            explanation_algorithm_type=None
        )
        pending_operation_ids = self._build_pdp_cache(
            request_context, model_id, realized_background_data_split_info,
            score_type, cache_key
        )
        if pending_operation_ids:
            return PendingOperationsOr.from_operations(pending_operation_ids)
        return PendingOperationsOr.from_value(
            self.partial_dependence_plot_caches[cache_key]
        )

    def _build_fi_cache(
        self, request_context: RequestContext, num: int, model_id: str,
        split_id: str,
        realized_background_data_split_info: RealizedBackgroundDataSplitInfo,
        score_type: str
    ) -> Tuple[Sequence[str], Optional[CacheKey]]:
        use_shap = self.artifact_metadata_client.is_shap_algorithm_type(
            request_context, self.project_id
        )
        split_id = split_id or self.get_default_split_id_for_model(
            request_context, model_id
        )
        dataset = self.get_dataset(model_id)
        split_obj = dataset.get_split(split_id)

        # determine if we have a cache hit (either in-memory in AIQ or if we can load a cache file from disk)
        for explanation_algorithm_type in self._get_fi_algorithm_types_to_query(
            use_shap
        ):
            cache_key = CacheKey(
                model_id,
                split_id,
                realized_background_data_split_info.id,
                realized_background_data_split_info.index,
                str(realized_background_data_split_info.filter_expression),
                score_type,
                explanation_algorithm_type=explanation_algorithm_type
            )

            # TODO(AB#176) Not thread safe.

            # cache already in-memory
            if cache_key in self.feature_influence_caches:
                feature_influence_cache = self.feature_influence_caches[
                    cache_key]
                if feature_influence_cache.contains_index_range(0, num):
                    # check if cache needs to be invalidated for error infs
                    if score_type in fi_constants.MODEL_ERROR_SCORE_TYPES and feature_influence_cache.get_updated_on(
                    ) < split_obj.updated_on:
                        del self.feature_influence_caches[cache_key]
                    else:
                        return [], cache_key

            self._load_fi_cache(
                request_context, model_id, split_id,
                realized_background_data_split_info, score_type, cache_key
            )

            # after loading cache files from disk, determine if there is a hit
            feature_influence_cache = self.feature_influence_caches[cache_key]
            if feature_influence_cache.contains_index_range(0, num):
                self.logger.info("Cache loaded %d", num)
                return [], cache_key

        self.logger.info(
            "Building fi cache: %s, %s, %s", model_id, split_id, score_type
        )

        # cache miss
        if use_shap:  # cannot trigger MRs for SHAP infs.
            raise TruEraNotFoundError(
                "Requested feature influences are not precomputed. New feature influences can only be generated if the project's influence algorithm is set to truera-qii!"
            )

        # trigger MRs for QIIs.
        model_wrapper = self.get_model(model_id)
        self._validate_score_type(dataset, split_id, model_id, score_type)
        maximum_model_runner_failure_rate = self.metric_config_loader.fetch_config(
            request_context, self.project_id
        ).maximum_model_runner_failure_rate

        use_data_service_write = get_config_value(
            self.server_config, "data_write_mode", "use_data_service_write",
            False
        )
        job_id = model_wrapper.launch_feature_influence_job(
            request_context,
            score_type,
            0,
            num,
            dataset,
            split_id,
            realized_background_data_split_info,
            maximum_model_runner_failure_rate,
            use_data_service_write=use_data_service_write
        )
        self.logger.info("Launched job: %s", job_id)
        return [job_id], None

    def _build_pdp_cache(
        self, request_context: RequestContext, model_id: str,
        realized_background_data_split_info: RealizedBackgroundDataSplitInfo,
        score_type: str, cache_key: CacheKey
    ) -> Optional[Sequence[str]]:
        # TODO(AB#176) Not thread safe.
        if cache_key in self.partial_dependence_plot_caches:
            return []
        self._load_pdp_cache(
            request_context, model_id, realized_background_data_split_info,
            score_type, cache_key
        )
        if cache_key in self.partial_dependence_plot_caches:
            return []
        self.logger.info(
            "Building pdp cache: %s, %s, %s", model_id,
            realized_background_data_split_info.id, score_type
        )
        model_wrapper = self.get_model(model_id)
        job_id = model_wrapper.launch_partial_dependence_plot_job(
            request_context, score_type,
            self.get_dataset(model_id).get_split(
                realized_background_data_split_info.id
            ).num_inputs, realized_background_data_split_info
        )
        self.logger.info("Launched job: %s", job_id)
        return [job_id]

    def _build_model_prediction_cache(
        self, request_context: RequestContext, num: int, model_id: str,
        split_id: str, score_type: str, readonly: bool
    ) -> Sequence[str]:
        split_id = split_id or self.get_default_split_id_for_model(
            request_context, model_id
        )
        cache_key = ModelScoreTypeTuple(model_id, split_id, score_type)
        num = num or self.get_dataset(model_id).get_split(split_id).num_inputs
        # TODO(AB#176) Not thread safe.
        if cache_key in self.model_prediction_caches:
            model_prediction_cache = self.model_prediction_caches[cache_key]
            if model_prediction_cache.contains_index_range(0, num):
                return []

        self._load_model_prediction_cache(
            model_id, split_id, score_type, request_context
        )
        model_prediction_cache = self.model_prediction_caches[cache_key]
        if model_prediction_cache.contains_index_range(0, num):
            return []
        if readonly:
            self.logger.info(
                "Skipping model prediction cache generation in readonly request."
            )
            return []

        self.logger.info(
            "Building prediction cache: %s, %s, %s", model_id, split_id,
            score_type
        )
        model_wrapper = self.get_model(model_id)
        dataset = self.get_dataset(model_id)
        self._validate_score_type(dataset, split_id, model_id, score_type)
        maximum_model_runner_failure_rate = self.metric_config_loader.fetch_config(
            request_context, self.project_id
        ).maximum_model_runner_failure_rate
        use_data_service_write = get_config_value(
            self.server_config, "data_write_mode", "use_data_service_write",
            False
        )
        job_id = model_wrapper.launch_model_prediction_job(
            score_type,
            0,
            num,
            dataset,
            split_id=split_id,
            maximum_model_runner_failure_rate=maximum_model_runner_failure_rate,
            use_data_service_write=use_data_service_write
        )
        self.logger.info("Launched model prediction job: %s", job_id)
        return [job_id]

    def _compute_feature_influence_remote(
        self,
        request_ctx: RequestContext,
        model_id: str,
        split_id: str,
        score_type: str,
        start: int,
        stop: int,
        realized_background_data_split_info: RealizedBackgroundDataSplitInfo,
        include_system_data: bool = False
    ) -> Sequence[Mapping[str, float]]:
        model_wrapper = self.get_model(model_id)
        dataset = self.get_dataset(model_id)
        self._validate_score_type(dataset, split_id, model_id, score_type)
        return model_wrapper.compute_feature_influence_remote(
            request_ctx,
            score_type,
            start,
            stop,
            dataset,
            split_id,
            realized_background_data_split_info,
            include_system_data=include_system_data
        )

    def _create_explanation_cache_metadata(
        self, model_id: str, split_id: str,
        background_data_split_id: Optional[str], score_type: str,
        explanation_cache_type: int, request_ctx: RequestContext
    ) -> ExplanationCacheMetadata:
        explanation_cache_metadata = ExplanationCacheMetadata()
        explanation_cache_metadata.model_id.project_id = self.project_id
        explanation_cache_metadata.model_id.model_id = model_id
        explanation_cache_metadata.model_input_spec.split_id = split_id
        explanation_cache_metadata.score_type = aiq_proto.GetQuantityOfInterestFromScoreType(
            score_type
        )
        explanation_cache_metadata.explanation_cache_type = explanation_cache_type
        if background_data_split_id is not None:
            explanation_cache_metadata.background_data_split_info.id = background_data_split_id
        if self.analytics_config_loader:
            analytics_config = self.analytics_config_loader.fetch_config(
                request_ctx, self.project_id
            )
            explanation_cache_metadata.config.CopyFrom(analytics_config)
        return explanation_cache_metadata

    def _create_model_prediction_cache_metadata(
        self, model_id: str, split_id: str, score_type: str
    ) -> ModelPredictionCacheMetadata:
        model_prediction_cache_metadata = ModelPredictionCacheMetadata()
        model_prediction_cache_metadata.model_id.project_id = self.project_id
        model_prediction_cache_metadata.model_id.model_id = model_id
        model_prediction_cache_metadata.model_input_spec.split_id = split_id
        model_prediction_cache_metadata.score_type = aiq_proto.GetQuantityOfInterestFromScoreType(
            score_type
        )
        return model_prediction_cache_metadata

    def _load_fi_cache(
        self, request_context: RequestContext, model_id: str, split_id: str,
        realized_background_data_split_info: RealizedBackgroundDataSplitInfo,
        score_type: str, cache_key: CacheKey
    ) -> bool:
        if not self.explanation_cache_manager:
            return
        if cache_key.explanation_algorithm_type is None:
            raise TruEraInternalError(
                "Cannot retrieve feature influences for algorithm type `None`!"
            )
        split_obj = self.get_dataset(model_id).get_split(split_id)
        columns = split_obj.feature_names
        if cache_key not in self.feature_influence_caches:
            self.feature_influence_caches[
                cache_key] = caching_util.create_empty_cache(
                    columns,
                    unique_id_column=split_obj.unique_id_column_name,
                    timestamp_column_name=split_obj.timestamp_column_name
                )
        cache = self.feature_influence_caches[cache_key]
        background_data_split_is_default_split = not self.artifact_metadata_client.get_default_base_split_id_for_model(
            request_context,
            self.project_id,
            model_id,
            infer_base_split_if_not_set=False
        )

        explanation_cache_metadata = self._create_explanation_cache_metadata(
            # TODO(davidkurokawa): add in background_data_split_index and filter stuff too!
            model_id,
            split_id,
            realized_background_data_split_info.id,
            score_type,
            cache_key.explanation_algorithm_type,
            request_context
        )
        self.explanation_cache_manager.load_feature_influence_cache_metarepo(
            request_context, cache, explanation_cache_metadata,
            background_data_split_is_default_split, split_obj.updated_on
        )
        return cache.len() > 0

    def _load_pdp_cache(
        self, request_context: RequestContext, model_id: str,
        realized_background_data_split_info: RealizedBackgroundDataSplitInfo,
        score_type: str, cache_key: CacheKey
    ) -> bool:
        if cache_key in self.partial_dependence_plot_caches:
            return True
        if not self.explanation_cache_manager:
            return False
        pdp_cache_metadata = self._create_explanation_cache_metadata(
            # TODO(davidkurokawa): add in background_data_split_index and filter stuff too!
            model_id,
            realized_background_data_split_info.id,
            realized_background_data_split_info.id,
            score_type,
            ExplanationCacheMetadata.ExplanationCacheType.PARTIAL_DEPENDENCE,
            request_context
        )
        cache = self.explanation_cache_manager.load_partial_dependence_plot_cache_metarepo(
            request_context, pdp_cache_metadata
        )
        if cache:
            self.partial_dependence_plot_caches[cache_key] = cache
            return True
        return False

    def _load_model_prediction_cache(
        self, model_id: str, split_id: str, score_type: str,
        request_ctx: RequestContext
    ) -> bool:
        if not self.model_prediction_cache_manager:
            return
        cache_key = ModelScoreTypeTuple(model_id, split_id, score_type)
        if cache_key not in self.model_prediction_caches:
            split_obj = self.get_dataset(model_id).get_split(split_id)
            self.model_prediction_caches[
                cache_key] = caching_util.create_empty_cache(
                    [aiq_proto.PREDICTION_CACHE_COLUMN],
                    unique_id_column=split_obj.unique_id_column_name,
                    timestamp_column_name=split_obj.timestamp_column_name
                )
        cache = self.model_prediction_caches[cache_key]
        model_prediction_cache_metadata = self._create_model_prediction_cache_metadata(
            model_id, split_id, score_type
        )
        self.model_prediction_cache_manager.load_cache_metarepo(
            cache, model_prediction_cache_metadata, request_ctx
        )
        return cache.len() > 0
