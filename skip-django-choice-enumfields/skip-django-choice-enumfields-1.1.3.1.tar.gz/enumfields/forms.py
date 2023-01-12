from django.forms import TypedChoiceField
from django.forms.fields import TypedMultipleChoiceField

from .enums import ChoicesEnum


__all__ = (
    'EnumChoiceField', 'EnumMultipleChoiceField'
)


class EnumChoiceFieldMixin:

    def prepare_value(self, value):
        # Widgets expect to get strings as values.
        if value is None:
            return ''
        if isinstance(value, ChoicesEnum):
            value = value.value
        return super().prepare_value(value)

    def valid_value(self, value):
        if isinstance(value, ChoicesEnum):  # Try validation using the enum value first.
            if super().valid_value(value.value):
                return True
        return super().valid_value(value)

    def to_python(self, value):
        if isinstance(value, ChoicesEnum):
            value = value.value
        return super().to_python(value)


class EnumChoiceField(EnumChoiceFieldMixin, TypedChoiceField):
    pass


class EnumMultipleChoiceField(EnumChoiceFieldMixin, TypedMultipleChoiceField):

    def prepare_value(self, value):
        if value is None:
            return ''
        super_cls = super()
        return [
            super_cls.prepare_value(v) for v in value
        ]
