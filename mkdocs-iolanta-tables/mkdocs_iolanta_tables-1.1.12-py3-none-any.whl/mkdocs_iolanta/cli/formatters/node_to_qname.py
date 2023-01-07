from classes import typeclass
from rdflib import Graph, URIRef
from rdflib.term import Node

from mkdocs_iolanta.types import ComputedQName


@typeclass
def node_to_qname(node: Node, graph: Graph):
    """Convert a node to a QName."""


@node_to_qname.instance(object)
def _object_to_qname(node: URIRef, graph: Graph):
    return node


@node_to_qname.instance(URIRef)
def _uriref_to_qname(node: URIRef, graph: Graph):
    try:
        qname = graph.compute_qname(node)
    except ValueError:
        return node
    except NameError as err:
        raise ValueError(f'NameError! On: {node}') from err

    return ComputedQName(*qname)
