#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from typing import Any, Callable, ContextManager, Dict, Iterator, List, Optional, Sequence, Union
import psycopg2
import psycopg2.extras
from pydantic.types import StrictStr
import contextlib
from datetime import datetime

import pyspark
import pandas as pd
import pyarrow as pa
from psycopg2 import sql
from katonic.fs.core.offline_stores.postgres_source import PostgreSQLSource
from katonic.fs.core.offline_stores.dataframe_source import DataFrameSource
from katonic.fs.core.offline_stores.postgres_util import PostgreSQLConfig, get_postgres_conn

from katonic.fs.data_source import DataSource
from katonic.fs.core.offline_stores.offline_store import RetrievalJob
from katonic.fs.core.offline_stores.offline_store import OfflineStore
from katonic.fs.entities.feature_table import FeatureTable
from katonic.fs.entities.feature_view import FeatureView
from katonic.fs.entities.entity import Entity
from katonic.fs.registry import Registry
from katonic.fs.repo_config import RepoConfig
from katonic.fs.type_map import arrow_to_pg_type, pg_type_code_to_arrow
from katonic.fs.core.offline_stores.offline_utils import (
    df_to_create_table_sql,
    build_point_in_time_query,
    get_expected_join_keys,
    get_feature_view_query_context,
    get_temp_entity_table_name,
    infer_event_timestamp_from_entity_df,
    assert_expected_columns_in_entity_df
)


class PostgreSQLOfflineStoreConfig(PostgreSQLConfig):
    type: Optional[StrictStr]

    db_schema: Optional[StrictStr] = None


