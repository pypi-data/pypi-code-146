import os
import subprocess
from . import EnvPrefix, StoreInterface


class Store(StoreInterface):
    def __init__(self, name, infos):
        self.name = name
        # self.url = super().get_from_config(name, "url", infos)
        # self.user = super().get_from_config(name, "user", infos)
        # self.password = super().get_from_config(name, "password", infos)

    def gen_parser(self, parser):
        parser.add_argument("secret")

    def read_secret(self, secret) -> str:
        result = subprocess.run(["rbw", "get", secret], capture_output=True)
        if result.returncode != 0:
            stderr = result.stderr.strip().decode("utf-8")
            raise Exception(f"bitwarden store: rbw error during execution: {stderr}")
        return result.stdout.strip().decode("utf-8")
