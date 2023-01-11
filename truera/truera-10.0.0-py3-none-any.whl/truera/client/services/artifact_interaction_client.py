from __future__ import annotations

from dataclasses import dataclass
import datetime
import json
import logging
import os
from pathlib import Path
import random
from typing import (
    Any, List, Mapping, Optional, Sequence, Type, TYPE_CHECKING, Union
)
import uuid

from google.protobuf.json_format import MessageToDict
import yaml

import truera
from truera.artifactrepo.utils.filter_utils import \
    parse_expression_to_filter_proto
import truera.client.cli.cli_utils as cli_utils
from truera.client.client_utils import InvalidArgumentCombinationException
from truera.client.client_utils import TextExtractorParams
from truera.client.client_utils import validate_add_model_metadata
import truera.client.client_utils as client_utils
from truera.client.column_info import ColumnInfo
from truera.client.column_info import create_materialized_output_file
from truera.client.column_info import CreateCacheInfo
from truera.client.data_source_utils import DATA_SOURCE_NAME_TO_DATA_KIND
from truera.client.errors import MetadataNotFoundException
from truera.client.errors import NotFoundError
from truera.client.errors import SimpleException
from truera.client.errors import TruException
from truera.client.public.communicator.http_communicator import \
    AlreadyExistsError
import truera.client.services.artifactrepo_client as ar_client
import truera.client.services.data_service_client as ds_client
from truera.client.util.data_split.base_data_split_path_container import \
    BaseDataSplitPathContainer
from truera.protobuf.public import metadata_message_types_pb2 as md_pb
from truera.protobuf.public.common.data_kind_pb2 import \
    DataKindDescribed  # pylint: disable=no-name-in-module
from truera.protobuf.public.data_service import \
    data_service_messages_pb2 as ds_messages_pb
from truera.protobuf.public.qoi_pb2 import \
    ExplanationAlgorithmType  # pylint: disable=no-name-in-module
from truera.protobuf.public.util import split_mode_pb2 as sm_pb
from truera.protobuf.public.util.time_range_pb2 import \
    TimeRange  # pylint: disable=no-name-in-module
from truera.utils.datetime_util import datetime_helper

if TYPE_CHECKING:
    from truera.client.truera_workspace import RemoteTrueraWorkspace
    from truera.client.truera_workspace import TrueraWorkspace

#############################################################################################################
# The cli uses the interaction client to create projects, models, data_collections, and splits. See Tru.py. #
#############################################################################################################


class SplitTooLargeError(SimpleException):
    pass


class InvalidModelFolderException(SimpleException):
    pass


class MissingParameterException(SimpleException):
    pass


class InvalidColumnInfoFileException(SimpleException):
    pass


class RowsetNotPersistableException(SimpleException):
    pass


class InvalidCredentialCombinationException(TruException):
    pass


class InvalidFilterError(SimpleException):
    pass


class _SourceDataLocator(object):

    def __init__(
        self,
        base_path: str,
        *,
        pre_transform_path: Optional[str] = None,
        post_transform_path: Optional[str] = None,
        labels_path: Optional[str] = None,
        extra_data_path: Optional[str] = None,
        split_dir: Optional[str] = None,
        data_split_loader_wrapper_path: Optional[str] = None,
        split_mode: sm_pb.SplitMode
    ):
        self.base_path = base_path

        # to_upload is a set so that the paths can be duplicates without appending all the data to the repo file twice
        self.to_upload = set()
        self.pre_transform_file: str = None
        self.post_transform_file: str = None
        self.labels_file: str = None
        self.extra_data_file: str = None

        self._repo_base_path: str = None

        self._repo_pre_transform_path: str = None
        self._repo_post_transform_path: str = None
        self._repo_labels_path: str = None
        self._repo_extra_data_path: str = None

        # For NN split
        self.split_dir = None

        if split_mode == sm_pb.SplitMode.SPLIT_MODE_DATA_REQUIRED:
            if not pre_transform_path:
                raise ValueError(
                    f"`pre_transform_path` is required for this configuration."
                )
        elif split_mode == sm_pb.SplitMode.SPLIT_MODE_NON_TABULAR:
            if not pre_transform_path and not split_dir:
                raise ValueError(
                    f"`pre_transform_path` or `split_dir` must be provided for this configuration."
                )
        elif split_mode == sm_pb.SplitMode.SPLIT_MODE_PREDS_REQUIRED:
            if not labels_path:
                raise ValueError(
                    f"`labels_path` is required for this configuration."
                )

        if pre_transform_path:
            self.pre_transform_file = self._get_file_name_from_path(
                pre_transform_path
            )
            self.to_upload.add(os.path.join(base_path, pre_transform_path))
        if split_dir:
            self.split_dir = split_dir
            self.data_split_loader_wrapper_file = self._get_file_name_from_path(
                data_split_loader_wrapper_path
            )
            self.to_upload.add(
                os.path.join(base_path, data_split_loader_wrapper_path)
            )
        if post_transform_path:
            self.post_transform_file = self._get_file_name_from_path(
                post_transform_path
            )
            self.to_upload.add(os.path.join(base_path, post_transform_path))
        if labels_path:
            self.labels_file = self._get_file_name_from_path(labels_path)
            self.to_upload.add(os.path.join(base_path, labels_path))
        if extra_data_path:
            self.extra_data_file = self._get_file_name_from_path(
                extra_data_path
            )
            self.to_upload.add(os.path.join(base_path, extra_data_path))

    def _add_base_path(self, data_collection_repo_path: str):
        self._repo_base_path = data_collection_repo_path

        if self.pre_transform_file:
            self._repo_pre_transform_path = os.path.join(
                self._repo_base_path, self.pre_transform_file
            )
        elif self.split_dir:
            self._repo_pre_transform_path = self._repo_base_path
        if self.post_transform_file:
            self._repo_post_transform_path = os.path.join(
                self._repo_base_path, self.post_transform_file
            )
        if self.labels_file:
            self._repo_labels_path = os.path.join(
                self._repo_base_path, self.labels_file
            )
        if self.extra_data_file:
            self._repo_extra_data_path = os.path.join(
                self._repo_base_path, self.extra_data_file
            )

    def _get_repo_paths(self, data_collection_repo_path: str):
        if not self._repo_base_path:
            self._add_base_path(data_collection_repo_path)

        return self._repo_pre_transform_path, self._repo_post_transform_path, self._repo_labels_path, self._repo_extra_data_path

    def _get_file_name_from_path(self, path: str):
        head, tail = os.path.split(path)
        return tail or os.path.basename(head)


class DataSplit(object):

    def __init__(
        self,
        split_name: str,
        split_type: cli_utils.SplitType,
        split_locator: _SourceDataLocator,
        *,
        split_time_range_begin: Optional[str] = None,
        split_time_range_end: Optional[str] = None,
        split_mode: sm_pb.SplitMode
    ):
        self.split_name = split_name
        self.split_type = str(split_type.name)
        self.split_locator = split_locator
        self.artifact_repo_location = None
        self.split_time_range_begin = split_time_range_begin
        self.split_time_range_end = split_time_range_end

        if split_mode == sm_pb.SplitMode.SPLIT_MODE_INVALID:
            raise ValueError(
                f"Valid `split_mode` must be provided for data split {split_name}"
            )

        self.split_mode = split_mode

    def get_repo_paths(self):
        return self.split_locator._get_repo_paths(self.artifact_repo_location)

    def files_to_upload(self):
        yield from self.split_locator.to_upload


@dataclass
class DataCollectionContainer:
    name: str
    id: str


class DataCollection(object):

    def __init__(
        self, data_collection_name: str,
        feature_transform_type: md_pb.FeatureTransformationType
    ):
        self.data_collection_name = data_collection_name
        self.feature_transform_type = feature_transform_type
        self.splits = []

    def AddSplit(self, split: DataSplit):
        self.splits.append(split)

    def create_data_split(
        self,
        split_name: str,
        split_type: cli_utils.SplitType,
        *,
        source_base_path: Optional[str] = "",
        pre_transform_path: Optional[str] = None,
        post_transform_path: Optional[str] = None,
        labels_path: Optional[str] = None,
        extra_data_path: Optional[str] = None,
        split_time_range_begin: Optional[Union[str, float,
                                               datetime.datetime]] = None,
        split_time_range_end: Optional[Union[str, float,
                                             datetime.datetime]] = None,
        split_dir: Optional[str] = None,
        data_split_loader_wrapper_path: Optional[str] = None,
        split_mode: sm_pb.SplitMode
    ):
        source_locator = _SourceDataLocator(
            source_base_path,
            pre_transform_path=pre_transform_path,
            post_transform_path=post_transform_path,
            labels_path=labels_path,
            extra_data_path=extra_data_path,
            split_dir=split_dir,
            data_split_loader_wrapper_path=data_split_loader_wrapper_path,
            split_mode=split_mode
        )
        split = DataSplit(
            split_name,
            split_type,
            source_locator,
            split_time_range_begin=datetime_helper.
            create_datetime_str(split_time_range_begin),
            split_time_range_end=datetime_helper.
            create_datetime_str(split_time_range_end),
            split_mode=split_mode
        )
        self.AddSplit(split)

    def upload(self, client: ArtifactInteractionClient, project_id: str) -> str:
        client._upload_data_collection_to_ar(project_id, self)
        return client._upload_data_collection_to_mr(project_id, self)

    def upload_new_split(
        self, client: ArtifactInteractionClient, project_id: str
    ):
        files_uploaded = client._upload_data_collection_to_ar(project_id, self)
        client._add_datasplits_only_to_mr(project_id, self)
        return files_uploaded


