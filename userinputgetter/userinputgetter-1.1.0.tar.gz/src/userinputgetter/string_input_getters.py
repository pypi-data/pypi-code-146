from typing import Iterable
from typing import Optional

from userinputgetter.user_input_getter import UserInputGetter


class CaseInsensitiveStringInputGetter(UserInputGetter):
    def __init__(self, supported_options: Optional[Iterable[str]] = None):
        if supported_options is not None:
            supported_options = tuple(x for x in supported_options)
            if not all(isinstance(x, str) for x in supported_options):
                raise TypeError("All supported options, if specified, must be strings")

        super().__init__(supported_options)

    def parse(self, value: str) -> str:
        if self.supported_options is None:
            return value

        # If possible, match the case of another otherwise-matching entry
        for option in self.supported_options:
            if option.lower() == value.lower():
                return option

        # If not possible, pass the value on unchanged to be flagged as not supported
        return value

    def is_supported(self, value: str) -> bool:
        if self.supported_options is None:
            return True

        return value.lower() in {x.lower() for x in self.supported_options}
