from marshmallow import fields, post_load

from cryptowatch.resources.base import BaseResource, BaseSchema


class AllowanceSchema(BaseSchema):
    cost = fields.Integer()
    remaining = fields.Integer()
    remainingPaid = fields.Integer(load_default=0)
    upgrade = fields.Str(load_default="")
    account = fields.Str(load_default="")

    @post_load
    def make_resource(self, data, **kwargs):
        return BaseResource(_name="Allowance", _display_key="remaining", **data)
