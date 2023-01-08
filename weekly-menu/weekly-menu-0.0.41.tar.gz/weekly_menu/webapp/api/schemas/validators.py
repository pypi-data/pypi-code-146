from marshmallow import fields, Schema, validates_schema, ValidationError

from ..exceptions import CannotUpdateResourceOwner, CannotSetResourceId, CannotSetOrChangeCreationUpdateTime


class OwnerNotRequiredMixin:
    # Owner is not required because it will be attached server side based on token
    owner = fields.String(required=False)


class CheckUnknownFieldsMixin:
    @validates_schema(pass_original=True)
    def check_unknown_fields(self, data, original_data):
        unknown = set(original_data) - set(self.fields)
        if unknown:
            raise ValidationError('Unknown field', unknown)


class DenyOwnerOverrideMixin:
    @validates_schema
    def check_owner_overwrite(self, data):
        if 'owner' in data:
            raise CannotUpdateResourceOwner('Can\'t overwrite owner property')


class DenyIdOverrideMixin:
    @validates_schema
    def id_not_allowed(self, data):
        if 'id' in data:
            raise CannotSetResourceId()


class DenyInsertUpdateDateTime:
    @validates_schema
    def insert_update_time_not_allowed(self, data):
        if 'insert_timestamp' in data \
                or 'update_timestamp' in data:
            raise CannotSetOrChangeCreationUpdateTime()


class BaseValidatorsMixin(OwnerNotRequiredMixin, DenyOwnerOverrideMixin, DenyInsertUpdateDateTime):
    _id = fields.String(required=False)

    insert_timestamp = fields.Int(required=False)
    update_timestamp = fields.Int(required=False)
