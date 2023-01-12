import abc

import six
from six import add_metaclass

from hackle import logger as _logging
from hackle.evaluation.match.value_operator_matcher import ValueOperatorMatcher, ValueOperatorMatcherFactory


@add_metaclass(abc.ABCMeta)
class ConditionMatcher(object):

    @abc.abstractmethod
    def matches(self, condition, workspace, user):
        pass


class UserConditionMatcher(ConditionMatcher):
    def __init__(self, user_value_resolver, value_operator_matcher, logger=None):
        self.user_value_resolver = user_value_resolver
        self.value_operator_matcher = value_operator_matcher
        self.logger = _logging.adapt_logger(logger or _logging.NoOpLogger())

    def matches(self, condition, workspace, user):
        user_value = self.user_value_resolver.resolve_or_none(user, condition.key)
        if user_value is None:
            return False

        return self.value_operator_matcher.matches(user_value, condition.match)


class UserValueResolver(object):

    def __init__(self, logger=None):
        self.logger = _logging.adapt_logger(logger or _logging.NoOpLogger())

    def resolve_or_none(self, user, target_key):
        if target_key.type == 'USER_ID':
            return user.identifiers.get(target_key.name)
        elif target_key.type == 'USER_PROPERTY':
            return user.properties.get(target_key.name)
        elif target_key.type == 'HACKLE_PROPERTY':
            return None
        elif target_key.type == 'SEGMENT':
            raise Exception('Unsupported target_key.type [SEGMENT]')
        else:
            self.logger.debug('Unsupported type [{}]. Please use the latest version of sdk.'.format(target_key))
            return None


class SegmentConditionMatcher(ConditionMatcher):

    def __init__(self, segment_matcher, logger=None):
        self.segment_matcher = segment_matcher
        self.logger = _logging.adapt_logger(logger or _logging.NoOpLogger())

    def matches(self, condition, workspace, user):
        if condition.key.type != 'SEGMENT':
            raise Exception('Unsupported target.key.type [{}]'.format(condition.key.type))

        for value in condition.match.values:
            if self._matches(value, workspace, user):
                return self._match_type(condition.match.type, True)

        return self._match_type(condition.match.type, False)

    def _matches(self, value, workspace, user):
        segment_key = value
        if not isinstance(segment_key, six.string_types):
            raise Exception('SegmentKey[{}]'.format(segment_key))
        segment = workspace.get_segment_or_none(segment_key)
        if not segment:
            raise Exception('Segment[{}]'.format(segment_key))

        return self.segment_matcher.matches(segment, workspace, user)

    def _match_type(self, match_type, is_matched):
        if match_type == 'MATCH':
            return is_matched
        elif match_type == 'NOT_MATCH':
            return not is_matched
        else:
            self.logger.debug('Unsupported type[{}]. Please use the latest version of sdk.'.format(match_type))
            return False


class SegmentMatcher(object):
    def __init__(self, user_condition_matcher):
        self.user_condition_matcher = user_condition_matcher

    def matches(self, segment, workspace, user):
        for target in segment.targets:
            if self._matches(target, workspace, user):
                return True
        return False

    def _matches(self, target, workspace, user):
        for condition in target.conditions:
            if not self.user_condition_matcher.matches(condition, workspace, user):
                return False
        return True


class ConditionMatcherFactory(object):

    def __init__(self, logger=None):
        self.logger = _logging.adapt_logger(logger or _logging.NoOpLogger())

        self.user_condition_matcher = UserConditionMatcher(
            UserValueResolver(self.logger),
            ValueOperatorMatcher(ValueOperatorMatcherFactory(), self.logger),
            self.logger)
        self.segment_condition_matcher = SegmentConditionMatcher(SegmentMatcher(self.user_condition_matcher),
                                                                 self.logger)

    def get_condition_matcher_or_none(self, target_key_type):
        if target_key_type == 'USER_ID':
            return self.user_condition_matcher
        elif target_key_type == 'USER_PROPERTY':
            return self.user_condition_matcher
        elif target_key_type == 'HACKLE_PROPERTY':
            return self.user_condition_matcher
        elif target_key_type == 'SEGMENT':
            return self.segment_condition_matcher
        else:
            return None
