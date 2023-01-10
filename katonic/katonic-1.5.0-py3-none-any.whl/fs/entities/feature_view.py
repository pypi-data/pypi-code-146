#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union

from katonic.fs.data_source import DataSource

from katonic.fs.entities.feature import Feature
from katonic.fs.repo_config import RepoConfig


class FeatureView:

    name: str
    entities: List[str]
    features: List[Feature]
    ttl: timedelta
    online: bool
    batch_source: DataSource
    created_timestamp: Optional[datetime] = None
    last_updated_timestamp: Optional[datetime] = None

    offline_config: RepoConfig

    def __init__(
        self,
        name: str,
        entities: List[str],
        ttl: str,
        batch_source: Optional[DataSource] = None,
        features: Optional[Union[str, List[Feature]]] = None,
        online: bool = True,
    ):
        _features = features or []

        self.name = name
        self.entities = entities  # dummy entities when no entity is given
        self.features = _features

        if isinstance(ttl, str):
            if "h" in ttl[-1]:
                time = int(ttl[: -1]) * 60 * 60
            elif "d" in ttl[-1]:
                time = int(ttl[: -1]) * 24 * 3600
            elif "m" in ttl[-1]:
                time = int(ttl[: -1]) * 30 * 24 * 3600
            elif "y" in ttl[-1]:
                time = int(ttl[: -1]) * 365 * 24 * 3600
            else:
                raise TypeError(
                    "Please give 'ttl' as a string like dayes '2d' or you can provide it in years '2y', months '1m' or hours '6h'.")
            self.ttl = timedelta(seconds=time)

        if isinstance(ttl, timedelta):
            self.ttl = ttl

        self.online = online
        self.batch_source = batch_source

        self.created_timestamp: Optional[datetime] = None
        self.last_updated_timestamp: Optional[datetime] = None

    def __repr__(self):
        items = (f"{k} = {v}" for k, v in self.__dict__.items())
        return f"<{self.__class__.__name__}({', '.join(items)})>"

    def __str__(self):
        return str(self.to_dict())

    def __hash__(self):
        return hash((id(self), self.name))

    def __eq__(self, other):
        if not isinstance(other, FeatureView):
            raise TypeError(
                "Comparisons should only involve FeatureView class objects."
            )

        if (
            self.name != other.name
            or self.online != other.online
        ):
            return False

        if sorted(self.entities) != sorted(other.entities):
            return False
        if sorted(self.features) != sorted(other.features):
            return False
        if self.batch_source != other.batch_source:
            return False

        return True

    def is_valid(self):
        """
        Validates the state of this feature view locally.

        Raises:
            ValueError: The feature view does not have a name or does not have entities.
        """
        if not self.name:
            raise ValueError("Feature view needs a name.")

        if not self.entities:
            raise ValueError("Feature view has no entities.")

    def to_dict(self) -> Dict:
        """
        Converts feature view to dict.

        Returns:
            Dictionary object representation of feature view.
        """
        batch_source_dict = self.batch_source.to_dict()
        batch_source_dict["data_source_class_type"] = f"{self.batch_source.__class__.__module__}.{self.batch_source.__class__.__name__}"

        return {
            "name": self.name,
            "entities": self.entities,
            "features": self.features,
            "ttl": self.ttl,
            "online": self.online,
            "batch_source": batch_source_dict,
        }

    @classmethod
    def from_dict(cls, feature_view_dict: Dict):
        """
        Creates a feature view from a Dictionary representation of a feature view.

        Args:
            feature_view_dict: A Dictionary representation of a feature view.

        Returns:
            A FeatureView object based on the feature view Dictionary.
        """
        batch_source = DataSource.from_dict(feature_view_dict["batch_source"])

        # feature_view
        return cls(
            name=feature_view_dict["name"],
            entities=list(feature_view_dict["entities"]),
            features=feature_view_dict["features"],
            online=feature_view_dict["online"],
            ttl=feature_view_dict["ttl"],
            batch_source=batch_source,
        )
