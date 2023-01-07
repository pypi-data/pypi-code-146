import configparser
import json
import os
from typing import Final

lib_path = os.path.dirname(os.path.abspath(__file__))
sdk_path = os.path.dirname(lib_path)
project_path = os.path.dirname(sdk_path)
config_path = os.path.join(project_path, "config")


def read_config(file_path: str) -> configparser.ConfigParser():
    config = configparser.ConfigParser()
    with open(file_path) as f:
        config.read_file(f)
    return config


class ConfigObject(object):

    def __init__(self, conf: configparser.ConfigParser()) -> None:
        self._conf = conf

    def get_val(self, *args):
        value = self._conf
        for key in args:
            if isinstance(value, str):
                value = json.loads(value.strip('"').replace("'", '"'))
            value = value[key]
        return value


class Config(object):
    _test = ConfigObject(
        read_config(os.path.join(config_path, "test", "config.ini")))
    _prod = ConfigObject(
        read_config(os.path.join(config_path, "test", "config.ini")))
    _dev = ConfigObject(
        read_config(os.path.join(config_path, "test", "config.ini")))

    @property
    def test(self):
        return self._test

    @property
    def dev(self):
        return self._dev

    @property
    def prod(self):
        return self._prod


config: Final[Config] = Config()
