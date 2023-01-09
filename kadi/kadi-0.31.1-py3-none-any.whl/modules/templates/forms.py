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
from copy import deepcopy

from flask_babel import gettext as _
from flask_babel import lazy_gettext as _l
from flask_login import current_user
from marshmallow import ValidationError as SchemaValidationError
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import ValidationError

from .models import Template
from .models import TemplateVisibility
from .schemas import RecordTemplateSchema
from kadi.ext.db import db
from kadi.lib.conversion import empty_str
from kadi.lib.conversion import lower
from kadi.lib.conversion import none
from kadi.lib.conversion import normalize
from kadi.lib.conversion import strip
from kadi.lib.forms import check_duplicate_identifier
from kadi.lib.forms import DynamicMultiSelectField
from kadi.lib.forms import DynamicSelectField
from kadi.lib.forms import KadiForm
from kadi.lib.forms import LFTextAreaField
from kadi.lib.forms import SelectField
from kadi.lib.forms import StringField
from kadi.lib.forms import SubmitField
from kadi.lib.forms import validate_identifier
from kadi.lib.licenses.models import License
from kadi.lib.permissions.core import get_permitted_objects
from kadi.lib.resources.forms import RolesField
from kadi.lib.resources.forms import TagsField
from kadi.lib.tags.models import Tag
from kadi.modules.collections.models import Collection
from kadi.modules.collections.models import CollectionState
from kadi.modules.records.extras import ExtrasField
from kadi.modules.records.extras import is_nested_type
from kadi.modules.records.models import Record


class BaseTemplateForm(KadiForm):
    """Base form class for use in creating or updating templates.

    :param template: (optional) A template used for prefilling the form, which must be
        of the correct type corresponding to each form class.
    """

    title = StringField(
        _l("Title"),
        filters=[normalize],
        validators=[
            DataRequired(),
            Length(max=Template.Meta.check_constraints["title"]["length"]["max"]),
        ],
    )

    identifier = StringField(
        _l("Identifier"),
        filters=[lower, strip],
        validators=[
            DataRequired(),
            Length(max=Template.Meta.check_constraints["identifier"]["length"]["max"]),
            validate_identifier,
        ],
        description=_l("Unique identifier of this template."),
    )

    description = LFTextAreaField(
        _l("Description"),
        filters=[empty_str],
        validators=[
            Length(max=Template.Meta.check_constraints["description"]["length"]["max"])
        ],
    )

    visibility = SelectField(
        _l("Visibility"),
        choices=[
            (TemplateVisibility.PRIVATE, _l("Private")),
            (TemplateVisibility.PUBLIC, _l("Public")),
        ],
        description=_l(
            "Public visibility automatically grants EVERY logged-in user read"
            " permissions for this template."
        ),
    )

    def __init__(self, *args, template=None, data=None, **kwargs):
        # Prefill all simple fields using the "data" attribute, depending on whether any
        # existing data is passed in or not.
        if template is not None:
            new_data = {
                "title": template.title,
                "identifier": template.identifier,
                "description": template.description,
                "visibility": template.visibility,
            }

            if data is not None:
                data.update(new_data)
            else:
                data = new_data

        super().__init__(*args, data=data, **kwargs)

    @property
    def template_data(self):
        """Get the collected template data.

        The data may optionally be validated again. If it is invalid, ``None`` should be
        returned instead.
        """
        return None


def _remove_extra_values(extras):
    new_extras = []

    for extra in extras:
        new_extra = deepcopy(extra)

        if is_nested_type(extra["type"]):
            new_extra["value"] = _remove_extra_values(extra["value"])
        else:
            new_extra["value"] = None

        new_extras.append(new_extra)

    return new_extras


