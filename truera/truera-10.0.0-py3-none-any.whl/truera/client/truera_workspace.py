from __future__ import annotations

import importlib.util
import logging
import os
from pathlib import Path
import pickle
import shutil
import tempfile
from typing import Any, Dict, Mapping, Optional, Sequence, TYPE_CHECKING, Union

import numpy as np
import pandas as pd
import yaml

from truera.client.base_truera_workspace import BaseTrueraWorkspace
from truera.client.client_utils import get_model_type_from_string
from truera.client.errors import MetadataNotFoundException
from truera.client.errors import NotFoundError
from truera.client.ingestion_client import Credential
from truera.client.ingestion_client import IngestionClient
from truera.client.ingestion_client import Table
from truera.client.intelligence.explainer import Explainer
from truera.client.nn import wrappers as base
from truera.client.nn.client_configs import AttributionConfiguration
from truera.client.nn.client_configs import DEFAULT_NN_HASH_BG
from truera.client.nn.client_configs import NLPAttributionConfiguration
from truera.client.nn.client_configs import RNNAttributionConfiguration
from truera.client.nn.client_configs import RNNUserInterfaceConfiguration
from truera.client.nn.wrappers import nlp
from truera.client.public.communicator.http_communicator import \
    AlreadyExistsError
from truera.client.public.communicator.http_communicator import \
    NotSupportedError
from truera.client.remote_truera_workspace import RemoteTrueraWorkspace
from truera.client.services.artifact_interaction_client import \
    ArtifactInteractionClient
from truera.client.services.artifact_interaction_client import \
    ModelCacheUploader
from truera.client.services.artifactrepo_client import ArtifactType
from truera.client.truera_authentication import TrueraAuthentication
from truera.client.truera_workspace_utils import create_temp_file_path
from truera.client.truera_workspace_utils import ExplainerQiiCacheKey
from truera.client.truera_workspace_utils import sample_spark_dataframe
from truera.client.util import workspace_validation_utils
from truera.protobuf.public.metadata_message_types_pb2 import \
    CacheType  # pylint: disable=no-name-in-module
from truera.protobuf.public.metadata_message_types_pb2 import \
    FEATURE_TRANSFORM_TYPE_MODEL_FUNCTION  # pylint: disable=no-name-in-module
from truera.protobuf.public.metadata_message_types_pb2 import \
    FEATURE_TRANSFORM_TYPE_PRE_POST_DATA  # pylint: disable=no-name-in-module
from truera.protobuf.public.metadata_message_types_pb2 import \
    ModelType  # pylint: disable=no-name-in-module
from truera.protobuf.public.qoi_pb2 import \
    ExplanationAlgorithmType  # pylint: disable=no-name-in-module
from truera.utils.general import safe_isinstance

if TYPE_CHECKING:
    from truera.client.local.local_artifacts import Project
    from truera.client.local.local_truera_workspace import LocalTrueraWorkspace


def is_local_enabled() -> bool:
    try:
        import truera.client.local
        return True
    except ModuleNotFoundError:
        return False


