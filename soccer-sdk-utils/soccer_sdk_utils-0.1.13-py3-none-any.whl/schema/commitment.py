from marshmallow import EXCLUDE, Schema, fields, post_load

from soccer_sdk_utils.model.commitment import Commitment
from soccer_sdk_utils.schema.values import ValuesSchema


class CommitmentSchema(Schema):
    school = fields.Str(allow_none=True, load_default=None)
    urls = fields.Nested(ValuesSchema)

    class Meta:
        strict = True
        ordered = True
        model = Commitment
        unknown = EXCLUDE

    @post_load
    def make_commitment(self, data, **kwargs):
        return Commitment(**data)