class Model(object):

    def __init__(
        self,
        model_id: str,
        model_name: str,
        project_id: str,
        model_type: cli_utils.ModelType,
        model_output_type: str,
        local_model_path: str,
        data_collection_name: str,
        extra_data_path: Optional[str] = None,
        train_split_id: Optional[str] = None,
        train_parameters: Optional[Mapping[str, Any]] = None
    ):
        self.model_id = model_id
        self.model_name = model_name
        self.project_id = project_id
        self.model_type = str(model_type.name)
        self.model_output_type = str(model_output_type)
        self.model_path = local_model_path
        self.data_collection_name = data_collection_name
        self.extra_data_path = extra_data_path
        self.training_metadata = md_pb.ModelTrainingMetadata(
            train_split_id=train_split_id
        )
        if train_parameters:
            self.training_metadata.parameters.update(train_parameters)  # pylint: disable=no-member

    def upload_model_object(self, client: ArtifactInteractionClient) -> str:
        return client._upload_model_to_ar(self.project_id, self)

    def upgrade_virtual(
        self, client: ArtifactInteractionClient,
        new_model_type: cli_utils.ModelType, local_model_obj_path: str
    ):
        if self.model_type != str(cli_utils.ModelType.Virtual.name):
            raise ValueError("Model is not virtual!")
        self.model_type = str(new_model_type.name)
        self.model_path = local_model_obj_path
        artifact_repo_model_path = self.upload_model_object(client)
        client._upgrade_virtual_model_in_mr(self, artifact_repo_model_path)

    def upload(self, client: ArtifactInteractionClient):
        artifact_repo_model_path = ""
        if self.model_type != str(cli_utils.ModelType.Virtual.name):
            artifact_repo_model_path = self.upload_model_object(client)
        self.model_id = client._upload_model_to_mr(
            self,
            artifact_repo_model_path,
            data_collection_name=self.data_collection_name
        )

    def get_extra_files_to_upload(self):
        if not self.extra_data_path:
            return []
        return [self.extra_data_path]


class Project(object):

    def __init__(
        self,
        project_name: str,
        artifact_interaction_client: ArtifactInteractionClient,
        *,
        project_id: Optional[str] = None,
        score_type: Optional[str] = None,
        input_type: Optional[str] = None
    ):
        self.name = project_name
        self.id = project_id
        self.client = artifact_interaction_client
        self.score_type = score_type
        self.input_type = input_type

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def get_model(self, model_name: str, data_collection_name: str) -> Model:
        model_meta = self.client.get_model_metadata(
            self.name, model_name=model_name
        )
        return Model(
            model_id=model_meta["id"],
            model_name=model_meta["name"],
            project_id=self.name,
            model_type=cli_utils._map_model_type(model_meta["model_type"]),
            model_output_type=model_meta["model_output_type"],
            local_model_path=model_meta["locator"],
            data_collection_name=data_collection_name
        )

    def create_model(
        self,
        model_name: str,
        model_type: cli_utils.ModelType,
        model_output_type: str,
        local_model_path: str,
        *,
        data_collection_name: str,
        extra_data_path: Optional[str] = None,
        train_split_name: Optional[str] = None,
        train_parameters: Optional[Mapping[str, Any]] = None
    ) -> Model:
        if train_split_name:
            train_split_id = self.client.get_split_metadata(
                self.name, data_collection_name, train_split_name
            )["id"]
        else:
            train_split_id = None
        return Model(
            model_id=model_name,
            model_name=model_name,
            project_id=self.id,
            model_type=model_type,
            model_output_type=model_output_type,
            local_model_path=local_model_path,
            data_collection_name=data_collection_name,
            extra_data_path=extra_data_path,
            train_split_id=train_split_id,
            train_parameters=train_parameters
        )

    def create_data_collection(
        self, data_collection_name: str,
        feature_transform_type: md_pb.FeatureTransformationType
    ):
        return DataCollection(
            data_collection_name=data_collection_name,
            feature_transform_type=feature_transform_type
        )

    def create_prediction_cache(
        self,
        model_name: str,
        data_collection_name: str,
        split_name: str,
        cache_location: str,
        score_type: str,
        model_output_type: str,
        client_name: str,
        client_version: str,
        row_count: Optional[int] = None
    ):
        if row_count is None:
            with open(cache_location, 'r') as f:
                # Assumes that there is a header
                row_count = max(0, len(f.readlines()) - 1)

        # data_collection_name should be changed to data_collection_id as part of AB#2708
        return Cache(
            cache_type=md_pb.CacheType.MODEL_PREDICTION_CACHE,
            project_id=self.id,
            model_name=model_name,
            data_collection_name=data_collection_name,
            split_name=split_name,
            cache_location=cache_location,
            score_type=score_type,
            model_output_type=model_output_type,
            row_count=row_count,
            client_name=client_name,
            client_version=client_version
        )

    def create_explanation_cache(
        self, model_id: str, data_collection_name: str, split_id: str, *,
        cache_location: str, score_type: str, model_output_type: str,
        explanation_algorithm_type: ExplanationAlgorithmType, client_name: str,
        client_version: str
    ):
        with open(cache_location, 'r') as f:
            # Assumes that there is a header
            row_count = max(0, len(f.readlines()) - 1)

        # data_collection_name should be changed to data_collection_id as part of AB#2708
        return Cache(
            cache_type=md_pb.CacheType.EXPLANATION_CACHE,
            project_id=self.id,
            model_name=model_id,
            data_collection_name=data_collection_name,
            split_name=split_id,
            cache_location=cache_location,
            score_type=score_type,
            model_output_type=model_output_type,
            row_count=row_count,
            client_name=client_name,
            client_version=client_version,
            explanation_algorithm_type=explanation_algorithm_type
        )

    def exists(self):
        return self.client.project_exists(self.id)

    def data_collection_exists(self, data_collection_name: str):
        return self.client.data_collection_exists(self.id, data_collection_name)

    def get_data_collection_id(self, data_collection_name: str):
        return self.client.get_data_collection_id(self.id, data_collection_name)

    def get_data_collection_metadata(
        self, data_collection_name: str, as_json: bool = True
    ):
        return self.client.get_data_collection_metadata(
            self.name, data_collection_name, as_json
        )


