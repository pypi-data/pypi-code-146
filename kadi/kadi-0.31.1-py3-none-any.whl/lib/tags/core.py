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
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import StaleDataError

from .models import Tag
from kadi.lib.db import NestedTransaction


class TaggingMixin:
    """Mixin for SQLALchemy models to add support for tagging.

    The model needs a many-to-many ``tags`` relationship connecting itself with the
    :class:`.Tag` model.
    """

    def set_tags(self, names):
        """Set one or more tags.

        Will create a new tag object for each tag name that does not yet exist in the
        database and add it to the relationship. Existing tags from the relationship
        that are not in the given list are removed.

        :param names: A list of tag names.
        :return: ``True`` if the tags were set successfully, ``False`` otherwise.
        """
        with NestedTransaction(exc=StaleDataError) as t:
            for tag in self.tags:
                if tag.name not in names:
                    self.tags.remove(tag)

        if not t.success:
            return False

        with NestedTransaction(exc=IntegrityError) as t:
            for name in names:
                tag = Tag.get_or_create(name)

                if tag not in self.tags:
                    self.tags.append(tag)

        return t.success
