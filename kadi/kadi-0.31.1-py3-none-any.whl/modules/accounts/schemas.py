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
from flask_login import current_user
from marshmallow import fields
from marshmallow import post_dump
from marshmallow import validates
from marshmallow.validate import ValidationError

from .models import User
from kadi.lib.permissions.models import Role
from kadi.lib.schemas import KadiSchema
from kadi.lib.web import url_for


class IdentitySchema(KadiSchema):
    """Schema to represent identities.

    See :class:`.Identity`.
    """

    type = fields.String(dump_only=True, data_key="identity_type")

    displayname = fields.String(dump_only=True)

    username = fields.String(dump_only=True)

    created_at = fields.DateTime(dump_only=True)

    last_modified = fields.DateTime(dump_only=True)

    identity_name = fields.Method("_get_identity_name")

    email = fields.Method("_get_email")

    @post_dump
    def _post_dump(self, data, **kwargs):
        if "email" in data and data["email"] is None:
            del data["email"]

        return data

    def _get_identity_name(self, obj):
        return str(obj.Meta.identity_type["name"])

    def _get_email(self, obj):
        if obj.user == current_user or not obj.user.email_is_private:
            return obj.email

        return None


class UserSchema(KadiSchema):
    """Schema to represent users.

    See :class:`.User`.
    """

    id = fields.Integer(required=True)

    is_sysadmin = fields.Bool(dump_only=True)

    state = fields.String(dump_only=True)

    created_at = fields.DateTime(dump_only=True)

    last_modified = fields.DateTime(dump_only=True)

    identity = fields.Nested(IdentitySchema, dump_only=True)

    system_role = fields.Method("_get_system_role")

    _links = fields.Method("_generate_links")

    _actions = fields.Method("_generate_actions")

    @validates("id")
    def _validate_id(self, value):
        if User.query.get_active(value) is None:
            raise ValidationError("No user with this ID exists.")

    @post_dump
    def _post_dump(self, data, **kwargs):
        if "_actions" in data and data["_actions"] is None:
            del data["_actions"]

        return data

    def _get_system_role(self, obj):
        role = obj.roles.filter(Role.object.is_(None), Role.object_id.is_(None)).first()
        return role.name if role is not None else None

    def _generate_links(self, obj):
        links = {
            "self": url_for("api.get_user", id=obj.id),
            "identities": url_for("api.get_user_identities", id=obj.id),
            "records": url_for("api.get_user_records", id=obj.id),
            "collections": url_for("api.get_user_collections", id=obj.id),
            "templates": url_for("api.get_user_templates", id=obj.id),
            "groups": url_for("api.get_user_groups", id=obj.id),
        }

        if self._internal:
            if obj.image_name:
                links["image"] = url_for("api.preview_user_image", id=obj.id)

            links["view"] = url_for("accounts.view_user", id=obj.id)

        return links

    def _generate_actions(self, obj):
        if self._internal:
            return {
                "change_role": url_for("api.change_system_role", id=obj.id),
                "toggle_state": url_for("api.toggle_user_state", id=obj.id),
                "toggle_sysadmin": url_for("api.toggle_user_sysadmin", id=obj.id),
                "delete": url_for("api.delete_user", id=obj.id),
            }

        return None
