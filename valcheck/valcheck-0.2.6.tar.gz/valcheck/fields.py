from typing import Any, Callable, Iterable, List, Optional

from valcheck.models import Error
from valcheck.utils import (
    is_instance_of_any,
    is_iterable,
    is_valid_datetime_string,
    is_valid_email_id,
    is_valid_json_string,
    is_valid_string,
    is_valid_uuid_string,
    set_as_empty,
)


class BaseField:
    def __init__(
            self,
            *,
            required: Optional[bool] = True,
            nullable: Optional[bool] = False,
            default_func: Optional[Callable] = None,
            validators: Optional[List[Callable]] = None,
            error: Optional[Error] = None,
        ) -> None:
        """
        Parameters:
            - required (bool): True if the field is required, else False. Default: True
            - nullable (bool): True if the field is nullable, else False. Default: False
            - default_func (callable): Callable that returns the default value to set for the field
            if `required=False` and the field is missing.
            - validators (list of callables): List of callables that each return a boolean.
            The callable returns True if validation is successful, else False.
            - error (Error instance): Instance of type `valcheck.models.Error`.
        """
        assert isinstance(required, bool), "Param `required` must be of type 'bool'"
        assert isinstance(nullable, bool), "Param `nullable` must be of type 'bool'"
        assert default_func is None or callable(default_func), (
            "Param `default_func` must be a callable that returns the default value if the field is missing when `required=False`"
        )
        assert validators is None or isinstance(validators, list), "Param `validators` must be of type 'list'"
        if isinstance(validators, list):
            for validator in validators:
                assert callable(validator), "Param `validators` must be a list of callables"
        assert error is None or isinstance(error, Error), "Param `error` must be of type `valcheck.models.Error`"

        self._field_value = set_as_empty()
        self.required = required
        self.nullable = nullable
        self.default_func = default_func
        self.validators = validators or []
        self.error = error or Error()

    @property
    def field_value(self) -> Any:
        return self._field_value

    @field_value.setter
    def field_value(self, value: Any) -> None:
        self._field_value = value

    def can_be_set_to_null(self) -> bool:
        return self.nullable and self.field_value is None

    def has_valid_custom_validators(self) -> bool:
        if not self.validators:
            return True
        validator_return_values = [validator(self.field_value) for validator in self.validators]
        for return_value in validator_return_values:
            assert isinstance(return_value, bool), (
                f"Expected the return type of `validators` to be 'bool', but got '{type(return_value).__name__}'"
            )
        return all(validator_return_values)

    def is_valid(self) -> bool:
        """Needs to be implemented by all child classes of the `BaseField` class"""
        raise NotImplementedError()


class AnyField(BaseField):
    def __init__(self, **kwargs: Any) -> None:
        super(AnyField, self).__init__(**kwargs)

    def is_valid(self) -> bool:
        if super().can_be_set_to_null():
            return True
        return super().has_valid_custom_validators()


class BooleanField(BaseField):
    def __init__(self, **kwargs: Any) -> None:
        super(BooleanField, self).__init__(**kwargs)

    def is_valid(self) -> bool:
        if super().can_be_set_to_null():
            return True
        return isinstance(self.field_value, bool) and super().has_valid_custom_validators()


class StringField(BaseField):
    def __init__(self, *, allow_empty: Optional[bool] = True, **kwargs: Any) -> None:
        self.allow_empty = allow_empty
        super(StringField, self).__init__(**kwargs)

    def is_valid(self) -> bool:
        if super().can_be_set_to_null():
            return True
        return (
            is_valid_string(
                value=self.field_value,
                allow_empty=self.allow_empty,
            )
            and super().has_valid_custom_validators()
        )


class JsonStringField(StringField):
    def __init__(self, **kwargs: Any) -> None:
        super(JsonStringField, self).__init__(**kwargs)

    def is_valid(self) -> bool:
        if super().can_be_set_to_null():
            return True
        return (
            super().is_valid()
            and is_valid_json_string(self.field_value)
        )


class EmailIdField(StringField):
    def __init__(self, **kwargs: Any) -> None:
        super(EmailIdField, self).__init__(**kwargs)

    def is_valid(self) -> bool:
        if super().can_be_set_to_null():
            return True
        return (
            super().is_valid()
            and is_valid_email_id(self.field_value)
        )


