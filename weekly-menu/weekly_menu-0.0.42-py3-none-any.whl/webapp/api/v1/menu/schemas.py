import marshmallow_mongoengine as me

from marshmallow import Schema, fields, validates_schema, ValidationError

from ... import mongo
from ...models import Menu, Recipe
from ...exceptions import CannotUpdateResourceOwner
from ...schemas import BaseValidatorsMixin, DenyIdOverrideMixin


class MenuSchema(me.ModelSchema, BaseValidatorsMixin):

    # Overriding datefield
    date = fields.Date(required=True)

    class Meta:
        model = Menu

class PutMenuSchema(MenuSchema):
    pass

class PatchMenuSchema(PutMenuSchema):

    date = fields.Date(required=False)

class MenuRecipeSchema(Schema):

    recipe_id = fields.String()

