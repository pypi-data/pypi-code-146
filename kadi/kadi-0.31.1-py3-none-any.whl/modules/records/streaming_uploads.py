# Copyright 2021 Karlsruhe Institute of Technology
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
import hashlib

from flask import abort
from flask import json
from flask_login import current_user
from streaming_form_data.parser import StreamingFormDataParser
from streaming_form_data.targets import BaseTarget
from streaming_form_data.targets import ValueTarget

import kadi.lib.constants as const
from kadi.ext.db import db
from kadi.lib.api.core import json_error_response
from kadi.lib.conversion import parse_boolean_string
from kadi.lib.db import update_object
from kadi.lib.exceptions import KadiChecksumMismatchError
from kadi.lib.exceptions import KadiFilesizeExceededError
from kadi.lib.exceptions import KadiFilesizeMismatchError
from kadi.lib.storage.core import get_storage
from kadi.lib.storage.schemas import StorageSchema
from kadi.modules.records.api.utils import check_file_exists
from kadi.modules.records.api.utils import check_storage_compatibility
from kadi.modules.records.api.utils import check_upload_user_quota
from kadi.modules.records.models import File
from kadi.modules.records.models import Upload
from kadi.modules.records.models import UploadType
from kadi.modules.records.schemas import UploadSchema
from kadi.modules.records.uploads import complete_file_upload


