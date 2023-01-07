from marshmallow import EXCLUDE, Schema, fields, post_load

from soccer_sdk_utils.model.values import Values


class ValuesSchema(Schema):
    sw = fields.Str(allow_none=True, load_default=None)
    tds = fields.Str(allow_none=True, load_default=None)
    tgs = fields.Str(allow_none=True, load_default=None)
    ga = fields.Str(allow_none=True, load_default=None)
    ecnl = fields.Str(allow_none=True, load_default=None)

    class Meta:
        strict = True
        ordered = True
        model = Values
        unknown = EXCLUDE

    @post_load
    def make_values(self, data, **kwargs):
        return Values(**data)
