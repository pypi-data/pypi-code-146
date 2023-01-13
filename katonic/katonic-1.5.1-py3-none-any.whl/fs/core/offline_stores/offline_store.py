#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, List, Optional, Sequence, Union

import pandas as pd
import pyarrow
import pyspark

# from katonic.fs.data_source import DataSource
from katonic.fs.entities.feature_view import FeatureView
from katonic.fs.entities.entity import Entity
from katonic.fs.entities.feature_table import FeatureTable
from katonic.fs.registry import Registry
from katonic.fs.repo_config import RepoConfig


class RetrievalJob(ABC):
    """RetrievalJob is used to manage the execution of a historical feature retrieval"""

    # @property
    # @abstractmethod
    # def full_feature_names(self) -> bool:
    #     pass

    def to_df(self) -> pd.DataFrame:
        """Return dataset as Pandas DataFrame synchronously including on demand transforms"""
        # features_df = self._to_df_internal()
        # if self.on_demand_feature_views is None:
        #     return features_df

        # for odfv in self.on_demand_feature_views:
        #     features_df = features_df.join(
        #         odfv.get_transformed_features_df(self.full_feature_names, features_df)
        #     )
        return self._to_df_internal()  # features_df

    @abstractmethod
    def _to_df_internal(self) -> pd.DataFrame:
        """Return dataset as Pandas DataFrame synchronously"""
        pass

    @abstractmethod
    def _to_arrow_internal(self) -> pyarrow.Table:
        """Return dataset as pyarrow Table synchronously"""
        pass

    def to_arrow(self) -> pyarrow.Table:
        """Return dataset as pyarrow Table synchronously"""
        # if self.on_demand_feature_views is None:
        #     return self._to_arrow_internal()

        features_df = self._to_df_internal()
        # for odfv in self.on_demand_feature_views:
        #     features_df = features_df.join(
        #         odfv.get_transformed_features_df(self.full_feature_names, features_df)
        #     )
        return pyarrow.Table.from_pandas(features_df)


# class IngestionJob(ABC):
#     """IngestionJob is used to manage the execution of a historical feature writing"""

#     @property
#     @abstractmethod
#     def full_feature_names(self) -> bool:
#         pass

#     def to_df(self) -> pd.DataFrame:
#         """Return dataset as Pandas DataFrame synchronously including on demand transforms"""
#         features_df = self._to_df_internal()
#         if self.on_demand_feature_views is None:
#             return features_df

#         for odfv in self.on_demand_feature_views:
#             features_df = features_df.join(
#                 odfv.get_transformed_features_df(self.full_feature_names, features_df)
#             )
#         return features_df

#     @abstractmethod
#     def _to_df_internal(self) -> pd.DataFrame:
#         """Return dataset as Pandas DataFrame synchronously"""
#         pass

#     @abstractmethod
#     def _to_arrow_internal(self) -> pyarrow.Table:
#         """Return dataset as pyarrow Table synchronously"""
#         pass

#     def to_arrow(self) -> pyarrow.Table:
#         """Return dataset as pyarrow Table synchronously"""
#         if self.on_demand_feature_views is None:
#             return self._to_arrow_internal()

#         features_df = self._to_df_internal()
#         for odfv in self.on_demand_feature_views:
#             features_df = features_df.join(
#                 odfv.get_transformed_features_df(self.full_feature_names, features_df)
#             )
#         return pyarrow.Table.from_pandas(features_df)


class OfflineStore(ABC):
    """
    OfflineStore is an object used for all interaction between Kfs and the service used for offline storage of
    features.
    """

    @staticmethod
    @abstractmethod
    def pull_latest_from_table_or_query(
        config,
        data_source: Any,
        join_key_columns: List[str],
        feature_name_columns: List[str],
        event_timestamp_column: str,
        created_timestamp_column: Optional[str],
        start_date: datetime,
        end_date: datetime,
    ) -> RetrievalJob:
        """
        Note that join_key_columns, feature_name_columns, event_timestamp_column, and created_timestamp_column
        have all already been mapped to column names of the source table and those column names are the values passed
        into this function.
        """
        pass

    @staticmethod
    @abstractmethod
    def get_historical_features(
        config,
        feature_views: List[FeatureView],
        feature_refs: List[str],
        entity_df: Union[pd.DataFrame, str],
        registry: Registry,
        project: str,
        # full_feature_names: bool = False,
    ) -> RetrievalJob:
        pass

    @staticmethod
    @abstractmethod
    def write_offline_features(
        config: RepoConfig,
        data: Optional[Union[pd.DataFrame, pyspark.sql.DataFrame]],
        # entity_df: Union[pd.DataFrame, pyspark.sql.DataFrame, str],
        tables_to_keep: Sequence[Union[FeatureTable, FeatureView]],
        entities_to_keep: Sequence[Entity],
        # format: Optional[str] = "parquet",
        # mode: Optional[str] = "append"
    ) -> None:
        pass
