from dataclasses import dataclass
from typing import Optional

from documented import DocumentedError
from rdflib import URIRef


@dataclass
class YAMLError(DocumentedError):
    """
    Invalid YAML.

    File: {self.iri}

    {self.error}
    """

    iri: Optional[URIRef]
    error: Exception
