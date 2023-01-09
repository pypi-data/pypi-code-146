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
from flask_babel import gettext as _
from flask_babel import lazy_gettext as _l
from flask_login import current_user
from wtforms.validators import DataRequired
from wtforms.validators import InputRequired
from wtforms.validators import Length
from wtforms.validators import NumberRange
from wtforms.validators import ValidationError

from .extras import ExtrasField
from .models import Chunk
from .models import File
from .models import FileState
from .models import Record
from .models import RecordLink
from .models import RecordVisibility
from kadi.ext.db import db
from kadi.lib.conversion import empty_str
from kadi.lib.conversion import lower
from kadi.lib.conversion import none
from kadi.lib.conversion import normalize
from kadi.lib.conversion import strip
from kadi.lib.format import filesize
from kadi.lib.forms import check_duplicate_identifier
from kadi.lib.forms import DynamicMultiSelectField
from kadi.lib.forms import DynamicSelectField
from kadi.lib.forms import FileField
from kadi.lib.forms import IntegerField
from kadi.lib.forms import KadiForm
from kadi.lib.forms import LFTextAreaField
from kadi.lib.forms import SelectField
from kadi.lib.forms import StringField
from kadi.lib.forms import SubmitField
from kadi.lib.forms import validate_identifier
from kadi.lib.forms import validate_mimetype
from kadi.lib.licenses.models import License
from kadi.lib.permissions.core import get_permitted_objects
from kadi.lib.permissions.core import has_permission
from kadi.lib.resources.forms import RolesField
from kadi.lib.resources.forms import TagsField
from kadi.lib.tags.models import Tag
from kadi.modules.collections.models import Collection
from kadi.modules.collections.models import CollectionState
from kadi.modules.templates.models import TemplateType


class BaseRecordForm(KadiForm):
    """Base form class for use in creating or updating records.

    :param record: (optional) A record used for prefilling the form.
    :param template: (optional) A record or extras template used for prefilling the
        form.
    """

    title = StringField(
        _l("Title"),
        filters=[normalize],
        validators=[
            DataRequired(),
            Length(max=Record.Meta.check_constraints["title"]["length"]["max"]),
        ],
    )

    identifier = StringField(
        _l("Identifier"),
        filters=[lower, strip],
        validators=[
            DataRequired(),
            Length(max=Record.Meta.check_constraints["identifier"]["length"]["max"]),
            validate_identifier,
        ],
        description=_l("Unique identifier of this record."),
    )

    type = DynamicSelectField(
        _l("Type"),
        filters=[lower, normalize, none],
        validators=[Length(max=Record.Meta.check_constraints["type"]["length"]["max"])],
        description=_l(
            "Optional type of this record, e.g. dataset, experimental device, etc."
        ),
    )

    description = LFTextAreaField(
        _l("Description"),
        filters=[empty_str],
        validators=[
            Length(max=Record.Meta.check_constraints["description"]["length"]["max"])
        ],
    )

    license = DynamicSelectField(
        _l("License"),
        description=_l(
            "Specifying an optional license can determine the conditions for the"
            " correct reuse of data and metadata when the record is published or simply"
            " shared with other users. A license can also be uploaded as a file, in"
            " which case one of the 'Other' licenses can be chosen."
        ),
    )

    visibility = SelectField(
        _l("Visibility"),
        choices=[
            (RecordVisibility.PRIVATE, _l("Private")),
            (RecordVisibility.PUBLIC, _l("Public")),
        ],
        description=_l(
            "Public visibility automatically grants EVERY logged-in user read"
            " permissions for this record."
        ),
    )

    tags = TagsField(
        _l("Tags"),
        max_len=Tag.Meta.check_constraints["name"]["length"]["max"],
        description=_l("An optional list of keywords further describing the record."),
    )

    extras = ExtrasField(_l("Extra metadata"))

    def __init__(self, *args, record=None, template=None, **kwargs):
        data = None

        # Prefill all simple fields using the "data" attribute.
        if record is not None:
            data = {
                "title": record.title,
                "identifier": record.identifier,
                "description": record.description,
                "visibility": record.visibility,
                "extras": record.extras,
            }
        elif template is not None:
            if template.type == TemplateType.RECORD:
                data = {
                    "title": template.data.get("title", ""),
                    "identifier": template.data.get("identifier", ""),
                    "description": template.data.get("description", ""),
                    "extras": template.data.get("extras", []),
                }
            elif template.type == TemplateType.EXTRAS:
                data = {"extras": template.data}

        super().__init__(*args, data=data, **kwargs)

        # Prefill all other fields separately, depending on whether the form was
        # submitted or not.
        if self.is_submitted():
            if self.type.data is not None:
                self.type.initial = (self.type.data, self.type.data)

            if self.license.data is not None:
                license = License.query.filter_by(name=self.license.data).first()

                if license is not None:
                    self.license.initial = (license.name, license.title)

            self.tags.initial = [(tag, tag) for tag in sorted(self.tags.data)]

        elif record is not None:
            if record.type is not None:
                self.type.initial = (record.type, record.type)

            if record.license is not None:
                self.license.initial = (record.license.name, record.license.title)

            self.tags.initial = [
                (tag.name, tag.name) for tag in record.tags.order_by("name")
            ]

        elif template is not None and template.type == TemplateType.RECORD:
            if template.data.get("type") is not None:
                self.type.initial = (template.data["type"], template.data["type"])

            if template.data.get("license") is not None:
                license = License.query.filter_by(name=template.data["license"]).first()

                if license is not None:
                    self.license.initial = (license.name, license.title)

            self.tags.initial = [
                (tag, tag) for tag in sorted(template.data.get("tags", []))
            ]

    def validate_license(self, license):
        # pylint: disable=missing-function-docstring
        if (
            license.data is not None
            and License.query.filter_by(name=license.data).first() is None
        ):
            raise ValidationError(_("Not a valid license."))


