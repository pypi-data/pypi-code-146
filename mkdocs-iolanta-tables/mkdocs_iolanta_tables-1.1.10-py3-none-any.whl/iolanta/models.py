from typing import Any, Dict, List, NamedTuple, Union

from rdflib import Literal, URIRef
# JSON-LD context
from rdflib.term import Node

LDContext = Dict[str, Any]  # type: ignore
LDDocument = Union[Dict[str, Any], List[Dict[str, Any]]]  # type: ignore


# Named context URLs
ContextAliases = Dict[str, str]


def render_node(node: Node) -> str:
    """Render an RDFLib node as string."""
    if isinstance(node, URIRef):
        return f'<{node}>'

    if isinstance(node, Literal):
        rendered_node = f'"{node}"'
        if node.datatype:
            rendered_node = f'{rendered_node}^^{node.datatype}'

        if node.language:
            rendered_node = f'{rendered_node}@{node.language}'

        return rendered_node

    return f'<??? What is this? {node} ???>'


class Triple(NamedTuple):
    """RDF triple."""

    subject: URIRef
    predicate: URIRef
    object: Union[URIRef, Literal]  # noqa: WPS125

    def as_quad(self, graph: URIRef) -> 'Quad':
        """Add graph to this triple and hence get a quad."""
        return Quad(
            subject=self.subject,
            predicate=self.predicate,
            object=self.object,
            graph=graph,
        )


class Quad(NamedTuple):
    """Triple assigned to a named graph."""

    subject: Node
    predicate: Node
    object: Node  # noqa: WPS125
    graph: URIRef

    def as_triple(self):
        """Convert this to triple."""
        return Triple(self.subject, self.predicate, self.object)

    def __repr__(self):
        (
            rendered_subject,
            rendered_predicate,
            rendered_object,
            rendered_graph,
        ) = map(render_node, self)
        return (
            f'({rendered_subject} {rendered_predicate} {rendered_object} @ '
            f'{rendered_graph})'
        )
