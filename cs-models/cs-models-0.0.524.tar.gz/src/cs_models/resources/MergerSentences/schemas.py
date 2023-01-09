from marshmallow import (
    Schema,
    fields,
    validate,
)


class MergerSentenceResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    merger_id = fields.Integer(required=True)
    text = fields.String(required=True, validate=not_blank)
    updated_at = fields.DateTime()
