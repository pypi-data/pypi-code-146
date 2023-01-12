from typing import Optional, Tuple

from more_itertools import first
from rdflib import URIRef
from rdflib.term import Node

from ldflex import LDFlex

EVALUATION_QUERY = '''
    SELECT ?evaluation ?value WHERE {
        $position ibis:evaluation ?evaluation .
        ?evaluation prov:value* ?value .

        FILTER (isLiteral(?value))
    }
'''


def retrieve_evaluation_for_position(
    position: URIRef,
    ldflex: LDFlex,
) -> Optional[Tuple[Optional[bool], Optional[Node]]]:
    """Find out whether the position is accepted by us or not."""
    rows = ldflex.query(EVALUATION_QUERY, position=position)

    try:
        row = first(rows)
    except ValueError:
        return None, None

    return row['value'].value, row['evaluation']
