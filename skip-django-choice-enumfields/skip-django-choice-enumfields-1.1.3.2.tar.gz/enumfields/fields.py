from enum import Enum

import django
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields import BLANK_CHOICE_DASH
from django.db.models.signals import post_save
from django.utils.functional import cached_property
from django.utils.module_loading import import_string
from django.utils.translation import gettext

from .enums import ChoicesEnum, Choice
from .forms import EnumChoiceField


class CastOnAssignDescriptor:
    """
    A property descriptor which ensures that `field.to_python()` is called on _every_ assignment to the field.

    This used to be provided by the `django.db.models.subclassing.Creator` class, which in turn
    was used by the deprecated-in-Django-1.10 `SubfieldBase` class, hence the reimplementation here.
    """

    def __init__(self, field):
        self.field = field

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return obj.__dict__[self.field.name]

    def __set__(self, obj, value):
        initial_field_name = self.field.get_initial_cache_name()
        python_value = self.field.to_python(value)
        obj.__dict__.setdefault(initial_field_name, python_value)
        obj.__dict__[self.field.name] = python_value


class EnumFieldValidationMixin:

    def get_initial_cache_name(self):
        return '_initial_{}'.format(self.name)

    def _validate_next_value(self, value, model_instance):
        initial_field_name = self.get_initial_cache_name()
        previous_choice = getattr(model_instance, initial_field_name, None)
        if (
            previous_choice is not None
            and value != previous_choice
            and previous_choice.next is not None
            and value.name not in previous_choice.next
        ):
            raise ValidationError(
                gettext(
                    'Transition from current "{}" choice to "{}" choice is not allowed'
                ).format(
                    previous_choice.name, value.name
                )
            )

    def _validate_inital_value(self, value, model_instance):
        if model_instance._state.adding and value and not value.initial:
            initial_choices = {
                choice for choice in self.enum if choice.initial
            }
            raise ValidationError(
                gettext('Allowed choices are {}.').format(
                    ', '.join(
                        ('{} ({})'.format(*(choice.name, choice.value))
                         for choice in initial_choices)
                    )
                )
            )


def deconstruct_enum(enum):
    name, enum_base, enum_type, choices = enum.deconstruct_cls()
    if not enum_type and not choices:
        return enum_base

    return {
        'name': name,
        'base': enum_base,
        'type': enum_type,
        'choices': choices
    }


def construct_enum(enum):
    if isinstance(enum, str):
        return import_string(enum)
    elif isinstance(enum, dict):
        enum_type = None
        if enum['type']:
            enum_type = import_string(enum['type']) if isinstance(enum['type'], str) else enum['type']
        return import_string(enum['base'])(enum['name'], {
            name: Choice(**choice) for name, choice in enum['choices'].items()
        }, type=enum_type)
    else:
        return enum


