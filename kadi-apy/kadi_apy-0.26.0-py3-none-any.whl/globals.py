# Copyright 2021 Karlsruhe Institute of Technology
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
import re
from enum import Enum
from pathlib import Path

from kadi_apy.lib.exceptions import KadiAPYInputError


CONFIG_PATH = Path.home().joinpath(".kadiconfig")

RESOURCE_TYPES = ["record", "collection", "group", "template"]

RESOURCE_ROLES = {
    "record": ["member", "collaborator", "editor", "admin"],
    "collection": ["member", "collaborator", "editor", "admin"],
    "group": ["member", "editor", "admin"],
    "template": ["member", "editor", "admin"],
}


def get_resource_type(resource_type):
    """Map a resource described via string to a class."""

    from kadi_apy.lib.resources.collections import Collection
    from kadi_apy.lib.resources.groups import Group
    from kadi_apy.lib.resources.records import Record
    from kadi_apy.lib.resources.templates import Template

    if resource_type not in RESOURCE_TYPES:
        raise KadiAPYInputError(f"Resource type '{resource_type}' does not exists.")

    _mapping = {
        "record": Record,
        "collection": Collection,
        "group": Group,
        "template": Template,
    }
    return _mapping[resource_type]


def list_to_tokenlist(input_list, separator=","):
    """Create a tokenlist based on a list."""

    return separator.join(str(v) for v in input_list)


def generate_identifier(identifier):
    """Creates a valid identifier."""

    identifier = re.sub("[^a-z0-9-_ ]+", "", identifier.lower())
    identifier = re.sub("[ ]+", "-", identifier)
    return identifier[:50]


class Verbose(Enum):
    """Class to handle different verbose level for output."""

    ERROR = 30
    WARNING = 20
    INFO = 10
    DEBUG = 0
