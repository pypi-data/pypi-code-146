from .abs_except import AbsException
from typing import Optional


class BadSharepointAuth(AbsException):
    def __init__(self, username:str, password: str, link: str, message: Optional[str] = None, *args, **kwargs):
        super().__init__(message)
        self.username = username
        self.password = password
        self.link = link


    # _default_message(): Retrieves the default message for the exception
    def _default_message(self) -> str:
        return f"Unable to access the file/folder in sharepoint by the link \"{self.link}\""
