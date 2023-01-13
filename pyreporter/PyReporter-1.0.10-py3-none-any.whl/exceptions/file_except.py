from .abs_except import AbsException
from typing import Optional


# NonExistentFileError: Exception if a file does not exists
class NonExistentFileError(AbsException):
    """
    This Class inherits from :class:`~Reporter.exceptions.abs_except.AbsException`

    Exception thrown when a file does not exists

    Attributes
    ----------
    filename: :class:`str`
        The name of the file that was searched

    message: Optional[:class:`str`]
        a specific message to overwrite the default message template of this exception
    """
    def __init__(self, filename: str, message: Optional[str] = None, *args, **kwargs):
        super().__init__(message)
        self.filename = filename


    # _default_message(): Retrieves the default message for the exception
    def _default_message(self) -> str:
        return f"The file by the name, \"{self.filename}\", does not exist!"


# KeyValueMismatchError: Exception if the number of keys does not match the number
#   of values in a blank file
class KeyValueMismatchError(AbsException):
    def __init__(self, no_of_keys: int, no_of_values: int, message: Optional[str] = None, *args, **kwargs):
        super().__init__(message)
        self.no_of_keys = no_of_keys
        self.no_of_values = no_of_values


    # _default_message(): Retrieves the default message for the exception
    def _default_message(self) -> str:
        return  f"The number of keys ({self.no_of_keys}) does not match the number of values ({self.no_of_values})."
