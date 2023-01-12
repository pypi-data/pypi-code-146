import abc

from six import add_metaclass, string_types

from hackle.commons import validator
from hackle.evaluation.match.semantic_version import SemanticVersion


@add_metaclass(abc.ABCMeta)
class OperatorMatcher(object):

    @abc.abstractmethod
    def string_matches(self, user_value, match_value):
        pass

    @abc.abstractmethod
    def number_matches(self, user_value, match_value):
        pass

    @abc.abstractmethod
    def bool_matches(self, user_value, match_value):
        pass

    @abc.abstractmethod
    def version_matches(self, user_value, match_value):
        pass


class InMatcher(OperatorMatcher):
    def string_matches(self, user_value, match_value):
        if isinstance(user_value, string_types) and isinstance(match_value, string_types):
            return user_value == match_value
        else:
            return False

    def number_matches(self, user_value, match_value):
        if validator.is_finite_number(user_value) and validator.is_finite_number(match_value):
            return user_value == match_value
        else:
            return False

    def bool_matches(self, user_value, match_value):
        if isinstance(user_value, bool) and isinstance(match_value, bool):
            return user_value == match_value
        else:
            return False

    def version_matches(self, user_value, match_value):
        if isinstance(user_value, SemanticVersion) and isinstance(match_value, SemanticVersion):
            return user_value == match_value
        else:
            return False


class ContainsMatcher(OperatorMatcher):
    def string_matches(self, user_value, match_value):
        if isinstance(user_value, string_types) and isinstance(match_value, string_types):
            return match_value in user_value
        else:
            return False

    def number_matches(self, user_value, match_value):
        return False

    def bool_matches(self, user_value, match_value):
        return False

    def version_matches(self, user_value, match_value):
        return False


class StartsWithMatcher(OperatorMatcher):
    def string_matches(self, user_value, match_value):
        if isinstance(user_value, string_types) and isinstance(match_value, string_types):
            return user_value.startswith(match_value)
        else:
            return False

    def number_matches(self, user_value, match_value):
        return False

    def bool_matches(self, user_value, match_value):
        return False

    def version_matches(self, user_value, match_value):
        return False


class EndsWithMatcher(OperatorMatcher):
    def string_matches(self, user_value, match_value):
        if isinstance(user_value, string_types) and isinstance(match_value, string_types):
            return user_value.endswith(match_value)
        else:
            return False

    def number_matches(self, user_value, match_value):
        return False

    def bool_matches(self, user_value, match_value):
        return False

    def version_matches(self, user_value, match_value):
        return False


class GreaterThanMatcher(OperatorMatcher):
    def string_matches(self, user_value, match_value):
        return False

    def number_matches(self, user_value, match_value):
        if validator.is_finite_number(user_value) and validator.is_finite_number(match_value):
            return user_value > match_value
        else:
            return False

    def bool_matches(self, user_value, match_value):
        return False

    def version_matches(self, user_value, match_value):
        if isinstance(user_value, SemanticVersion) and isinstance(match_value, SemanticVersion):
            return user_value > match_value
        else:
            return False


class GreaterThanOrEqualToMatcher(OperatorMatcher):
    def string_matches(self, user_value, match_value):
        return False

    def number_matches(self, user_value, match_value):
        if validator.is_finite_number(user_value) and validator.is_finite_number(match_value):
            return user_value >= match_value
        else:
            return False

    def bool_matches(self, user_value, match_value):
        return False

    def version_matches(self, user_value, match_value):
        if isinstance(user_value, SemanticVersion) and isinstance(match_value, SemanticVersion):
            return user_value >= match_value
        else:
            return False


class LessThanMatcher(OperatorMatcher):
    def string_matches(self, user_value, match_value):
        return False

    def number_matches(self, user_value, match_value):
        if validator.is_finite_number(user_value) and validator.is_finite_number(match_value):
            return user_value < match_value
        else:
            return False

    def bool_matches(self, user_value, match_value):
        return False

    def version_matches(self, user_value, match_value):
        if isinstance(user_value, SemanticVersion) and isinstance(match_value, SemanticVersion):
            return user_value < match_value
        else:
            return False


class LessThanOrEqualToMatcher(OperatorMatcher):
    def string_matches(self, user_value, match_value):
        return False

    def number_matches(self, user_value, match_value):
        if validator.is_finite_number(user_value) and validator.is_finite_number(match_value):
            return user_value <= match_value
        else:
            return False

    def bool_matches(self, user_value, match_value):
        return False

    def version_matches(self, user_value, match_value):
        if isinstance(user_value, SemanticVersion) and isinstance(match_value, SemanticVersion):
            return user_value <= match_value
        else:
            return False
