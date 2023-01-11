"""
Tools used to handle accounting files
"""
from typing import IO, Iterable
from zope.interface import Interface, implementer


class IAccountingOperationStreamer(Interface):
    """
    Data streamer used to stream the raw data representing operations
    """

    def stream(self) -> Iterable[dict]:
        """
        Stream dictionnaries for each operations
        """
        pass


@implementer(IAccountingOperationStreamer)
class AccountingSlkStreamer:

    def __init__(self, file_object: IO):
        self.file_object = file_object

