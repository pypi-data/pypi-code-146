from marshmallow import Schema, fields


class CategoryAttrsSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class CategorySchema(Schema):
    category = fields.Nested(CategoryAttrsSchema())
