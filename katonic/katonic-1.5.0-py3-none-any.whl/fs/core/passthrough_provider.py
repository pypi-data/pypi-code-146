#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import pyspark
import pandas as pd

from katonic.fs.entities.entity import Entity
from katonic.fs.entities.feature_view import FeatureView
from katonic.fs.entities.feature_table import FeatureTable
from katonic.fs.core.offline_stores.offline_store import RetrievalJob
from katonic.fs.core.offline_stores.offline_utils import get_offline_store_from_config
from katonic.fs.core.online_stores.helpers import get_online_store_from_config
from katonic.fs.core.provider import (
    Provider,
    _convert_arrow_to_dict,
)
from katonic.fs.registry import Registry
from katonic.fs.repo_config import RepoConfig


class PassthroughProvider(Provider):
    """
    The Passthrough provider delegates all operations to the underlying online and offline stores.
    """

    def __init__(self, config: RepoConfig):
        super().__init__(config)

        self.repo_config = config
        self.offline_store = get_offline_store_from_config(
            config.offline_store)
        self.online_store = get_online_store_from_config(config.online_store)

    # Done
    def update_infra(
        self,
        project: str,
        tables_to_keep: Sequence[Union[FeatureTable, FeatureView]],
        entities_to_keep: Sequence[Entity],
    ):
        self.online_store.update(
            config=self.repo_config,
            tables_to_keep=tables_to_keep,
            entities_to_keep=entities_to_keep,
        )

    def teardown_infra(
        self,
        project: str,
        tables: Sequence[Union[FeatureTable, FeatureView]],
        entities: Sequence[Entity],
    ) -> None:
        self.online_store.teardown(self.repo_config, tables, entities)

    def online_write_batch(
        self,
        config: RepoConfig,
        table: Union[FeatureTable, FeatureView],
        data: List[
            Tuple[Dict[str, Any], Dict[str, Any], datetime, Optional[datetime]]
        ],
    ) -> None:
        self.online_store.online_write_batch(config, table, data)

    def online_read(
        self,
        config: RepoConfig,
        table: Union[FeatureTable, FeatureView],
        entity_keys: List[Dict[str, Any]],
        requested_features: List[str] = None,
    ) -> List[Tuple[Optional[datetime], Optional[Dict[str, Any]]]]:
        return self.online_store.online_read(config, table, entity_keys, requested_features)

    def materialize_single_feature_view(
        self,
        config: RepoConfig,
        feature_view: FeatureView,
        start_date: datetime,
        end_date: datetime,
        registry: Registry,
        project: str,
    ) -> None:
        # entities
        join_key_columns = list(feature_view.entities)
        event_timestamp_column = feature_view.batch_source.event_timestamp_column
        created_timestamp_column = feature_view.batch_source.created_timestamp_column
        feature_name_columns = list(feature_view.features)

        feature_name_columns = list(set(feature_name_columns) - set(join_key_columns) - {
                                    event_timestamp_column, created_timestamp_column})

        # issue with data_source path etc...
        offline_job = self.offline_store.pull_latest_from_table_or_query(
            config=config,
            data_source=feature_view.batch_source,
            join_key_columns=join_key_columns,
            feature_name_columns=feature_name_columns,
            event_timestamp_column=event_timestamp_column,
            created_timestamp_column=created_timestamp_column,
            start_date=start_date,
            end_date=end_date,
        )
        table = offline_job.to_arrow()

        # [entity.join_key for entity in entities]
        join_keys = join_key_columns
        rows_to_write = _convert_arrow_to_dict(table, feature_view, join_keys)

        self.online_write_batch(
            self.repo_config, feature_view, rows_to_write
        )

    def get_historical_features(
        self,
        config: RepoConfig,
        feature_views: List[FeatureView],
        feature_refs: List[str],
        entity_df: Union[pd.DataFrame, str],
        registry: Registry,
        project: str,
    ) -> RetrievalJob:
        return self.offline_store.get_historical_features(
            config=config,
            feature_views=feature_views,
            feature_refs=feature_refs,
            entity_df=entity_df,
            registry=registry,
            project=project,
        )

    def write_offline_features_data(
        self,
        project: str,
        data: Optional[Union[pd.DataFrame, pyspark.sql.DataFrame]],
        tables_to_keep: Sequence[Union[FeatureTable, FeatureView]],
        entities_to_keep: Sequence[Entity],
    ) -> List[Dict]:
        return self.offline_store.write_offline_features(
            config=self.repo_config,
            data=data,
            tables_to_keep=tables_to_keep,
            entities_to_keep=entities_to_keep,
        )
