import dataclasses
from dataclasses import dataclass
import logging
from typing import Any, Mapping, Optional, Sequence, Union

import numpy as np
import pandas as pd

from truera.client.base_truera_workspace import BaseTrueraWorkspace
from truera.client.base_truera_workspace import WorkspaceContextCleaner
from truera.client.client_utils import validate_add_model_metadata
from truera.client.client_utils import validate_model_metadata
from truera.client.errors import NotFoundError
from truera.client.ingestion_client import Table
import truera.client.intelligence.metrics_util as metrics_util
from truera.client.local.intelligence.local_data_profiler import \
    LocalDataProfiler
from truera.client.local.intelligence.local_explainer import LocalExplainer
from truera.client.local.intelligence.local_nlp_explainer import \
    LocalNLPExplainer
from truera.client.local.intelligence.local_rnn_explainer import \
    LocalRNNExplainer
from truera.client.local.intelligence.local_tester import LocalTester
from truera.client.local.local_artifacts import DataCollection
from truera.client.local.local_artifacts import PdCache
from truera.client.local.local_artifacts import Project
from truera.client.local.local_artifacts import QiiCache
from truera.client.nn import NNBackend as NNB
from truera.client.nn import wrappers as base
from truera.client.nn.client_configs import AttributionConfiguration
from truera.client.nn.client_configs import NLPAttributionConfiguration
from truera.client.nn.client_configs import RNNAttributionConfiguration
from truera.client.nn.client_configs import RNNUserInterfaceConfiguration
from truera.client.nn.wrappers import nlp
from truera.client.nn.wrappers import timeseries
from truera.client.public.communicator.http_communicator import \
    AlreadyExistsError
from truera.client.public.communicator.http_communicator import \
    NotSupportedError
from truera.client.util import workspace_validation_utils
from truera.protobuf.public.metadata_message_types_pb2 import \
    ModelType  # pylint: disable=no-name-in-module
from truera.public.feature_influence_constants import \
    get_output_type_from_score_type


@dataclass(eq=True, frozen=True)
class TrueraWorkspaceContext:
    project_name: str
    data_collection_name: str
    data_split_name: str
    model_name: str


