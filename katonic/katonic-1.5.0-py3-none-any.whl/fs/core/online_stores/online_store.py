#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional, Sequence, Tuple, Union

from katonic.fs.entities import Entity, FeatureTable
from katonic.fs.entities import FeatureView
from katonic.fs.repo_config import RepoConfig
from katonic.fs.value_type import ValueType


class OnlineStore(ABC):
    """
    OnlineStore is an object used for all interaction between KFS and the service used for online storage of
    features.
    """

    @abstractmethod
    def online_write_batch(
        self,
        config: RepoConfig,
        table: Union[FeatureTable, FeatureView],
        data: List[
            Tuple[str, Dict[str, ValueType], datetime, Optional[datetime]]
        ],
    ) -> None:
        """
        Write a batch of feature rows to the online store. This is a low level interface, not
        expected to be used by the users directly.

        If a tz-naive timestamp is passed to this method, it should be assumed to be UTC by implementors.

        Args:
            config: The RepoConfig for the current FeatureStore.
            table: KFS FeatureTable or FeatureView
            data: a list of quadruplets containing Feature data. Each quadruplet contains an Entity Key,
            a dict containing feature values, an event timestamp for the row, and
            the created timestamp for the row if it exists.
            progress: Optional function to be called once every mini-batch of rows is written to
            the online store. Can be used to display progress.
        """
        ...

    @abstractmethod
    def online_read(
        self,
        config: RepoConfig,
        table: Union[FeatureTable, FeatureView],
        entity_keys: List[str],
        requested_features: Optional[List[str]] = None,
    ) -> List[Tuple[Optional[datetime], Optional[Dict[str, ValueType]]]]:
        """
        Read feature values given an Entity Key. This is a low level interface, not
        expected to be used by the users directly.

        Args:
            config: The RepoConfig for the current FeatureStore.
            table: KFS FeatureTable or FeatureView
            entity_keys: a list of entity keys that should be read from the FeatureStore.
            requested_features: (Optional) A subset of the features that should be read from the FeatureStore.
        Returns:
            Data is returned as a list, one item per entity key. Each item in the list is a tuple
            of event_ts for the row, and the feature data as a dict from feature names to values.
        """
        ...

    @abstractmethod
    def update(
        self,
        config: RepoConfig,
        tables_to_keep: Sequence[Union[FeatureTable, FeatureView]],
        entities_to_keep: Sequence[Entity],
    ):
        ...

    @abstractmethod
    def teardown(
        self,
        config: RepoConfig,
        tables: Sequence[Union[FeatureTable, FeatureView]],
        entities: Sequence[Entity],
    ):
        ...
