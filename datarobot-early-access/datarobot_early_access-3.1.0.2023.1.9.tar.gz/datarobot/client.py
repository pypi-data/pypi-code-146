#
# Copyright 2021-2022 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from contextlib import contextmanager
import contextvars
import logging
import os
import re
from typing import Optional, Tuple, TYPE_CHECKING, Union
import warnings

from urllib3 import Retry
import yaml

from ._version import __expected_server_version__, __version__
from .errors import ClientError
from .rest import DataRobotClientConfig, RESTClientObject

if TYPE_CHECKING:
    from requests import Response

logger = logging.getLogger(__package__)
VERSION_RE = re.compile(r"^(\d+)\.(\d+).*")

__all__ = ("Client", "get_client", "set_client", "client_configuration")

_global_client: Optional[RESTClientObject] = None
_context_client: contextvars.ContextVar[RESTClientObject] = contextvars.ContextVar("dr_rest_client")


def _create_client(
    token: Optional[str] = None,
    endpoint: Optional[str] = None,
    config_path: Optional[str] = None,
    connect_timeout: Optional[int] = None,
    user_agent_suffix: Optional[str] = None,
    ssl_verify: bool = True,
    max_retries: Optional[Union[int, Retry]] = None,
    token_type: str = "Token",
) -> RESTClientObject:
    """Return a new `RESTClientObject` with optional configuration.
    Missing configuration will be read from environment variables or a config
    file.

    .. note::
        This function is intended for use with the ``client_configuration``
        context manager only. Use of the global context will eventually
        be deprecated.

    Parameters
    ----------
    token : str, optional
        API token
    endpoint : str, optional
        Base url of API
    config_path : str, optional
        Alternate location of config file
    connect_timeout : int, optional
        How long the client should be willing to wait before establishing a connection with
        the server
    user_agent_suffix : str, optional
        Additional text that is appended to the User-Agent HTTP header when communicating with
        the DataRobot REST API. This can be useful for identifying different applications that
        are built on top of the DataRobot Python Client, which can aid debugging and help track
        usage.
    ssl_verify : bool or str, optional
        Whether to check SSL certificate.
        Could be set to path with certificates of trusted certification authorities
    max_retries : int or datarobot.rest.Retry, optional
        Either an integer number of times to retry connection errors,
        or a `urllib3.util.retry.Retry` object to configure retries.
    token_type: str, "Token" by default
        Authentication token type: Token, Bearer.
        "Bearer" is for DataRobot OAuth2 token, "Token" for token generated in Developer Tools
    """
    env_config = _get_config_file_from_env()
    if token and endpoint:
        drconfig = DataRobotClientConfig(
            endpoint=endpoint,
            token=token,
            connect_timeout=connect_timeout,
            user_agent_suffix=user_agent_suffix,
            ssl_verify=ssl_verify,
            max_retries=max_retries,
            token_type=token_type,
        )
    elif config_path:
        if not _file_exists(config_path):
            raise ValueError(f"Invalid config path - no file at {config_path}")
        drconfig = _config_from_file(config_path)
    elif env_config:
        if not _file_exists(env_config):
            raise ValueError(f"Invalid config path - no file at {env_config}")
        drconfig = _config_from_file(env_config)
    else:
        try:
            drconfig = _config_from_env()
        except ValueError:
            default_config_path = _get_default_config_file()
            if default_config_path is not None:
                drconfig = _config_from_file(default_config_path)
            else:
                raise ValueError("No valid configuration found")

    if not drconfig.max_retries:
        drconfig.max_retries = Retry(backoff_factor=0.1, respect_retry_after_header=True)

    client = RESTClientObject.from_config(drconfig)
    if not _is_compatible_client(client):
        raise ValueError("The client is not compatible with the server version")

    return client


def Client(
    token: Optional[str] = None,
    endpoint: Optional[str] = None,
    config_path: Optional[str] = None,
    connect_timeout: Optional[int] = None,
    user_agent_suffix: Optional[str] = None,
    ssl_verify: bool = True,
    max_retries: Optional[Union[int, Retry]] = None,
    token_type: str = "Token",
) -> RESTClientObject:
    """
    Configures the global API client for the Python SDK with optional
    configuration. Missing configuration will be read from env
    or config file.

    Parameters
    ----------
    token : str, optional
        API token
    endpoint : str, optional
        Base url of API
    config_path : str, optional
        Alternate location of config file
    connect_timeout : int, optional
        How long the client should be willing to wait before establishing a connection with
        the server.
    user_agent_suffix : str, optional
        Additional text that is appended to the User-Agent HTTP header when communicating with
        the DataRobot REST API. This can be useful for identifying different applications that
        are built on top of the DataRobot Python Client, which can aid debugging and help track
        usage.
    ssl_verify : bool or str, optional
        Whether to check SSL certificate.
        Could be set to path with certificates of trusted certification authorities.
    max_retries : int or datarobot.rest.Retry, optional
        Either an integer number of times to retry connection errors,
        or a `urllib3.util.retry.Retry` object to configure retries.
    token_type: str, "Token" by default
        Authentication token type: Token, Bearer.
        "Bearer" is for DataRobot OAuth2 token, "Token" for token generated in Developer Tools.

    Returns
    -------
        The ``RESTClientObject`` instance created.
    """
    new_client = _create_client(
        token,
        endpoint,
        config_path,
        connect_timeout,
        user_agent_suffix,
        ssl_verify,
        max_retries,
        token_type,
    )

    set_client(new_client)

    return new_client


