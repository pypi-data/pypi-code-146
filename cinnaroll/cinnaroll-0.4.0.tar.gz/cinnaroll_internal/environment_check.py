import os
import requests
import toml
from typing import List, Optional

from cli import login
from cinnaroll_internal import constants, utils


API_KEY_ENV_VAR_NAME = "CINNAROLL_API_KEY"
WORKING_DIRECTORY = os.getcwd()

PING_ENDPOINT_URL = constants.BACKEND_BASE_URL + "/modelUpload"


class WrongAPIKeyError(Exception):
    def __init__(
        self, message: str = "API Key is wrong. Has it been pasted correctly?"
    ) -> None:
        super().__init__(message)


class DisallowedWriteError(Exception):
    ...


class CinnarollAPIKeyMissingError(Exception):
    ...


class CinnarollEnvironmentConfigurationError(Exception):
    ...


def find_disallowed_write_error() -> Optional[Exception]:
    if not os.access(WORKING_DIRECTORY, os.W_OK):
        return DisallowedWriteError(
            f"Can’t save files in current working directory ({WORKING_DIRECTORY}). "
            f"Ensure you have write permissions to it."
        )
    return None


def find_api_key_error() -> Optional[Exception]:
    api_key = get_api_key()
    if not api_key:
        return CinnarollAPIKeyMissingError(
            f"Cinnaroll API Key is missing. Use cinnaroll-login to configure the API Key, "
            f"or set {API_KEY_ENV_VAR_NAME} environment variable."
        )
    headers = {
        constants.API_KEY_HEADER_KEY: api_key
    }
    try:
        # todo: discuss endpoint
        response: requests.Response = requests.get(url=PING_ENDPOINT_URL, headers=headers)
        if response.status_code == requests.codes.unauthorized:
            return WrongAPIKeyError()
        return None
    # return WrongAPIKeyError only if we know API Key is wrong (401)
    # if e.g. request times out - we don't know and shouldn't stop user from configuring rollout
    except requests.exceptions.RequestException:
        return None


def get_api_key_from_toml_file_content(credentials_file: str) -> str:
    try:
        api_key: str = toml.loads(credentials_file)["default"]["API Key"]
        return api_key
    except KeyError:
        return ""


def get_api_key() -> str:
    api_key = os.environ.get(API_KEY_ENV_VAR_NAME)
    if api_key:
        return api_key
    try:
        with open(login.CREDENTIALS_FILE_PATH, "r") as credentials_file:
            api_key = get_api_key_from_toml_file_content(credentials_file.read())
            if api_key:
                return api_key
    except FileNotFoundError:
        return ""
    return ""


def find_environment_errors() -> List[Exception]:
    errors: List[Exception] = []
    utils.append_if_not_none(errors, find_disallowed_write_error())
    utils.append_if_not_none(errors, find_api_key_error())
    return errors


def check_environment() -> None:
    errors = find_environment_errors()

    if len(errors):
        print(
            "The following errors were found. Correct them and import the package again.\n"
        )
        for err in errors:
            print(f"{err}\n")
        raise CinnarollEnvironmentConfigurationError
