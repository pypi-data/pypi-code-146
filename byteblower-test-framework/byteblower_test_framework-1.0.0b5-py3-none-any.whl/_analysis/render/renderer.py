"""Contains the data analysis renderer interface."""


class Renderer(object):
    """Renderer interface of Data analysis."""

    __slots__ = ()

    def __init__(self) -> None:
        """Make a new reporter."""
        pass

    def render(self) -> str:
        """
        .. note::
           Virtual method.
        """
        pass

    def _verbatim(self, text: str) -> str:
        return '<pre>' + text + '</pre>'