class LocalTrueraWorkspace(BaseTrueraWorkspace):

    def __init__(self, log_level: int = logging.INFO):
        """Construct a new local TrueraWorkspace.
        Args:
            log_level: Log level (defaults to `logging.INFO`).
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        self.projects = {}
        self.context = TrueraWorkspaceContext(None, None, None, None)
        self.rnn_attr_configs = {}
        self.nlp_attr_configs = {}
        self.data_profiler = LocalDataProfiler()
        self.tester = LocalTester()
        self.qii_cache = QiiCache()
        self.pd_cache = PdCache()

    def get_projects(self) -> Sequence[str]:
        return list(self.projects.keys())

    def add_project(
        self,
        project: str,
        score_type: str,
        input_type: Optional[str] = "tabular",
        num_default_influences: Optional[int] = None
    ):
        self._validate_add_project(
            project, score_type, input_type, num_default_influences
        )
        if input_type == "text" or input_type == "time_series_tabular":
            num_default_influences = num_default_influences or LocalRNNExplainer._NUM_DEFAULT_INFLUENCES
        else:
            num_default_influences = num_default_influences or BaseTrueraWorkspace._DEFAULT_NUM_DEFAULT_INFLUENCES
        self.projects[project] = Project(
            project,
            score_type=score_type,
            input_type=input_type,
            num_default_influences=num_default_influences,
        )
        if self._get_current_active_project_name():
            self.set_data_collection(None)
            self.set_model(None)
        self.context = dataclasses.replace(self.context, project_name=project)

    def set_project(self, project: str):
        if project == self._get_current_active_project_name():
            return
        if project:
            self._validate_set_project(project)
        if self._get_current_active_project_name():
            self.set_data_collection(None)
            self.set_model(None)
        self.context = dataclasses.replace(self.context, project_name=project)

    def set_score_type(self, score_type: str):
        self._ensure_project()
        self._validate_score_type(score_type)
        project_obj = self._get_current_project_obj()
        project_obj.score_type = score_type

    def set_influence_type(self, algorithm: str):
        self._ensure_project()
        self._get_current_project_obj().set_influence_algorithm(algorithm)

    def get_influence_type(self) -> str:
        self._ensure_project()
        return self._get_current_project_obj().get_influence_algorithm()

    def get_num_default_influences(self) -> int:
        self._ensure_project()
        return self._get_current_project_obj().num_default_influences

    def set_num_default_influences(self, num_default_influences: int):
        self._validate_num_default_influences(num_default_influences)
        self._get_current_project_obj(
        ).num_default_influences = num_default_influences

    def list_performance_metrics(self) -> Sequence[str]:
        if self._get_output_type() == "regression":
            return list(metrics_util.LOCAL_REGRESSION_METRICS.keys())
        return list(metrics_util.LOCAL_CLASSIFICATION_METRICS.keys())

    def get_default_performance_metrics(self) -> Sequence[str]:
        # TODO(DC-73)
        raise NotSupportedError(
            "Performance metrics can only be get/set in remote workspaces!"
        )

    def set_default_performance_metrics(
        self, performance_metrics: Sequence[str]
    ):
        # TODO(DC-73)
        raise NotSupportedError(
            "Performance metrics can only be get/set in remote workspaces!"
        )

    def get_num_internal_qii_samples(self) -> int:
        self._ensure_project()
        return self._get_current_project_obj().num_samples

    def set_num_internal_qii_samples(self, num_samples: int):
        self._validate_num_samples_for_influences(num_samples)
        self._get_current_project_obj().num_samples = num_samples

    def set_maximum_model_runner_failure_rate(
        self, maximum_model_runner_failure_rate: float
    ):
        raise NotSupportedError(
            "Setting the maximum model runner failure rate is currently unsupported for local projects!"
        )

    def get_maximum_model_runner_failure_rate(self) -> float:
        raise NotSupportedError(
            "Getting the maximum model runner failure rate is currently unsupported for local projects!"
        )

    def get_models(
        self,
        project_name: Optional[str] = None,
        data_collection_name: Optional[str] = None
    ) -> Sequence[str]:
        if not project_name:
            self._ensure_project()
            project_name = self.context.project_name
        if project_name in self.projects:
            models_mapping = self.projects[project_name].models
            if data_collection_name:
                if not data_collection_name in self.get_data_collections():
                    raise NotFoundError(
                        f"Data collection {data_collection_name} does not exist."
                    )
                return [
                    model_name for model_name in models_mapping
                    if models_mapping[model_name].data_collection.name ==
                    data_collection_name
                ]
            return list(models_mapping.keys())
        return []

    def set_model(self, model_name: str):
        if model_name == self._get_current_active_model_name():
            return
        if not model_name:
            self.context = dataclasses.replace(self.context, model_name=None)
            return
        self._ensure_project()
        if model_name not in self.get_models():
            raise ValueError(f"No such model {model_name}!")
        data_collection_name = self.projects[
            self.context.project_name].models[model_name].data_collection.name
        self._print_model_associated_with_different_data_collection_message(
            self.logger,
            model_name,
            data_collection_name,
            self._get_current_active_data_collection_name(),
            is_remote=False
        )
        self.set_data_collection(data_collection_name)
        self._print_set_model_context(self.logger, model_name, is_remote=False)
        self.context = dataclasses.replace(self.context, model_name=model_name)

    def delete_model(
        self, model_name: Optional[str] = None, *, recursive: bool = False
    ):
        self._ensure_project()
        if model_name not in self.get_models():
            raise ValueError(f"No such model {model_name}!")
        project_name = self._get_current_active_project_name()
        self.qii_cache.cleanup_cache_for_model(project_name, model_name)
        self.pd_cache.cleanup_cache_for_model(project_name, model_name)
        del self._get_current_project_obj().models[model_name]
        if self.context.model_name == model_name:
            self.context = dataclasses.replace(self.context, model_name=None)

    def get_data_collections(self, project_name: str = None) -> Sequence[str]:
        if not project_name:
            self._ensure_project()
            return list(self._get_current_project_obj().data_collections.keys())
        if project_name in self.projects:
            return list(self.projects[project_name].data_collections.keys())
        return []

    def get_data_splits(self) -> Sequence[str]:
        self._ensure_project()
        self._ensure_data_collection()
        return list(self._get_current_data_collection_obj().data_splits.keys())

    def add_data_collection(
        self,
        data_collection_name: str,
        pre_to_post_feature_map: Optional[Mapping[str, Sequence[str]]] = None,
        provide_transform_with_model: Optional[bool] = None
    ):
        self._validate_add_data_collection(
            data_collection_name,
            pre_to_post_feature_map=pre_to_post_feature_map
        )
        self.set_data_split(None)
        self.set_model(None)
        current_data_collection_name = self._get_current_active_data_collection_name(
        )
        transform_type = workspace_validation_utils.get_feature_transform_type_from_feature_map(
            pre_to_post_feature_map, provide_transform_with_model
        )
        self._get_current_project_obj().add_data_collection(
            data_collection_name, transform_type
        )
        self.context = dataclasses.replace(
            self.context, data_collection_name=data_collection_name
        )

        if pre_to_post_feature_map:
            data_collection_obj = self._get_current_project_obj(
            ).data_collections[self.context.data_collection_name]
            data_collection_obj.set_feature_map(pre_to_post_feature_map)
        self._print_change_data_collection_message(
            self.logger,
            current_data_collection_name,
            data_collection_name,
            is_remote=False
        )

    def _validate_set_data_collection(self, data_collection_name: str):
        # Returns whether data collection already exists.
        workspace_validation_utils.ensure_valid_identifier(data_collection_name)
        self._ensure_project()
        if data_collection_name not in self.get_data_collections():
            raise ValueError(
                f"No such data collection \"{data_collection_name}\"! See `add_data_collection` to add it."
            )

    def set_data_collection(self, data_collection_name: str):
        if data_collection_name == self._get_current_active_data_collection_name(
        ):
            return
        if data_collection_name:
            self._validate_set_data_collection(data_collection_name)
        self.set_data_split(None)
        self.set_model(None)
        current_data_collection_name = self._get_current_active_data_collection_name(
        )
        self.context = dataclasses.replace(
            self.context, data_collection_name=data_collection_name
        )
        self._print_change_data_collection_message(
            self.logger,
            current_data_collection_name,
            data_collection_name,
            is_remote=False
        )

    def set_data_split(self, data_split_name: str):
        if not data_split_name:
            self.context = dataclasses.replace(
                self.context, data_split_name=None
            )
            return
        self._ensure_project()
        self._ensure_data_collection()
        self._get_current_data_collection_obj(
        ).validate_data_split(data_split_name)
        self.context = dataclasses.replace(
            self.context, data_split_name=data_split_name
        )

    def add_python_model(
        self,
        model_name: str,
        model: Any,
        transformer: Optional[Any] = None,
        *,
        additional_pip_dependencies: Optional[Sequence[str]] = None,
        additional_modules: Optional[Sequence[Any]] = None,
        classification_threshold: Optional[float] = None,
        train_split_name: Optional[str] = None,
        train_parameters: Optional[Mapping[str, Any]] = None,
        verify_model: bool = True,
        compute_predictions: bool = True,
        compute_feature_influences: bool = False,
        compute_for_all_splits: bool = False,
        **kwargs
    ):
        self._validate_add_model(model_name)
        validate_model_metadata(
            train_split_name=train_split_name,
            existing_split_names=self.get_data_splits(),
            train_parameters=train_parameters,
            logger=self.logger
        )
        model_output_type = self._get_output_type()
        classification_threshold = workspace_validation_utils.validate_model_threshold(
            classification_threshold, self._get_score_type()
        )
        feature_transform_type = self._get_current_data_collection_obj(
        ).feature_transform_type
        self._get_current_project_obj().add_model_obj(
            model_name,
            model,
            transformer,
            self.context.data_collection_name,
            model_output_type,
            classification_threshold=classification_threshold,
            feature_transform_type=feature_transform_type,
            verify_model=verify_model
        )
        self._add_model_metadata(model_name, train_split_name, train_parameters)
        self.context = dataclasses.replace(self.context, model_name=model_name)
        self._print_add_model_message(
            self.logger,
            model_name,
            self._get_current_active_data_collection_name(),
            is_remote=False
        )

    def add_nn_model(
        self,
        model_name: str,
        model_or_load_wrapper: Union[Any, base.Wrappers.ModelLoadWrapper],
        model_run_wrapper: base.Wrappers.ModelRunWrapper,
        attribution_config,
        train_split_name: Optional[str] = None,
        train_parameters: Optional[Mapping[str, Any]] = None,
        **kwargs
    ):
        self._ensure_project()
        data_collection_name = self._ensure_data_collection()
        if model_name in self.get_models():
            raise ValueError(f"Model {model_name} already exists!")
        if model_or_load_wrapper == ModelType.VIRTUAL:
            self.logger.warning(
                'The model will not be available to query. This can happen if a virtual model was uploaded then re-downloaded. If you need a model object, reset the model with `delete_model` and `add_nn_model`'
            )
        elif not isinstance(
            model_or_load_wrapper, base.Wrappers.ModelLoadWrapper
        ):
            self.logger.warning(
                "Adding a model object instead of the load wrapper (see `ModelLoadWrapper`) means the model binary will not be uploaded to the TruEra platform during `upload_project` call."
            )
        if self._get_input_type() == "time_series_tabular":
            model_type = "rnn"
        elif self._get_input_type() == "text":
            model_type = "nlp"
        model_output_type = self._get_output_type()
        self._get_current_project_obj().add_model_obj(
            model_name,
            model_or_load_wrapper,
            None,
            data_collection_name,
            model_output_type,
            model_type=model_type,
            model_run_wrapper=model_run_wrapper
        )
        self._add_model_metadata(model_name, train_split_name, train_parameters)
        self.context = dataclasses.replace(self.context, model_name=model_name)

        self.update_nn_user_config(attribution_config)
        self._print_add_model_message(
            self.logger, model_name, data_collection_name, is_remote=False
        )

    def add_model(
        self,
        model_name: str,
        train_split_name: Optional[str] = None,
        train_parameters: Optional[Mapping[str, Any]] = None
    ):
        raise NotSupportedError(
            "Adding or registering models without a model object is not supported in local workspaces! See `tru.add_python_model()`."
        )

    def add_packaged_python_model(
        self,
        model_name: str,
        model_dir: str,
        data_collection_name: Optional[str] = None,
        train_split_name: Optional[str] = None,
        train_parameters: Optional[Mapping[str, Any]] = None,
        verify_model: bool = True,
        compute_predictions: bool = True,
        compute_feature_influences: bool = False,
        compute_for_all_splits: bool = False
    ):
        raise NotSupportedError(
            "Packaged Python models can only be ingested in remote workspaces!."
        )

    def create_packaged_python_model(
        self,
        output_dir: str,
        model_obj: Optional[Any] = None,
        additional_pip_dependencies: Optional[Sequence[str]] = None,
        additional_modules: Optional[Sequence[Any]] = None,
        model_path: Optional[str] = None,
        model_code_files: Optional[Sequence[str]] = None
    ):
        raise NotSupportedError(
            "Python models can only be packaged in remote workspaces!"
        )

    def verify_packaged_model(self, model_path: str):
        raise NotSupportedError(
            "Python models can only be packaged in remote workspaces!"
        )

    def delete_data_split(
        self,
        data_split_name: Optional[str] = None,
        *,
        recursive: bool = False
    ):
        with WorkspaceContextCleaner(self, delete_data_split=True):
            self._ensure_project()
            self._ensure_data_collection()
            data_split_name = data_split_name if data_split_name else self.context.data_split_name
            self.qii_cache.cleanup_cache_for_data_split(
                self.context.project_name, self.context.data_collection_name,
                data_split_name
            )
            self.pd_cache.cleanup_cache_for_data_split(
                self.context.project_name, self.context.data_collection_name,
                data_split_name
            )
            self._get_current_project_obj(
            ).clear_train_split_from_models(data_split_name)
            self._get_current_data_collection_obj(
            ).delete_data_split(data_split_name)

    def delete_data_collection(
        self,
        data_collection_name: Optional[str] = None,
        *,
        recursive: bool = False
    ):
        self._ensure_project()
        data_collection_name = data_collection_name if data_collection_name else self.context.data_collection_name
        self._get_current_project_obj().ensure_can_delete_data_collection(
            data_collection_name, recursive=recursive
        )
        with WorkspaceContextCleaner(self, delete_data_collection=True):
            self.set_data_collection(data_collection_name)
            for data_split in self.get_data_splits():
                self.delete_data_split(data_split)
            del self._get_current_project_obj(
            ).data_collections[data_collection_name]

    def add_data_split(
        self,
        data_split_name: str,
        pre_data: pd.DataFrame,
        *,
        post_data: Optional[pd.DataFrame] = None,
        label_data: Optional[Union[pd.DataFrame, pd.Series, np.ndarray]] = None,
        prediction_data: Optional[pd.DataFrame] = None,
        feature_influence_data: Optional[pd.DataFrame] = None,
        label_col_name: Optional[str] = None,
        id_col_name: Optional[str] = None,
        extra_data_df: Optional[pd.DataFrame] = None,
        split_type: Optional[str] = "all",
        timestamp_col_name: Optional[str] = None,
        background_split_name: Optional[str] = None,
        influence_type: Optional[str] = None,
        **kwargs
    ):
        if not isinstance(pre_data, pd.DataFrame):
            raise ValueError(
                "`pre_data` must be of type `pd.DataFrame` in local workspace!"
            )
        if post_data is not None and not isinstance(post_data, pd.DataFrame):
            raise ValueError(
                "`post_data` must be of type `pd.DataFrame` in local workspace!"
            )
        if kwargs.get("prediction_col_name") is not None:
            raise NotSupportedError(
                "Cannot supply predictions with data split in local workspace!"
            )
        if id_col_name is not None:
            raise NotSupportedError(
                "Cannot supply `id_col_name` with data split in local workspace!"
            )
        if timestamp_col_name is not None:
            raise NotSupportedError(
                "Cannot supply 'timestamp_col_name' with data split in local workspace!"
            )
        self._validate_add_data_split(
            data_split_name,
            pre_data=pre_data,
            post_data=post_data,
            label_data=label_data,
            label_col_name=label_col_name,
            extra_data_df=extra_data_df,
            split_type=split_type,
            **kwargs
        )
        if isinstance(label_data, pd.DataFrame):
            label_data = label_data[label_data.columns[0]].to_numpy().flatten()
        if label_col_name:
            label_data = pre_data[label_col_name]
            pre_data = pre_data.drop(columns=[label_col_name], inplace=False)
            if post_data is not None:
                post_data = post_data.drop(
                    columns=[label_col_name], inplace=False, errors="ignore"
                )

        self._get_current_data_collection_obj().add_data_split(
            name=data_split_name,
            xs_pre=pre_data,
            xs_post=post_data,
            extra=extra_data_df,
            ys=label_data,
            split_type=split_type
        )
        self.context = dataclasses.replace(
            self.context, data_split_name=data_split_name
        )
        self._print_add_data_split_message(
            self.logger, data_split_name, is_remote=False
        )

    def add_data_split_from_data_source(
        self,
        data_split_name: str,
        pre_data: Union[Table, str],
        *,
        post_data: Optional[Union[Table, str]] = None,
        label_col_name: Optional[str] = None,
        id_col_name: Optional[str] = None,
        extra_data: Optional[Union[Table, str]] = None,
        split_type: Optional[str] = "all",
        **kwargs
    ):
        raise NotSupportedError(
            "Adding data splits from data sources is not supported in local workspaces."
        )

    def add_labels(
        self, label_data: Union[Table, str], label_col_name: str,
        id_col_name: str, **kwargs
    ):
        raise NotSupportedError(
            "Adding labels after split creation is not supported in local workspaces. Use `add_data_split` to create a local data split with labels."
        )

    def add_extra_data(
        self, extra_data: Union[Table, str],
        extras_col_name: Union[str, Sequence[str]], id_col_name: str, **kwargs
    ):
        raise NotSupportedError(
            "Adding extra data after split creation is not supported in local workspaces. Use `add_data_split` to create a local data split with extra_data."
        )

    def add_nn_data_split(
        self,
        data_split_name: str,
        truera_wrappers: base.WrapperCollection,
        split_type: Optional[str] = "all",
        *,
        pre_data: Optional[Union[np.ndarray, pd.DataFrame]] = None,
        label_data: Optional[pd.DataFrame] = None,
        extra_data_df: Optional[pd.DataFrame] = None
    ):
        self._validate_add_nn_data_split(
            data_split_name, label_data, extra_data_df
        )
        self._get_current_data_collection_obj().add_nn_data_split(
            data_split_name,
            truera_wrappers,
            split_type,
            xs_pre=pre_data,
            ys=label_data,
            extra_data_df=extra_data_df
        )
        self.context = dataclasses.replace(
            self.context, data_split_name=data_split_name
        )
        self._print_add_data_split_message(
            self.logger, data_split_name, is_remote=False
        )

    def add_model_predictions(
        self,
        prediction_data: Union[pd.Series, np.ndarray, Table, str],
        *,
        prediction_col_name: Optional[str] = None,
        id_col_name: Optional[str] = None,
        data_split_name: Optional[str] = None
    ):
        raise NotSupportedError(
            "Adding model predictions is not supported in local workspaces!"
        )

    def add_model_feature_influences(
        self,
        feature_influence_data: pd.DataFrame,
        *,
        data_split_name: Optional[str] = None,
        background_split_name: Optional[str] = None,
        id_col_name: Optional[str] = None,
        timestamp_col_name: Optional[str] = None,
        influence_type: Optional[str] = None
    ):
        raise NotSupportedError(
            "Adding model influences is not supported in local workspaces!"
        )

    def attach_packaged_python_model_object(
        self, model_object_dir: str, verify_model: bool = True
    ):
        raise NotSupportedError(
            "Attaching model objects to virtual models is not supported in local workspaces!"
        )

    def attach_python_model_object(
        self,
        model_object: Any,
        additional_pip_dependencies: Optional[Sequence[str]] = None,
        verify_model: bool = True,
    ):
        raise NotSupportedError(
            "Attaching model objects to virtual models is not supported in local workspaces!"
        )

    def add_feature_metadata(
        self,
        feature_description_map: Optional[Mapping[str, str]] = None,
        missing_values: Optional[Sequence[str]] = None,
        force_update: bool = False
    ):
        self._ensure_project()
        self._ensure_data_collection()
        if feature_description_map is not None:
            raise NotSupportedError(
                "Adding feature descriptions is not supported in local project."
            )
        if missing_values is not None:
            raise NotSupportedError(
                "Adding missing values is not supported in local project."
            )

        previous_feature_map = self._get_pre_to_post_feature_map()
        if not force_update and previous_feature_map is not None:
            raise AlreadyExistsError(
                f"Feature list already present for project `{self._get_current_active_project_name()}` in data-collection {self._get_current_active_data_collection_name()}"
            )

    def _get_pre_to_post_feature_map(
        self
    ) -> Optional[Mapping[str, Sequence[str]]]:
        self._ensure_project()
        self._ensure_data_collection()
        data_collection_obj = self._get_current_project_obj().data_collections[
            self.context.data_collection_name]
        return data_collection_obj.feature_map

    def get_ingestion_client(self):
        raise NotSupportedError(
            "Ingestion client is not supported in local project."
        )

    def get_data_sources(self):
        raise NotSupportedError(
            "Remote data sources are not supported in local projects"
        )

    def delete_data_source(self, name):
        raise NotSupportedError(
            "Remote data sources are not supported in local projects"
        )

    def add_segment_group(
        self, name: str, segment_definitions: Mapping[str, str]
    ) -> None:
        self._validate_add_segment_group(name, segment_definitions)
        self._get_current_project_obj().add_segment_group(
            name, segment_definitions,
            self._get_current_active_data_collection_name(),
            self._get_current_active_data_split_name()
        )

    def set_as_protected_segment(
        self, segment_group_name: str, segment_name: str
    ):
        raise NotSupportedError(
            "Protected segments are not supported in local projects"
        )

    def delete_segment_group(self, name: str) -> None:
        self._ensure_project()
        self._get_current_project_obj().delete_segment_group(name)

    def get_segment_groups(self) -> Mapping[str, Mapping[str, str]]:
        self._ensure_project()
        segment_groups = self._get_current_project_obj().get_segment_groups()
        return self._get_str_desc_of_segment_groups(segment_groups)

    def get_explainer(
        self,
        base_data_split: Optional[str] = None,
        comparison_data_splits: Optional[Sequence[str]] = None
    ) -> LocalExplainer:
        self._ensure_project()
        self._ensure_model()
        project_obj = self._get_current_project_obj()
        model_obj = project_obj.models[self.context.model_name]
        data_collection_obj = project_obj.data_collections[
            self.context.data_collection_name]
        if model_obj is not None and model_obj.model_type == 'rnn':
            project_model_key = (
                self.context.project_name, self.context.model_name
            )
            attr_config = self.rnn_attr_configs[project_model_key]
            return LocalRNNExplainer(
                model_obj, data_collection_obj, base_data_split, project_obj,
                attr_config, self.qii_cache, self.logger
            )
        elif model_obj is not None and model_obj.model_type == 'nlp':
            project_model_key = (
                self.context.project_name, self.context.model_name
            )
            attr_config = self.nlp_attr_configs[project_model_key]
            return LocalNLPExplainer(
                model_obj, data_collection_obj, base_data_split, project_obj,
                attr_config, self.qii_cache, self.logger
            )
        return LocalExplainer(
            self, project_obj, model_obj, data_collection_obj, base_data_split,
            comparison_data_splits
        )

    def get_xs(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        extra_data: bool = False,
        system_data: bool = False
    ) -> pd.DataFrame:
        if system_data:
            raise ValueError("`system_data` is not supported in local!")
        start, stop = self._convert_start_stop(start, stop)
        project_obj = self._get_current_project_obj()
        data_collection_obj = project_obj.data_collections[
            self.context.data_collection_name]
        data_split_obj = data_collection_obj.data_splits[
            self.context.data_split_name]
        data = data_split_obj.xs_pre
        if isinstance(data, pd.DataFrame):
            ret = data.iloc[start:stop, :]
        elif isinstance(data, np.ndarray):
            ret = data[start:stop, :]
        else:
            raise TypeError(
                f"Data must be of type pandas.DataFrame or numpy.ndarray. Found {type(data)}."
            )
        if extra_data and data_split_obj.extra is not None:
            ret = ret.join(data_split_obj.extra)
        return ret

    def get_ys(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        system_data: bool = False
    ) -> pd.Series:
        if system_data:
            raise ValueError("`system_data` is not supported in local!")
        start, stop = self._convert_start_stop(start, stop)
        project_obj = self._get_current_project_obj()
        data_collection_obj = project_obj.data_collections[
            self.context.data_collection_name]
        data = data_collection_obj.data_splits[self.context.data_split_name].ys
        if isinstance(data, pd.Series):
            return data.iloc[start:stop]
        elif data is None:
            raise NotFoundError("Labels were not found for this data split.")
        raise TypeError(
            f"Data must be of type pandas.Series. Found {type(data)}."
        )

    def get_model_threshold(self) -> float:
        self._validate_get_model_threshold()
        return self._get_current_project_obj().models[self.context.model_name
                                                     ].classification_threshold

    def update_model_threshold(self, classification_threshold: float) -> None:
        self._ensure_project()
        self._ensure_model()
        if self._get_output_type() == "regression":
            self.logger.warning(
                "Regression models do not use a threshold. Ignoring request to update."
            )
            return
        score_type = self._get_score_type()
        classification_threshold = workspace_validation_utils.validate_model_threshold(
            classification_threshold, score_type
        )
        self._get_current_project_obj().models[
            self.context.model_name
        ].set_classification_threshold(classification_threshold)

    def set_influences_background_data_split(
        self,
        data_split_name: str,
        data_collection_name: Optional[str] = None
    ) -> None:
        self._ensure_project()
        if self._get_input_type() == "time_series_tabular":
            raise NotSupportedError(
                "This functionality is currently not supported for \"time_series_tabular\" project!"
            )
        if data_collection_name:
            self._validate_data_collection(data_collection_name)
        else:
            self._ensure_data_collection()
            data_collection_name = self._get_current_active_data_collection_name(
            )
        self._get_current_project_obj().data_collections[
            data_collection_name].set_base_split(data_split_name)

    def get_influences_background_data_split(
        self,
        data_collection_name: Optional[str] = None,
    ) -> str:
        self._ensure_project()
        if self._get_input_type() == "time_series_tabular":
            raise NotSupportedError(
                "This functionality is currently not supported for \"time_series_tabular\" project!"
            )
        if data_collection_name:
            self._validate_data_collection(data_collection_name)
        else:
            self._ensure_data_collection()
            data_collection_name = self._get_current_active_data_collection_name(
            )
        data_collection = self._get_current_project_obj(
        ).data_collections[data_collection_name]
        if data_collection.base_split is None:
            raise ValueError(
                f"Background data split has not been set for data collection \"{data_collection.name}\"! Please set it using `set_influences_background_data_split`"
            )
        return data_collection.base_split.name

    def get_context(self) -> Mapping[str, str]:
        return {
            "project": self.context.project_name or "",
            "data-collection": self.context.data_collection_name or "",
            "data-split": self.context.data_split_name or "",
            "model": self.context.model_name or "",
        }

    def _get_current_project_obj(self) -> Project:
        return self.projects[self.context.project_name]

    def _get_current_data_collection_obj(self) -> DataCollection:
        return self._get_current_project_obj().data_collections[
            self.context.data_collection_name]

    def _get_score_type(self):
        return self._get_current_project_obj().score_type

    def _get_input_type(self):
        self._ensure_project()
        return self._get_current_project_obj().input_type

    def _convert_start_stop(self, start: Optional[int], stop: Optional[int]):
        if start is None:
            start = 0
        return start, stop

    def verify_nn_wrappers(
        self,
        *,
        clf: NNB.Model,
        model_run_wrapper: base.Wrappers.ModelRunWrapper,
        split_load_wrapper: base.Wrappers.SplitLoadWrapper,
        model_load_wrapper: Optional[base.Wrappers.ModelLoadWrapper] = None,
        tokenizer_wrapper: Optional[nlp.Wrappers.TokenizerWrapper] = None,
        attr_config: AttributionConfiguration = None
    ) -> None:
        """Validates that all wrappers and methods are well formed.

        Args:
            clf (NNB.Model): The model object.
            model_run_wrapper (base.Wrappers.ModelRunWrapper): The ModelRunWrapper implementation.
            split_load_wrapper (base.Wrappers.SplitLoadWrapper): The SplitLoadWrapper implementation.
            model_load_wrapper (Optional[base.Wrappers.ModelLoadWrapper], optional): The ModelLoadWrapper implementation.
            tokenizer_wrapper (Optional[nlp.Wrappers.TokenizerWrapper], optional): The TokenizerWrapper implementation. This is only needed for input_type 'text'.
            attr_config (AttributionConfiguration, optional): The run configurations.
        """
        from truera.client.cli.verify_nn_ingestion import verify
        from truera.client.cli.verify_nn_ingestion import VerifyHelper

        try:
            self._ensure_project()
        except ValueError:
            raise ValueError(
                "No project set in the TruEra Workspace. A project is needed to determine the correct data type to validate against. Add a project with .add_project() or set the current project using `.set_project()`."
            )
        project_input_type = self.projects[
            self._get_current_active_project_name()].input_type

        score_type = self._get_current_project_obj().score_type
        output_type = get_output_type_from_score_type(score_type)
        from truera.client.cli.verify_nn_ingestion import verify
        from truera.client.cli.verify_nn_ingestion import VerifyHelper
        verify_helper: VerifyHelper = verify.get_helper(
            model_input_type=project_input_type,
            model_output_type=output_type,
            attr_config=attr_config,
            model=clf,
            split_load_wrapper=split_load_wrapper,
            model_run_wrapper=model_run_wrapper,
            model_load_wrapper=model_load_wrapper,
            tokenizer_wrapper=tokenizer_wrapper
        )

        verify_helper.verify_wrapper_types()
        verify_helper.verify_attr_config()

        super(LocalTrueraWorkspace,
              self)._verify_nn_wrappers(verify_helper, logger=self.logger)

    def _get_project_model_key(self):
        project_name = self._ensure_project()
        model_name = self._ensure_model()
        return (project_name, model_name)

    def get_nn_user_configs(
        self
    ) -> Union[AttributionConfiguration, RNNUserInterfaceConfiguration]:
        project_model_key = self._get_project_model_key()
        if project_model_key in self.rnn_attr_configs:
            return self.rnn_attr_configs[project_model_key]
        elif project_model_key in self.nlp_attr_configs:
            return self.nlp_attr_configs[project_model_key]
        return None

    def update_nn_user_config(
        self, config: Union[AttributionConfiguration,
                            RNNUserInterfaceConfiguration]
    ):
        project_model_key = self._get_project_model_key()
        if isinstance(config, RNNAttributionConfiguration):
            self.rnn_attr_configs[project_model_key] = config
        elif isinstance(config, NLPAttributionConfiguration):
            self.nlp_attr_configs[project_model_key] = config
        elif isinstance(config, RNNUserInterfaceConfiguration):
            return
        else:
            raise ValueError(
                f"Unrecognized user config: {type(config)}. Current supported configs are AttributionConfiguration and UIConfig."
            )

    def add_model_metadata(
        self,
        train_split_name: Optional[str] = None,
        train_parameters: Optional[Mapping[str, Any]] = None,
        overwrite: bool = False
    ) -> None:
        self._ensure_project()
        model_name = self._ensure_model()
        validate_model_metadata(
            train_split_name=train_split_name,
            existing_split_names=self.get_data_splits(),
            train_parameters=train_parameters,
            logger=self.logger
        )
        self._add_model_metadata(
            model_name, train_split_name, train_parameters, overwrite
        )

    def _add_model_metadata(
        self,
        model_name: str,
        train_split_name: Optional[str] = None,
        train_parameters: Optional[Mapping[str, Any]] = None,
        overwrite: bool = False
    ) -> None:
        model_metadata = self._get_model_metadata(model_name)
        existing_train_split_name = model_metadata["train_split_name"]
        existing_train_parameters = model_metadata["train_parameters"]
        validate_add_model_metadata(
            model_name=model_name,
            train_split_name=train_split_name,
            existing_train_split_name=existing_train_split_name,
            train_parameters=train_parameters,
            existing_train_parameters=existing_train_parameters,
            overwrite=overwrite
        )
        model = self._get_current_project_obj().models[model_name]
        if train_split_name:
            model.train_split_name = train_split_name
        if train_parameters:
            model.train_parameters = train_parameters

    def delete_model_metadata(self) -> None:
        self._ensure_project()
        model_name = self._ensure_model()
        model = self._get_current_project_obj().models[model_name]
        model.train_split_name = None
        model.train_parameters = None

    def get_model_metadata(self) -> Mapping[str, Union[str, Mapping[str, str]]]:
        self._ensure_project()
        model_name = self._ensure_model()
        return self._get_model_metadata(model_name)

    def _get_model_metadata(
        self, model_name: str
    ) -> Mapping[str, Union[str, Mapping[str, str]]]:
        model = self._get_current_project_obj().models[model_name]
        return {
            "train_split_name": model.train_split_name,
            "train_parameters": model.train_parameters
        }

    def _get_project_settings(self,
                              project: str) -> Mapping[str, Union[str, int]]:
        return {
            "input_type":
                self.projects[project].input_type,
            "score_type":
                self.projects[project].score_type,
            "num_default_influences":
                self.projects[project].num_default_influences,
        }

    def _delete_empty_project(self):
        del self.projects[self.context.project_name]

    def reset_context(self):
        self.set_model(None)
        self.set_data_collection(None)
        self.context = dataclasses.replace(self.context, project_name=None)

    def schedule_ingestion(self, raw_json: str, cron_schedule: str):
        raise NotSupportedError(
            "Scheduled ingestion not supported in local workspace!"
        )

    def get_scheduled_ingestion(self, workflow_id: str):
        raise NotSupportedError(
            "Scheduled ingestion not supported in local workspace!"
        )

    def schedule_existing_data_split(
        self,
        split_name: str,
        cron_schedule: str,
        override_split_name: str = None,
        append: bool = True
    ):
        raise NotSupportedError(
            "Scheduled ingestion not supported in local workspace!"
        )

    def serialize_split(
        self,
        split_name: str,
        override_split_name: str = None,
    ) -> str:
        raise NotSupportedError(
            "Scheduled ingestion not supported in local workspace!"
        )

    def cancel_scheduled_ingestion(self, workflow_id: str) -> str:
        raise NotSupportedError(
            "Scheduled ingestion not supported in local workspace!"
        )

    def list_scheduled_ingestions(
        self, last_key: str = None, limit: int = 50
    ) -> str:
        raise NotSupportedError(
            "Scheduled ingestion not supported in local workspace!"
        )

    def _get_feature_transform_type_for_data_collection(self):
        data_collection_obj = self._get_current_data_collection_obj()
        return data_collection_obj.feature_transform_type

    def list_monitoring_tables(self) -> str:
        raise NotSupportedError(
            "Listing Monitoring tables is not supported in local workspace!"
        )
