from .abs_except import AbsException
from typing import Optional


class BadSourceException(AbsException):
    """
    This Class inherits from :class:`~Reporter.exceptions.abs_except.AbsException`

    Exception when a source is unable to import its corresponding table

    Attributes
    ----------
    source_name: :class:`str`
        The name of the source that threw the exception

    prev_import_errs: :class:`str`
        Any previous exception messages from attempting to import using the table using
        other import methods

    message: Optional[:class:`str`]
        a specific message to overwrite the default message template of this exception
    """
    def __init__(self, source_name: str, prev_import_errs: str, message: Optional[str] = None, *args, **kwargs):
        super().__init__(message)
        self.source_name = source_name
        self.prev_import_errs = prev_import_errs


    # _default_message(): Retrieves the default message for the exception
    def _default_message(self) -> str:
        message = f"Unable to Load the source by the name \"{self.source_name}\" using any of its available import methods."
        message += f"\n{self.prev_import_errs}"

        return message
