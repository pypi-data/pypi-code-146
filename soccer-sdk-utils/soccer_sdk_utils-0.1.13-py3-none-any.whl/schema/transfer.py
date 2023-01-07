from marshmallow import EXCLUDE, Schema, fields, post_load

from soccer_sdk_utils.model.transfer import Transfer


class TransferSchema(Schema):
    name = fields.Str(allow_none=False, load_default="")
    url = fields.Str(allow_none=True, load_default=None)
    position = fields.Str(allow_none=True, load_default=None)
    former_school_name = fields.Str(allow_none=True, load_default=None)
    former_school_url = fields.Str(allow_none=True, load_default=None)
    new_school_name = fields.Str(allow_none=True, load_default=None)
    new_school_url = fields.Str(allow_none=True, load_default=None)

    class Meta:
        strict = True
        ordered = True
        model = Transfer
        unknown = EXCLUDE

    @post_load
    def make_transfer(self, data, **kwargs):
        return Transfer(**data)