class UuidStringField(StringField):
    def __init__(self, **kwargs: Any) -> None:
        super(UuidStringField, self).__init__(**kwargs)

    def is_valid(self) -> bool:
        if super().can_be_set_to_null():
            return True
        return (
            super().is_valid()
            and is_valid_uuid_string(self.field_value)
        )


class DateStringField(StringField):
    def __init__(self, *, format_: Optional[str] = "%Y-%m-%d", **kwargs: Any) -> None:
        self.format_ = format_
        super(DateStringField, self).__init__(**kwargs)

    def is_valid(self) -> bool:
        if super().can_be_set_to_null():
            return True
        return (
            super().is_valid()
            and is_valid_datetime_string(self.field_value, self.format_)
        )


class DatetimeStringField(StringField):
    def __init__(self, *, format_: Optional[str] = "%Y-%m-%d %H:%M:%S", **kwargs: Any) -> None:
        self.format_ = format_
        super(DatetimeStringField, self).__init__(**kwargs)

    def is_valid(self) -> bool:
        if super().can_be_set_to_null():
            return True
        return (
            super().is_valid()
            and is_valid_datetime_string(self.field_value, self.format_)
        )


class ChoiceField(BaseField):
    def __init__(self, *, choices: Iterable[Any], **kwargs: Any) -> None:
        assert is_iterable(choices), "Param `choices` must be an iterable"
        self.choices = choices
        super(ChoiceField, self).__init__(**kwargs)

    def is_valid(self) -> bool:
        if super().can_be_set_to_null():
            return True
        return self.field_value in self.choices and super().has_valid_custom_validators()


class IntegerField(BaseField):
    def __init__(self, **kwargs: Any) -> None:
        super(IntegerField, self).__init__(**kwargs)

    def is_valid(self) -> bool:
        if super().can_be_set_to_null():
            return True
        return isinstance(self.field_value, int) and super().has_valid_custom_validators()


class PositiveIntegerField(IntegerField):
    def __init__(self, **kwargs: Any) -> None:
        super(PositiveIntegerField, self).__init__(**kwargs)

    def is_valid(self) -> bool:
        if super().can_be_set_to_null():
            return True
        return (
            super().is_valid()
            and self.field_value > 0
        )


class NegativeIntegerField(IntegerField):
    def __init__(self, **kwargs: Any) -> None:
        super(NegativeIntegerField, self).__init__(**kwargs)

    def is_valid(self) -> bool:
        if super().can_be_set_to_null():
            return True
        return (
            super().is_valid()
            and self.field_value < 0
        )


class FloatField(BaseField):
    def __init__(self, **kwargs: Any) -> None:
        super(FloatField, self).__init__(**kwargs)

    def is_valid(self) -> bool:
        if super().can_be_set_to_null():
            return True
        return isinstance(self.field_value, float) and super().has_valid_custom_validators()


class NumberField(BaseField):
    def __init__(self, **kwargs: Any) -> None:
        super(NumberField, self).__init__(**kwargs)

    def is_valid(self) -> bool:
        if super().can_be_set_to_null():
            return True
        return is_instance_of_any(obj=self.field_value, types=[int, float]) and super().has_valid_custom_validators()


class DictionaryField(BaseField):
    def __init__(self, **kwargs: Any) -> None:
        super(DictionaryField, self).__init__(**kwargs)

    def is_valid(self) -> bool:
        if super().can_be_set_to_null():
            return True
        return isinstance(self.field_value, dict) and super().has_valid_custom_validators()


class ListField(BaseField):
    def __init__(self, **kwargs: Any) -> None:
        super(ListField, self).__init__(**kwargs)

    def is_valid(self) -> bool:
        if super().can_be_set_to_null():
            return True
        return isinstance(self.field_value, list) and super().has_valid_custom_validators()


class MultiChoiceField(ListField):
    def __init__(self, *, choices: Iterable[Any], **kwargs: Any) -> None:
        assert is_iterable(choices), "Param `choices` must be an iterable"
        self.choices = choices
        super(MultiChoiceField, self).__init__(**kwargs)

    def is_valid(self) -> bool:
        if super().can_be_set_to_null():
            return True
        return (
            super().is_valid()
            and all([item in self.choices for item in self.field_value])
        )


class BytesField(BaseField):
    def __init__(self, **kwargs: Any) -> None:
        super(BytesField, self).__init__(**kwargs)

    def is_valid(self) -> bool:
        if super().can_be_set_to_null():
            return True
        return isinstance(self.field_value, bytes) and super().has_valid_custom_validators()

