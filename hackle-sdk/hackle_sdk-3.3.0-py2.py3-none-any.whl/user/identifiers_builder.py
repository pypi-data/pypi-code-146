from six import string_types

from hackle import logger as _logging


class IdentifiersBuilder(object):

    def __init__(self, logger=None):
        self.logger = _logging.adapt_logger(logger or _logging.NoOpLogger())
        self.identifiers = {}

    def add_identifiers(self, identifiers):
        if identifiers is None:
            return self

        if not isinstance(identifiers, dict):
            self.logger.warning('Identifiers must be dictionary.')
            return self

        for identifier_type in identifiers:
            self.add(identifier_type, identifiers[identifier_type])

        return self

    def add(self, identifier_type, identifier_value):
        if self._is_valid(identifier_type, identifier_value):
            self.identifiers[identifier_type] = identifier_value
        else:
            self.logger.warning('Invalid user identifier [type={}, value={}]'.format(identifier_type, identifier_value))
        return self

    def _is_valid(self, identifier_type, identifier_value):
        if identifier_type is None:
            return False

        if not isinstance(identifier_type, string_types):
            return False

        if len(identifier_type) == 0:
            return False

        if len(identifier_type) > 128:
            return False

        if identifier_value is None:
            return False

        if not isinstance(identifier_value, string_types):
            return False

        if len(identifier_value) == 0:
            return False

        if len(identifier_value) > 512:
            return False

        return True

    def build(self):
        return self.identifiers
