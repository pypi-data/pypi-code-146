import json
import subprocess
from typing import Any, Dict, List, Optional

from bin.env.env_provider import EnvProvider


class EjsonEnvProvider(EnvProvider):
    __EJSON_KEY = "ejson"
    __EJSON_ENV_KEY = "env"

    def __init__(self, cmd_args: Optional[List[str]] = None) -> None:
        self.__cmd_args = cmd_args or ["ejson", "decrypt"]

    def merge(self, env: Dict[Any, Any]) -> Dict[Any, Any]:
        ejson_path = env.pop(self.__EJSON_KEY, None)
        if ejson_path is None:
            return env

        if not isinstance(ejson_path, str):
            raise EnvProvider.custom_error("ejson path must be a string")

        result = subprocess.run(self.__cmd_args + [str(ejson_path)], capture_output=True)
        if result.returncode != 0:
            raise EnvProvider.custom_error("ejson decryption failed")

        ejson_env = self.__load_json(result.stdout).get(self.__EJSON_ENV_KEY)
        if ejson_env is None:
            raise EnvProvider.custom_error("ejson file is missing the environment dict")

        return {**self.__fix_public_var_format(ejson_env), **env}

    def __load_json(self, data: bytes) -> Dict[Any, Any]:
        try:
            return json.loads(data)  # type: ignore
        except Exception:
            raise EnvProvider.custom_error("ejson parsing failed")

    def __fix_public_var_format(self, data: Dict[Any, Any]) -> Dict[Any, Any]:
        result = {}
        for key, value in data.items():
            fixed_key = key[1:] if key.startswith("_") else key
            result[fixed_key] = value

        return result
