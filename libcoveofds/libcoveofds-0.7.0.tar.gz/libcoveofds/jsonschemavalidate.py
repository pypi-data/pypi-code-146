from jsonschema import FormatChecker
from jsonschema.exceptions import ValidationError as JSONSchemaExceptionsValidationError
from jsonschema.validators import Draft202012Validator

from libcoveofds.schema import OFDSSchema


class JSONSchemaValidator:
    """Validates data using the JSON Schema method"""

    def __init__(self, schema: OFDSSchema):
        self._schema = schema

    def validate(self, json_data: dict) -> list:
        """Call with data. Results are returned."""
        validator = Draft202012Validator(
            schema=self._schema.get_package_schema(), format_checker=FormatChecker()
        )
        output = []
        for e in validator.iter_errors(json_data):
            output.append(ValidationError(e, json_data, self._schema))
        return output


class ValidationError:
    """Any problems found in data are returned as an instance of this class."""

    def __init__(
        self,
        json_schema_exceptions_validation_error: JSONSchemaExceptionsValidationError,
        json_data: dict,
        schema: OFDSSchema,
    ):
        self._message = json_schema_exceptions_validation_error.message
        self._path = json_schema_exceptions_validation_error.path
        self._schema_path = json_schema_exceptions_validation_error.schema_path
        self._validator = json_schema_exceptions_validation_error.validator
        self._validator_value = json_schema_exceptions_validation_error.validator_value
        self._data_ids = schema.extract_data_ids_from_data_and_path(
            json_data, self._path
        )
        self._context = json_schema_exceptions_validation_error.context
        self._instance = json_schema_exceptions_validation_error.instance

    def json(self):
        """Return representation of this error in JSON."""
        return {
            "message": self._message,
            "path": list(self._path),
            "schema_path": list(self._schema_path),
            "validator": self._validator,
            "data_ids": self._data_ids,
            "validator_value": self._validator_value,
            "context": self._context,
            "instance": self._instance,
        }