class PostgreSQLOfflineStore(OfflineStore):
    offline_table_name: str

    @staticmethod
    def pull_latest_from_table_or_query(
        config: RepoConfig,
        data_source: DataSource,
        join_key_columns: List[str],
        feature_name_columns: List[str],
        event_timestamp_column: str,
        created_timestamp_column: Optional[str],
        start_date: datetime,
        end_date: datetime,
    ) -> RetrievalJob:
        assert isinstance(data_source, (PostgreSQLSource, DataFrameSource))
        from_expression = (f"SELECT * FROM {PostgreSQLOfflineStore.offline_table_name}")

        partition_by_join_key_string = ", ".join(_append_alias(join_key_columns, "a"))
        if partition_by_join_key_string != "":
            partition_by_join_key_string = f'PARTITION BY {partition_by_join_key_string}'
        timestamps = [event_timestamp_column]
        if created_timestamp_column:
            timestamps.append(created_timestamp_column)
        timestamp_desc_string = " DESC, ".join(_append_alias(timestamps, "a")) + " DESC"
        a_field_string = ", ".join(
            _append_alias(join_key_columns + feature_name_columns + timestamps, "a")
        )
        b_field_string = ", ".join(
            _append_alias(join_key_columns + feature_name_columns + timestamps, "b")
        )

        query = f"""
            SELECT
                {b_field_string}
            FROM (
                SELECT {a_field_string},
                ROW_NUMBER() OVER({partition_by_join_key_string} ORDER BY {timestamp_desc_string}) AS _kfs_row
                FROM ({from_expression}) a
                WHERE a.{event_timestamp_column} BETWEEN '{start_date}'::timestamptz AND '{end_date}'::timestamptz
            ) b
            WHERE _kfs_row = 1
            """

        return PostgreSQLRetrievalJob(
            query=query,
            config=config,
            full_feature_names=False,
        )

    @staticmethod
    def get_historical_features(
        config: RepoConfig,
        feature_views: List[FeatureView],
        feature_refs: List[str],  # unnecessary feature_refs remove it
        entity_df: Union[pd.DataFrame, str],
        registry: Registry,
        project: str,
        full_feature_names: bool = False,
    ) -> RetrievalJob:
        @contextlib.contextmanager
        def query_generator() -> Iterator[str]:
            table_name = get_temp_entity_table_name()
            entity_schema = _df_to_table(config.offline_store, entity_df, table_name)

            entity_df_event_timestamp_col = infer_event_timestamp_from_entity_df(
                entity_schema
            )

            expected_join_keys = get_expected_join_keys(
                project, feature_views, registry
            )

            assert_expected_columns_in_entity_df(
                entity_schema, expected_join_keys, entity_df_event_timestamp_col
            )

            query_context = get_feature_view_query_context(
                feature_refs, feature_views, registry, project,
            )

            query = build_point_in_time_query(
                query_context,
                left_table_query_string=table_name,
                entity_df_event_timestamp_col=entity_df_event_timestamp_col,
                query_template=MULTIPLE_FEATURE_VIEW_POINT_IN_TIME_JOIN,
                full_feature_names=full_feature_names,
            )

            try:
                yield query
            finally:
                with get_postgres_conn(config.offline_store) as conn, conn.cursor() as cur:
                    cur.execute(
                        sql.SQL(
                            """
                            DROP TABLE IF EXISTS {};
                            """
                        ).format(sql.Identifier(table_name)),
                    )

        return PostgreSQLRetrievalJob(
            query=query_generator,
            config=config,
            full_feature_names=full_feature_names,
        )

    @staticmethod
    def write_offline_features(
        config: RepoConfig,
        data: Optional[Union[pd.DataFrame, pyspark.sql.DataFrame]],
        tables_to_keep: Sequence[Union[FeatureTable, FeatureView]],
        entities_to_keep: Sequence[Entity],
    ):
        """
        Args:
            config: RepoConfig
            data: dataframe or file_name or file_path Union[pd.DataFrame, pyspark.sql.DataFrame, str]
            tables_to_keep: name of the feature view or feature that needs to be updated
            entities_to_keep: entity key names that needs to be updated

        """
        for view in tables_to_keep:
            view.is_valid()
            feature_view_dict = view.to_dict()
            cols = list(feature_view_dict["features"]) + list(feature_view_dict["entities"])

        cols += [feature_view_dict["batch_source"]["event_timestamp_column"]]
        if feature_view_dict["batch_source"]["created_timestamp_column"]:
            cols += [feature_view_dict["batch_source"]["created_timestamp_column"]]

        offline_table_name = PostgreSQLOfflineStore.offline_table_name = f"{feature_view_dict['name']}_offline_store"

        # read and write with psycopg2
        with get_postgres_conn(config.offline_store) as conn, conn.cursor() as cur:

            if data is None:
                data_query = feature_view_dict["batch_source"]["custom_options"]["configuration"]["query"]

                cur.execute(
                    sql.SQL(data_query),
                )
                tuples = cur.fetchall()
                df_columns = pd.read_sql(f"{data_query} LIMIT 1", conn,)
                df = pd.DataFrame(tuples, columns=df_columns.columns)

            elif isinstance(data, pd.DataFrame):
                df = data
            elif isinstance(data, pyspark.sql.DataFrame):
                df = data.toPandas()

            # filter desired/given columns
            df = df[cols]

            # Creating a list of tupples from the dataframe values
            tpls = [tuple(x) for x in df.to_numpy()]

            columns = [
                f""""{col_name}" {arrow_to_pg_type(str(col_type))}""" for col_name, col_type in zip(df.columns, df.dtypes)
            ]
            cur.execute(
                f"""
                CREATE TABLE "{offline_table_name}" (
                    {", ".join(columns)}
                );
                """
            )

            conn.commit()

            # SQL query to execute
            query = "INSERT INTO %s(%s) VALUES %%s " % (offline_table_name, ", ".join(cols))
            psycopg2.extras.execute_values(cur, query, tpls)

            feature_columns = df.columns.tolist()
            feature_dtypes = [dtype.name for dtype in df.dtypes]

        return [{'name': n, 'value_type': feature_dtypes[i]} for i, n in enumerate(feature_columns)]


def _df_to_table(
    config: PostgreSQLOfflineStoreConfig, entity_df: Union[pd.DataFrame, str], table_name: str
) -> Dict[str, str]:
    if isinstance(entity_df, pd.DataFrame):
        return df_to_postgres_table(config, entity_df, table_name)
    elif isinstance(entity_df, str):
        return sql_to_postgres_table(config, entity_df, table_name)
    else:
        raise TypeError(entity_df)