class TrueraWorkspace(BaseTrueraWorkspace):
    """Workspace for Truera computations --- both local and remote."""

    _VALID_UPLOAD_STRATEGIES = [
        "create_new_project", "overwrite_project", "add_to_project"
    ]

    _VALID_DOWNLOAD_STRATEGIES = [
        "create_new_project", "overwrite_project", "add_to_project"
    ]

    def __init__(
        self,
        connection_string: Optional[str] = None,
        authentication: Optional[TrueraAuthentication] = None,
        log_level: int = logging.INFO,
        **kwargs
    ) -> None:
        """Construct a new TruEra workspace.
        Args:
            connection_string: URL of the TruEra deployment. Defaults to None.
            authentication: Credentials to connect to TruEra deployment. Defaults to None.
            log_level: Log level (defaults to `logging.INFO`).
            **verify_cert (bool|str): When set to `False` certificate verification failures will be ignored (not recommended).
                A path to certificate file or directory can also be provided. If `verify_cert` is set to a path to a directory,
                the directory must have been processed using the c_rehash utility supplied with OpenSSL.
        Raises:
            ValueError: Raised if exactly one of connection_string and authentication is None.
        """
        logging.basicConfig(
        )  # Have to do this in order to enable setting log level below WARNING in jupyter
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        self.remote_tru = None
        if connection_string or authentication:
            self.set_remote_environment(
                connection_string, authentication, **kwargs
            )
        self._local_tru = None
        if is_local_enabled():
            from truera.client.local.local_truera_workspace import \
                LocalTrueraWorkspace
            self._local_tru = LocalTrueraWorkspace(log_level)
            self.current_tru = self._local_tru
        else:
            if self.remote_tru is None:
                raise ValueError(
                    "Local analytics are not enabled! Pass in your remote TruEra `connection_string` and `authentication` credentials."
                )
            self.current_tru = self.remote_tru

        self.data_profiler = self.current_tru.data_profiler
        self.tester = self.current_tru.tester
        self._data_tempdir = tempfile.TemporaryDirectory()

    @property
    def local_tru(self) -> LocalTrueraWorkspace:
        if self._local_tru is None:
            raise ValueError(
                "Local analytics are not enabled! To use local functionality, upgrade your TruEra SDK."
            )
        return self._local_tru

    @property
    def artifact_interaction_client(
        self
    ) -> Optional[ArtifactInteractionClient]:
        if self.remote_tru is not None:
            return self.remote_tru.artifact_interaction_client
        return None

    def set_environment(self, environment: str):
        """Set the environment (either local or remote) for the workspace.
        Args:
            environment (str): Workspace environment to set. Must be either "local" or "remote".
        """
        if environment not in ["remote", "local"]:
            raise ValueError(
                "Environment must be set to either `local` or `remote`!"
            )
        if environment == "remote":
            if self.remote_tru is None:
                raise ValueError(
                    "Remote TrueraWorkspace is not set! Set the remote environment using `set_remote_environment`."
                )
            self.current_tru = self.remote_tru
            self.data_profiler = self.current_tru.data_profiler
            self.tester = self.current_tru.tester
        else:
            self.current_tru = self.local_tru
            self.data_profiler = self.current_tru.data_profiler
            self.tester = self.current_tru.tester

    def get_environment(self) -> str:
        """Get the environment (either local or remote) for the workspace.
        Returns:
            str: Current workspace environment. Either "local" or "remote".
        """
        return "remote" if self.current_tru == self.remote_tru else "local"

    def get_projects(self) -> Sequence[str]:
        return self.current_tru.get_projects()

    def _entity_exists(self, entity_name: str, entity_get_func):
        return entity_name in entity_get_func()

    def _get_project_settings(self,
                              project: str) -> Mapping[str, Union[str, int]]:
        return self.current_tru._get_project_settings(project)

    def add_project(
        self,
        project: str,
        score_type: str,
        input_type: Optional[str] = "tabular",
        num_default_influences: Optional[int] = None
    ):
        if workspace_validation_utils.is_nontabular_project(
            input_type
        ) and self.get_environment() == "remote":
            raise ValueError(
                f"Project with input type of `{input_type}` can only be created locally! Please set environment to \"local\" before proceeding."
            )
        self.current_tru.add_project(
            project,
            score_type=score_type,
            input_type=input_type,
            num_default_influences=num_default_influences
        )

    def set_project(self, project: str):
        return self.current_tru.set_project(project)

    def set_score_type(self, score_type: str):
        return self.current_tru.set_score_type(score_type)

    def set_influence_type(self, algorithm: str):
        if algorithm not in ["truera-qii", "shap"]:
            return ValueError(
                "Influence algorithm type must be one of [\"truera-qii\", \"shap\"]!"
            )
        return self.current_tru.set_influence_type(algorithm)

    def get_influence_type(self) -> str:
        return self.current_tru.get_influence_type()

    def get_num_default_influences(self) -> int:
        return self.current_tru.get_num_default_influences()

    def set_num_default_influences(self, num_default_influences: int):
        return self.current_tru.set_num_default_influences(
            num_default_influences
        )

    def list_performance_metrics(self) -> Sequence[str]:
        return self.current_tru.list_performance_metrics()

    def get_default_performance_metrics(self) -> Sequence[str]:
        return self.current_tru.get_default_performance_metrics()

    def set_default_performance_metrics(
        self, performance_metrics: Sequence[str]
    ):
        return self.current_tru.set_default_performance_metrics(
            performance_metrics
        )

    def get_num_internal_qii_samples(self) -> int:
        return self.current_tru.get_num_internal_qii_samples()

    def set_num_internal_qii_samples(self, num_samples: int) -> None:
        return self.current_tru.set_num_internal_qii_samples(num_samples)

    def set_maximum_model_runner_failure_rate(
        self, maximum_model_runner_failure_rate: float
    ):
        return self.current_tru.set_maximum_model_runner_failure_rate(
            maximum_model_runner_failure_rate
        )

    def get_maximum_model_runner_failure_rate(self) -> float:
        return self.current_tru.get_maximum_model_runner_failure_rate()

    def get_models(self) -> Sequence[str]:
        return self.current_tru.get_models()

    def set_model(self, model_name: str):
        self.current_tru.set_model(model_name)

    def delete_model(
        self, model_name: Optional[str] = None, *, recursive: bool = False
    ):
        model_name = model_name or self._get_current_active_model_name()
        if not model_name:
            raise ValueError(
                "Must provide `model_name` or set the current model using `set_model`!"
            )
        self.current_tru.delete_model(model_name, recursive=recursive)

    def get_data_collections(self) -> Sequence[str]:
        return self.current_tru.get_data_collections()

    def get_data_splits(self) -> Sequence[str]:
        return self.current_tru.get_data_splits()

    def add_data_collection(
        self,
        data_collection_name: str,
        pre_to_post_feature_map: Optional[Mapping[str, Sequence[str]]] = None,
        provide_transform_with_model: Optional[bool] = None
    ):
        self.current_tru.add_data_collection(
            data_collection_name,
            pre_to_post_feature_map=pre_to_post_feature_map,
            provide_transform_with_model=provide_transform_with_model
        )

    def set_data_collection(self, data_collection_name: str):
        self.current_tru.set_data_collection(data_collection_name)

    def set_data_split(self, data_split_name: str):
        self.current_tru.set_data_split(data_split_name)

    def set_influences_background_data_split(
        self,
        data_split_name: str,
        data_collection_name: Optional[str] = None
    ) -> None:
        self.current_tru.set_influences_background_data_split(
            data_split_name, data_collection_name
        )

    def get_influences_background_data_split(
        self,
        data_collection_name: Optional[str] = None,
    ) -> str:
        return self.current_tru.get_influences_background_data_split(
            data_collection_name
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
        self.current_tru.add_python_model(
            model_name,
            model,
            transformer,
            additional_pip_dependencies=additional_pip_dependencies,
            additional_modules=additional_modules,
            classification_threshold=classification_threshold,
            train_split_name=train_split_name,
            train_parameters=train_parameters,
            verify_model=verify_model,
            compute_predictions=compute_predictions,
            compute_feature_influences=compute_feature_influences,
            compute_for_all_splits=compute_for_all_splits,
            **kwargs
        )

    def add_nn_model(
        self,
        model_name: str,
        truera_wrappers: base.WrapperCollection,
        attribution_config: dict,
        model: Optional[Any] = None,
        train_split_name: Optional[str] = None,
        train_parameters: Optional[Mapping[str, Any]] = None,
        **kwargs
    ):
        if workspace_validation_utils.is_tabular_project(
            self._get_input_type()
        ):
            raise ValueError(
                "Adding NN models is not supported for `tabular` project."
            )

        model_arg = model if model is not None else truera_wrappers.model_load_wrapper
        workspace_validation_utils.ensure_valid_identifier(model_name)
        self.current_tru.add_nn_model(
            model_name, model_arg, truera_wrappers.model_run_wrapper,
            attribution_config, train_split_name, train_parameters, **kwargs
        )

    def add_model(
        self,
        model_name,
        train_split_name: Optional[str] = None,
        train_parameters: Optional[Mapping[str, Any]] = None,
    ):
        self.current_tru.add_model(
            model_name, train_split_name, train_parameters
        )

    def create_packaged_python_model(
        self,
        output_dir: str,
        model_obj: Optional[Any] = None,
        additional_pip_dependencies: Optional[Sequence[str]] = None,
        additional_modules: Optional[Sequence[Any]] = None,
        model_path: Optional[str] = None,
        model_code_files: Optional[Sequence[str]] = None,
        **kwargs
    ):
        self.current_tru.create_packaged_python_model(
            output_dir,
            model_obj=model_obj,
            additional_pip_dependencies=additional_pip_dependencies,
            additional_modules=additional_modules,
            model_path=model_path,
            model_code_files=model_code_files,
            **kwargs
        )

    def verify_packaged_model(self, model_path: str):
        self.current_tru.verify_packaged_model(model_path)

    def add_packaged_python_model(
        self,
        model_name: str,
        model_dir: str,
        *,
        data_collection_name: Optional[str] = None,
        train_split_name: Optional[str] = None,
        train_parameters: Optional[Mapping[str, Any]] = None,
        verify_model: bool = True,
        compute_predictions: bool = True,
        compute_feature_influences: bool = False,
        compute_for_all_splits: bool = False,
    ):
        return self.current_tru.add_packaged_python_model(
            model_name,
            model_dir,
            data_collection_name=data_collection_name,
            train_split_name=train_split_name,
            train_parameters=train_parameters,
            verify_model=verify_model,
            compute_predictions=compute_predictions,
            compute_feature_influences=compute_feature_influences,
            compute_for_all_splits=compute_for_all_splits
        )

    def add_model_metadata(
        self,
        train_split_name: Optional[str] = None,
        train_parameters: Optional[Mapping[str, Any]] = None,
        overwrite: bool = False
    ) -> None:
        self.current_tru.add_model_metadata(
            train_split_name, train_parameters, overwrite
        )

    def delete_model_metadata(self) -> None:
        self.current_tru.delete_model_metadata()

    def get_model_metadata(self) -> Mapping[str, Union[str, Mapping[str, str]]]:
        return self.current_tru.get_model_metadata()

    def _get_model_metadata(
        self, model_name: str
    ) -> Mapping[str, Union[str, Mapping[str, str]]]:
        return self.current_tru._get_model_metadata(model_name)

    def delete_data_split(
        self,
        data_split_name: Optional[str] = None,
        *,
        recursive: bool = False
    ):
        data_split_name = data_split_name or self._get_current_active_data_split_name(
        )
        if not data_split_name:
            raise ValueError(
                "Must provide `data_split_name` or set the current data split using `set_data_split`!"
            )
        self.current_tru.delete_data_split(data_split_name, recursive=recursive)

    def delete_data_collection(
        self,
        data_collection_name: Optional[str] = None,
        *,
        recursive: bool = False
    ):
        data_collection_name = data_collection_name or self._get_current_active_data_collection_name(
        )
        if not data_collection_name:
            raise ValueError(
                "Must provide `data_collection_name` or set the current data collection using `set_data_collection`!"
            )
        self.current_tru.delete_data_collection(
            data_collection_name, recursive=recursive
        )

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
        background_split_name: Optional[str] = None,
        influence_type: Optional[str] = None,
        **kwargs
    ):
        if workspace_validation_utils.is_nontabular_project(
            self._get_input_type()
        ):
            raise ValueError(
                "Adding split using `add_data_split` is not supported for `time_series_tabular` or `nlp` projects. Use `add_nn_data_split` instead."
            )

        sample_count = kwargs.pop("sample_count", 5000)
        sample_kind = kwargs.pop("sample_kind", "random")
        seed = kwargs.pop("seed", 0)

        if safe_isinstance(pre_data, "pyspark.sql.dataframe.DataFrame"):
            pre_data = sample_spark_dataframe(
                pre_data,
                sample_count=sample_count,
                sample_kind=sample_kind,
                seed=seed,
                logger=self.logger
            )
        if safe_isinstance(post_data, "pyspark.sql.dataframe.DataFrame"):
            post_data = sample_spark_dataframe(
                post_data,
                sample_count=sample_count,
                sample_kind=sample_kind,
                seed=seed,
                logger=self.logger
            )
        self.current_tru.add_data_split(
            data_split_name,
            pre_data=pre_data,
            post_data=post_data,
            label_data=label_data,
            prediction_data=prediction_data,
            feature_influence_data=feature_influence_data,
            label_col_name=label_col_name,
            id_col_name=id_col_name,
            extra_data_df=extra_data_df,
            split_type=split_type,
            timestamp_col_name=kwargs.pop("timestamp_col_name", None),
            sample_count=sample_count,
            background_split_name=background_split_name,
            influence_type=influence_type,
            **kwargs
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
        self.current_tru.add_data_split_from_data_source(
            data_split_name,
            pre_data=pre_data,
            post_data=post_data,
            label_col_name=label_col_name,
            id_col_name=id_col_name,
            extra_data=extra_data,
            split_type=split_type,
            **kwargs
        )

    def add_labels(
        self, label_data: Union[Table, str], label_col_name: str,
        id_col_name: str, **kwargs
    ):
        if workspace_validation_utils.is_nontabular_project(
            self._get_input_type()
        ):
            raise NotSupportedError(
                "Adding labels after split creation is not supported for non-tabular projects. Use `add_nn_data_split` instead."
            )
        self.current_tru.add_labels(
            label_data=label_data,
            label_col_name=label_col_name,
            id_col_name=id_col_name,
            **kwargs
        )

    def add_extra_data(
        self, extra_data: Union[Table, str],
        extras_col_name: Union[str, Sequence[str]], id_col_name: str, **kwargs
    ):
        if workspace_validation_utils.is_nontabular_project(
            self._get_input_type()
        ):
            raise NotSupportedError(
                "Adding extra_data after split creation is only supported for `tabular` project."
            )
        self.current_tru.add_extra_data(
            extra_data=extra_data,
            extras_col_name=extras_col_name,
            id_col_name=id_col_name,
            **kwargs
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
        self.current_tru.add_nn_data_split(
            data_split_name,
            truera_wrappers,
            split_type,
            pre_data=pre_data,
            label_data=label_data,
            extra_data_df=extra_data_df
        )

    def add_model_predictions(
        self,
        prediction_data: Union[pd.Series, np.ndarray, Table, str],
        *,
        prediction_col_name: Optional[str] = None,
        id_col_name: Optional[str] = None,
        data_split_name: Optional[str] = None
    ):
        self.current_tru.add_model_predictions(
            prediction_data=prediction_data,
            prediction_col_name=prediction_col_name,
            id_col_name=id_col_name,
            data_split_name=data_split_name
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

        self.current_tru.add_model_feature_influences(
            feature_influence_data,
            data_split_name=data_split_name,
            background_split_name=background_split_name,
            id_col_name=id_col_name,
            timestamp_col_name=timestamp_col_name,
            influence_type=influence_type
        )

    def attach_packaged_python_model_object(
        self, model_object_dir: str, verify_model: bool = True
    ):
        return self.current_tru.attach_packaged_python_model_object(
            model_object_dir, verify_model=verify_model
        )

    def attach_python_model_object(
        self,
        model_object: Any,
        additional_pip_dependencies: Optional[Sequence[str]] = None,
        verify_model: bool = True,
    ):
        return self.current_tru.attach_python_model_object(
            model_object,
            additional_pip_dependencies=additional_pip_dependencies,
            verify_model=verify_model
        )

    def add_feature_metadata(
        self,
        feature_description_map: Optional[Mapping[str, str]] = None,
        missing_values: Optional[Sequence[str]] = None,
        force_update: bool = False
    ):
        self.current_tru.add_feature_metadata(
            feature_description_map=feature_description_map,
            missing_values=missing_values,
            force_update=force_update
        )

    def _get_pre_to_post_feature_map(
        self
    ) -> Optional[Mapping[str, Sequence[str]]]:
        return self.current_tru._get_pre_to_post_feature_map()

    def get_xs(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        extra_data: bool = False,
        system_data: bool = False
    ) -> pd.DataFrame:
        return self.current_tru.get_xs(
            start, stop, extra_data=extra_data, system_data=system_data
        )

    def get_ys(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        system_data: bool = False
    ) -> Union[pd.Series, pd.DataFrame]:
        return self.current_tru.get_ys(start, stop, system_data=system_data)

    def get_feature_influences(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        score_type: Optional[str] = None,
        system_data: bool = False,
        wait: bool = True
    ) -> pd.DataFrame:
        return self.current_tru.get_feature_influences(
            start,
            stop,
            score_type=score_type,
            system_data=system_data,
            wait=wait
        )

    def get_explainer(
        self,
        base_data_split: Optional[str] = None,
        comparison_data_splits: Optional[Sequence[str]] = None
    ) -> Explainer:
        return self.current_tru.get_explainer(
            base_data_split, comparison_data_splits
        )

    def add_segment_group(
        self, name: str, segment_definitions: Mapping[str, str]
    ) -> None:
        self.current_tru.add_segment_group(name, segment_definitions)

    def set_as_protected_segment(
        self, segment_group_name: str, segment_name: str
    ):
        self.current_tru.set_as_protected_segment(
            segment_group_name, segment_name
        )

    def delete_segment_group(self, name: str) -> None:
        self.current_tru.delete_segment_group(name)

    def get_segment_groups(self) -> Mapping[str, Mapping[str, str]]:
        return self.current_tru.get_segment_groups()

    def get_ingestion_client(self) -> IngestionClient:
        self._ensure_is_remote("Using ingestion client")
        return self.current_tru.get_ingestion_client()

    def add_credential(self, name, secret, identity=None) -> Credential:
        return self.get_ingestion_client().add_credential(
            name, secret, identity
        )

    def get_credential_metadata(self, name) -> Credential:
        md = self.get_ingestion_client().get_credential(name)
        return Credential(
            md["name"],
            md["id"],
            projects_with_access=md["projects_with_access"]
        )

    def delete_credential(self, name) -> None:
        return self.get_ingestion_client().delete_credential(name)

    def add_data_source(
        self,
        name: str,
        uri: str,
        credential:
        Credential = None,  # TODO(AB#3679) take cred name as the input
        **kwargs
    ) -> Table:
        workspace_validation_utils.ensure_valid_identifier(name)
        return self.get_ingestion_client().add_data_source(
            name, uri, credential, **kwargs
        )

    def get_data_source(self, name) -> Table:
        return self.get_ingestion_client().get_data_source(name)

    def get_data_sources(self) -> Sequence[str]:
        self._ensure_is_remote("Interacting with Remote Data Sources")
        return self.current_tru.get_data_sources()

    def delete_data_source(self, name: str):
        return self.current_tru.delete_data_source(name)

    def set_remote_environment(
        self, connection_string: str, authentication: TrueraAuthentication,
        **kwargs
    ) -> None:
        """Configure the remote environment and set the current environment to be remote.
        Args:
            connection_string: URL of the TruEra deployment. Defaults to None.
            authentication: Credentials to connect to TruEra deployment. Defaults to None.
        """
        if (connection_string is None) != (authentication is None):
            raise ValueError(
                "connection_string and authentication must both be supplied or neither!"
            )
        if connection_string.endswith("/p"):
            connection_string = connection_string[:-1]
            self.logger.info(
                f"Provided `connection_string` contains extra characters. Setting to: {connection_string}"
            )
        self.remote_tru = RemoteTrueraWorkspace(
            connection_string, authentication, self.logger.getEffectiveLevel(),
            **kwargs
        )
        self.set_environment("remote")

    def get_nn_user_configs(
        self
    ) -> Union[AttributionConfiguration, RNNUserInterfaceConfiguration]:
        configs = {}
        if self._sync_current_and_remote():
            configs["remote"] = self.remote_tru.get_nn_user_configs()
        if self.current_tru == self.local_tru:
            configs["local"] = self.local_tru.get_nn_user_configs()
        return configs

    def update_nn_user_config(
        self, config: Union[AttributionConfiguration,
                            RNNUserInterfaceConfiguration]
    ):
        if not isinstance(
            config, (AttributionConfiguration, RNNUserInterfaceConfiguration)
        ):
            raise ValueError(
                f"Unrecognized user config: {type(config)}. Current supported configs are AttributionConfig and UIConfig."
            )
        if self._sync_current_and_remote():
            self.remote_tru.update_nn_user_config(config)
        if self.current_tru == self.local_tru:
            self.local_tru.update_nn_user_config(config)

    def _sync_current_and_remote(self) -> bool:
        """
        Tries to get the current and remote contexts in sync.
        Returns a boolean indicating whether the sync is successful.
        If the current context is a local project and model, this will set the remote context to match.
        If the current project or model does not exist as a remote entity, the sync will not be successful.
        If the current context is already remote, then it implies a successful sync
        """
        if self.current_tru == self.remote_tru:
            return True
        project_name = self.local_tru._get_current_active_project_name()
        # Store context.
        context = self.get_context()
        context_model_name = context["model"]
        context_data_collection_name = context["data-collection"]
        context_data_split_name = context["data-split"]
        project_exists_remotely = self._entity_exists(
            project_name, self.remote_tru.get_projects
        ) if self.remote_tru is not None else False
        if project_exists_remotely:
            self.remote_tru.set_project(project_name)
        else:
            self.logger.debug(
                f"Remote project {project_name} does not exist. aborting attempted sync."
            )
            return False
        model_exists_remotely = self._entity_exists(
            context_model_name, self.remote_tru.get_models
        ) if self.remote_tru is not None else False
        if not model_exists_remotely:
            self.logger.debug(
                f"Remote model: {context_model_name} in project {project_name} does not exist. aborting attempted sync."
            )
            return False

        self.set_model(context_model_name)
        self.remote_tru.set_model(context_model_name)

        data_collection_exists_remotely = self._entity_exists(
            context_data_collection_name, self.remote_tru.get_data_collections
        ) if self.remote_tru is not None else False
        if data_collection_exists_remotely:
            self.set_data_collection(context_data_collection_name)
            self.remote_tru.set_data_collection(context_data_collection_name)
        data_split_exists_remotely = self._entity_exists(
            context_data_split_name, self.remote_tru.get_data_splits
        ) if self.remote_tru is not None else False
        if data_split_exists_remotely:
            self.set_data_split(context_data_split_name)
            self.remote_tru.set_data_split(context_data_split_name)
        return True

    def _add_remote_model_metadata(
        self, metadata: Union[RNNAttributionConfiguration,
                              RNNUserInterfaceConfiguration]
    ):
        # Add should only be done during ingestion.
        self.remote_tru.update_nn_user_config(metadata)

    def get_model_threshold(self) -> Optional[float]:
        return self.current_tru.get_model_threshold()

    def update_model_threshold(self, classification_threshold: float) -> None:
        self.current_tru.update_model_threshold(classification_threshold)

    def _validate_upload_project(
        self, virtual_models: bool, upload_strategy: str
    ):
        assert isinstance(virtual_models, bool)
        assert isinstance(upload_strategy, str)
        self.current_tru._ensure_project()
        if self.local_tru != self.current_tru:
            raise ValueError("Currently using a remote project, cannot upload!")
        if self.remote_tru is None:
            raise ValueError(
                "Set the remote environment using `set_remote_environment`."
            )
        if not self.get_num_default_influences():
            raise ValueError("`num_default_influences` of project must be > 0!")
        if upload_strategy not in self._VALID_UPLOAD_STRATEGIES:
            raise ValueError(
                f"`upload_strategy` must be in {self._VALID_UPLOAD_STRATEGIES}!"
            )

    def _validate_download_project(
        self, project_name: str, download_strategy: str
    ):
        project_exists_remotely = self._entity_exists(
            project_name, self.remote_tru.get_projects
        ) if self.remote_tru is not None else False
        if not project_exists_remotely:
            raise ValueError(
                f"Project {project_name} does not exist in remote!"
            )
        if download_strategy not in self._VALID_DOWNLOAD_STRATEGIES:
            raise ValueError(
                f"`download_strategy` must be in {self._VALID_DOWNLOAD_STRATEGIES}!"
            )

    def upload_project(
        self,
        virtual_models: bool = True,
        upload_strategy: str = "add_to_project",
        *,
        upload_error_qiis: bool = False,
        upload_partial_dependencies: bool = False
    ):
        """Upload a local project to a remote server.
        Args:
            virtual_models: Whether to upload any models as virtual (i.e. all prediction, influences, and partial dependencies computed locally). Defaults to True. 
                Predictions and influences for the default score type of the project will always be computed and uploaded. 
            upload_strategy: Strategy to deal with conflicts. Can be one of:
                1. "create_new_project": upload project only if it does not already exist on the remote server
                2. "overwrite_project": delete any existing project with the same name from the remote server, and upload new artifacts
                3. "add_to_project": for an existing project, upload artifacts (data collections, splits, and models) if and only if they do not exist on the remote server already
            upload_error_qiis: Whether to upload error QIIs (for stability analysis). Defaults to False.
            upload_partial_dependencies: Whether to upload partial dependencies for PDPs. Defaults to False.
        """
        # TODO(davidkurokawa): This whole thing needs to be atomic.
        self._validate_upload_project(virtual_models, upload_strategy)
        # Store context.
        previous_local_context = self.local_tru.get_context()
        local_context_score_type = self.local_tru._get_score_type(
        ) if previous_local_context["project"] else None
        local_context_input_type = self.local_tru._get_input_type(
        ) if previous_local_context["project"] else None
        local_context_num_default_influences = self.local_tru.get_num_default_influences(
        ) if previous_local_context["project"] else None
        local_context_num_samples = self.local_tru.get_num_internal_qii_samples(
        ) if previous_local_context["project"] else None

        # Store previous remote context.
        previous_remote_context = self.remote_tru.get_context()
        remote_context_score_type = self.remote_tru._get_score_type(
        ) if previous_remote_context["project"] else None
        remote_context_input_type = self.remote_tru._get_input_type(
        ) if previous_remote_context["project"] else None
        remote_context_num_default_influences = self.remote_tru.get_num_default_influences(
        ) if previous_remote_context["project"] else None
        remote_context_num_samples = self.remote_tru.get_num_internal_qii_samples(
        ) if previous_remote_context["project"] else None

        # Upload.
        project = self.local_tru._get_current_project_obj()
        project_name = self.local_tru._get_current_project_obj().name
        try:
            if project_name in self.remote_tru.get_projects():
                if upload_strategy == "create_new_project":
                    raise ValueError(
                        f"Project \"{project_name}\" exists on remote TruEra workspace! Set `upload_strategy` to \"add_to_project\" to attempt to merge or to \"overwrite_project\" to clobber."
                    )
                if upload_strategy == "overwrite_project":
                    self.remote_tru.delete_project(project_name)
            if project_name not in self.remote_tru.get_projects():
                self.remote_tru.add_project(
                    project_name,
                    score_type=project.score_type,
                    input_type=project.input_type,
                    num_default_influences=project.num_default_influences
                )
            self.remote_tru.set_project(project_name)
            self.remote_tru.set_num_default_influences(
                project.num_default_influences
            )
            self.remote_tru.set_num_internal_qii_samples(project.num_samples)
            self.remote_tru.set_influence_type(
                self.local_tru.get_influence_type()
            )
            self._upload_data_collections(project)
            self._upload_models(
                project, virtual_models, local_context_score_type,
                local_context_num_default_influences, upload_error_qiis,
                upload_partial_dependencies
            )
            self._upload_segment_groups(project)
        finally:
            # Regardless of whatever happens, restore context.
            self._set_project_context(
                self.local_tru, previous_local_context["project"],
                previous_local_context["model"],
                previous_local_context["data-collection"],
                previous_local_context["data-split"]
            )

            # Restore the remote_tru context as well
            self._set_project_context(
                self.remote_tru, previous_remote_context["project"],
                previous_remote_context["model"],
                previous_remote_context["data-collection"],
                previous_remote_context["data-split"]
            )

    def _upload_data_collections(self, project: Project):
        for data_collection_name, data_collection in project.data_collections.items(
        ):
            self.logger.info(
                f"Uploading data collection {data_collection_name}."
            )
            already_exists_warning_message = f"Data Collection {data_collection_name} exists in remote. Skipping upload."
            if data_collection_name not in self.remote_tru.get_data_collections(
            ):
                feature_transform = None
                if data_collection.feature_transform_type == FEATURE_TRANSFORM_TYPE_MODEL_FUNCTION:
                    feature_transform = True
                elif data_collection.feature_transform_type == FEATURE_TRANSFORM_TYPE_PRE_POST_DATA:
                    feature_transform = False
                self.remote_tru.add_data_collection(
                    data_collection_name, data_collection.feature_map,
                    feature_transform
                )
            else:
                self.logger.warning(already_exists_warning_message)
            self.local_tru.set_data_collection(data_collection_name)
            self.remote_tru.set_data_collection(data_collection_name)

            for data_split_name, data_split in data_collection.data_splits.items(
            ):
                if data_split_name in self.remote_tru.get_data_splits():
                    # TODO(davidkurokawa): Check that this split is the same as the one stored remotely.
                    self.logger.warning(
                        f"Data split \"{data_split_name}\" exists in remote. Skipping upload."
                    )
                else:
                    self.logger.info(f"Uploading data split {data_split_name}.")
                    if workspace_validation_utils.is_nontabular_project(
                        project.input_type
                    ):
                        self.local_tru.set_data_split(data_split_name)
                        explainer = self.get_explainer(data_split_name)
                        self.remote_tru.add_nn_data_split(
                            data_split_name=data_split_name,
                            truera_wrappers=data_split.truera_wrappers,
                            split_type=data_split.split_type,
                            pre_data=explainer.get_xs(system_data=True),
                            label_data=explainer.get_ys(system_data=True),
                            extra_data_df=data_split.extra_data_df,
                        )
                    else:
                        post_data = data_split.xs_post if data_collection.feature_transform_type == FEATURE_TRANSFORM_TYPE_PRE_POST_DATA else None
                        self.remote_tru.add_data_split(
                            data_split_name,
                            pre_data=data_split.xs_pre,
                            post_data=post_data,
                            label_data=data_split.ys,
                            extra_data_df=data_split.extra,
                            split_type=data_split.split_type
                        )

    def _upload_models(
        self, project: Project, virtual_models: bool, context_score_type: str,
        context_num_default_influences: int, upload_error_qiis: bool,
        upload_partial_dependencies: bool
    ):
        remote_models = self.remote_tru.get_models()

        for model_name, model in project.models.items():
            self.set_model(model_name)
            already_exists_warning_message = f"Model {model_name} exists in remote. Skipping upload."
            data_collection_name = self.local_tru._get_current_active_data_collection_name(
            )
            self.remote_tru.set_data_collection(data_collection_name)

            if model_name in remote_models:
                self.logger.warning(already_exists_warning_message)

            try:
                if workspace_validation_utils.is_tabular_project(
                    project.input_type
                ):
                    if not virtual_models:
                        self.logger.info(f"Uploading model {model_name}.")
                        self.remote_tru.add_python_model(
                            model_name,
                            model.model_obj,
                            transformer=model.transform_obj,
                            classification_threshold=model.
                            classification_threshold,
                            train_split_name=model.train_split_name,
                            train_parameters=model.train_parameters,
                            verify_model=False,
                            compute_predictions=False,
                            compute_feature_influences=False
                        )
                    else:
                        self.remote_tru.add_model(
                            model_name,
                            train_split_name=model.train_split_name,
                            train_parameters=model.train_parameters
                        )
                elif workspace_validation_utils.is_nontabular_project(
                    project.input_type
                ):
                    self.logger.info(f"Uploading NN model {model_name}.")
                    if workspace_validation_utils.is_rnn_project(
                        project.input_type
                    ):
                        attr_config = self.local_tru.rnn_attr_configs[
                            (project.name, model_name)]
                    elif workspace_validation_utils.is_nlp_project(
                        project.input_type
                    ):
                        attr_config = self.local_tru.nlp_attr_configs[
                            (project.name, model_name)]
                    self.remote_tru.add_nn_model(
                        model_name,
                        model.model_obj,
                        model.model_run_wrapper,
                        attr_config,
                        train_split_name=model.train_split_name,
                        train_parameters=model.train_parameters,
                        virtual_models=virtual_models
                    )
            except AlreadyExistsError as e:
                # TODO(davidkurokawa): Check that this model is the same as the one stored remotely.
                self.logger.warning(already_exists_warning_message)

            self.remote_tru.set_model(model_name)
            if workspace_validation_utils.is_tabular_project(
                project.input_type
            ):
                if model.classification_threshold is not None:
                    self.remote_tru.update_model_threshold(
                        model.classification_threshold
                    )

            for valid_score_type in self.list_valid_score_types():
                self.set_score_type(valid_score_type)
                self._upload_prediction_artifacts_from_local_tru()
            self.set_score_type(context_score_type)
            compute_feature_influences_if_not_exists = virtual_models or workspace_validation_utils.is_nontabular_project(
                project.input_type
            )
            self._upload_explanation_artifacts_from_local_tru(
                context_num_default_influences,
                compute_feature_influences_if_not_exists, upload_error_qiis,
                upload_partial_dependencies
            )
            if self.local_tru.get_nn_user_configs():
                self.remote_tru.set_model(model_name)
                self._add_remote_model_metadata(
                    self.local_tru.get_nn_user_configs()
                )

    def _upload_prediction_artifacts_from_local_tru(self):
        for data_split_name in self.get_data_splits():
            self.set_data_split(data_split_name)
            cache_location = create_temp_file_path(extension="csv")
            with ModelCacheUploader(
                self, CacheType.MODEL_PREDICTION_CACHE, cache_location
            ) as cache_uploader:
                ys_pred = self.get_explainer(data_split_name).get_ys_pred()
                if isinstance(ys_pred, pd.Series):
                    ys_pred.name = "Result"
                ys_pred.to_csv(cache_location, index=None)
                cache_uploader.upload(row_count=len(ys_pred))

    def _upload_explanation_artifacts_from_local_tru(
        self,
        num_default_influences: Optional[int] = None,
        compute_feature_influences_if_not_exists: bool = True,
        upload_error_qiis: bool = False,
        upload_partial_dependencies: bool = False
    ):
        input_type = self.local_tru._get_current_project_obj().input_type
        default_score_type = self.local_tru._get_score_type()
        for data_split_name in self.get_data_splits():
            curr_num_default_influences = num_default_influences
            self.set_data_split(data_split_name)
            explainer = self.local_tru.get_explainer(data_split_name)
            ys = explainer._base_data_split.ys
            all_computed_qiis = explainer.get_all_computed_feature_influences()
            background_data_split_name = explainer.get_influences_background_data_split_or_set_from_default(
            ).name
            self.remote_tru.set_influences_background_data_split(
                background_data_split_name
            )

            # compute influences for default score type if necessary
            if workspace_validation_utils.is_tabular_project(input_type):
                # don't perform this check for NN because split data is only loaded from cache when explanations are completed
                num_xs = explainer.get_xs().shape[0]
                if curr_num_default_influences > num_xs:
                    self.logger.info(
                        f"`num_default_influences` is greater than the number of available data points for split \"{self.local_tru._get_current_active_data_split_name()}\". Setting to this: {num_xs}"
                    )
                    curr_num_default_influences = num_xs
            score_types_to_upload = [default_score_type]
            if upload_error_qiis and ys is not None and len(ys) > 0:
                error_score_type = "mean_absolute_error_for_classification"
                if self._get_output_type() == "regression":
                    error_score_type = "mean_absolute_error_for_regression"
                score_types_to_upload.append(error_score_type)
            influence_type = self.local_tru.get_influence_type()
            self.logger.info(
                f"Influence algorithm for local project is: {influence_type}"
            )
            accepted_algorithm_types = [
                ExplanationAlgorithmType.TRUERA_QII
            ] if influence_type == "truera-qii" else [
                ExplanationAlgorithmType.KERNEL_SHAP,
                ExplanationAlgorithmType.TREE_SHAP_PATH_DEPENDENT,
                ExplanationAlgorithmType.TREE_SHAP_INTERVENTIONAL
            ]

            for score_type_to_upload in score_types_to_upload:
                precomputed = False
                for algorithm_type in accepted_algorithm_types:
                    if ExplainerQiiCacheKey(
                        score_type_to_upload, algorithm_type
                    ) in all_computed_qiis:
                        precomputed = True

                if not precomputed:
                    if compute_feature_influences_if_not_exists:
                        self.logger.warning(
                            f"Computing feature influences for model \"{self.local_tru._get_current_active_model_name()}\", data split \"{self.local_tru._get_current_active_data_split_name()}\", score type \"{self.local_tru._get_score_type()}\" before upload..."
                        )
                        try:
                            self.get_explainer(
                                data_split_name
                            ).get_feature_influences(
                                0,
                                curr_num_default_influences,
                                score_type=score_type_to_upload
                            )
                        except:
                            self.logger.warning(
                                f"Failed to compute influences for score_type {score_type_to_upload} ..."
                            )
                    else:
                        self.logger.warning(
                            f"Feature influences for data split \"{self.local_tru._get_current_active_data_split_name()}\", score type \"{self.local_tru._get_score_type()}\" are not computed."
                        )
                        continue

            # refetch all cached QIIs as we may have computed more
            all_computed_qiis = explainer.get_all_computed_feature_influences()

            # only upload default influences for NN projects
            if workspace_validation_utils.is_nontabular_project(input_type):
                qiis = all_computed_qiis.get(
                    ExplainerQiiCacheKey(
                        default_score_type,
                        ExplanationAlgorithmType.INTEGRATED_GRADIENTS
                    )
                )
                if qiis is None:
                    return
                cache_location = explainer.get_cache_dir_path()
                if not cache_location.endswith("/"):
                    cache_location = f"{cache_location}/"
                with ModelCacheUploader(
                    self, CacheType.EXPLANATION_CACHE, cache_location
                ) as cache_uploader:
                    cache_uploader.upload(
                        row_count=len(qiis),
                        background_data_split_name=background_data_split_name,
                        explanation_algorithm_type=ExplanationAlgorithmType.
                        INTEGRATED_GRADIENTS
                    )
            else:
                # upload all computed influences for tabular projects
                for exp_cache_key, qiis in all_computed_qiis.items():
                    cache_location = create_temp_file_path(extension="csv")
                    with ModelCacheUploader(
                        self, CacheType.EXPLANATION_CACHE, cache_location
                    ) as cache_uploader:
                        qiis.to_csv(cache_location, index=None)
                        cache_uploader.upload(
                            row_count=len(qiis),
                            score_type=exp_cache_key.score_type,
                            background_data_split_name=
                            background_data_split_name,
                            explanation_algorithm_type=exp_cache_key.algorithm
                        )

            # upload partial dependencies if necessary
            if upload_partial_dependencies:
                # TODO(this_pr): this only uploads for this score type
                pds_proto = explainer._get_partial_dependencies_as_proto()
                cache_location = create_temp_file_path(extension="txtproto")
                with ModelCacheUploader(
                    self, CacheType.PARTIAL_DEPENDENCE_PLOT_CACHE,
                    cache_location
                ) as cache_uploader:
                    with open(cache_location, "wb") as f:
                        f.write(pds_proto.SerializeToString())
                    cache_uploader.upload(
                        row_count=self.get_xs().shape[0],
                        score_type=self._get_score_type(),
                        background_data_split_name=data_split_name
                    )

    def _upload_segment_groups(self, project: Project) -> None:
        segment_groups = self.local_tru._get_current_project_obj(
        ).get_segment_groups()
        remote_segment_groups = self.remote_tru.get_segment_groups()
        for sg_name in segment_groups:
            if sg_name in remote_segment_groups:
                self.logger.warning(
                    f"Segment group {sg_name} already exists in remote! Skipped uploading this from local."
                )
                continue
            self.remote_tru.aiq_client.upload_segment_group(
                project_id=self.remote_tru.project.id,
                segment_group=segment_groups[sg_name]
            )

    def get_context(self) -> Mapping[str, str]:
        context = self.current_tru.get_context()
        context["environment"] = self.get_environment()
        return context

    def reset_context(self):
        self.current_tru.reset_context()

    def verify_nn_wrappers(
        self,
        *,
        clf,
        attr_config: Optional[AttributionConfiguration] = None,
        truera_wrappers: base.WrapperCollection,
    ):
        """Validates that all wrappers and methods are well formed.

        Args:
            clf (NNBackend.Model): The model object.
            truera_wrappers (Optional[base.WrapperCollection]): A collection of wrappers
        """
        model_run_wrapper = truera_wrappers.model_run_wrapper
        split_load_wrapper = truera_wrappers.split_load_wrapper
        model_load_wrapper = truera_wrappers.model_load_wrapper
        tokenizer_wrapper = truera_wrappers.tokenizer_wrapper if isinstance(
            truera_wrappers, nlp.WrapperCollection
        ) else None

        self.current_tru.verify_nn_wrappers(
            clf=clf,
            model_run_wrapper=model_run_wrapper,
            split_load_wrapper=split_load_wrapper,
            model_load_wrapper=model_load_wrapper,
            tokenizer_wrapper=tokenizer_wrapper,
            attr_config=attr_config
        )

    def _get_score_type(self):
        return self.current_tru._get_score_type()

    def _get_input_type(self):
        return self.current_tru._get_input_type()

    def _ensure_is_remote(self, operation):
        if not self.remote_tru or self.current_tru != self.remote_tru:
            raise ValueError(
                operation + " is only supported on remote projects."
                " To create a remote project, use `set_project` after `tru.set_environment(\"remote\")`"
            )

    def delete_project(self, project_name: Optional[str] = None):
        project_name = project_name or self._get_current_active_project_name()
        if not project_name:
            raise ValueError(
                "Must provide `project_name` or set the current project using `set_project`!"
            )
        self.current_tru.delete_project(project_name)

    def download_project(
        self, project_name: str, download_strategy: str = "add_to_project"
    ):
        """Download content of remote project to local.

        Args:
            project_name: Name of the project to be downloaded to local workspace.
            download_strategy: Strategy to deal with conflicts. Can be one of:
                1. "create_new_project": download project only if it does not already exist on local.
                2. "overwrite_project": delete any existing project with the same name from the local workspace, and download artifacts from remote.
                3. "add_to_project": for an existing project, download artifacts (data collections, splits, and models) if and only if they do not exist on the local workspce.
        """
        self._validate_download_project(project_name, download_strategy)
        # Store previous local context.
        previous_local_context = self.local_tru.get_context()
        local_context_score_type = self.local_tru._get_score_type(
        ) if previous_local_context["project"] else None
        local_context_input_type = self.local_tru._get_input_type(
        ) if previous_local_context["project"] else None
        local_context_num_default_influences = self.local_tru.get_num_default_influences(
        ) if previous_local_context["project"] else None
        local_context_num_samples = self.local_tru.get_num_internal_qii_samples(
        ) if previous_local_context["project"] else None

        # Store previous remote context.
        previous_remote_context = self.remote_tru.get_context()
        remote_context_score_type = self.remote_tru._get_score_type(
        ) if previous_remote_context["project"] else None
        remote_context_input_type = self.remote_tru._get_input_type(
        ) if previous_remote_context["project"] else None
        remote_context_num_default_influences = self.remote_tru.get_num_default_influences(
        ) if previous_remote_context["project"] else None
        remote_context_num_samples = self.remote_tru.get_num_internal_qii_samples(
        ) if previous_remote_context["project"] else None
        try:
            self.remote_tru.set_project(project_name)
            project_score_type_in_remote = self.remote_tru._get_score_type()
            project_input_type_in_remote = self.remote_tru._get_input_type()
            project_num_default_influences_in_remote = self.remote_tru.get_num_default_influences(
            )
            project_num_samples_for_influences_in_remote = self.remote_tru.get_num_internal_qii_samples(
            )
            if project_name in self.local_tru.get_projects():
                if download_strategy == "create_new_project":
                    raise ValueError(
                        f"Project \"{project_name}\" exists on local TruEra workspace! Set `download_strategy` to \"add_to_project\" to attempt to merge or to \"overwrite_project\" to remove existing local project with the same name."
                    )
                if download_strategy == "overwrite_project":
                    self.local_tru.delete_project(project_name)
                    self.local_tru.add_project(
                        project_name,
                        score_type=project_score_type_in_remote,
                        input_type=project_input_type_in_remote,
                        num_default_influences=
                        project_num_default_influences_in_remote
                    )
                else:
                    self.local_tru.set_project(project_name)
                    self.local_tru.set_score_type(project_score_type_in_remote)
                    self.local_tru.set_num_default_influences(
                        project_num_default_influences_in_remote
                    )
            else:
                self.local_tru.add_project(
                    project_name,
                    score_type=project_score_type_in_remote,
                    input_type=project_input_type_in_remote,
                    num_default_influences=
                    project_num_default_influences_in_remote
                )
            self.local_tru.set_num_internal_qii_samples(
                project_num_samples_for_influences_in_remote
            )
            self.local_tru.set_influence_type(
                self.remote_tru.get_influence_type()
            )

            self.logger.info(f"Download temp_dir: {self._data_tempdir.name}")
            data_splits_in_local_before_download = {}
            for data_collection_name in self.local_tru.get_data_collections():
                self.local_tru.set_data_collection(data_collection_name)
                data_splits_in_local_before_download[
                    data_collection_name] = self.local_tru.get_data_splits()
            data_collections_to_sync = self._download_data_collections()
            self._download_models(
                data_collections_to_sync, data_splits_in_local_before_download
            )
            self._download_segment_groups()
        finally:
            # Regardless of whatever happens, restore context.
            self._set_project_context(
                self.local_tru, previous_local_context["project"],
                previous_local_context["model"],
                previous_local_context["data-collection"],
                previous_local_context["data-split"]
            )

            # Restore the remote_tru context as well
            self._set_project_context(
                self.remote_tru,
                previous_remote_context["project"],
                previous_remote_context["model"],
                previous_remote_context["data-collection"],
                previous_remote_context["data-split"],
            )

    def _download_data_collections(self) -> Sequence[str]:
        """ Download all data_collections that are in current remote_tru project to local_tru. """
        # TODO(AB#5184): Update function to handle data with pre/post transformations
        project_name = self.remote_tru._get_current_active_project_name()
        project_input_type = self.remote_tru._get_input_type()
        data_collections_to_sync = []
        for data_collection in self.remote_tru._get_data_collections_with_metadata(
        ):
            data_collection_name = data_collection.data_collection_name
            self.remote_tru.set_data_collection(data_collection_name)
            remote_pre_to_post_feature_map = self.remote_tru._get_pre_to_post_feature_map(
            )
            self.logger.info(
                f"Syncing data collection \"{data_collection_name}\" to local."
            )
            if data_collection_name not in self.local_tru.get_data_collections(
            ):
                feature_transform = None
                if data_collection.feature_transform_type == FEATURE_TRANSFORM_TYPE_MODEL_FUNCTION:
                    feature_transform = True
                elif data_collection.feature_transform_type == FEATURE_TRANSFORM_TYPE_PRE_POST_DATA:
                    feature_transform = False

                self.local_tru.add_data_collection(
                    data_collection_name, remote_pre_to_post_feature_map,
                    feature_transform
                )
            else:
                self.local_tru.set_data_collection(data_collection_name)
                # check for feature map incompatibilities
                local_pre_to_post_feature_map = self.local_tru._get_pre_to_post_feature_map(
                )
                if local_pre_to_post_feature_map:
                    # local map exists and but does not match remote -> skip data collection
                    local_pre_to_post_ordered = {
                        pre: sorted(post)
                        for pre, post in local_pre_to_post_feature_map.items()
                    }
                    if remote_pre_to_post_feature_map:
                        remote_pre_to_post_ordered = {
                            pre: sorted(post) for pre, post in
                            remote_pre_to_post_feature_map.items()
                        }
                    if (
                        not remote_pre_to_post_feature_map
                    ) or local_pre_to_post_ordered != remote_pre_to_post_ordered:
                        self.logger.error(
                            "Local project has feature map that does not match the one on remote. Skipping download of this data collection."
                        )
                        continue
                    # local map exists and matches remote -> do nothing
                elif remote_pre_to_post_feature_map:
                    # local map does not exist, but remote map must be validated against existing splits
                    local_splits = self.local_tru.get_data_splits()
                    if local_splits:
                        split_obj = self.local_tru._get_current_project_obj(
                        ).data_collections[data_collection_name].data_splits[
                            local_splits[0]]
                        try:
                            workspace_validation_utils.validate_split_with_feature_map(
                                self.logger, remote_pre_to_post_feature_map,
                                split_obj.xs_pre, split_obj.xs_post
                            )
                        except Exception as e:
                            self.logger.error(
                                "Local project has existing data splits that do not match the remote feature map. Skipping download of this data collection."
                            )
                            continue

            data_collections_to_sync.append(data_collection_name)
            for data_split_name in self.remote_tru.get_data_splits():
                if data_split_name in self.local_tru.get_data_splits():
                    # TODO: check if the two datasplits with same name actually are the same?
                    self.logger.warning(
                        f"Data split \"{data_split_name}\" exists in local. Skipping."
                    )
                    continue
                self.remote_tru.set_data_split(data_split_name)
                self.logger.info(
                    f"Syncing data split \"{data_split_name}\" to local."
                )
                split_metadata = self.remote_tru.artifact_interaction_client.get_split_metadata(
                    project_name, data_collection_name, data_split_name
                )
                # TODO: any better way to convert split_type coming from MR to the ones accepted by cli_utils._map_split_type()?
                split_type = split_metadata["split_type"].split("_")[0].lower()

                if workspace_validation_utils.is_tabular_project(
                    project_input_type
                ):
                    try:
                        ys = self.remote_tru.get_ys()
                    except NotFoundError:
                        ys = None
                    post_data = self.remote_tru._get_xs_postprocessed(
                    ) if data_collection.feature_transform_type == FEATURE_TRANSFORM_TYPE_PRE_POST_DATA else None
                    self.local_tru.add_data_split(
                        data_split_name,
                        pre_data=self.remote_tru.get_xs(),
                        post_data=post_data,
                        label_data=ys,
                        split_type=split_type
                    )
                else:
                    try:
                        data_split_tempdir = self.remote_tru.download_nn_artifact(
                            ArtifactType.datasplit, self._data_tempdir.name
                        )
                        split_load_wrapper_path = os.path.join(
                            data_split_tempdir,
                            'truera_split_load_wrapper.pickle'
                        )
                        with open(split_load_wrapper_path, 'rb') as f:
                            split_load_wrapper = pickle.load(f)
                        split_load_wrapper.data_path = Path(data_split_tempdir)

                        truera_wrappers = base.WrapperCollection(
                            split_load_wrapper=split_load_wrapper,
                            model_load_wrapper=None,
                            model_run_wrapper=None,
                        )
                        self.local_tru.add_nn_data_split(
                            data_split_name=data_split_name,
                            truera_wrappers=truera_wrappers,
                            split_type=split_type
                        )
                    except Exception as e:
                        self.logger.error(
                            f"Failed to sync data split \"{data_split_name}\" in data_collection \"{data_collection_name}\" to local: {e}"
                        )
                        raise e
        return data_collections_to_sync

    def _download_models(
        self, data_collections_to_sync: Sequence[str],
        data_splits_in_local_before_download: Dict[str, Sequence[str]]
    ):
        """ Download all models that are in current remote_tru project to local_tru. """
        project_name = self.remote_tru._get_current_active_project_name()
        project_input_type = self.remote_tru._get_input_type()
        project_num_samples_for_influences = self.remote_tru.get_num_internal_qii_samples(
        )
        for model_name in self.remote_tru.get_models():
            if model_name in self.local_tru.get_models():
                # TODO: check if the two models with same name actually are the same?
                self.logger.warning(
                    f"Model \"{model_name}\" already exists in local. Skipping."
                )
                continue
            model_metadata = self.remote_tru.artifact_interaction_client.get_model_metadata(
                project_name, model_name
            )
            train_split_name = None
            if model_metadata["training_metadata"]["train_split_id"]:
                try:
                    train_split_name = self.remote_tru.artifact_interaction_client.get_split_metadata_by_id(
                        model_metadata["project_id"],
                        model_metadata["training_metadata"]["train_split_id"]
                    )["name"]
                except MetadataNotFoundException:
                    self.logger.warning(
                        f"Cannot resolve metadata for train split of model \"{model_name}\""
                    )

            train_parameters = None
            if "parameters" in model_metadata["training_metadata"]:
                train_parameters = model_metadata["training_metadata"][
                    "parameters"]
            data_collection_id = model_metadata["data_collection_id"]
            data_collection_name = None
            if data_collection_id:
                data_collection_name = self.remote_tru.artifact_interaction_client.get_data_collection_name(
                    self.remote_tru.project.id, data_collection_id
                )
            self.remote_tru.set_model(model_name)
            if data_collection_name not in data_collections_to_sync:
                self.logger.error(
                    f"Model \"{model_name}\" relies on data collection \"{data_collection_name}\" which could not be downloaded. Skipping download of model."
                )
                continue
            self.local_tru.set_data_collection(data_collection_name)

            is_nontabular_project = workspace_validation_utils.is_nontabular_project(
                project_input_type
            )
            if not is_nontabular_project:
                if not get_model_type_from_string(
                    model_metadata["model_type"]
                ) == ModelType.PYFUNC:
                    self.logger.info(
                        f"Skipping sync of model \"{model_name}\" as it is not a PyFunc model."
                    )
                    continue
                self.logger.info(f"Syncing model {model_name} to local.")
                model_tempdir = self.remote_tru.download_nn_artifact(
                    ArtifactType.model, self._data_tempdir.name
                )
                try:
                    model_details = yaml.safe_load(
                        open(os.path.join(model_tempdir, 'MLmodel'))
                    )
                    model_file = model_details['flavors']['python_function'][
                        'data']
                    model_loader = model_details['flavors']['python_function'][
                        'loader_module']
                    spec = importlib.util.spec_from_file_location(
                        "loader",
                        os.path.join(
                            model_tempdir, 'code', f"{model_loader}.py"
                        )
                    )
                    loader = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(loader)
                    model_obj = loader._load_pyfunc(
                        os.path.join(model_tempdir, model_file)
                    )
                    transform_obj = None
                    if hasattr(model_obj,
                               "transform") and callable(model_obj.transform):
                        transform_obj = model_obj.transform
                    if hasattr(model_obj, "get_model"):
                        model_obj = model_obj.get_model()
                    else:
                        model_obj = model_obj.predict
                    self.local_tru.add_python_model(
                        model_name,
                        model_obj,
                        transformer=transform_obj,
                        train_split_name=train_split_name,
                        train_parameters=train_parameters
                    )
                    for data_split_name in self.remote_tru.get_data_splits():
                        # Ignore explanation cache for splits that have conflict with local
                        if data_split_name in data_splits_in_local_before_download.get(
                            data_collection_name, []
                        ):
                            continue
                        try:
                            self.local_tru.set_data_split(data_split_name)
                            self.remote_tru.set_data_split(data_split_name)
                            remote_explainer = self.remote_tru.get_explainer(
                                data_split_name
                            )
                            qiis, algorithm_type = remote_explainer._get_all_feature_influences_and_algorithm_type(
                            )
                            if qiis is None or len(qiis) == 0:
                                self.logger.info(
                                    f"Computing feature influences in remote for model \"{model_name}\" and split \"{data_split_name}\""
                                )
                                qiis = remote_explainer.get_feature_influences()
                            self.local_tru.set_influences_background_data_split(
                                self.remote_tru.
                                get_influences_background_data_split()
                            )
                            local_explainer = self.local_tru.get_explainer(
                                data_split_name
                            )
                            local_explainer._add_feature_influences_from_cache(
                                data_split_name,
                                qiis.to_numpy(),
                                num_samples=project_num_samples_for_influences,
                                explanation_algorithm_type=algorithm_type
                            )
                        except Exception as e:
                            self.logger.error(
                                f"Failed to sync explanation cache for model \"{model_name}\" "\
                                f"and data_split \"{data_split_name}\" to local: {e}")
                except Exception as e:
                    self.logger.error(
                        f"Failed to sync model {model_name} to local: {e}"
                    )
                finally:
                    if os.path.exists(model_tempdir):
                        shutil.rmtree(model_tempdir)

            if is_nontabular_project:
                try:
                    model_type = get_model_type_from_string(
                        model_metadata["model_type"]
                    )
                    if model_type == ModelType.VIRTUAL:
                        model_load_wrapper = ModelType.VIRTUAL
                        model_run_wrapper = ModelType.VIRTUAL
                    elif model_type == ModelType.PYFUNC:
                        model_tempdir = self.remote_tru.download_nn_artifact(
                            ArtifactType.model, self._data_tempdir.name
                        )
                        model_load_wrapper_path = os.path.join(
                            model_tempdir, 'truera_model_load_wrapper.pickle'
                        )
                        with open(model_load_wrapper_path, 'rb') as f:
                            model_load_wrapper = pickle.load(f)
                        model_load_wrapper.model_path = model_tempdir
                        model_run_wrapper_path = os.path.join(
                            model_tempdir, 'truera_model_run_wrapper.pickle'
                        )
                        with open(model_run_wrapper_path, 'rb') as f:
                            model_run_wrapper = pickle.load(f)

                    if workspace_validation_utils.is_nontabular_project(
                        project_input_type
                    ):
                        if workspace_validation_utils.is_rnn_project(
                            project_input_type
                        ):
                            attr_config = RNNAttributionConfiguration.from_dict(
                                model_metadata["rnn_attribution_config"]
                            )
                        elif workspace_validation_utils.is_nlp_project(
                            project_input_type
                        ):
                            attr_config = NLPAttributionConfiguration.from_dict(
                                model_metadata["nlp_attribution_config"]
                            )

                        self.local_tru.add_nn_model(
                            model_name,
                            model_load_wrapper,
                            model_run_wrapper,
                            attr_config,
                            train_split_name=train_split_name,
                            train_parameters=train_parameters
                        )
                    for data_split_name in self.remote_tru.get_data_splits():
                        # Ignore explanation cache for splits that have conflict with local
                        if data_split_name in data_splits_in_local_before_download.get(
                            data_collection_name, []
                        ):
                            continue
                        try:
                            self.local_tru.set_data_split(data_split_name)
                            self.remote_tru.set_data_split(data_split_name)
                            #TODO(anoosha): make the flow same for RNN and NLP(move run_config to models in NLP)
                            cache_tempdir = self.remote_tru.download_nn_artifact(
                                ArtifactType.cache, self._data_tempdir.name
                            )

                            hash_bg = DEFAULT_NN_HASH_BG
                            if workspace_validation_utils.is_rnn_project(
                                project_input_type
                            ):
                                hash_bg = self.local_tru.get_explainer(
                                    data_split_name
                                )._attr_config.baseline_split
                            self.local_tru.get_explainer(
                                data_split_name
                            )._set_cache_dir(cache_tempdir, hash_bg)
                        except Exception as e:
                            self.logger.error(
                                f"Failed to sync cache for {project_input_type} model {model_name} and data_split {data_split_name}: {e}"
                            )

                except Exception as e:
                    self.logger.error(
                        f"Failed to sync NN model {model_name} to local: {e}"
                    )

    def _download_segment_groups(self):
        self.logger.info(f"Syncing segments groups from remote to local.")
        segment_groups = self.remote_tru.aiq_client.get_wrapped_segmentations(
            self.remote_tru.project.id, convert_model_ids_to_model_names=True
        ).response
        local_segment_groups = self.local_tru._get_current_project_obj(
        ).segment_groups
        for sg_name in segment_groups:
            if sg_name in local_segment_groups:
                self.logger.warning(
                    f"Segment group {sg_name} already exists in local! Skipped downloading this from remote."
                )
                continue
            local_segment_groups[sg_name] = segment_groups[sg_name]

    def _set_project_context(
        self, target_tru: BaseTrueraWorkspace, project_name: str,
        model_name: str, data_collection_name: str, data_split_name: str
    ):
        if project_name:
            target_tru.set_project(project_name)
            target_tru.set_model(model_name)
            target_tru.set_data_collection(data_collection_name)
            target_tru.set_data_split(data_split_name)
        else:
            target_tru.reset_context()

    def schedule_ingestion(self, raw_json: str, cron_schedule: str):
        return self.current_tru.schedule_ingestion(raw_json, cron_schedule)

    def get_scheduled_ingestion(self, workflow_id: str):
        return self.current_tru.get_scheduled_ingestion(workflow_id)

    def schedule_existing_data_split(
        self,
        split_name: str,
        cron_schedule: str,
        override_split_name: str = None,
        append: bool = True
    ):
        return self.current_tru.schedule_existing_data_split(
            split_name,
            cron_schedule,
            override_split_name=override_split_name,
            append=append
        )

    def serialize_split(
        self,
        split_name: str,
        override_split_name: str = None,
    ) -> str:
        return self.current_tru.serialize_split(split_name, override_split_name)

    def cancel_scheduled_ingestion(self, workflow_id: str) -> str:
        return self.current_tru.cancel_scheduled_ingestion(workflow_id)

    def list_scheduled_ingestions(
        self, last_key: str = None, limit: int = 50
    ) -> str:
        return self.current_tru.list_scheduled_ingestions(last_key, limit)

    def _get_feature_transform_type_for_data_collection(self):
        return self.current_tru._get_feature_transform_type_for_data_collection(
        )

    def list_monitoring_tables(self) -> str:
        return self.current_tru.list_monitoring_tables()
