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
from marshmallow.validate import OneOf
from marshmallow.validate import Range

from kadi.lib.schemas import KadiSchema
from kadi.lib.web import url_for


class BasicResourceSchema(KadiSchema):
    """Schema to represent the basic attributes of resources.

    Currently, these resources may refer to instances of :class:`.Record`,
    :class:`.Collection`, :class:`.Template` or :class:`.Group`.
    """

    id = fields.Integer(dump_only=True)

    title = fields.String(dump_only=True)

    identifier = fields.String(dump_only=True)

    visibility = fields.String(dump_only=True)

    created_at = fields.DateTime(dump_only=True)

    last_modified = fields.DateTime(dump_only=True)

    # The type of the resource.
    type = fields.String(dump_only=True)

    # The human-readable type of the resource.
    pretty_type = fields.String(dump_only=True)

    _links = fields.Method("_generate_links")

    def _generate_links(self, obj):
        return {
            "view": url_for(f"{obj.type}s.view_{obj.type}", id=obj.id),
        }


class DeletedResourceSchema(BasicResourceSchema):
    """Schema to represent the basic attributes of deleted resources."""

    last_modified = fields.DateTime(dump_only=True, data_key="deleted_at")

    _actions = fields.Method("_generate_actions")

    def _generate_actions(self, obj):
        return {
            "restore": url_for(f"api.restore_{obj.type}", id=obj.id),
            "purge": url_for(f"api.purge_{obj.type}", id=obj.id),
        }


class ResourceRolesSchema(KadiSchema):
    """Schema to represent user and group roles of different resources.

    Mainly useful in combination with :func:`kadi.lib.resources.views.update_roles`.

    :param roles: A list of valid role values.
    """

    subject_type = fields.String(required=True, validate=OneOf(["user", "group"]))

    subject_id = fields.Integer(required=True, validate=Range(min=1))

    role = fields.String(required=True, allow_none=True)

    @validates("role")
    def _validate_role(self, value):
        # Always accept None values.
        if value is None:
            return

        if value not in self.roles:
            raise ValidationError(f"Must be one of: {', '.join(self.roles)}.")

    def __init__(self, roles, **kwargs):
        super().__init__(**kwargs)
        self.roles = set(roles)
