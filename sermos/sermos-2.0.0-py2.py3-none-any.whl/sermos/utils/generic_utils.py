""" Generic utilities w/ no non standard dependencies.
"""
import os
from typing import Union
from sermos.constants import USING_SERMOS_CLOUD, LOCAL_DEPLOYMENT_VALUE


def get_access_key(access_key: Union[str, None] = None,
                   env_var_name: str = 'SERMOS_ACCESS_KEY'):
    """ Simple helper to get admin server access key in a standard fashion. If
    one is provided, return it back. If not, look in environment for
    `env_var_name`. If that doesn't exist, raise useful error.

    If this is a local deployment, no access key is required/relevant,
    so simply return 'local'
    """
    if access_key is not None:
        return access_key

    if not USING_SERMOS_CLOUD:
        return LOCAL_DEPLOYMENT_VALUE  # e.g. 'local'

    try:
        return os.environ[env_var_name]
    except KeyError:
        raise KeyError(
            f"{env_var_name} not found in this environment. Find a valid "
            "access key in your Sermos Cloud administration console.")


# TODO cast to UUID?
def get_deployment_id(deployment_id: Union[str, None] = None,
                      env_var_name: str = 'SERMOS_DEPLOYMENT_ID'):
    """ Simple helper to get the deployment id in a standard fashion. Look in
    the environment for `env_var_name`. If that doesn't exist, raise useful
    error.

    If this is a local deployment, no deployment id is required/relevant,
    so this will simply return 'local' in the event the DEFAULT_BASE_URL is
    set to the LOCAL_DEPLOYMENT_VALUE ('local' by default) in the environment.
    """
    if deployment_id is not None:
        return deployment_id

    if not USING_SERMOS_CLOUD:
        return LOCAL_DEPLOYMENT_VALUE  # e.g. 'local'

    try:
        return os.environ[env_var_name]
    except KeyError:
        raise KeyError(
            f"{env_var_name} not found in this environment. Note: this is "
            "required when running a Celery worker as `beat`. Find this ID "
            "in your administration console. For local development, this can "
            "be any arbitrary string.")
