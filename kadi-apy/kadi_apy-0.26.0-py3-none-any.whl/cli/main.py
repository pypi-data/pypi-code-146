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

from xmlhelpy import Group
from xmlhelpy import group

from .commands.workflows import workflows
from kadi_apy.globals import CONFIG_PATH
from kadi_apy.version import __version__


class KadiApyGroup(Group):
    """Custom click group to dynamically add commands."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            config_file = configparser.ConfigParser()
            config_file.read(CONFIG_PATH)

            if config_file["global"].getboolean("experimental_features"):
                self.add_command(workflows)
        except:
            pass


@group(version=__version__, cls=KadiApyGroup)
def kadi_apy():
    """The kadi-apy command line interface."""


# pylint: disable=unused-import


from .commands.collections import collections
from .commands.config import config
from .commands.groups import groups
from .commands.miscellaneous import miscellaneous
from .commands.records import records
from .commands.templates import templates
from .commands.users import users
