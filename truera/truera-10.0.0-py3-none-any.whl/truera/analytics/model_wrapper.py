from dataclasses import dataclass
from datetime import datetime
import hashlib
import logging
import os
from typing import Any, Optional, Tuple

import pandas as pd
from prometheus_client import Histogram

from truera.aiq.realized_background_data_split_info import \
    RealizedBackgroundDataSplitInfo
from truera.analytics.remote_model import RemoteModel
from truera.authn.usercontext import RequestContext
from truera.caching import util as cache_util
from truera.modelrunner.client.models.ingestion_mode import IngestionMode
from truera.modelrunner.client.models.system_columns import SystemColumns
from truera.protobuf.public.metadata_message_types_pb2 import \
    ModelType  # pylint: disable=no-name-in-module
from truera.utils.truera_status import TruEraInfluenceUnavailableError
from truera.utils.truera_status import TruEraNotFoundError
from truera.utils.truera_status import TruEraPredictionUnavailableError


@dataclass
class ModelCapability:
    is_regression: bool = False
    can_launch_model_runner: bool = True


class ModelWrapper:
    """Represents a model trained over a dataset.
    """

    CANNOT_LAUNCH_MODEL_MESSAGE = (
        "This analysis requires {requested_data} data which was not provided to "
        "TruEra platform. Please provide the required data or upload the model to TruEra. "
        "Project: {project}; Model: {model}; DataCollection: {data_collection}; "
        "Split/Data: {split_or_data}; IndexRange: {index_range}; ScorerType: {scorer_type}"
    )

    def __init__(
        self,
        model_id: str,
        model: RemoteModel,
        dataset_id: Optional[str] = None,
        model_name: Optional[str] = None,
        project_id: Optional[str] = None,
        model_metadata: Optional[Any] = None,
        is_regression: bool = False,
        server_config: Optional[dict] = None,
        updated_on: Optional[datetime] = None
    ):
        """[summary]
        
        Arguments:
            model_id: Model ID
            model_name: Friendly model name
            model: Classifier trained via scikit
            dataset_id: ID of corresponding dataset
        """
        self.logger = logging.getLogger(__name__)
        self.model_id = model_id
        self.model: RemoteModel = model
        self.dataset_id = dataset_id
        self.model_name = model_name
        self.project_id = project_id
        self.model_metadata = model_metadata
        self.model_type = model_metadata['model_type']
        self.model_capability = ModelCapability(
            is_regression=is_regression,
            can_launch_model_runner=self.model_type != ModelType.VIRTUAL
        )
        self.server_config = server_config
        self._updated_on = updated_on

    @property
    def updated_on(self) -> datetime:
        if self._updated_on is not None:
            return self._updated_on
        return datetime.min

    @property
    def name(self) -> str:
        if self.model_name:
            return self.model_name
        return self.model_id

    @property
    def wrapped_model(self) -> RemoteModel:
        return self.model

    @property
    def can_launch_model_runner(self):
        return self.model_capability.can_launch_model_runner

    @property
    def is_regression(self):
        return self.model_capability.is_regression

    def get_dataset_id(self):
        return self.dataset_id

    feature_importance_timer = Histogram(
        'aiq_model_feature_importance_latency_seconds',
        'Feature importance latency (in seconds)'
    )

    @feature_importance_timer.time()
    def compute_feature_influence_remote(
        self,
        request_ctx: RequestContext,
        scorer_type,
        start,
        stop,
        dataset,
        split_id,
        realized_background_data_split_info: RealizedBackgroundDataSplitInfo,
        include_system_data: bool = False
    ):
        if not self.can_launch_model_runner:
            raise TruEraInfluenceUnavailableError(
                ModelWrapper.CANNOT_LAUNCH_MODEL_MESSAGE.format(
                    requested_data="Feature Influence",
                    project=self.project_id,
                    model=self.model_id,
                    data_collection=self.dataset_id,
                    split_or_data=split_id,
                    index_range=f"[{start}:{stop})",
                    scorer_type=scorer_type
                )
            )
        split = dataset.get_split(split_id)
        xs = split.processed_or_preprocessed_data_with_system_data.iloc[
            start:stop]
        self.logger.debug("%s, %s", type(xs), xs)
        ys = split.label_data_with_system_data
        if ys is not None:
            ys = ys.iloc[start:stop]
        system_columns = None
        if split.system_column_names:
            system_columns = SystemColumns(
                id_column_name=split.unique_id_column_name,
                timestamp_column_name=split.timestamp_column_name
            )
        return self.model.feature_influence_from_daemon(
            request_ctx,
            scorer_type,
            xs,
            ys,
            system_columns,
            realized_background_data_split_info,
            include_system_data=include_system_data
        )

    def compute_prediction_score_remote_proba(
        self,
        request_ctx: RequestContext,
        scorer_type,
        input_data,
        system_columns,
        include_system_data: bool = False
    ) -> pd.DataFrame:
        if not self.can_launch_model_runner:
            raise TruEraPredictionUnavailableError(
                ModelWrapper.CANNOT_LAUNCH_MODEL_MESSAGE.format(
                    requested_data="Prediction",
                    project=self.project_id,
                    model=self.model_id,
                    data_collection=self.dataset_id,
                    split_or_data=input_data,
                    index_range=None,
                    scorer_type=scorer_type
                )
            )

        prediction_np = self.model.predict_proba_remote(
            request_ctx,
            input_data,
            system_columns,
            scorer_type,
            include_system_data=include_system_data
        )
        return prediction_np

    def launch_feature_influence_job(
        self,
        request_ctx: RequestContext,
        scorer_type,
        start,
        stop,
        dataset,
        split_id,
        realized_background_data_split_info,
        maximum_model_runner_failure_rate: Optional[float],
        use_data_service_write: bool = False
    ) -> str:
        if not self.can_launch_model_runner:
            raise TruEraInfluenceUnavailableError(
                ModelWrapper.CANNOT_LAUNCH_MODEL_MESSAGE.format(
                    requested_data="Feature Influence",
                    project=self.project_id,
                    model=self.model_id,
                    data_collection=self.dataset_id,
                    split_or_data=split_id,
                    index_range=f"[{start}:{stop})",
                    scorer_type=scorer_type
                )
            )
        split = dataset.get_split(split_id)
        input_locator = split.post_transform_locator if split.post_transform_locator else split.pre_transform_locator
        label_locator = split.label_locator
        cache_location = self._cache_location(
            scorer_type, split_id, realized_background_data_split_info,
            "feature_influence"
        )
        system_columns = None
        if split.system_column_names:
            system_columns = SystemColumns(
                id_column_name=split.unique_id_column_name,
                timestamp_column_name=split.timestamp_column_name
            )

        ingestion_mode, scratch_path = self._get_ingestion_params(
            use_data_service_write, split.unique_id_column_name, split_id,
            scorer_type, "feature_influence"
        )
        return self.model.launch_feature_influence_job(
            request_ctx, scorer_type, input_locator, label_locator,
            split.split_id, realized_background_data_split_info, start, stop,
            cache_location, system_columns, maximum_model_runner_failure_rate,
            ingestion_mode, scratch_path
        )

    def launch_partial_dependence_plot_job(
        self,
        request_ctx,
        scorer_type,
        num,
        realized_background_data_split_info,
    ) -> str:
        if not self.can_launch_model_runner:
            raise TruEraNotFoundError(
                ModelWrapper.CANNOT_LAUNCH_MODEL_MESSAGE.format(
                    requested_data="PDP",
                    project=self.project_id,
                    model=self.model_id,
                    data_collection=self.dataset_id,
                    split_or_data=realized_background_data_split_info.id,
                    index_range="all",
                    scorer_type=scorer_type
                )
            )
        cache_location = self._cache_location(
            scorer_type, "NA", realized_background_data_split_info,
            "partial_dependence_plot"
        )
        return self.model.launch_partial_dependence_plot_job(
            request_ctx, scorer_type, num, realized_background_data_split_info,
            cache_location
        )

    def launch_model_prediction_job(
        self,
        scorer_type,
        start,
        stop,
        dataset,
        split_id=None,
        maximum_model_runner_failure_rate=0,
        use_data_service_write=False
    ) -> str:
        if not self.can_launch_model_runner:
            raise TruEraPredictionUnavailableError(
                ModelWrapper.CANNOT_LAUNCH_MODEL_MESSAGE.format(
                    requested_data="Prediction",
                    project=self.project_id,
                    model=self.model_id,
                    data_collection=self.dataset_id,
                    split_or_data=split_id,
                    index_range=f"[{start}:{stop})",
                    scorer_type=scorer_type
                )
            )
        split = dataset.get_split(split_id)
        input_locator = split.post_transform_locator if split.post_transform_locator else split.pre_transform_locator
        label_locator = split.label_locator
        cache_location = self._model_prediction_cache_location(
            scorer_type, split_id
        )
        system_columns = None
        if split.system_column_names:
            system_columns = SystemColumns(
                id_column_name=split.unique_id_column_name,
                timestamp_column_name=split.timestamp_column_name
            )

        ingestion_mode, scratch_path = self._get_ingestion_params(
            use_data_service_write, split.unique_id_column_name, split_id,
            scorer_type, "model_prediction"
        )
        return self.model.launch_model_prediction_job(
            scorer_type, input_locator, label_locator, split.split_id, start,
            stop, cache_location, system_columns,
            maximum_model_runner_failure_rate, ingestion_mode, scratch_path
        )

    def stop_runners_if_any(self):
        if self.model:
            self.model.stop()

    def _get_ingestion_params(
        self, use_data_service_write: bool, unique_id_column_name: str,
        split_id: str, scorer_type: str, scratch_path_root_name: str
    ) -> Tuple[IngestionMode, str]:
        scratch_path = None
        ingestion_mode = IngestionMode.DIRECT_WRITE
        # If config for data service write is set and the split has
        # id columns we can perform write through data service.
        if use_data_service_write and unique_id_column_name:
            scratch_path = self._get_scratch_location(
                scorer_type, split_id, scratch_path_root_name
            )
            ingestion_mode = IngestionMode.DATASVC

        return ingestion_mode, scratch_path

    def _cache_location(
        self, scorer_type, split_id,
        realized_background_data_split_info: RealizedBackgroundDataSplitInfo,
        prefix
    ) -> str:
        background_data_split_filter_encoding = str(None)
        if realized_background_data_split_info.filter_expression is not None and str(
            realized_background_data_split_info.filter_expression
        ):
            background_data_split_filter_encoding = hashlib.sha1( # nosec B324 
                str(realized_background_data_split_info.filter_expression
                   ).encode("utf-8")
            ).hexdigest()
        cache_folder = os.path.join(
            cache_util.get_v2_cache_file_directory(
                self.server_config, self.project_id
            ), self.model_id
        )
        filename = f"{prefix}__split={split_id}__score_type={scorer_type}__bg={realized_background_data_split_info.id}__index={realized_background_data_split_info.index}__filter={background_data_split_filter_encoding}"
        return cache_util.make_path_fs_safe(
            os.path.join(cache_folder, filename)
        )

    def _model_prediction_cache_location(self, scorer_type, split_id) -> str:
        cache_folder = os.path.join(
            cache_util.get_v2_cache_file_directory(
                self.server_config, self.project_id
            ), self.model_id
        )
        filename = "{}_{}_{}.csv".format(
            "model_prediction", split_id, scorer_type
        )
        return cache_util.make_path_fs_safe(
            os.path.join(cache_folder, filename)
        )

    def _get_scratch_location(
        self, scorer_type: str, split_id: str, scratch_path_root_name: str
    ) -> str:
        cache_folder = os.path.join(
            cache_util.get_v2_cache_file_directory(
                self.server_config, self.project_id
            ), self.model_id
        )
        filename = f"{scratch_path_root_name}_{split_id}_{scorer_type}_scratch.csv"
        return cache_util.make_path_fs_safe(
            os.path.join(cache_folder, filename)
        )
