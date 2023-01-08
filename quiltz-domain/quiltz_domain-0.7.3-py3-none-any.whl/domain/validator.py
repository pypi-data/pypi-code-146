from .email import is_valid_email_address
from .results import Success, Failure
from inspect import signature


class Parameters(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self

    def with_attribute(self, parameter_name, value):
        return Parameters({**{parameter_name: value}, **self})


class ValidationResults:
    def __init__(self):
        self.valid_parameters = Parameters()

    def add(self, parameter_name, value):
        self.valid_parameters = self.valid_parameters.with_attribute(parameter_name, value)

    def map(self, fn):
        return fn(self.valid_parameters)


class Validator:
    def __init__(self, parameter_name, value):
        self.parameter_name = parameter_name
        self.value = value


class PresenceOf(Validator):
    def validate(self, results):
        if self.value is None:
            return Failure(message="{} is missing".format(self.parameter_name))
        results.add(self.parameter_name, self.value)
        return Success()


class OptionalityOf(Validator):
    def validate(self, results):
        results.add(self.parameter_name, self.value)
        return Success()

class OptionalValidation:
    def __init__(self, validation: Validator):
        self._optional_validation = validation
    def validate(self, results):
        if self._optional_validation.value == None:
            results.add(self._optional_validation.parameter_name, None)
            return Success()
        return self._optional_validation.validate(results)

class MaxLengthOf(Validator):
    def __init__(self, parameter, value, max):
        super().__init__(parameter, value)
        self.max = max

    def validate(self, results):
        if len(self.value) > self.max: 
            return Failure(message="{} is too long".format(self.parameter_name))
        results.add(self.parameter_name, self.value)
        return Success()


class IsBetween(Validator):
    def __init__(self, parameter, value, lower_bound, upper_bound):
        super().__init__(parameter, value)
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def validate(self, results):
        return (int_from_string(self.value, self.parameter_name)
                .map(self._is_between)
                .do(lambda result: results.add(self.parameter_name, result.value)))

    def _is_between(self, result):
        if self.lower_bound <= result.value <= self.upper_bound:
            return Success(value=result.value) 
        return Failure(message='{} should be between {} and {}'.format(self.parameter_name, self.lower_bound, self.upper_bound))


class ConversionOf(Validator):
    def __init__(self, parameter, value, type_to_convert_to):
        super().__init__(parameter, value)
        self.type_to_convert_to = type_to_convert_to
    
    def validate(self, results):
        fn = self.type_to_convert_to.parse_from
        if 'success_attribute' in signature(fn).parameters:
            result = self.type_to_convert_to.parse_from(self.value, self.parameter_name)
        else:
            result = self.type_to_convert_to.parse_from(self.value)
        return result.do(lambda result: results.add(self.parameter_name, getattr(result, self.parameter_name)))


class ValidEmailAddress(Validator):
    def validate(self, results):
        stripped = self.value.strip()
        if not is_valid_email_address(stripped):
            return Failure(message="{} does not contain a valid email address".format(self.parameter_name))
        results.add(self.parameter_name, stripped)
        return Success()


class TryTo(Validator):
    def __init__(self, parameter_name, value, success_attr):
        super().__init__(parameter_name, value)
        self.success_attr = success_attr

    def validate(self, results):
        if self.value.is_failure():
            return self.value
        results.add(self.parameter_name, self.value.body[self.success_attr])
        return Success()


def presence_of(parameter, value):
    return PresenceOf(parameter, value)


def optionality_of(parameter, value):
    return OptionalityOf(parameter, value)


def max_length_of(parameter, value, max):
    return MaxLengthOf(parameter, value, max)


def is_between(parameter, value, lower_bound, upper_bound):
    return IsBetween(parameter, value, lower_bound, upper_bound)


def conversion_of(parameter, value, type_to_convert_to):
    return ConversionOf(parameter, value, type_to_convert_to)


def email_validity_of(parameter, value):
    return ValidEmailAddress(parameter, value)


def an_attempt_to(value, parameter, success_attr):
    return TryTo(parameter, value, success_attr=success_attr)

def optional(validation):
    return OptionalValidation(validation)

def validate(*validations):
    validation_results = ValidationResults()
    for validation in validations:
        last_result = validation.validate(validation_results)
        if last_result.is_failure():
            return last_result
    return validation_results


def int_from_string(string_value, name):
    if string_value is None: return Failure(message="{} is missing".format(name))
    try: 
        return Success(value=int(string_value))
    except ValueError:
        return Failure(message='{} is not an integer value'.format(name))
