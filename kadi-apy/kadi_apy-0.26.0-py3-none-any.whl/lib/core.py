# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import configparser
import json
import os
import time
from enum import Enum

import click
import requests
import urllib3

from kadi_apy.cli.lib.miscellaneous import Miscellaneous
from kadi_apy.globals import CONFIG_PATH
from kadi_apy.globals import Verbose
from kadi_apy.lib.exceptions import KadiAPYConfigurationError
from kadi_apy.lib.exceptions import KadiAPYInputError
from kadi_apy.lib.resources.collections import Collection
from kadi_apy.lib.resources.groups import Group
from kadi_apy.lib.resources.records import Record
from kadi_apy.lib.resources.templates import Template
from kadi_apy.lib.resources.users import User
from kadi_apy.lib.search import SearchResource
from kadi_apy.lib.search import SearchUser


def _key_exit(key, instance):
    raise KadiAPYConfigurationError(
        f"Please define the key '{key}' for instance '{instance}' in the config file."
    )


def _read_config(config, value, instance):
    try:
        value_read = config[instance][value]
    except:
        _key_exit(value, instance)
    if not value_read:
        _key_exit(value, instance)
    return value_read


def _read_verify(config, instance):
    try:
        return config[instance].getboolean("verify")
    except ValueError as e:
        raise KadiAPYConfigurationError(
            "Please set either 'True' or 'False' in the config file for the"
            " key 'verify'."
        ) from e


def _read_timeout(config, instance):
    try:
        return config[instance].getint("timeout")
    except ValueError as e:
        raise KadiAPYConfigurationError(
            "Please set an integer in the config file for the key 'timeout'."
        ) from e


def _read_ca_bundle(config, instance):
    ca_bundle = config[instance]["ca_bundle"]
    if not os.path.isfile(ca_bundle):
        raise KadiAPYConfigurationError(
            f"CA bundle file does not exist at '{ca_bundle}'."
        )
    return ca_bundle


