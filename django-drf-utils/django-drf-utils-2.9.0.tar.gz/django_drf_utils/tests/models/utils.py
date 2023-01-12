from typing import Type

from django.core.exceptions import ValidationError
from django.db import models


# TODO contribute to django / pytest
def validate_field(
    model: Type[models.Model], field_name: str, field_value, expected: bool
):
    model_instance = model(**{field_name: field_value})
    validation_errors = get_validation_errors(model_instance)
    if expected:
        # field should NOT raise an error
        assert (  # nosec
            field_name not in validation_errors
        ), f"'{field_name}' should NOT be in '{validation_errors}'."
    else:
        # field should raise an error
        assert (  # nosec
            field_name in validation_errors
        ), f"'{field_name}' should be in '{validation_errors}'."


# TODO contribute to django / pytest
def get_validation_errors(model_object: models.Model):
    try:
        model_object.full_clean()
        # if we reach this point, no ValidationError was raised
        return set()
    except ValidationError as e:
        return set(e.message_dict.keys())