class PostgreSQLRetrievalJob(RetrievalJob):
    def __init__(
        self,
        query: Union[str, Callable[[], ContextManager[str]]],
        config: RepoConfig,
        full_feature_names: bool,
    ):
        if not isinstance(query, str):
            self._query_generator = query
        else:

            @contextlib.contextmanager
            def query_generator() -> Iterator[str]:
                assert isinstance(query, str)
                yield query

            self._query_generator = query_generator
        self.config = config
        self.connection = get_postgres_conn(self.config.offline_store)
        self._full_feature_names = full_feature_names

    @property
    def full_feature_names(self) -> bool:
        return self._full_feature_names

    def _to_df_internal(self) -> pd.DataFrame:
        # We use arrow format because it gives better control of the table schema
        return self._to_arrow_internal().to_pandas()

    def to_sql(self) -> str:
        with self._query_generator() as query:
            return query

    def _to_arrow_internal(self) -> pa.Table:
        with self._query_generator() as query, self.connection as conn, conn.cursor() as cur:
            cur.execute(query)
            fields = [
                (c.name, pg_type_code_to_arrow(c.type_code))
                for c in cur.description
            ]
            data = cur.fetchall()
            schema = pa.schema(fields)
            # TODO: Fix...
            data_transposed: List[List[Any]] = []
            for col in range(len(fields)):
                data_transposed.append([])
                for row in range(len(data)):
                    data_transposed[col].append(data[row][col])

            # table
            return pa.Table.from_arrays(
                [pa.array(row) for row in data_transposed], schema=schema
            )


def _append_alias(field_names: List[str], alias: str) -> List[str]:
    return [f"{alias}.{field_name}" for field_name in field_names]


def df_to_postgres_table(
    config: PostgreSQLOfflineStoreConfig, df: pd.DataFrame, table_name: str
) -> Dict[str, str]:
    """
    Create a table for the data frame, insert all the values, and return the table schema
    """
    with get_postgres_conn(config) as conn, conn.cursor() as cur:
        cur.execute(df_to_create_table_sql(df, table_name))
        psycopg2.extras.execute_values(
            cur,
            f"""
            INSERT INTO {table_name}
            VALUES %s
            """,
            df.to_numpy(),
        )
        return dict(zip(df.columns, df.dtypes))


def sql_to_postgres_table(
    config: PostgreSQLOfflineStoreConfig, sql_query: str, table_name: str
) -> Dict[str, str]:
    """
    Create a table for the sql statement and return the table schema
    """
    with get_postgres_conn(config) as conn, conn.cursor() as cur:
        cur.execute(
            sql.SQL(
                """
                CREATE TABLE {} AS ({});
                """
            ).format(sql.Identifier(table_name), sql.Literal(sql_query),),
        )
        df = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 1", conn,)
        return dict(zip(df.columns, df.dtypes))


