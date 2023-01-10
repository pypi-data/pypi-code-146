#!/usr/bin/env python3

# Standard libraries
from typing import List

# Bundle class, pylint: disable=too-few-public-methods
class Bundle:

    # Aliases
    ALIAS: str = 'gcil'

    # Arguments
    ARGUMENT_NETWORKS_ENUM: List[str] = ['bridge', 'host', 'none']
    ARGUMENT_SSH_USER_DEFAULT: str = 'root'
    ARGUMENT_TAGS_DEFAULT: List[str] = ['deploy', 'local', 'publish']

    # Names
    NAME: str = 'gitlabci-local'

    # Configurations
    CONFIGURATION: str = '.gitlab-ci.yml'

    # Sources
    REPOSITORY: str = 'https://gitlab.com/AdrianDC/gitlabci-local'

    # Releases
    RELEASE_FIRST_TIMESTAMP: int = 1579337311

    # Environment
    ENV_COMMIT_SHA: str = 'CI_COMMIT_SHA'
    ENV_COMMIT_REF_NAME: str = 'CI_COMMIT_REF_NAME'
    ENV_COMMIT_REF_SLUG: str = 'CI_COMMIT_REF_SLUG'
    ENV_COMMIT_SHORT_SHA1: str = 'CI_COMMIT_SHORT_SHA'
    ENV_ENGINE: str = 'CI_LOCAL_ENGINE'
    ENV_ENGINE_NAME: str = 'CI_LOCAL_ENGINE_NAME'
    ENV_GIT_BINARY_PATH: str = 'GIT_BINARY_PATH'
    ENV_HISTORIES_DURATION_FAKE: str = 'CI_LOCAL_HISTORIES_DURATION_FAKE'
    ENV_HOST: str = 'CI_LOCAL_HOST'
    ENV_LOCAL: str = 'CI_LOCAL'
    ENV_NETWORK: str = 'CI_LOCAL_NETWORK'
    ENV_NO_GIT_SAFETIES: str = 'CI_LOCAL_NO_GIT_SAFETIES'
    ENV_NO_SCRIPT_FAIL: str = 'CI_LOCAL_NO_SCRIPT_FAIL'
    ENV_NOTIFY_BINARY_PATH: str = 'NOTIFY_BINARY_PATH'
    ENV_PODMAN_BINARY_PATH: str = 'PODMAN_BINARY_PATH'
    ENV_PROJECT_NAME: str = 'CI_PROJECT_NAME'
    ENV_PROJECT_NAMESPACE: str = 'CI_PROJECT_NAMESPACE'
    ENV_UPDATES_DAILY: str = 'CI_LOCAL_UPDATES_DAILY'
    ENV_UPDATES_DISABLE: str = 'CI_LOCAL_UPDATES_DISABLE'
    ENV_UPDATES_FAKE: str = 'CI_LOCAL_UPDATES_FAKE'
    ENV_UPDATES_OFFLINE: str = 'CI_LOCAL_UPDATES_OFFLINE'
    ENV_VERSION_FAKE: str = 'CI_LOCAL_VERSION_FAKE'
    ENV_WINPTY: str = 'CI_LOCAL_WINPTY'
    ENV_WINPTY_PATH: str = 'WINPTY_BINARY_PATH'
