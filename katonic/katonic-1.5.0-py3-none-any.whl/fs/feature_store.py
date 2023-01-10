#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#
import base64
import os
from collections import Counter
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import pandas as pd
from colorama import Fore
from colorama import Style
from katonic.fs import utils
from katonic.fs.core.offline_stores.dataframe_source import DataFrameSource
from katonic.fs.core.offline_stores.offline_store import RetrievalJob
from katonic.fs.core.online_stores.online_response import OnlineResponse
from katonic.fs.core.provider import get_provider
from katonic.fs.core.provider import Provider
from katonic.fs.entities.entity import Entity
from katonic.fs.entities.feature_view import FeatureView
from katonic.fs.errors import EntityNotFoundException
from katonic.fs.errors import FeatureViewNotFoundException
from katonic.fs.registry import Registry
from katonic.fs.repo_config import load_repo_config
from katonic.fs.repo_config import RepoConfig
from katonic.version import get_version
from pydantic.types import StrictStr


class FeatureStore:

    """
    A FeatureStore object is used to define, create, and retrieve features.

    Args:
        user_name: person who is initialized the feature store.
        project_name: name of the project going to use on feature store.
        description (Optional): description of the project.
    """

    config: RepoConfig
    repo_path: Path
    _registry: Registry

    HUDI_FORMAT = "hudi"
    HIVE_FORMAT = "hive"
    SPARK_FORMAT = "spark"
    DELTA_FORMAT = "delta"

    MERGE = "merge"
    APPEND = "append"
    OVERWRITE = "overwrite"

    def __init__(
        self,
        project_name: str,
        user_name: str,
        description: Optional[str] = None,
    ):
        """
        Creates a FeatureStore object.
        """

        self.repo_path = Path("/kfs_private/")
        credentials = self.__get_local_config(
            project_name=project_name,
            description=description,
            user_name=user_name,
            repo_path=self.repo_path,
        )

        self.config = load_repo_config(credentials)

        registry_config = self.config.get_registry_config()
        self._registry = Registry(registry_config, repo_path=self.repo_path)
        self._provider = get_provider(self.config, self.repo_path)
        self._registry._initialize_registry()

    @property
    def project(self) -> StrictStr:
        """Gets the project of this feature store."""
        return self.config.project

    @property
    def provider(self) -> Any:
        """Gets the provider of this feature store."""
        return self.config.provider

    @property
    def registry(self) -> Registry:
        """Gets the registry of this feature store."""
        return self._registry

    def _get_provider(self) -> Provider:
        # TODO: Bake self.repo_path into self.config so that we dont only have one interface to paths
        return self._provider

    def list_entities(self) -> List[str]:
        """
        Retrieves the list of entities from the registry.

        Returns:
            A list of entities.
        """
        return self.registry.list_entities(self.project)  # type: ignore

    def list_feature_views(self) -> List[str]:
        """
        Retrieves the list of feature views from the registry.

        Returns:
            A list of entities.
        """
        return self.registry.list_feature_views(self.project)  # type: ignore

    def get_registry_info(
        self, project_name: Optional[str] = "", user_name: Optional[str] = ""
    ) -> pd.DataFrame:
        """
        Retrieves a pandas data frame related to the given user name and project.

        Returns:
            A pandas DataFrame.

        Raises:
            TypeError: If neither of user_name and project_name are specified.
        """
        if project_name or user_name:
            return self.registry.get_registry_info(
                project_name,
                user_name,
            )
        else:
            raise TypeError(
                "get_registry_info() missing 1 required positional argument: 'project_name' or 'user_name'"
            )

    def get_feature_view(self, name: str) -> FeatureView:
        """
        Retrieves a feature view.

        Args:
            name: Name of feature view
            project: Project name that this feature view belongs to

        Returns:
            Returns either the specified feature view, or raises an exception if
            none is found
        """
        return self.registry.get_feature_view(
            name,
            self.project,
        )

    def write_table(
        self,
        objects: Union[
            Entity,
            FeatureView,
            List[Union[FeatureView, Entity]],
        ],
    ):
        """Writes feature table to an offline store"""
        from colorama import Fore, Style

        if not isinstance(objects, Iterable):
            objects = [objects]

        entities_to_update = list(filter(lambda ob: isinstance(ob, Entity), objects))
        self.views_to_update = list(
            filter(lambda ob: isinstance(ob, FeatureView), objects)
        )

        _validate_feature_views(self.views_to_update)

        if len(self.views_to_update) + len(entities_to_update) != len(objects):  # type: ignore
            raise ValueError("Unknown object type provided as part of write table.")

        for entity in entities_to_update:
            print(
                f"Registered entity {Style.BRIGHT + Fore.GREEN}{entity.name}{Style.RESET_ALL}"
            )

        for view in self.views_to_update:
            print(
                f"Registered feature view {Style.BRIGHT + Fore.GREEN}{view.name}{Style.RESET_ALL}"
            )

        for name in [view.name for view in self.views_to_update]:
            print(
                f"Deploying infrastructure for {Style.BRIGHT + Fore.GREEN}{name}{Style.RESET_ALL}"
            )

        # lets take feature view as a single for now, later for multi fv we can add for loop to register all fvs.
        data = None
        if (
            len(self.views_to_update) == 1
            and type(self.views_to_update[0].batch_source) == DataFrameSource
        ):
            data = self.views_to_update[0].batch_source.data_df

        features_list = self._get_provider().write_offline_features_data(
            project=self.project,
            data=data,
            tables_to_keep=self.views_to_update,
            entities_to_keep=entities_to_update,
        )

        self._get_provider().update_infra(
            project=self.project,
            tables_to_keep=self.views_to_update,
            entities_to_keep=entities_to_update,
        )

        fv = []
        for view in self.views_to_update:
            view = view.to_dict()
            view["features"] = features_list
            fv.append(FeatureView.from_dict(view))

        for view, ent in zip(fv, entities_to_update):
            self.registry.apply_feature_view(view, ent, config=self.config)

    def get_historical_features(
        self,
        entity_df: Union[pd.DataFrame, str],
        feature_view: List[str],
        features: List[str],
    ) -> RetrievalJob:
        """Enrich an entity dataframe with historical feature values for either training or batch scoring.

        This method joins historical feature data from one or more feature views to an entity dataframe by using a time
        travel join.

        Args:
            entity_df (Union[pd.DataFrame, str]): An entity dataframe is a collection of rows containing all entity
                columns (e.g., customer_id, driver_id) on which features need to be joined, as well as a event_timestamp
                column used to ensure point-in-time correctness. Either a Pandas DataFrame can be provided or a string
                SQL query. The query must be of a format supported by the configured offline store (e.g., BigQuery)
            features: A list of features, that should be retrieved from the offline store.
                Either a list of string feature names or a single feature name.
            feature_view: Name of the feature view that you want to retrieve the features from.

        Returns:
            RetrievalJob which can be used to materialize the results.

        Raises:
            FeatureViewNotFoundException: If specified feature view not found in registry.
        """
        feature_views = [self.get_feature_view(fv_name) for fv_name in feature_view]

        for fv in feature_views:
            if fv.name in feature_view:
                feature_ids = _feature_id(feature_view, features)
            else:
                raise FeatureViewNotFoundException(feature_view)

        return self._get_provider().get_historical_features(
            self.config,
            feature_views,
            feature_ids,
            entity_df,
            self.registry,
            self.project,
        )

    def version(self) -> str:
        """Returns the version of the current Katonic SDK."""
        return get_version()  # type: ignore

    def publish_table(
        self,
        start_ts: datetime,
        end_ts: datetime,
        feature_view: List[str],
    ) -> None:
        """
        Writes/Materialize data from the offline store into the online store.

        This method loads feature data in the specified interval from either
        the specified feature views, or all feature views if none are specified,
        into the online store where it is available for online serving.

        Args:
            start_date (datetime): Start date for time range of data to materialize into the online store
            end_date (datetime): End date for time range of data to materialize into the online store
            feature_views (List[str]): Optional list of feature view names. If selected, will only run
                materialization for the specified feature views.

        Examples:
            Materialize all features into the online store over the interval
            from 3 hours ago to 10 minutes ago.

            >>> from katonic.fs import FeatureStore
            >>> from datetime import datetime, timedelta
            >>> fs = FeatureStore(user_name = "user_name", project_name = "project_name")
            >>> fs.publish_table(
            ...     start_date=datetime.utcnow() - timedelta(hours=3), end_date=datetime.utcnow() - timedelta(minutes=10)
            ... )
            Materializing...
            <BLANKLINE>
            ...
        """
        start_date: datetime = utils.make_tzaware(start_ts)
        end_date: datetime = utils.make_tzaware(end_ts)

        if start_date > end_date:
            raise ValueError(
                f"The given start_date {start_date} is greater than the given end_date {end_date}."
            )

        feature_views_to_materialize = [
            self.get_feature_view(fv_name) for fv_name in feature_view
        ]

        _print_materialization_log(
            start_date,
            end_date,
            len(feature_views_to_materialize),
            self.config.online_store.type,
        )
        provider = self._get_provider()

        # TODO paging large loads
        for feature_view in feature_views_to_materialize:

            provider.materialize_single_feature_view(
                config=self.config,
                feature_view=feature_view,
                start_date=start_date,
                end_date=end_date,
                registry=self.registry,
                project=self.project,
            )

    def get_online_features(
        self,
        feature_view: List[str],
        features: List[str],
        entity_rows: List[Dict[str, Any]],
    ) -> OnlineResponse:
        """
        Retrieves the latest online feature data.

        Note: This method will download the full feature registry the first time it is run. If you are using a
        remote registry like GCS or S3 then that may take a few seconds. The registry remains cached up to a TTL
        duration (which can be set to infinity). If the cached registry is stale (more time than the TTL has
        passed), then a new registry will be downloaded synchronously by this method. This download may
        introduce latency to online feature retrieval. In order to avoid synchronous downloads, please call
        refresh_registry() prior to the TTL being reached. Remember it is possible to set the cache TTL to
        infinity (cache forever).

        Args:
            features: List of feature names in string format.
            feature_view: List of feature view name.
            entity_rows: A list of dictionaries where each key-value is an entity-name, entity-value pair.

        Returns:
            OnlineResponse containing the feature data in records.

        Raises:
            Exception: No entity with the specified name exists.

        Examples:
            Materialize all features into the online store over the interval
            from 3 hours ago to 10 minutes ago, and then retrieve these online features.

            >>> from katonic.fs import FeatureStore
            >>> fs = FeatureStore(user_name="username", project_name="project name")
            >>> online_response = fs.get_online_features(
            ...     features=["conv_rate", "acc_rate", "avg_daily_trips"],
            ...     feature_view = ["feature_view_name],
            ...     entity_rows=[{"driver_id": 1001}, {"driver_id": 1002}, {"driver_id": 1003}, {"driver_id": 1004}],
            ... ).to_dict()
        """
        _feature_refs = _feature_id(feature_view, features)
        all_feature_views = [self.get_feature_view(fv_name) for fv_name in feature_view]

        _validate_feature_refs(_feature_refs)
        grouped_refs = _group_feature_refs(_feature_refs, all_feature_views)

        provider = self._get_provider()
        entity_name_to_join_key_map = {
            entities: entities
            for view in all_feature_views
            for entities in view.entities
        }

        join_key_rows = []
        for row in entity_rows:
            join_key_row = {}
            for entity_name, entity_value in row.items():
                try:
                    join_key = entity_name_to_join_key_map[entity_name]
                except KeyError as e:
                    raise EntityNotFoundException(entity_name, self.project) from e
                join_key_row[join_key] = entity_value
            if join_key_row:
                # May be empty if this entity row was request data
                join_key_rows.append(join_key_row)

        requested_feature = []
        for table, requested_features in grouped_refs:
            requested_feature = requested_features
            result_rows = self._populate_result_rows_from_feature_view(
                entity_keys=join_key_rows,
                provider=provider,
                requested_features=requested_features,
                table=table,
            )
            break
        for entity in entity_name_to_join_key_map:
            requested_feature = requested_feature + [entity]

        # issue with multiple feature views/feature table data

        return OnlineResponse(
            online_response=result_rows,
            requested_features=requested_feature,
        )

    def _populate_result_rows_from_feature_view(
        self,
        entity_keys: List[Dict[str, Any]],
        provider: Provider,
        requested_features: List[str],
        table: FeatureView,
    ) -> List[
        Tuple[Optional[datetime], Optional[Dict[str, Any]], Optional[Dict[str, Any]]]
    ]:
        result_rows: List[
            Tuple[
                Optional[datetime], Optional[Dict[str, Any]], Optional[Dict[str, Any]]
            ]
        ] = []
        read_rows = provider.online_read(
            config=self.config,
            table=table,
            entity_keys=entity_keys,
            requested_features=requested_features,
        )
        # Each row is a set of features for a given entity key
        for read_row, entity_key in zip(read_rows, entity_keys):
            row_ts, feature_data = read_row

            if feature_data is None:
                raise ValueError(
                    "No data found related to given features and entities id."
                )
            result_rows.append((row_ts, feature_data, entity_key))

        return result_rows

    def __encode_py(self, message):
        message_bytes = message.encode("ascii")
        base64_bytes = base64.b64encode(message_bytes)
        return base64_bytes.decode("ascii")

    def __decode_py(self, message):
        base64_bytes = message.encode("ascii")
        message_bytes = base64.b64decode(base64_bytes)
        return message_bytes.decode("ascii")

    def __get_local_config(
        self,
        project_name: str,
        description: Optional[str],
        user_name: str,
        repo_path: Path,
    ) -> Dict[str, Any]:

        return {
            "user_name": user_name or None,
            "project": project_name,
            "description": description or None,
            "registry": {
                "type": "postgres",
                "db_name": self.__decode_py(os.getenv("DB_NAME")),
                "host": self.__decode_py(os.getenv("HOST")),
                "port": 5432,
                "user": self.__decode_py(os.getenv("USER")),
                "password": self.__decode_py(os.getenv("POSTGRES_PASSWORD")),
                "db_schema": self.__decode_py(os.getenv("DB_SCHEMA")),
            },
            "repo_path": repo_path,
            "offline_store": {"type": "file", "path": "data/offline_store.parquet"},
            "online_store": {
                "type": "redis",
                "connection_string": f"{self.__decode_py(os.getenv('REDIS_HOST'))}:6379:{self.__decode_py(os.getenv('REDIS_PASSWORD'))}",
            },
        }


