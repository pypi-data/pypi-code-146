import hvac
import os
from . import EnvPrefix, StoreInterface


class Store(StoreInterface):
    def __init__(self, name, infos):
        self.url = super().get_from_config(name, "url", infos)
        self.token = super().get_from_config(name, "token", infos)
        self.client = hvac.Client(url=self.url, token=self.token)

    def gen_parser(self, parser):
        parser.add_argument("secret")
        parser.add_argument("--key")
        parser.add_argument("--engine")

    def read_secret(self, secret, key="", engine=""):
        read_response = self.client.secrets.kv.read_secret_version(
            path=secret, mount_point=engine
        )

        if key:
            return read_response["data"]["data"][key]
        else:
            return read_response
