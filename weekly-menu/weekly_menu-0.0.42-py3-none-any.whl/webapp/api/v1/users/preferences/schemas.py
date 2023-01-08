import marshmallow_mongoengine as me

from marshmallow import Schema, fields, validates_schema, ValidationError

from .... import mongo
from ....models import UserPreferences, RecipeIngredient
from ....exceptions import CannotUpdateResourceOwner
from ....schemas import BaseValidatorsMixin, DenyIdOverrideMixin

class UserPreferencesSchema(me.ModelSchema, BaseValidatorsMixin):
    class Meta:
        model = UserPreferences

class PutUserPreferencesSchema(UserPreferencesSchema):
    pass

class PatchUserPreferencesSchema(UserPreferencesSchema):
    pass