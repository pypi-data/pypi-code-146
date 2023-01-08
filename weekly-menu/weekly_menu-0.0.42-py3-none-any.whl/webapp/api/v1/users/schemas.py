import marshmallow_mongoengine as me

from marshmallow import Schema, fields, validates_schema, ValidationError

from ... import mongo
from ...models import User, RecipeIngredient
from ...exceptions import CannotUpdateResourceOwner
from ...schemas import BaseValidatorsMixin, DenyIdOverrideMixin

class UserSchema(me.ModelSchema, BaseValidatorsMixin):

    class Meta:
        model = User