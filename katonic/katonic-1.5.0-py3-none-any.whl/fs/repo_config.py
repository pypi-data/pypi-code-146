#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from pydantic import BaseModel
from pydantic.types import StrictStr, StrictInt
from pydantic.class_validators import root_validator, validator
from pydantic.error_wrappers import ErrorWrapper, ValidationError

from katonic.fs.importer import get_class_from_type


ONLINE_STORE_CLASS_FOR_TYPE = {
    "sqlite": "katonic.fs.core.online_stores.sqlite.SqliteOnlineStore",
    "redis": "katonic.fs.core.online_stores.redis.RedisOnlineStore",
}

OFFLINE_STORE_CLASS_FOR_TYPE = {
    "file": "katonic.fs.core.offline_stores.file_store.FileOfflineStore",
    "postgres": "katonic.fs.core.offline_stores.postgres_store.PostgreSQLOfflineStore",
}


class KFSBaseModel(BaseModel):
    """ Kfs Pydantic Configuration Class """

    class Config:
        arbitrary_types_allowed = True
        extra = "allow"


class KfsConfigBaseModel(BaseModel):
    """ KFS Pydantic Configuration Class """

    class Config:
        arbitrary_types_allowed = True
        extra = "forbid"


class RegistryConfig(KFSBaseModel):
    """ Metadata Store Configuration. Configuration that relates to reading from and writing to the KFS registry."""

    registry_store_type: Optional[StrictStr] = 'postgres'
    """ str: Provider name or a class name that implements RegistryStore. """

    path: Optional[StrictStr]
    """ str: Path to metadata store. Can be a local path, or remote object storage path, e.g. a GCS URI """

    host: Optional[StrictStr]
    """ str: Host of metadata store. Can be a local host, or remote storage host """

    port: Optional[StrictInt]
    """ str: Port of metadata store. Can be a local port, or remote storage port """

    db: Optional[StrictStr]
    """ str: Database Name of metadata store. Can be a local database name, or remote storage database name """

    user: Optional[StrictStr]
    """ str: Database User of metadata store. Can be a local database user name, or remote storage database user name """

    password: Optional[StrictStr]
    """ str: Password of metadata store. Can be a local password for your database, or remote storage password """

    db_schema: Optional[StrictStr] = "public"
    """ str: Database schema of metadata store. Can be a specific  database Schema, or 'public' """


