from dominate.tags import a, img, span
from more_itertools import first
from urlpath import URL

from iolanta.facet import Facet


class GithubRepo(Facet):
    """Render a link to a GitHub repo."""

    def octicon_path(self, name: str):
        """Path to octicon."""
        return URL(
            'https://raw.githubusercontent.com/squidfunk/mkdocs-material/master'
            '/material/.icons/octicons',
        ) / f'{name}.svg'

    @property
    def icon(self):
        return span(
            img(
                src=self.octicon_path('mark-github-16'),
            ),
            cls='twemoji',
        )

    def html(self):
        """Render as a link."""
        label = first(
            self.query(
                '''
            SELECT ?label WHERE { ?repo rdfs:label ?label }
            ''',
                repo=self.uriref,
            ),
        )['label']

        return a(
            self.icon,
            ' ',
            label,
            href=self.iri,
            target='_blank',
        )
