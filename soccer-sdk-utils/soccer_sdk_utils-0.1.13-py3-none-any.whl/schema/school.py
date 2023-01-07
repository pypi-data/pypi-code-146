from marshmallow import EXCLUDE, Schema, fields, post_load

from soccer_sdk_utils.model.school import School
from soccer_sdk_utils.schema.values import ValuesSchema


class SchoolSchema(Schema):
    id = fields.UUID(required=True)
    name = fields.Str(required=True)
    gender = fields.Str(required=True)
    ids = fields.Nested(ValuesSchema)
    urls = fields.Nested(ValuesSchema)

    class Meta:
        strict = True
        ordered = True
        model = School
        unknown = EXCLUDE

    @post_load
    def make_school(self, data, **kwargs):
        return School(**data)
