import textwrap
from dataclasses import dataclass, field
from typing import List

from documented import DocumentedError
from rdflib import URIRef
from rdflib.term import Literal, Node

from iolanta.facets.base import FacetSearchAttempt


@dataclass
class FacetNotCallable(DocumentedError):
    """
    Python facet not callable.

    !!! error "Cannot import an object or cannot call it."

          - Import path: `{self.path}`
          - Object imported: `{self.facet}`

        The imported Python object is not a callable and thus cannot be used as
        a facet.
    """

    path: str
    facet: object


@dataclass
class FacetNotFound(DocumentedError):
    """
    Facet not found.

    !!! error "No way to render the node you asked for"
        - **Node:** `{self.node}` *({self.node_type})*
        - **Environments tried:** `{self.environments}`

        We tried desperately but could not find a facet to display this node 😟

        {self.render_facet_search_attempts}
    """

    node: Node
    environments: List[URIRef]
    facet_search_attempts: List[FacetSearchAttempt]
    node_types: List[URIRef] = field(default_factory=list)

    @property
    def node_type(self) -> str:
        """Node type."""
        node_type = type(self.node).__name__
        if isinstance(self.node, Literal):
            datatype = self.node.datatype
            node_type = f'{node_type}, datatype={datatype}'

        return node_type

    @property
    def render_facet_search_attempts(self):
        """Render facet search attempts."""
        return textwrap.indent(
            ''.join(
                f'\n\n## {attempt}'
                for attempt in self.facet_search_attempts
            ),
            '    ',
        )


@dataclass
class FacetError(DocumentedError):
    """
    Facet rendering failed.

    !!! error "Facet has thrown an unhandled exception"
        - Node: `{self.node}`
        - Facet IRI: `{self.facet_iri}`

        ### Exception

        {self.indented_error}

        Why was this facet at all chosen for this node?

        ### {self.render_facet_search_attempt}
    """

    node: Node
    facet_iri: URIRef
    facet_search_attempt: FacetSearchAttempt
    error: Exception

    @property
    def render_facet_search_attempt(self):
        """Render facet search attempt."""
        return textwrap.indent(
            f'\n## {self.facet_search_attempt}',
            '    ',
        )

    @property
    def indented_error(self):
        """Format the underlying error text."""
        return textwrap.indent(
            str(self.error),
            prefix='    ',
        )