class NewRecordForm(BaseRecordForm):
    """A form for use in creating new records.

    :param record: (optional) See :class:`BaseRecordForm`.
    :param template: (optional) See :class:`BaseRecordForm`.
    :param collection: (optional) A collection used for prefilling the linked
        collections.
    :param user: (optional) A user that will be used for checking various access
        permissions when prefilling the form. Defaults to the current user.
    """

    collections = DynamicMultiSelectField(
        _l("Linked collections"),
        coerce=int,
        description=_l("Directly link this record with one or more collections."),
    )

    roles = RolesField(
        _l("Permissions"),
        roles=[(r, r.capitalize()) for r, _ in Record.Meta.permissions["roles"]],
        description=_l("Directly add user or group roles to this record."),
    )

    submit = SubmitField(_l("Create record"))

    def __init__(
        self, *args, record=None, template=None, collection=None, user=None, **kwargs
    ):
        user = user if user is not None else current_user
        super().__init__(*args, record=record, template=template, **kwargs)

        linkable_collection_ids_query = (
            get_permitted_objects(user, "link", "collection")
            .filter(Collection.state == CollectionState.ACTIVE)
            .with_entities(Collection.id)
        )

        if self.is_submitted():
            if self.collections.data:
                collections = Collection.query.filter(
                    db.and_(
                        Collection.id.in_(linkable_collection_ids_query),
                        Collection.id.in_(self.collections.data),
                    )
                )
                self.collections.initial = [
                    (c.id, f"@{c.identifier}") for c in collections
                ]

            self.roles.set_initial_data(user=user)

        else:
            if record is not None:
                collections = record.collections.filter(
                    Collection.id.in_(linkable_collection_ids_query)
                )
                self.collections.initial = [
                    (c.id, f"@{c.identifier}") for c in collections
                ]

                self.roles.set_initial_data(resource=record, user=user)

            elif template is not None and template.type == TemplateType.RECORD:
                if template.data.get("collections"):
                    collections = Collection.query.filter(
                        db.and_(
                            Collection.id.in_(linkable_collection_ids_query),
                            Collection.id.in_(template.data["collections"]),
                        )
                    )
                    self.collections.initial = [
                        (c.id, f"@{c.identifier}") for c in collections
                    ]

                self.roles.set_initial_data(
                    data=template.data.get("roles", []), user=user
                )

            # If a collection is given, overwrite all values set previously for the
            # linked collections.
            if collection is not None:
                self.collections.initial = [
                    (collection.id, f"@{collection.identifier}")
                ]

    def validate_identifier(self, identifier):
        # pylint: disable=missing-function-docstring
        check_duplicate_identifier(Record, identifier.data)


class EditRecordForm(BaseRecordForm):
    """A form for use in editing existing records.

    :param record: The record to edit, used for prefilling the form.
    """

    submit = SubmitField(_l("Save changes"))

    submit_quit = SubmitField(_l("Save changes and quit"))

    def __init__(self, record, *args, **kwargs):
        self.record = record
        super().__init__(*args, record=record, **kwargs)

    def validate_identifier(self, identifier):
        # pylint: disable=missing-function-docstring
        check_duplicate_identifier(Record, identifier.data, exclude=self.record)


class BaseRecordLinkForm(KadiForm):
    """Base form class for use in creating or updating record links.

    :param record_link: (optional) A record link used for prefilling the form.
    """

    name = DynamicSelectField(
        _l("Name"),
        filters=[normalize],
        validators=[
            DataRequired(),
            Length(max=RecordLink.Meta.check_constraints["name"]["length"]["max"]),
        ],
        description=_l("The name of the link."),
    )

    term = StringField(
        _l("Term IRI"),
        filters=[strip, none],
        validators=[
            Length(max=RecordLink.Meta.check_constraints["term"]["length"]["max"])
        ],
        description=_l(
            "An IRI specifying an existing term that the link should represent."
        ),
    )

    def __init__(self, *args, record_link=None, **kwargs):
        data = None

        # Prefill all simple fields using the "data" attribute.
        if record_link is not None:
            data = {"term": record_link.term}

        super().__init__(*args, data=data, **kwargs)

        # Prefill all other fields separately, depending on whether the form was
        # submitted or not.
        if self.is_submitted():
            if self.name.data is not None:
                self.name.initial = (self.name.data, self.name.data)

        elif record_link is not None:
            if record_link.name is not None:
                self.name.initial = (record_link.name, record_link.name)


