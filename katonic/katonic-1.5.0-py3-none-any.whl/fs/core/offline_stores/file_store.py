#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from pydantic.typing import Literal
from pydantic.types import StrictStr

from pathlib import Path
import pytz
from datetime import datetime
from typing import Any, Callable, List, Optional, Sequence, Union

import pyarrow
import pyspark
import pandas as pd
from katonic.fs.core.offline_stores.dataframe_source import DataFrameSource

from katonic.fs.entities.entity import Entity
from katonic.fs.core.offline_stores.offline_store import OfflineStore
from katonic.fs.entities.feature_table import FeatureTable
from katonic.fs.errors import KfsJoinKeysDuringMaterialization
from katonic.fs.entities.feature_view import FeatureView  # , DUMMY_ENTITY_ID, DUMMY_ENTITY_VAL,
from katonic.fs.core.offline_stores.offline_store import OfflineStore, RetrievalJob
from katonic.fs.core.offline_stores.offline_utils import (
    DEFAULT_ENTITY_DF_EVENT_TIMESTAMP_COL,
)
from katonic.fs.core.provider import (
    _get_requested_feature_views_to_features_dict,
)
from katonic.fs.registry import Registry
from katonic.fs.repo_config import KfsConfigBaseModel, RepoConfig


class FileOfflineStoreConfig(KfsConfigBaseModel):
    """ Offline store config for local (file-based) store """

    type: Literal["file"] = "file"
    """ Offline store type selector"""

    path: StrictStr = "data/offline_store.parquet"
    """ (optional) Path to Offline store file """


class FileRetrievalJob(RetrievalJob):
    def __init__(
        self,
        evaluation_function: Callable,
    ):
        """Initialize a lazy historical retrieval job"""

        self.evaluation_function = evaluation_function

    def _to_df_internal(self) -> pd.DataFrame:
        # Only execute the evaluation function to build the final historical retrieval dataframe at the last moment.
        return self.evaluation_function()

    def _to_arrow_internal(self):
        # Only execute the evaluation function to build the final historical retrieval dataframe at the last moment.
        df = self.evaluation_function()
        return pyarrow.Table.from_pandas(df)


