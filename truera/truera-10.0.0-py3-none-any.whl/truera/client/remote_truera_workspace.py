import itertools
import logging
import os
import shutil
import sys
import tempfile
from typing import Any, Mapping, Optional, Sequence, Union
from urllib.parse import quote
from urllib.parse import urlparse
import uuid

import cloudpickle
from google.protobuf.json_format import MessageToJson
import numpy as np
import pandas as pd

from truera.client.base_truera_workspace import BaseTrueraWorkspace
from truera.client.base_truera_workspace import WorkspaceContextCleaner
# TODO: cli_utils needs to be refactored and this dependency should be removed
from truera.client.cli.cli_utils import _map_split_type
from truera.client.cli.cli_utils import format_remaining_list
from truera.client.cli.cli_utils import ModelType
from truera.client.client_utils import EXPLANATION_ALGORITHM_TYPE_TO_STR
from truera.client.client_utils import get_string_from_qoi_string
from truera.client.client_utils import validate_model_metadata
from truera.client.data_source_utils import best_effort_remove_temp_files
from truera.client.errors import MetadataNotFoundException
from truera.client.errors import NotFoundError
from truera.client.feature_client import FeatureClient
from truera.client.ingestion.sdk_model_packaging import CatBoostModelPackager
from truera.client.ingestion.sdk_model_packaging import LightGBMModelPackager
from truera.client.ingestion.sdk_model_packaging import ModelPredictPackager
from truera.client.ingestion.sdk_model_packaging import PySparkModelPackager
from truera.client.ingestion.sdk_model_packaging import SklearnModelPackager
from truera.client.ingestion.sdk_model_packaging import \
    SklearnPipelineModelPackager
from truera.client.ingestion.sdk_model_packaging import XgBoostModelPackager
from truera.client.ingestion_client import IngestionClient
from truera.client.ingestion_client import Table
from truera.client.intelligence.remote_data_profiler import RemoteDataProfiler
from truera.client.intelligence.remote_explainer import RemoteExplainer
from truera.client.intelligence.remote_tester import RemoteTester
from truera.client.model_preprocessing import PipDependencyParser
from truera.client.model_preprocessing import prepare_template_model_folder
from truera.client.model_preprocessing import verify_python_model_folder
from truera.client.nn import wrappers as base
from truera.client.nn.client_configs import AttributionConfiguration
from truera.client.nn.client_configs import NLPAttributionConfiguration
from truera.client.nn.client_configs import RNNAttributionConfiguration
from truera.client.nn.client_configs import RNNUserInterfaceConfiguration
from truera.client.nn.wrappers import MODEL_LOAD_WRAPPER_SAVE_NAME
from truera.client.nn.wrappers import MODEL_RUN_WRAPPER_SAVE_NAME
from truera.client.nn.wrappers import nlp
from truera.client.nn.wrappers import SPLIT_LOAD_WRAPPER_SAVE_NAME
from truera.client.public.communicator.http_communicator import \
    NotSupportedError
from truera.client.services.aiq_client import AiqClient
from truera.client.services.artifact_interaction_client import \
    ArtifactInteractionClient
from truera.client.services.artifact_interaction_client import DataCollection
from truera.client.services.artifact_interaction_client import \
    DataCollectionContainer
from truera.client.services.artifact_interaction_client import Model
from truera.client.services.artifact_interaction_client import \
    ModelCacheUploader
from truera.client.services.artifact_interaction_client import Project
from truera.client.services.artifact_repo_client_factory import get_ar_client
from truera.client.services.artifactrepo_client import ArtifactType
from truera.client.services.configuration_service_client import \
    ConfigurationServiceClient
from truera.client.services.data_service_client import DataServiceClient
from truera.client.services.monitoring_control_plane_client import \
    MonitoringControlPlaneClient
from truera.client.services.rbac_service_client import RbacServiceClient
from truera.client.services.scheduled_ingestion_client import \
    ScheduledIngestionClient
from truera.client.services.user_manager_service_client import \
    UserManagerServiceClient
from truera.client.truera_authentication import TrueraAuthentication
from truera.client.truera_workspace_utils import create_temp_file_path
from truera.client.truera_workspace_utils import validate_remote_url
from truera.client.util import workspace_validation_utils
from truera.client.util.data_split.pd_data_split_path_container import NAN_REP
from truera.client.util.data_split.pd_data_split_path_container import \
    PandasDataSplitPathContainer
from truera.client.util.validate_model_packaging_sdk import \
    validate_packaged_python_model
from truera.protobuf.aiq.config_pb2 import \
    AnalyticsConfig  # pylint: disable=no-name-in-module
from truera.protobuf.public.aiq.accuracy_pb2 import \
    AccuracyType  # pylint: disable=no-name-in-module
from truera.protobuf.public.metadata_message_types_pb2 import \
    CacheType  # pylint: disable=no-name-in-module
from truera.protobuf.public.metadata_message_types_pb2 import \
    FEATURE_TRANSFORM_TYPE_PRE_POST_DATA  # pylint: disable=no-name-in-module
from truera.protobuf.public.metadata_message_types_pb2 import \
    FeatureTransformationType  # pylint: disable=no-name-in-module
from truera.protobuf.public.qoi_pb2 import \
    ExplanationAlgorithmType  # pylint: disable=no-name-in-module
from truera.protobuf.public.util import split_mode_pb2 as sm_pb
from truera.public.feature_influence_constants import \
    get_output_type_from_score_type
import truera.public.feature_influence_constants as fi_constants
from truera.utils.package_requirement_utils import get_python_version_str
from truera.utils.pyspark_util import is_supported_pyspark_tree_model
from truera.utils.truera_status import TruEraInternalError

PREDICTION_COLUMN_NAME = "Result"


