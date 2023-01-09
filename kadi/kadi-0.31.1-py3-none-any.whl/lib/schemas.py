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
from flask import abort
from flask import request
from flask_babel import gettext as _
from marshmallow import fields
from marshmallow import Schema
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest

from .validation import validate_identifier as _validate_identifier
from .validation import validate_uuid
from .validation import validator
from kadi.lib.api.core import json_error_response
from kadi.lib.api.utils import check_max_content_length
from kadi.lib.api.utils import is_internal_api_request
from kadi.lib.validation import validate_mimetype as _validate_mimetype


class KadiSchema(Schema):
    """Base class for all schemas.

    :param _internal: (optional) Flag indicating whether additional data that's only
        relevant for internal use should be included when serializing objects. If not
        set, the value returned by :func:`kadi.lib.api.utils.is_internal_api_request`
        will be taken instead. Note that this flag will generally not get passed
        automatically to any nested schemas.
    """

    def __init__(self, *args, _internal=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._internal = _internal

        if self._internal is None:
            self._internal = is_internal_api_request()

    def load_or_400(self, data=None):
        """Try to deserialize the given input.

        Will try to deserialize/load the given input data using the schemas ``load``
        method. If the validation fails, automatically abort the current request with
        status code 400 and a corresponding error response as JSON.

        :param data: (optional) The input to deserialize. Defaults to the JSON body of
            the current request.
        :return: The deserialized input.
        """
        check_max_content_length()

        try:
            # Always try to parse the data, even if no correct "Content-Type" header is
            # set, which makes handling JSON data more consistent with other content
            # types and also ensures that the input stream is always consumed (even if
            # that should only matter when using the development server).
            data = data if data is not None else request.get_json(force=True)
        except BadRequest as e:
            abort(json_error_response(400, description=e.description))

        try:
            data = self.load(data)
        except ValidationError as e:
            abort(json_error_response(400, errors=e.messages))

        return data


class FilteredString(fields.String):
    """Custom string field that allows for additional filtering and validation.

    :param allow_ws_only: (optional) Flag indicating whether strings that are empty or
        only contain whitespace will be considered valid.
    :param filters: (optional) A list of filter or conversion functions that will be
        applied when deserializing the field data.
    """

    def __init__(self, *args, allow_ws_only=False, filters=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.allow_ws_only = allow_ws_only
        self.filters = filters if filters is not None else []

    def _deserialize(self, value, attr, data, **kwargs):
        output = super()._deserialize(value, attr, data, **kwargs)

        if not self.allow_ws_only and not output.strip():
            raise ValidationError(_("String must not be empty."))

        for _filter in self.filters:
            output = _filter(output)

        return output


class SortedPluck(fields.Pluck):
    """Pluck field that sorts its serialized output in case ``many`` is set."""

    def _serialize(self, nested_obj, attr, obj, **kwargs):
        output = super()._serialize(nested_obj, attr, obj, **kwargs)

        if self.many:
            return sorted(output)

        return output


class ValidateUUID:
    """Validate a UUID of a specific version in a schema field.

    :param version: (optional) The UUID version.
    """

    def __init__(self, version=4):
        self.version = version

    @validator(ValidationError)
    def __call__(self, value):
        validate_uuid(value, version=self.version)


@validator(ValidationError)
def validate_identifier(value):
    """Validate an identifier in a schema field.

    Uses :func:`kadi.lib.validation.validate_identifier`.

    :param value: The field value.
    """
    _validate_identifier(value)


@validator(ValidationError)
def validate_mimetype(value):
    """Validate a MIME type in a schema field.

    Uses :func:`kadi.lib.validation.validate_mimetype`.

    :param value: The field value.
    """
    _validate_mimetype(value)


def check_duplicate_identifier(model, identifier, exclude=None):
    """Check for a duplicate identifier in a schema.

    :param model: The model class to check the identifier of.
    :param identifier: The identifier to check.
    :param exclude: (optional) An instance of the model that should be excluded in the
        check.
    """
    obj_to_check = model.query.filter_by(identifier=identifier).first()

    if obj_to_check is not None and (exclude is None or exclude != obj_to_check):
        raise ValidationError("Identifier is already in use.")
