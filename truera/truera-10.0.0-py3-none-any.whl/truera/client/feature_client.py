from collections import defaultdict
import itertools
import json
import logging
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set

import click
from google.protobuf.json_format import Parse

from truera.client.client_pb_utils import parse_message_from_file
from truera.client.client_utils import NotSupportedFileTypeException
from truera.client.errors import NotFoundError
from truera.client.errors import SimpleException
from truera.client.public.communicator.http_communicator import \
    AlreadyExistsError
import truera.client.services.artifactrepo_client as ar_client
from truera.protobuf.public import feature_pb2 as feature_pb
from truera.utils.config_merge import MergeDictionaryConfiguration


class InvalidMapException(SimpleException):
    pass


def validate_feature_map_types(
    pre_to_post_feature_map: Mapping[str, Sequence[str]]
):
    if not all(
        isinstance(val, (list, tuple))
        for val in pre_to_post_feature_map.values()
    ):
        raise ValueError(
            "`pre_to_post_feature_map` must map each pre-transform column (str) to all associated post-transform columns (list)"
        )


def validate_feature_map_one_to_many(
    pre_to_post_feature_map: Optional[Mapping[str, Sequence[str]]]
) -> bool:
    if pre_to_post_feature_map:
        post_features = list()
        for features in pre_to_post_feature_map.values():
            for f in features:
                if f in post_features:
                    raise ValueError(
                        "Feature transform with many-to-many mapping is not supported."
                    )
                else:
                    post_features.append(f)