class BaseRecordTemplateForm(BaseTemplateForm):
    """Base form class for use in creating or updating record templates.

    :param template: (optional) See :class:`BaseTemplateForm`.
    :param record: (optional) A record used for prefilling the template data.
    :param user: (optional) A user that will be used for checking various access
        permissions when prefilling the form. Defaults to the current user.
    """

    record_title = StringField(
        _l("Title"),
        filters=[normalize, empty_str],
        validators=[
            Length(max=Record.Meta.check_constraints["title"]["length"]["max"])
        ],
    )

    record_identifier = StringField(
        _l("Identifier"),
        filters=[lower, strip, empty_str],
        validators=[
            Length(max=Record.Meta.check_constraints["identifier"]["length"]["max"])
        ],
        description=_l("Unique identifier of a record."),
    )

    record_type = DynamicSelectField(
        _l("Type"),
        filters=[lower, normalize, none],
        validators=[Length(max=Record.Meta.check_constraints["type"]["length"]["max"])],
        description=_l(
            "Optional type of a record, e.g. dataset, experimental device, etc."
        ),
    )

    record_description = LFTextAreaField(
        _l("Description"),
        filters=[empty_str],
        validators=[
            Length(max=Record.Meta.check_constraints["description"]["length"]["max"])
        ],
    )

    record_license = DynamicSelectField(
        _l("License"),
        description=_l("Optional license of a record."),
    )

    record_tags = TagsField(
        _l("Tags"),
        max_len=Tag.Meta.check_constraints["name"]["length"]["max"],
        description=_l("An optional list of keywords further describing a record."),
    )

    record_extras = ExtrasField(_l("Extra metadata"), is_template=True)

    record_collections = DynamicMultiSelectField(
        _l("Linked collections"),
        coerce=int,
        description=_l("Directly link a record with one or more collections."),
    )

    record_roles = RolesField(
        _l("Permissions"),
        roles=[(r, r.capitalize()) for r, _ in Record.Meta.permissions["roles"]],
        description=_l("Directly add user or group roles to a record."),
    )

    def __init__(self, *args, template=None, record=None, user=None, **kwargs):
        user = user if user is not None else current_user
        data = None

        # Prefill all simple fields using the "data" attribute.
        if template is not None:
            data = {
                "record_title": template.data.get("title", ""),
                "record_identifier": template.data.get("identifier", ""),
                "record_description": template.data.get("description", ""),
                "record_extras": template.data.get("extras", []),
            }
        elif record is not None:
            data = {
                "record_title": record.title,
                "record_identifier": record.identifier,
                "record_description": record.description,
                "record_extras": _remove_extra_values(record.extras),
            }

        super().__init__(*args, template=template, data=data, **kwargs)

        linkable_collection_ids_query = (
            get_permitted_objects(user, "link", "collection")
            .filter(Collection.state == CollectionState.ACTIVE)
            .with_entities(Collection.id)
        )

        # Prefill all other fields separately, depending on whether the form was
        # submitted or not.
        if self.is_submitted():
            if self.record_type.data is not None:
                self.record_type.initial = (
                    self.record_type.data,
                    self.record_type.data,
                )

            if self.record_license.data is not None:
                license = License.query.filter_by(name=self.record_license.data).first()

                if license is not None:
                    self.record_license.initial = (license.name, license.title)

            self.record_tags.initial = [
                (tag, tag) for tag in sorted(self.record_tags.data)
            ]

            if self.record_collections.data:
                collections = Collection.query.filter(
                    db.and_(
                        Collection.id.in_(linkable_collection_ids_query),
                        Collection.id.in_(self.record_collections.data),
                    )
                )
                self.record_collections.initial = [
                    (c.id, f"@{c.identifier}") for c in collections
                ]

            self.record_roles.set_initial_data(user=user, keep_user_roles=True)

        elif template is not None:
            if template.data.get("type") is not None:
                self.record_type.initial = (
                    template.data["type"],
                    template.data["type"],
                )

            if template.data.get("license") is not None:
                license = License.query.filter_by(name=template.data["license"]).first()

                if license is not None:
                    self.record_license.initial = (license.name, license.title)

            self.record_tags.initial = [
                (tag, tag) for tag in sorted(template.data.get("tags", []))
            ]

            if template.data.get("collections"):
                collections = Collection.query.filter(
                    db.and_(
                        Collection.id.in_(linkable_collection_ids_query),
                        Collection.id.in_(template.data["collections"]),
                    )
                )
                self.record_collections.initial = [
                    (c.id, f"@{c.identifier}") for c in collections
                ]

            self.record_roles.set_initial_data(
                data=template.data.get("roles", []), user=user, keep_user_roles=True
            )

        elif record is not None:
            if record.type is not None:
                self.record_type.initial = (record.type, record.type)

            if record.license is not None:
                self.record_license.initial = (
                    record.license.name,
                    record.license.title,
                )

            self.record_tags.initial = [
                (tag.name, tag.name) for tag in record.tags.order_by("name")
            ]

            collections = record.collections.filter(
                Collection.id.in_(linkable_collection_ids_query)
            )
            self.record_collections.initial = [
                (c.id, f"@{c.identifier}") for c in collections
            ]

            self.record_roles.set_initial_data(resource=record, user=user)

    def validate_record_identifier(self, record_identifier):
        # pylint: disable=missing-function-docstring
        if record_identifier.data:
            validate_identifier(self, record_identifier)

    def validate_record_license(self, record_license):
        # pylint: disable=missing-function-docstring
        if (
            record_license.data is not None
            and License.query.filter_by(name=record_license.data).first() is None
        ):
            raise ValidationError(_("Not a valid license."))

    @property
    def template_data(self):
        data = {
            "title": self.record_title.data,
            "identifier": self.record_identifier.data,
            "type": self.record_type.data,
            "description": self.record_description.data,
            "license": self.record_license.data,
            "tags": self.record_tags.data,
            "extras": self.record_extras.data,
            "collections": self.record_collections.data,
            "roles": self.record_roles.data,
        }

        try:
            # Validate the collected data with the corresponding schema again to ensure
            # it is consistent.
            data = RecordTemplateSchema().load(data)
        except SchemaValidationError:
            return None

        return data


