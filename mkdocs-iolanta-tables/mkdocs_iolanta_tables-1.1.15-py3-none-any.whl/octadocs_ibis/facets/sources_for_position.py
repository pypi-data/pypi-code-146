from boltons.iterutils import chunked_iter
from dominate.tags import div, table, tbody, td, tr

from iolanta.facet import Facet
from iolanta.namespaces import IOLANTA
from iolanta.renderer import render
from octadocs_ibis.models import IBIS

# Number of columns in the sources table.
COLUMN_COUNT = 2


class SourcesForPosition(Facet):
    """List sources for a given Position."""

    sparql_query = '''
    SELECT ?source WHERE {
        $position prov:wasDerivedFrom ?source .

        OPTIONAL {
            ?source mkdocs:position ?explicit_position .
        }

        BIND(COALESCE(?explicit_position, 0) as ?position)
    } ORDER BY ?position
    '''

    def html(self):
        sources = self.query(
            self.sparql_query,
            position=self.uriref,
        )

        renderables = [
            render(
                source['source'],
                environments=[IBIS.SourcesForPosition, IOLANTA.html],
                iolanta=self.iolanta,
            ) for source in sources
        ]

        if renderables:
            return div(*renderables)

        return ''
