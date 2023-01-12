import itertools
import operator
from typing import Iterable, List

from dominate.tags import div, h2, h3, table, td, tr
from more_itertools import grouper
from rdflib import URIRef

from iolanta.facet import Facet
from iolanta.namespaces import IOLANTA
from iolanta.renderer import render
from mkdocs_iolanta_tables.models import TABLE
from octadocs_ibis.models import IBIS

COLUMN_COUNT = 3


class ArgumentsForPosition(Facet):
    """Render arguments list of a given Position."""

    query_text = '''
    SELECT ?arg ?link WHERE {
        ?arg
            ?link $position ;
            a ibis:Argument .
    } ORDER BY ?link ?arg
    '''

    def construct_table_rows(self) -> Iterable[tr]:
        rows = self.query(
            self.query_text,
            position=self.iri,
        )

        rows_by_relation = itertools.groupby(
            rows,
            key=operator.itemgetter('link'),
        )

        return {
            relation: [item['arg'] for item in items]
            for relation, items in rows_by_relation
        }

    def format_table_rows(self, arguments: List[URIRef]) -> Iterable[tr]:
        """Format table rows for a gallery of arguments."""
        env = [TABLE.td, IOLANTA.html]
        renderables = [
            render(
                argument,
                environments=env,
                iolanta=self.iolanta,
            ) for argument in arguments
        ]

        grouped_renderables = grouper(renderables, COLUMN_COUNT, '')

        for group in grouped_renderables:
            cells = [td(renderable) for renderable in group]
            yield tr(*cells)

    def html(self):
        arguments_by_relation = self.construct_table_rows()

        if not arguments_by_relation:
            return ''

        with div() as container:
            h2('Аргументы')

            for relation, arguments in arguments_by_relation.items():
                h3(
                    render(
                        relation,
                        environments=[IOLANTA.td, IOLANTA.html],
                        iolanta=self.iolanta,
                    ),
                )

                table_rows = self.format_table_rows(arguments)

                table(*table_rows)

        return container
