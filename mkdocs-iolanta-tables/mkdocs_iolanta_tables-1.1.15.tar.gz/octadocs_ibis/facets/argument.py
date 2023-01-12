from dominate.tags import p, span
from dominate.util import text
from more_itertools import first

from iolanta.facet import Facet
from iolanta.namespaces import IOLANTA
from iolanta.renderer import render


class Argument(Facet):
    sparql_query = '''
        SELECT ?agent WHERE {
            $argument ibis:endorsed-by ?agent .
        }
    '''

    def html(self):
        rows = self.query(self.sparql_query, argument=self.uriref)

        argument_body = render(
            self.uriref,
            environments=[IOLANTA.html],
            iolanta=self.iolanta,
        )

        try:
            row = first(rows)

        except ValueError:
            return argument_body

        agent = render(
            row['agent'],
            environments=[IOLANTA.html, IOLANTA.td],
            iolanta=self.iolanta,
        )

        return span(
            p(
                agent,
                text(': '),
            ),
            argument_body
        )

