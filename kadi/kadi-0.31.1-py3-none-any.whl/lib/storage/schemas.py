# Copyright 2022 Karlsruhe Institute of Technology
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
from marshmallow import fields
from marshmallow import validates
from marshmallow import ValidationError

import kadi.lib.constants as const
from .core import get_storage
from kadi.lib.schemas import KadiSchema


class StorageSchema(KadiSchema):
    """Schema to represent storages.

    See :class:`.BaseStorage`.
    """

    storage_type = fields.String(load_default=const.STORAGE_TYPE_LOCAL)

    storage_name = fields.String(dump_only=True)

    @validates("storage_type")
    def _validate_storage_type(self, value):
        if not get_storage(value):
            raise ValidationError("Not a valid storage type.")