class FileOfflineStore(OfflineStore):
    @staticmethod
    def get_historical_features(
        config: RepoConfig,
        feature_views: List[FeatureView],
        feature_refs: List[str],
        entity_df: Union[pd.DataFrame, str],
        registry: Registry,
        project: str,
        # full_feature_names: bool = False,
    ) -> RetrievalJob:
        if not isinstance(entity_df, pd.DataFrame):
            raise ValueError(
                f"Please provide an entity_df of type {type(pd.DataFrame)} instead of type {type(entity_df)}"
            )

        entity_df_event_timestamp_col = DEFAULT_ENTITY_DF_EVENT_TIMESTAMP_COL  # local modifiable copy of global variable
        if entity_df_event_timestamp_col not in entity_df.columns:
            datetime_columns = entity_df.select_dtypes(
                include=["datetime", "datetimetz"]
            ).columns
            if len(datetime_columns) == 1:
                print(
                    f"Using {datetime_columns[0]} as the event timestamp. To specify a column explicitly, please name it {DEFAULT_ENTITY_DF_EVENT_TIMESTAMP_COL}."
                )
                entity_df_event_timestamp_col = datetime_columns[0]
            else:
                raise ValueError(
                    f"Please provide an entity_df with a column named {DEFAULT_ENTITY_DF_EVENT_TIMESTAMP_COL} representing the time of events."
                )

        feature_views_to_features = _get_requested_feature_views_to_features_dict(
            feature_refs,
            feature_views,
        )

        # Create lazy function that is only called from the RetrievalJob object
        def evaluate_historical_retrieval():

            # Make sure all event timestamp fields are tz-aware. We default tz-naive fields to UTC
            entity_df[entity_df_event_timestamp_col] = entity_df[
                entity_df_event_timestamp_col
            ].apply(lambda x: x if x.tzinfo is not None else x.replace(tzinfo=pytz.utc))

            # Create a copy of entity_df to prevent modifying the original
            entity_df_with_features = entity_df.copy()

            # Convert event timestamp column to datetime and normalize time zone to UTC
            # This is necessary to avoid issues with pd.merge_asof
            entity_df_with_features[entity_df_event_timestamp_col] = pd.to_datetime(
                entity_df_with_features[entity_df_event_timestamp_col], utc=True
            )

            # Sort event timestamp values
            entity_df_with_features = entity_df_with_features.sort_values(
                entity_df_event_timestamp_col
            )

            # Load feature view data from sources and join them incrementally
            for feature_view, features in feature_views_to_features.items():

                # Read offline store parquet data in pyarrow/spark format.
                # this function has no use

                path = config.repo_path / config.offline_store.path
                table = pyarrow.parquet.read_table(path)  # , filesystem=filesystem)

                event_timestamp_column = (
                    feature_view.batch_source.event_timestamp_column
                )
                created_timestamp_column = (
                    feature_view.batch_source.created_timestamp_column
                )

                # Rename columns by the field mapping dictionary if it exists
                # if feature_view.batch_source.field_mapping is not None:
                #     table = _run_field_mapping(
                #         table, feature_view.batch_source.field_mapping
                #     )

                # Convert pyarrow table to pandas dataframe. Note, if the underlying data has missing values,
                # pandas will convert those values to np.nan if the dtypes are numerical (floats, ints, etc.) or boolean
                # If the dtype is 'object', then missing values are inferred as python `None`s.
                # More details at:
                # https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html#values-considered-missing
                df_to_join = table.to_pandas()

                # Make sure all timestamp fields are tz-aware. We default tz-naive fields to UTC

                # deal with timezone + data types (if pandas read timestamps as objects)
                df_to_join[event_timestamp_column] = pd.to_datetime(df_to_join[event_timestamp_column])

                df_to_join[event_timestamp_column] = df_to_join[
                    event_timestamp_column
                ].apply(
                    lambda x: x if x.tzinfo is not None else x.replace(tzinfo=pytz.utc)
                )
                if created_timestamp_column:
                    df_to_join[created_timestamp_column] = pd.to_datetime(df_to_join[created_timestamp_column])

                    df_to_join[created_timestamp_column] = df_to_join[
                        created_timestamp_column
                    ].apply(
                        lambda x: x
                        if x.tzinfo is not None
                        else x.replace(tzinfo=pytz.utc)
                    )

                # Sort dataframe by the event timestamp column
                df_to_join = df_to_join.sort_values(event_timestamp_column)

                # Build a list of all the features we should select from this source
                feature_names = []
                for feature in features:
                    # Modify the separator for feature refs in column names to double underscore. We are using
                    # double underscore as separator for consistency with other databases like BigQuery,
                    # where there are very few characters available for use as separators
                    # if full_feature_names:
                    #     formatted_feature_name = f"{feature_view.name}__{feature}"
                    # else:
                    formatted_feature_name = feature
                    # Add the feature name to the list of columns
                    feature_names.append(formatted_feature_name)

                    # Ensure that the source dataframe feature column includes the feature view name as a prefix
                    df_to_join.rename(
                        columns={formatted_feature_name: formatted_feature_name}, inplace=True,
                    )

                # Build a list of entity columns to join on (from the right table)
                # join_keys = [entity_name for entity_name in feature_view.entities] # entity = registry.get_entity(entity_name, project)
                join_keys = list(feature_view.entities)  # entity = registry.get_entity(entity_name, project)

                right_entity_columns = join_keys
                right_entity_key_columns = [
                    event_timestamp_column
                ] + right_entity_columns

                # Remove all duplicate entity keys (using created timestamp)
                right_entity_key_sort_columns = right_entity_key_columns
                if created_timestamp_column:
                    # If created_timestamp is available, use it to dedupe deterministically
                    right_entity_key_sort_columns = right_entity_key_sort_columns + [
                        created_timestamp_column
                    ]

                df_to_join.sort_values(by=right_entity_key_sort_columns, inplace=True)
                df_to_join.drop_duplicates(
                    right_entity_key_sort_columns,
                    keep="last",
                    ignore_index=True,
                    inplace=True,
                )

                # Select only the columns we need to join from the feature dataframe
                df_to_join = df_to_join[right_entity_key_columns + feature_names]

                # Do point in-time-join between entity_df and feature dataframe
                entity_df_with_features = pd.merge_asof(
                    entity_df_with_features,
                    df_to_join,
                    left_on=entity_df_event_timestamp_col,
                    right_on=event_timestamp_column,
                    by=right_entity_columns or None,
                    # tolerance=feature_view.ttl,
                )

                # Remove right (feature table/view) event_timestamp column.
                if event_timestamp_column != entity_df_event_timestamp_col:
                    entity_df_with_features.drop(
                        columns=[event_timestamp_column], inplace=True
                    )

                # Ensure that we delete dataframes to free up memory
                del df_to_join

            # Move "event_timestamp" column to front
            current_cols = entity_df_with_features.columns.tolist()
            current_cols.remove(entity_df_event_timestamp_col)
            entity_df_with_features = entity_df_with_features[
                [entity_df_event_timestamp_col] + current_cols
            ]

            return entity_df_with_features

        job = FileRetrievalJob(
            evaluation_function=evaluate_historical_retrieval,
        )
        return job

    @staticmethod
    def pull_latest_from_table_or_query(
        config: RepoConfig,
        data_source: Any,  # DataSource
        join_key_columns: List[str],
        feature_name_columns: List[str],
        event_timestamp_column: str,
        created_timestamp_column: Optional[str],
        start_date: datetime,
        end_date: datetime,
    ) -> RetrievalJob:
        # assert isinstance(data_source, FileSource)

        # Create lazy function that is only called from the RetrievalJob object
        def evaluate_offline_job():

            path = config.repo_path / config.offline_store.path

            if type(data_source) == DataFrameSource:
                offline_data_df = pyarrow.parquet.read_table(path)
                offline_data_df = offline_data_df.to_pandas()
            # move to spark/pyarrow if required or provide as option for users requirement
            elif str(path).split(".")[-1] == "parquet":
                offline_data_df = pd.read_parquet(path)  # , filesystem=filesystem)
            else:
                offline_data_df = pd.read_csv(path)

            # Make sure all timestamp fields are tz-aware. We default tz-naive fields to UTC
            offline_data_df[event_timestamp_column] = pd.to_datetime(offline_data_df[event_timestamp_column])
            offline_data_df[event_timestamp_column] = offline_data_df[event_timestamp_column].apply(
                lambda x: x if x.tzinfo is not None else x.replace(tzinfo=pytz.utc)
            )
            if created_timestamp_column:
                offline_data_df[created_timestamp_column] = pd.to_datetime(offline_data_df[created_timestamp_column])
                offline_data_df[created_timestamp_column] = offline_data_df[
                    created_timestamp_column
                ].apply(
                    lambda x: x if x.tzinfo is not None else x.replace(tzinfo=pytz.utc)
                )

            offline_data_columns = set(offline_data_df.columns)
            if not set(join_key_columns).issubset(offline_data_columns):
                raise KfsJoinKeysDuringMaterialization(
                    data_source.path, set(join_key_columns), offline_data_columns
                )

            ts_columns = (
                [event_timestamp_column, created_timestamp_column]
                if created_timestamp_column
                else [event_timestamp_column]
            )

            offline_data_df.sort_values(by=ts_columns, inplace=True)

            filtered_df = offline_data_df[
                (offline_data_df[event_timestamp_column] >= start_date)
                & (offline_data_df[event_timestamp_column] < end_date)
            ]

            columns_to_extract = set(
                join_key_columns + feature_name_columns + ts_columns
            )
            if join_key_columns:
                last_values_df = filtered_df.drop_duplicates(
                    join_key_columns, keep="last", ignore_index=True
                )
            else:
                last_values_df = filtered_df
                # last_values_df[DUMMY_ENTITY_ID] = DUMMY_ENTITY_VAL
                # columns_to_extract.add(DUMMY_ENTITY_ID)

            return last_values_df[columns_to_extract]

        # When materializing a single feature view, we don't need full feature names. On demand transforms aren't materialized
        return FileRetrievalJob(
            evaluation_function=evaluate_offline_job,
        )

    @staticmethod
    def write_offline_features(
        config: RepoConfig,
        data: Optional[Union[pd.DataFrame, pyspark.sql.DataFrame]],
        # entity_df: Union[pd.DataFrame, pyspark.sql.DataFrame, str],
        tables_to_keep: Sequence[Union[FeatureTable, FeatureView]],
        entities_to_keep: Sequence[Entity],
        # feature_views: List[FeatureView],
        # registry: Registry,
        # format: Optional[str] = "parquet",
        # mode: Optional[str] = "append",
    ):
        """
        Args:
            config: RepoConfig
            data: dataframe or file_name or file_path Union[pd.DataFrame, pyspark.sql.DataFrame, str]
            tables_to_keep: name of the feature view or feature that needs to be updated
            entities_to_keep: entity key names that needs to be updated

        """
        # # SparkSession
        # _spark_session = SparkSession.builder.getOrCreate()
        # _spark_context = _spark_session.sparkContext
        # _jvm = _spark_context._jvm

        # _spark_session.conf.set("hive.exec.dynamic.partition", "true")
        # _spark_session.conf.set("hive.exec.dynamic.partition.mode", "nonstrict")
        # _spark_session.conf.set("spark.sql.hive.convertMetastoreParquet", "false")

        offline_store_file_path = str(config.repo_path / config.offline_store.path)
        Path(offline_store_file_path).parent.mkdir(exist_ok=True)

        for view in tables_to_keep:
            view.is_valid()
            feature_view_dict = view.to_dict()
            # cols = [feature for feature in feature_view_dict["features"]] + [entities for entities in feature_view_dict["entities"]]
            cols = list(feature_view_dict["features"]) + list(feature_view_dict["entities"])

        cols += [feature_view_dict["batch_source"]["event_timestamp_column"]]
        if feature_view_dict["batch_source"]["created_timestamp_column"]:
            cols += [feature_view_dict["batch_source"]["created_timestamp_column"]]

        if data is None:

            data_url = feature_view_dict["batch_source"]["file_options"]["file_url"]

            # read with spark
            # spark_df = _spark_session.read.parquet(data)

            # read with pandas
            if feature_view_dict["batch_source"]['file_options']['file_format'].lower() == 'csv':
                pandas_df = pd.read_csv(data_url, engine="c")
            if feature_view_dict["batch_source"]['file_options']['file_format'].lower() == 'parquet':
                pandas_df = pd.read_parquet(data_url, engine="pyarrow")

            pandas_df = pd.DataFrame(pandas_df, columns=cols)

            # choose given features
            # for feature_view in feature_views:
            #     cols = [feature.name for features in feature_view["feature"] for feature in features]

            # spark_df.select([col for col in spark_df.columns if col in cols])

            # write
            if feature_view_dict["batch_source"]["file_options"]["file_format"] == "parquet" or "csv":
                # spark_df.write.parquet("demo_store.parquet")
                # _spark_session.stop()
                pandas_df.to_parquet(offline_store_file_path, use_deprecated_int96_timestamps=True, engine="pyarrow")

                # collecting feature names and dtypes of given features
                feature_columns = pandas_df.columns.tolist()
                feature_dtypes = [dtype.name for dtype in pandas_df.dtypes]

            else:
                print(f"Provided format: {feature_view_dict['batch_source']['file_options']['file_format']} is currently not supported.")

        else:
            if isinstance(data, pd.DataFrame):
                data.to_parquet(offline_store_file_path, use_deprecated_int96_timestamps=True, engine="pyarrow")

                # collecting feature names and dtypes of given features
                feature_columns = data.columns.tolist()
                feature_dtypes = [dtype.name for dtype in data.dtypes]

            elif isinstance(data, pyspark.sql.DataFrame):
                mode = feature_view_dict["batch_source"]["df_options"]["mode"]

                # for example (experimental)
                # data.to_pandas()

                data.write.format("parquet").mode(mode).save(offline_store_file_path)

                # collecting feature names and dtypes of given features
                feature_columns = data.columns
                feature_dtypes = [dtype[1] for dtype in data.dtypes]

        # if feature_view_dict["batch_source"]["file_options"]["file_format"] == "csv":
        #     # spark_df.write.parquet("demo_store.parquet")
        #     # _spark_session.stop()
        #     pandas_df.to_csv(file_path)

        # if format:
        #     return ParquetFormat()

        # if format:
        #     return CSVFormat()

        # # pandas dataframe
        # if isinstance(data, pd.DataFrame):
        #     pass

        # # spark dataframe
        # elif isinstance(data, pyspark.sql.DataFrame):
        #     pass

        # # csv file
        # elif isinstance(data.rsplit('.', 1)[-1], 'csv'):
        #     pass

        # # parquet file
        # elif isinstance(data.rsplit('.', 1)[-1], 'parquet'):
        #     pass

        return [{'name': n, 'value_type': feature_dtypes[i]} for i, n in enumerate(feature_columns)]
