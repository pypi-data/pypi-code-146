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
from marshmallow import fields
from marshmallow import post_dump
from marshmallow import validates
from marshmallow.validate import Length
from marshmallow.validate import OneOf
from marshmallow.validate import ValidationError

from .models import Group
from kadi.lib.api.core import check_access_token_scopes
from kadi.lib.conversion import lower
from kadi.lib.conversion import normalize
from kadi.lib.conversion import strip
from kadi.lib.schemas import check_duplicate_identifier
from kadi.lib.schemas import FilteredString
from kadi.lib.schemas import KadiSchema
from kadi.lib.schemas import validate_identifier
from kadi.lib.web import url_for
from kadi.modules.accounts.schemas import UserSchema


class GroupSchema(KadiSchema):
    """Schema to represent groups.

    See :class:`.Group`.

    :param previous_group: (optional) A group whose identifier should be excluded when
        checking for duplicates while deserializing.
    """

    id = fields.Integer(required=True)

    identifier = FilteredString(
        required=True,
        filters=[lower, strip],
        validate=[
            Length(max=Group.Meta.check_constraints["identifier"]["length"]["max"]),
            validate_identifier,
        ],
    )

    title = FilteredString(
        required=True,
        filters=[normalize],
        validate=Length(max=Group.Meta.check_constraints["title"]["length"]["max"]),
    )

    description = fields.String(
        validate=Length(
            max=Group.Meta.check_constraints["description"]["length"]["max"]
        )
    )

    visibility = fields.String(
        validate=OneOf(Group.Meta.check_constraints["visibility"]["values"])
    )

    plain_description = fields.String(dump_only=True)

    state = fields.String(dump_only=True)

    created_at = fields.DateTime(dump_only=True)

    last_modified = fields.DateTime(dump_only=True)

    creator = fields.Nested(UserSchema, dump_only=True)

    _links = fields.Method("_generate_links")

    _actions = fields.Method("_generate_actions")

    def __init__(self, previous_group=None, **kwargs):
        super().__init__(**kwargs)
        self.previous_group = previous_group

    @validates("id")
    def _validate_id(self, value):
        if Group.query.get_active(value) is None:
            raise ValidationError("No group with this ID exists.")

    @validates("identifier")
    def _validate_identifier(self, value):
        check_duplicate_identifier(Group, value, exclude=self.previous_group)

    @post_dump
    def _post_dump(self, data, **kwargs):
        if "creator" in data and not check_access_token_scopes("user.read"):
            del data["creator"]

        return data

    def _generate_links(self, obj):
        links = {
            "self": url_for("api.get_group", id=obj.id),
            "members": url_for("api.get_group_members", id=obj.id),
            "revisions": url_for("api.get_group_revisions", id=obj.id),
        }

        if self._internal:
            if obj.image_name:
                links["image"] = url_for("api.preview_group_image", id=obj.id)

            links["view"] = url_for("groups.view_group", id=obj.id)

        return links

    def _generate_actions(self, obj):
        return {
            "edit": url_for("api.edit_group", id=obj.id),
            "delete": url_for("api.delete_group", id=obj.id),
            "add_member": url_for("api.add_group_member", id=obj.id),
        }