class KadiManager:
    r"""Base manager class for the API.

    Manages the host and the personal access token (PAT) to use for all API requests.
    The KadiManager can instantiate new resources (e.g. records) via factory methods.

    :param instance: The name of the instance to use in combination with a config file.
    :type instance: str, optional
    :param host: Name of the host.
    :type host: str, optional
    :param token: Personal access token.
    :type token: str, optional
    :param verify: Whether to verify the SSL/TLS certificate of the host.
    :type verify: bool, optional
    :param timeout: Timeout in seconds for the requests.
    :type timeout: float, optional
    :param verbose: Global verbose level to define the amount of prints.
    :type verbose: optional
    """

    def __init__(
        self,
        instance=None,
        host=None,
        token=None,
        verify=True,
        timeout=60,
        verbose=None,
    ):
        self.instance = instance
        self.host = host
        self.token = token
        self.verify = verify
        self.timeout = timeout
        self._pat_user = None
        self.verbose = verbose
        self._misc = None

        if host is None and token is None:
            if not os.path.isfile(CONFIG_PATH):
                raise KadiAPYConfigurationError(
                    f"Config file does not exist at '{CONFIG_PATH}'.\n"
                    "You can run 'kadi-apy config create' to create the config file at"
                    f" '{CONFIG_PATH}."
                )

            config = configparser.ConfigParser()
            try:
                config.read(CONFIG_PATH)
            except configparser.ParsingError as e:
                raise KadiAPYConfigurationError(
                    f"Error during parsing of config file:\n{e}"
                ) from e

            if self.instance is None:
                try:
                    self.instance = config["global"]["default"]
                except Exception as e:
                    raise KadiAPYConfigurationError(
                        "No default instance defined in the config file at"
                        f" '{CONFIG_PATH}."
                    ) from e

            instances = config.sections()
            instances.remove("global")

            if self.instance not in instances:
                raise KadiAPYConfigurationError(
                    "Please use an instance which is defined in the config file.\n"
                    f"Choose one of {instances}"
                )

            self.token = _read_config(config, "pat", self.instance)
            self.host = _read_config(config, "host", self.instance)

            if "verify" in config[self.instance]:
                self.verify = _read_verify(config, self.instance)
            elif "verify" in config["global"]:
                self.verify = _read_verify(config, "global")

            if self.verify is True:
                if "ca_bundle" in config[self.instance]:
                    self.verify = _read_ca_bundle(config, self.instance)
                elif "ca_bundle" in config["global"]:
                    self.verify = _read_ca_bundle(config, "global")

            if "timeout" in config[self.instance]:
                self.timeout = _read_timeout(config, self.instance)
            elif "timeout" in config["global"]:
                self.timeout = _read_timeout(config, "global")

        if self.host is None:
            raise KadiAPYConfigurationError("No host information provided.")

        if self.token is None:
            raise KadiAPYConfigurationError("No personal access token (PAT) provided.")

        if self.host.endswith("/"):
            self.host = self.host[:-1]

        if not self.host.endswith("/api"):
            self.host = self.host + "/api"

        if not self.verify:
            requests.packages.urllib3.disable_warnings(
                urllib3.exceptions.InsecureRequestWarning
            )

    @property
    def misc(self):
        """Functions for miscellaneous."""

        if self._misc is None:
            self._misc = Miscellaneous(self)

        return self._misc

    def _make_request(self, endpoint, method=None, headers=None, timeout=1, **kwargs):
        if not endpoint.startswith(self.host):
            endpoint = self.host + endpoint

        # For debugging:
        self.debug(
            "---------------- Request Info -------------------\n"
            f"Request type: {method}\n"
            f"Endpoint: {endpoint}\n"
        )
        try:
            self.debug(f"Kwargs: {json.dumps(kwargs, indent=4)}\n")
        except:
            pass
        self.debug("-------------------------------------------------\n")

        response = getattr(requests, method)(
            endpoint,
            headers={"Authorization": f"Bearer {self.token}"},
            verify=self.verify,
            timeout=self.timeout,
            **kwargs,
        )

        # Check if any rate limit is exceeded and just wait an increasing amount of time
        # before repeating the request.
        if (
            response.status_code == 429
            and "Rate limit exceeded" in response.json()["description"]
        ):
            time.sleep(timeout)
            return self._make_request(
                endpoint, method=method, headers=headers, timeout=timeout + 1, **kwargs
            )

        return response

    def _get(self, endpoint, **kwargs):
        return self._make_request(endpoint, method="get", **kwargs)

    def _post(self, endpoint, **kwargs):
        return self._make_request(endpoint, method="post", **kwargs)

    def _patch(self, endpoint, **kwargs):
        return self._make_request(endpoint, method="patch", **kwargs)

    def _put(self, endpoint, **kwargs):
        return self._make_request(endpoint, method="put", **kwargs)

    def _delete(self, endpoint, **kwargs):
        return self._make_request(endpoint, method="delete", **kwargs)

    def make_request(self, endpoint, method="get", **kwargs):
        r"""Low level functionality to perform a request.

        This function can be used to use endpoints for which no own functions exist yet.

        :param endpoint: Endpoint to use for the request.
        :type endpoint: str
        :param method: Method to use for the request. Defaults to 'get'. Further
            possibilities are 'post', 'patch', 'put' and 'delete'.
        :type method: str, optional
        :param \**kwargs: Additional parameters.
        :raises KadiAPYInputError: If method is invalid.
        """

        if method not in ["get", "post", "patch", "put", "delete"]:
            raise KadiAPYInputError(f"No valid method given ('{method}').")

        return self._make_request(endpoint, method, **kwargs)

    @property
    def pat_user_id(self):
        """Get the user id related to the PAT.

        :return: The user id.
        :rtype: int
        """

        return self.pat_user.id

    @property
    def pat_user(self):
        """Get the user related to the PAT.

        :return: The user.
        :rtype: User
        """

        if self._pat_user is None:
            self._pat_user = self.user(use_pat=True)

        return self._pat_user

    def record(self, **kwargs):
        r"""Init a record.

        :param \**kwargs: Parameter for the initialization.
        :return: The record.
        :rtype: Record
        """

        return Record(manager=self, **kwargs)

    def collection(self, **kwargs):
        r"""Init a collection.

        :param \**kwargs: Parameter for the initialization.
        :return: The collection.
        :rtype: Collection
        """

        return Collection(manager=self, **kwargs)

    def group(self, **kwargs):
        r"""Init a group.

        :param \**kwargs: Parameter for the initialization.
        :return: The group.
        :rtype: Group
        """

        return Group(manager=self, **kwargs)

    def user(self, **kwargs):
        r"""Init a user.

        :param \**kwargs: Parameter for the initialization.
        :return: The user.
        :rtype: User
        """

        return User(manager=self, **kwargs)

    def template(self, **kwargs):
        r"""Init a template.

        :param \**kwargs: Parameter for the initialization.
        :return: The template.
        :rtype: Template
        """

        return Template(manager=self, **kwargs)

    def search_resource(self, **kwargs):
        r"""Init a search for resources.

        :param \**kwargs: Parameter for the initialization.
        :return: The search for resources.
        :rtype: SearchResource
        """

        return SearchResource(manager=self, **kwargs)

    def search_user(self, **kwargs):
        r"""Init a search for users.

        :param \**kwargs: Parameter for the initialization.
        :return: The search for users.
        :rtype: SearchUser
        """

        return SearchUser(manager=self, **kwargs)

    def error(self, text, **kwargs):
        r"""Print text for error level.

        :param text: Text to be printed via :func:`click.echo()`.
        :param \**kwargs: Additional parameters for :func:`click.echo()`.
        :rtype: :func:`echo()`
        """

        self.echo(text, Verbose.ERROR, **kwargs)

    def warning(self, text, **kwargs):
        r"""Print text for warning level.

        :param text: Text to be printed via :func:`click.echo()`.
        :param \**kwargs: Additional parameters for :func:`click.echo()`.
        :rtype: :func:`echo()`
        """

        self.echo(text, Verbose.WARNING, **kwargs)

    def info(self, text, **kwargs):
        r"""Print text for info level.

        :param text: Text to be printed via :func:`click.echo()`.
        :param \**kwargs: Additional parameters for :func:`click.echo()`.
        :rtype: :func:`echo()`
        """

        self.echo(text, Verbose.INFO, **kwargs)

    def debug(self, text, **kwargs):
        r"""Print text for debug level.

        :param text: Text to be printed via :func:`click.echo()`.
        :param \**kwargs: Additional parameters for :func:`click.echo()`.
        :rtype: :func:`echo()`
        """

        self.echo(text, Verbose.DEBUG, **kwargs)

    def echo(self, text, verbose_level, **kwargs):
        r"""Print text via :func:`click.echo()` if global verbose level is reached.

        :param text: Text to be printed via :func:`click.echo()`.
        :type text: str
        :param verbose_level: Verbose level.
        :param \**kwargs: Additional parameters for :func:`click.echo()`.
        """

        if self.is_verbose(verbose_level):
            click.echo(text, **kwargs)

    def is_verbose(self, verbose_level=Verbose.INFO):
        """Check the verbose level.

        :param verbose_level: Local verbose level of the function.
        :return: ``True`` if verbose level is reached, ``False`` otherwise.
        :rtype: bool
        """

        if isinstance(verbose_level, Enum):
            value_verbose_level_local = verbose_level.value
        else:
            value_verbose_level_local = verbose_level

        if isinstance(self.verbose, Enum):
            value_verbose_level_global = self.verbose.value
        else:
            value_verbose_level_global = self.verbose

        if (
            self.verbose is None
            or value_verbose_level_global > value_verbose_level_local
        ):
            return False

        return True
