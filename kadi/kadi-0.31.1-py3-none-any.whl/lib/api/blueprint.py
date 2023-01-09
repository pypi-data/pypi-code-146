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
import os

from flask import Blueprint

import kadi.lib.constants as const
from kadi.lib.utils import as_list


class APIBlueprint(Blueprint):
    """Custom Flask blueprint with support for API versioning."""

    def route(self, rule, **options):
        r"""Decorator to register a view function for a given URL rule.

        Adds a new option ``v`` to Flask's ``route`` decorator, allowing to set an API
        endpoint for one or multiple specific API versions.

        **Example:**

        .. code-block:: python3

            @blueprint.route("/records", v=["v1", "v2"])
            def get_records():
                pass

        The specified API versions all have to be valid, i.e. they have to be part of
        the available API versions defined in :const:`kadi.lib.constants.API_VERSIONS`.
        If no versions are given, the endpoint defaults to all available versions. In
        any case, the normal endpoint without any version will be created as well,
        pointing to the same function as the endpoint with the latest version.

        For example, the above code would lead to the following endpoints and URLs
        (assuming an URL prefix of ``"/api"``), where the last two endpoints would point
        to the same function:

        * ``"api.get_records_v1"`` -> ``"/api/v1/records"``
        * ``"api.get_records_v2"`` -> ``"/api/v2/records"``
        * ``"api.get_records"`` -> ``"/api/records"``

        Alternatively, the version can be set to ``None`` explicitly, in which case this
        decorator will behave like the standard ``route`` decorator, i.e. no versioning
        will be used at all. This is especially useful for internal endpoints where
        versioning is unnecessary.

        The version is also used when generating the API documentation.

        :param rule: The URL rule as string.
        :param endpoint: (optional) The endpoint for the registered URL rule. Defaults
            to the name of the function with the version appended, if present.
        :param v: (optional) A string or list of strings specifying the supported API
            versions.
        :param \**options: Additional options to be forwarded to the underlying rule
            system of Flask.
        """

        def decorator(func):
            endpoint = options.pop("endpoint", func.__name__)
            versions = as_list(options.pop("v", const.API_VERSIONS))

            apidoc_meta = []

            if versions is None:
                self.add_url_rule(rule, endpoint, func, **options)
            else:
                for version in versions:
                    if version not in const.API_VERSIONS:
                        continue

                    apidoc_meta.append(version)

                    self.add_url_rule(
                        f"{version}{rule}", f"{endpoint}_{version}", func, **options
                    )

                    if version == const.API_VERSIONS[-1]:
                        self.add_url_rule(rule, endpoint, func, **options)

            if hasattr(func, "_apidoc"):
                func._apidoc["versions"] = apidoc_meta
            else:
                func._apidoc = {"versions": apidoc_meta}

            return func

        return decorator

    def _check_setup_finished(self, *args):
        # This environment variable check can be used as a workaround to disable the
        # checks regarding the route setup order of this blueprint in certain cases.
        if os.environ.get(const.VAR_API_BP) != "1":
            super()._check_setup_finished(*args)


bp = APIBlueprint("api", __name__, url_prefix="/api")


# pylint: disable=unused-import


import kadi.modules.accounts.api
import kadi.modules.collections.api
import kadi.modules.groups.api
import kadi.modules.main.api
import kadi.modules.notifications.api
import kadi.modules.records.api
import kadi.modules.settings.api
import kadi.modules.sysadmin.api
import kadi.modules.templates.api
