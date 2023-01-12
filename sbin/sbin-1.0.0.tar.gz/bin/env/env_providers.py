from typing import Any, Dict, List

from bin.env.ejson_env_provider import EjsonEnvProvider
from bin.env.env_provider import EnvProvider


class EnvProviders(EnvProvider):
    def __init__(self, providers: List[EnvProvider]) -> None:
        self.__providers = providers

    @classmethod
    def init(cls) -> "EnvProviders":
        return cls([EjsonEnvProvider()])

    def merge(self, env: Dict[Any, Any]) -> Dict[Any, Any]:
        new_env = env.copy()
        for provider in self.__providers:
            new_env = provider.merge(new_env)

        return new_env
