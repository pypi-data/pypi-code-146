import os
from decouple import Config, RepositoryEnv


def get_current_directory():
    return os.path.abspath(os.curdir)


def get_env_vars():
    current_directory = get_current_directory()
    return Config(RepositoryEnv(f'{current_directory}/.env'))


def add_query_to_url(base_url, queries):
    url = f'{base_url}?'
    for field, value in queries.items():
        url += f'{field}={value}&'
    return url[:-1]
