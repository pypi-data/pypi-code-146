import base64
import json
import logging
import os
from typing import Any, List, Optional

import boto3
from dynaconf import Dynaconf

log = logging.getLogger(__name__)


class LazyConfig:
    def __init__(self, settings: Dynaconf = None):
        self._settings = settings

    def __getattr__(self, item) -> Any:
        return self.get(item)

    def __getitem__(self, item):
        return self.get(item)

    @property
    def settings(self) -> Dynaconf:
        if not self._settings:
            self.load()
        return self._settings

    @property
    def env_name(self) -> Optional[str]:
        return self.get("ENV_FOR_DYNACONF")

    def get(self, key: str, default=None) -> Any:
        return self.settings.get(key) or os.getenv(key) or default

    def set(self, key: str, value: Any):
        if not self._settings:
            raise Exception("Config not loaded")
        self._settings.set(key, value)

    def update(self, **kwargs):
        if not self._settings:
            raise Exception("Config not loaded")
        self._settings.update(**kwargs)

    def load(self, extra_files: List[str] = None):
        log.info("Loading configurations...")
        if not extra_files:
            extra_files = []
        settings_files = ["settings.toml", "local.toml", "secrets.toml"] + extra_files
        self._settings = Dynaconf(environments=True, settings_files=settings_files)

    def load_from_secrets_manager(self, secret_id: Optional[str]) -> dict:
        if not secret_id:
            log.info("No secret_id provided")
            return {}
        client = boto3.client(service_name="secretsmanager")
        response = client.get_secret_value(SecretId=secret_id)
        if "SecretString" in response:
            secrets_string = response["SecretString"]
        else:
            secrets_string = base64.b64decode(response["SecretBinary"])
        secrets_dict = json.loads(secrets_string) or {}
        self.update(**secrets_dict)  # type: ignore
        log.info("Secrets loaded successfully")
        return secrets_dict

    def load_ssm_parameters(self, names: List[str]):
        ssm_client = boto3.client("ssm")
        response = ssm_client.get_parameters(Names=names, WithDecryption=True)
        for param in response["Parameters"]:
            name, value = param["Name"], param["Value"]
            self.set(name, value)
        for param in response["InvalidParameters"]:
            log.warning(f"Invalid parameter: {param}")
