import operator
from typing import Iterable, Optional, Tuple, Union

import pygraphviz
from funcy import distinct
from rdflib import Literal

from iolanta.facet import Facet
from iolanta.renderer import render
from ldflex.ldflex import SelectRow
from octadocs_ibis.mixins import LanguageAware
from octadocs_ibis.models import IBIS


class IBISGraph(LanguageAware, Facet):
    """Draw graph."""

    nodes_query = '''
    SELECT ?node ?node_type ?title ?url ?is_accepted WHERE {
        $this mkdocs:subjectOf ?current_page .

        ?current_directory mkdocs:isParentOf ?current_page .

        {
            ?current_directory mkdocs:isParentOf ?page .
        } UNION {
            ?current_directory mkdocs:isParentOf / mkdocs:isParentOf ?page .
            ?page a mkdocs:IndexPage .
        }

        GRAPH ?page {
            ?node mkdocs:title ?title .
        }

        ?node a skos:Concept, ?node_type .

        OPTIONAL {
            ?node mkdocs:url ?url .
        }

        ?node_type mkdocs:position ?node_type_priority .

        OPTIONAL {
            ?node ibis:evaluation / prov:value ?is_accepted .
            FILTER(!isBlank(?is_accepted))
        }

        FILTER(?node_type IN (ibis:Issue, ibis:Position, ibis:Argument))
    } ORDER BY ?node ?node_type_priority
    '''

    edges_query = '''
    SELECT ?edge ?source ?destination ?edge_label WHERE {
        ?source ?edge ?destination .
        ?edge rdfs:label ?edge_label .

        FILTER(
            ?edge IN (
                ibis:suggests,
                ibis:response,
                ibis:supported-by,
                ibis:opposed-by
            )
        )
    } ORDER BY DESC(LANG(?edge_label))
    '''

    def _node_options(self, row: SelectRow):
        if not row.get('url'):
            return {}

        is_accepted_literal: Optional[Literal] = row.get('is_accepted')

        if is_accepted_literal is None:
            # This is not an ibis:Position, or it does not have an evaluation.
            return {'fillcolor': '#CCCCCC', 'color': '#00000052'}

        is_accepted: bool = is_accepted_literal.toPython()

        if is_accepted:
            return {'fillcolor': '#00c853bb', 'color': '#00c853'}
        else:
            return {'fillcolor': '#ff5252bb', 'color': '#ff5252'}

    def _edge_options(
        self, row: SelectRow,
    ) -> Iterable[Tuple[str, Optional[Union[str, int]]]]:
        """Construct  edge options depending on its type."""
        if row['edge'] == IBIS.term('supported-by'):
            yield 'tooltip', '➕ За'

    def distinct_nodes(self, rows):
        return distinct(
            rows,
            key=operator.itemgetter('node'),
        )

    def _construct_node_rows(self):
        yield from self.distinct_nodes(
            self.query(self.nodes_query, this=self.uriref),
        )

    def html(self):
        node_rows = list(self._construct_node_rows())

        graph = pygraphviz.AGraph(
            directed=True,
            rankdir='LR',
            bgcolor='#ffffff00',
            splines='ortho',
        )

        for row in node_rows:
            rendered_node = render(
                row['node'],
                environments=[IBIS.IBISNode],
                iolanta=self.iolanta,
            )

            node_style = 'rounded,filled'

            node_shape = 'box'
            pen_width = 1
            if row['node'] == self.uriref:
                node_style = f'{node_style},bold'
                pen_width = 4

            if href := row.get('url'):
                href_options = {'href': href}
                if not href.startswith('/'):
                    # This is an external link.
                    rendered_node = f'{rendered_node} ⧉'
                    href_options.update(target='_blank')

            else:
                node_style = 'rounded,filled'
                href_options = {}

            graph.add_node(
                row['node'],
                shape=node_shape,
                style=node_style,
                label=f'<{rendered_node}>',
                fontname='Roboto',
                margin=0.2,
                penwidth=pen_width,
                **href_options,
                **self._node_options(row),
            )

        node_iris = set(
            map(
                operator.itemgetter('node'),
                node_rows,
            ),
        )

        edges_rows = list(
            self.remove_duplicate_edges(
                self.query(self.edges_query),
            ),
        )

        for row in edges_rows:
            if row['source'] in node_iris and row['destination'] in node_iris:
                direction = 'forward'
                edge_color = '#00000052'
                if row['edge'] in {
                    IBIS.term('supported-by'),
                    IBIS.term('opposed-by'),
                    IBIS.term('questioned-by'),
                }:
                    direction = 'back'

                graph.add_edge(
                    row['source'],
                    row['destination'],
                    fontname='Roboto',

                    penwidth=2,
                    dir=direction,
                    color=edge_color,

                    **dict(self._edge_options(row)),
                )

        return graph.draw(format='svg', prog='dot').decode('utf-8')

    def remove_duplicate_edges(self, rows):
        """
        ibis:questioned-by is an rdfs:subPropertyOf of ibis:suggests.

        This creates duplicates. They must be removed.
        """
        questioned_by_edges = {
            (row['source'], row['destination'])
            for row in rows
            if row['edge'] == IBIS.term('questioned-by')
        }

        for row in rows:
            if (
                row['edge'] == IBIS.suggests
                and (row['source'], row['destination']) in questioned_by_edges
            ):
                continue

            yield row
