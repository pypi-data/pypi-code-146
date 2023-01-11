import argparse
import os
from abc import ABC, abstractmethod


EnvPrefix = "METASTORE"


class StoreInterface(ABC):
    @abstractmethod
    def __init__(self, name: str, infos: dict) -> None:
        """Init the store, check the provided keys, and create possible client"""
        pass

    def get_from_config(self, store: str, value: str, infos: dict) -> str:
        if value not in infos and f"{EnvPrefix}_{store}_{value}" not in os.environ:
            raise Exception(f"Config error: '{value}' is required in store '{store}'")
        return infos.get(
            value,
            os.getenv(f"{EnvPrefix}_{store}_{value}"),
        )

    @abstractmethod
    def gen_parser(self, parser: argparse.ArgumentParser) -> None:
        """Generate the parser that reads the arguments and options"""
        pass

    @abstractmethod
    def read_secret(self, secret: str) -> str:
        """Read a secret from the desired password store"""
        pass