def _is_compatible_client(client: RESTClientObject) -> bool:
    """
    Check that this client version is not ahead of the DataRobot version that
    the server points to. There will be unsupported functionality

    Parameters
    ----------
    client : RESTClientObject

    Returns
    -------
    bool : True if client is compatible with server, False otherwise.
    """
    try:
        server_response = client.get("version/")
    except ClientError as cerr:
        if cerr.status_code == 401:
            w_msg_tmpl = (
                'Unable to authenticate to the server - are you sure the provided token of "{}" '
                'and endpoint of "{}" are correct? '.format(client.token, client.endpoint)
            )
        else:
            w_msg_tmpl = (
                "Error retrieving a version string from the server. "
                "Server did not reply with an API version. This may indicate the "
                "endpoint parameter `{}` is incorrect, or that the server there is "
                "incompatible with this version of the DataRobot client package. "
            )
        w_msg_tmpl += (
            "Note that if you access the DataRobot webapp at "
            "`https://app.datarobot.com`, then the correct endpoint to specify would "
            "be `https://app.datarobot.com/api/v2`."
        )
        warnings.warn(w_msg_tmpl.format(client.endpoint))
        return False

    if not _is_compatible_version(server_response):
        return False

    _ensure_protocol_match(client, server_response)
    return True


# TODO: consider replacing this function with `packaging` library once we'll need to have a more
# complicated version checking
def _get_major_minor_version(version_string: str) -> Tuple[int, int]:
    """
    Parse DataRobot version string and return major and minor numbers.

    Parameters
    ----------
    version_string : str
        The version string returned by client or server.

    Returns
    -------
    Tuple[int, int]
    """
    major, minor = VERSION_RE.match(version_string).groups()
    return int(major), int(minor)


def _is_compatible_version(version_response: Response) -> bool:
    """
    Ensure that server and client are compatible.

    Parameters
    ----------
    version_response : request.Response
        client.get('version/') response object

    Returns
    -------
    bool : True if client and server versions are compatible, False otherwise
    """
    response_json = version_response.json()
    server_version_string = response_json["versionString"]
    if server_version_string is None:
        warn_msg = (
            "Server did not respond with a version string, you may have incompatibilities. "
            "Please check that your versions of the DataRobot application and this package "
            "are compatible"
        )
        warnings.warn(warn_msg)
        return True
    expected_server_version_string = _get_expected_server_version()
    server_major, server_minor = _get_major_minor_version(server_version_string)
    expected_major, expected_minor = _get_major_minor_version(expected_server_version_string)
    if server_major > expected_major:
        err_msg = (
            f"Client and server versions incompatible. Expected server version: {expected_server_version_string} - "
            f"Actual server version: {server_version_string}"
        )
        warnings.warn(err_msg)
        return False
    if server_major < expected_major or server_minor < expected_minor:
        warn_msg = (
            "Client version is ahead of server version, you may have incompatibilities. "
            f"Expected server version: {expected_server_version_string} - "
            f"Actual server version: {server_version_string}"
        )
        warnings.warn(warn_msg)
    return True


def _ensure_protocol_match(client: RESTClientObject, server_response: Response) -> None:
    """
    Check if server responded using the same protocol as the client endpoint configuration.
    If protocol mismatch detected - the client endpoint will be updated to https version.

    Parameters
    ----------
    client : RESTClientObject
        datarobot client instance
    server_response : request.Response
        response from 'version/' endpoint.
    """
    # Do not proceed if there was no redirect
    if not server_response.history:
        return
    # check the redirect location, if it is the https version - update client endpoint.
    location = server_response.history[0].headers["Location"]
    expected_location = client._join_endpoint("version/").replace("http://", "https://")
    if location == expected_location:
        warn_msg = (
            "Client endpoint is configured for HTTP protocol; "
            "however the server users HTTPS. HTTPS will be used."
        )
        warnings.warn(warn_msg)
        if not client.endpoint:
            raise ValueError("Client endpoint is not set and is required.")
        client.endpoint = client.endpoint.replace("http://", "https://")