class NewRecordLinkForm(BaseRecordLinkForm):
    """A form for use in creating new record links.

    :param user: (optional) A user that will be used for checking various access
        permissions when prefilling the form. Defaults to the current user.
    """

    record = DynamicSelectField(_l("Record"), validators=[DataRequired()], coerce=int)

    link_direction = SelectField(
        _l("Link direction"), choices=[("out", _l("Outgoing")), ("in", _l("Incoming"))]
    )

    submit = SubmitField(_l("Link record"))

    def __init__(self, *args, user=None, **kwargs):
        user = user if user is not None else current_user
        super().__init__(*args, **kwargs)

        if self.is_submitted() and self.record.data is not None:
            record = Record.query.get_active(self.record.data)

            if record is not None and has_permission(user, "read", "record", record.id):
                self.record.initial = (record.id, f"@{record.identifier}")


class EditRecordLinkForm(BaseRecordLinkForm):
    """A form for use in editing existing record links.

    :param record_link: The record link to edit, used for prefilling the form.
    """

    submit = SubmitField(_l("Save changes"))

    def __init__(self, record_link, *args, **kwargs):
        super().__init__(*args, record_link=record_link, **kwargs)


class LinkCollectionsForm(KadiForm):
    """A form for use in linking records with collections."""

    collections = DynamicMultiSelectField(
        _l("Collections"), validators=[DataRequired()], coerce=int
    )

    submit = SubmitField(_l("Link collections"))


class AddRolesForm(KadiForm):
    """A form for use in adding user or group roles to a record."""

    roles = RolesField(
        _l("New permissions"),
        roles=[(r, r.capitalize()) for r, _ in Record.Meta.permissions["roles"]],
    )

    submit = SubmitField(_l("Add permissions"))

    def validate(self, extra_validators=None):
        success = super().validate(extra_validators=extra_validators)

        if success and self.roles.data:
            return True

        return False


class ChunkForm(KadiForm):
    """A form for use in uploading file chunks.

    Currently only used within the API.

    :param chunk_count: The total amount of chunks that the upload this chunk is part of
        has. Will be used to validate the chunk's index.
    :param chunk_size: The configured chunk size.
    """

    class Meta:
        """Container to store meta class attributes."""

        csrf = False

    checksum = StringField(
        filters=[strip],
        validators=[Length(max=File.Meta.check_constraints["name"]["length"]["max"])],
    )

    index = IntegerField(
        validators=[
            InputRequired(message="Missing data for required field."),
            NumberRange(
                min=Chunk.Meta.check_constraints["index"]["range"]["min"],
                message="Must be greater than or equal to %(min)s.",
            ),
        ]
    )

    size = IntegerField(
        validators=[
            InputRequired(message="Missing data for required field."),
            NumberRange(
                min=Chunk.Meta.check_constraints["size"]["range"]["min"],
                message="Must be greater than or equal to %(min)s.",
            ),
        ],
    )

    blob = FileField(validators=[DataRequired()])

    def __init__(self, chunk_count, chunk_size, *args, **kwargs):
        self.chunk_count = chunk_count
        self.chunk_size = chunk_size

        super().__init__(*args, **kwargs)

    def validate_index(self, index):
        # pylint: disable=missing-function-docstring
        if index.data is not None and index.data >= self.chunk_count:
            raise ValidationError(f"Must be less than {self.chunk_count}.")

    def validate_size(self, size):
        # pylint: disable=missing-function-docstring
        if size.data is not None and size.data > self.chunk_size:
            raise ValidationError(
                f"Maximum size exceeded ({filesize(self.chunk_size)})."
            )


class EditFileForm(KadiForm):
    """A form for use in editing file metadata.

    :param file: A file used for prefilling the form and checking for duplicate file
        names.
    """

    name = StringField(
        _l("Filename"),
        filters=[normalize],
        validators=[
            DataRequired(),
            Length(max=File.Meta.check_constraints["name"]["length"]["max"]),
        ],
    )

    mimetype = StringField(
        _l("MIME type"),
        filters=[lower, normalize],
        validators=[
            DataRequired(),
            Length(max=File.Meta.check_constraints["mimetype"]["length"]["max"]),
            validate_mimetype,
        ],
    )

    description = LFTextAreaField(
        _l("Description"),
        filters=[empty_str],
        validators=[
            Length(max=File.Meta.check_constraints["description"]["length"]["max"])
        ],
    )

    submit = SubmitField(_l("Save changes"))

    def __init__(self, file, *args, **kwargs):
        self.file = file
        super().__init__(*args, obj=file, **kwargs)

    def validate_name(self, name):
        # pylint: disable=missing-function-docstring
        file = File.query.filter(
            File.record_id == self.file.record_id,
            File.state == FileState.ACTIVE,
            File.name == name.data,
        ).first()

        if file is not None and self.file != file:
            raise ValidationError(_("Name is already in use."))
