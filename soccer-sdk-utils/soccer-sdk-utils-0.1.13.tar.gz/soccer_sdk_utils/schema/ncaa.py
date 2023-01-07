from marshmallow import EXCLUDE, Schema, fields, post_load

from soccer_sdk_utils.model.ncaa import School


class SchoolSchema(Schema):
    name = fields.Str(required=True)
    conference = fields.Str(required=True)
    private = fields.Bool(required=True)
    hbcu = fields.Bool(required=True)
    state = fields.Str(required=True)

    class Meta:
        strict = True
        ordered = True
        model = School
        unknown = EXCLUDE

    @post_load
    def make_school(self, data, **kwargs):
        return School(**data)
