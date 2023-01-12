import itertools
import logging
import operator
from dataclasses import dataclass
from functools import cached_property
from typing import Dict, List, Optional

from dominate import tags
from mkdocs.structure.pages import Page
from more_itertools import first
from rdflib import URIRef
from rdflib.term import Literal, Node

from iolanta.iolanta import Iolanta
from iolanta.renderer import render

logger = logging.getLogger(__name__)


def app_by_property(iolanta: Iolanta) -> Dict[URIRef, URIRef]:
    """Find apps connected to properties."""
    pairs = iolanta.query(
        '''
        SELECT ?property ?app WHERE {
            ?property iolanta:facet ?facet .
            ?app iolanta:supports adr:sidebar .
        }
        '''
    )
    return {
        row['property']: row['facet']
        for row in pairs
    }


def default_property_facet(
    iolanta: Iolanta,
    property_iri: URIRef,
    property_values: List[Node],
) -> Optional[str]:
    """Default facet to render a property with its values."""
    label = first(
        map(
            operator.itemgetter('label'),
            iolanta.query(
                '''
                SELECT ?label WHERE {
                    ?property rdfs:label ?label .
                } ORDER BY ?label LIMIT 1
                ''',
                property=property_iri,
            ),
        ),
        None,
    )

    if label is None:
        return

    if len(property_values) > 1:
        raise Exception('Too many values')

    property_value = property_values[0]

    if isinstance(property_value, Literal):
        return f'<strong>{label}</strong>: {property_value}'

    rendered_value = render(
        iolanta=iolanta,
        node=property_value,
    )
    return f'<strong>{label}</strong>: {rendered_value}'


@dataclass
class DecisionContext:
    """Context for the Decision template."""

    page: Page
    iolanta: Iolanta

    @cached_property
    def iri(self) -> URIRef:
        """Retrieve the IRI of current page."""
        return self.page.iri

    @cached_property
    def status(self) -> str:
        status_choices = self.iolanta.query('''
            SELECT ?label ?symbol WHERE {
                ?page adr:status [
                    rdfs:label ?label ;
                    mkdocs:symbol ?symbol
                ] .
            }
        ''', page=self.iri)

        if not status_choices:
            return ''

        elif len(status_choices) < 2:
            status, = status_choices
            label = status['label']
            symbol = status['symbol']
            return f'{symbol} {label}'

        raise ValueError(
            f'This page has too many status values: {status_choices}',
        )

    @cached_property
    def author(self):
        authors = self.iolanta.query('''
            SELECT ?name ?url WHERE {
                ?page adr:author [
                    schema:name ?name ;
                    schema:url ?url
                ] .
            }
        ''', page=self.iri)

        if not authors:
            return ''

        if len(authors) < 2:
            author, = authors

            dom = tags.li(
                tags.a(
                    tags.strong('Author: '),
                    author['name'],

                    cls='md-nav__link',
                    href=author['url'],
                    target='_blank',
                ),
                cls='md-nav__item',
            )

            return str(dom)

        raise ValueError('page has too many authors!')

    @cached_property
    def date(self) -> str:
        date_choice = self.iolanta.query('''
            SELECT ?date WHERE {
                ?page adr:date ?date .
            }
        ''', page=self.iri).first

        if not date_choice:
            return ''

        return date_choice['date'].value

    def describe_this_page(self) -> Dict[URIRef, List[Node]]:
        """List all properties of current page that can be rendered."""
        about_this_page = self.iolanta.query(
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
            page=self.page.iri,
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

    def page_properties(self):
        """Render page properties block."""
        properties_and_apps = app_by_property(self.iolanta)
        properties_and_values = self.describe_this_page()

        for property_iri, property_values in properties_and_values.items():
            if attached_app_iri := properties_and_apps.get(property_iri):
                raise ValueError(f'Attached app: {attached_app_iri}')

            rendered_facet = default_property_facet(
                iolanta=self.iolanta,
                property_iri=property_iri,
                property_values=property_values,
            )

            yield f'<li class="md-nav__item md-nav__link">{rendered_facet}</li>'

    @property
    def render_page_properties(self):
        return '\n'.join(filter(None, self.page_properties()))