class EnumFieldMixin(EnumFieldValidationMixin):

    def __init__(self, enum, **options):
        self.enum = construct_enum(enum)

        if 'choices' not in options:
            options['choices'] = self.enum.choices

        super().__init__(**options)

    def refresh_from_db(self, instance):
        initial_field_name = self.get_initial_cache_name()
        instance.__dict__[initial_field_name] = getattr(instance, self.name)

    def contribute_to_class(self, cls, name):
        super().contribute_to_class(cls, name)

        def update_initial_field(instance, update_fields, **kwargs):
            if update_fields is None or self.name in update_fields:
                self.refresh_from_db(instance)

        tmp_refresh_from_db = cls.refresh_from_db
        def refresh_from_db(instance, using=None, fields=None, *args, **kwargs):
            returned_value = tmp_refresh_from_db(instance, using=using, fields=fields, *args, **kwargs)
            if not fields or self.name in fields:
                self.refresh_from_db(instance)
            return returned_value
        cls.refresh_from_db = refresh_from_db

        setattr(cls, name, CastOnAssignDescriptor(self))
        post_save.connect(update_initial_field, sender=cls, weak=False)

    def to_python(self, value):
        if isinstance(value, self.enum):
            return value
        else:
            value = super().to_python(value)
            if value in [None, '']:
                return None

            try:
                return self.enum(value)
            except ValueError:
                raise ValidationError(
                    '%s is not a valid value for enum %s' % (value, self.enum),
                    code='invalid_enum_value'
                )

    def get_prep_value(self, value):
        if value is None:
            return None
        if isinstance(value, self.enum):  # Already the correct type -- fast path
            return value.value
        return self.enum(value).value

    def from_db_value(self, value, expression, connection, *args):
        return self.to_python(value)

    def value_to_string(self, obj):
        """
        This method is needed to support proper serialization. While its name is value_to_string()
        the real meaning of the method is to convert the value to some serializable format.
        Since most of the enum values are strings or integers we WILL NOT convert it to string
        to enable integers to be serialized natively.
        """
        if django.VERSION >= (2, 0):
            value = self.value_from_object(obj)
        else:
            value = self._get_val_from_obj(obj)
        return value.value if value else None

    def get_default(self):
        if self.has_default():
            if self.default is None:
                return None

            if isinstance(self.default, Enum):
                return self.default

            return self.enum(self.default)

        return super().get_default()

    def deconstruct(self):
        name, path, args, keywords = super().deconstruct()
        keywords['enum'] = deconstruct_enum(self.enum)
        keywords.pop('choices', None)
        if 'default' in keywords:
            if hasattr(keywords['default'], 'value'):
                keywords['default'] = keywords['default'].value

        return name, path, args, keywords

    def get_choices(self, include_blank=True, blank_choice=BLANK_CHOICE_DASH):
        # Force enum fields' options to use the `value` of the enumeration
        # member as the `value` of SelectFields and similar.
        return [
            (i.value if isinstance(i, Enum) else i, display)
            for (i, display)
            in super().get_choices(include_blank, blank_choice)
        ]

    def formfield(self, form_class=None, choices_form_class=None, **kwargs):
        if not choices_form_class:
            choices_form_class = EnumChoiceField

        return super().formfield(
            form_class=form_class,
            choices_form_class=choices_form_class,
            **kwargs
        )

    def validate(self, value, model_instance):
        self._validate_inital_value(value, model_instance)
        self._validate_next_value(value, model_instance)
        super().validate(value, model_instance)


class CharEnumField(EnumFieldMixin, models.CharField):

    def __init__(self, enum, **kwargs):
        enum = construct_enum(enum)
        kwargs.setdefault('max_length', max(max([len(str(choice.value)) for choice in enum]), 10))
        super().__init__(enum, **kwargs)
        self.validators = []


class IntegerEnumField(EnumFieldMixin, models.IntegerField):

    @cached_property
    def validators(self):
        # Skip IntegerField validators, since they will fail with
        #   TypeError: unorderable types: TheEnum() < int()
        # when used database reports min_value or max_value from
        # connection.ops.integer_field_range method.
        return super(models.IntegerField, self).validators

    def get_prep_value(self, value):
        if value is None:
            return None

        if isinstance(value, Enum):
            return value.value

        try:
            return int(value)
        except ValueError:
            return self.to_python(value).value


class EnumSubFieldMixin(EnumFieldValidationMixin):

    def __init__(self, parent_field_name, enum, **options):
        self.parent_field_name = parent_field_name
        super().__init__(enum, **options)

    def _get_supvalue(self, model_instance):
        return getattr(model_instance, self.parent_field_name)

    def _get_all_parent_values(self):
        parents = set()
        for choice in self.enum:
            parents |= set(choice.parents)
        return parents

    def _get_all_parent_choices(self, supvalue):
        return {
            choice for choice in self.enum if supvalue in choice.parents
        }

    def _validate_parent_value_empty(self, value, supvalue):
        if supvalue not in self._get_all_parent_values() and value is not None:
            raise ValidationError(gettext('Value must be empty'))

    def _validate_parent_value(self, value, supvalue):
        allowed_values = self._get_all_parent_choices(supvalue)
        if allowed_values and value not in allowed_values:
            raise ValidationError(gettext('Allowed choices are {}.').format(
                ', '.join(('{} ({})'.format(*(val.label, val)) for val in allowed_values))
            ))

    def validate(self, value, model_instance):
        parent_field_value = self._get_supvalue(model_instance)
        if self._get_all_parent_choices(parent_field_value):
            self._validate_parent_value_empty(value, parent_field_value)
            self._validate_parent_value(value, parent_field_value)
        self._validate_inital_value(value, model_instance)
        self._validate_next_value(value, model_instance)
        super().validate(value, model_instance)

    def deconstruct(self):
        name, path, args, keywords = super().deconstruct()
        keywords['parent_field_name'] = self.parent_field_name
        return name, path, args, keywords


class CharEnumSubField(EnumSubFieldMixin, CharEnumField):
    pass


class IntegerEnumSubField(EnumSubFieldMixin, IntegerEnumField):
    pass