class KadiValueTarget(ValueTarget):
    r"""Extended ``ValueTarget`` for use in streaming form data parsers.

    :param \*args: Additional arguments to pass to the ``ValueTarget``.
    :param on_finish: (optional) A callback that will be invoked with the parsed value
        once the parser is done processing the respective input.
    :param \**kwargs: Additional keyword arguments to pass to the ``ValueTarget``.
    """

    def __init__(self, *args, on_finish=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.index = 0
        self._on_finish = on_finish

    def to_string(self):
        """Converts a value from a ``ValueTarget`` to string.

        :return: The value as string.
        """
        return self.value.decode()

    def to_int(self):
        """Converts a value from a ``ValueTarget`` to int.

        :return: The value as int.
        """
        return int(self.to_string())

    def on_finish(self):
        if self._on_finish is not None:
            self._on_finish(self)


class StorageTarget(BaseTarget):
    r"""Extended ``BaseTarget`` for use in streaming form data parsers.

    For use in file uploads to directly store received file data in a storage.

    :param file_factory: A factory function that needs to return a tuple containing a
        storage and an open file handle.
    :param \*args: Additional arguments to pass to the ``BaseTarget``.
    :param on_data_received: (optional) A callback that will be invoked with each
        received chunk of the uploaded file.
    :param on_upload_finished: (optional) A callback that will be invoked with the final
        size of the uploaded file.
    :param \**kwargs: Additional keyword arguments to pass to the ``BaseTarget``.
    """

    def __init__(
        self,
        file_factory,
        *args,
        on_data_received=None,
        on_upload_finished=None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.index = 0
        self.file_factory = file_factory
        self._on_data_received = on_data_received
        self._on_upload_finished = on_upload_finished

    def on_start(self):
        self.storage, self.file = self.file_factory(self)

    def on_data_received(self, chunk):
        self.file.write(chunk)

        if self._on_data_received is not None:
            self._on_data_received(chunk)

    def on_finish(self):
        self.storage.close(self.file)

        if self._on_upload_finished is not None:
            self._on_upload_finished()


class StreamingContext:
    """Container class used to pass information between individual parsing stages.

    :param record: The record the streamed upload belongs to.
    """

    class _StreamingForm:
        """Container class to hold all field values while the form is being parsed."""

        def __init__(self):
            self.storage_type = const.STORAGE_TYPE_LOCAL
            self.replace_file = False
            self.checksum = None
            self.name = None
            self.size = 0

            # We do not provide default values for MIME type and description at this
            # stage, so we can detect whether a corresponding value was explicitely
            # supplied or not.
            self.mimetype = None
            self.description = None

    def __init__(self, record):
        self.record = record
        self.upload = None
        self.file = None
        self.replaced_file = None
        self.form = self._StreamingForm()
        self.file_exists = False
        self.upload_started = False
        self.calculated_checksum = hashlib.md5()
        self.targets = []


def validate_via_schema(schema_cls, field, streaming_context):
    """Validate a streamed form field via a given schema.

    :param streaming_context: The :class:`.StreamingContext`.
    :param schema_cls: The schema class to use for validation.
    :param field: The name of the field, which is used as the corresponding field in the
        schema and for storing the validated field value in the form held by the
        streaming context.
    """

    def _validate_via_schema(target):
        schema = schema_cls(only=[field])
        value = schema.load_or_400({field: target.to_string()})[field]

        setattr(streaming_context.form, field, value)

    return _validate_via_schema


def _abort_if_not_none(response):
    if response is not None:
        abort(response)


def validate_filename(streaming_context):
    """Validate the file name sent via a form field.

    :param streaming_context: The :class:`.StreamingContext`.
    """

    def _validate_filename(target):
        schema = UploadSchema(only=["name"])
        name = schema.load_or_400({"name": target.to_string()})["name"]

        streaming_context.form.name = name

        response = check_file_exists(streaming_context.record, name)

        if response is not None:
            if not streaming_context.form.replace_file:
                abort(response)

            streaming_context.file_exists = True
            replaced_file = json.loads(response.data)["file"]

            _abort_if_not_none(
                check_storage_compatibility(
                    get_storage(replaced_file["storage"]["storage_type"]),
                    get_storage(streaming_context.form.storage_type),
                )
            )

            # Store a dictionary representation of the replaced file so it can be
            # referenced again later, if necessary.
            streaming_context.replaced_file = replaced_file

    return _validate_filename


def validate_filesize(streaming_context):
    """Validate the file size sent via a form field.

    Also checks if any quotas for locally stored file uploads are exceeded.

    :param streaming_context: The :class:`.StreamingContext`.
    """

    def _validate_filesize(target):
        schema = UploadSchema(only=["size"])
        size = schema.load_or_400({"size": target.to_string()})["size"]

        streaming_context.form.size = size
        additional_size = size

        if streaming_context.replaced_file is not None:
            additional_size -= streaming_context.replaced_file["size"]

        _abort_if_not_none(check_upload_user_quota(additional_size=additional_size))

    return _validate_filesize


def file_factory(streaming_context):
    """Factory to create a storage and corresponding file.

    :param streaming_context: The :class:`.StreamingContext`.
    """

    def _file_factory(target):
        file_name = streaming_context.form.name
        replaced_file = None

        if streaming_context.replaced_file is not None:
            replaced_file = streaming_context.record.active_files.filter(
                File.name == file_name
            ).first()

        # If no MIME type was provided, take the one from the previous file or fall back
        # to its default value.
        mimetype = streaming_context.form.mimetype

        if mimetype is None:
            if replaced_file is not None:
                mimetype = replaced_file.mimetype
            else:
                mimetype = const.MIMETYPE_DEFAULT

        # If no description was provided, take the one from the previous file or fall
        # back to its default value.
        description = streaming_context.form.description

        if description is None:
            if replaced_file is not None:
                description = replaced_file.description
            else:
                description = ""

        storage = get_storage(streaming_context.form.storage_type)

        upload = Upload.create(
            creator=current_user,
            record=streaming_context.record,
            file=replaced_file,
            upload_type=UploadType.DIRECT,
            storage=storage,
            name=file_name,
            size=streaming_context.form.size,
            checksum=streaming_context.form.checksum,
            mimetype=mimetype,
            description=description,
        )

        db.session.commit()

        streaming_context.upload = upload

        filepath = storage.create_filepath(str(streaming_context.upload.id))
        storage.ensure_filepath_exists(filepath)

        streaming_context.upload_started = True

        return (storage, storage.open(filepath, "wb"))

    return _file_factory


def finish_upload(streaming_context):
    """Updates the remaining information of the file after the upload finished.

    Uses :func:`complete_file_upload` to complete the file upload process.

    :param streaming_context: The :class:`.StreamingContext`.
    """

    def _finish_upload():
        upload = streaming_context.upload
        checksum = upload.checksum or streaming_context.calculated_checksum.hexdigest()

        update_object(
            upload,
            calculated_checksum=streaming_context.calculated_checksum.hexdigest(),
            checksum=checksum,
        )

        streaming_context.upload_started = False

        try:
            streaming_context.file = complete_file_upload(streaming_context.upload)

            if streaming_context.file is None:
                abort(json_error_response(400, "Error creating or updating file."))

        except (
            KadiFilesizeExceededError,
            KadiFilesizeMismatchError,
            KadiChecksumMismatchError,
        ) as e:
            abort(json_error_response(400, description=str(e)))

    return _finish_upload


def check_field(on_field_received, streaming_context):
    """Check if all form fields that are required so far have been received.

    If not, the request is aborted with a status code of 400.

    :param on_field_received: Function that is be called when the field is checked
        successfully.
    :param streaming_context: The :class:`.StreamingContext`.
    """

    def _check_field(target):
        for i in range(0, target.index):
            target_info = streaming_context.targets[i]

            # Check if all fields that are required so far have been received.
            if target_info["required"] and not target_info["received"]:
                abort(
                    json_error_response(
                        400,
                        errors={
                            target_info["name"]: ["Missing data for required field."]
                        },
                    )
                )

        streaming_context.targets[target.index]["received"] = True
        return on_field_received(target)

    return _check_field


def check_required_fields_received(streaming_context):
    """Check if all required fields are received.

    :param streaming_context: The :class:`.StreamingContext`.
    :return: An error response or ``None`` if all required fields are received.
    """
    for target_info in streaming_context.targets:
        if target_info["required"] and not target_info["received"]:
            return json_error_response(
                400, errors={target_info["name"]: ["Missing data for required field."]}
            )


def create_streaming_parser(headers, streaming_context):
    """Creates a `StreamingFormDataParser` suitable to handle direct file uploads.

    Note that during the file streaming one or more database commits are issued.

    :param headers: The HTTP-headers of the request the parser is used in.
    :param streaming_context: The :class:`.StreamingContext`.
    """

    def _on_replace_file_received(target):
        streaming_context.form.replace_file = parse_boolean_string(target.to_string())

    def _on_data_received(chunk):
        streaming_context.calculated_checksum.update(chunk)

    parser = StreamingFormDataParser(headers=headers)

    def _register_target(name, target, required):
        parser.register(name, target)

        target.index = len(streaming_context.targets)
        streaming_context.targets.append(
            {"name": name, "required": required, "received": False}
        )

    # Note that the order of registration matters.
    _register_target(
        "storage_type",
        KadiValueTarget(
            on_finish=check_field(
                validate_via_schema(StorageSchema, "storage_type", streaming_context),
                streaming_context,
            )
        ),
        required=False,
    )
    _register_target(
        "replace_file",
        KadiValueTarget(
            on_finish=check_field(_on_replace_file_received, streaming_context)
        ),
        required=False,
    )
    _register_target(
        "mimetype",
        KadiValueTarget(
            on_finish=check_field(
                validate_via_schema(UploadSchema, "mimetype", streaming_context),
                streaming_context,
            )
        ),
        required=False,
    )
    _register_target(
        "checksum",
        KadiValueTarget(
            on_finish=check_field(
                validate_via_schema(UploadSchema, "checksum", streaming_context),
                streaming_context,
            )
        ),
        required=False,
    )
    _register_target(
        "description",
        KadiValueTarget(
            on_finish=check_field(
                validate_via_schema(UploadSchema, "description", streaming_context),
                streaming_context,
            )
        ),
        required=False,
    )
    _register_target(
        "name",
        KadiValueTarget(
            on_finish=check_field(
                validate_filename(streaming_context), streaming_context
            )
        ),
        required=True,
    )
    _register_target(
        "size",
        KadiValueTarget(
            on_finish=check_field(
                validate_filesize(streaming_context), streaming_context
            )
        ),
        required=True,
    )
    _register_target(
        "blob",
        StorageTarget(
            check_field(file_factory(streaming_context), streaming_context),
            on_data_received=_on_data_received,
            on_upload_finished=finish_upload(streaming_context),
        ),
        required=True,
    )

    return parser
