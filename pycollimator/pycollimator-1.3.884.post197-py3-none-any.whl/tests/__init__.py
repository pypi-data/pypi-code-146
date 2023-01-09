import json
import os
import pathlib
from functools import lru_cache

import pycollimator as collimator


config = None
ENV = None


@lru_cache(maxsize=None)
def setup_auth_token():
    global config
    global ENV

    if ENV is None:
        ENV = os.environ.get("ENV", "dev")
        print("ENV is", ENV)

    if ENV == "local":
        token = None
    elif ENV == "dev":
        path = pathlib.Path(__file__).parent.resolve().parent.resolve()
        token_file_path = os.path.join(path, "secrets", "token.txt")
        with open(token_file_path, "r") as f:
            token = f.read().strip()
    else:
        raise NotImplementedError(f"unspported ENV: {ENV} (should be either local or dev)")

    config_file_path = os.path.join(pathlib.Path(__file__).parent.resolve(), f"config-{ENV}.json")
    with open(config_file_path, "r") as f:
        config = json.loads(f.read())
        api_url = config["api_url"]
    collimator.global_variables.set_auth_token(token=token, api_url=api_url)

    projects = collimator.Api.get_projects()["projects"]
    project_uuid = None
    for p in projects:
        if p["title"] == config["project_title"]:
            project_uuid = p["uuid"]
            break

    if project_uuid is None:
        raise ValueError(f"project with title '{config['project_title']} 'not found")

    collimator.global_variables.set_auth_token(token=token, project_uuid=project_uuid, api_url=api_url)
    return token


@lru_cache(maxsize=None)
def get_model_uuid(name: str) -> str:
    global config
    return config["models"][name]["uuid"]


def get_model_name(short_name: str) -> str:
    fixtures_root = os.environ.get("FIXTURES_ROOT", "")
    with open(f"{fixtures_root}tests/fixtures/{short_name}.json", "r") as f:
        model_data = json.loads(f.read())
        return model_data["name"]


def __setup():
    os.environ["CI"] = "true"
    # collimator.Log.set_level("TRACE")
    setup_auth_token()


__setup()