MULTIPLE_FEATURE_VIEW_POINT_IN_TIME_JOIN = """
/*
 Compute a deterministic hash for the `left_table_query_string` that will be used throughout
 all the logic as the field to GROUP BY the data
*/
WITH entity_dataframe AS (
    SELECT *,
        {{entity_df_event_timestamp_col}} AS entity_timestamp
        {% for featureview in featureviews %}
            {% if featureview.entities %}
            ,(
                {% for entity in featureview.entities %}
                    CAST({{entity}} as VARCHAR) ||
                {% endfor %}
                CAST({{entity_df_event_timestamp_col}} AS VARCHAR)
            ) AS {{featureview.name}}__entity_row_unique_id
            {% else %}
            ,CAST({{entity_df_event_timestamp_col}} AS VARCHAR) AS {{featureview.name}}__entity_row_unique_id
            {% endif %}
        {% endfor %}
    FROM {{ left_table_query_string }}
),

{% for featureview in featureviews %}

{{ featureview.name }}__entity_dataframe AS (
    SELECT
        {{ featureview.entities | join(', ')}}{% if featureview.entities %},{% else %}{% endif %}
        entity_timestamp,
        {{featureview.name}}__entity_row_unique_id
    FROM entity_dataframe
    GROUP BY
        {{ featureview.entities | join(', ')}}{% if featureview.entities %},{% else %}{% endif %}
        entity_timestamp,
        {{featureview.name}}__entity_row_unique_id
),

/*
 This query template performs the point-in-time correctness join for a single feature set table
 to the provided entity table.

 1. We first join the current feature_view to the entity dataframe that has been passed.
 This JOIN has the following logic:
    - For each row of the entity dataframe, only keep the rows where the `event_timestamp_column`
    is less than the one provided in the entity dataframe
    - If there a TTL for the current feature_view, also keep the rows where the `event_timestamp_column`
    is higher the the one provided minus the TTL
    - For each row, Join on the entity key and retrieve the `entity_row_unique_id` that has been
    computed previously

 The output of this CTE will contain all the necessary information and already filtered out most
 of the data that is not relevant.
*/

{{ featureview.name }}__subquery AS (
    SELECT
        {{ featureview.event_timestamp_column }} as event_timestamp,
        {{ featureview.created_timestamp_column ~ ' as created_timestamp,' if featureview.created_timestamp_column else '' }}
        {{ featureview.entity_selections | join(', ')}}{% if featureview.entity_selections %},{% else %}{% endif %}
        {% for feature in featureview.features %}
            {{ feature }} as {% if full_feature_names %}{{ featureview.name }}__{{feature}}{% else %}{{ feature }}{% endif %}{% if loop.last %}{% else %}, {% endif %}
        {% endfor %}
    FROM {{ featureview.table_subquery }} sub
    WHERE {{ featureview.event_timestamp_column }} <= (SELECT MAX(entity_timestamp) FROM entity_dataframe)
    
    /*
    {% if featureview.ttl == 0 %}{% else %}
    AND {{ featureview.event_timestamp_column }} >= (SELECT MIN(entity_timestamp) FROM entity_dataframe) - {{ featureview.ttl }} * interval '1' second
    {% endif %} 
    */
),

{{ featureview.name }}__base AS (
    SELECT
        subquery.*,
        entity_dataframe.entity_timestamp,
        entity_dataframe.{{featureview.name}}__entity_row_unique_id
    FROM {{ featureview.name }}__subquery AS subquery
    INNER JOIN {{ featureview.name }}__entity_dataframe AS entity_dataframe
    ON TRUE
        AND subquery.event_timestamp <= entity_dataframe.entity_timestamp

        /*
        {% if featureview.ttl == 0 %}{% else %}
        AND subquery.event_timestamp >= entity_dataframe.entity_timestamp - {{ featureview.ttl }} * interval '1' second
        {% endif %}
        */

        {% for entity in featureview.entities %}
        AND subquery.{{ entity }} = entity_dataframe.{{ entity }}
        {% endfor %}
),

/*
 2. If the `created_timestamp_column` has been set, we need to
 deduplicate the data first. This is done by calculating the
 `MAX(created_at_timestamp)` for each event_timestamp.
 We then join the data on the next CTE
*/
{% if featureview.created_timestamp_column %}
{{ featureview.name }}__dedup AS (
    SELECT
        {{featureview.name}}__entity_row_unique_id,
        event_timestamp,
        MAX(created_timestamp) as created_timestamp
    FROM {{ featureview.name }}__base
    GROUP BY {{featureview.name}}__entity_row_unique_id, event_timestamp
),
{% endif %}

/*
 3. The data has been filtered during the first CTE "*__base"
 Thus we only need to compute the latest timestamp of each feature.
*/
{{ featureview.name }}__latest AS (
    SELECT
        {{featureview.name}}__entity_row_unique_id,
        MAX(event_timestamp) AS event_timestamp
        {% if featureview.created_timestamp_column %}
            ,MAX(created_timestamp) AS created_timestamp
        {% endif %}

    FROM {{ featureview.name }}__base
    {% if featureview.created_timestamp_column %}
        INNER JOIN {{ featureview.name }}__dedup
        USING ({{featureview.name}}__entity_row_unique_id, event_timestamp, created_timestamp)
    {% endif %}

    GROUP BY {{featureview.name}}__entity_row_unique_id
),

/*
 4. Once we know the latest value of each feature for a given timestamp,
 we can join again the data back to the original "base" dataset
*/
{{ featureview.name }}__cleaned AS (
    SELECT base.*
    FROM {{ featureview.name }}__base as base
    INNER JOIN {{ featureview.name }}__latest
    USING(
        {{featureview.name}}__entity_row_unique_id,
        event_timestamp
        {% if featureview.created_timestamp_column %}
            ,created_timestamp
        {% endif %}
    )
) {% if loop.last %}{% else %}, {% endif %}


{% endfor %}
/*
 Joins the outputs of multiple time travel joins to a single table.
 The entity_dataframe dataset being our source of truth here.
 */

SELECT *
FROM entity_dataframe
{% for featureview in featureviews %}
LEFT JOIN (
    SELECT
        {{featureview.name}}__entity_row_unique_id
        {% for feature in featureview.features %}
            ,{% if full_feature_names %}{{ featureview.name }}__{{feature}}{% else %}{{ feature }}{% endif %}
        {% endfor %}
    FROM {{ featureview.name }}__cleaned
) {{featureview.name}} USING ({{featureview.name}}__entity_row_unique_id)
{% endfor %}
"""
