#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from typing import List, Optional, Tuple, Union
import pandas as pd
import pytz
import psycopg2
from psycopg2 import sql
from datetime import datetime
from pathlib import Path

from katonic.fs.entities.feature_table import FeatureTable
from katonic.fs.entities.feature_view import FeatureView
from katonic.fs.registry import Registry


from katonic.fs.registry_store import RegistryStore
from katonic.fs.repo_config import RegistryConfig


class PostgreSQLRegistryStore(RegistryStore):

    _conn: Optional[psycopg2.connect] = None

    def __init__(self, registry_config: RegistryConfig, repo_path: Path):
        self._registry_config = registry_config
    
    def _get_postgres_reg_conn(self, config: RegistryConfig):
        
        if not self._conn:
            self._conn = psycopg2.connect(
                dbname=config.db,
                host=config.host,
                port=int(config.port),
                user=config.user,
                password=config.password,
                options="-c search_path={}".format(
                    config.db_schema or config.user
                ),
            )

        return self._conn

    def create_registry(self, table_query: str, index_query: str):

        with self._get_postgres_reg_conn(self._registry_config) as conn, conn.cursor() as cur:
            cur.execute(sql.SQL(table_query))
            cur.execute(sql.SQL(index_query))
            conn.commit()

    def get_registry(self, get_query: str):

        with self._get_postgres_reg_conn(self._registry_config) as conn:

            return pd.read_sql_query(sql.SQL(get_query), conn)

    def update_registry(self, update_query: Tuple, insert_query: Tuple):
        self._write_registry(update_query, insert_query)

    def teardown(self, config: RegistryConfig):
        with self._get_postgres_reg_conn(self._registry_config) as conn: #, conn.cursor() as cur:
            conn.dispose()

        # try:
        #     self._get_postgres_reg_conn(config).dispose()
        # except ConnectionAbortedError:
        #     # If the file deletion fails with FileNotFoundError, the file has already
        #     # been deleted.
        #     pass

    def _write_registry(self, update_query: Tuple, insert_query: Tuple):

        with self._get_postgres_reg_conn(self._registry_config) as conn, conn.cursor() as cur:
            update_sql_query, update_values = update_query
            cur.execute(update_sql_query, update_values)
            insert_sql_query, insert_values = insert_query
            cur.execute(insert_sql_query, insert_values)
            conn.commit()

    def get_feature_view(self, get_query: str) -> pd.DataFrame:
        """
        Retrieves a feature view.

        Args:
            get_query: SQL Query to get feature view

        Returns:
            Returns the feature views associated with specified project
        """

        with self._get_postgres_reg_conn(self._registry_config) as conn, conn.cursor() as cur:

            return pd.read_sql_query(sql.SQL(get_query), conn)


def _table_id(project: str, table: Union[FeatureTable, FeatureView]) -> str:
    return f"{project}_{table.name}"


def _to_naive_utc(ts: datetime):
    if ts.tzinfo is None:
        return ts
    else:
        return ts.astimezone(pytz.utc).replace(tzinfo=None)