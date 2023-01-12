from dataclasses import dataclass
from functools import cached_property
from typing import Optional, Union

from dominate.tags import html_tag
from rdflib.term import BNode, Node, URIRef

from iolanta.iolanta import Iolanta
from ldflex import LDFlex


@dataclass
class Facet:
    """Base facet class."""

    iri: Node
    iolanta: Iolanta
    environment: Optional[URIRef] = None

    @property
    def ldflex(self) -> LDFlex:
        """Extract LDFLex instance."""
        return self.iolanta.ldflex

    @cached_property
    def uriref(self) -> Union[URIRef, BNode]:
        """Format as URIRef."""
        if isinstance(self.iri, BNode):
            return self.iri

        return URIRef(self.iri)

    def query(self, query_text: str, **kwargs):
        """SPARQL query."""
        return self.ldflex.query(
            query_text=query_text,
            **kwargs,
        )

    def html(self) -> Union[str, html_tag]:
        """Render the facet."""
        raise NotImplementedError()

    @property
    def language(self):
        # return self.iolanta.language
        return 'en'

    def __str__(self):
        """Render."""
        return str(self.html())
