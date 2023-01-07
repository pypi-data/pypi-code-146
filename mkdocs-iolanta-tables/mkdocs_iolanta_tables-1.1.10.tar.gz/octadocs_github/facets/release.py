from datetime import date, datetime
from typing import Iterable

from dominate.tags import a, br, code, html_tag, span
from more_itertools import first

from iolanta.facet import Facet


class Release(Facet):
    """Render a software project release."""

    sparql = '''
    PREFIX github: <https://octadocs.io/github/>

    SELECT * WHERE {
        $release github:name ?name .

        OPTIONAL {
            $release github:published_at ?date .
        }

        OPTIONAL {
            $release github:prerelease ?prerelease .
        }
    }
    '''

    def construct_content(self) -> Iterable[html_tag]:
        """Construct release description."""
        rows = self.query(
            self.sparql,
            release=self.iri,
        )

        row = first(rows)

        date_value = row.get('date')

        if date_value is not None:
            date_value = date_value.value

            if isinstance(date_value, datetime):
                date_value = date_value.date()

            yield code(str(date_value))
            yield br()

        yield a(
            row['name'],
            href=row['release'],
        )

    def html(self):
        """Draw release description."""
        return span(
            *self.construct_content(),
            cls='octadocs-github-release',
        )
