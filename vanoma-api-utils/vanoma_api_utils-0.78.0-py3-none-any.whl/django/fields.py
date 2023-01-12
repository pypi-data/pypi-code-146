import uuid
from typing import Any
from django.db import models
from .validators import validate_number
from ..misc import get_shortuuid


class StringField(models.CharField):
    """
    A field used to store a reasonable-sized string. It's a shortcut
    to always having to declare max_length on CharField. Value stored
    in this field should be smaller that what TextField can store but
    also bigger than what ShortStringField (see below) can store.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["max_length"] = 150
        super().__init__(*args, **kwargs)


class ShortStringField(models.CharField):
    """
    A general purpose field used to store typically single-word type of
    strings. Examples include a primary key value, status and type values, etc.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["max_length"] = 40
        super().__init__(*args, **kwargs)


class LegacyPrimaryKeyField(ShortStringField):
    """
    Primary key used in auth-api and payment-api services. Because both services
    are used in older delivery services, we have to keep the max length to avoid
    truncating existing rows' primary keys.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["editable"] = False
        kwargs["primary_key"] = True
        kwargs["default"] = uuid.uuid4
        super().__init__(*args, **kwargs)


class PrimaryKeyField(models.CharField):
    """
    Notice that we are using a shortened version of UUID. This is so that the
    primary key can be used on URL and UUID, although safe, are user-friendly
    in a URL. Among the defaults, max_length is set to 22 as shortuuid generates
    22-character key.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["editable"] = False
        kwargs["primary_key"] = True
        kwargs["max_length"] = 22
        kwargs["default"] = get_shortuuid
        super().__init__(*args, **kwargs)


class ReferenceKeyField(models.CharField):
    """
    A field that references PrimaryKeyField from another service. In this case
    using models.ForeignKey is not applicable. The convenience of this field
    to set a max length.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["max_length"] = 22  # Shortuuid are 22 max
        super().__init__(*args, **kwargs)


class PhoneNumberField(models.CharField):
    """
    Field that is used to store phone numbers. It adds validation using Google's
    libphonenumber and sets max length to 15 as suggested by this single -
    https://stackoverflow.com/a/4729239
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["max_length"] = 15
        kwargs["validators"] = [validate_number]
        super().__init__(*args, **kwargs)
