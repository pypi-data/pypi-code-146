#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
from urllib.parse import urlparse

from katonic.fs import importer
from katonic.fs.entities.entity import Entity
from katonic.fs.entities.feature_view import FeatureView
from katonic.fs.entities.feature_table import FeatureTable
from katonic.fs.errors import FeatureViewNotFoundException
from katonic.fs.repo_config import RegistryConfig, RepoConfig

REGISTRY_SCHEMA_VERSION = "1"


REGISTRY_STORE_CLASS_FOR_TYPE = {
    "PostgreSQLRegistryStore": "katonic.fs.core.registry.postgres.PostgreSQLRegistryStore",
    "LocalRegistryStore": "katonic.fs.core.registry.local.LocalRegistryStore",
}

REGISTRY_STORE_CLASS_FOR_SCHEME = {
    "postgres": "PostgreSQLRegistryStore",
    "file": "LocalRegistryStore",
    "": "LocalRegistryStore",
}


def get_registry_store_class_from_type(registry_store_type: str):
    if not registry_store_type.endswith("RegistryStore"):
        raise Exception('Registry store class name should end with "RegistryStore"')
    if registry_store_type in REGISTRY_STORE_CLASS_FOR_TYPE:
        registry_store_type = REGISTRY_STORE_CLASS_FOR_TYPE[registry_store_type]
    module_name, registry_store_class_name = registry_store_type.rsplit(".", 1)

    return importer.get_class_from_type(
        module_name, registry_store_class_name, "RegistryStore"
    )


def get_registry_store_class_from_scheme(registry_path: str):
    uri = urlparse(registry_path)
    if uri.scheme not in REGISTRY_STORE_CLASS_FOR_SCHEME:
        raise Exception(
            f"Registry path {registry_path} has unsupported scheme {uri.scheme}. "
            f"Supported schemes are file, s3 and gs."
        )
    registry_store_type = REGISTRY_STORE_CLASS_FOR_SCHEME[uri.scheme]
    return get_registry_store_class_from_type(registry_store_type)


