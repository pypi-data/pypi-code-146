import operator

from more_itertools import first
from rdflib.term import Node

from iolanta.iolanta import Iolanta


def default(iolanta: Iolanta, node: Node) -> str:
    """
    Default facet to render an arbitrary object.

    Relies upon rdfs:label.
    """
    rows = iolanta.query(
        'SELECT ?label WHERE { ?node rdfs:label ?label }',
        node=node,
    )

    labels = map(
        operator.itemgetter('label'),
        rows,
    )

    return first(labels, '[No Label]')
