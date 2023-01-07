from dataclasses import dataclass

from documented import DocumentedError
from urlpath import URL


@dataclass
class IsAContext(DocumentedError):
    """
    The provided file is a context.

        - Path: {self.path}

    This file is not a piece of data and cannot be loaded into the graph.
    """

    path: URL


@dataclass
class ParserNotFound(DocumentedError):
    """
    Parser not found.

        Path: {self.path}
    """

    path: URL
