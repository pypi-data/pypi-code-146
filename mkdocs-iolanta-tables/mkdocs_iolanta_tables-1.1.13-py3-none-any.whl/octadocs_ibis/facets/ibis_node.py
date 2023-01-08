import html
import textwrap

import funcy
from dominate.tags import br

from iolanta.facet import Facet
from octadocs_ibis.mixins import LanguageAware


class IBISNode(LanguageAware, Facet):
    sparql_query = '''
    SELECT * WHERE {
        $iri
            mkdocs:title ?title ;
            a ?type .

        OPTIONAL {
            $iri mkdocs:symbol ?symbol .
        }

        ?type rdfs:label ?type_title .
    } ORDER BY DESC(LANG(?type_title))
    '''

    def html(self):
        rows = self.query(
            self.sparql_query,
            iri=self.uriref,
        )

        row = funcy.first(rows)

        if row is None:
            return str(self.uriref)

        heading = row['title']
        if symbol := row.get('symbol'):
            heading = f'{symbol} {heading}'

        wrapped_title = textwrap.wrap(
            html.escape(heading.replace('"', '')),
            width=20,
        )

        wrapped_title_with_line_breaks = funcy.interpose(
            # See:
            #   https://renenyffenegger.ch/notes/tools/Graphviz/attributes/
            #   label/HTML-like/index
            br().render(xhtml=True),
            wrapped_title,
        )

        return ''.join(wrapped_title_with_line_breaks)
