import re
from typing import Iterable
from typing import Optional

from userinputgetter.user_input_getter import UserInputGetter


class IntegerInputGetter(UserInputGetter):
    regex = re.compile("^([-+]?[1-9][0-9]*|0)$")

    def __init__(self, supported_options: Optional[Iterable[int]] = None):
        if supported_options is not None:
            supported_options = tuple(x for x in supported_options)
            if not all(isinstance(x, int) for x in supported_options):
                raise TypeError("All supported options, if specified, must be integers")

        super().__init__(supported_options)

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return bool(cls.regex.match(value))

    @staticmethod
    def parse(value: str) -> int:
        return int(value)
