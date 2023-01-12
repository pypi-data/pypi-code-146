import re
from typing import Any, Callable, Dict, Generator

from bin.env.env_provider import EnvProvider
from bin.env.env_providers import EnvProviders
from bin.env.errors import EnvProvisionError

VALID_KEY_REGEX = re.compile(r"^[A-Za-z_]+[A-Za-z0-9_]*$")


class Env(Dict[str, str]):
    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[Dict[str, Any]], "Env"], None, None]:
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: Dict[str, Any]) -> None:
        pass

    @classmethod
    def validate(cls, data: Dict[str, Any]) -> "Env":
        if not isinstance(data, dict):
            raise EnvProvider.must_be_a_dict()

        valid_env: Dict[str, str] = {}
        for key, value in data.items():
            if any(VALID_KEY_REGEX.match(str(key)) is None for key in data):
                raise EnvProvider.key_error()

            if isinstance(value, dict) or isinstance(value, list):
                raise EnvProvider.value_error()

            valid_env[key] = str(value)

        return cls(valid_env)

    def provide(self) -> Dict[str, str]:
        try:
            provided = EnvProviders.init().merge(self)
            return Env.validate(provided)
        except Exception as e:
            raise EnvProvisionError(str(e))
