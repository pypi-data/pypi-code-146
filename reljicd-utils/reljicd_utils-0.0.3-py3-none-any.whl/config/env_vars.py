import configparser
import os

from str2bool import str2bool

config_file_path = os.getenv('CONFIG_FILE')
if config_file_path:
    config = configparser.ConfigParser()
    config.read(config_file_path)
else:
    config = None


def get_env(key: str, default: str) -> str:
    """ Returns default even if env var is empty string """
    env = os.getenv(key)
    if env:
        return env

    if config and key in config['DEFAULT'] and config['DEFAULT'][key]:
        return config['DEFAULT'][key]

    return default


POSTGRES_HOST: str = get_env(key='POSTGRES_HOST', default='localhost')
POSTGRES_PORT: int = int(get_env(key='POSTGRES_PORT', default='5432'))
POSTGRES_DB: str = get_env(key='POSTGRES_DB', default='al_data')
POSTGRES_USER: str = get_env(key='POSTGRES_USER', default='postgres')
POSTGRES_PASSWORD: str = get_env(key='POSTGRES_PASSWORD', default='postgres')

LOGGING_LEVEL: str = get_env(key='LOGGING_LEVEL', default='info')

DEBUG: bool = str2bool(get_env(key='DEBUG', default='False'))