class BaseExtrasTemplateForm(BaseTemplateForm):
    """Base form class for use in creating or updating extras templates.

    :param template: (optional) See :class:`BaseTemplateForm`.
    :param record: (optional) A record used for prefilling the template data.
    """

    extras = ExtrasField(_l("Extra metadata"), is_template=True)

    def __init__(self, *args, template=None, record=None, **kwargs):
        data = None

        if template is not None:
            data = {"extras": template.data}
        elif record is not None:
            data = {"extras": _remove_extra_values(record.extras)}

        super().__init__(*args, template=template, data=data, **kwargs)

    @property
    def template_data(self):
        return self.extras.data


class NewTemplateFormMixin:
    """Mixin class for forms used in creating new templates.

    :param template: (optional) See :class:`BaseTemplateForm`.
    :param user: (optional) A user that will be used for checking various access
        permissions when prefilling the form. Defaults to the current user.
    """

    roles = RolesField(
        _l("Permissions"),
        roles=[(r, r.capitalize()) for r, _ in Template.Meta.permissions["roles"]],
        description=_l("Directly add user or group roles to this template."),
    )

    submit = SubmitField(_l("Create template"))

    def __init__(self, *args, template=None, user=None, **kwargs):
        user = user if user is not None else current_user
        super().__init__(*args, template=template, user=user, **kwargs)

        if self.is_submitted():
            self.roles.set_initial_data(user=user)
        elif template is not None:
            self.roles.set_initial_data(resource=template, user=user)

    def validate_identifier(self, identifier):
        # pylint: disable=missing-function-docstring
        check_duplicate_identifier(Template, identifier.data)


class NewRecordTemplateForm(NewTemplateFormMixin, BaseRecordTemplateForm):
    """A form for use in creating new record templates."""


class NewExtrasTemplateForm(NewTemplateFormMixin, BaseExtrasTemplateForm):
    """A form for use in creating new extras templates."""


class EditTemplateFormMixin:
    """Mixin class for forms used in editing existing templates.

    :param template: The template to edit, used for prefilling the form.
    """

    submit = SubmitField(_l("Save changes"))

    submit_quit = SubmitField(_l("Save changes and quit"))

    def __init__(self, template, *args, **kwargs):
        self.template = template
        super().__init__(*args, template=template, **kwargs)

    def validate_identifier(self, identifier):
        # pylint: disable=missing-function-docstring
        check_duplicate_identifier(Template, identifier.data, exclude=self.template)


class EditRecordTemplateForm(EditTemplateFormMixin, BaseRecordTemplateForm):
    """A form for use in updating record templates."""


class EditExtrasTemplateForm(EditTemplateFormMixin, BaseExtrasTemplateForm):
    """A form for use in updating extras templates."""


class AddRolesForm(KadiForm):
    """A form for use in adding user or group roles to a template."""

    roles = RolesField(
        _l("New permissions"),
        roles=[(r, r.capitalize()) for r, _ in Template.Meta.permissions["roles"]],
    )

    submit = SubmitField(_l("Add permissions"))

    def validate(self, extra_validators=None):
        success = super().validate(extra_validators=extra_validators)

        if success and self.roles.data:
            return True

        return False
