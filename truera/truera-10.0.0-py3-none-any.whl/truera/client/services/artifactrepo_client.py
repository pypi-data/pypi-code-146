from __future__ import annotations

from collections import namedtuple
from enum import Enum
import hashlib
from itertools import chain
import logging
import os
import sys
from typing import List, Mapping, Optional, Sequence, Union
import uuid

from google.protobuf.json_format import MessageToDict
from google.protobuf.json_format import Parse

from truera.artifactrepo.arlib import artifactrepolib as lib
from truera.client.client_utils import create_time_range
from truera.client.client_utils import get_input_data_format_from_string
from truera.client.client_utils import get_qoi_from_string
from truera.client.errors import SimpleException
from truera.client.nn.client_configs import NLPAttributionConfiguration
from truera.client.nn.client_configs import RNNAttributionConfiguration
from truera.client.nn.client_configs import RNNUserInterfaceConfiguration
from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.artifactrepo_http_communicator import \
    HttpArtifactRepoCommunicator
from truera.client.public.communicator.http_communicator import \
    AlreadyExistsError
from truera.protobuf.configuration.project_pb2 import \
    ProjectDocumentation  # pylint: disable=no-name-in-module
from truera.protobuf.public import artifactrepo_pb2 as ar_pb
from truera.protobuf.public import metadata_message_types_pb2 as md_pb
from truera.protobuf.public import tokenservice_pb2 as tokenservice_pb2
from truera.protobuf.public.aiq.rnn_config_pb2 import \
    NLPAttributionConfig  # pylint: disable=no-name-in-module
from truera.protobuf.public.aiq.rnn_config_pb2 import \
    RNNAttributionConfig  # pylint: disable=no-name-in-module
from truera.protobuf.public.aiq.rnn_config_pb2 import \
    RNNUIConfig  # pylint: disable=no-name-in-module
from truera.protobuf.public.qoi_pb2 import \
    ExplanationAlgorithmType  # pylint: disable=no-name-in-module
from truera.protobuf.public.util import split_mode_pb2 as sm_pb
from truera.public.artifact_repo_lib import ensure_valid_identifier


class ArtifactType(Enum):
    invalid = 0
    model = 1
    datasplit = 2
    documentation = 3
    data_collection = 4
    project = 5
    feature_map = 6
    data_source = 7
    materialized_file = 8
    cache = 9


class ArtifactMetaFetchMode(Enum):
    ALL = 0
    NAMES = 1
    IDS = 2


class DeleteFailedException(SimpleException):
    pass


class LabelIngestionFailedException(SimpleException):
    pass


class ArtifactRepoClientContext:

    def __init__(self):
        pass

    def abort(self, _, message):
        print(message)
        sys.exit(1)


# This is just a wrapper for an iterator that can be used to guarantee that the iterator is non-empty.
class NonEmptyIterator:

    def __init__(self, itr_to_wrap, message_if_empty):
        super().__init__()
        if isinstance(itr_to_wrap, list):
            if len(itr_to_wrap) == 0:
                raise lib.EmptyIteratorError(message_if_empty)
            self.first = itr_to_wrap[0]
            self.itr = iter(itr_to_wrap[1:])
        else:
            self.first = next(itr_to_wrap, None)
            if self.first == None:
                raise lib.EmptyIteratorError(message_if_empty)
            else:
                self.itr = itr_to_wrap
        self.returned_first = False

    def __iter__(self):
        return self

    def __next__(self):
        if not self.returned_first:
            self.returned_first = True
            return self.first
        return next(self.itr)


