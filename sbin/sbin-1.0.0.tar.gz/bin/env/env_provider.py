import abc
from typing import Any, Dict


class EnvProvider(abc.ABC):
    @abc.abstractmethod
    def merge(self, env: Dict[Any, Any]) -> Dict[Any, Any]:
        """
        EnvProvider decides whether they should provide more env variables through the
        env they receive as parameter.

        Use the static ctor from EnvProvider to raise ValueError when something is off in your env

        When adding new providers, edit the EnvProviders.init() method

        :param env: Existing environment
        :return: Combined environment with self data
        """

    @staticmethod
    def must_be_a_dict() -> ValueError:
        return ValueError("must be a dictionary")

    @staticmethod
    def custom_error(msg: str) -> ValueError:
        return ValueError(msg)

    @staticmethod
    def key_error() -> ValueError:
        return ValueError("keys must contain only alphanumerical or underscore chars")

    @staticmethod
    def value_error() -> ValueError:
        return ValueError("values must be a string or number")