def _get_expected_server_version() -> str:
    return __expected_server_version__


def _get_client_version() -> str:
    return __version__


def get_client() -> RESTClientObject:
    return _context_client.get(_global_client) or Client()


class staticproperty(property):
    def __get__(self, instance, owner):
        return self.fget()


def set_client(client: RESTClientObject) -> Optional[RESTClientObject]:
    """
    Configure the global HTTP client for the Python SDK.
    Returns previous instance.
    """
    global _global_client  # pylint: disable=W0603
    previous = _context_client.get(_global_client)
    _context_client.set(client)
    # addressing issue for ipykernel < 6.0
    # https://github.com/ipython/ipython/issues/11565
    # fall back to _global_client
    _global_client = client
    return previous


def _get_config_file_from_env() -> Optional[str]:
    if "DATAROBOT_CONFIG_FILE" in os.environ:
        config_path = os.environ["DATAROBOT_CONFIG_FILE"]
        if os.path.exists(config_path):
            return config_path
        else:
            raise ValueError("Environment variable DATAROBOT_CONFIG_FILE points to a missing file")
    return None


def _get_config_dir() -> str:
    return os.path.expanduser("~/.config/datarobot")


def _get_default_config_file() -> Optional[str]:
    first_choice_config_path = os.path.join(_get_config_dir(), "drconfig.yaml")
    if _file_exists(first_choice_config_path):
        return first_choice_config_path
    else:
        return None


_file_exists = os.path.isfile


def _config_from_env() -> DataRobotClientConfig:
    """
    Create and return a DataRobotClientConfig from environment variables.

    There are two ways this can be used:
    1. Use the environment variable DATAROBOT_CONFIG_FILE to specify the path to a yaml config
       file specifying the configuration to use
    2. Use both the environment variables DATAROBOT_ENDPOINT and DATAROBOT_API_TOKEN to specify
       the connection parameters. Note that this method only allows for configuration of endpoint,
       token and user_agent_suffix; any more advanced configuration must be done through a yaml
       file

    Returns
    -------
    config : DataRobotClientConfig

    Raises
    ------
    ValueError
        If either of DATAROBOT_ENDPOINT or DATAROBOT_API_TOKEN is not specified as an environment
        variable
    IOError
        If the config file that DATAROBOT_CONFIG_FILE points to does not exist
    """
    endpoint = os.environ.get("DATAROBOT_ENDPOINT")
    token = os.environ.get("DATAROBOT_API_TOKEN")
    user_agent_suffix = os.environ.get("DATAROBOT_USER_AGENT_SUFFIX")
    max_retries: Optional[Union[str, int]] = os.environ.get("DATAROBOT_MAX_RETRIES")
    if max_retries is not None:
        max_retries = int(max_retries)
    if endpoint is None or token is None:
        e_msg = (
            "Incomplete DataRobot configuration specified in environment variables; both "
            "DATAROBOT_ENDPOINT and DATAROBOT_API_TOKEN must be specified"
        )
        raise ValueError(e_msg)
    return DataRobotClientConfig(
        endpoint=endpoint, token=token, user_agent_suffix=user_agent_suffix, max_retries=max_retries
    )


def _config_from_file(config_path: str) -> DataRobotClientConfig:
    """
    Create and return a DataRobotClientConfig from a config path. The file must be
    a yaml formatted file

    Parameters
    ----------
    config_path : str
        Path to the configuration file

    Returns
    -------
    config : DataRobotClientConfig
    """
    with open(config_path, "rb") as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
    return DataRobotClientConfig.from_data(data)


@contextmanager
def client_configuration(*args, **kwargs):
    """
    This context manager can be used to temporarily change the global HTTP client.

    In multithreaded scenarios, it is highly recommended to use a fresh manager object
    per thread.

    DataRobot does not recommend nesting these contexts.

    Parameters
    ----------
        args : Parameters passed to ``datarobot.client.Client()``
        kwargs : Keyword arguments passed to ``datarobot.Client()``

    Examples
    --------

    .. code-block:: python

        from datarobot.client import client_configuration
        from datarobot.models import Project

        with client_configuration(token="api-key-here", endpoint="https://host-name.com"):
            Project.list()

    .. code-block:: python

        from datarobot.client import Client, client_configuration
        from datarobot.models import Project

        Client()  # Interact with DataRobot using the default configuration.
        Project.list()

        with client_configuration(config_path="/path/to/a/drconfig.yaml"):
            # Interact with DataRobot using a different configuration.
            Project.list()
    """

    contextvars_token: contextvars.Token[RESTClientObject] = None
    try:
        client = _create_client(*args, **kwargs)
        contextvars_token = _context_client.set(client)
        yield
    finally:
        if contextvars_token is not None:
            _context_client.reset(contextvars_token)