class Cache(object):

    def __init__(
        self,
        *,
        cache_type: md_pb.CacheType,
        project_id: str,
        model_name: str,
        data_collection_name: str,
        split_name: str,
        cache_location: str,
        score_type: str,
        model_output_type: str,
        row_count: int,
        client_name: str,
        client_version: str,
        background_data_split_name: Optional[str] = None,
        explanation_algorithm_type: Optional[ExplanationAlgorithmType] = None
    ):
        self.cache_type = cache_type
        self.project_id = project_id
        self.model_name = model_name
        self.data_collection_name = data_collection_name
        self.split_name = split_name
        self.cache_location = cache_location
        self.score_type = score_type
        self.model_output_type = model_output_type
        self.row_count = row_count
        self.client_name = client_name
        self.client_version = client_version
        self.background_data_split_name = background_data_split_name
        self.explanation_algorithm_type = explanation_algorithm_type

    def upload(
        self,
        client: ArtifactInteractionClient,
        create_model: bool = False,
        overwrite: bool = False
    ):
        cache_name_suffix = "_prediction_cache" if self.cache_type == md_pb.CacheType.MODEL_PREDICTION_CACHE \
                                                else "_explanation_cache"
        if self.explanation_algorithm_type is not None:
            # pylint: disable=protobuf-enum-value
            cache_name_suffix += f"_{ExplanationAlgorithmType.Name(self.explanation_algorithm_type)}"

        try:
            model = client.ar_client.get_model_metadata(
                self.project_id, model_name=self.model_name
            )
            self.model_id = model.id
        except NotFoundError:
            self.model_id = None

        file_name = os.path.basename(self.cache_location)
        ext = os.path.splitext(file_name)[-1]
        if not file_name:
            self.format = 'DIR'
        else:
            if 'csv' in ext.lower():
                self.format = 'CSV'
            elif 'arrow' in ext.lower():
                self.format = 'ARROW'
            elif 'txtproto' in ext.lower():
                self.format = "PROTO"
            else:
                raise ValueError("Invalid cache file extension: " + ext.lower())

        if not self.model_id and create_model:
            # Create a virtual model in the metadata
            # TODO(Chris): addition is not rolled back if model was created but rest of the command failed
            model = Model(
                model_id=self.model_name,
                model_name=self.model_name,
                project_id=self.project_id,
                model_type=cli_utils.ModelType.Virtual,
                model_output_type=self.model_output_type,
                local_model_path="",
                data_collection_name=self.data_collection_name
            )
            self.model_id = client._upload_model_to_mr(
                model,
                "",
                data_collection_name=self.data_collection_name,
                insert_only=not overwrite
            )
        elif not self.model_id:
            raise ValueError(
                f"Provided MODEL NAME: {self.model_name} has not been created. \
                             Set create_model to add a virtual model"
            )

        artifact_repo_cache_path = client._upload_cache(
            project_id=self.project_id,
            model_id=self.model_id,
            data_collection_id=self.data_collection_name,
            data_split_id=self.split_name,
            background_data_split_name=self.background_data_split_name,
            explanation_algorithm_type=self.explanation_algorithm_type,
            score_type=self.score_type,
            cache_type=self.cache_type,
            path=self.cache_location,
            name=f"{self.model_name}__{self.split_name}__{cache_name_suffix}"
        )

        artifact_repo_cache_path = artifact_repo_cache_path.rstrip("/")
        artifact_repo_cache_path += f"/{file_name}"
        self.cache_id = client._upload_cache_to_mr(
            self, artifact_repo_cache_path
        )


@dataclass
class OutputSplitInfo:
    project_id: str
    data_collection_id: str
    split_name: str
    split_type: str
    split_time_range_begin: str = None
    split_time_range_end: str = None


@dataclass
class ModelInfoForCache:
    project_id: str
    model_name: str
    score_type: str


@dataclass
class RowsetIdentifierInfo:
    rowset_id: str
    data_source_name: str
    project_id: str

    def get_rowset_id(self, artifact_interaction_client) -> str:
        if self.rowset_id:
            return self.rowset_id
        if not self.data_source_name:
            raise MissingParameterException(
                "Neither rowset id nor data source name were provided."
            )
        return artifact_interaction_client.get_root_rowset_by_name(
            self.project_id, self.data_source_name
        )


@dataclass
class CreateDataSplitColumnSpec:
    label_col: str = None
    id_col: str = None
    prediction_col: str = None
    pre_data_additional_skip_cols: List[str] = None
    column_spec_file: str = None
    all_columns_pre: bool = False
    timestamp_col: str = None

    def get_column_info(self, logger):
        if self.column_spec_file:
            return build_column_info_from_file(self.column_spec_file)
        # If no column spec file is specified, we can only handle pre data.
        elif self.label_col or self.id_col or self.prediction_col or self.pre_data_additional_skip_cols or self.timestamp_col:
            # id_col and timestamp_col are treated as system columns internally, they will be stored along with data
            # but will not be part of model input.
            columns_to_skip = [
                col for col in [
                    self.label_col, self.id_col, self.prediction_col, self.
                    timestamp_col, *(self.pre_data_additional_skip_cols or [])
                ] if col is not None
            ]
            return ColumnInfo(
                pre_skip=columns_to_skip,
                label=self.label_col,
                prediction=self.prediction_col,
                id_column=self.id_col,
                timestamp_column=self.timestamp_col
            )
        elif self.all_columns_pre:
            logger.warning(
                "Warning: Materializing split from all available columns"
            )
            return ColumnInfo(pre_skip=[])
        else:
            raise MissingParameterException(
                "Either label column, prediction column, column spec file, or all_pre flag must be specified."
            )


@dataclass
class OutputSpec:
    approx_row_count: int
    sample_kind: str
    seed: int = None


