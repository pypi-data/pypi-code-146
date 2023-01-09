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
from flask_babel import lazy_gettext as _l

from kadi.modules.collections.models import Collection
from kadi.modules.collections.schemas import CollectionSchema
from kadi.modules.groups.models import Group
from kadi.modules.groups.schemas import GroupSchema
from kadi.modules.records.models import Record
from kadi.modules.records.schemas import RecordSchema
from kadi.modules.templates.models import Template
from kadi.modules.templates.schemas import TemplateSchema


RESOURCE_TYPES = {
    "record": {
        "model": Record,
        "schema": RecordSchema,
        "title": _l("Record"),
        "title_plural": _l("Records"),
        "endpoint": "records.records",
    },
    "collection": {
        "model": Collection,
        "schema": CollectionSchema,
        "title": _l("Collection"),
        "title_plural": _l("Collections"),
        "endpoint": "collections.collections",
    },
    "template": {
        "model": Template,
        "schema": TemplateSchema,
        "title": _l("Template"),
        "title_plural": _l("Templates"),
        "endpoint": "templates.templates",
    },
    "group": {
        "model": Group,
        "schema": GroupSchema,
        "title": _l("Group"),
        "title_plural": _l("Groups"),
        "endpoint": "groups.groups",
    },
}