def _print_materialization_log(
    start_date, end_date, num_feature_views: int, online_store: str
):
    if start_date:
        print(
            f"Materializing {Style.BRIGHT + Fore.GREEN}{num_feature_views}{Style.RESET_ALL} feature views"
            f" from {Style.BRIGHT + Fore.GREEN}{start_date.replace(microsecond=0).astimezone()}{Style.RESET_ALL}"
            f" to {Style.BRIGHT + Fore.GREEN}{end_date.replace(microsecond=0).astimezone()}{Style.RESET_ALL}"
            f" into the {Style.BRIGHT + Fore.GREEN}{online_store}{Style.RESET_ALL} online store.\n"
        )
    else:
        print(
            f"Materializing {Style.BRIGHT + Fore.GREEN}{num_feature_views}{Style.RESET_ALL} feature views"
            f" to {Style.BRIGHT + Fore.GREEN}{end_date.replace(microsecond=0).astimezone()}{Style.RESET_ALL}"
            f" into the {Style.BRIGHT + Fore.GREEN}{online_store}{Style.RESET_ALL} online store.\n"
        )


def _validate_feature_views(feature_views: List[FeatureView]):
    """Verify feature views have case-insensitively unique names"""
    fv_names = set()
    for fv in feature_views:
        case_insensitive_fv_name = fv.name.lower()
        if case_insensitive_fv_name in fv_names:
            raise ValueError(
                f"""
                More than one feature view with name {case_insensitive_fv_name} found. Please ensure that all feature view names are case-insensitively unique.
                """
            )
        else:
            fv_names.add(case_insensitive_fv_name)