class Registry:
    """
    Registry: A registry allows for the management and persistence of feature definitions and related metadata.
    """

    def __init__(self, registry_config: RegistryConfig, repo_path: Path):
        """
        Create the Registry object.

        Args:
            registry_config: RegistryConfig object containing the destination path and cache ttl,
            repo_path: Path to the base of the feature store repository
            or where it will be created if it does not exist yet.
        """
        registry_store_type = registry_config.registry_store_type
        registry_path = registry_config.path

        self._registry_name = "registry"

        if registry_store_type is None:
            cls = get_registry_store_class_from_scheme(registry_path)
        else:
            cls = get_registry_store_class_from_type(str(REGISTRY_STORE_CLASS_FOR_SCHEME[registry_store_type]))

        self._registry_store = cls(registry_config, repo_path)

    def _initialize_registry(self):
        """Explicitly initializes the registry with an empty table if it doesn't exist."""

        table_query = f"""
                        CREATE TABLE IF NOT EXISTS {self._registry_name} (
                        id SERIAL PRIMARY KEY,
                        project_name VARCHAR(100) NOT NULL,
                        user_name VARCHAR(100) NOT NULL,
                        description VARCHAR DEFAULT NULL,
                        feature_table VARCHAR(200) NOT NULL,
                        feature_table_version INT DEFAULT 1,
                        created TEXT DEFAULT CURRENT_TIMESTAMP,
                        last_modified TEXT DEFAULT CURRENT_TIMESTAMP,
                        last_modified_by VARCHAR(100) NOT NULL,
                        primary_key VARCHAR NOT NULL,
                        no_of_features INTEGER NOT NULL,
                        features TEXT NOT NULL,
                        event_timestamp_column VARCHAR NOT NULL,
                        created_timestamp_column VARCHAR NOT NULL,
                        data_source JSON NOT NULL,
                        offline_store JSON NOT NULL,
                        online_store JSON NOT NULL,
                        type VARCHAR DEFAULT 'CACHED',
                        online VARCHAR DEFAULT 'NO',
                        stage VARCHAR(200) DEFAULT 'DEVELOPMENT',
                        feature_views JSON NOT NULL
                        );
                    """

        index_query = f"""
                        CREATE INDEX IF NOT EXISTS {self._registry_name}_ek ON {self._registry_name} (id);
                      """

        self._registry_store.create_registry(table_query, index_query)

    def list_entities(self, project: str) -> List[str]:
        """
        Retrieve a list of entities from the registry

        Args:
            project: Filter entities based on project name

        Returns:
            List of entities
        """
        query = f"SELECT primary_key FROM {self._registry_name} WHERE (project_name='{project}');"

        return self._registry_store.get_registry(query)

    def get_registry_info(self, project: str = '', user: str = '') -> Dict:
        """
        Retrieves a pandas data frame related to the given user name and project.

        Returns:
            A pandas DataFrame.
        """
        key = 'AND' if project and user else 'OR'
        context = f"WHERE (project_name='{project}' {key} user_name='{user}')" if project or user else ''
        query = f"SELECT * FROM {self._registry_name} {context};"

        return self._registry_store.get_registry(query)

    def apply_feature_table(
        self, feature_table: FeatureTable, entitiy: Entity, config: RepoConfig
    ):
        """
        Registers a single feature table with feature store

        Args:
            feature_table: Feature table that will be registered
            project: Feature store project that this feature table belongs to
            commit: Whether the change should be persisted immediately
        """
        feature_table.is_valid()
        feature_table_dict = feature_table.to_dict()
        feature_table_dict["project"] = config.project
        feature_table_dict["offline_store"] = {}
        feature_table_dict["offline_store"]["store"] = _table_id(config.project, feature_table_dict)
        feature_table_dict["offline_store"]["cloud"] = 'FileSystem'
        feature_table_dict["offline_store"]["storage"] = config.offline_store.type
        feature_table_dict["online_store"] = {}
        feature_table_dict["online_store"]["store"] = _table_id(config.project, feature_table_dict)
        feature_table_dict["online_store"]["cloud"] = 'FileSystem'
        feature_table_dict["online_store"]["storage"] = config.online_store.type

        feature_table_version: int = 1
        no_of_features: int = (len(feature_table_dict["features"]) + len(feature_table_dict["entities"]) +
                               len([feature_table_dict["batch_source"]["event_timestamp_column"], feature_table_dict["batch_source"]["created_timestamp_column"]]))

        n = "%s"

        update_query = (f"""
                                UPDATE {self._registry_name}
                                SET features = {n}, feature_table = {n}, feature_table_version = {n}, last_modified = {n}, 
                                last_modified_by = {n}, no_of_features = {n}, data_source = {n}, stage = {n}
                                WHERE (primary_key = {n} AND project_name = {n})
                        """,
                        (
                            # SET
                            json.dumps(feature_table_dict["features"]),
                            _table_id(config.project, feature_table_dict),
                            feature_table_version,
                            str(datetime.now()),
                            config.user_name,
                            no_of_features,
                            feature_table_dict["batch_source"],
                            "UPDATED FEATURE VIEW",
                            # WHERE
                            feature_table_dict["entities"],
                            feature_table_dict["project"],
                        ),
                        )

        insert_query = (f"""
                                INSERT OR IGNORE INTO {self._registry_name}
                                (project_name, user_name, description, feature_table, feature_table_version, created, 
                                last_modified, last_modified_by, primary_key, no_of_features, features, event_timestamp_column, 
                                created_timestamp_column, data_source, offline_store, online_store, online, stage)
                                VALUES ({n}, {n}, {n}, {n}, {n}, {n}, {n}, {n}, {n}, {n}, {n}, {n}, {n}, {n}, {n}, {n}, {n}, {n})
                        """,
                        (
                            str(feature_table_dict["project"]),
                            str(config.user_name),
                            str(config.description),
                            _table_id(config.project, feature_table_dict),  # feature_view name == feature_table name
                            feature_table_version,
                            datetime.now(),
                            datetime.now(),
                            str(config.user_name),
                            entitiy.name,
                            no_of_features,
                            json.dumps(feature_table_dict["features"]),
                            str(feature_table_dict["batch_source"]["event_timestamp_column"]),
                            str(feature_table_dict["batch_source"]["created_timestamp_column"]),
                            json.dumps(feature_table_dict["batch_source"]),
                            json.dumps(feature_table_dict["offline_store"]),
                            json.dumps(feature_table_dict["online_store"]),
                            "YES" if feature_table_dict["online"] else "NO",
                            "INSERTED FEATURE TABLE",
                        ),
                        )

        return self._registry_store.update_registry(update_query, insert_query)

    def apply_feature_view(
        self, feature_view: FeatureView, entitiy: Entity, config: RepoConfig
    ):
        """
        Registers a single feature view with feature store

        Args:
            feature_view: Feature view that will be registered
            project: Feature store project that this feature view belongs to
            commit: Whether the change should be persisted immediately
        """
        feature_view.is_valid()
        feature_view_dict = feature_view.to_dict()
        feature_view_dict["project"] = config.project
        feature_view_dict["offline_store"] = {}
        feature_view_dict["offline_store"]["store"] = _table_id(config.project, feature_view_dict)  # actual offline store name
        feature_view_dict["offline_store"]["cloud"] = 'FileSystem'
        feature_view_dict["offline_store"]["storage"] = config.offline_store.type
        feature_view_dict["online_store"] = {}
        feature_view_dict["online_store"]["store"] = _table_id(config.project, feature_view_dict)  # actual online store name
        feature_view_dict["online_store"]["cloud"] = 'FileSystem'
        feature_view_dict["online_store"]["storage"] = config.online_store.type
        feature_view_dict['ttl'] = str(feature_view_dict['ttl'])

        feature_table_version: int = 1
        no_of_features: int = len(set(filter(lambda x: x not in [None, ""], list(map(lambda x: x.get('name'), feature_view_dict["features"])) + feature_view_dict["entities"] +
                                             [feature_view_dict["batch_source"]["event_timestamp_column"], feature_view_dict["batch_source"]["created_timestamp_column"]])))

        feature_views = {feature_view_dict['name']: feature_view_dict}
        n = "%s"

        update_query = (f"""
                                UPDATE {self._registry_name}
                                SET features = {n}, feature_table = {n}, feature_table_version = {n}, last_modified = {n}, 
                                last_modified_by = {n}, no_of_features = {n}, data_source = {n}, stage = {n}
                                WHERE (primary_key = {n} AND project_name = {n})
                        """,
                        (
                            # SET
                            str(feature_view_dict["features"]),
                            _table_id(config.project, feature_view_dict),
                            feature_table_version,
                            datetime.now(),
                            config.user_name,
                            no_of_features,
                            json.dumps(feature_view_dict["batch_source"]),
                            "UPDATED FEATURE VIEW",
                            # WHERE
                            entitiy.name,
                            feature_view_dict["project"],
                        ),
                )

        insert_query = (f"""
                                INSERT INTO {self._registry_name}
                                (project_name, user_name, description, feature_table, feature_table_version, created, 
                                last_modified, last_modified_by, primary_key, no_of_features, features, event_timestamp_column, 
                                created_timestamp_column, data_source, offline_store, online_store, online, stage, feature_views)
                                VALUES ({n}, {n}, {n}, {n}, {n}, {n}, {n}, {n}, {n}, {n}, {n}, {n}, {n}, {n}, {n}, {n}, {n}, {n}, {n})
                        """,  # OR IGNORE
                        (
                            str(feature_view_dict["project"]),
                            str(config.user_name),
                            str(config.description),
                            _table_id(config.project, feature_view_dict),  # feature_view name == feature_table name
                            feature_table_version,
                            datetime.now(),
                            datetime.now(),
                            str(config.user_name),
                            entitiy.name,
                            no_of_features,
                            str(feature_view_dict["features"]),
                            str(feature_view_dict["batch_source"]["event_timestamp_column"]),
                            str(feature_view_dict["batch_source"]["created_timestamp_column"]),
                            json.dumps(feature_view_dict["batch_source"]),
                            # str(feature_view_dict["batch_source"]),
                            json.dumps(feature_view_dict["offline_store"]),
                            json.dumps(feature_view_dict["online_store"]),
                            "YES" if feature_view_dict["online"] else "NO",
                            "INSERTED FEATURE VIEW",
                            json.dumps(feature_views),
                        ),
                        )
        return self._registry_store.update_registry(update_query, insert_query)

    def list_feature_tables(self, project: str) -> List[str]:
        """
        Retrieve a list of feature tables from the registry

        Args:
            project: Filter feature tables based on project name

        Returns:
            List of feature tables
        """
        query = f"SELECT feature_table FROM {self._registry_name} WHERE (project_name='{project}');"

        return self._registry_store.get_registry(query)

    def list_feature_views(self, project: str) -> List[str]:
        """
        Retrieve a list of feature views from the registry

        Args:
            project: Filter feature tables based on project name

        Returns:
            List of feature views
        """
        query = f"SELECT feature_table FROM {self._registry_name} WHERE (project_name='{project}');"

        return self._registry_store.get_registry(query)

    def get_feature_view(self, name: str, project: str) -> FeatureView:
        """
        Retrieves a feature view.

        Args:
            name: Name of feature view
            project: Feast project that this feature view belongs to

        Returns:
            Returns either the specified feature view, or raises an exception if
            none is found
        """
        query = f"SELECT feature_views FROM {self._registry_name} WHERE (project_name='{project}');"
        registry = self._registry_store.get_feature_view(query)

        for feature_view in registry.feature_views.to_list():
            if (
                name in feature_view.keys()
                and feature_view[name]['project'] == project
            ):
                feature_view[name]['ttl'] = timedelta(int(feature_view[name]['ttl'].split(' days,')[0]))
                feature_view[name]['features'] = list(
                    set(
                        map(lambda x: x['name'], feature_view[name]['features'])
                    ).difference(
                        {
                            feature_view[name]['batch_source'][
                                'created_timestamp_column'
                            ]
                            or '',
                            feature_view[name]['batch_source'][
                                'event_timestamp_column'
                            ],
                            feature_view[name]['entities'][0],
                        }
                    )
                )

                return FeatureView.from_dict(feature_view[name])
        raise FeatureViewNotFoundException(name, project)

    def teardown(self):
        """Tears down (removes) the registry."""
        self._registry_store.teardown()


def _table_id(project: str, table: Dict) -> str:  # table: Union[FeatureTable, FeatureView]
    return f"{project}_{table['name']}"
