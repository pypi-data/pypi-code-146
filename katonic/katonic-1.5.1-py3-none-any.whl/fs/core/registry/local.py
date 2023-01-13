#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from contextlib import closing
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple, Union

import pytz

from katonic.fs.entities import FeatureTable
from katonic.fs.entities.feature_view import FeatureView
from katonic.fs.core.passthrough_provider import PassthroughProvider
from katonic.fs.registry_store import RegistryStore
from katonic.fs.repo_config import RegistryConfig


class LocalProvider(PassthroughProvider):
    """
    This class only exists for backwards compatibility.
    """

    pass


class LocalRegistryStore(RegistryStore):

    _conn: Optional[sqlite3.Connection] = None

    def __init__(self, registry_config: RegistryConfig, repo_path: Path):
        registry_path = Path(registry_config.path)
        self._registry_config = registry_config

        if registry_path.is_absolute():
            self._filepath = registry_path
        else:
            self._filepath = repo_path.joinpath(registry_path)

    def _get_sqlite_reg_conn(self, config: RegistryConfig):
        if not self._conn:
            db_path = self._filepath
            Path(db_path).parent.mkdir(exist_ok=True)
            self._conn = sqlite3.connect(
                db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
            )
        return self._conn

    def create_registry(self, table_query: str, index_query: str):
        
        if not self._filepath.exists():
            with self._get_sqlite_reg_conn(self._registry_config) as conn:
                conn.execute(table_query)
                conn.execute(index_query)
                
        # raise FileNotFoundError(
        #     f'Registry not found at path "{self._filepath}". Have you initializes "FeatureStore"?'
        # )

    def get_registry(self, get_query: str):

        if self._filepath.exists():
            with closing(self._get_sqlite_reg_conn(self._registry_config).cursor()) as cur:
                cur.execute(get_query)

                return list(cur.fetchall())

        # raise FileNotFoundError(
        #     f'Registry not found at path "{self._filepath}". Have you initializes "FeatureStore"?'
        # )

    def update_registry(self, update_query: Tuple, insert_query: Tuple):
        self._write_registry(update_query, insert_query)

    def teardown(self):
        try:
            self._filepath.unlink()
        except FileNotFoundError:
            # If the file deletion fails with FileNotFoundError, the file has already
            # been deleted.
            pass

    def _write_registry(self, update_query: Tuple, insert_query: Tuple):

        conn = self._get_sqlite_reg_conn(self._registry_config)
        # cur = conn.cursor()

        if self._filepath.exists():
            update_sql_query, update_values = update_query
            conn.execute(update_sql_query, update_values)
            insert_sql_query, insert_values = insert_query
            conn.execute(insert_sql_query, insert_values)
            conn.commit()
        # raise FileNotFoundError(
        #     f'Registry not found at path "{self._filepath}". Have you initializes "FeatureStore"?'
        # )


def _table_id(project: str, table: Union[FeatureTable, FeatureView]) -> str:
    return f"{project}_{table.name}"


def _to_naive_utc(ts: datetime):
    if ts.tzinfo is None:
        return ts
    else:
        return ts.astimezone(pytz.utc).replace(tzinfo=None)