class FeatureClient(object):

    def __init__(self, ar_client: ar_client.ArtifactRepoClient, logger):
        self.logger = logger
        self.ar_client = ar_client
        self.merge_tool = MergeDictionaryConfiguration

    def get_feature_list(self, project_name: str, data_collection_name: str):
        try:
            return self.ar_client.get_feature_list(
                project_name, data_collection_name
            )
        except NotFoundError:
            return None

    def get_pre_to_post_feature_map(
        self, project_name: str, data_collection_name: str
    ):
        feature_list = self.get_feature_list(project_name, data_collection_name)
        if not feature_list:
            return None
        return {
            feature["name"]: feature["derived_model_readable_columns"]
            for feature in feature_list["features"]
        }

    def get_feature_description_map(
        self, project_name: str, data_collection_name: str
    ):
        feature_list = self.get_feature_list(project_name, data_collection_name)
        if not feature_list:
            return None
        return {
            feature["name"]: feature["description"]
            for feature in feature_list["features"]
        }

    # Assumes the caller has checked that the file is valid, the project, and data_collection exist.
    # pylint: disable=no-member
    def upload_feature_list_metadata(
        self, feature_description_file, project_name, data_collection_name,
        force
    ):
        feature_list = feature_pb.FeatureList()

        try:
            parse_message_from_file(feature_description_file, feature_list)
        except NotSupportedFileTypeException as e:
            click.echo(e.message)
            raise

        project_metadata = self.ar_client.get_project_metadata(
            project_name, as_json=False
        )
        feature_list.project_id = project_metadata.id

        data_collection_id = self.ar_client.get_data_collection_metadata(
            project_name, data_collection_name=data_collection_name
        ).id

        feature_list.data_collection_id = data_collection_id

        return self.ar_client.upload_feature_list_metadata(
            feature_list, insert_only=(not force)
        )

    def _build_feature_list_proto(
        self, project_name: str, data_collection_name: str, feature_list: Dict
    ) -> feature_pb.FeatureList:
        feature_list_proto = Parse(
            json.dumps(feature_list), feature_pb.FeatureList()
        )
        project_metadata = self.ar_client.get_project_metadata(
            project_name, as_json=False
        )
        feature_list_proto.project_id = project_metadata.id
        data_collection_id = self.ar_client.get_data_collection_metadata(
            project_metadata.id, data_collection_name=data_collection_name
        ).id
        feature_list_proto.data_collection_id = data_collection_id
        return feature_list_proto

    def _combine_feature_metadata(
        self, pre_features: Sequence[str],
        pre_to_post_feature_map: Optional[Mapping[str, Sequence[str]]],
        feature_description_map: Optional[Mapping[str, str]],
        group_to_feature_map: Optional[Mapping[str, Set[str]]],
        only_update_metadata: bool, previous_feature_list: Mapping[str, Any]
    ) -> Dict:
        if feature_description_map is None:
            feature_description_map = dict()
        if group_to_feature_map is None:
            group_to_feature_map = dict()
        feature_to_groups_map = defaultdict(list)
        if group_to_feature_map:
            # invert the group details map from group -> set(cols) to  col -> set(groups)
            for group in group_to_feature_map:
                cols = group_to_feature_map[group]
                for c in cols:
                    feature_to_groups_map[c].append(group)
        features = []
        for col in pre_features:
            feature = {"name": col}
            if col in feature_description_map:
                feature["description"] = feature_description_map[col]
            if col in feature_to_groups_map:
                feature["groups"] = feature_to_groups_map[col]

            if pre_to_post_feature_map is not None:
                if col not in pre_to_post_feature_map:
                    raise InvalidMapException(
                        f"Pre-transform feature {col} was not found in provided pre/post-transform feature map."
                    )
                feature["derived_model_readable_columns"
                       ] = pre_to_post_feature_map[col]

            else:
                if not only_update_metadata or len(
                    previous_feature_list.get("features")
                ) == 0:
                    feature["derived_model_readable_columns"] = [col]
                else:
                    for f in previous_feature_list.get("features"):
                        if f.get("name") == col:
                            feature["derived_model_readable_columns"] = f.get(
                                "derived_model_readable_columns", [col]
                            )
                            break

            features.append(feature)
        return features

    def upload_feature_description_and_group_metadata(
        self,
        project_name: str,
        data_collection_name: str,
        pre_features: Sequence[str],
        post_features: Sequence[str] = None,
        feature_description_map: Optional[Mapping[str, str]] = None,
        pre_to_post_feature_map: Optional[Mapping[str, Sequence[str]]] = None,
        group_to_feature_map: Optional[Mapping[str, Set[str]]] = None,
        missing_values: Optional[Sequence[str]] = None,
        force: bool = False,
        only_update_metadata: bool = True
    ):
        previous_feature_list = self.get_feature_list(
            project_name, data_collection_name
        ) or {}
        override = {}
        if missing_values:
            if not force and previous_feature_list.get("missing_values"):
                raise AlreadyExistsError(
                    f"Missing values already present for project `{project_name}` in data-collection `{data_collection_name}`.  Pass force=True to overwrite."
                )
            override["missing_values"] = missing_values

        if feature_description_map or pre_to_post_feature_map or group_to_feature_map:
            if not force and previous_feature_list.get("features"):
                raise AlreadyExistsError(
                    f"Feature list already present for project `{project_name}` in data-collection `{data_collection_name}`.  Pass force=True to overwrite."
                )
            override["features"] = self._combine_feature_metadata(
                pre_features,
                pre_to_post_feature_map,
                feature_description_map,
                group_to_feature_map,
                only_update_metadata=only_update_metadata,
                previous_feature_list=previous_feature_list
            )
        feature_list = self.merge_tool.subst_merge(
            default=previous_feature_list, override=override
        )
        feature_list_proto = self._build_feature_list_proto(
            project_name, data_collection_name, feature_list
        )

        pre_transform_columns_from_map = [
            feature.name for feature in feature_list_proto.features
        ]
        post_transform_columns_from_map = [
            post_transform_feature for feature in feature_list_proto.features
            for post_transform_feature in feature.derived_model_readable_columns
        ]
        post_features = post_transform_columns_from_map if only_update_metadata else post_features
        FeatureClient.verify_feature_map(
            pre_features,
            pre_features if post_features is None else post_features,
            pre_transform_columns_from_map, post_transform_columns_from_map,
            self.logger
        )
        return self.ar_client.upload_feature_list_metadata(
            feature_list_proto, insert_only=False
        )

    @staticmethod
    def verify_feature_map_from_map_file(
        map_file,
        pre_transform_file,
        post_transform_file,
        logger: logging.Logger,
        *,
        id_column: Optional[str] = None
    ):
        feature_list = feature_pb.FeatureList()
        try:
            # Verifies that the file is a valid type and can be parsed into the proto
            parse_message_from_file(map_file, feature_list)
        except NotSupportedFileTypeException as e:
            click.echo(e.message)
            raise

        with open(pre_transform_file) as fp:
            pre_transform_columns_from_header = [
                c.strip() for c in fp.readline().split(",")
            ]

        with open(post_transform_file) as fp:
            post_transform_columns_from_header = [
                c.strip() for c in fp.readline().split(",")
            ]

        pre_transform_columns_from_map = [
            feature.name for feature in feature_list.features
        ]
        post_transform_columns_from_map = [
            post_transform_feature for feature in feature_list.features
            for post_transform_feature in feature.derived_model_readable_columns
        ]

        FeatureClient.verify_feature_map(
            pre_transform_columns_from_header,
            post_transform_columns_from_header,
            pre_transform_columns_from_map,
            post_transform_columns_from_map,
            logger,
            id_column=id_column
        )

    @staticmethod
    def verify_feature_map_from_dict(
        pre_to_post_feature_map: Mapping[str, Sequence[str]],
        logger: logging.Logger
    ):
        validate_feature_map_types(pre_to_post_feature_map)
        validate_feature_map_one_to_many(pre_to_post_feature_map)
        pre_columns_from_map = list(pre_to_post_feature_map.keys())
        post_columns_from_map = list(
            itertools.chain.from_iterable(pre_to_post_feature_map.values())
        )
        FeatureClient.verify_feature_map(
            None, None, pre_columns_from_map, post_columns_from_map, logger
        )

    @staticmethod
    def verify_feature_map(
        pre_transform_columns_from_header: Optional[Sequence[str]],
        post_transform_columns_from_header: Optional[List[str]],
        pre_transform_columns_from_map: List[str],
        post_transform_columns_from_map: List[str],
        logger: logging.Logger,
        *,
        id_column: Optional[str] = None
    ):

        logger.debug(
            f"Pre-transform columns provided in feature map: {pre_transform_columns_from_map}"
        )
        logger.debug(
            f"Post-transform columns provided in feature map: {post_transform_columns_from_map}"
        )

        # Verify that pre transform column names are unique
        FeatureClient._check_unique_fail_if_not(
            pre_transform_columns_from_map, "pre transform columns from map"
        )

        # Verify that post transform column names are unique across all features
        # This is enough to guarantee that map is one to many and not many to many
        FeatureClient._check_unique_fail_if_not(
            post_transform_columns_from_map, "post transform columns from map"
        )

        if pre_transform_columns_from_header:
            # Verifies that the file's header does not repeat columns
            FeatureClient._check_unique_fail_if_not(
                pre_transform_columns_from_header,
                "header for pre transform file"
            )

            # Verify that all columns in the pre transform header occur in the map
            # Devnote - A more permissive behavior may be to assume those that do not occur are not used.
            columns_in_pre_transform_header_not_addressed = [
                col for col in pre_transform_columns_from_header if
                col not in pre_transform_columns_from_map and col != id_column
            ]

            if len(columns_in_pre_transform_header_not_addressed) > 0:
                raise InvalidMapException(
                    f"Columns occurred in pre transform header that was not in feature map: {columns_in_pre_transform_header_not_addressed}"
                )

            # Verify that all pre transform columns in the map occur in the pre transform header
            pre_columns_in_map_not_in_header = [
                col for col in pre_transform_columns_from_map
                if col not in pre_transform_columns_from_header
            ]

            if len(pre_columns_in_map_not_in_header) > 0:
                raise InvalidMapException(
                    f"Columns occurred in pre/post feature map that was not in pre transform header: {pre_columns_in_map_not_in_header}"
                )

        if post_transform_columns_from_header:
            # Verifies that the file's header does not repeat columns
            FeatureClient._check_unique_fail_if_not(
                post_transform_columns_from_header,
                "header for post transform file"
            )

            # Verify that all columns in the post transform header occur in the map
            columns_in_post_transform_header_not_addressed = [
                col for col in post_transform_columns_from_header if
                col not in post_transform_columns_from_map and col != id_column
            ]

            if len(columns_in_post_transform_header_not_addressed) > 0:
                message = "Columns occurred in post transform header that was not in feature map: " + str(
                    columns_in_post_transform_header_not_addressed
                )
                raise InvalidMapException(message)

            # Verify that all post transform columns in the map occur in the post transform header
            post_columns_in_map_not_in_header = [
                col for col in post_transform_columns_from_map
                if col not in post_transform_columns_from_header
            ]

            if len(post_columns_in_map_not_in_header) > 0:
                raise InvalidMapException(
                    f"Columns occurred in pre/post feature map that was not in post transform header: {post_columns_in_map_not_in_header}"
                )

    @staticmethod
    def _check_unique_fail_if_not(list_of_columns, location_string_for_error):
        set_of_columns = set(list_of_columns)

        if len(set_of_columns) != len(list_of_columns):
            repeated_columns = [
                col for col in set_of_columns if list_of_columns.count(col) > 1
            ]
            message = "Column name was repeated in " + location_string_for_error + ". Repeated columns: " + str(
                repeated_columns
            ) + "."
            raise InvalidMapException(message)
