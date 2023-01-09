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
from kadi_apy.cli.commons import RaiseRequestErrorMixin
from kadi_apy.cli.lib.collections import CLICollection
from kadi_apy.cli.lib.groups import CLIGroup
from kadi_apy.cli.lib.miscellaneous import CLIMiscellaneous
from kadi_apy.cli.lib.records import CLIRecord
from kadi_apy.cli.lib.templates import CLITemplate
from kadi_apy.cli.lib.users import CLIUser
from kadi_apy.cli.search import CLISearchResource
from kadi_apy.cli.search import CLISearchUser
from kadi_apy.globals import Verbose
from kadi_apy.lib.core import KadiManager
from kadi_apy.lib.resources.collections import Collection
from kadi_apy.lib.resources.groups import Group
from kadi_apy.lib.resources.records import Record
from kadi_apy.lib.resources.templates import Template
from kadi_apy.lib.resources.users import User
from kadi_apy.lib.search import SearchResource
from kadi_apy.lib.search import SearchUser


class CLIKadiManager(KadiManager, RaiseRequestErrorMixin):
    """Kadi Manager for the command line interface (CLI).

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

    def __init__(self, verbose=Verbose.INFO, **kwargs):
        super().__init__(verbose=verbose, **kwargs)

        self._misc = None

    @property
    def misc(self):
        if self._misc is None:
            self._misc = CLIMiscellaneous(self)

        return self._misc

    def record(self, use_base_resource=False, **kwargs):
        """Init a record to be used in a CLI.

        :param use_base_resource: Flag indicating if the base resource should be used.
        :type use_base_resource: bool
        :return: The record of class Record or CLIRecord.
        :rtype: Record, CLIRecord
        """
        # pylint: disable=arguments-differ
        if use_base_resource:
            return Record(manager=self, **kwargs)

        return CLIRecord(manager=self, **kwargs)

    def collection(self, use_base_resource=False, **kwargs):
        """Init a collection to be used in a CLI.

        :param use_base_resource: Flag indicating if the base resource should be used.
        :type use_base_resource: bool
        :return: The collection of class Collection or CLICollection.
        :rtype: Collection, CLICollection
        """
        # pylint: disable=arguments-differ
        if use_base_resource:
            return Collection(manager=self, **kwargs)

        return CLICollection(manager=self, **kwargs)

    def group(self, use_base_resource=False, **kwargs):
        """Init a group to be used in a CLI.

        :param use_base_resource: Flag indicating if the base resource should be used.
        :type use_base_resource: bool
        :return: The group of class Group or CLIGroup.
        :rtype: Group, CLIGroup
        """
        # pylint: disable=arguments-differ
        if use_base_resource:
            return Group(manager=self, **kwargs)

        return CLIGroup(manager=self, **kwargs)

    def user(self, use_base_resource=False, **kwargs):
        """Init a user to be used in a CLI.

        :param use_base_resource: Flag indicating if the base resource should be used.
        :type use_base_resource: bool
        :return: The user of class User or CLIUser.
        :rtype: User, CLIUser
        """
        # pylint: disable=arguments-differ
        if use_base_resource:
            return User(manager=self, **kwargs)

        return CLIUser(manager=self, **kwargs)

    def template(self, use_base_resource=False, **kwargs):
        """Init a template to be used in a CLI.

        :param use_base_resource: Flag indicating if the base resource should be used.
        :type use_base_resource: bool
        :return: The template of class Template or CLITemplate.
        :rtype: Template, CLITemplate
        """
        # pylint: disable=arguments-differ
        if use_base_resource:
            return Template(manager=self, **kwargs)

        return CLITemplate(manager=self, **kwargs)

    def search_resource(self, use_base_resource=False, **kwargs):
        """Init a search to be used for resources in a CLI.

        :param use_base_resource: Flag indicating if the base resource should be used.
        :type use_base_resource: bool
        :return: The group of class SearchResource or CLISearchResource.
        :rtype: SearchResource or CLISearchResource
        """
        # pylint: disable=arguments-differ
        if use_base_resource:
            return SearchResource(manager=self, **kwargs)

        return CLISearchResource(manager=self, **kwargs)

    def search_user(self, use_base_resource=False, **kwargs):
        """Init a search to be used for users in a CLI.

        :param use_base_resource: Flag indicating if the base resource should be used.
        :type use_base_resource: bool
        :return: The group of class SearchUser or CLISearchUser.
        :rtype: SearchUser, CLISearchUser
        """
        # pylint: disable=arguments-differ
        if use_base_resource:
            return SearchUser(manager=self, **kwargs)

        return CLISearchUser(manager=self, **kwargs)
