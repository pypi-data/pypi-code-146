#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

import abc
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import pandas as pd
import pyarrow
import pyspark

from katonic.fs import errors, importer
from katonic.fs.entities.entity import Entity
from katonic.fs.entities.feature_table import FeatureTable
from katonic.fs.entities.feature_view import FeatureView
from katonic.fs.core.offline_stores.offline_store import RetrievalJob
from katonic.fs.registry import Registry
from katonic.fs.repo_config import RepoConfig


class Provider(abc.ABC):
    @abc.abstractmethod
    def __init__(self, config: RepoConfig):
        ...

    @abc.abstractmethod
    def update_infra(
        self,
        project: str,
        tables_to_keep: Sequence[Union[FeatureTable, FeatureView]],
        entities_to_keep: Sequence[Entity],
    ):
        """
        Reconcile cloud resources with the objects declared in the feature repo.

        Args:
            project: Project to which tables belong
            tables_to_keep: Tables that are still in the feature repo. Depending on implementation,
                provider may or may not need to update the corresponding resources.
            entities_to_keep: Entities that are still in the feature repo. Depending on implementation,
                provider may or may not need to update the corresponding resources.

        """
        ...

    @abc.abstractmethod
    def teardown_infra(
        self,
        project: str,
        tables: Sequence[Union[FeatureTable, FeatureView]],
        entities: Sequence[Entity],
    ):
        """
        Tear down all cloud resources for a repo.

        Args:
            project: Kfs project to which tables belong
            tables: Tables that are declared in the feature repo.
            entities: Entities that are declared in the feature repo.
        """
        ...

    @abc.abstractmethod
    def online_write_batch(
        self,
        config: RepoConfig,
        table: Union[FeatureTable, FeatureView],
        data: List[
            Tuple[Dict[str, Any], Dict[str, Any], datetime, Optional[datetime]]
        ],
    ) -> None:
        """
        Write a batch of feature rows to the online store. This is a low level interface, not
        expected to be used by the users directly.

        If a tz-naive timestamp is passed to this method, it is assumed to be UTC.

        Args:
            config: The RepoConfig for the current FeatureStore.
            table: Kfs FeatureTable
            data: a list of quadruplets containing Feature data. Each quadruplet contains an Entity Key,
                a dict containing feature values, an event timestamp for the row, and
                the created timestamp for the row if it exists.
        """
        ...

    @abc.abstractmethod
    def materialize_single_feature_view(
        self,
        config: RepoConfig,
        feature_view: FeatureView,
        start_date: datetime,
        end_date: datetime,
        registry: Registry,
        project: str,
    ) -> None:
        pass

    @abc.abstractmethod
    def get_historical_features(
        self,
        config: RepoConfig,
        feature_views: List[FeatureView],
        feature_refs: List[str],
        entity_df: Union[pd.DataFrame, str],
        registry: Registry,
        project: str,
    ) -> RetrievalJob:
        pass

    @abc.abstractmethod
    def online_read(
        self,
        config: RepoConfig,
        table: Union[FeatureTable, FeatureView],
        entity_keys: List[Dict[str, Any]],
        requested_features: List[str] = None,
    ) -> List[Tuple[Optional[datetime], Optional[Dict[str, Any]]]]:
        """
        Read feature values given an Entity Key. This is a low level interface, not
        expected to be used by the users directly.

        Returns:
            Data is returned as a list, one item per entity key. Each item in the list is a tuple
            of event_ts for the row, and the feature data as a dict from feature names to values.
            Values are returned as Value Dictionary.
        """
        ...

    @abc.abstractmethod
    def write_offline_features_data(
        self,
        project: str,
        data: Optional[Union[pd.DataFrame, pyspark.sql.DataFrame]],
        tables_to_keep: Sequence[Union[FeatureTable, FeatureView]],
        entities_to_keep: Sequence[Entity],
    ) -> List[Dict]:
        """
        Reconcile cloud resources with the objects declared in the feature repo.

        Args:
            project: Project to which tables belong
            data: Data as Pandas dataframe or Spark DataFrame.
            tables_to_keep: Tables that are still in the feature repo. Depending on implementation,
                provider may or may not need to update the corresponding resources.
            entities_to_keep: Entities that are still in the feature repo. Depending on implementation,
                provider may or may not need to update the corresponding resources.
        """
        ...


def get_provider(config: RepoConfig, repo_path: Path) -> Provider:
    # if "." not in config.provider:
    #     if config.provider not in {"postgres", "local"}:
    #         raise errors.KfsProviderNotImplementedError(config.provider)
    from katonic.fs.core.passthrough_provider import PassthroughProvider

    return PassthroughProvider(config)
    # else:
    #     # Split provider into module and class names by finding the right-most dot.
    #     # For example, provider 'foo.bar.MyProvider' will be parsed into 'foo.bar' and 'MyProvider'
    #     module_name, class_name = config.provider.rsplit(".", 1)

    #     cls = importer.get_class_from_type(module_name, class_name, "Provider")

    #     return cls(config)


def _get_requested_feature_views_to_features_dict(
    feature_refs: List[str],
    feature_views: List[FeatureView],
) -> Dict[FeatureView, List[str]]:
    """Create a dict of FeatureView -> List[Feature] for all requested features.
    Set full_feature_names to True to have feature names prefixed by their feature view name."""

    feature_views_to_feature_map: Dict[FeatureView,
                                       List[str]] = defaultdict(list)

    for ref in feature_refs:
        ref_parts = ref.split(":")
        feature_view_from_ref = ref_parts[0]
        feature_from_ref = ref_parts[1]

        found = False
        for fv in feature_views:
            if fv.name == feature_view_from_ref:
                found = True
                feature_views_to_feature_map[fv].append(feature_from_ref)

        if not found:
            raise ValueError(
                f"Could not find feature view from reference {ref}")

    return feature_views_to_feature_map


def _convert_arrow_to_dict(
    table: pyarrow.Table, feature_view: FeatureView, join_keys: List[str],
) -> List[Tuple[Dict[str, Any], Dict[str, Any], datetime, Optional[datetime]]]:
    rows_to_write = []

    def _coerce_datetime(ts):
        """
        Depending on underlying time resolution, arrow to_pydict() sometimes returns pandas
        timestamp type (for nanosecond resolution), and sometimes you get standard python datetime
        (for microsecond resolution).

        While pandas timestamp class is a subclass of python datetime, it doesn't always behave the
        same way. We convert it to normal datetime so that consumers downstream don't have to deal
        with these quirks.
        """

        return ts.to_pydatetime() if isinstance(ts, pd.Timestamp) else ts

    for row in zip(*table.to_pydict().values()):
        entity_key = {}
        for join_key in join_keys:
            idx = table.column_names.index(join_key)
            entity_key[join_key] = row[idx]
        feature_dict = {}
        for feature in feature_view.features:
            idx = table.column_names.index(feature)
            feature_dict[feature] = row[idx]
        event_timestamp_idx = table.column_names.index(
            feature_view.batch_source.event_timestamp_column
        )
        event_timestamp = _coerce_datetime(row[event_timestamp_idx])

        if feature_view.batch_source.created_timestamp_column:
            created_timestamp_idx = table.column_names.index(
                feature_view.batch_source.created_timestamp_column
            )
            created_timestamp = _coerce_datetime(row[created_timestamp_idx])
        else:
            created_timestamp = None

        rows_to_write.append(
            (entity_key, feature_dict, event_timestamp, created_timestamp)
        )
    return rows_to_write