class ArtifactInteractionClient(object):

    def __init__(
        self,
        ar_client: ar_client.ArtifactRepoClient,
        ds_client: ds_client.DataServiceClient,
        logger=None
    ):
        self.logger = logger or logging.getLogger(__name__)
        self.ar_client = ar_client
        self.data_service_client = ds_client

        self.split_max_size = cli_utils.get_split_max_size()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.ar_client.close()
        self.data_service_client.close()

    def create_project(
        self,
        project_name: str,
        score_type: str,
        *,
        description_json: str = None,
        input_data_format: str = "tabular"
    ) -> Project:
        project_id = self.ar_client.create_project(
            project_name, description_json, score_type, input_data_format
        )
        return Project(
            project_name,
            self,
            project_id=project_id,
            score_type=score_type,
            input_type=input_data_format
        )

    def _upload_model_to_ar(self, project_id: str, model: Model):
        model_name = model.model_name
        src_model_path = model.model_path
        extra_files_to_upload = model.get_extra_files_to_upload()
        if not os.path.isdir(src_model_path):
            raise InvalidModelFolderException(
                f"The provided path {src_model_path} is not a directory. Please use the '> tru package' command to package the model."
            )

        # An NN model will upload additional wrapper files.
        # Future packaging work on NN may end up using MLModel files,
        # but until then, this is a simple way to skip the MLModel requirement.
        # Tracked in AB#3556
        model_is_nn_model = bool(extra_files_to_upload)
        if not model_is_nn_model and not os.path.isfile(
            os.path.join(src_model_path, "MLmodel")
        ):
            raise InvalidModelFolderException(
                f"The provided path: {src_model_path} does not contain a MLModel file. Please use the '> tru package' command to package the model."
            )
        return self.ar_client.upload_artifact(
            src_model_path,
            project_id,
            ar_client.ArtifactType.model,
            model_name,
            "", [],
            list_of_src_files_or_dirs=extra_files_to_upload,
            stream=True
        )

    def upload_data_source_file(
        self,
        project_id: str,
        file_path: str,
        name: str,
        text_extractor_params: TextExtractorParams,
        *,
        user_requested: bool = True,
        data_collection_id: str = None,
        data_kind: DataKindDescribed = DataKindDescribed.DATA_KIND_ALL
    ):
        if not os.path.isfile(file_path):
            raise ValueError(
                "Provided path {} does not refer to a single file.".
                format(file_path)
            )

        uri = self.ar_client.upload_artifact(
            file_path, project_id, ar_client.ArtifactType.data_source, name or
            str(uuid.uuid4()), "", []
        )
        rowset_id, _ = self.data_service_client.load_data_source_local(
            project_id,
            uri,
            text_extractor_params.to_format_pb(),
            name=name,
            creation_reason=ds_messages_pb.CreationReason.DS_CR_USER_REQUESTED
            if user_requested else
            ds_messages_pb.CreationReason.DS_CR_SYSTEM_REQUESTED,
            data_collection_id=data_collection_id,
            data_kind=data_kind
        )
        return rowset_id

    def _upload_cache(
        self, *, project_id: str, model_id: str, data_collection_id: str,
        data_split_id: str, background_data_split_name: str,
        explanation_algorithm_type: Optional[ExplanationAlgorithmType],
        score_type: str, cache_type: md_pb.CacheType, path: str, name: str
    ):
        scoping_ids = [
            model_id,
            data_collection_id,
            data_split_id,
            score_type,
        ]
        if cache_type == md_pb.CacheType.MODEL_PREDICTION_CACHE:
            scoping_ids = ["prediction_caches"] + scoping_ids
        elif cache_type == md_pb.CacheType.PARTIAL_DEPENDENCE_PLOT_CACHE:
            scoping_ids = ["partial_dependency_caches"
                          ] + scoping_ids + [background_data_split_name or ""]
        elif cache_type == md_pb.CacheType.EXPLANATION_CACHE:
            scoping_ids = ["explanation_caches"] + scoping_ids + [
                background_data_split_name or "",
                ExplanationAlgorithmType.Name(explanation_algorithm_type)
            ]
        return self.ar_client.upload_artifact(
            path,
            project_id,
            ar_client.ArtifactType.cache,
            name,
            "",
            scoping_ids,
            stream=True
        )

    def _upload_cache_to_mr(self, cache: Cache, ar_cache_location: str):
        return self.ar_client.create_cache_metadata(
            cache_type=cache.cache_type,
            project_id=cache.project_id,
            model_id=cache.model_id,
            data_collection_name=cache.data_collection_name,
            split_name=cache.split_name,
            location=ar_cache_location,
            format=cache.format,
            score_type=cache.score_type,
            row_count=cache.row_count,
            client_name=cache.client_name,
            client_version=cache.client_version,
            background_data_split_name=cache.background_data_split_name,
            explanation_algorithm_type=cache.explanation_algorithm_type
        )

    def add_wasb_data_source(
        self,
        project_id,
        uri,
        account_key,
        data_source_credential_id,
        name,
        text_extractor_params: TextExtractorParams,
        *,
        user_requested=True,
        data_kind: DataKindDescribed = DataKindDescribed.DATA_KIND_ALL
    ):
        rowset_id, _ = self.data_service_client.load_data_source_wasb_blob(
            project_id,
            uri,
            text_extractor_params.to_format_pb(),
            account_key=account_key,
            credential_id=data_source_credential_id,
            name=name,
            creation_reason=ds_messages_pb.CreationReason.DS_CR_USER_REQUESTED
            if user_requested else
            ds_messages_pb.CreationReason.DS_CR_SYSTEM_REQUESTED,
            data_kind=data_kind
        )
        return rowset_id

    def add_s3_bucket_data_source(
        self,
        project_id,
        uri,
        access_key_id,
        secret_access_key,
        data_source_credential_id,
        name,
        text_extractor_params: TextExtractorParams,
        *,
        user_requested=True,
        data_kind: DataKindDescribed = DataKindDescribed.DATA_KIND_ALL,
        file_time_range: TimeRange = None
    ):
        rowset_id, _ = self.data_service_client.load_data_source_s3_bucket(
            project_id,
            uri,
            text_extractor_params.to_format_pb(),
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            credential_id=data_source_credential_id,
            name=name,
            creation_reason=ds_messages_pb.CreationReason.DS_CR_USER_REQUESTED
            if user_requested else
            ds_messages_pb.CreationReason.DS_CR_SYSTEM_REQUESTED,
            data_kind=data_kind,
            file_time_range=file_time_range
        )
        return rowset_id

    def add_data_source_cred(
        self, project_id, credential_name, identity, secret
    ):
        credential_metadata = ds_messages_pb.CredentialMetadata(
            name=credential_name
        )
        credential_metadata.projects_with_access.append(project_id)
        cred = ds_messages_pb.Credentials(
            identity=identity, secret=secret, metadata=credential_metadata
        )

        return self.data_service_client.put_secret_cred(cred)

    def add_mysql_db_data_source(
        self,
        project_id,
        uri,
        database_name,
        table_name,
        username,
        password,
        data_source_credential_id,
        name,
        *,
        user_requested=True,
        columns=[],
        data_kind: DataKindDescribed = DataKindDescribed.DATA_KIND_ALL
    ):
        rowset_id, _ = self.data_service_client.load_data_source_mysql_table(
            project_id,
            uri,
            database_name,
            table_name,
            username=username,
            password=password,
            credential_id=data_source_credential_id,
            name=name,
            creation_reason=ds_messages_pb.CreationReason.DS_CR_USER_REQUESTED
            if user_requested else
            ds_messages_pb.CreationReason.DS_CR_SYSTEM_REQUESTED,
            columns=columns,
            data_kind=data_kind
        )

        return rowset_id

    def add_hive_data_source(
        self,
        project_id,
        uri,
        database_name,
        table_name,
        username,
        password,
        data_source_credential_id,
        name,
        *,
        user_requested=True,
        data_kind: DataKindDescribed = DataKindDescribed.DATA_KIND_ALL
    ):
        rowset_id, _ = self.data_service_client.load_data_source_hive_table(
            project_id,
            uri,
            database_name,
            table_name,
            username=username,
            password=password,
            credential_id=data_source_credential_id,
            name=name,
            creation_reason=ds_messages_pb.CreationReason.DS_CR_USER_REQUESTED
            if user_requested else
            ds_messages_pb.CreationReason.DS_CR_SYSTEM_REQUESTED,
            data_kind=data_kind
        )

        return rowset_id

    def add_bigquery_data_source(
        self,
        project_id: str,
        database_name: str,
        table_name: str,
        password: str,
        name: str,
        *,
        credential_id: str = None,
        user_requested: bool = True,
        columns=[],
        data_kind: DataKindDescribed = DataKindDescribed.DATA_KIND_ALL
    ):
        rowset_id, _ = self.data_service_client.load_data_source_big_query_table(
            project_id,
            database_name,
            table_name,
            password=password,
            credential_id=credential_id,
            name=name,
            creation_reason=(
                ds_messages_pb.CreationReason.DS_CR_USER_REQUESTED
                if user_requested else
                ds_messages_pb.CreationReason.DS_CR_SYSTEM_REQUESTED
            ),
            columns=columns,
            data_kind=data_kind
        )

        return rowset_id

    def add_jdbc_data_source(
        self,
        project_id,
        uri,
        database_name,
        table_name,
        username,
        password,
        data_source_credential_id,
        name,
        *,
        user_requested=True,
        columns=[],
        data_kind: DataKindDescribed = DataKindDescribed.DATA_KIND_ALL
    ):
        rowset_id, _ = self.data_service_client.load_data_source_jdbc(
            project_id,
            uri,
            database_name,
            table_name,
            username=username,
            password=password,
            credential_id=data_source_credential_id,
            name=name,
            creation_reason=ds_messages_pb.CreationReason.DS_CR_USER_REQUESTED
            if user_requested else
            ds_messages_pb.CreationReason.DS_CR_SYSTEM_REQUESTED,
            columns=columns,
            data_kind=data_kind
        )
        return rowset_id

    def check_only_one_cred_provided(
        self, username, password, data_source_credential_id
    ):
        if data_source_credential_id and (username or password):
            raise InvalidCredentialCombinationException(
                "Both credential id and username / password provided."
            )

    def check_credential_id_exists(self, project_id, data_source_credential_id):
        metadata = self.get_data_source_credential_metadata(
            project_id, data_source_credential_id
        )
        if not metadata:
            raise MetadataNotFoundException(
                f"Could not find metadata related to credential {data_source_credential_id}"
            )

    def get_data_source_credential_metadata(
        self, project_id, data_source_credential_id
    ):
        return self.ar_client.get_credential_metadata(
            project_id, data_source_credential_id
        )

    def create_data_split_via_data_service(
        self,
        project_id: str,
        data_collection_id: str,
        split_name: str,
        split_type: str,
        data_split_params: Type[BaseDataSplitPathContainer],
        id_col,
        *,
        timestamp_col: Optional[str] = None,
        split_time_range_begin: Optional[str] = None,
        split_time_range_end: Optional[str] = None,
        split_mode: sm_pb.SplitMode = sm_pb.SplitMode.SPLIT_MODE_DATA_REQUIRED,
        materialize_approx_max_rows: Optional[int] = 5000,
        background_split_id: Optional[str] = None,
        model_id: Optional[str] = None,
        score_type: Optional[str] = None,
        influence_type: Optional[str] = None
    ):

        @dataclass
        class RowsetFromInputFile:
            path: str
            typ: str
            rowset_id: str

        upload_list = data_split_params.get_valid_data_sources()
        rowsets_from_inputs = [
            RowsetFromInputFile(
                path, typ,
                self.upload_data_source_file(
                    project_id,
                    path,
                    None,
                    params,
                    user_requested=False,
                    data_collection_id=data_collection_id,
                    data_kind=DATA_SOURCE_NAME_TO_DATA_KIND[typ]
                )
            ) for path, typ, params in upload_list
        ]

        joined_rowset = self.data_service_client.join_rowsets(
            [ipt.rowset_id for ipt in rowsets_from_inputs], [id_col]
        )

        output_files = self._generate_output_files_from_joins(
            rowsets_from_inputs
        )

        fi_included = False
        prediction_included = False
        for rowset in rowsets_from_inputs:
            if rowset.typ == "feature_influence":
                fi_included = True
            if rowset.typ == "prediction":
                prediction_included = True

        cache_info = None
        if fi_included or prediction_included:
            if fi_included and not background_split_id:
                raise ValueError(
                    "Must provide background split for Feature Influence Data."
                )
            cache_info = CreateCacheInfo(
                model_id,
                score_type=score_type,
                background_split_id=background_split_id,
                explanation_algorithm_type=influence_type
            ).build_create_cache_info()

        materialize_op = self.data_service_client.materialize_data(
            project_id,
            joined_rowset,
            data_collection_id,
            materialize_approx_max_rows,
            "RANDOM",
            random.randint(0, 64 * 1024),
            split_name,
            split_type,
            outputFiles=output_files,
            id_column=id_col,
            timestamp_column=timestamp_col,
            uniquified_columns_expected=True,
            split_time_range_begin=split_time_range_begin,
            split_time_range_end=split_time_range_end,
            split_mode=split_mode,
            cache_info=cache_info
        )

        status_lambda = lambda: self.get_materialize_operation_status(
            project_id=project_id, operation_id=materialize_op
        )
        client_utils.wait_for_status(
            self.logger,
            status_lambda=status_lambda,
            success_state="OK",
            running_states=["RUNNING"],
            failed_state="FAILED",
            timeout_seconds=300,
            error_on_timeout=True,
            wait_duration_in_seconds=2
        )

        status = self.data_service_client.get_materialize_data_status(
            project_id, materialize_op
        )

        return status.output_split_id

    def _generate_output_files_from_joins(self, join_inputs):
        projection_list = []
        for rowset_from_input in join_inputs:
            if rowset_from_input.typ == "pre":
                projection_list.append(
                    create_materialized_output_file(
                        ds_messages_pb.MaterializedOutputFile.
                        MaterializedFileType.MFT_PRETRANSFORM,
                        upstream_input_rowset_id=rowset_from_input.rowset_id
                    )
                )
            if rowset_from_input.typ == "post":
                projection_list.append(
                    create_materialized_output_file(
                        ds_messages_pb.MaterializedOutputFile.
                        MaterializedFileType.MFT_POSTTRANSFORM,
                        upstream_input_rowset_id=rowset_from_input.rowset_id
                    )
                )
            if rowset_from_input.typ == "extra":
                projection_list.append(
                    create_materialized_output_file(
                        ds_messages_pb.MaterializedOutputFile.
                        MaterializedFileType.MFT_EXTRA,
                        upstream_input_rowset_id=rowset_from_input.rowset_id
                    )
                )
            if rowset_from_input.typ == "label":
                projection_list.append(
                    create_materialized_output_file(
                        ds_messages_pb.MaterializedOutputFile.
                        MaterializedFileType.MFT_LABEL,
                        upstream_input_rowset_id=rowset_from_input.rowset_id
                    )
                )
            if rowset_from_input.typ == "prediction":
                projection_list.append(
                    create_materialized_output_file(
                        ds_messages_pb.MaterializedOutputFile.
                        MaterializedFileType.MFT_PREDICTIONCACHE,
                        upstream_input_rowset_id=rowset_from_input.rowset_id
                    )
                )
            if rowset_from_input.typ == "feature_influence":
                projection_list.append(
                    create_materialized_output_file(
                        ds_messages_pb.MaterializedOutputFile.
                        MaterializedFileType.MFT_EXPLANATIONCACHE,
                        upstream_input_rowset_id=rowset_from_input.rowset_id
                    )
                )

        return projection_list

    def _upload_data_collection_to_ar(
        self, project_id: str, data_collection: DataCollection
    ):
        number_of_files_uploaded = 0
        for split in data_collection.splits:
            to_upload = split.files_to_upload()
            total_size = sum(
                [os.stat(p).st_size for p in split.files_to_upload()]
            )

            if total_size > self.split_max_size:
                raise SplitTooLargeError(
                    f"The total size of the provided files is too large: {total_size} bytes. The maximum allowed size is: {self.split_max_size} bytes."
                )
            split_dir = split.split_locator.split_dir
            if isinstance(split_dir, Path):
                split_dir = str(split_dir)
            if split_dir:
                split.artifact_repo_location = self.ar_client.upload_artifact(
                    split_dir,
                    project_id,
                    ar_client.ArtifactType.datasplit,
                    split.split_name,
                    "", [data_collection.data_collection_name],
                    list_of_src_files_or_dirs=to_upload,
                    stream=True
                )
                for (dir_path, _, file_names) in os.walk(split_dir):
                    number_of_files_uploaded += len(file_names)
            else:
                split.artifact_repo_location = self.ar_client.upload_artifact_list(
                    to_upload, project_id, ar_client.ArtifactType.datasplit,
                    split.split_name, "",
                    [data_collection.data_collection_name]
                )
                number_of_files_uploaded += len(list(split.files_to_upload()))

        return number_of_files_uploaded

    def _upgrade_virtual_model_in_mr(
        self,
        model: Model,
        artifact_repo_model_path: str,
    ):
        model_metadata = {
            "locator": artifact_repo_model_path,
            "model_type": model.model_type
        }
        self.ar_client.update_model_metadata(
            model.project_id, model.model_name, model_metadata
        )

    def _upload_model_to_mr(
        self,
        model: Model,
        artifact_repo_model_path: str,
        data_collection_name: Optional[str] = None,
        insert_only: Optional[bool] = True
    ):
        return self.ar_client.create_model_metadata(
            model_id=model.model_id,
            model_name=model.model_name,
            project_id=model.project_id,
            data_collection_name=data_collection_name,
            model_type=model.model_type,
            model_output_type=model.model_output_type,
            locator=artifact_repo_model_path,
            training_metadata=model.training_metadata,
            insert_only=insert_only
        )

    def _upload_data_collection_to_mr(
        self, project_id: str, data_collection: DataCollection
    ) -> str:
        data_collection_id = self.ar_client.create_data_collection(
            project_id, data_collection.data_collection_name,
            data_collection.feature_transform_type
        )
        for split in data_collection.splits:
            pre_transform, post_transform, label, extra = split.get_repo_paths()
            self.ar_client.create_split_metadata(
                split_name=split.split_name,
                project_id=project_id,
                data_collection_name=data_collection.data_collection_name,
                split_type=split.split_type,
                preprocessed_locator=pre_transform,
                processed_locator=post_transform,
                label_locator=label,
                extra_data_locator=extra,
                split_time_range_begin=split.split_time_range_begin,
                split_time_range_end=split.split_time_range_end,
                split_mode=split.split_mode
            )
        return data_collection_id

    def _add_datasplits_only_to_mr(
        self, project_id: str, data_collection: DataCollection
    ):
        for split in data_collection.splits:
            pre_transform, post_transform, label, extra = split.get_repo_paths()
            self.ar_client.create_split_metadata(
                split_name=split.split_name,
                project_id=project_id,
                data_collection_name=data_collection.data_collection_name,
                split_type=split.split_type,
                preprocessed_locator=pre_transform,
                processed_locator=post_transform,
                label_locator=label,
                extra_data_locator=extra,
                split_time_range_begin=split.split_time_range_begin,
                split_time_range_end=split.split_time_range_end,
                split_mode=split.split_mode
            )

    def ingest_delayed(
        self,
        project_name: str,
        data_source_name: str,
        rowset_id: str,
        data_collection_name: str,
        existing_split_name: str,
        *,
        pre_columns: Optional[Sequence[str]] = None,
        pre_skip_columns: Optional[Sequence[str]] = None,
        post_columns: Optional[Sequence[str]] = None,
        extra_columns: Optional[Sequence[str]] = None,
        label_column: Optional[str] = None,
        prediction_column: Optional[str] = None,
        feature_influence_columns: Optional[Sequence[str]] = None,
        id_column: Optional[str],
        timestamp_column: Optional[str] = None,
        model_info_for_cache: Optional[ModelInfoForCache] = None,
        background_split_id: Optional[str] = None,
        approx_row_count: int,
        seed: int,
        sample_strategy: str,
        influence_type: Optional[str] = None
    ):
        if data_source_name is None and rowset_id is None:
            raise InvalidArgumentCombinationException(
                "One of data_source_name or rowset_id need to be provided."
            )

        project_id = self.get_project_id(project_name)
        data_collection_id = self.get_data_collection_id(
            project_id, data_collection_name
        )
        existing_split_id = self.get_split_metadata(
            project_name, data_collection_name, existing_split_name
        )["id"]
        if rowset_id and data_source_name:
            self.logger.warning(
                f"Warning: both rowset id {rowset_id} and data source name {data_source_name} specified. Data source name will be ignored."
            )
        if not rowset_id:
            rowset_id = self.get_root_rowset_by_name(
                project_id, data_source_name
            )

        column_info = ColumnInfo(
            pre=pre_columns,
            pre_skip=pre_skip_columns,
            post=post_columns,
            extra=extra_columns,
            label=[label_column] if label_column is not None else None,
            id_column=[id_column],
            prediction=[prediction_column]
            if prediction_column is not None else None,
            feature_influences=feature_influence_columns,
        )
        create_cache_info = None
        if model_info_for_cache is not None:
            model_id = self.get_model_metadata(
                project_id, model_info_for_cache.model_name
            )["id"]
            create_cache_info = CreateCacheInfo(
                model_id=model_id,
                score_type=model_info_for_cache.score_type,
                background_split_id=background_split_id,
                explanation_algorithm_type=influence_type
            )
        return self.data_service_client.materialize_data(
            project_id,
            rowset_id,
            data_collection_id,
            approx_row_count,
            sample_strategy,
            seed,
            existing_split_id=existing_split_id,
            outputFiles=column_info.get_projections(),
            id_column=id_column,
            timestamp_column=timestamp_column,
            cache_info=create_cache_info.build_create_cache_info()
            if create_cache_info is not None else create_cache_info
        )

    def create_data_split_from_data_source(
        self, rowset_id_info: RowsetIdentifierInfo,
        output_split_info: OutputSplitInfo,
        model_info_for_cache: ModelInfoForCache,
        create_split_column_info: CreateDataSplitColumnSpec,
        output_spec: OutputSpec, split_mode: sm_pb.SplitMode
    ):
        column_info = None
        if create_split_column_info.label_col and create_split_column_info.column_spec_file:
            self.logger.warning(
                f"Warning: both label column \"{create_split_column_info.label_col}\" and column spec file \"{create_split_column_info.column_spec_file}\" specified. Ignoring label column."
            )

        if create_split_column_info.id_col and create_split_column_info.column_spec_file:
            self.logger.warning(
                f"Warning: both system ID column \"{create_split_column_info.id_col}\" and column spec file \"{create_split_column_info.column_spec_file}\" specified. Ignoring ID column."
            )

        if create_split_column_info.timestamp_col and create_split_column_info.column_spec_file:
            self.logger.warning(
                f"Warning: both timestamp column \"{create_split_column_info.timestamp_col}\" and column spec file \"{create_split_column_info.column_spec_file}\" specified. Ignoring timestamp column."
            )

        if rowset_id_info.rowset_id and rowset_id_info.data_source_name:
            self.logger.warning(
                f"Warning: both data source name \"{rowset_id_info.data_source_name}\" and rowset id \"{rowset_id_info.rowset_id}\" specified. Ignoring data source name."
            )

        column_info = create_split_column_info.get_column_info(self.logger)

        create_cache_info = None
        if column_info.includes_cache():
            if model_info_for_cache.model_name is None:
                raise MissingParameterException(
                    "Model name must be provided when materializing prediction caches"
                )
            model_id = self.get_model_metadata(
                model_info_for_cache.project_id, model_info_for_cache.model_name
            )["id"]
            create_cache_info = CreateCacheInfo(
                model_id=model_id, score_type=model_info_for_cache.score_type
            )

        return self.data_service_client.materialize_data(
            output_split_info.project_id,
            rowset_id_info.get_rowset_id(self),
            output_split_info.data_collection_id,
            output_spec.approx_row_count,
            output_spec.sample_kind,
            output_spec.seed,
            output_split_info.split_name,
            output_split_info.split_type,
            outputFiles=column_info.get_projections(),
            id_column=column_info.id_column[0]
            if column_info.id_column else create_split_column_info.id_col,
            timestamp_column=column_info.timestamp_column[0]
            if column_info.timestamp_column else
            create_split_column_info.timestamp_col,
            split_time_range_begin=output_split_info.split_time_range_begin,
            split_time_range_end=output_split_info.split_time_range_end,
            cache_info=create_cache_info.build_create_cache_info()
            if create_cache_info else None,
            split_mode=split_mode
        )

    def get_root_rowset_by_name(self, project_id, data_source_name):
        return self.data_service_client.get_rowset_status_full_response(
            project_id=project_id, data_source_name=data_source_name
        ).rowset_id

    def add_filter_to_rowset(
        self, project_id, rowset_id, data_source_name, filter
    ):
        input_rowset_id = None
        if rowset_id:
            input_rowset_id = rowset_id
        else:
            input_rowset_id = self.get_root_rowset_by_name(
                project_id, data_source_name
            )

        try:
            output_rowset_id = self.data_service_client.apply_filter(
                project_id, input_rowset_id,
                parse_expression_to_filter_proto(filter, self.logger)
            )

            return input_rowset_id, output_rowset_id
        except ValueError as e:
            raise InvalidFilterError(str(e))

    def get_rowset_status(self, project_id, name, rowset_id):
        if not name and not rowset_id:
            raise MissingParameterException(
                "Neither data source name nor rowset id were provided."
            )

        if not rowset_id:
            rowset_id = self.get_root_rowset_by_name(project_id, name)

        status, error = self.data_service_client.get_rowset_status(
            project_id, rowset_id, throw_on_error=False
        )

        return client_utils.rowset_status_to_str(status), error

    def get_materialize_operation_status(self, project_id, operation_id):
        response = self.data_service_client.get_materialize_data_status(
            project_id, operation_id, throw_on_error=False
        )
        return client_utils.materialize_status_to_str(
            response.status
        ), response.error

    # pylint: disable=no-member
    def project_exists(self, project_id: str):
        try:
            self.ar_client.get_project_metadata(project_id)
        except NotFoundError:
            return False

        return True

    # pylint: disable=no-member
    def data_collection_exists(
        self, project_id: str, data_collection_name: str
    ):
        try:
            self.ar_client.get_data_collection_metadata(
                project_id, data_collection_name=data_collection_name
            )
        except NotFoundError:
            return False

        return True

    # pylint: disable=no-member
    def get_project_id(self, project_name: str) -> str:
        return self.get_project_metadata(project_name, as_json=False).id

    # pylint: disable=no-member
    def get_project_name(self, project_id: str) -> str:
        return self.ar_client.get_project_metadata(project_id).name

    # pylint: disable=no-member
    def get_data_collection_id(
        self, project_id: str, data_collection_name: str
    ):
        try:
            data_collection_metadata = self.ar_client.get_data_collection_metadata(
                project_id, data_collection_name=data_collection_name
            )
        except NotFoundError as e:
            message = f"Could not get specified data_collection : {data_collection_name} in project: {project_id}."
            self.logger.error(message)
            e.message = message
            raise e
        return data_collection_metadata.id

    def get_data_collection_name(
        self, project_id: str, data_collection_id: str
    ):
        try:
            data_collection_metadata = self.ar_client.get_data_collection_metadata(
                project_id, data_collection_id=data_collection_id
            )
        except NotFoundError as e:
            message = f"Could not get specified data_collection : {data_collection_id} in project: {project_id}."
            self.logger.error(message)
            e.message = message
            raise e
        return data_collection_metadata.name

    def get_all_projects(self):
        return self.ar_client.list_all(
            artifact_type=ar_client.ArtifactType.project
        )

    def get_all_models_in_project(
        self,
        project_id: str,
        data_collection_name: Optional[str] = None,
        data_collection_id: Optional[str] = None,
        ar_meta_fetch_mode: ar_client.ArtifactMetaFetchMode = ar_client.
        ArtifactMetaFetchMode.IDS
    ):
        return self.ar_client.list_all(
            artifact_type=ar_client.ArtifactType.model,
            project_id=project_id,
            data_collection_name=data_collection_name,
            data_collection_id=data_collection_id,
            ar_meta_fetch_mode=ar_meta_fetch_mode
        )

    def get_all_model_metadata_in_project(
        self,
        project_id: str,
        data_collection_id: Optional[str] = "",
        as_json: bool = True
    ) -> Sequence[md_pb.ModelMetadata]:
        return self.ar_client.get_all_model_metadata_in_project(
            project_id, data_collection_id=data_collection_id, as_json=as_json
        )

    def get_all_data_collections_in_project(self, project_id: str):
        return self.ar_client.list_all(
            artifact_type=ar_client.ArtifactType.data_collection,
            project_id=project_id
        )

    def get_all_data_collections_with_ids_in_project(self, project_id: str):
        return self.ar_client.list_all(
            artifact_type=ar_client.ArtifactType.data_collection,
            project_id=project_id,
            ar_meta_fetch_mode=ar_client.ArtifactMetaFetchMode.ALL
        )

    def get_all_data_collections_with_transform_type_in_project(
        self, project_id: str
    ):
        dc_obj_list = []
        data_collections = self.ar_client.list_all(
            artifact_type=ar_client.ArtifactType.data_collection,
            project_id=project_id
        )
        for dc_name in data_collections:
            metadata = self.ar_client.get_data_collection_metadata(
                project_id, data_collection_name=dc_name
            )
            dc_obj_list.append(
                DataCollection(dc_name, metadata.feature_transform_type)
            )
        return dc_obj_list

    def get_all_datasplits_in_data_collection(
        self,
        project_name: str,
        data_collection_name: str,
        fetch_metadata: bool = False
    ):
        return self.ar_client.list_all(
            artifact_type=ar_client.ArtifactType.datasplit,
            project_id=project_name,
            data_collection_name=data_collection_name,
            ar_meta_fetch_mode=ar_client.ArtifactMetaFetchMode.ALL
            if fetch_metadata else ar_client.ArtifactMetaFetchMode.IDS
        )

    def get_all_feature_maps_in_project(self, project_id: str):
        return self.ar_client.list_all(
            artifact_type=ar_client.ArtifactType.feature_map,
            project_id=project_id
        )

    def get_all_data_sources_in_project(self, project_id: str):
        rowsets = []

        returned_rowsets, has_more_data = [], True

        while has_more_data:
            returned_rowsets, has_more_data = self.data_service_client.get_rowsets(
                project_id, only_root_rowsets=True
            )
            rowsets.extend(
                [
                    MessageToDict(
                        rs,
                        including_default_value_fields=True,
                        preserving_proto_field_name=True
                    ) for rs in returned_rowsets
                ]
            )

        return rowsets

    def get_all_credentials(self, project_id: str, last_key: str):
        md_list, has_more_data = self.data_service_client.get_credentials(
            project_id, last_key=last_key
        )
        md_list = [
            MessageToDict(
                entry,
                including_default_value_fields=True,
                preserving_proto_field_name=True
            ) for entry in md_list
        ]
        return md_list, has_more_data

    def get_all_rowsets(
        self,
        project_id,
        root_rowset_id,
        only_root_rowsets,
        last_key,
        *,
        include_system_requested=False
    ):
        md_list, has_more_data = self.data_service_client.get_rowsets(
            project_id,
            last_key=last_key,
            root_rowset_id=root_rowset_id,
            only_root_rowsets=only_root_rowsets,
            include_system_requested=include_system_requested
        )

        md_list = [
            MessageToDict(
                entry,
                including_default_value_fields=True,
                preserving_proto_field_name=True
            ) for entry in md_list
        ]
        return md_list, has_more_data

    def get_rowset_metadata(self, rowset_id):
        md = self.data_service_client.get_rowset_metadata(rowset_id)

        return MessageToDict(
            md.rowset,
            including_default_value_fields=True,
            preserving_proto_field_name=True
        )

    def get_materialize_operations(self, project_id, last_key):
        md_list, has_more_data = self.data_service_client.get_materialize_operations(
            project_id, last_key=last_key
        )

        md_list = [
            MessageToDict(
                entry,
                including_default_value_fields=True,
                preserving_proto_field_name=True
            ) for entry in md_list
        ]
        return md_list, has_more_data

    def set_data_collection_for_model(
        self, project_id: str, model_name: str, data_collection_name: str,
        force: bool
    ):
        current_model_metadata = self.ar_client.get_model_metadata(
            project_id, model_name=model_name
        )

        if current_model_metadata.data_collection_id == "" or force:
            if current_model_metadata.HasField("rnn_attribution_config"):
                nn_attribution_config = current_model_metadata.rnn_attribution_config
            elif current_model_metadata.HasField("nlp_attribution_config"):
                nn_attribution_config = current_model_metadata.nlp_attribution_config
            else:
                nn_attribution_config = None
            self.ar_client.create_model_metadata(
                model_id=current_model_metadata.id,
                model_name=current_model_metadata.name,
                description=current_model_metadata.description,
                project_id=current_model_metadata.project_id,
                data_collection_name=data_collection_name,
                model_type=current_model_metadata.model_type,
                model_output_type=current_model_metadata.model_output_type,
                locator=current_model_metadata.locator,
                nn_attribution_config=nn_attribution_config,
                rnn_ui_config=current_model_metadata.rnn_ui_config,
                training_metadata=current_model_metadata.training_metadata,
                tags=current_model_metadata.tags,
                insert_only=False
            )
            return True
        else:
            return False

    def add_train_split_to_model(
        self,
        project_name: str,
        model_name: str,
        train_split_name: str = None,
        overwrite: bool = False
    ) -> None:
        if not train_split_name:
            return
        current_model_metadata = self.get_model_metadata(
            project_name, model_name=model_name, as_json=False
        )
        existing_train_split_name = None
        if current_model_metadata.training_metadata.train_split_id:
            existing_train_split_name = self.get_split_metadata_by_id(
                current_model_metadata.project_id,
                current_model_metadata.training_metadata.train_split_id
            )["name"]
        validate_add_model_metadata(
            model_name=model_name,
            train_split_name=train_split_name,
            existing_train_split_name=existing_train_split_name,
            overwrite=overwrite
        )
        data_collection_name = None
        if current_model_metadata.data_collection_id:
            data_collection_name = self.get_data_collection_metadata_by_id(
                current_model_metadata.project_id,
                current_model_metadata.data_collection_id
            )["name"]
        model_metadata = {
            "train_split_id":
                self.get_split_metadata(
                    project_name, data_collection_name, train_split_name
                )["id"]
        }
        self.ar_client.update_model_metadata(
            current_model_metadata.project_id, model_name, model_metadata
        )

    def add_train_parameters_to_model(
        self,
        project_name: str,
        model_name: str,
        train_parameters: Mapping[str, Any],
        overwrite: bool = False
    ) -> None:
        if not train_parameters:
            return
        current_model_metadata = self.get_model_metadata(
            project_name, model_name=model_name, as_json=False
        )
        validate_add_model_metadata(
            model_name=model_name,
            train_parameters=train_parameters,
            existing_train_parameters=current_model_metadata.training_metadata.
            parameters,
            overwrite=overwrite
        )
        model_metadata = {"train_parameters": train_parameters}
        self.ar_client.update_model_metadata(
            current_model_metadata.project_id, model_name, model_metadata
        )

    def delete_project(self, project_id: str, recursive: bool = False):
        return self.ar_client.delete_metadata(
            project_id,
            ar_client.ArtifactType.project,
            project_id,
            recursive=recursive
        )

    def delete_model(
        self, project_id: str, model_name: str, recursive: bool = False
    ):
        model = self.get_model_metadata(project_id, model_name=model_name)
        success, remaining_items = self.ar_client.delete_metadata(
            project_id,
            ar_client.ArtifactType.model,
            model_name,
            recursive=recursive
        )
        self.logger.info(f"remaining items: {remaining_items}")
        if success:
            if model['model_type'].lower() == 'virtual':
                self.logger.info(
                    "Skipped artifact deletion: model type is virtual"
                )
            else:
                self.ar_client.delete_artifact(
                    project_id, ar_client.ArtifactType.model, model_name, "", []
                )
        return success, remaining_items

    def delete_data_collection(
        self,
        project_id: str,
        data_collection_name: str,
        recursive: bool = False
    ):
        return self.ar_client.delete_metadata(
            project_id,
            ar_client.ArtifactType.data_collection,
            data_collection_name,
            recursive=recursive
        )

    def delete_data_split(
        self,
        project_id: str,
        data_collection_name: str,
        split_name: str,
        recursive: bool = False
    ):
        split_metadata = self.get_split_metadata(
            project_id, data_collection_name, split_name
        )
        success, remaining_items = self.ar_client.delete_metadata(
            project_id,
            ar_client.ArtifactType.datasplit,
            split_name,
            data_collection_name,
            recursive=recursive
        )

        if success:
            if (self.ar_client.is_data_layer_split(split_metadata)):
                self.ar_client.delete_artifact(
                    project_id, ar_client.ArtifactType.materialized_file,
                    split_name, "", [split_metadata["data_collection_id"]]
                )
            else:
                self.ar_client.delete_artifact(
                    project_id, ar_client.ArtifactType.datasplit, split_name,
                    "", [data_collection_name]
                )
        return success, remaining_items

    def delete_feature_map(self, project_id: str, data_collection_name: str):
        self.ar_client.delete_metadata(
            project_id,
            ar_client.ArtifactType.feature_map,
            "__EMPTY__",
            data_collection_name=data_collection_name
        )

    def delete_data_source(self, project_id: str, data_source_name: str):
        rowset_id = self.get_root_rowset_by_name(project_id, data_source_name)
        rowset_metadata = self.data_service_client.get_rowset_metadata(
            rowset_id
        ).rowset
        is_ds_local = False
        if len(rowset_metadata.root_data) == 1:
            is_ds_local = rowset_metadata.root_data[
                0].type == ds_messages_pb.DataSourceType.DS_LOCAL
        self.data_service_client.delete_rowset(rowset_id, delete_children=True)
        if is_ds_local:
            self.ar_client.delete_artifact(
                project_id, ar_client.ArtifactType.data_source,
                data_source_name, "", []
            )

    def delete_credential(self, credential_id=None, credential_name=None):
        if not credential_id and not credential_name:
            raise MissingParameterException(
                "Neither credential id nor credential name provided."
            )

        if not credential_id:
            credential_id = self.data_service_client.get_credential_metadata(
                credential_id=None, credential_name=credential_name
            ).id

        self.data_service_client.delete_credential(credential_id)

    def get_project_metadata(self, project_name, *, as_json=True):
        try:
            return self.ar_client.get_project_metadata(
                project_name, as_json=as_json
            )
        except NotFoundError:
            raise MetadataNotFoundException(
                "Metadata was not found for the project: {}".
                format(project_name)
            ) from None

    def get_model_metadata(
        self, project_name, model_name=None, as_json=True, model_id=None
    ):
        if not (model_name or model_id):
            raise ValueError("Must provide either model name or ID!")
        try:
            return self.ar_client.get_model_metadata(
                project_name,
                model_name=model_name,
                model_id=model_id,
                as_json=as_json
            )
        except NotFoundError:
            raise MetadataNotFoundException(
                "Metadata was not found for the model {} in project {}".format(
                    model_name, project_name
                )
            ) from None

    def get_data_collection_metadata(
        self,
        project_name: str,
        data_collection_name: str,
        as_json: bool = True
    ):
        try:
            return self.ar_client.get_data_collection_metadata(
                project_name,
                data_collection_name=data_collection_name,
                as_json=as_json
            )
        except NotFoundError:
            raise MetadataNotFoundException(
                "Metadata was not found for data collection {} in the project {}"
                .format(data_collection_name, project_name)
            ) from None

    def get_data_collection_metadata_by_id(
        self, project_id, data_collection_id
    ):
        try:
            return self.ar_client.get_data_collection_metadata(
                project_id, data_collection_id=data_collection_id, as_json=True
            )
        except NotFoundError:
            raise MetadataNotFoundException(
                "Metadata was not found for data collection {} in the project {}"
                .format(data_collection_id, project_id)
            ) from None

    def get_split_metadata(
        self, project_name, data_collection_name, split_name
    ):
        try:
            return self.ar_client.get_datasplit_metadata(
                project_name,
                data_collection_name=data_collection_name,
                datasplit_name=split_name,
                as_json=True
            )
        except NotFoundError:
            raise MetadataNotFoundException(
                "Metadata was not found for split {} in data collection {} in the project {}"
                .format(split_name, data_collection_name, project_name)
            ) from None

    def get_split_metadata_by_id(
        self, project_id: str, split_id: str
    ) -> Mapping[str, Union[str, Sequence, Mapping]]:
        try:
            return self.ar_client.get_datasplit_metadata(
                project_id, datasplit_id=split_id, as_json=True
            )
        except NotFoundError:
            raise MetadataNotFoundException(
                "Metadata was not found for split_id {} in the project_id {}".
                format(split_id, project_id)
            ) from None

    def get_feature_list(self, project_name, data_collection_name):
        try:
            return self.ar_client.get_feature_list(
                project_name, data_collection_name=data_collection_name
            )
        except NotFoundError:
            raise MetadataNotFoundException(
                "Feature list was not found for data collection {} in the project {}"
                .format(data_collection_name, project_name)
            ) from None

    def get_schema_of_rowset(self, project_id, rowset_id, data_source_name):
        if rowset_id and data_source_name:
            self.logger.warning(
                f"Warning: both rowset id {rowset_id} and data source name {data_source_name} specified. Data source name will be ignored."
            )
        if not rowset_id and not data_source_name:
            raise MissingParameterException(
                "Neither data source name nor rowset id were provided."
            )

        if not rowset_id:
            rowset_id = self.get_root_rowset_by_name(
                project_id, data_source_name
            )

        return self.data_service_client.get_rowset_columns(
            project_id, rowset_id
        )

    def get_credential_metadata(
        self, credential_id=None, credential_name=None, *, as_json=True
    ):
        if not credential_id and not credential_name:
            raise MissingParameterException(
                "Neither credential id nor credential name provided."
            )

        md = self.data_service_client.get_credential_metadata(
            credential_id=credential_id, credential_name=credential_name
        )
        if as_json:
            return MessageToDict(
                md,
                including_default_value_fields=True,
                preserving_proto_field_name=True
            )
        else:
            return md


