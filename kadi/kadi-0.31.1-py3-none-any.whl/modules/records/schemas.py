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
from marshmallow.validate import Length
from marshmallow.validate import OneOf
from marshmallow.validate import Range
from marshmallow.validate import ValidationError

import kadi.lib.constants as const
from .models import File
from .models import Record
from .models import RecordLink
from .models import Upload
from .models import UploadType
from kadi.lib.api.core import check_access_token_scopes
from kadi.lib.conversion import lower
from kadi.lib.conversion import normalize
from kadi.lib.conversion import strip
from kadi.lib.licenses.schemas import LicenseSchema
from kadi.lib.schemas import check_duplicate_identifier
from kadi.lib.schemas import FilteredString
from kadi.lib.schemas import KadiSchema
from kadi.lib.schemas import SortedPluck
from kadi.lib.schemas import validate_identifier
from kadi.lib.schemas import validate_mimetype
from kadi.lib.schemas import ValidateUUID
from kadi.lib.storage.schemas import StorageSchema
from kadi.lib.tags.schemas import TagSchema
from kadi.lib.web import url_for
from kadi.modules.accounts.schemas import UserSchema
from kadi.modules.records.extras import ExtraSchema


class RecordSchema(KadiSchema):
    """Schema to represent records.

    See :class:`.Record`.

    :param previous_record: (optional) A record whose identifier should be excluded when
        checking for duplicates while deserializing.
    :param linked_collection: (optional) A collection that is linked to each record that
        should be serialized. Will be used to build endpoints for corresponding actions.
    :param is_template: (optional) Flag indicating whether the schema is used inside a
        template. Currently, this is only relevant for the extra metadata.
    """

    id = fields.Integer(required=True)

    identifier = FilteredString(
        required=True,
        filters=[lower, strip],
        validate=[
            Length(max=Record.Meta.check_constraints["identifier"]["length"]["max"]),
            validate_identifier,
        ],
    )

    title = FilteredString(
        required=True,
        filters=[normalize],
        validate=Length(max=Record.Meta.check_constraints["title"]["length"]["max"]),
    )

    type = FilteredString(
        allow_none=True,
        filters=[lower, normalize],
        validate=Length(max=Record.Meta.check_constraints["type"]["length"]["max"]),
    )

    description = fields.String(
        validate=Length(
            max=Record.Meta.check_constraints["description"]["length"]["max"]
        )
    )

    license = fields.Pluck(LicenseSchema, "name", allow_none=True)

    visibility = fields.String(
        validate=OneOf(Record.Meta.check_constraints["visibility"]["values"])
    )

    extras = fields.Method("_serialize_extras", deserialize="_deserialize_extras")

    tags = SortedPluck(TagSchema, "name", many=True)

    plain_description = fields.String(dump_only=True)

    state = fields.String(dump_only=True)

    created_at = fields.DateTime(dump_only=True)

    last_modified = fields.DateTime(dump_only=True)

    creator = fields.Nested(UserSchema, dump_only=True)

    _links = fields.Method("_generate_links")

    _actions = fields.Method("_generate_actions")

    def __init__(
        self,
        previous_record=None,
        linked_collection=None,
        is_template=False,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.previous_record = previous_record
        self.linked_collection = linked_collection
        self.is_template = is_template

    @validates("id")
    def _validate_id(self, value):
        if Record.query.get_active(value) is None:
            raise ValidationError("No record with this ID exists.")

    @validates("identifier")
    def _validate_identifier(self, value):
        check_duplicate_identifier(Record, value, exclude=self.previous_record)

    @post_dump
    def _post_dump(self, data, **kwargs):
        if "creator" in data and not check_access_token_scopes("user.read"):
            del data["creator"]

        return data

    @post_load
    def _post_load(self, data, **kwargs):
        if data.get("license") is not None:
            data["license"] = data["license"]["name"]

        if "tags" in data:
            data["tags"] = sorted(list({tag["name"] for tag in data["tags"]}))

        return data

    def _serialize_extras(self, obj):
        return obj.extras

    def _deserialize_extras(self, value):
        return ExtraSchema(is_template=self.is_template, many=True).load(value)

    def _generate_links(self, obj):
        links = {
            "self": url_for("api.get_record", id=obj.id),
            "files": url_for("api.get_files", id=obj.id),
            "records_to": url_for("api.get_record_links", id=obj.id, direction="out"),
            "records_from": url_for("api.get_record_links", id=obj.id, direction="in"),
            "collections": url_for("api.get_record_collections", id=obj.id),
            "user_roles": url_for("api.get_record_user_roles", id=obj.id),
            "group_roles": url_for("api.get_record_group_roles", id=obj.id),
            "revisions": url_for("api.get_record_revisions", id=obj.id),
            "file_revisions": url_for("api.get_file_revisions", id=obj.id),
        }

        if self._internal:
            links["view"] = url_for("records.view_record", id=obj.id)

        return links

    def _generate_actions(self, obj):
        actions = {
            "edit": url_for("api.edit_record", id=obj.id),
            "delete": url_for("api.delete_record", id=obj.id),
            "new_upload": url_for("api.new_upload", id=obj.id),
            "upload_file": url_for("api.upload_file", id=obj.id),
            "link_record": url_for("api.new_record_link", id=obj.id),
            "link_collection": url_for("api.add_record_collection", id=obj.id),
            "add_user_role": url_for("api.add_record_user_role", id=obj.id),
            "add_group_role": url_for("api.add_record_group_role", id=obj.id),
        }

        if self.linked_collection:
            actions["remove_link"] = url_for(
                "api.remove_collection_record",
                collection_id=self.linked_collection.id,
                record_id=obj.id,
            )

        return actions


class RecordLinkSchema(KadiSchema):
    """Schema to represent record links.

    See :class:`.RecordLink`.

    :param current_record: (optional) The current record in whose context the record
        links are being serialized, in order to generate corresponding URLs to view or
        edit each record link. Only relevant for internal use.
    """

    id = fields.Integer(dump_only=True)

    name = FilteredString(
        required=True,
        filters=[normalize],
        validate=Length(max=RecordLink.Meta.check_constraints["name"]["length"]["max"]),
    )

    term = FilteredString(
        filters=[strip],
        validate=Length(max=RecordLink.Meta.check_constraints["term"]["length"]["max"]),
    )

    created_at = fields.DateTime(dump_only=True)

    last_modified = fields.DateTime(dump_only=True)

    creator = fields.Nested(UserSchema, dump_only=True)

    record_from = fields.Nested(RecordSchema, dump_only=True)

    record_to = fields.Nested(RecordSchema, required=True)

    _links = fields.Method("_generate_links")

    _actions = fields.Method("_generate_actions")

    def __init__(self, current_record=None, **kwargs):
        super().__init__(**kwargs)
        self.current_record = current_record

    @post_dump
    def _post_dump(self, data, **kwargs):
        if "creator" in data and not check_access_token_scopes("user.read"):
            del data["creator"]

        return data

    def _generate_links(self, obj):
        links = {
            "self": url_for(
                "api.get_record_link", record_id=obj.record_from_id, link_id=obj.id
            )
        }

        if self._internal and self.current_record is not None:
            links["view"] = url_for(
                "records.view_record_link",
                record_id=self.current_record.id,
                link_id=obj.id,
            )
            links["edit"] = url_for(
                "records.edit_record_link",
                record_id=self.current_record.id,
                link_id=obj.id,
            )

        return links

    def _generate_actions(self, obj):
        return {
            "edit": url_for(
                "api.edit_record_link", record_id=obj.record_from_id, link_id=obj.id
            ),
            "remove": url_for(
                "api.remove_record_link", record_id=obj.record_from_id, link_id=obj.id
            ),
        }


class RecordLinkRevisionSchema(RecordLinkSchema):
    """Schema to represent record link revisions.

    Additionally includes the direct serialization of the IDs of the linked records.
    """

    record_from_id = fields.Integer(dump_only=True)

    record_to_id = fields.Integer(dump_only=True)


class RecordRevisionSchema(RecordSchema):
    """Schema to represent record revisions.

    Additionally includes the direct serialization of record links with a limited subset
    of attributes.
    """

    links_to = fields.Nested(
        RecordLinkRevisionSchema,
        only=["record_to_id", "name", "term"],
        many=True,
        dump_only=True,
    )

    linked_from = fields.Nested(
        RecordLinkRevisionSchema,
        only=["record_from_id", "name", "term"],
        many=True,
        dump_only=True,
    )


class FileSchema(KadiSchema):
    """Schema to represent files.

    See :class:`.File`.

    :param record: (optional) A record the file to be deserialized belongs to. Will be
        used to check for duplicate filenames while deserializing.
    :param previous_file: (optional) A file that will be excluded when checking for
        duplicate filenames while deserializing.
    """

    id = fields.String(required=True, validate=ValidateUUID(version=4))

    name = FilteredString(
        required=True,
        filters=[normalize],
        validate=Length(max=File.Meta.check_constraints["name"]["length"]["max"]),
    )

    size = fields.Integer(
        required=True,
        validate=Range(min=File.Meta.check_constraints["size"]["range"]["min"]),
    )

    description = fields.String(
        validate=Length(max=File.Meta.check_constraints["description"]["length"]["max"])
    )

    mimetype = FilteredString(
        filters=[lower, normalize],
        validate=[
            Length(max=File.Meta.check_constraints["mimetype"]["length"]["max"]),
            validate_mimetype,
        ],
    )

    checksum = FilteredString(
        filters=[strip],
        validate=Length(max=File.Meta.check_constraints["checksum"]["length"]["max"]),
    )

    magic_mimetype = fields.String(dump_only=True)

    state = fields.String(dump_only=True)

    created_at = fields.DateTime(dump_only=True)

    last_modified = fields.DateTime(dump_only=True)

    creator = fields.Nested(UserSchema, dump_only=True)

    storage = fields.Nested(StorageSchema, dump_only=True)

    _links = fields.Method("_generate_links")

    _actions = fields.Method("_generate_actions")

    def __init__(self, record=None, previous_file=None, **kwargs):
        super().__init__(**kwargs)

        self.record = record
        self.previous_file = previous_file

    @validates("name")
    def _validate_name(self, value):
        if self.record is not None:
            file = self.record.active_files.filter(File.name == value).first()

            if file is not None and (
                self.previous_file is None or self.previous_file != file
            ):
                raise ValidationError("Name is already in use.")

    @post_dump
    def _post_dump(self, data, **kwargs):
        if "creator" in data and not check_access_token_scopes("user.read"):
            del data["creator"]

        return data

    def _generate_links(self, obj):
        links = {
            "self": url_for("api.get_file", record_id=obj.record_id, file_id=obj.id),
            "record": url_for("api.get_record", id=obj.record_id),
            "download": url_for(
                "api.download_file", record_id=obj.record_id, file_id=obj.id
            ),
        }

        if self._internal:
            links["view"] = url_for(
                "records.view_file", record_id=obj.record_id, file_id=obj.id
            )
            links["edit_metadata"] = url_for(
                "records.edit_file_metadata", record_id=obj.record_id, file_id=obj.id
            )
            links["update_data"] = url_for(
                "records.add_files", id=obj.record_id, file=obj.id
            )

        return links

    def _generate_actions(self, obj):
        return {
            "delete": url_for(
                "api.delete_file", record_id=obj.record_id, file_id=obj.id
            ),
            "edit_metadata": url_for(
                "api.edit_file_metadata", record_id=obj.record_id, file_id=obj.id
            ),
            "edit_data": url_for(
                "api.edit_file_data", record_id=obj.record_id, file_id=obj.id
            ),
        }


class ChunkSchema(KadiSchema):
    """Schema to represent chunks.

    See :class:`.Chunk`.
    """

    index = fields.Integer(dump_only=True)

    size = fields.Integer(dump_only=True)

    state = fields.String(dump_only=True)


class UploadSchema(KadiSchema):
    """Schema to represent uploads.

    See :class:`.Upload`.
    """

    id = fields.String(dump_only=True)

    name = FilteredString(
        required=True,
        filters=[normalize],
        validate=Length(max=Upload.Meta.check_constraints["name"]["length"]["max"]),
    )

    size = fields.Integer(
        required=True,
        validate=Range(min=Upload.Meta.check_constraints["size"]["range"]["min"]),
    )

    description = fields.String(
        validate=Length(
            max=Upload.Meta.check_constraints["description"]["length"]["max"]
        )
    )

    mimetype = FilteredString(
        filters=[lower, normalize],
        validate=[
            Length(max=Upload.Meta.check_constraints["mimetype"]["length"]["max"]),
            validate_mimetype,
        ],
    )

    checksum = FilteredString(
        filters=[strip],
        validate=Length(max=Upload.Meta.check_constraints["checksum"]["length"]["max"]),
    )

    storage = fields.Nested(
        StorageSchema, load_default={"storage_type": const.STORAGE_TYPE_LOCAL}
    )

    upload_type = fields.String(dump_only=True)

    chunk_count = fields.Integer(dump_only=True)

    state = fields.String(dump_only=True)

    created_at = fields.DateTime(dump_only=True)

    last_modified = fields.DateTime(dump_only=True)

    creator = fields.Nested(UserSchema, dump_only=True)

    file = fields.Nested(FileSchema, dump_only=True)

    chunks = fields.Nested(ChunkSchema, many=True, dump_only=True)

    _links = fields.Method("_generate_links")

    _actions = fields.Method("_generate_actions")

    @post_dump(pass_original=True)
    def _post_dump(self, data, obj, **kwargs):
        if "creator" in data and not check_access_token_scopes("user.read"):
            del data["creator"]

        return data

    def _generate_links(self, obj):
        return {
            "status": url_for(
                "api.get_upload_status", record_id=obj.record_id, upload_id=obj.id
            ),
            "record": url_for("api.get_record", id=obj.record_id),
        }

    def _generate_actions(self, obj):
        _actions = {
            "delete": url_for(
                "api.delete_upload", record_id=obj.record_id, upload_id=obj.id
            )
        }

        if obj.upload_type == UploadType.CHUNKED:
            _actions["upload_chunk"] = url_for(
                "api.upload_chunk", record_id=obj.record_id, upload_id=obj.id
            )
            _actions["finish_upload"] = url_for(
                "api.finish_upload", record_id=obj.record_id, upload_id=obj.id
            )

        return _actions
