from dataclasses import dataclass
from typing import List

from documented import DocumentedError
from rdflib import URIRef
from rdflib.term import Node


@dataclass
class PageNotFound(DocumentedError):
    """
    Page not found by IRI: `{self.iri}`.

    !!! error "Page not found by IRI: `{self.iri}`"
        Every page on your documentation site, just as any other entity described on
        it, has an IRI — a unique identifier similar to a URL. IRI can be generated
        in two alternative ways.

          1. If you wanted to use IRI generated automatically, then please confirm
             that in the `docs` directory there is a file under the following path:

             ```
             {self.possible_path}
             ```

          2. If you wanted to use IRI that you specified explicitly then confirm
             there is a Markdown file somewhere in `docs` directory which contains
             the following text in its header:

             ```markdown
             ---
             $id: {self.possible_id}
             ---
             ```
    """

    iri: URIRef

    @property
    def possible_path(self) -> str:
        """Guess on a possible path."""
        base_path = str(self.iri).replace('local:', '')
        return f'{base_path}.md'

    @property
    def possible_id(self) -> str:
        """Guess on a possible $id."""
        return str(self.iri).replace('local:', '')


@dataclass
class MultipleFacetsFoundForTypes(DocumentedError):
    """
    Multiple suitable facets found.

    Unable to render the node unambiguously.

      - Node: {self.node}
      - Types:
    {self.formatted_types}
      - Facets found:
    {self.formatted_facets}
    """

    node: Node
    types: List[URIRef]
    facets: List[URIRef]

    @property
    def formatted_facets(self):
        return '\n'.join([
            f'    - {facet}'
            for facet in self.facets
        ])

    @property
    def formatted_types(self):
        return '\n'.join([
            f'    - <{node_type}>'
            for node_type in self.types
        ])

