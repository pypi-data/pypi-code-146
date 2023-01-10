from rest_framework.exceptions import PermissionDenied


class CreateOrUpdateOnlyMixin:
    """
    A mixin for ModelSerializer that allows fields that can be sent only in create methods or fields that only can be
    sent in update methods.
    """

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        if self.instance:
            create_only_fields = getattr(self.Meta, 'create_only_fields', tuple())
            for field in create_only_fields:
                ret.pop(field, None)
        else:
            update_only_fields = getattr(self.Meta, 'update_only_fields', tuple())
            for field in update_only_fields:
                ret.pop(field, None)
        return ret

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        if hasattr(self.Meta, 'create_only_fields') and self.instance:
            for field in self.Meta.create_only_fields:
                extra_kwargs.setdefault(field, {}).update({'required': False})
        return extra_kwargs


class PermissionForFieldMixin:
    """
    A mixin for ModelSerializer that allows set permissions for certain fields in your serializer that are related to
    model instances.
    """

    @property
    def permissions_for_field(self):
        permissions_for_field = getattr(self.Meta, 'permissions_for_field', dict())

        list_fields = list(permissions_for_field.keys())

        for fields in list_fields:
            if isinstance(fields, str):
                permissions_for_field[(fields,)] = permissions_for_field.pop(fields)

        return permissions_for_field

    def get_permissions_for_field(self, field):
        for fields, permissions in self.permissions_for_field.items():
            if field in fields:
                return permissions

    def check_field_permission(self, field_name, obj):
        request = self.context.get('request')
        view = self.context.get('view')
        for permission in [permission() for permission in self.get_permissions_for_field(field_name)]:
            if not permission.has_object_permission(request, view, obj):
                raise PermissionDenied(
                    detail=f'You do not have permission to use `{field_name}` with id `{obj.id}`.'
                )

    def validate(self, attrs):
        for fields in self.permissions_for_field.keys():
            [self.check_field_permission(field, attrs[field]) for field in fields if field in attrs]
        return attrs


class DynamicModelFieldsMixin:
    """
    A mixin for ModelSerializer that takes an additional `fields` argument that controls which fields should be
    displayed.

    The field_type_mapping attribute is a dictionary that maps field types to attribute names in the Meta class of the
    serializer, where:
        - keys: The symbol which will be in the fields query param.
            example: https://example.com/fields=@min
        - values: Field's name defined in serializer Meta.
            example: min_fields: ('id', 'name', 'test')

    example:
        class Serializer(DynamicModelFieldsMixin, ModelSerializer):
            class Meta:
                model = Model
                min_fields = ('id', 'test')
                default_fields = ('id', 'name', 'url')

    There are three default field's types which return certain fields that are defined in ModelSerializer, they are:
    - @min - only the `basic` object's fields
    - @default - only the default object's fields
    - @all - all object's fields

    You can modify this fields as you want.
    """
    field_type_mapping = {'@min': 'min_fields', '@default': 'default_fields'}
    all_symbol = '@all'

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:

            if self.all_symbol in fields:
                return

            for field in fields:
                if field in self.field_type_mapping:
                    field_values = getattr(self.Meta, self.field_type_mapping[field], tuple())
                    fields += field_values

            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