class ModelCacheUploader:
    """Utility to help upload model artifact caches (predictions, explanations) with proper error handling.
    """

    def __init__(
        self, tru: Union[TrueraWorkspace, RemoteTrueraWorkspace],
        cache_type: md_pb.CacheType, cache_location: str
    ):
        self.cache_type = cache_type
        self.tru = tru
        self.logger = tru.logger
        self.cache_location = cache_location

    def __enter__(self):
        return self

    def upload(
        self,
        *,
        row_count: int,
        score_type: Optional[str] = None,
        background_data_split_name: Optional[str] = None,
        explanation_algorithm_type: Optional[ExplanationAlgorithmType] = None,
        create_model: bool = True,
        overwrite: bool = True
    ):
        if self.cache_type == md_pb.CacheType.EXPLANATION_CACHE and explanation_algorithm_type is None:
            raise ValueError(
                "Must specify explanation algorithm type when uploading explanation caches!"
            )
        tru_to_use = self.tru.local_tru if hasattr(
            self.tru, "local_tru"
        ) else self.tru  # TrueraWorkspace uploads from local -> remote, but if calling this within RemoteTrueraWorkspace, uploading from remote -> remote

        if score_type is None:
            score_type = tru_to_use._get_score_type()
        self.logger.info(
            f"Uploading cache {self.cache_type} for model \"{tru_to_use._get_current_active_model_name()}\", data_split \"{self.tru._get_current_active_data_split_name()}\", score type \"{score_type}\""
        )
        cache = Cache(
            cache_type=self.cache_type,
            project_id=tru_to_use._get_current_active_project_name(),
            model_name=tru_to_use._get_current_active_model_name(),
            data_collection_name=tru_to_use.
            _get_current_active_data_collection_name(),
            split_name=self.tru._get_current_active_data_split_name(),
            cache_location=self.cache_location,
            score_type=score_type,
            model_output_type=tru_to_use._get_output_type(),
            row_count=row_count,
            client_name="python_client",
            client_version=truera.__version__,
            background_data_split_name=background_data_split_name,
            explanation_algorithm_type=explanation_algorithm_type
        )
        cache.upload(
            self.tru.artifact_interaction_client,
            create_model=create_model,
            overwrite=overwrite
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            os.remove(self.cache_location)
        except Exception:
            pass

        if exc_type is AlreadyExistsError:
            self.logger.warning(
                f"Model artifact {self.cache_type} for model \"{self.tru._get_current_active_model_name()}\" and data_split \"{self.tru._get_current_active_data_split_name()}\" exists in remote. Skipping upload."
            )
            return True  # suppress error


def build_column_info_from_file(column_spec_file):
    _, ext = os.path.splitext(column_spec_file)

    parsed_file = None

    if ext == ".yml" or ext == ".yaml":
        with open(column_spec_file) as fp:
            parsed_file = yaml.safe_load(fp)
    elif ext == ".json":
        try:
            with open(column_spec_file) as fp:
                parsed_file = json.load(fp)
        except json.decoder.JSONDecodeError:
            raise InvalidColumnInfoFileException(
                f"Provided column spec file {column_spec_file} was not a valid json file."
            )
    else:
        message = "Could not determine type of provided column spec file. Please provide a '.json', '.yaml', or '.yml' file. Provided file: " + column_spec_file
        raise client_utils.NotSupportedFileTypeException(message)

    if not "columns" in parsed_file:
        raise InvalidColumnInfoFileException(
            f"Provided column spec file {column_spec_file} did not contain top level element 'columns'. For an example file use '> tru get sample column-spec-file'."
        )

    def coalesce_key_to_list(key):
        if not key in parsed_file["columns"]:
            return None
        else:
            to_ret = parsed_file["columns"][key]
            to_ret = [to_ret] if isinstance(to_ret, str) else to_ret
            for col in to_ret:
                if not isinstance(col, str):
                    raise InvalidColumnInfoFileException(
                        f"Provided column spec file {column_spec_file} did not contain a list of strings under {key}. For an example file use '> tru get sample column-spec-file'."
                    )
            return to_ret

    pre_columns = coalesce_key_to_list("pre_transform_columns")
    post_columns = coalesce_key_to_list("post_transform_columns")
    label_col_from_spec = coalesce_key_to_list("label_column")
    extra_columns = coalesce_key_to_list("extra_data_columns")
    prediction_columns = coalesce_key_to_list("prediction_columns") or None
    feature_influence_columns = coalesce_key_to_list(
        "feature_influence_columns"
    ) or None
    id_column = coalesce_key_to_list("id_column")
    timestamp_column = coalesce_key_to_list("timestamp_column")
    return ColumnInfo(
        pre=pre_columns,
        post=post_columns,
        label=label_col_from_spec,
        extra=extra_columns,
        prediction=prediction_columns,
        feature_influences=feature_influence_columns,
        id_column=id_column,
        timestamp_column=timestamp_column
    )
