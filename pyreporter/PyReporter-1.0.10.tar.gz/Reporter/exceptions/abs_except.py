from typing import Optional


class AbsException(Exception):
    """
    This Class inherits from :class:`Exception`

    The base exception the API

    Attributes
    ----------
    message: Optional[:class:`str`]
        the error message to be sent
    """
    def __init__(self, message: Optional[str] = None, *args, **kwargs):
        self.message = message
        self.args = args
        self.kwargs = kwargs
        super().__init__(self.message)


    # _default_message(): Retrieves the default message for the exception
    def _default_message(self) -> str:
        pass


    # __str__(): Overwrites the message for the exception
    def __str__(self) -> str:
        if (self.message is None):
            return self._default_message()
        else:
            return self.message