class RemoteTrueraWorkspace(BaseTrueraWorkspace):

    def __init__(
        self,
        connection_string: str,
        authentication: TrueraAuthentication,
        log_level: int = logging.INFO,
        **kwargs
    ) -> None:
        """Construct a new remote TrueraWorkspace.
        Args:
            connection_string: URL of the Truera deployment.
            authentication: Credentials to connect to Truera deployment.
            log_level: Log level (defaults to `logging.INFO`).
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        validate_remote_url(connection_string)
        connection_string = connection_string.rstrip("/")
        ignore_version_mismatch = kwargs.get("ignore_version_mismatch", False)
        verify_cert = kwargs.get("verify_cert", True)
        authentication.set_connection_string(connection_string)
        self.ar_client = get_ar_client(
            connection_string=connection_string,
            auth_details=authentication.get_auth_details(),
            logger=self.logger,
            use_http=True,
            ignore_version_mismatch=ignore_version_mismatch,
            verify_cert=verify_cert
        )
        self.data_service_client = DataServiceClient.create(
            connection_string=connection_string,
            logger=self.logger,
            auth_details=authentication.get_auth_details(),
            use_http=True,
            verify_cert=verify_cert
        )
        self.user_manager_client = UserManagerServiceClient.create(
            connection_string=connection_string,
            logger=self.logger,
            auth_details=authentication.get_auth_details(),
            use_http=True,
            verify_cert=verify_cert
        )
        self.rbac_service_client = RbacServiceClient.create(
            connection_string=connection_string,
            logger=self.logger,
            auth_details=authentication.get_auth_details(),
            use_http=True,
            verify_cert=verify_cert
        )
        self.scheduled_ingestion_client = ScheduledIngestionClient.create(
            connection_string=connection_string,
            data_service_client=self.data_service_client,
            logger=self.logger,
            auth_details=authentication.get_auth_details(),
            use_http=True,
            verify_cert=verify_cert
        )
        self.artifact_interaction_client = ArtifactInteractionClient(
            self.ar_client, self.data_service_client, self.logger
        )
        self.aiq_client = AiqClient(
            connection_string=connection_string,
            auth_details=authentication.get_auth_details(),
            use_http=True,
            verify_cert=verify_cert,
            artifact_interaction_client=self.artifact_interaction_client
        )
        self.cs_client = ConfigurationServiceClient(
            connection_string=connection_string,
            auth_details=authentication.get_auth_details(),
            use_http=True,
            verify_cert=verify_cert
        )
        self.feature_client = FeatureClient(self.ar_client, self.logger)
        self.monitoring_control_plane_client = MonitoringControlPlaneClient.create(
            connection_string=connection_string,
            logger=self.logger,
            auth_details=authentication.get_auth_details(),
            use_http=True,
            verify_cert=verify_cert
        )
        self.data_profiler = RemoteDataProfiler(
            self, self.artifact_interaction_client, self.cs_client,
            connection_string, authentication.get_auth_details(), verify_cert
        )
        self.tester = RemoteTester(
            self, self.artifact_interaction_client, connection_string,
            authentication.get_auth_details(), verify_cert
        )
        self.project: Optional[Project] = None
        self.model: Optional[Model] = None
        self.data_collection: Optional[DataCollectionContainer] = None
        self.data_split_name: str = None
        self.connection_string = connection_string
        self.authentication = authentication

    def get_projects(self) -> Sequence[str]:
        return self.artifact_interaction_client.get_all_projects()

    def _get_project_settings(self,
                              project: str) -> Mapping[str, Union[str, int]]:
        project_metadata = self._fetch_and_parse_project_metadata(project)
        project_num_default_influences = self.cs_client.get_num_default_influences(
            project_metadata['id']
        )
        return {
            "input_type": project_metadata['input_type'],
            "num_default_influences": project_num_default_influences,
            "score_type": project_metadata['score_type']
        }

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
        if self._get_current_active_project_name():
            self.set_data_collection(None)
            self.set_model(None)
        self.project = self.artifact_interaction_client.create_project(
            project, score_type, input_data_format=input_type
        )
        if num_default_influences:
            self.set_num_default_influences(num_default_influences)

    def set_project(self, project: str):
        if project == self._get_current_active_project_name():
            return
        if project:
            self._validate_set_project(project)
        if self._get_current_active_project_name():
            self.set_data_collection(None)
            self.set_model(None)
        project_metadata = self._fetch_and_parse_project_metadata(project)
        self.project = Project(
            project_name=project,
            artifact_interaction_client=self.artifact_interaction_client,
            project_id=project_metadata["id"]
        )

    def set_score_type(self, score_type: str):
        self._ensure_project()
        self._validate_score_type(score_type)
        self.cs_client.update_metric_configuration(
            self.project.id, score_type=score_type
        )

    def set_influence_type(self, algorithm: str):
        if algorithm == "truera-qii":
            algorithm_enum = AnalyticsConfig.AlgorithmType.TRUERA_QII
        elif algorithm == "integrated-gradients":
            algorithm_enum = AnalyticsConfig.AlgorithmType.INTEGRATED_GRADIENTS
        else:
            algorithm_enum = AnalyticsConfig.AlgorithmType.SHAP
        return self.cs_client.update_analytics_configuration(
            project_id=self.project.id, influence_algorithm_type=algorithm_enum
        )

    def get_influence_type(self) -> str:
        return self.cs_client.get_influence_algorithm_type(self.project.id)

    def set_maximum_model_runner_failure_rate(
        self, maximum_model_runner_failure_rate: float
    ):
        self._ensure_project()
        if maximum_model_runner_failure_rate < 0 or maximum_model_runner_failure_rate >= 1:
            raise ValueError(
                "`maximum_model_runner_failure_rate` must be in [0, 1)!"
            )
        self.cs_client.update_metric_configuration(
            self.project.id,
            maximum_model_runner_failure_rate=maximum_model_runner_failure_rate
        )

    def get_maximum_model_runner_failure_rate(self) -> float:
        self._ensure_project()
        return self.cs_client.get_metric_configuration(
            self.project.id
        ).metric_configuration.maximum_model_runner_failure_rate

    def get_num_default_influences(self) -> int:
        self._ensure_project()
        return self.cs_client.get_num_default_influences(self.project.id)

    def set_num_default_influences(self, num_default_influences: int) -> None:
        self._validate_num_default_influences(num_default_influences)
        self.cs_client.update_analytics_configuration(
            self.project.id, num_default_influences=num_default_influences
        )

    def list_performance_metrics(self) -> Sequence[str]:
        # TODO(DC-74): This isn't correct!
        return self.aiq_client.list_performance_metrics()

    def get_default_performance_metrics(self) -> Sequence[str]:
        return [
            AccuracyType.Type.Name(curr) for curr in
            self.cs_client.get_default_performance_metrics(self.project.id)
        ]

    def set_default_performance_metrics(
        self, performance_metrics: Sequence[str]
    ):
        valid_performance_metrics = self.list_performance_metrics()
        performance_metrics_enumified = workspace_validation_utils.validate_performance_metrics(
            performance_metrics, valid_performance_metrics
        )
        self.cs_client.update_metric_configuration(
            self.project.id, performance_metrics=performance_metrics_enumified
        )

    def get_num_internal_qii_samples(self) -> int:
        self._ensure_project()
        return self.cs_client.get_num_internal_qii_samples(self.project.id)

    def set_num_internal_qii_samples(self, num_samples: int) -> None:
        self._validate_num_samples_for_influences(num_samples)
        self.cs_client.update_analytics_configuration(
            self.project.id, num_internal_qii_samples=num_samples
        )

    def get_models(self, project_name: str = None) -> Sequence[str]:
        if not project_name:
            self._ensure_project()
            return self.artifact_interaction_client.get_all_models_in_project(
                self.project.id
            )
        project_metadata = self._fetch_and_parse_project_metadata(project_name)
        if project_metadata:
            return self.artifact_interaction_client.get_all_models_in_project(
                project_metadata['id']
            )
        return []

    def set_model(self, model_name: str):
        if model_name == self._get_current_active_model_name():
            return
        if not model_name:
            self.model = None
            return
        self._ensure_project()
        if model_name not in self.get_models():
            raise ValueError(
                f"Could not find model {model_name} in project {self.project.name}"
            )
        model_meta = self.artifact_interaction_client.get_model_metadata(
            self.project.name, model_name
        )
        data_collection_id = model_meta["data_collection_id"]
        data_collection_name = None
        if data_collection_id:
            data_collection_name = self.artifact_interaction_client.get_data_collection_name(
                self.project.id, data_collection_id
            )
        self._print_model_associated_with_different_data_collection_message(
            self.logger,
            model_name,
            data_collection_name,
            self._get_current_active_data_collection_name(),
            is_remote=True
        )
        self.set_data_collection(data_collection_name)
        self._print_set_model_context(self.logger, model_name, is_remote=True)
        self.model = self.project.get_model(model_name, data_collection_name)

    def delete_model(
        self, model_name: Optional[str] = None, *, recursive: bool = False
    ):
        project_name = self._ensure_project()
        if not model_name:
            self._ensure_model()
        model_name = model_name if model_name else self.model.model_name
        with WorkspaceContextCleaner(self, delete_model=True):
            success, remaining_items = self.artifact_interaction_client.delete_model(
                project_name, model_name, recursive=recursive
            )
            if not success:
                if remaining_items:
                    raise ValueError(
                        "Deletion of model failed as there are model tests that are using the model as a reference. "
                        "Please delete these model tests or pass recursive=True. Affected test ids: {}"
                        .format(remaining_items)
                    )
                raise TruEraInternalError(
                    "Delete failed. Expected model deletion to succeed as there are no affected model tests."
                )

    def get_data_collections(self, project_name: str = None) -> Sequence[str]:
        if not project_name:
            self._ensure_project()
            return self.artifact_interaction_client.get_all_data_collections_in_project(
                self.project.id
            )
        project_metadata = self.artifact_interaction_client.get_project_metadata(
            project_name
        )
        return self.artifact_interaction_client.get_all_data_collections_in_project(
            project_metadata['id']
        )

    def _get_data_collections_with_metadata(self) -> Sequence[DataCollection]:
        self._ensure_project()
        return self.artifact_interaction_client.get_all_data_collections_with_transform_type_in_project(
            self.project.id
        )

    def get_data_splits(self) -> Sequence[str]:
        self._ensure_project()
        self._ensure_data_collection()
        return self.artifact_interaction_client.get_all_datasplits_in_data_collection(
            self._get_current_active_project_name(),
            self._get_current_active_data_collection_name()
        )

    def get_data_sources(self, project_name: str = None) -> Sequence[str]:

        def rowset_has_name(rowset_metadata):
            return "rowset" in rowset_metadata and "root_data" in rowset_metadata[
                "rowset"] and len(
                    rowset_metadata["rowset"]["root_data"]
                ) > 0 and "name" in rowset_metadata["rowset"]["root_data"][0]

        if not project_name:
            self._ensure_project()
            return [
                rowset_metadata["rowset"]["root_data"][0]["name"]
                for rowset_metadata in self.artifact_interaction_client.
                get_all_data_sources_in_project(self.project.id)
                if rowset_has_name(rowset_metadata)
            ]
        project_metadata = self.artifact_interaction_client.get_project_metadata(
            project_name
        )
        return [
            rowset_metadata["rowset"]["root_data"][0]["name"]
            for rowset_metadata in self.artifact_interaction_client.
            get_all_data_sources_in_project(project_metadata["id"])
            if rowset_has_name(rowset_metadata)
        ]

    def delete_data_source(self, name: str):
        self._ensure_project()
        return self.artifact_interaction_client.delete_data_source(
            self.project.id, name
        )

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
        project_name = self._get_current_active_project_name()
        self.set_data_split(None)
        self.set_model(None)

        preprocessed_cols = None
        postprocessed_cols = None
        if pre_to_post_feature_map:
            preprocessed_cols = list(pre_to_post_feature_map.keys())
            postprocessed_cols = list(
                itertools.chain.from_iterable(pre_to_post_feature_map.values())
            )
        data_collection = self.project.create_data_collection(
            data_collection_name,
            workspace_validation_utils.
            get_feature_transform_type_from_feature_map(
                pre_to_post_feature_map, provide_transform_with_model
            )
        )
        data_collection_id = data_collection.upload(
            self.artifact_interaction_client, project_name
        )
        self.feature_client.upload_feature_description_and_group_metadata(
            project_name,
            data_collection_name,
            pre_features=preprocessed_cols,
            post_features=postprocessed_cols,
            pre_to_post_feature_map=pre_to_post_feature_map,
            only_update_metadata=False
        )
        self.data_collection = DataCollectionContainer(
            data_collection_name, data_collection_id
        )

    def _validate_set_data_collection(self, data_collection_name: str) -> str:
        # Returns ID of data collection
        workspace_validation_utils.ensure_valid_identifier(data_collection_name)
        self._ensure_project()
        data_collection_name_to_ids = {
            pair["name"]: pair["id"]
            for pair in self.artifact_interaction_client.
            get_all_data_collections_with_ids_in_project(self.project.id
                                                        )["name_id_pairs"]
        }
        if data_collection_name not in data_collection_name_to_ids:
            raise ValueError(
                f"No such data collection \"{data_collection_name}\"! See `add_data_collection` to add it."
            )
        return data_collection_name_to_ids[data_collection_name]

    def set_data_collection(self, data_collection_name: str):
        current_data_collection_name = self._get_current_active_data_collection_name(
        )
        if data_collection_name == current_data_collection_name:
            return
        self.set_data_split(None)
        self.set_model(None)
        if not data_collection_name:
            self.data_collection = None
            return
        data_collection_id = self._validate_set_data_collection(
            data_collection_name
        )
        self.data_collection = DataCollectionContainer(
            name=data_collection_name, id=data_collection_id
        )
        self._print_change_data_collection_message(
            self.logger,
            current_data_collection_name,
            data_collection_name,
            is_remote=True
        )

    def set_data_split(self, data_split_name: str):
        if not data_split_name:
            self.data_split_name = None
            return
        self._ensure_project()
        self._ensure_data_collection()
        if data_split_name not in self.get_data_splits():
            raise ValueError(f"No such data split \"{data_split_name}\"!")
        self.data_split_name = data_split_name

    def add_nn_model(
        self,
        model_name: str,
        model_load_wrapper: base.Wrappers.ModelLoadWrapper,
        model_run_wrapper: base.Wrappers.ModelRunWrapper,
        attribution_config: AttributionConfiguration,
        train_split_name: Optional[str] = None,
        train_parameters: Optional[Mapping[str, Any]] = None,
        virtual_models: bool = False,
        **kwargs
    ) -> Model:
        self._ensure_project()
        data_collection_name = self._ensure_data_collection()
        validate_model_metadata(
            train_split_name=train_split_name,
            existing_split_names=self.get_data_splits(),
            train_parameters=train_parameters,
            logger=self.logger
        )

        wrapper_tmp_dir = tempfile.TemporaryDirectory()
        wrapper_tmp_path = wrapper_tmp_dir.name
        model_dir = None
        try:
            if not virtual_models:
                if not isinstance(
                    model_load_wrapper, base.Wrappers.ModelLoadWrapper
                ):
                    raise ValueError(
                        f"Uploading an NN model to remote server is only supported for `ModelLoadWrapper`s. Provided `model_load_wrapper` is of type {type(model_load_wrapper)}. If this model is not intended to be loaded, try uploading with `virtual_models=True`"
                    )
                model_dir = model_load_wrapper.get_model_path()
                try:
                    self._save_object_file(
                        wrapper_tmp_path, MODEL_LOAD_WRAPPER_SAVE_NAME,
                        model_load_wrapper
                    )
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    raise ValueError(
                        f'Failed to upload model object. Make sure the model can be loaded from file, or try uploading with `virtual_models=True`'
                    )

            self._save_object_file(
                wrapper_tmp_path, MODEL_RUN_WRAPPER_SAVE_NAME, model_run_wrapper
            )

            model_dir = model_dir or wrapper_tmp_path

            if virtual_models:
                model_type = ModelType.Virtual
            else:
                model_type = ModelType.PyFunc
            #TODO: If MLFlow is the right implementation, enable an equivalent of  model_preprocessing.prepare_python_model_folder for nn
            # This would use backend and pip dependencies paraneters passed into this function
            # Tracked in AB#3556
            model = self.project.create_model(
                model_name=model_name,
                model_type=model_type,
                model_output_type=self._get_output_type(),
                local_model_path=model_dir,
                data_collection_name=data_collection_name,
                extra_data_path=wrapper_tmp_path,
                train_split_name=train_split_name,
                train_parameters=train_parameters
            )
            model.upload(self.artifact_interaction_client)
            self.model = model
            self.update_nn_user_config(attribution_config)
            self._print_add_model_message(
                self.logger, model_name, data_collection_name, is_remote=True
            )
            print(
                f"Model uploaded to: {self.connection_string}/p/{quote(self.project.name)}/m/{quote(model.model_name)}/"
            )

        finally:
            try:
                wrapper_tmp_dir.cleanup()
            except:
                pass

    def add_model(
        self,
        model_name: str,
        train_split_name: Optional[str] = None,
        train_parameters: Optional[Mapping[str, Any]] = None
    ):
        self._ensure_project()
        self._ensure_data_collection()
        validate_model_metadata(
            train_split_name=train_split_name,
            existing_split_names=self.get_data_splits(),
            train_parameters=train_parameters,
            logger=self.logger
        )
        model = self.project.create_model(
            model_name=model_name,
            model_type=ModelType.Virtual,
            model_output_type=self._get_output_type(),
            local_model_path="",
            data_collection_name=self._get_current_active_data_collection_name(
            ),
            train_split_name=train_split_name,
            train_parameters=train_parameters
        )
        model.upload(self.artifact_interaction_client)
        self.set_model(model_name)

    def _trigger_computations_post_ingestion(
        self,
        model_name: str,
        compute_predictions: bool = True,
        compute_feature_influences: bool = False,
        compute_for_all_splits: bool = False
    ):
        if not (compute_predictions or compute_feature_influences):
            return
        with WorkspaceContextCleaner(self):
            self.set_model(model_name)
            all_data_splits = self.get_data_splits()
            if not all_data_splits:
                return  # nothing to trigger

            try:
                if compute_for_all_splits:
                    splits_to_trigger = all_data_splits
                else:
                    # Set background data split, and switch workspace context to use this split
                    self.get_explainer(
                    )._ensure_influences_background_data_split_is_set()
                    splits_to_trigger = [
                        self.get_influences_background_data_split()
                    ]

                for split_name in splits_to_trigger:
                    # Trigger
                    explainer = self.get_explainer(base_data_split=split_name)
                    if compute_predictions:
                        self.logger.info(
                            f"Triggering computations for model predictions on split {split_name}."
                        )
                        explainer.get_ys_pred(
                            include_all_points=True, wait=False
                        )
                    if compute_feature_influences:
                        self.logger.info(
                            f"Triggering computations for model feature influences on split {split_name}."
                        )
                        explainer.get_feature_influences(wait=False)
            except Exception as e:
                self.logger.warning(
                    f"Failed to autotrigger computations. See error: {str(e)}"
                )

    def _validate_add_model_remote(
        self,
        model_name: str,
        train_split_name: Optional[str] = None,
        train_parameters: Optional[Mapping[str, Any]] = None,
    ):
        self._validate_add_model(model_name)
        validate_model_metadata(
            train_split_name=train_split_name,
            existing_split_names=self.get_data_splits(),
            train_parameters=train_parameters,
            logger=self.logger
        )

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
        compute_for_all_splits: bool = False
    ):
        self._validate_add_model_remote(
            model_name,
            train_split_name=train_split_name,
            train_parameters=train_parameters
        )
        self._add_packaged_python_model(
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

    def _add_packaged_python_model(
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
        compute_for_all_splits: bool = False
    ):
        if data_collection_name:
            if data_collection_name not in self.get_data_collections():
                raise ValueError(
                    f"The data_collection: {data_collection_name} does not exist in the current project {self.project.name}"
                )
        else:
            data_collection_name = self._get_current_active_data_collection_name(
            )
        if verify_model:
            self.verify_packaged_model(
                model_dir
            )  # full validation using split data
        else:
            verify_python_model_folder(
                model_dir, logger=self.logger
            )  # basic checking on folder structure
        model = self.project.create_model(
            model_name=model_name,
            model_type=ModelType.PyFunc,
            model_output_type=self._get_output_type(),
            local_model_path=model_dir,
            data_collection_name=data_collection_name,
            train_split_name=train_split_name,
            train_parameters=train_parameters
        )
        model.upload(self.artifact_interaction_client)
        self.model = model
        self._print_add_model_message(
            self.logger, model_name, data_collection_name, is_remote=True
        )
        print(
            f"Model uploaded to: {self.connection_string}/p/{quote(self.project.name)}/m/{quote(model.model_name)}/"
        )
        self._trigger_computations_post_ingestion(
            model_name,
            compute_predictions=compute_predictions,
            compute_feature_influences=compute_feature_influences,
            compute_for_all_splits=compute_for_all_splits
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
        if model_code_files is None:
            model_code_files = []
        if model_obj is not None:
            self.logger.debug("Packaging Python model from model object.")
            feature_transform_type = self._get_feature_transform_type_for_data_collection(
            )
            self.prepare_python_model_folder_from_model_object(
                output_dir,
                model_obj,
                None,
                feature_transform_type=feature_transform_type,
                additional_pip_dependencies=additional_pip_dependencies,
                additional_modules=additional_modules,
                **kwargs
            )
        else:
            prepare_template_model_folder(
                output_dir,
                self._get_output_type(),
                model_path,
                model_code_files,
                pip_dependencies=additional_pip_dependencies,
                python_version=kwargs.get("python_version", None)
            )
        self.logger.info(
            f"Successfully generated template model package at path '{output_dir}'"
        )

    def verify_packaged_model(self, model_path: str):
        self._ensure_project()
        data_collection_name = self._ensure_data_collection()
        dc_metadata = self.project.get_data_collection_metadata(
            data_collection_name, as_json=False
        )
        available_data_splits = self.get_data_splits()
        test_data = None if not available_data_splits else self._get_xs_for_split(
            available_data_splits[0], 0, 1, get_post_processed_data=True
        )
        validate_packaged_python_model(
            self.logger,
            model_path,
            test_data=test_data,
            is_regression_model=self._get_output_type() == "regression",
            feature_transform_type=dc_metadata.feature_transform_type
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
        self._validate_additional_modules(additional_modules)
        self._validate_add_model_remote(
            model_name,
            train_split_name=train_split_name,
            train_parameters=train_parameters
        )
        feature_transform_type = self._get_feature_transform_type_for_data_collection(
        )
        score_type = self._get_score_type()
        classification_threshold = workspace_validation_utils.validate_model_threshold(
            classification_threshold, score_type
        )
        temp_staging_dir = tempfile.mkdtemp()
        shutil.rmtree(temp_staging_dir, ignore_errors=True)
        try:
            self.prepare_python_model_folder_from_model_object(
                temp_staging_dir,
                model,
                transformer,
                feature_transform_type=feature_transform_type,
                additional_pip_dependencies=additional_pip_dependencies,
                additional_modules=additional_modules,
                **kwargs
            )
            self._add_packaged_python_model(
                model_name,
                temp_staging_dir,
                train_split_name=train_split_name,
                train_parameters=train_parameters,
                verify_model=verify_model,
                compute_predictions=compute_predictions,
                compute_feature_influences=compute_feature_influences,
                compute_for_all_splits=compute_for_all_splits
            )
            if score_type in fi_constants.VALID_SCORE_TYPES_FOR_CLASSIFICATION:
                self.update_model_threshold(classification_threshold)
        finally:
            shutil.rmtree(temp_staging_dir, ignore_errors=True)

    def delete_data_split(
        self,
        data_split_name: Optional[str] = None,
        *,
        recursive: bool = False
    ):
        project_name = self._ensure_project()
        data_collection_name = self._ensure_data_collection()
        if not data_split_name:
            data_split_name = self._ensure_data_split()
        with WorkspaceContextCleaner(self, delete_data_split=True):
            success, remaining_items = self.artifact_interaction_client.delete_data_split(
                project_name,
                data_collection_name,
                data_split_name,
                recursive=recursive
            )
            if not success:
                if remaining_items:
                    raise ValueError(
                        "Deletion of data split failed as there are model tests that are using the data split. "
                        "Please delete these model tests or pass recursive=True. Affected test ids: {}"
                        .format(remaining_items)
                    )
                raise TruEraInternalError(
                    "Delete failed. Expected split deletion to succeed as there are no affected model tests."
                )

    def delete_data_collection(
        self,
        data_collection_name: Optional[str] = None,
        *,
        recursive: bool = False
    ):
        project_name = self._ensure_project()
        if not data_collection_name:
            data_collection_name = self._ensure_data_collection()
        with WorkspaceContextCleaner(self, delete_data_collection=True):
            success, remaining_items = self.artifact_interaction_client.delete_data_collection(
                project_name, data_collection_name, recursive=recursive
            )
            if not success:
                if remaining_items:
                    raise ValueError(
                        "Deletion of data collection failed as there are entities contained in the data collection. "
                        "Please delete these entites or pass recursive=True. Remaining entities:\n {}"
                        .format(format_remaining_list(remaining_items))
                    )
                raise TruEraInternalError(
                    "Delete failed. Expected data collection deletion to succeed as no remaining items returned."
                )

    def _use_data_layer_for_split_ingestion(
        self, pre_data: Union[str, pd.DataFrame], label_col_name: str,
        id_col_name: str
    ) -> bool:
        if not id_col_name:
            return False
        if not self.get_client_setting_value(
            "workspace_use_tables_for_split_ingestion"
        ):
            if id_col_name:
                raise ValueError(
                    "To ingest splits with an ID column, you must activate split ingestion from tables by default. Run `tru.activate_client_setting('workspace_use_tables_for_split_ingestion')`"
                )
            return False

        # We don't want to use this if already given a table.
        if isinstance(pre_data, Table):
            return False

        # We don't want to use this if data is remote anyway.
        if isinstance(pre_data, str):
            parsed = urlparse(pre_data)
            scheme = parsed.scheme.lower()
            if scheme and scheme != "file":
                return False

        # For now, we won't pull the label column out if just that is provided.
        if label_col_name:
            return False

        return True

    def _infer_background_split(self, background_split_name):
        background_split_id = None
        if not background_split_name:
            background_split_id = self.cs_client.get_base_split(
                self.project.id,
                self.data_collection.id,
                infer_base_split_if_not_set=True
            )
            background_split_name = self.artifact_interaction_client.get_split_metadata_by_id(
                self.project.id, background_split_id
            )["name"]
        else:
            background_split_id = self.artifact_interaction_client.get_split_metadata(
                self.project.name, self.data_collection.name,
                background_split_name
            )["id"]
        if not background_split_name or not background_split_id:
            raise ValueError(
                "Background split cannot be inferred. Please make sure Background split is present in "
                "data collection."
            )
        return background_split_name, background_split_id

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
        split_mode: sm_pb.SplitMode = sm_pb.SplitMode.SPLIT_MODE_DATA_REQUIRED,
        sample_count: int = 5000,
        background_split_name: Optional[str] = None,
        influence_type: Optional[str] = None,
        **kwargs
    ):
        upload_via_data_layer = self._use_data_layer_for_split_ingestion(
            pre_data, label_col_name, id_col_name
        )

        background_split_id = None
        if feature_influence_data is not None:
            background_split_name, background_split_id = self._infer_background_split(
                background_split_name
            )
            influence_type = EXPLANATION_ALGORITHM_TYPE_TO_STR[
                workspace_validation_utils.
                validate_influence_type_str_for_virtual_model_upload(
                    influence_type, self.get_influence_type()
                )]

        self._validate_add_data_split(
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
            timestamp_col_name=timestamp_col_name,
            split_mode=split_mode,
            background_split_name=background_split_name,
            **kwargs
        )
        model_id = None
        if self._get_current_active_model_name():
            model_id = self.model.model_id
        # If we have an Id column and experimental feature is on, use data layer for all split
        # ingestion.
        if upload_via_data_layer:
            self._add_data_split_from_local_data_via_data_layer(
                data_split_name,
                pre_data,
                post_data=post_data,
                label_data=label_data,
                prediction_data=prediction_data,
                feature_influence_data=feature_influence_data,
                id_col_name=id_col_name,
                extra_data_df=extra_data_df,
                split_type=split_type,
                timestamp_col_name=timestamp_col_name,
                split_mode=split_mode,
                materialize_approx_max_rows=sample_count,
                background_split_id=background_split_id,
                model_id=model_id,
                score_type=self._get_score_type(),
                influence_type=influence_type
            )
        else:
            self.logger.info(
                "Upload of `prediction_data` and `feature_influence_data` is not supported."
            )
            self.create_data_split_via_upload_files(
                data_split_name,
                pre_data=pre_data,
                post_data=post_data,
                label_data=label_data,
                label_col_name=label_col_name,
                extra_data_df=extra_data_df,
                split_type=split_type,
                split_mode=split_mode,
                **kwargs
            )
        self._auto_create_model_tests(data_split_name)

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
        split_mode: sm_pb.SplitMode = sm_pb.SplitMode.SPLIT_MODE_DATA_REQUIRED,
        **kwargs
    ):
        self._validate_add_data_split_from_data_source(
            data_split_name,
            pre_data=pre_data,
            post_data=post_data,
            label_col_name=label_col_name,
            id_col_name=id_col_name,
            extra_data=extra_data,
            split_type=split_type,
            split_mode=split_mode,
            **kwargs
        )
        # If the user has just given us a uri and we're going to add a data source then attach
        # and create a split, we don't want that rowset showing up in queries unprompted. This
        # will set the creation reason to SYSTEM and we will filter in get rowsets calls by
        # default - for example on the data page.
        if isinstance(pre_data, str):
            if not kwargs:
                kwargs = {}
            kwargs["user_requested"] = False
        #TODO support post data + extra data here
        result = self._add_split_from_data_source(
            data_split_name, pre_data, label_col_name, id_col_name, split_type,
            kwargs.pop("timestamp_col_name", None), split_mode, **kwargs
        )
        if result["status"] == "OK":
            self._auto_create_model_tests(data_split_name)

    def _auto_create_model_tests(self, data_split_name: str):
        # TODO(AB #6997): (move call to auto create tests to the backend)
        if self.get_client_setting_value(
            "create_model_tests_on_split_ingestion"
        ):
            split_metadata = self.artifact_interaction_client.get_split_metadata(
                self._get_current_active_project_name(),
                self._get_current_active_data_collection_name(), data_split_name
            )
            self.tester.model_test_client.create_tests_from_split(
                self.project.id, split_metadata["id"]
            )

    def _add_data_split_from_local_data_via_data_layer(
        self,
        data_split_name: str,
        pre_data: Union[pd.DataFrame, Table, str],
        *,
        post_data: Optional[pd.DataFrame] = None,
        label_data: Optional[Union[pd.DataFrame, pd.Series, np.ndarray]] = None,
        prediction_data: Optional[pd.DataFrame] = None,
        feature_influence_data: Optional[pd.DataFrame] = None,
        id_col_name: Optional[str] = None,
        extra_data_df: Optional[pd.DataFrame] = None,
        split_type: Optional[str] = "all",
        timestamp_col_name: Optional[str] = None,
        split_mode: sm_pb.SplitMode = sm_pb.SplitMode.SPLIT_MODE_DATA_REQUIRED,
        materialize_approx_max_rows: Optional[int] = 5000,
        background_split_id: Optional[str] = None,
        model_id: Optional[str] = None,
        score_type: Optional[str] = None,
        influence_type: Optional[str] = None
    ):
        try:
            data_split_params = PandasDataSplitPathContainer(
                pre_data,
                post_data,
                extra_data_df,
                label_data,
                prediction_data,
                feature_influence_data,
                logger=self.logger
            )
            self.artifact_interaction_client.create_data_split_via_data_service(
                self.project.id,
                self.data_collection.id,
                data_split_name,
                split_type,
                data_split_params,
                id_col_name,
                split_mode=split_mode,
                timestamp_col=timestamp_col_name,
                materialize_approx_max_rows=materialize_approx_max_rows,
                background_split_id=background_split_id,
                model_id=model_id,
                score_type=score_type,
                influence_type=influence_type
            )
        finally:
            data_split_params.clean_up_temp_files()
        self.data_split_name = data_split_name
        return

    def _get_rowset(
        self, rowset: Union[Table, str], data_split_name: str, **kwargs
    ):
        if isinstance(rowset, str):
            temp_data_source_name = data_split_name + str(uuid.uuid4())
            return self.get_ingestion_client().add_data_source(
                temp_data_source_name, rowset, **kwargs
            )
        else:
            return rowset

    def _add_check_status_lambda(self, result):
        result[
            "check_status_lambda"
        ] = lambda: self.artifact_interaction_client.get_materialize_operation_status(
            self.project.id, result["operation_id"]
        )
        return result

    def add_labels(
        self, label_data: Union[Table, str], label_col_name: str,
        id_col_name: str, **kwargs
    ):
        self._validate_add_labels(label_data)
        data_split_name = self._get_current_active_data_split_name()
        rowset = self._get_rowset(label_data, data_split_name, **kwargs)

        result = rowset.add_labels(
            data_split_name, label_col_name, id_col_name, **kwargs
        )
        if result["status"] != "OK":
            self._add_check_status_lambda(result)
            self.logger.warning(
                "Labels are being uploaded, you can check the status of the operation by using `check_status_lambda`. "
            )
        return result

    def add_extra_data(
        self, extra_data: Union[Table, str], extras_col_name: str,
        id_col_name: str, **kwargs
    ):
        self._validate_add_extra_data(extra_data)
        data_split_name = self._get_current_active_data_split_name()
        rowset = self._get_rowset(extra_data, data_split_name, **kwargs)

        result = rowset.add_extra_data(
            data_split_name, extras_col_name, id_col_name, **kwargs
        )
        if result["status"] != "OK":
            self._add_check_status_lambda(result)
            self.logger.warning(
                "Extra data is being uploaded, you can check the status of the operation by using `check_status_lambda`. "
            )
        return result

    def add_nn_data_split(
        self,
        data_split_name: str,
        truera_wrappers: base.WrapperCollection,
        split_type: Optional[str] = "all",
        *,
        pre_data: Optional[Union[np.ndarray, pd.DataFrame]] = None,
        label_data: Optional[pd.DataFrame] = None,
        extra_data_df: Optional[pd.DataFrame] = None,
    ):
        self._validate_add_nn_data_split(
            data_split_name, label_data, extra_data_df
        )
        try:
            wrapper_tmp_dir = tempfile.TemporaryDirectory()
            wrapper_tmp_path = wrapper_tmp_dir.name
            self._save_object_file(
                wrapper_tmp_path, SPLIT_LOAD_WRAPPER_SAVE_NAME,
                truera_wrappers.split_load_wrapper
            )
            local_file_location = truera_wrappers.split_load_wrapper.get_data_path(
            )
            data_collection_name = self._get_current_active_data_collection_name(
            )
            dc_metadata = self.project.get_data_collection_metadata(
                data_collection_name, as_json=False
            )
            data_collection = self.project.create_data_collection(
                data_collection_name, dc_metadata.feature_transform_type
            )
            if label_data is not None and "__truera_id__" in label_data.columns:
                label_data = label_data.drop(columns=["__truera_id__"])
            label_file_name = self._write_input_file(
                label_data, "label", header=False, extension="csv"
            )
            if extra_data_df is not None and "__truera_id__" in extra_data_df.columns:
                extra_data_df = extra_data_df.drop(columns=["__truera_id__"])
            extra_data_file_name = self._write_input_file(
                extra_data_df, "extra", extension="csv"
            )
            if pre_data is not None and isinstance(pre_data, pd.DataFrame):
                pre_data_file_name = self._write_input_file(
                    pre_data, "pre", extension="csv"
                )
            else:
                # TODO: this only works if there are labels which we can assume for the time being.
                pre_data_file_name = self._write_input_file(
                    pd.DataFrame(data=list(range(len(label_data)))),
                    "pre",
                    extension="csv"
                )

            data_collection.create_data_split(
                data_split_name,
                _map_split_type(split_type),
                pre_transform_path=pre_data_file_name,
                labels_path=label_file_name,
                extra_data_path=extra_data_file_name,
                split_dir=local_file_location,
                data_split_loader_wrapper_path=wrapper_tmp_path,
                split_mode=sm_pb.SplitMode.SPLIT_MODE_NON_TABULAR
            )

            data_collection.upload_new_split(
                self.artifact_interaction_client, self.project.name
            )
        finally:
            try:
                wrapper_tmp_dir.cleanup()
            except:
                pass

        self.data_split_name = data_split_name
        self._print_add_data_split_message(
            self.logger, data_split_name, is_remote=True
        )

    def create_data_split_via_upload_files(
        self,
        data_split_name: str,
        *,
        pre_data: pd.DataFrame,
        post_data: Optional[pd.DataFrame] = None,
        label_data: Optional[Union[pd.DataFrame, pd.Series, np.ndarray]] = None,
        label_col_name: Optional[str] = None,
        extra_data_df: Optional[pd.DataFrame] = None,
        split_type: Optional[str] = "all",
        split_mode: sm_pb.SplitMode = sm_pb.SplitMode.SPLIT_MODE_DATA_REQUIRED,
        **kwargs
    ):
        label_df = self.get_df_from_args(
            column_name=label_col_name, source_df=pre_data, raw_data=label_data
        )

        prediction_col_name = kwargs.pop("prediction_col_name", None)
        prediction_df = self.get_df_from_args(
            column_name=prediction_col_name, source_df=pre_data, raw_data=None
        )

        pre_data_df = self.drop_other_columns(
            pre_data, other_columns=[label_col_name, prediction_col_name]
        )
        post_data_df = self.drop_other_columns(
            post_data, other_columns=[label_col_name, prediction_col_name]
        )

        try:
            if not kwargs:
                kwargs = {}
            label_file_name = self._write_input_file(
                label_df, "label", header=False, extension="csv"
            )
            extra_data_file_name = self._write_input_file(
                extra_data_df, "extra", extension="csv"
            )
            prediction_file_name = self._write_input_file(
                prediction_df, "prediction", extension="csv"
            )
            pre_data_file_name = self._write_input_file(
                pre_data_df, "pre", extension="csv"
            )
            post_data_file_name = self._write_input_file(
                post_data_df,
                "post",
                info_log=
                "Separate pre/post-transform data has been ingested. This should adhere to the feature mapping you specified while adding the data collection.",
                extension="csv"
            )
            prediction_cache = None

            if prediction_df is not None:
                import truera
                prediction_cache = self.project.create_prediction_cache(
                    self._get_current_active_model_name(),
                    self._get_current_active_data_collection_name(),
                    split_name=data_split_name,
                    cache_location=prediction_file_name,
                    score_type=self._get_score_type(),
                    model_output_type=self._get_output_type(),
                    client_name="notebook_client",
                    client_version=f"{truera.__version__}",
                    row_count=len(prediction_df)
                )
            data_collection_name = self._get_current_active_data_collection_name(
            )
            dc_metadata = self.project.get_data_collection_metadata(
                data_collection_name, as_json=False
            )
            data_collection = self.project.create_data_collection(
                data_collection_name, dc_metadata.feature_transform_type
            )

            if split_mode == sm_pb.SplitMode.SPLIT_MODE_DATA_REQUIRED:
                pre_transform_path = pre_data_file_name
                if post_data is not None:
                    post_transform_path = post_data_file_name
                else:
                    post_transform_path = pre_data_file_name
            else:
                pre_transform_path = None
                post_transform_path = None

            data_collection.create_data_split(
                data_split_name,
                _map_split_type(split_type),
                pre_transform_path=pre_transform_path,
                post_transform_path=post_transform_path,
                labels_path=label_file_name,
                extra_data_path=extra_data_file_name,
                split_mode=split_mode,
                **kwargs
            )

            data_collection.upload_new_split(
                self.artifact_interaction_client, self.project.name
            )
            if prediction_cache:
                prediction_cache.upload(
                    self.artifact_interaction_client,
                    create_model=False,
                    overwrite=False
                )

        finally:
            best_effort_remove_temp_files(
                [
                    label_file_name, extra_data_file_name, pre_data_file_name,
                    post_data_file_name, prediction_file_name
                ]
            )
        self.data_split_name = data_split_name
        self._print_add_data_split_message(
            self.logger, data_split_name, is_remote=True
        )

    def get_df_from_args(self, column_name, source_df, raw_data):
        if column_name:
            return source_df[column_name]
        elif isinstance(raw_data, np.ndarray):
            return pd.DataFrame(raw_data)
        elif isinstance(raw_data, pd.Series):
            return raw_data.to_frame()
        else:
            return raw_data

    def drop_other_columns(self, input_data, other_columns):
        if input_data is not None:
            return input_data.drop(
                columns=other_columns, inplace=False, errors="ignore"
            )
        return None

    def _write_input_file(
        self,
        df,
        file_name_for_log,
        *,
        info_log=None,
        header=True,
        extension=None
    ):
        if df is not None:
            output_path = create_temp_file_path(extension=extension)
            df.to_csv(output_path, index=False, header=header, na_rep=NAN_REP)

            self.logger.debug(
                f"Saved {file_name_for_log} data file to {output_path}. Size of file: {os.path.getsize(output_path)}"
            )
            if info_log:
                self.logger.info(info_log)

            return output_path

        return None

    def _is_virtual_model(self) -> bool:
        model_meta = self.artifact_interaction_client.get_model_metadata(
            project_name=self._get_current_active_project_name(),
            model_name=self._get_current_active_model_name()
        )
        return model_meta["model_type"].lower() == "virtual"

    def _validate_add_virtual_model_artifact(
        self, data_split_name: Optional[str], is_predictions: bool = True
    ):
        self._ensure_project()
        self._ensure_data_collection()
        self._ensure_model()
        if data_split_name is None:
            self._ensure_data_split()
            data_split_name = self._get_current_active_data_split_name()
        elif data_split_name not in self.get_data_splits():
            raise ValueError(
                f"Split `{data_split_name}` does not exist in data collection {self._get_current_active_data_collection_name()}"
            )
        if not self._is_virtual_model():
            artifact_name = "predictions" if is_predictions else "feature influences"
            alternative_fn_name = "`tru.get_ys_pred()`" if is_predictions else "`tru.get_feature_influences()`"
            raise ValueError(
                f"Adding {artifact_name} is only supported for virtual models! See {alternative_fn_name} to get {artifact_name} for non-virtual models."
            )

        split_metadata = self.artifact_interaction_client.get_split_metadata(
            self._get_current_active_project_name(),
            self._get_current_active_data_collection_name(), data_split_name
        )
        if split_metadata["split_mode"] == "SPLIT_MODE_PREDS_REQUIRED":
            raise ValueError(
                "Delayed predictions cannot be added for monitoring super lite splits!"
            )
        aiq_split_metadata = self.aiq_client.get_split_metadata(
            self.project.id,
            split_metadata["id"],
            split_metadata["data_collection_id"],
        )
        return aiq_split_metadata

    def _validate_add_model_predictions(
        self,
        prediction_data: Union[pd.Series, np.ndarray, Table, str],
        *,
        prediction_col_name: Optional[str] = None,
        id_col_name: Optional[str] = None,
        data_split_name: Optional[str] = None
    ) -> bool:
        aiq_split_metadata = self._validate_add_virtual_model_artifact(
            data_split_name, is_predictions=True
        )

        # if prediction_data is [pd.Series, np.ndarray], then must align with x data
        if isinstance(prediction_data, (pd.Series, np.ndarray)):
            if len(prediction_data) != aiq_split_metadata.rows:
                raise ValueError(
                    f"Provided prediction data has {len(prediction_data)} rows, but split has {aiq_split_metadata.rows} rows! To add partial predictions, prediction data must be a Table or string URI with a valid ID column to join."
                )
            if prediction_data.ndim != 1:
                raise ValueError(
                    "Provided prediction data is not one-dimensional!"
                )
            self.logger.warning(
                "Assuming that predictions are aligned to underlying split data. It is recommended to add model predictions using a Table or URI along with an ID column to safely join predictions to split data."
            )
            return False

        # otherwise, ingestion happens via data layer using ID col join
        if isinstance(prediction_data, (Table, str)):
            if not prediction_col_name or not id_col_name:
                raise ValueError(
                    "`prediction_col_name` and `id_col_name` must be provided if ingesting predictions from a Table or str!"
                )
            if not aiq_split_metadata.system_columns.unique_id_column_name:
                raise ValueError(
                    "Cannot add prediction data to split without a system ID column!"
                )
            return True

        raise ValueError(
            f"`prediction_data` is type {type(prediction_data)}, expected one of [pd.Series, np.ndarray, Table, str]!"
        )

    def _validate_add_model_feature_influences(
        self,
        feature_influence_data: pd.DataFrame,
        data_split_name: Optional[str] = None,
        background_data_split_name: Optional[str] = None,
        id_col_name: Optional[str] = None,
        timestamp_col_name: Optional[str] = None,
        influence_type: Optional[str] = None
    ) -> bool:
        aiq_split_metadata = self._validate_add_virtual_model_artifact(
            data_split_name, is_predictions=False
        )

        return workspace_validation_utils.validate_add_feature_influence(
            feature_influence_data,
            aiq_split_metadata,
            data_splits=self.get_data_splits(),
            data_collection_name=self._get_current_active_data_collection_name(
            ),
            background_data_split_name=background_data_split_name,
            id_col_name=id_col_name,
            timestamp_col_name=timestamp_col_name,
            influence_type=influence_type,
            project_influence_type=self.get_influence_type()
        )

    def add_model_predictions(
        self,
        prediction_data: Union[pd.Series, np.ndarray, Table, str],
        *,
        prediction_col_name: Optional[str] = None,
        id_col_name: Optional[str] = None,
        data_split_name: Optional[str] = None
    ):
        #TODO(AB#6655): always force prediction through data layer
        add_preds_via_data_layer = self._validate_add_model_predictions(
            prediction_data,
            prediction_col_name=prediction_col_name,
            id_col_name=id_col_name,
            data_split_name=data_split_name
        )
        data_split_name = data_split_name or self._get_current_active_data_split_name(
        )
        if not add_preds_via_data_layer:
            if not isinstance(prediction_data, pd.Series):
                prediction_data = pd.Series(
                    prediction_data, name=PREDICTION_COLUMN_NAME
                )
            with WorkspaceContextCleaner(self):
                cache_location = create_temp_file_path(extension="csv")
                self.set_data_split(data_split_name)
                with ModelCacheUploader(
                    self, CacheType.MODEL_PREDICTION_CACHE, cache_location
                ) as cache_uploader:
                    prediction_data.to_csv(
                        cache_location, index=False, header=True
                    )
                    cache_uploader.upload(
                        row_count=len(prediction_data),
                        create_model=False,
                        overwrite=False
                    )
        else:
            result = self._get_rowset(
                prediction_data, data_split_name
            ).add_predictions(
                data_split_name,
                prediction_col_name,
                id_col_name,
                model_name=self._get_current_active_model_name(),
                score_type=self._get_score_type()
            )
            if result["status"] != "OK":
                self._add_check_status_lambda(result)
                self.logger.warning(
                    "Predictions are being uploaded, you can check the status of the operation by using `check_status_lambda`. "
                )
            return result

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
        background_split_name, background_split_id = self._infer_background_split(
            background_split_name
        )

        add_via_data_layer = self._validate_add_model_feature_influences(
            feature_influence_data,
            data_split_name=data_split_name,
            background_data_split_name=background_split_name,
            id_col_name=id_col_name,
            timestamp_col_name=timestamp_col_name,
            influence_type=influence_type
        )

        data_split_name = data_split_name or self._get_current_active_data_split_name(
        )

        if timestamp_col_name:
            feature_influence_data[timestamp_col_name] = pd.to_datetime(
                feature_influence_data[timestamp_col_name],
                infer_datetime_format=True
            )
            # data layer expects timestamp in format %Y-%m-%d %H:%M:%S (1996-06-08 10:01:11)
            feature_influence_data[timestamp_col_name] = feature_influence_data[
                timestamp_col_name].dt.strftime(
                    DataServiceClient.TIMESTAMP_FORMAT
                )

        cache_location = create_temp_file_path(extension="csv")
        feature_influence_data.to_csv(cache_location, index=False)

        with WorkspaceContextCleaner(self):
            if not add_via_data_layer:
                explanation_algorithm_type = workspace_validation_utils.\
                    validate_influence_type_str_for_virtual_model_upload(influence_type, self.get_influence_type())
                self.set_data_split(data_split_name)

                with ModelCacheUploader(
                    self, CacheType.EXPLANATION_CACHE, cache_location
                ) as cache_uploader:
                    cache_uploader.upload(
                        row_count=len(feature_influence_data),
                        background_data_split_name=background_split_name,
                        explanation_algorithm_type=explanation_algorithm_type,
                        create_model=False,
                        overwrite=False
                    )
            else:
                fi_table = self.get_ingestion_client().add_data_source(
                    name=f"{data_split_name}_fis_{str(uuid.uuid4())}",
                    uri=cache_location,
                    format="csv",
                    date_format=DataServiceClient.TIMESTAMP_FORMAT
                )

                fi_table.add_feature_influences(
                    data_split_name=data_split_name,
                    feature_influence_col_names=feature_influence_data.columns.
                    tolist(),
                    id_col_name=id_col_name,
                    model_name=self.model.model_name,
                    timestamp_col_name=timestamp_col_name,
                    background_split_id=background_split_id,
                    influence_type=influence_type
                )

    def _validate_attach_model_object(self):
        self._ensure_project()
        self._ensure_data_collection()
        self._ensure_model()
        if not self._is_virtual_model():
            raise ValueError(
                "Attaching executable model objects is only supported for virtual model! This model is already executable."
            )

    def attach_packaged_python_model_object(
        self, model_object_dir: str, verify_model: bool = True
    ):
        self._validate_attach_model_object()
        if verify_model:
            self.verify_packaged_model(
                model_object_dir
            )  # full validation using split data
        else:
            verify_python_model_folder(
                model_object_dir, logger=self.logger
            )  # basic checking on folder structure

        model = self.project.get_model(
            self._get_current_active_model_name(),
            self._get_current_active_data_collection_name()
        )
        model.upgrade_virtual(
            self.artifact_interaction_client, ModelType.PyFunc, model_object_dir
        )

    def attach_python_model_object(
        self,
        model_object: Any,
        additional_pip_dependencies: Optional[Sequence[str]] = None,
        verify_model: bool = True,
    ):
        self._validate_attach_model_object()
        feature_transform_type = self._get_feature_transform_type_for_data_collection(
        )
        temp_staging_dir = tempfile.mkdtemp()
        shutil.rmtree(temp_staging_dir, ignore_errors=True)
        try:
            self.prepare_python_model_folder_from_model_object(
                temp_staging_dir,
                model_object,
                None,
                feature_transform_type=feature_transform_type,
                additional_pip_dependencies=additional_pip_dependencies,
            )
            self.attach_packaged_python_model_object(
                temp_staging_dir, verify_model=verify_model
            )
        finally:
            shutil.rmtree(temp_staging_dir, ignore_errors=True)

    def add_feature_metadata(
        self,
        feature_description_map: Optional[Mapping[str, str]] = None,
        missing_values: Optional[Sequence[str]] = None,
        force_update: bool = False
    ):
        project_name = self._ensure_project()
        data_collection_name = self._ensure_data_collection()
        self.logger.info(
            f"Uploading feature description for project: {project_name} and data_collection: {data_collection_name}"
        )
        preprocessed_cols = None
        postprocessed_cols = None

        if feature_description_map:
            if self.get_data_splits():
                with WorkspaceContextCleaner(self):
                    self.set_data_split(self.get_data_splits()[0])
                    preprocessed_cols = set(self.get_xs(0, 1).columns)
                    postprocessed_cols = set(
                        self._get_xs_postprocessed(0, 1).columns
                    )
            else:  # feature description map provided
                preprocessed_cols = list(feature_description_map.keys())
        self.feature_client.upload_feature_description_and_group_metadata(
            project_name,
            data_collection_name,
            pre_features=preprocessed_cols,
            post_features=postprocessed_cols,
            feature_description_map=feature_description_map,
            missing_values=missing_values,
            force=force_update,
            only_update_metadata=True
        )

    def _get_pre_to_post_feature_map(
        self
    ) -> Optional[Mapping[str, Sequence[str]]]:
        project_name = self._ensure_project()
        data_collection_name = self._ensure_data_collection()
        return self.feature_client.get_pre_to_post_feature_map(
            project_name, data_collection_name
        )

    def _get_feature_description_map(
        self
    ) -> Optional[Mapping[str, Sequence[str]]]:
        project_name = self._ensure_project()
        data_collection_name = self._ensure_data_collection()
        return self.feature_client.get_feature_description_map(
            project_name, data_collection_name
        )

    def get_xs(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        extra_data: bool = False,
        system_data: bool = False
    ) -> pd.DataFrame:
        self._ensure_project()
        self._ensure_data_collection()
        self._ensure_data_split()
        return self._get_xs_for_split(
            self._get_current_active_data_split_name(),
            start,
            stop,
            extra_data=extra_data,
            system_data=system_data
        )

    def _get_xs_for_split(
        self,
        data_split_name: str,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        extra_data: bool = False,
        system_data: bool = False,
        get_post_processed_data: bool = False
    ):
        split_metadata = self.artifact_interaction_client.get_split_metadata(
            self._get_current_active_project_name(),
            self._get_current_active_data_collection_name(), data_split_name
        )
        return self.aiq_client.get_xs(
            self.project.id,
            split_metadata["id"],
            split_metadata["data_collection_id"],
            start,
            stop,
            extra_data=extra_data,
            system_data=system_data,
            get_post_processed_data=get_post_processed_data
        ).response

    def _get_xs_postprocessed(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        system_data: bool = False
    ) -> pd.DataFrame:
        self._ensure_project()
        self._ensure_data_collection()
        self._ensure_data_split()
        return self._get_xs_for_split(
            self._get_current_active_data_split_name(),
            start,
            stop,
            get_post_processed_data=True,
            system_data=system_data
        )

    def get_ys(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        system_data: bool = False
    ) -> Union[pd.Series, pd.DataFrame]:
        project_name = self._ensure_project()
        data_collection_name = self._ensure_data_collection()
        split_name = self._ensure_data_split()
        split_metadata = self.artifact_interaction_client.get_split_metadata(
            project_name, data_collection_name, split_name
        )
        return self.aiq_client.get_ys(
            self.project.id,
            split_metadata["id"],
            split_metadata["data_collection_id"],
            start,
            stop,
            system_data=system_data
        ).response

    def get_model_threshold(self) -> float:
        self._validate_get_model_threshold()
        return self.cs_client.get_classification_threshold(
            self.project.id, self.model.model_id, self._get_score_type()
        )

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
        self.cs_client.update_classification_threshold_configuration(
            self.project.id,
            self.model.model_id,
            classification_threshold=classification_threshold,
            score_type=score_type
        )

    def set_influences_background_data_split(
        self,
        data_split_name: str,
        data_collection_name: Optional[str] = None
    ) -> None:
        self._ensure_project()
        if data_collection_name:
            self._validate_data_collection(data_collection_name)
        else:
            data_collection_name = self._ensure_data_collection()
        self._validate_data_split(data_split_name, data_collection_name)
        background_split_id = self.artifact_interaction_client.get_split_metadata(
            self._get_current_active_project_name(),
            data_collection_name,
            split_name=data_split_name
        )["id"]
        self.cs_client.set_base_split(
            self.project.id, self.data_collection.id, background_split_id
        )

    def get_influences_background_data_split(
        self, data_collection_name: Optional[str] = None
    ) -> str:
        self._ensure_project()
        if not data_collection_name:
            data_collection_name = self._ensure_data_collection()
            data_collection_id = self.data_collection.id
        else:
            self._validate_data_collection(data_collection_name)
            data_collection_id = self.artifact_interaction_client.get_data_collection_id(
                self.project.id, data_collection_name
            )

        background_split_id = self.cs_client.get_base_split(
            self.project.id,
            data_collection_id,
        )
        if not background_split_id:
            raise ValueError(
                f"Background data split has not been set for data collection \"{data_collection_name}\"! Please set it using `set_influences_background_data_split`"
            )
        return self.artifact_interaction_client.get_split_metadata_by_id(
            self.project.id, split_id=background_split_id
        )["name"]

    def add_segment_group(
        self, name: str, segment_definitions: Mapping[str, str]
    ) -> None:
        self._validate_add_segment_group(name, segment_definitions)
        split_metadata = self.artifact_interaction_client.get_split_metadata(
            self._get_current_active_project_name(),
            self._get_current_active_data_collection_name(),
            self._get_current_active_data_split_name()
        )
        self.aiq_client.add_segment_group(
            self.project.id, name, segment_definitions,
            split_metadata["data_collection_id"], split_metadata["id"],
            self._get_score_type()
        )

    def set_as_protected_segment(
        self, segment_group_name: str, segment_name: str
    ):
        segment_groups = self.aiq_client.get_wrapped_segmentations(
            self.project.id
        ).response
        if segment_group_name not in segment_groups:
            raise NotFoundError(
                f"Segment group \"{segment_group_name}\" does not exist!"
            )
        if segment_name not in segment_groups[segment_group_name].get_segments(
        ):
            raise NotFoundError(
                f"Segment \"{segment_name}\" does not exist in segment group \"{segment_group_name}\"!"
            )
        self.aiq_client.set_as_protected_segment(
            self.project.id, segment_groups[segment_group_name].id, segment_name
        )

    def delete_segment_group(self, name: str) -> None:
        self._ensure_project()
        self.aiq_client.delete_segment_group(self.project.id, name)

    def get_segment_groups(self) -> Mapping[str, Mapping[str, str]]:
        self._ensure_project()
        segment_groups = self.aiq_client.get_wrapped_segmentations(
            self.project.id, convert_model_ids_to_model_names=True
        ).response
        return self._get_str_desc_of_segment_groups(segment_groups)

    def get_explainer(
        self,
        base_data_split: Optional[str] = None,
        comparison_data_splits: Optional[Sequence[str]] = None
    ) -> RemoteExplainer:
        self._ensure_project()
        self._ensure_model()
        return RemoteExplainer(
            self, self.project, self.model,
            self._get_current_active_data_collection_name(), base_data_split,
            comparison_data_splits
        )

    def get_ingestion_client(self) -> IngestionClient:
        project_name = self._ensure_project()
        data_collection_name = self._ensure_data_collection()
        return IngestionClient(
            project=project_name,
            default_score_type=self._get_score_type(),
            data_collection=data_collection_name,
            artifact_interaction_client=self.artifact_interaction_client,
            data_service_client=self.data_service_client,
            configuration_service_client=self.cs_client,
            logger=self.logger
        )

    def get_context(self) -> Mapping[str, str]:
        return {
            "project":
                self.project.name if self.project else "",
            "data-collection":
                self.data_collection.name if self.data_collection else "",
            "data-split":
                self.data_split_name or "",
            "model":
                self.model.model_name if self.model else "",
            "connection-string":
                self.connection_string
        }

    def add_model_metadata(
        self,
        train_split_name: Optional[str] = None,
        train_parameters: Optional[Mapping[str, Any]] = None,
        overwrite: bool = False
    ) -> None:
        self._ensure_project()
        self._ensure_model()
        validate_model_metadata(
            train_split_name=train_split_name,
            existing_split_names=self.get_data_splits(),
            train_parameters=train_parameters,
            logger=self.logger
        )
        self.artifact_interaction_client.add_train_split_to_model(
            project_name=self._get_current_active_project_name(),
            model_name=self._get_current_active_model_name(),
            train_split_name=train_split_name,
            overwrite=overwrite
        )
        self.artifact_interaction_client.add_train_parameters_to_model(
            project_name=self._get_current_active_project_name(),
            model_name=self._get_current_active_model_name(),
            train_parameters=train_parameters,
            overwrite=overwrite
        )

    def delete_model_metadata(self) -> None:
        self._ensure_project()
        self._ensure_model()
        self.ar_client.update_model_metadata(
            self.project.id, self._get_current_active_model_name(), {
                "train_split_id": "",
                "train_parameters": {}
            }
        )

    def get_model_metadata(self) -> Mapping[str, Union[str, Mapping[str, str]]]:
        self._ensure_project()
        self._ensure_model()
        return self._get_model_metadata(self._get_current_active_model_name())

    def _get_model_metadata(
        self, model_name: str
    ) -> Mapping[str, Union[str, Mapping[str, str]]]:
        model_metadata = self.artifact_interaction_client.get_model_metadata(
            self.project.id, model_name=model_name, as_json=True
        )
        train_split_name = None
        if model_metadata["training_metadata"]["train_split_id"]:
            train_split_name = self.artifact_interaction_client.get_split_metadata_by_id(
                self.project.id,
                model_metadata["training_metadata"]["train_split_id"]
            )["name"]
        if not model_metadata["training_metadata"].get("parameters"):
            model_metadata["training_metadata"]["parameters"] = None
        return {
            "train_split_name":
                train_split_name,
            "train_parameters":
                model_metadata["training_metadata"]["parameters"]
        }

    def _get_score_type(self) -> str:
        self._ensure_project()
        return self._get_score_type_for_project(self.project.id)

    def _get_score_type_for_project(self, project_id: str) -> str:
        project_metadata = self.artifact_interaction_client.get_project_metadata(
            project_id
        )
        return get_string_from_qoi_string(
            project_metadata["settings"]["score_type"]
        )

    def _get_input_type(self):
        self._ensure_project()
        return self._fetch_and_parse_project_metadata(
            self._get_current_active_project_name()
        )["input_type"]

    def _save_object_file(self, path: str, name: str, obj: Any):
        path_to_file = os.path.join(path, name)
        with open(path_to_file, 'wb+') as handle:
            cloudpickle.dump(obj, handle)
        return path_to_file

    def verify_nn_wrappers(
        self,
        clf,
        model_run_wrapper: base.Wrappers.ModelRunWrapper,
        split_load_wrapper: base.Wrappers.SplitLoadWrapper,
        model_load_wrapper: base.Wrappers.ModelLoadWrapper,
        attr_config: AttributionConfiguration = None
    ):
        from truera.client.cli.verify_nn_ingestion import verify
        from truera.client.cli.verify_nn_ingestion import VerifyHelper

        self._ensure_project()
        if model_load_wrapper is None:
            raise ValueError(
                f"The current project: {self.get_context()['project']} is a remote project. pass a ModelLoadWrapper using `model_load_wrapper`"
            )
        project_input_type = self.project.input_type
        score_type = self._get_score_type()
        output_type = get_output_type_from_score_type(score_type)

        verify_helper: VerifyHelper = verify.get_helper(
            model_input_type=project_input_type,
            model_output_type=output_type,
            attr_config=attr_config,
            model=clf,
            split_load_wrapper=split_load_wrapper,
            model_run_wrapper=model_run_wrapper,
            model_load_wrapper=model_load_wrapper
        )

        verify.verify_model(verify_helper)
        super(RemoteTrueraWorkspace,
              self)._verify_nn_wrappers(verify_helper, logger=self.logger)

    def get_nn_user_configs(
        self
    ) -> Union[AttributionConfiguration, RNNUserInterfaceConfiguration]:
        self._ensure_model()
        model_metadata = self.artifact_interaction_client.get_model_metadata(
            self.project.id, model_name=self.model.model_name, as_json=False
        )
        if model_metadata.HasField("rnn_attribution_config"):
            nn_attribution_config = model_metadata.rnn_attribution_config
        elif model_metadata.HasField("nlp_attribution_config"):
            nn_attribution_config = model_metadata.nlp_attribution_config
        return (model_metadata.rnn_ui_config, nn_attribution_config)

    def update_nn_user_config(
        self, config: Union[AttributionConfiguration,
                            RNNUserInterfaceConfiguration]
    ):
        self._ensure_model()
        if not isinstance(
            config, (AttributionConfiguration, RNNUserInterfaceConfiguration)
        ):
            raise ValueError(
                f"Trying to add an unsupported NN config: {config}. Supported NN config types: [`AttributionConfiguration`, `RNNUserInterfaceConfiguration`]"
            )
        if isinstance(config, RNNUserInterfaceConfiguration):
            param_name = "rnn_ui_config"
        elif isinstance(config, RNNAttributionConfiguration):
            param_name = "rnn_attribution_config"
        elif isinstance(config, NLPAttributionConfiguration):
            param_name = "nlp_attribution_config"

        self.ar_client.update_model_metadata(
            self.project.id, self.model.model_name, {param_name: config}
        )

    def _add_split_from_data_source(
        self, data_split_name: str, data: Union[Table, str],
        label_col_name: str, id_col_name: str, split_type: str,
        timestamp_col_name: str, split_mode: sm_pb.SplitMode, **kwargs
    ):
        if isinstance(data, str):
            temp_data_source_name = data_split_name + str(uuid.uuid4())
            rowset = self.get_ingestion_client().add_data_source(
                temp_data_source_name, data, **kwargs
            )
        elif isinstance(data, Table):
            rowset = data
        else:
            raise ValueError("Expected data to either `Table` or `str` (URI).")

        # Presence of model is verified in _validate_add_data_split()
        if kwargs.get("prediction_col_name"):
            kwargs["model_name"] = self._get_current_active_model_name()
            kwargs["score_type"] = self._get_score_type()

        result = rowset.add_data_split(
            data_split_name=data_split_name,
            data_split_type=split_type,
            label_col_name=label_col_name,
            id_col_name=id_col_name,
            timestamp_col_name=timestamp_col_name,
            split_mode=split_mode,
            **kwargs
        )
        if result["status"] == "OK":
            self.data_split_name = data_split_name
            return result
        result[
            "check_status_lambda"
        ] = lambda: self.artifact_interaction_client.get_materialize_operation_status(
            self.project.id, result["operation_id"]
        )
        self.logger.warning(
            "Split is being created, you can check the status of the operation by using `check_status_lambda`. "
            "To work on this split, use set_data_split once the operation is successful."
        )
        return result

    def _fetch_and_parse_project_metadata(self, project_name: str) -> dict:
        try:
            project_metadata = self.artifact_interaction_client.get_project_metadata(
                project_name
            )
            input_type = project_metadata["settings"]["input_data_format"
                                                     ].lower()
            score_type = get_string_from_qoi_string(
                project_metadata["settings"]["score_type"]
            )
            return {
                'id': project_metadata['id'],
                'created_at': project_metadata['created_at'],
                'input_type': input_type,
                'score_type': score_type
            }
        except MetadataNotFoundException:
            return {}

    def _delete_empty_project(self):
        for data_source_name in self.get_data_sources():
            self.delete_data_source(data_source_name)
        self.artifact_interaction_client.delete_project(self.project.id)

    def download_nn_artifact(
        self, artifact_type: ArtifactType, download_basepath: str
    ) -> str:
        """ Downloads NN artifacts from the TruEra deployment to a local path.
        This differs from current tabular implementation where data management is taken care of by TruEra's AIQ service.
        The NN non-remote aiq `truera.nlp/rnn.general.aiq.py` are stand-ins that try to best recreate aiq services. It accesses file paths with 
        special naming that mimics metarepo project/model/split conventions. All cache items end in a file folder of files
        in the form of memmaps, pickle, or txt files.

        Args:
            artifact_type: A datasplit, model, or cache designation. Determines what is being downloaded.
            download_basepath: The path to which files are to be downloaded. NN Artifacts are in memmap, pickle, or text files.

        Returns:
            The path of the downloaded files.
        """
        download_project_path = os.path.join(download_basepath, self.project.id)
        if artifact_type == ArtifactType.datasplit:
            artifact_id = self.data_split_name
            scoping_artifact_ids = [
                self._get_current_active_data_collection_name()
            ]
            download_path = os.path.join(
                download_project_path, "datasplits",
                self._get_current_active_data_collection_name(), artifact_id
            )
        elif artifact_type == ArtifactType.model:
            artifact_id = self.model.model_name
            scoping_artifact_ids = []
            download_path = os.path.join(
                download_project_path, "models", artifact_id
            )
        elif artifact_type == ArtifactType.cache:
            artifact_id = f"{self.model.model_name}__{self.data_split_name}___explanation_cache_INTEGRATED_GRADIENTS"
            scoping_artifact_ids = [
                "explanation_caches", self.model.model_id,
                self._get_current_active_data_collection_name(),
                self.data_split_name,
                self._get_score_type(),
                self.get_influences_background_data_split(),
                ExplanationAlgorithmType.Name(
                    ExplanationAlgorithmType.INTEGRATED_GRADIENTS
                )
            ]
            download_path = os.path.join(
                download_project_path, "caches", *scoping_artifact_ids,
                artifact_id
            )
        else:
            raise ValueError(
                f"Unsupported artifact_type for download: {artifact_type}"
            )
        self.ar_client.download_artifact(
            src_project_id=self.project.name,
            src_artifact_type=artifact_type,
            src_artifact_id=artifact_id,
            src_intra_artifact_path='',
            scoping_artifact_ids=scoping_artifact_ids,
            dest=download_path
        )
        return download_path

    def _validate_data_split(
        self, data_split_name: str, data_collection_name: str
    ) -> None:
        available_splits = self.artifact_interaction_client.get_all_datasplits_in_data_collection(
            self.project.id, data_collection_name
        )
        if data_split_name not in available_splits:
            raise ValueError(
                f"No such data split \"{data_split_name}\" in data collection \"{data_collection_name}\"!"
            )

    def reset_context(self):
        self.set_model(None)
        self.set_data_collection(None)
        self.project = None

    def prepare_python_model_folder_from_model_object(
        self,
        output_dir: str,
        model: Any,
        transformer: Optional[Any],
        feature_transform_type: FeatureTransformationType,
        additional_pip_dependencies: Optional[Sequence[str]] = None,
        additional_modules: Optional[Sequence[Any]] = None,
        **kwargs
    ) -> str:
        self._validate_additional_modules(additional_modules)
        additional_pip_dependencies = PipDependencyParser(
            additional_pip_dependencies
        )
        additional_pip_dependencies.add_default_model_runner_dependencies()
        # devnote: the `python_version` kwarg is undocumented; should be used as an override only if absolutely necessary
        python_version = kwargs.get("python_version", get_python_version_str())
        output_type = self._get_output_type()
        if callable(model):
            ModelPredictPackager(
                model, transformer, output_type, python_version,
                additional_pip_dependencies
            ).save_model(
                self.logger, output_dir, additional_modules=additional_modules
            )
        else:
            (name,
             module) = (model.__class__.__name__, model.__class__.__module__)
            if module.startswith("xgboost"):
                self.logger.info("Uploading xgboost model: %s", name)
                XgBoostModelPackager(
                    model, transformer, output_type, python_version,
                    additional_pip_dependencies
                ).save_model(
                    self.logger,
                    output_dir,
                    additional_modules=additional_modules
                )
            elif module.startswith("sklearn.pipeline"):
                self.logger.info(f"Uploading sklearn.pipeline model: {name}")
                if feature_transform_type == FEATURE_TRANSFORM_TYPE_PRE_POST_DATA:
                    raise ValueError(
                        "Pre-/post-data transform is not supported for sklearn pipeline object."
                    )

                SklearnPipelineModelPackager(
                    model, transformer, output_type, python_version,
                    additional_pip_dependencies, feature_transform_type
                ).save_model(
                    self.logger,
                    output_dir,
                    additional_modules=additional_modules
                )
            elif module.startswith("sklearn"):
                self.logger.info("Uploading sklearn model: %s", name)
                SklearnModelPackager(
                    model, transformer, output_type, python_version,
                    additional_pip_dependencies
                ).save_model(
                    self.logger,
                    output_dir,
                    additional_modules=additional_modules
                )
            elif module == "catboost.core":
                self.logger.info("Uploading catboost model")
                CatBoostModelPackager(
                    model, transformer, output_type, python_version,
                    additional_pip_dependencies
                ).save_model(self.logger, output_dir)
            elif module == "lightgbm.basic" and name == "Booster":
                self.logger.info("Uploading lightgbm booster.")
                LightGBMModelPackager(
                    model, transformer, output_type, python_version,
                    additional_pip_dependencies
                ).save_model(
                    self.logger,
                    output_dir,
                    additional_modules=additional_modules
                )
            elif module == "lightgbm.sklearn" and name == "LGBMClassifier":
                self.logger.info("Uploading lightgbm classifier.")
                if output_type != "classification":
                    raise ValueError(
                        f"LGBMClassifier expected for classification model, found {output_type}."
                    )
                LightGBMModelPackager(
                    model, transformer, output_type, python_version,
                    additional_pip_dependencies
                ).save_model(
                    self.logger,
                    output_dir,
                    additional_modules=additional_modules
                )
            elif module == "lightgbm.sklearn" and name == "LGBMRegressor":
                self.logger.info("Uploading lightgbm regressor.")
                if output_type != "regression":
                    raise ValueError(
                        f"LGBMRegressor expected for regression model, found {output_type}."
                    )
                LightGBMModelPackager(
                    model, transformer, output_type, python_version,
                    additional_pip_dependencies
                ).save_model(
                    self.logger,
                    output_dir,
                    additional_modules=additional_modules
                )
            elif is_supported_pyspark_tree_model(model):
                self.logger.info("Uploading pyspark tree model.")
                if output_type not in name.lower():
                    raise ValueError(
                        f"Expected a {output_type} model, but provided a model of class {name}!"
                    )
                PySparkModelPackager(
                    model, transformer, output_type, python_version,
                    additional_pip_dependencies
                ).save_model(self.logger, output_dir)
            else:
                raise NotSupportedError(
                    f"Model of type: {module}.{name} is not supported. Serialize the model and use `add_packaged_python_model` to upload "
                )

    def schedule_ingestion(self, raw_json: str, cron_schedule: str):
        return self.scheduled_ingestion_client.schedule_new(
            json=raw_json,
            schedule=self.scheduled_ingestion_client.
            serialize_schedule(cron_schedule),
        )

    def get_scheduled_ingestion(self, workflow_id: str):
        return self.scheduled_ingestion_client.get(workflow_id)

    def _builds_scheduled_ingestion_request_tree_from_split(
        self,
        split_name,
        override_split_name: str = None,
        append: bool = False
    ):
        split_metadata = self.artifact_interaction_client.get_split_metadata(
            self._get_current_active_project_name(),
            self._get_current_active_data_collection_name(), split_name
        )
        materialize_operation_id = split_metadata["provenance"][
            "materialized_by_operation"]
        materialize_response = self.data_service_client.get_materialize_data_status(
            self.project.id, materialize_operation_id, throw_on_error=True
        )
        return self.scheduled_ingestion_client.build_request_tree(
            materialize_status_response=materialize_response,
            project_id=self.project.id,
            override_split_name=override_split_name,
            existing_split_id=split_metadata['id']
            if append and not override_split_name else None
        )

    def schedule_existing_data_split(
        self,
        split_name: str,
        cron_schedule: str,
        override_split_name: str = None,
        append: bool = True
    ):
        return self.scheduled_ingestion_client.schedule_new(
            tree=self._builds_scheduled_ingestion_request_tree_from_split(
                split_name, override_split_name, append=append
            ),
            schedule=self.scheduled_ingestion_client.
            serialize_schedule(cron_schedule),
        )

    def serialize_split(
        self,
        split_name: str,
        override_split_name: str = None,
        append: bool = True
    ) -> str:
        return MessageToJson(
            self._builds_scheduled_ingestion_request_tree_from_split(
                split_name, override_split_name, append=append
            )
        )

    def cancel_scheduled_ingestion(self, workflow_id: str) -> str:
        return self.scheduled_ingestion_client.cancel(workflow_id)

    def list_scheduled_ingestions(
        self, last_key: Optional[str] = None, limit: int = 50
    ) -> str:
        self._ensure_project()
        self._ensure_data_collection()
        return self.scheduled_ingestion_client.get_workflows(
            self.project.id,
            self.data_collection.id,
            last_key=last_key,
            limit=limit,
        )

    def _get_feature_transform_type_for_data_collection(
        self, data_collection_name: Optional[str] = None
    ):
        if not data_collection_name:
            data_collection_name = self.data_collection.name
        dc_metadata = self.project.get_data_collection_metadata(
            data_collection_name, as_json=False
        )
        return dc_metadata.feature_transform_type

    def list_monitoring_tables(self) -> str:
        return MessageToJson(
            self.monitoring_control_plane_client.list_druid_tables(
                project_id=self.project.id
            )
        )