class RepoConfig(KFSBaseModel):
    """ Repo config. Typically loaded from `feature_store.yaml` """

    registry: Any
    """ str: Path to metadata store. Can be a local path, or remote object storage path, e.g. a GCS URI """

    project: StrictStr
    """ str: KFS project id. This can be any alphanumeric string up to 16 characters.
        You can have multiple independent feature repositories deployed to the same cloud
        provider account, as long as they have different project ids.
    """

    description: Optional[StrictStr]
    """ str: User name. """

    user_name: StrictStr
    """ str: User name. """

    # provider: StrictStr
    """ str: local or gcp or aws """

    online_store: Any
    """ OnlineStoreConfig: Online store configuration (optional depending on provider) """

    offline_store: Any
    """ OfflineStoreConfig: Offline store configuration (optional depending on provider) """

    repo_path: Optional[Path] = None

    def __init__(self, **data: Any):
        super().__init__(**data)

        if isinstance(self.online_store, Dict):
            self.online_store = get_online_config_from_type(self.online_store["type"])(
                **self.online_store
            )
        elif isinstance(self.online_store, str):
            self.online_store = get_online_config_from_type(self.online_store)()

        if isinstance(self.offline_store, Dict):
            self.offline_store = get_offline_config_from_type(
                self.offline_store["type"]
            )(**self.offline_store)
        elif isinstance(self.offline_store, str):
            self.offline_store = get_offline_config_from_type(self.offline_store)()

    def get_registry_config(self):
        return RegistryConfig(
            # registry_store_type=self.provider,
            host=self.registry["host"],
            port=self.registry["port"],
            db=self.registry["db_name"],
            user=self.registry["user"],
            password=self.registry["password"],
            db_schema=self.registry["db_schema"],
        )

    @root_validator(pre=True)
    def _validate_online_store_config(cls, values):

        # Set empty online_store config if it isn't set explicitly
        if "online_store" not in values:
            values["online_store"] = {}

        # Skip if we aren't creating the configuration from a dict
        if not isinstance(values["online_store"], Dict):
            return values

        # Make sure that the provider configuration is set. We need it to set the defaults
        # assert "provider" in values

        # Set the default type
        # This is only direct reference to a provider or online store that we should have
        # for backwards compatibility.
        if "type" not in values["online_store"]:
            # if values["provider"] == "local":
            #     values["online_store"]["type"] = "sqlite"
            # elif values["provider"] == "postgres":
            values["online_store"]["type"] = "redis"

        online_store_type = values["online_store"]["type"]

        # Validate the dict to ensure one of the union types match
        try:
            online_config_class = get_online_config_from_type(online_store_type)
            online_config_class(**values["online_store"])
        except ValidationError as e:
            raise ValidationError(
                [ErrorWrapper(e, loc="online_store")], model=RepoConfig,
            ) from e

        return values

    @root_validator(pre=True)
    def _validate_offline_store_config(cls, values):
        # Set empty offline_store config if it isn't set explicitly
        if "offline_store" not in values:
            values["offline_store"] = {}

        # Skip if we aren't creating the configuration from a dict
        if not isinstance(values["offline_store"], Dict):
            return values

        # Make sure that the provider configuration is set. We need it to set the defaults
        # assert "provider" in values

        # Set the default type
        if "type" not in values["offline_store"]:
            # if values["provider"] == "local":
            #     values["offline_store"]["type"] = "file"
            # elif values["provider"] == "postgres":
            values["offline_store"]["type"] = "postgres"

        offline_store_type = values["offline_store"]["type"]

        # Validate the dict to ensure one of the union types match
        try:
            offline_config_class = get_offline_config_from_type(offline_store_type)
            offline_config_class(**values["offline_store"])
        except ValidationError as e:
            raise ValidationError(
                [ErrorWrapper(e, loc="offline_store")], model=RepoConfig,
            ) from e

        return values

    @validator("project")
    def _validate_project_name(cls, v):
        from katonic.fs.utils import is_valid_name

        if not is_valid_name(v):
            raise ValueError(
                f"Project name, {v}, should only have "
                f"alphanumerical values and underscores but not start with an underscore."
            )
        return v

    def write_to_path(self, repo_path: Path):
        config_path = repo_path / "feature_store.yaml"
        with open(config_path, mode="w") as f:
            yaml.dump(
                yaml.safe_load(
                    self.json(
                        exclude={"repo_path"},
                        exclude_none=True,
                        exclude_unset=True,
                        exclude_defaults=True,
                    )
                ),
                f,
                sort_keys=False,
            )


class KFSConfigError(Exception):
    def __init__(self, error_message, config_path):
        self._error_message = error_message
        self._config_path = config_path
        super().__init__(self._error_message)

    def __str__(self) -> str:
        return f"{self._error_message}\nat {self._config_path}"

    def __repr__(self) -> str:
        return (
            f"KfsConfigError({repr(self._error_message)}, {repr(self._config_path)})"
        )


def get_data_source_class_from_type(data_source_type: str):
    module_name, config_class_name = data_source_type.rsplit(".", 1)
    return get_class_from_type(module_name, config_class_name, "Source")


def get_online_config_from_type(online_store_type: str):
    if online_store_type in ONLINE_STORE_CLASS_FOR_TYPE:
        online_store_type = ONLINE_STORE_CLASS_FOR_TYPE[online_store_type]
    else:
        assert online_store_type.endswith("OnlineStore")
    module_name, online_store_class_type = online_store_type.rsplit(".", 1)
    config_class_name = f"{online_store_class_type}Config"

    return get_class_from_type(module_name, config_class_name, config_class_name)


def get_offline_config_from_type(offline_store_type: str):
    if offline_store_type in OFFLINE_STORE_CLASS_FOR_TYPE:
        offline_store_type = OFFLINE_STORE_CLASS_FOR_TYPE[offline_store_type]
    else:
        assert offline_store_type.endswith("OfflineStore")
    module_name, offline_store_class_type = offline_store_type.rsplit(".", 1)
    config_class_name = f"{offline_store_class_type}Config"

    return get_class_from_type(module_name, config_class_name, config_class_name)


def load_repo_config(config: Dict) -> RepoConfig:
    try:
        return RepoConfig(**config)
    except ValidationError as e:
        raise KFSConfigError(e, config) from e