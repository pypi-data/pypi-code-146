#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

import os
from typing_extensions import Literal
from pydantic.types import StrictStr
from pathlib import Path
import pytz
import sqlite3
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union
from datetime import datetime

from katonic.fs.entities.entity import Entity
from katonic.fs.entities.feature_table import FeatureTable
from katonic.fs.entities.feature_view import FeatureView

from katonic.fs.core.online_stores.online_store import OnlineStore
from katonic.fs.repo_config import KfsConfigBaseModel, RepoConfig


class SqliteOnlineStoreConfig(KfsConfigBaseModel):
    """ Online store config for local (SQLite-based) store """

    type: Literal[
        "sqlite", "katonic.fs.core.online_stores.sqlite.SqliteOnlineStore"
    ] = "sqlite"
    """ Online store type selector"""

    path: StrictStr = "data/online.db"
    """ (optional) Path to sqlite db """


class SqliteOnlineStore(OnlineStore):
    """
    OnlineStore is an object used for all interaction between KFS and the service used for offline storage of
    features.
    """

    _conn: Optional[sqlite3.Connection] = None

    @staticmethod
    def _get_db_path(config: RepoConfig) -> str:
        assert (
            config.online_store.type == "sqlite"
            or config.online_store.type.endswith("SqliteOnlineStore")
        )

        if config.repo_path and not Path(config.online_store.path).is_absolute():
            return str(config.repo_path / config.online_store.path)
        else:
            return config.online_store.path

    def _get_sqlite_conn(self, config: RepoConfig):
        if not self._conn:
            db_path = self._get_db_path(config)
            Path(db_path).parent.mkdir(exist_ok=True)
            self._conn = sqlite3.connect(
                db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
            )
        return self._conn

    def online_write_batch(
        self,
        config: RepoConfig,
        table: Union[FeatureTable, FeatureView],
        data: List[
            Tuple[Dict[str, Any], Dict[str, Any], datetime, Optional[datetime]]
        ],
    ) -> None:
        conn = self._get_sqlite_conn(config)

        project = config.project

        with conn:
            for entity_keys, values, timestamp, created_ts in data:
                timestamp = _to_naive_utc(timestamp)
                if created_ts is not None:
                    created_ts = _to_naive_utc(created_ts)

                # issue with entity_key and value access for writing in database
                entity_key = table.entities[0]
                entity_val = entity_keys[entity_key]
                for feature_name, val in values.items():
                    conn.execute(
                        f"""
                            UPDATE {_table_id(project, table)}
                            SET value = ?, event_ts = ?, created_ts = ?
                            WHERE (entity_key = ? AND entity_value = ? AND feature_name = ?)
                        """,
                        (
                            # SET
                            val,
                            timestamp,
                            created_ts,
                            # WHERE
                            entity_key,
                            entity_val,
                            feature_name,
                        ),
                    )

                    conn.execute(
                        f"""INSERT OR IGNORE INTO {_table_id(project, table)}
                            (entity_key, entity_value, feature_name, value, event_ts, created_ts)
                            VALUES (?, ?, ?, ?, ?, ?)""",
                        (
                            entity_key,
                            entity_val,
                            feature_name,
                            val,
                            timestamp,
                            created_ts,
                        ),
                    )

    def online_read(
        self,
        config: RepoConfig,
        table: Union[FeatureTable, FeatureView],
        entity_keys: List[Dict[str, Any]],
        requested_features: Optional[List[str]] = None,
    ) -> List[Tuple[Optional[datetime], Optional[Dict[str, Any]]]]:
        conn = self._get_sqlite_conn(config)
        cur = conn.cursor()

        result: List[Tuple[Optional[datetime], Optional[Dict[str, Any]]]] = []

        project = config.project
        for entity_dict in entity_keys:
            entity_key = table.entities[0]
            entity_value = entity_dict[entity_key]  # issue with entities for key, value and feature view storage in registry
            cur.execute(
                f"SELECT feature_name, value, event_ts FROM {_table_id(project, table)} WHERE (entity_key = ? AND entity_value = ?)",
                (entity_key, entity_value),
            )

            res = {}
            res_ts = None
            for feature_name, val, ts in cur.fetchall():
                res[feature_name] = val
                res_ts = ts

            if not res:
                result.append((None, None))
            else:
                result.append((res_ts, res))
        return result

    def update(
        self,
        config: RepoConfig,
        tables_to_keep: Sequence[Union[FeatureTable, FeatureView]],
        entities_to_keep: Sequence[Entity],
    ):
        conn = self._get_sqlite_conn(config)
        project = config.project

        for table in tables_to_keep:
            conn.execute(
                f"CREATE TABLE IF NOT EXISTS {_table_id(project, table)} (entity_key TEXT, entity_value BLOB, feature_name TEXT, value BLOB, event_ts timestamp, created_ts timestamp,  PRIMARY KEY(entity_key, entity_value, feature_name))"
            )
            conn.execute(
                f"CREATE INDEX IF NOT EXISTS {_table_id(project, table)}_ek ON {_table_id(project, table)} (entity_key, entity_value);"
            )

    def teardown(
        self,
        config: RepoConfig,
        tables: Sequence[Union[FeatureTable, FeatureView]],
        entities: Sequence[Entity],
    ):
        try:
            os.unlink(self._get_db_path(config))
        except FileNotFoundError:
            pass


def _table_id(project: str, table: Union[FeatureTable, FeatureView]) -> str:
    return f"{project}_{table.name}"


def _to_naive_utc(ts: datetime):
    if ts.tzinfo is None:
        return ts
    else:
        return ts.astimezone(pytz.utc).replace(tzinfo=None)
