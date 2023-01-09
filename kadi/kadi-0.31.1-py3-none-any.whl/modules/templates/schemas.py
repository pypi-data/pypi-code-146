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
from marshmallow import post_load
from marshmallow import validates
from marshmallow import ValidationError
from marshmallow.validate import Length
from marshmallow.validate import OneOf
from marshmallow.validate import Range

from .models import Template
from .models import TemplateType
from kadi.lib.api.core import check_access_token_scopes
from kadi.lib.conversion import lower
from kadi.lib.conversion import normalize
from kadi.lib.conversion import strip
from kadi.lib.resources.schemas import ResourceRolesSchema
from kadi.lib.schemas import check_duplicate_identifier
from kadi.lib.schemas import FilteredString
from kadi.lib.schemas import KadiSchema
from kadi.lib.schemas import validate_identifier
from kadi.lib.web import url_for
from kadi.modules.accounts.schemas import UserSchema
from kadi.modules.records.extras import ExtraSchema
from kadi.modules.records.models import Record
from kadi.modules.records.schemas import RecordSchema


# Default values of record templates.
DEFAULT_RECORD_DATA = {
    "title": "",
    "identifier": "",
    "type": None,
    "description": "",
    "license": None,
    "tags": [],
    "extras": [],
    "collections": [],
    "roles": [],
}


class RecordTemplateSchema(RecordSchema):
    """Schema to represent the data of record templates.

    See :class:`.Template`.
    """

    identifier = FilteredString(
        allow_ws_only=True,
        filters=[lower, strip],
        validate=[
            Length(max=Record.Meta.check_constraints["identifier"]["length"]["max"])
        ],
    )

    title = FilteredString(
        allow_ws_only=True,
        filters=[normalize],
        validate=Length(max=Record.Meta.check_constraints["title"]["length"]["max"]),
    )

    collections = fields.List(fields.Integer(validate=Range(min=1)))

    roles = fields.Nested(
        ResourceRolesSchema(
            roles=[r for r, _ in Record.Meta.permissions["roles"]], many=True
        )
    )

    def __init__(self, **kwargs):
        kwargs["is_template"] = True
        kwargs["partial"] = True
        kwargs["exclude"] = ["id", "visibility", *kwargs.pop("exclude", [])]

        super().__init__(**kwargs)

    @post_load
    def _post_load(self, data, **kwargs):
        data = super()._post_load(data, **kwargs)

        # Fill in any missing default values of the data manually, so the resulting
        # template data is always consistent in regards to the included keys.
        for key, value in DEFAULT_RECORD_DATA.items():
            if key not in data:
                data[key] = value

        return data

    @validates("identifier")
    def _validate_identifier(self, value):
        # Skip the duplicate check and also skip the format validation if the identifier
        # value is empty.
        if value:
            validate_identifier(value)


class TemplateSchema(KadiSchema):
    """Schema to represent generic templates.

    See :class:`.Template`.

    :param previous_template: (optional) A template whose identifier should be excluded
        when checking for duplicates while deserializing.
    :param template_type: (optional) The type of the template. Used when deserializing
        the data and it contains no type value.
    """

    id = fields.Integer(dump_only=True)

    identifier = FilteredString(
        required=True,
        filters=[lower, strip],
        validate=[
            Length(max=Template.Meta.check_constraints["identifier"]["length"]["max"]),
            validate_identifier,
        ],
    )

    title = FilteredString(
        required=True,
        filters=[normalize],
        validate=Length(max=Template.Meta.check_constraints["title"]["length"]["max"]),
    )

    description = fields.String(
        validate=Length(
            max=Template.Meta.check_constraints["description"]["length"]["max"]
        )
    )

    visibility = fields.String(
        validate=OneOf(Template.Meta.check_constraints["visibility"]["values"])
    )

    type = FilteredString(
        required=True,
        filters=[lower, strip],
        validate=OneOf(Template.Meta.check_constraints["type"]["values"]),
    )

    data = fields.Raw(required=True)

    plain_description = fields.String(dump_only=True)

    state = fields.String(dump_only=True)

    created_at = fields.DateTime(dump_only=True)

    last_modified = fields.DateTime(dump_only=True)

    creator = fields.Nested(UserSchema, dump_only=True)

    _links = fields.Method("_generate_links")

    _actions = fields.Method("_generate_actions")

    def __init__(self, previous_template=None, template_type=None, **kwargs):
        super().__init__(**kwargs)

        self.previous_template = previous_template
        self.template_type = template_type

    @validates("identifier")
    def _validate_identifier(self, value):
        check_duplicate_identifier(Template, value, exclude=self.previous_template)

    @post_load
    def _post_load(self, data, **kwargs):
        if "data" not in data:
            return data

        current_type = data.get("type") or self.template_type

        if current_type == TemplateType.RECORD:
            schema = RecordTemplateSchema()
        elif current_type == TemplateType.EXTRAS:
            schema = ExtraSchema(is_template=True, many=True)
        else:
            # Will also be triggered when providing an invalid template type directly.
            raise ValidationError("Invalid value.", "type")

        try:
            data["data"] = schema.load(data["data"])
        except ValidationError as e:
            raise ValidationError(e.messages, "data") from e

        return data

    @post_dump
    def _post_dump(self, data, **kwargs):
        if "creator" in data and not check_access_token_scopes("user.read"):
            del data["creator"]

        return data

    def _generate_links(self, obj):
        links = {
            "self": url_for("api.get_template", id=obj.id),
            "user_roles": url_for("api.get_template_user_roles", id=obj.id),
            "group_roles": url_for("api.get_template_group_roles", id=obj.id),
        }

        if self._internal:
            links["view"] = url_for("templates.view_template", id=obj.id)

        return links

    def _generate_actions(self, obj):
        return {
            "edit": url_for("api.edit_template", id=obj.id),
            "delete": url_for("api.delete_template", id=obj.id),
            "add_user_role": url_for("api.add_template_user_role", id=obj.id),
            "add_group_role": url_for("api.add_template_group_role", id=obj.id),
        }
