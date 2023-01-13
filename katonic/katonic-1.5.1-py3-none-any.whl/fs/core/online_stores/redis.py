#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

import json
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from google.protobuf.timestamp_pb2 import Timestamp
from pydantic import StrictStr
from pydantic.typing import Literal

from katonic.fs.entities import Entity, FeatureTable, FeatureView
from katonic.fs.core.online_stores.helpers import _mmh3
from katonic.fs.core.online_stores.online_store import OnlineStore
from katonic.fs.repo_config import KfsConfigBaseModel, RepoConfig
from katonic.fs import utils

from rediscluster import RedisCluster
from redis import Redis


EX_SECONDS = 253402300799


class RedisType(str, Enum):
    redis = "redis"
    redis_cluster = "redis_cluster"


class RedisOnlineStoreConfig(KfsConfigBaseModel):
    """Online store config for Redis store"""

    type: Literal["redis"] = "redis"
    """Online store type selector"""

    redis_type: RedisType = RedisType.redis
    """Redis type: redis or redis_cluster"""

    connection_string: StrictStr = "localhost:6379"
    """Connection string containing the host, port, and configuration parameters for Redis
     format: host:port,parameter1,parameter2 eg. redis:6379,db=0 """


class RedisOnlineStore(OnlineStore):
    _client: Optional[Union[Redis, RedisCluster]] = None

    def update(
        self,
        config: RepoConfig,
        tables_to_keep: Sequence[Union[FeatureTable, FeatureView]],
        entities_to_keep: Sequence[Entity],
    ):
        """
        There's currently no setup done for Redis.
        """
        pass

    def teardown(
        self,
        config: RepoConfig,
        tables: Sequence[Union[FeatureTable, FeatureView]],
        entities: Sequence[Entity],
    ):
        """
        There's currently no teardown done for Redis.
        """
        pass

    @staticmethod
    def _parse_connection_string(connection_string: str):
        """
        Reads Redis connections string using format
        for RedisCluster:
            redis1:6379,redis2:6379,decode_responses=true,skip_full_coverage_check=true,ssl=true,password=...
        for Redis:
            redis_master:6379,db=0,ssl=true,password=...
        """
        startup_nodes = [
            dict(zip(["host", "port", "password"], c.split(":")))
            for c in connection_string.split(",")
            if "=" not in c
        ]
        params = {}
        for c in connection_string.split(","):
            if "=" in c:
                kv = c.split("=", 1)
                try:
                    kv[1] = json.loads(kv[1])
                except json.JSONDecodeError:
                    ...

                it = iter(kv)
                params.update(dict(zip(it, it)))

        return startup_nodes, params

    def _get_client(self, online_store_config: RedisOnlineStoreConfig):
        """
        Creates the Redis client RedisCluster or Redis depending on configuration
        """
        if not self._client:
            startup_nodes, kwargs = self._parse_connection_string(
                online_store_config.connection_string
            )
            if online_store_config.type == RedisType.redis_cluster:
                kwargs["startup_nodes"] = startup_nodes
                self._client = RedisCluster(**kwargs)
            else:
                kwargs["host"] = startup_nodes[0]["host"]
                kwargs["port"] = startup_nodes[0]["port"]
                if 'localhost' not in kwargs["host"]:
                    kwargs["password"] = startup_nodes[0]["password"]

                self._client = Redis(**kwargs)
        return self._client

    def online_write_batch(
        self,
        config: RepoConfig,
        table: Union[FeatureTable, FeatureView],
        data: List[
            Tuple[Dict[str, Any], Dict[str, Any], datetime, Optional[datetime]]
        ],
    ) -> None:
        online_store_config = config.online_store
        assert isinstance(online_store_config, RedisOnlineStoreConfig)

        client = self._get_client(online_store_config)
        project = config.project

        entity_hset = {}
        feature_view = table.name

        ex = Timestamp()
        ex.seconds = EX_SECONDS
        ex_str = ex.SerializeToString()

        for entity_key, values, timestamp, created_ts in data:
            for key, value in entity_key.items():
                entity_key_string = f"{key}_{value}"
                break
            redis_key = f"{project}_{entity_key_string}"
            # redis_key_bin = _redis_key(project, entity_key_string)
            ts = Timestamp()
            ts.seconds = int(utils.make_tzaware(timestamp).timestamp())
            entity_hset[f"_ts:{feature_view}"] = ts.SerializeToString()
            entity_hset[f"_ex:{feature_view}"] = ex_str

            for feature_name, val in values.items():
                f_key = _mmh3(f"{feature_view}:{feature_name}")
                entity_hset[f_key] = val

            client.hmset(redis_key, mapping=entity_hset)

    def online_read(
        self,
        config: RepoConfig,
        table: Union[FeatureTable, FeatureView],
        entity_keys: List[Dict[str, Any]],
        requested_features: Optional[List[str]] = None,
    ) -> List[Tuple[Optional[datetime], Optional[Dict[str, Any]]]]:
        online_store_config = config.online_store
        assert isinstance(online_store_config, RedisOnlineStoreConfig)

        client = self._get_client(online_store_config)
        feature_view = table.name
        project = config.project

        result: List[Tuple[Optional[datetime], Optional[Dict[str, Any]]]] = []

        if not requested_features:
            requested_features = [f.name for f in table.features]

        for entity_key in entity_keys:
            for key, value in entity_key.items():
                entity_key_string = f"{key}_{value}"
                break
            redis_key = f"{project}_{entity_key_string}"
            hset_keys = [_mmh3(f"{feature_view}:{k}") for k in requested_features]
            ts_key = f"_ts:{feature_view}"
            hset_keys.append(ts_key)
            values = client.hmget(redis_key, hset_keys)
            res_val = dict(zip(requested_features, [float(value.decode('utf-8')) for value in values[:-1]]))

            res_ts = Timestamp()
            ts_val = values[-1]
            if ts_val:
                res_ts.ParseFromString(ts_val)

            res = {}
            for feature_name, val_bin in res_val.items():
                res[feature_name] = val_bin

            if not res:
                result.append((None, None))
            else:
                timestamp = datetime.fromtimestamp(res_ts.seconds)
                result.append((timestamp, res))
        return result
