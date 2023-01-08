import itertools
import operator
from dataclasses import dataclass
from typing import Dict, Iterable, List

from documented import DocumentedError
from dominate.tags import li, strong, ul
from more_itertools import first
from rdflib import URIRef
from rdflib.term import Node

from iolanta.facet import Facet
from iolanta.iolanta import Iolanta
from iolanta.renderer import render
from octadocs_adr.models import ADR


def retrieve_properties_by_page(iolanta: Iolanta, iri: URIRef):
    about_this_page = iolanta.query(
        '''
        SELECT ?property ?value WHERE {
            ?page ?property ?value .

            ?property a adr:ADRProperty .

            OPTIONAL {
                ?property mkdocs:position ?explicit_position .
            }

            BIND(COALESCE(?explicit_position, 0) as ?position)
        } ORDER BY ?position ?property
        ''',
        page=iri,
    )

    groups = itertools.groupby(
        about_this_page,
        key=operator.itemgetter('property'),
    )

    return dict({
        grouper: list(map(
            operator.itemgetter('value'),
            group_items,
        ))
        for grouper, group_items in groups
    })


def render_property_values(
    property_values: List[Node],
    iolanta: Iolanta,
) -> str:
    rendered_values = [
        render(
            node=property_value,
            iolanta=iolanta,
            environments=[ADR.term('sidebar-property-value')],
        )
        for property_value in property_values
    ]

    if len(rendered_values) == 1:
        return rendered_values[0]

    return ul(*map(li, rendered_values))


def render_properties_and_values(
    properties_and_values: Dict[URIRef, List[Node]],
    iolanta: Iolanta,
) -> Iterable[li]:
    for property_iri, property_values in properties_and_values.items():
        rendered_property = render(
            node=property_iri,
            iolanta=iolanta,
            environments=[ADR.term('sidebar-property')],
        )

        rendered_values = render_property_values(
            property_values=property_values,
            iolanta=iolanta,
        )

        yield li(
            rendered_property,
            rendered_values,
            cls='md-nav__item md-nav__link',
        )


class PageSidebar(Facet):
    """Sidebar of an ADR page."""

    def html(self):
        """As HTML."""
        properties_and_values = retrieve_properties_by_page(
            iolanta=self.iolanta,
            iri=self.uriref,
        )

        return '\n'.join(map(str, render_properties_and_values(
            properties_and_values=properties_and_values,
            iolanta=self.iolanta,
        )))


@dataclass
class PropertyNotRenderable(DocumentedError):
    """
    Cannot render property for ADR page.

        Property IRI: {self.iri}

    Please ensure that the property has a proper `rdfs:label` assigned to it.
    """

    iri: URIRef


def sidebar_property(
    iolanta: Iolanta,
    iri: URIRef,
    environment: URIRef,
) -> str:
    """Render name of the property of the ADR page."""
    rows = iolanta.query(
        '''
        SELECT * WHERE {
            ?property rdfs:label ?label .

            OPTIONAL {
                ?property mkdocs:symbol ?symbol .
            }
        } LIMIT 1
        ''',
        property=iri,
    )

    try:
        row = first(rows)
    except ValueError as err:
        raise PropertyNotRenderable(iri=iri) from err

    label = row['label']
    if symbol := row.get('symbol'):
        label = f'{symbol} {label}'

    return strong(f'{label}: ')
