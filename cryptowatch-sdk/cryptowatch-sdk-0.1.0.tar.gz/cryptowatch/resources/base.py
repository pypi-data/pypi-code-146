import re

from marshmallow import EXCLUDE, Schema


CAMEL_CASE_RE = re.compile(r"(?<!^)(?=[A-Z])")


class BaseSchema(Schema):
    class Meta:
        unknown = EXCLUDE


class BaseResource:
    def __init__(self, *args, **kwargs):
        # Display options for repr
        self._name = kwargs.pop("_name", "Resource")
        self._display_key = kwargs.pop("_display_key", "")

        # Data from schema
        for k, v in kwargs.items():
            # Convert any camel case variables to snake
            k = CAMEL_CASE_RE.sub("_", k).lower()
            setattr(self, k, v)

    def __repr__(self):
        return "<{}({})>".format(self._name, getattr(self, self._display_key, ""))
