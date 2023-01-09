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
from kadi_apy.lib.resources.users import User


class CLIUser(User, RaiseRequestErrorMixin):
    """User class to be used in a CLI.

    A user can either be clearly identified via its id or the combination of username
    and identity type.

    :param manager: Manager to use for all API requests.
    :type manager: CLIManager
    :param id: The ID of an existing user.
    :type id: int, optional
    :param username: The username.
    :type username: str, optional
    :param identity_type: The identity type of the user.
    :type identity_type: str, optional
    :param use_pat: Flag to indicate that the pat stored in the CLIKadiManager should be
        used for instantiating the user.
    :type use_pat: bool, optional
    """

    def print_info(self):
        """Print user infos using a CLI."""

        # pylint: disable=arguments-differ

        self.info(
            f"Displayname: {self.meta['identity']['displayname']}\n"
            f"ID: {self.id}\n"
            f"Username: {self.meta['identity']['username']}\n"
            f"Identity type: {self.meta['identity']['identity_type']}"
        )
