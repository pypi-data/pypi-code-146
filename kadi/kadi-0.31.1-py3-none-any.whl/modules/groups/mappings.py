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
from elasticsearch_dsl import Date
from elasticsearch_dsl import Document
from elasticsearch_dsl import Keyword
from elasticsearch_dsl import MetaField
from elasticsearch_dsl import Text

from kadi.lib.search.core import MappingMixin


class GroupMapping(Document, MappingMixin):
    """Search mapping for groups.

    See :class:`.Group`.
    """

    class Meta:
        """Container to store meta class attributes."""

        dynamic = MetaField(False)

    identifier = Text(
        required=True,
        analyzer=MappingMixin.Analyzers.trigram,
        fields={"text": Text(), "keyword": Keyword()},
    )

    title = Text(
        required=True,
        analyzer=MappingMixin.Analyzers.trigram,
        fields={"text": Text(), "keyword": Keyword()},
    )

    plain_description = Text(required=True)

    created_at = Date(required=True, default_timezone="UTC")

    last_modified = Date(required=True, default_timezone="UTC")
