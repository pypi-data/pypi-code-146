#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from datetime import datetime, timedelta
from typing import Dict, List, MutableMapping, Optional

from katonic.fs.entities.feature import Feature
from katonic.fs.data_source import DataSource


class FeatureTable:
    """
    Represents a collection of features and associated metadata.
    """

    def __init__(
        self,
        name: str,
        entities: List[str],
        features: List[Feature],
        batch_source: DataSource = None,
        max_age: Optional[timedelta] = None,
        labels: Optional[MutableMapping[str, str]] = None,
    ):
        self._name = name
        self._entities = entities
        self._features = features
        self._batch_source = batch_source
        # self._stream_source = stream_source

        self._labels: MutableMapping[str, str]
        self._labels = dict() if labels is None else labels
        self._max_age = max_age
        self._created_timestamp: Optional[datetime] = None
        self._last_updated_timestamp: Optional[datetime] = None

    def __str__(self):
        return str(self._to_dict)

    def __eq__(self, other):
        if not isinstance(other, FeatureTable):
            raise TypeError(
                "Comparisons should only involve FeatureTable class objects."
            )

        if (
            self.labels != other.labels
            or self.name != other.name
            or self.max_age != other.max_age
        ):
            return False

        if sorted(self.entities) != sorted(other.entities):
            return False
        if sorted(self.features) != sorted(other.features):
            return False
        if self.batch_source != other.batch_source:
            return False
        # if self.stream_source != other.stream_source:
        #     return False

        return True

    @property
    def name(self):
        """
        Returns the name of this feature table
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """
        Sets the name of this feature table
        """
        self._name = name

    @property
    def entities(self):
        """
        Returns the entities of this feature table
        """
        return self._entities

    @entities.setter
    def entities(self, entities: List[str]):
        """
        Sets the entities of this feature table
        """
        self._entities = entities

    @property
    def features(self):
        """
        Returns the features of this feature table
        """
        return self._features

    @features.setter
    def features(self, features: List[Feature]):
        """
        Sets the features of this feature table
        """
        self._features = features

    @property
    def batch_source(self):
        """
        Returns the batch source of this feature table
        """
        return self._batch_source

    @batch_source.setter
    def batch_source(self, batch_source: DataSource):
        """
        Sets the batch source of this feature table
        """
        self._batch_source = batch_source

    # @property
    # def stream_source(self):
    #     """
    #     Returns the stream source of this feature table
    #     """
    #     return self._stream_source

    # @stream_source.setter
    # def stream_source(self, stream_source):# Union[KafkaSource, KinesisSource]):
    #     """
    #     Sets the stream source of this feature table
    #     """
    #     self._stream_source = stream_source

    @property
    def max_age(self):
        """
        Returns the maximum age of this feature table. This is the total maximum
        amount of staleness that will be allowed during feature retrieval for
        each specific feature that is looked up.
        """
        return self._max_age

    @max_age.setter
    def max_age(self, max_age: timedelta):
        """
        Set the maximum age for this feature table
        """
        self._max_age = max_age

    @property
    def created_timestamp(self):
        """
        Returns the created_timestamp of this feature table
        """
        return self._created_timestamp

    @property
    def last_updated_timestamp(self):
        """
        Returns the last_updated_timestamp of this feature table
        """
        return self._last_updated_timestamp

    def add_feature(self, feature: Feature):
        """
        Adds a new feature to the feature table.
        """
        self.features.append(feature)

    def is_valid(self):
        """
        Validates the state of a feature table locally. Raises an exception
        if feature table is invalid.
        """

        if not self.name:
            raise ValueError("No name found in feature table.")

        if not self.entities:
            raise ValueError("No entities found in feature table {self.name}.")

    def _to_dict(self) -> Dict:
        """
        Converts feature table to dict

        :return: Dictionary object representation of feature table
        """

        return {
            'name': self._name,
            'entities': self._entities,
            'feature': self._features if self.features else [],
            'max_age': self._max_age,
            'online': self.online,
            'batch_source': self._batch_source,
            'created_timestamp': self._created_timestamp,
            'last_updated_timestamp': self._last_updated_timestamp,
        }

    def _update_from_feature_table(self, feature_table):
        """
        Deep replaces one feature table with another

        Args:
            feature_table: Feature table to use as a source of configuration
        """

        self.name = feature_table.name
        self.entities = feature_table.entities
        self.features = feature_table.features
        self.max_age = feature_table.max_age
        self.batch_source = feature_table.batch_source
        # self.stream_source = feature_table.stream_source
        self._created_timestamp = feature_table.created_timestamp
        self._last_updated_timestamp = feature_table.last_updated_timestamp

    def __repr__(self):
        return f"FeatureTable <{self.name}>"