class ArtifactRepoClient:

    # Consider - we can consider tuning this value for performance / reliability.
    __READ_WRITE_SIZE__ = 2 * 1024 * 1024
    __UPDATE_AFTER_N_CHUNKS__ = 1

    def __init__(
        self,
        connection_string: str = None,
        logger=None,
        auth_details: AuthDetails = None,
        use_http: bool = False,
        *,
        verify_cert: Union[bool, str] = True
    ):
        if (not use_http):
            from truera.client.private.communicator.artifactrepo_grpc_communicator import \
                GrpcArtifactRepoCommunicator
        self.logger = logger
        self.client_context = ArtifactRepoClientContext()
        self.auth_details = auth_details
        self.communicator = HttpArtifactRepoCommunicator(
            connection_string, auth_details, logger, verify_cert=verify_cert
        ) if use_http else GrpcArtifactRepoCommunicator(
            connection_string, auth_details, logger
        )
        self._connection_string = connection_string

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        self.communicator.close()

    def log(self, log_line: str, end='\n', flush=False):
        if self.logger is not None:
            self.logger.info(log_line)
        else:
            print(log_line, end=end, flush=flush)

    # This should only be used for information we want to print to the console and not log -- and only when
    # that information is for informational purposes. The main user right now is file upload progress, which
    # we shouldn't print when we're passed a relatively silenced logger, but also should not be printed using
    # the logger since it doesn't have the ability to add to a line without a return.
    def conditionally_print(self, log_line, end='\n', flush=False):
        if self.logger is not None and self.logger.getEffectiveLevel(
        ) <= logging.INFO:
            print(log_line, end=end, flush=flush)

    def log_verbose(self, log_line: str, end='\n', flush=False):
        if self.logger is not None:
            self.logger.debug(log_line)
        else:
            print(log_line, end=end, flush=flush)

    def ping(self, ping_message: str = None) -> str:
        """
            Pings the artifact repo server with a string message which
            the server will return verbatim. If no string is provided
            the client will create a guid for the message.
        Args:
            ping_message: -- Message to be sent to the artifact repo server.
        
        Returns:
            str: version of the CLI that the server's build contains

        """
        ping_message = ping_message or str(uuid.uuid4())
        try:
            response = self.communicator.ping(
                self._build_ping_request(ping_message)
            )
        except ConnectionError:
            # devnote: a totally bogus connection string would throw an HTTPConnectionError.
            # however, if the deployment URL is partially correct but has unnecessary text appended e.g. http://truera-deployment.com/p
            # then a JSON parse error is thrown which is caught using TruEra's internal ConnectionError.
            raise ConnectionError(
                f"Failed to connect! Provided connection string: {self._connection_string}. Your connection string should be of the form http://your-truera-deployment.com/"
            )
        if ping_message != response.test_string_back:
            raise ValueError(
                f"Could not connect to the artifact repo using connection string {self._connection_string} and provided authentication credentials."
            )

        return response.cli_version

    # pylint: disable=no-member
    def upload_artifact(
        self,
        src: str,
        project_id: str,
        artifact_type: ArtifactType,
        artifact_id: str,
        intra_artifact_path: str,
        scoping_artifact_ids: List[str],
        list_of_src_files_or_dirs: Optional[List[str]] = None,
        stream: bool = False
    ) -> str:
        """
            Upload a file or folder to the artifact repository. In the case of a folder,
            the structure within the folder is preserved. 
        
        Args:
            src: source path of the file or folder to upload
            project_id: project id of the uploaded artifact
            artifact_type: artifact kind
            artifact_id: id for artifact tracking
            intra_artifact_path: path within that artifact
            list_of_src_files_or_dirs: additional files or dirs to be uploaded at the top level

        Returns:
            The path to the artifact in the repo.

        """
        if list_of_src_files_or_dirs is None:
            list_of_src_files_or_dirs = []
        ensure_valid_identifier(artifact_id, self.client_context)
        for scope_level in scoping_artifact_ids:
            ensure_valid_identifier(scope_level, self.client_context)
        try:
            flattened_src_list = [
                lib.flatten(extra_src, self.logger)
                for extra_src in list_of_src_files_or_dirs
            ]
            if src not in list_of_src_files_or_dirs:
                flattened_src_list.insert(0, lib.flatten(src, self.logger))
            src_itr = NonEmptyIterator(
                chain(*flattened_src_list),
                "Error: Zero files were provided for upload."
            )
            response = self.communicator.put_resource(
                self._flatten_into_call_iters(
                    src_itr, project_id, artifact_type, artifact_id,
                    intra_artifact_path, scoping_artifact_ids
                ),
                stream=stream
            )
        except AlreadyExistsError as e:
            e.message = "The entity " + artifact_id + " already exists."
            raise e
        self.conditionally_print('Put resource done.')
        return response.repo_artifact_path

    # pylint: disable=no-member
    def upload_artifact_list(
        self, list_of_src_files, project_id: str, artifact_type: ArtifactType,
        artifact_name: str, intra_artifact_path: str,
        scoping_artifact_ids: List[str]
    ) -> str:
        """
            Upload a file or folder to the artifact repository. In the case of a folder,
            the structure within the folder is preserved. 
        
        Args:
            list_of_src_files: source files to upload
            project_id: project id of the uploaded artifact
            artifact_type: artifact kind
            artifact_id: id for artifact tracking
            intra_artifact_path: path within that artifact

        Returns:
            The repo path.

        """
        ensure_valid_identifier(artifact_name, self.client_context)

        for scope_level in scoping_artifact_ids:
            ensure_valid_identifier(scope_level, self.client_context)
        try:
            src_files_itr = NonEmptyIterator(
                list_of_src_files, "Error: Zero files were provided for upload."
            )
            response = self.communicator.put_resource(
                self._request_list_from_list_of_files(
                    src_files_itr, project_id, artifact_type, artifact_name,
                    intra_artifact_path, scoping_artifact_ids
                )
            )
        except AlreadyExistsError as e:
            e.message = "The entity " + artifact_name + " already exists."
            raise e
        return response.repo_artifact_path

    def file_exists(
        self, project_id: str, artifact_type: ArtifactType, artifact_id: str,
        intra_artifact_path: str, scoping_artifact_ids: List[str]
    ) -> bool:
        """
            Checks for existence of a file at the specified path within the specified project.
        
        Args:
            project_id: project id of the uploaded artifact
            artifact_type: artifact kind
            artifact_id: id for artifact tracking
            intra_artifact_path: path within that artifact
        
        Returns:
            If a file exists at that path.

        """
        return self._artifact_exists(
            project_id, artifact_type, artifact_id, intra_artifact_path,
            scoping_artifact_ids
        ) == ar_pb.ExistsResponseOption.FILE_EXISTS

    def directory_exists(
        self, project_id: str, artifact_type: ArtifactType, artifact_id: str,
        intra_artifact_path: str, scoping_artifact_ids: List[str]
    ) -> bool:
        """
            Checks for existence of a directory at the specified path within the specified project.
        
        Args:
            project_id: project id of the uploaded artifact
            artifact_type: artifact kind
            artifact_id: id for artifact tracking
            intra_artifact_path: path within that artifact
        
        Returns:
            If a directory exists at that path.

        """
        return self._artifact_exists(
            project_id, artifact_type, artifact_id, intra_artifact_path,
            scoping_artifact_ids
        ) == ar_pb.ExistsResponseOption.DIRECTORY_EXISTS

    def download_artifact(
        self, src_project_id: str, src_artifact_type: ArtifactType,
        src_artifact_id: str, src_intra_artifact_path: str,
        scoping_artifact_ids: List[str], dest: str
    ):
        """
            Downloads the specified artifact from the specified project to the destination.
        
        Args:
            src_project_id: project id of the uploaded artifact
            src_artifact_type: artifact kind
            src_artifact_id: id for artifact tracking
            src_intra_artifact_path: path within that artifact
            dest: Local path where the downloaded artifacts should go

        """
        req = self._build_download_request(
            src_project_id, src_artifact_type, src_artifact_id,
            src_intra_artifact_path, scoping_artifact_ids
        )
        for response in self.communicator.get_resource(req):
            output_path = os.path.join(dest, response.intra_artifact_path)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'ab') as f:
                f.write(response.output_chunk)
                self.log_verbose(
                    'Wrote from get response for file: ' + output_path
                )

    # pylint: disable=no-member
    def delete_artifact(
        self, project_id: str, artifact_type: ArtifactType, artifact_id: str,
        intra_artifact_path: str, scoping_artifact_ids: List[str]
    ) -> None:
        """
            Remove all artifacts from the specified path in the specified project.
        
        Args:
            project_id: project id of the uploaded artifact
            artifact_type: artifact kind
            artifact_id: id for artifact tracking
            intra_artifact_path: path within that artifact
        
        Returns:
            If the delete operation was successful or not.

        """
        req = self._build_delete_request(
            project_id, artifact_type, artifact_id, intra_artifact_path,
            scoping_artifact_ids
        )
        try:
            self.communicator.delete_resource(req)
        except Exception as e:
            raise DeleteFailedException(
                "Delete artifact failed. Cause: " + str(e)
            ) from None
        self.log(
            "Delete resource succeeded. Project_id: " + project_id +
            " intra_artifact_path: " + intra_artifact_path
        )

    def create_project(
        self,
        project_name: str,
        description_json: Optional[str] = None,
        score_type: str = "logits",
        input_data_format: str = "tabular"
    ) -> str:
        """
            Create a project with the specified name.
        Args:
            project_name: The name of the project to create

        Returns:
            The id of the project created

        """
        ensure_valid_identifier(project_name, self.client_context)
        req = self._build_create_project_metadata_request(
            project_name, description_json, score_type, input_data_format
        )
        try:
            response = self.communicator.put_metadata(req)
        except AlreadyExistsError as e:
            message = "The entity " + project_name + " already exists."
            self.log(message)
            e.message = message
            raise e

        return response.id

    def create_model_metadata(
        self,
        *,
        model_id: str,
        model_name: str,
        description: str = None,
        project_id: str,
        data_collection_name: str,
        model_type: str,
        model_output_type: str,
        locator: str,
        nn_attribution_config: Optional[Union[RNNAttributionConfig,
                                              NLPAttributionConfig]] = None,
        rnn_ui_config: Optional[RNNUIConfig] = None,
        training_metadata: Optional[md_pb.ModelTrainingMetadata] = None,
        tags: Optional[Sequence[str]] = None,
        insert_only: bool = True
    ) -> str:
        """
            Create the metadata for a model. 
        Args:
            model_id: id of the model
            model_name: name of the model
            project_id: project id the model is under
            data_collection_name: data_collection id for the model's data
            model_type: type of model
            locator: pointer to the folder containing the model

        Args:
            A description of the model to store
            Tags associated with the model

        Returns:
            Id of the model.

        """
        ensure_valid_identifier(project_id, self.client_context)
        ensure_valid_identifier(model_name, self.client_context)
        req = self._build_create_model_metadata_request(
            model_id=model_id,
            model_name=model_name,
            description=description,
            project_id=project_id,
            data_collection_name=data_collection_name,
            model_type=model_type,
            model_output_type=model_output_type,
            locator=locator,
            nn_attribution_config=nn_attribution_config,
            rnn_ui_config=rnn_ui_config,
            training_metadata=training_metadata,
            tags=tags,
            insert_only=insert_only
        )
        try:
            response = self.communicator.put_metadata(req)
        except AlreadyExistsError as e:
            self.log("The entity " + model_name + " already exists.")
            raise e
        return response.id

    def create_data_collection(
        self,
        project_id,
        data_collection_name,
        feature_transform_type,
        tags=None,
        description="",
        *,
        schemas: md_pb.SchemaMetadata = None
    ) -> str:
        """
            Create a data_collection under the specified project with the provided name.
        Args:
            project_id: Id of the project to create the data_collection in
            data_collection_name: Name of the data_collection
            tags: tags

        Returns:
            Id of the data_collection created.

        """
        ensure_valid_identifier(project_id, self.client_context)
        ensure_valid_identifier(data_collection_name, self.client_context)
        req = self._build_create_data_collection_metadata_request(
            project_id, data_collection_name, feature_transform_type, tags,
            description, schemas
        )
        try:
            response = self.communicator.put_metadata(req)
        except AlreadyExistsError as e:
            message = 'The entity ' + data_collection_name + ' already exists.'
            self.log(message)
            e.message = message
            raise e
        return response.id

    def create_cache_metadata(
        self,
        cache_type: md_pb.CacheType,
        project_id: str,
        model_id: str,
        data_collection_name: str,
        split_name: str,
        location: str,
        format: str,
        score_type: str,
        row_count: int,
        client_name: str,
        client_version: str,
        background_data_split_name: Optional[str] = None,
        explanation_algorithm_type: Optional[ExplanationAlgorithmType] = None
    ) -> str:
        """
        Create metadata for a cache (either ModelPrediction or Explanation)
        """

        ensure_valid_identifier(project_id, self.client_context)
        ensure_valid_identifier(data_collection_name, self.client_context)
        ensure_valid_identifier(split_name, self.client_context)

        req = self._build_create_cache_request(
            project_id=project_id,
            model_id=model_id,
            data_collection_name=data_collection_name,
            split_name=split_name,
            background_data_split_name=background_data_split_name,
            location=location,
            format=format,
            score_type=score_type,
            row_count=row_count,
            cache_type=cache_type,
            explanation_algorithm_type=explanation_algorithm_type,
            client_name=client_name,
            client_version=client_version
        )

        try:
            response = self.communicator.put_metadata(req)
        except AlreadyExistsError as e:
            message = f"The cache entity for model id {model_id} of type {md_pb.CacheType.Name(cache_type)} already exists."
            self.log(message)
            e.message = message
            raise e
        return response.id

    def create_split_metadata(
        self,
        *,
        split_name: str,
        description: str = None,
        project_id: str,
        data_collection_name: str,
        split_type: str,
        preprocessed_locator: str = None,
        processed_locator: str = None,
        label_locator: str = None,
        extra_data_locator: str = None,
        tags=None,
        split_time_range_begin: str = None,
        split_time_range_end: str = None,
        id_column_name: str = None,
        split_mode: sm_pb.SplitMode,
        status: md_pb.SplitStatus = md_pb.SplitStatus.SPLIT_STATUS_ACTIVE
    ) -> str:
        """
            Create metadata for a data split.
        Args:
            split_name: The name of the split
            project_id: The project the split resides in.
            data_collection_name: The data_collection the split is part of.
            split_type: Type of the split.

        Args:
            description: Description of the split.
            preprocessed_locator: PreProcessed data locator.
            processed_locator: PostProcessed data locator.
            label_locator: Label data locator.
            extra_data_locator: Extra data locator.
            tags: tags.
            split_time_range_begin: start of the time range
            split_time_range_end: end of the time range

        Returns:
            Id of the split.

        """
        ensure_valid_identifier(project_id, self.client_context)
        ensure_valid_identifier(data_collection_name, self.client_context)
        ensure_valid_identifier(split_name, self.client_context)

        if split_mode == sm_pb.SplitMode.SPLIT_MODE_INVALID:
            raise ValueError(
                f"Valid `split_mode` must be provided for data split {split_name}."
            )

        try:
            response = self.communicator.put_metadata(
                self._build_create_split_metadata_request(
                    split_name, description, project_id, data_collection_name,
                    split_type, preprocessed_locator, processed_locator,
                    label_locator, extra_data_locator, tags,
                    split_time_range_begin, split_time_range_end,
                    id_column_name, split_mode, status
                )
            )
        except AlreadyExistsError as e:
            message = "The entity " + split_name + " already exists."
            self.log(message)
            e.message = message
            raise e
        return response.id

    def upload_feature_list_metadata(
        self, feature_list_pb, insert_only=False
    ) -> bool:
        try:
            response = self.communicator.put_metadata(
                self._build_create_feature_list_metadata_request(
                    feature_list_pb, insert_only
                )
            )
        except AlreadyExistsError as e:
            message = (
                "The project / data_collection combination " +
                feature_list_pb.project_id + " / " +
                feature_list_pb.data_collection_id +
                " already had a feature list. It can be overridden, or new features can be added."
            )
            self.log(message)
            e.message = message
            raise e
        return response.id

    def update_model_metadata(
        self, project_id, model_name, metadata: Mapping[str, any]
    ):

        self._validate_update_model_metadata(metadata)
        model_metadata = self._get_metadata_for_entity_by_name(
            project_id, ar_pb.ArtifactType.MODEL, model_name
        ).model
        for field_name, value in metadata.items():
            if field_name == "rnn_attribution_config":
                model_metadata.rnn_attribution_config.CopyFrom(
                    value._to_protobuf()
                )
            elif field_name == "rnn_ui_config":
                model_metadata.rnn_ui_config.CopyFrom(value._to_protobuf())
            elif field_name == "nlp_attribution_config":
                model_metadata.nlp_attribution_config.CopyFrom(
                    value._to_protobuf()
                )
            elif field_name == "train_split_id":
                model_metadata.training_metadata.train_split_id = value
            elif field_name == "train_parameters":
                model_metadata.training_metadata.parameters.Clear()
                model_metadata.training_metadata.parameters.update(value)
            elif field_name == "locator":
                model_metadata.locator = value
            elif field_name == "model_type":
                model_metadata.model_type = value
        req = ar_pb.PutMetadataRequest(model=model_metadata, insert_only=False)
        return self.communicator.put_metadata(req).id

    def _validate_update_model_metadata(
        self, metadata: Mapping[str, any]
    ) -> None:
        accepted_fields_and_types = {
            "rnn_attribution_config": RNNAttributionConfiguration,
            "rnn_ui_config": RNNUserInterfaceConfiguration,
            "nlp_attribution_config": NLPAttributionConfiguration,
            "train_split_id": str,
            "train_parameters": Mapping,
            "locator": str,
            "model_type": str,
        }
        for field_name, value in metadata.items():
            if field_name not in accepted_fields_and_types:
                raise ValueError(
                    f"Trying to update an unsupported model metadata: `{field_name}`. Currently only support updating: {list(accepted_fields_and_types.keys())}"
                )
            if not isinstance(value, accepted_fields_and_types[field_name]):
                raise ValueError(
                    f"`{field_name}` has to be of type `{accepted_fields_and_types[field_name]}`. Given type: {type(value)}"
                )

    def list_all(
        self,
        *,
        artifact_type: ArtifactType,
        project_id: Optional[str] = None,
        data_collection_name: Optional[str] = None,
        data_collection_id: Optional[str] = None,
        ar_meta_fetch_mode: ArtifactMetaFetchMode = ArtifactMetaFetchMode.IDS,
        include_non_active_splits: bool = False
    ):
        """[summary]
            Get all names for a particular artifact type. If the type is project, names of all projects will be returned.
            Otherwise, the project id will be used for scoping. If the type is model / data_collection, then names of all models /
            data_collections in the specified project will be returned. If the type is datasplit, then all splits in the project /
            data_collection combo will be returned. For Id's - see Name / Id pairs member in the response. 
        Args:
            artifact_type Type of the artifact to retrieve. Options: Projects, Models, Data_Collections, Datasplits.

        Args:
            project_id: project id used for scoping
            data_collection_name: data_collection name used for scoping (if data_collection_id is unspecified)
            data_collection_id: data_collection id used for scoping

        Returns:
            list of entities 
        """
        artifact_type = self.__map_artifacttype_to_pb(artifact_type)
        if artifact_type == ar_pb.ArtifactType.PROJECT:
            project_id = "___ALL___"
        request = ar_pb.GetAllMetadataRequest(
            project_id=project_id or "",
            data_collection_name=data_collection_name,
            data_collection_id=data_collection_id,
            artifact_type=artifact_type,
            include_non_active_splits=include_non_active_splits
        )
        response = self.communicator.get_all_metadata_for_resource(request)
        response_as_dict = MessageToDict(
            response,
            including_default_value_fields=True,
            preserving_proto_field_name=True
        )
        if ar_meta_fetch_mode == ArtifactMetaFetchMode.IDS:
            return list(response.id)
        elif ar_meta_fetch_mode == ArtifactMetaFetchMode.NAMES:
            return [item["name"] for item in response_as_dict["name_id_pairs"]]
        elif ar_meta_fetch_mode == ArtifactMetaFetchMode.ALL:
            return response_as_dict

    def get_project_metadata(
        self,
        project_id: str,
        *,
        as_json: bool = False
    ) -> md_pb.ProjectMetadata:
        response = self._get_metadata_for_entity_by_name(
            project_id, ar_pb.ArtifactType.PROJECT, project_id
        )

        if as_json:
            return MessageToDict(
                response.project,
                including_default_value_fields=True,
                preserving_proto_field_name=True
            )

        return response.project

    def get_model_metadata(
        self,
        project_id: str,
        *,
        model_name: str = None,
        model_id: str = None,
        as_json=False
    ) -> md_pb.ModelMetadata:
        if model_id:
            response = self._get_metadata_for_entity_by_id(
                project_id, ar_pb.ArtifactType.MODEL, model_id
            )
        elif model_name:
            response = self._get_metadata_for_entity_by_name(
                project_id, ar_pb.ArtifactType.MODEL, model_name
            )
        else:
            raise ValueError("Both model_name and model_id cannot be empty")
        if as_json:
            return MessageToDict(
                response.model,
                including_default_value_fields=True,
                preserving_proto_field_name=True
            )

        return response.model

    def get_all_model_metadata_in_project(
        self,
        project_id: str,
        data_collection_id: Optional[str] = "",
        as_json: bool = True
    ) -> Sequence[md_pb.ModelMetadata]:
        if not data_collection_id:
            data_collection_id = ""
        response = self.communicator.get_models(
            ar_pb.GetModelsRequest(
                project_id=project_id, data_collection_id=data_collection_id
            )
        )

        if as_json:
            return [
                MessageToDict(
                    model,
                    including_default_value_fields=True,
                    preserving_proto_field_name=True
                ) for model in response.models
            ]
        return response.models

    def get_all_splits_metadata_in_data_collection(
        self,
        project_id: str,
        data_collection_id: str,
        include_non_active_splits: bool = False
    ) -> Sequence[md_pb.DataSplitMetadata]:
        response = self.communicator.get_splits(
            ar_pb.GetSplitsRequest(
                project_id=project_id,
                for_items=[
                    ar_pb.GetSplitsRequestItem(
                        data_collection_id=data_collection_id,
                        sort_by_property="name"
                    )
                ],
                include_non_active_splits=include_non_active_splits
            )
        )

        # This api supports asking for multiple groups of splits but we don't need that here right now
        return response.split_items[0].splits

    def get_data_collection_metadata(
        self,
        project_id: str,
        *,
        data_collection_name: str = None,
        data_collection_id: str = None,
        as_json: bool = False
    ) -> md_pb.DataCollectionMetadata:
        if data_collection_id:
            response = self._get_metadata_for_entity_by_id(
                project_id, ar_pb.ArtifactType.DATACOLLECTION,
                data_collection_id
            )
        elif data_collection_name:
            response = self._get_metadata_for_entity_by_name(
                project_id,
                ar_pb.ArtifactType.DATACOLLECTION,
                entity_name=data_collection_name
            )
        else:
            raise ValueError(
                "Both data_collection_name and data_collection_id cannot be empty"
            )

        if as_json:
            return MessageToDict(
                response.data_collection,
                including_default_value_fields=True,
                preserving_proto_field_name=True
            )

        return response.data_collection

    def get_datasplit_metadata(
        self,
        project_id: str,
        *,
        data_collection_name: str = None,
        datasplit_name: str = None,
        datasplit_id: str = None,
        as_json: bool = False
    ) -> md_pb.DataSplitMetadata:
        if datasplit_id:
            response = self._get_metadata_for_entity_by_id(
                project_id, ar_pb.ArtifactType.DATASPLIT, datasplit_id
            )
        elif datasplit_name and data_collection_name:
            response = self._get_metadata_for_entity_by_name(
                project_id,
                ar_pb.ArtifactType.DATASPLIT,
                entity_name=datasplit_name,
                data_collection_name=data_collection_name
            )
        else:
            raise ValueError(
                "Required datasplit_id or (datasplit_name and data_collection_name)."
            )

        if as_json:
            return MessageToDict(
                response.split,
                including_default_value_fields=True,
                preserving_proto_field_name=True
            )
        return response.split

    def get_feature_list(
        self,
        project_id: str,
        data_collection_name: str = None,
    ):
        response = self._get_metadata_for_entity_by_name(
            project_id,
            ar_pb.ArtifactType.FEATURE_LIST,
            "__EMPTY__",
            data_collection_name=data_collection_name
        )
        return MessageToDict(
            response.feature_list,
            including_default_value_fields=True,
            preserving_proto_field_name=True
        )

    def get_credential_metadata(self, project_id, data_source_credential_id):
        return self._get_metadata_for_entity_by_id(
            project_id, ar_pb.ArtifactType.CREDENTIALS,
            data_source_credential_id
        )

    def delete_metadata(
        self,
        project_id: str,
        artifact_type: ArtifactType,
        artifact_name: str,
        data_collection_name: Optional[str] = None,
        recursive: bool = False
    ) -> None:
        request = ar_pb.DeleteMetadataRequest(
            project_id=project_id,
            artifact_type=self.__map_artifacttype_to_pb(artifact_type),
            entity_name=artifact_name,
            data_collection_name=data_collection_name,
            recursive=recursive
        )
        try:
            response = self.communicator.delete_metadata(request)
            RemainingItem = namedtuple(
                "RemainingItem",
                ("type", "name", "id", "can_be_deleted_via_recursive_flag")
            )
            return response.success, [
                RemainingItem(
                    type=str(ar_pb.ArtifactType.Name(entity.type)),
                    name=entity.name,
                    id=entity.id,
                    can_be_deleted_via_recursive_flag=entity.
                    can_be_deleted_via_recursive_flag
                ) for entity in response.blocking_entities
            ]
        except Exception as e:
            raise DeleteFailedException(
                "Delete metadata failed. Cause: " + str(e)
            ) from None

    def _get_metadata_for_entity_by_name(
        self,
        project_id: str,
        artifact_type: ar_pb.ArtifactType,
        entity_name: str,
        data_collection_name: Optional[str] = None
    ):
        request = ar_pb.GetMetadataForEntityRequest(
            project_id=project_id,
            artifact_type=artifact_type,
            entity_name=entity_name,
            data_collection_name=data_collection_name
        )
        return self.communicator.get_metadata_for_entity(request)

    def _get_metadata_for_entity_by_id(
        self,
        project_id: str,
        artifact_type: ar_pb.ArtifactType,
        entity_id: str,
    ):
        request = ar_pb.GetMetadataForEntityRequest(
            project_id=project_id,
            artifact_type=artifact_type,
            entity_id=entity_id
        )
        return self.communicator.get_metadata_for_entity(request)

    def _build_ping_request(self, ping_message: str = None):
        return ar_pb.PingRequest(test_string=ping_message)

    def _build_get_user_token_request(self):
        return tokenservice_pb2.GetUserTokenRequest()

    def _build_upload_request(
        self, path: str, project_id: str, artifact_type: ArtifactType,
        artifact_id: str, intra_artifact_path: str,
        scoping_artifact_ids: List[str]
    ):
        self.conditionally_print(
            "Uploading " + self.__get_file_name_from_path(path) + " -- #",
            end='',
            flush=True
        )
        chunk_count = 0
        with open(path, 'rb') as f:
            while True:
                fileBytes = bytes(f.read(self.__READ_WRITE_SIZE__))
                if chunk_count % self.__UPDATE_AFTER_N_CHUNKS__ == 0:
                    self.conditionally_print("#", end='', flush=True)
                chunk_count += 1
                if not fileBytes:
                    break
                checksum = ar_pb.ResourceChecksum(
                    value=hashlib.  # nosec B324 - not using for security
                    md5(fileBytes).hexdigest(),
                    type=ar_pb.ResourceChecksum.ChecksumType.MD5
                )
                yield ar_pb.PutRequest(
                    input_chunk=fileBytes,
                    project_id=project_id,
                    artifact_type=self.__map_artifacttype_to_pb(artifact_type),
                    artifact_id=artifact_id,
                    intra_artifact_path=intra_artifact_path,
                    scoping_artifact_ids=scoping_artifact_ids,
                    checksum=checksum
                )

        self.conditionally_print(" -- file upload complete.")

    def _flatten_into_call_iters(
        self, src_itr, project_id: str, artifact_type: ArtifactType,
        artifact_id: str, intra_artifact_path: str,
        scoping_artifact_ids: List[str]
    ):
        for relative_upload_file_path, full_upload_file_path in src_itr:
            repo_intra_artifact_path = os.path.join(
                intra_artifact_path, relative_upload_file_path
            )

            repo_intra_artifact_path = self.format_intra_artifact_paths_for_linux(
                repo_intra_artifact_path, os.sep
            )

            # The artifact repo service has rules about what kind of files can be uploaded
            # skip files that start with '.' because they are likely hidden from the user
            # and they probably didn't mean to upload that file.
            if (
                self.__get_file_name_from_path(full_upload_file_path
                                              ).startswith('.')
            ):
                self.log("Warning - file skipped: " + full_upload_file_path)
                continue
            yield from self._build_upload_request(
                full_upload_file_path, project_id, artifact_type, artifact_id,
                repo_intra_artifact_path, scoping_artifact_ids
            )

    def format_intra_artifact_paths_for_linux(self, path, separator):
        # This transforms all paths to the input format that artifact repo (which is on linux)
        # is expecting. For linux paths, this does not change them. For windows paths, it replaces
        # all the '\'s with '/' which is still valid.
        # on linux:
        # /home/usr/repos -> /home/usr/repos
        # /home/usr/repos/doc.doc -> /home/usr/repos/doc.doc
        # usr/repos/doc.doc -> usr/repos/doc.doc
        # on windows:
        # C:\Users\Usr\Downloads\ -> C:/Users/Usr/Downloads/
        # C:\Users\Usr\Downloads\doc.doc -> C:/Users/Usr/Downloads/doc.doc
        # F:\Users\Usr\Downloads\ -> F:/Users/Usr/Downloads/
        if not path:
            return path

        split_path = path.split(separator)
        return ('/').join(split_path)

    def is_data_layer_split(self, split_metadata):
        return lib.safe_dict_access(
            split_metadata, ["provenance", "split_creation_source"]
        ) == "CREATED_FROM_DATA_LAYER"

    def _request_list_from_list_of_files(
        self, source_file_itr, project_id: str, artifact_type: ArtifactType,
        artifact_id: str, intra_artifact_path: str,
        scoping_artifact_ids: List[str]
    ):
        for f in source_file_itr:
            # The artifact repo service has rules about what kind of files can be uploaded
            # skip files that start with '.' because they are likely hidden from the user
            # and they probably didn't mean to upload that file.
            if (self.__get_file_name_from_path(f).startswith('.')):
                self.log("Warning - file skipped: " + f)
                continue

            yield from self._build_upload_request(
                f, project_id, artifact_type, artifact_id,
                os.path.join(
                    intra_artifact_path, self.__get_file_name_from_path(f)
                ), scoping_artifact_ids
            )

    def __get_file_name_from_path(self, path: str):
        head, tail = os.path.split(path)
        return tail or os.path.basename(head)

    def _build_exists_request(
        self, project_id: str, artifact_type: ArtifactType, artifact_id: str,
        intra_artifact_path: str, scoping_artifact_ids: List[str]
    ):
        return ar_pb.ExistsRequest(
            project_id=project_id,
            artifact_type=self.__map_artifacttype_to_pb(artifact_type),
            artifact_id=artifact_id,
            intra_artifact_path=intra_artifact_path,
            scoping_artifact_ids=scoping_artifact_ids
        )

    # consider: we can consider exposing this as well - for now I think just exposing file / folder is enough
    def _artifact_exists(
        self, project_id: str, artifact_type: ArtifactType, artifact_id: str,
        intra_artifact_path: str, scoping_artifact_ids: List[str]
    ):
        response = self.communicator.resource_exists(
            self._build_exists_request(
                project_id, artifact_type, artifact_id, intra_artifact_path,
                scoping_artifact_ids
            )
        )
        return response.exists

    def _build_download_request(
        self, src_project_id: str, src_artifact_type: ArtifactType,
        src_artifact_id: str, src_intra_artifact_path: str,
        scoping_artifact_ids: List[str]
    ):
        return ar_pb.GetRequest(
            project_id=src_project_id,
            artifact_type=self.__map_artifacttype_to_pb(src_artifact_type),
            artifact_id=src_artifact_id,
            intra_artifact_path=src_intra_artifact_path,
            max_chunk_size=self.__READ_WRITE_SIZE__,
            scoping_artifact_ids=scoping_artifact_ids
        )

    def _build_delete_request(
        self, project_id: str, artifact_type: ArtifactType, artifact_id: str,
        intra_artifact_path: str, scoping_artifact_ids: List[str]
    ):
        return ar_pb.DeleteRequest(
            project_id=project_id,
            artifact_type=self.__map_artifacttype_to_pb(artifact_type),
            artifact_id=artifact_id,
            intra_artifact_path=intra_artifact_path,
            scoping_artifact_ids=scoping_artifact_ids
        )

    def _build_create_project_metadata_request(
        self, project_name: str, description_json: Optional[str],
        score_type: str, input_data_format: str
    ):
        documentation = ProjectDocumentation()
        if description_json:
            documentation = Parse(description_json, documentation)

        metadata = md_pb.ProjectMetadata(
            name=project_name,
            documentation=documentation,
            settings=md_pb.ProjectLevelSettings(
                score_type=get_qoi_from_string(score_type),
                input_data_format=get_input_data_format_from_string(
                    input_data_format
                )
            )
        )
        return ar_pb.PutMetadataRequest(project=metadata, insert_only=True)

    def _build_create_model_metadata_request(
        self, model_id: str, model_name: str, description: str, project_id: str,
        data_collection_name: str, model_type: str, model_output_type,
        locator: str, nn_attribution_config: Union[RNNAttributionConfig,
                                                   NLPAttributionConfig],
        rnn_ui_config: RNNUIConfig,
        training_metadata: md_pb.ModelTrainingMetadata, tags: Sequence[str],
        insert_only: bool
    ):

        data_collection_id = self.get_data_collection_metadata(
            project_id, data_collection_name=data_collection_name
        ).id if data_collection_name else None
        metadata = md_pb.ModelMetadata(
            id=model_id,
            name=model_name,
            description=description,
            project_id=project_id,
            data_collection_id=data_collection_id,
            model_type=model_type,
            model_output_type=lib.map_model_output_type(model_output_type),
            locator=self.format_intra_artifact_paths_for_linux(locator, os.sep),
            rnn_ui_config=rnn_ui_config,
            training_metadata=training_metadata,
            tags=tags
        )

        if isinstance(nn_attribution_config, RNNAttributionConfig):
            # pylint: disable=E5901
            metadata.rnn_attribution_configuration.CopyFrom(
                nn_attribution_config
            )
        if isinstance(nn_attribution_config, NLPAttributionConfig):
            # pylint: disable=E5901
            metadata.nlp_attribution_configuration.CopyFrom(
                nn_attribution_config
            )
        return ar_pb.PutMetadataRequest(model=metadata, insert_only=insert_only)

    def _build_create_data_collection_metadata_request(
        self,
        project_id,
        data_collection_name,
        feature_transform_type,
        tags,
        description,
        schemas: md_pb.SchemaMetadata = None
    ):
        metadata = md_pb.DataCollectionMetadata(
            name=data_collection_name,
            project_id=project_id,
            tags=tags,
            description=description,
            feature_transform_type=feature_transform_type
        )

        if schemas:
            metadata.schemas.extend(schemas)

        return ar_pb.PutMetadataRequest(
            data_collection=metadata, insert_only=True
        )

    def _build_create_split_metadata_request(
        self, split_name: str, description: str, project_id: str,
        data_collection_name: str, split_type: str, preprocessed_locator: str,
        processed_locator: str, label_locator: str, extra_data_locator: str,
        tags, split_time_range_begin: str, split_time_range_end: str,
        id_column_name: str, split_mode, status
    ):
        data_collection_id = self.get_data_collection_metadata(
            project_id, data_collection_name=data_collection_name
        ).id

        time_range = create_time_range(
            split_time_range_begin, split_time_range_end
        )

        metadata = md_pb.DataSplitMetadata(
            name=split_name,
            description=description,
            project_id=project_id,
            data_collection_id=data_collection_id,
            split_type=split_type,
            preprocessed_locator=self.format_intra_artifact_paths_for_linux(
                preprocessed_locator, os.sep
            ),
            processed_locator=self.format_intra_artifact_paths_for_linux(
                processed_locator, os.sep
            ),
            label_locator=self.format_intra_artifact_paths_for_linux(
                label_locator, os.sep
            ),
            extra_data_locator=self.format_intra_artifact_paths_for_linux(
                extra_data_locator, os.sep
            ),
            provenance=md_pb.DataProvenance(
                split_creation_source=md_pb.SplitCreationSource.CREATED_FROM_CLI
            ),
            tags=tags,
            time_range=time_range,
            unique_id_column_name=id_column_name,
            split_mode=split_mode,
            status=status
        )
        return ar_pb.PutMetadataRequest(split=metadata, insert_only=True)

    def _get_data_split_id_from_name(
        self, project_id: str, data_collection_name: str, data_split_name: str
    ):
        datasplit_metadata = self.get_datasplit_metadata(
            project_id,
            data_collection_name=data_collection_name,
            datasplit_name=data_split_name
        )
        if datasplit_metadata:
            return datasplit_metadata.id
        raise ValueError(
            f"Data split metadata was not for found for project ID \"{project_id}\", data collection \"{data_collection_name}\", data split \"{data_split_name}\"."
        )

    def _build_create_cache_request(
        self, *, project_id, model_id, data_collection_name, split_name,
        background_data_split_name, location, format, score_type, row_count,
        cache_type: md_pb.CacheType,
        explanation_algorithm_type: ExplanationAlgorithmType, client_name,
        client_version
    ):
        data_split_id = self._get_data_split_id_from_name(
            project_id, data_collection_name, split_name
        )
        model_input_spec_truncated = md_pb.ModelInputSpecTruncated(
            row_count=row_count, split_id=data_split_id
        )
        generated_by_info = md_pb.ClientGeneratedByInfo(
            client_name=client_name, client_version=client_version
        )
        metadata = md_pb.CacheMetadata(
            project_id=project_id,
            model_id=model_id,
            model_input_spec_truncated=model_input_spec_truncated,
            score_type=get_qoi_from_string(score_type),
            cache_type=cache_type,
            location=location,
            format=format,
            generated_by=generated_by_info
        )
        if explanation_algorithm_type is not None:
            metadata.explanation_algorithm_type = explanation_algorithm_type
        if background_data_split_name:
            background_data_split_id = self._get_data_split_id_from_name(
                project_id, data_collection_name, background_data_split_name
            )
            metadata.background_data_split_info.id = background_data_split_id
            metadata.background_data_split_info.all = True

        return ar_pb.PutMetadataRequest(cache=metadata, insert_only=True)

    def _build_create_feature_list_metadata_request(
        self, feature_list_pb, insert_only
    ):
        return ar_pb.PutMetadataRequest(
            feature_list=feature_list_pb, insert_only=insert_only
        )

    def __map_artifacttype_to_pb(self, artifact_type: ArtifactType):
        if artifact_type == ArtifactType.model:
            return ar_pb.ArtifactType.MODEL
        elif artifact_type == ArtifactType.datasplit:
            return ar_pb.ArtifactType.DATASPLIT
        elif artifact_type == ArtifactType.documentation:
            return ar_pb.ArtifactType.DOCUMENTATION
        elif artifact_type == ArtifactType.data_collection:
            return ar_pb.ArtifactType.DATACOLLECTION
        elif artifact_type == ArtifactType.project:
            return ar_pb.ArtifactType.PROJECT
        elif artifact_type == ArtifactType.feature_map:
            return ar_pb.ArtifactType.FEATURE_LIST
        elif artifact_type == ArtifactType.data_source:
            return ar_pb.ArtifactType.DATA_SOURCE
        elif artifact_type == ArtifactType.materialized_file:
            return ar_pb.MATERIALIZED_FILE
        elif artifact_type == ArtifactType.cache:
            return ar_pb.CACHE
        raise ValueError("Invalid artifact type: " + str(artifact_type))