def _validate_feature_refs(feature_refs: List[str]):

    feature_names = [ref.split(":")[1] if ":" in ref else ref for ref in feature_refs]
    # collided_feature_names
    [ref for ref, occurrences in Counter(feature_names).items() if occurrences > 1]
    # need to add message for feature names crashes...


def _group_feature_refs(
    features: List[str],
    all_feature_views: List[FeatureView],
) -> List[Tuple[FeatureView, List[str]]]:
    """Get list of feature views and corresponding feature names based on feature references"""

    # view name to view feature view
    view_index = {view.name: view for view in all_feature_views}

    # view name to feature names
    views_features = defaultdict(list)

    for ref in features:
        view_name, feat_name = ref.split(":")
        if view_name in view_index:
            views_features[view_name].append(feat_name)
        else:
            raise FeatureViewNotFoundException(view_name)

    fvs_result: List[Tuple[FeatureView, List[str]]] = []

    for view_name, feature_names in views_features.items():
        fvs_result.append((view_index[view_name], feature_names))
    return fvs_result


def _feature_id(feature_views: List[str], all_features: List[str]):
    """
    It will create a feature_view:feature pair for all the features and feature views.
    """
    if len(feature_views) == 1:
        feature_view_name = feature_views[0]
        return list(map(lambda feature: f"{feature_view_name}:{feature}", all_features))
