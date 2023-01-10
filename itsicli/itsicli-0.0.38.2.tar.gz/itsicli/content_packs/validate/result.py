from enum import Enum


def result(level, message):
    return ValidationResult(level, message)


class Level(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3

    def __str__(self):
        return str(self.name).lower()


class ValidationResult(object):

    def __init__(self, level, message):
        self.level = level
        self.message = message
