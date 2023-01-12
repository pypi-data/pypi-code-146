import operator

from dominate.tags import li, ul

from iolanta.facet import Facet
from iolanta.namespaces import IOLANTA
from iolanta.renderer import render


class PositionsForIssue(Facet):
    """List positions to answer the Issue."""

    sparql_query = '''
    SELECT * WHERE {
        ?position ibis:responds-to $issue .
    } ORDER BY ?position
    '''

    def html(self):
        rows = self.query(self.sparql_query, issue=self.uriref)
        positions = list(map(operator.itemgetter('position'), rows))

        return ul(
            li(
                render(
                    position,
                    environments=[IOLANTA.html],
                    iolanta=self.iolanta,
                ),
            ) for position in positions
        )
