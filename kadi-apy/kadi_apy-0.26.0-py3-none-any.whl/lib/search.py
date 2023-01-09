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
from kadi_apy.globals import get_resource_type
from kadi_apy.lib.helper import RequestMixin
from kadi_apy.lib.helper import VerboseMixin


class SearchResource(RequestMixin, VerboseMixin):
    """Search class for resources.

    :param manager: Manager to use for all API requests.
    :type manager: KadiManager
    """

    def search_items(self, item, **params):
        r"""Search for items.

        :param item: The resource type defined either as string or class.
        :param \**params: Additional parameters.
        :return: The response object.
        """

        if isinstance(item, str):
            item = get_resource_type(item)

        return self._get(endpoint=item.base_path, params=params)

    def search_items_user(self, item, user, **params):
        r"""Search for items of users.

        :param item: The resource type defined either as string or class.
        :param user: ID of the user whose items are to be searched for.
        :param \**params: Additional parameters.
        :return: The response object.
        """

        if isinstance(item, str):
            item = get_resource_type(item)

        endpoint = f"/users/{user}{item.base_path}"
        return self._get(endpoint=endpoint, params=params)


class SearchUser(RequestMixin, VerboseMixin):
    """Search class for users.

    :param manager: Manager to use for all API requests.
    :type manager: KadiManager
    """

    def search_users(self, **params):
        r"""Search for users.

        :param \**params: Additional parameters.
        :return: The response object.
        """

        return self._get(endpoint="/users", params=params)
