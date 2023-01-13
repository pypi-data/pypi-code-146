"""
Custom types module. Defines types that extend the ones available from click
to use for validation of the config options
"""

import logging

from click.types import BoolParamType, Choice, Path, IntRange


class ExtendedBoolType(BoolParamType):
    def convert(self, value, *args):
        """
        Uses the conversion according to the click type, but additionally
        accepts `on/off` options for True and False respectively
        """
        if value == "on":
            return True
        if value == "off":
            return False
        return super().convert(value, *args)


BOOL = ExtendedBoolType()
LOGGING_OPTIONS = Choice(choices=(logging._levelToName.values()))
DIR_PATH_NON_EXISTING = Path(exists=False, dir_okay=True)
FILE_PATH_NON_EXISTING = Path(exists=False, file_okay=True)
FILE_PATH_EXISTING = Path(exists=True, file_okay=True)
POSITIVE_INT = IntRange(min=1)
