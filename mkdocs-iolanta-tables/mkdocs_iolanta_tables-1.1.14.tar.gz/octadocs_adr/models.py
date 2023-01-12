from dataclasses import dataclass
from typing import Any

from documented import DocumentedError
from rdflib import Namespace

ADR = Namespace('https://octadocs.io/adr/')


@dataclass
class ADRNumberInvalid(DocumentedError):
    """
    The value `{self.number}` is not a valid ADR number.

    The number must be natural (i. e. a positive integer).

    ADR page to blame:

        {self.page}
    """

    number: Any
    page: str
