import operator
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

from mkdocs.plugins import BasePlugin
from rdflib import RDFS, Literal, URIRef
from typer import Typer
from urlpath import URL

from iolanta import as_document
from iolanta.conversions import path_to_url
from iolanta.models import LDContext, Triple
from mkdocs_iolanta.mixins import OctadocsMixin
from octadocs_github.cli import app, logger
from octadocs_github.models import GH, SPDX


@dataclass
class Repo:
    """Repository description."""

    url: str

    @property
    def url_parts(self) -> Tuple[str, str]:
        """Parse the GitHub URL."""
        try:
            _hostname, owner_name, repo_name, *etc = URL(self.url).parts
        except ValueError as err:
            raise ValueError(
                f'{self.url} is not a valid GitHub repo URL.',
            ) from err

        return owner_name, repo_name

    @property
    def owner_name(self):
        return self.url_parts[0]

    @property
    def repo_name(self):
        return self.url_parts[1]


class GithubPlugin(OctadocsMixin):
    """Render an HTML table from data presented in the graph."""

    namespaces = {
        'gh': GH,
        'spdx': SPDX,
    }
    plugin_data_dir = Path(__file__).parent / 'data'

    def on_files(self, *args, **kwargs):
        super().on_files(*args, **kwargs)

        self.iolanta.add(
            path_to_url(
                self.plugin_data_dir / 'github.yaml',
            ),
        )

    def typer(self) -> Typer:
        """Typer instance."""
        return app

    def named_contexts(self) -> Dict[str, LDContext]:
        """Reusable named contexts."""
        return {
            'github-generated': as_document(
                URL('file://', self.plugin_data_dir / 'gh-auto.yaml'),
            ),
            'github': as_document(
                URL('file://', self.plugin_data_dir / 'gh.yaml'),
            ),
        }

    def vocabularies(self) -> Dict[URIRef, Path]:
        """Load Github inference rules."""
        return {
            URIRef(GH): self.plugin_data_dir / 'github.yaml',
        }

    def inference(self):
        """Find all GitHub URLs and mark them."""
        logger.warning('Looking for GitHub URLs in the graph...')
        rows = self.query(
            '''
            SELECT DISTINCT ?url WHERE {
                {
                    ?url ?p ?o
                } UNION {
                    ?s ?p ?url
                }

                FILTER isIRI(?url) .

                FILTER(
                    STRSTARTS(
                        str(?url),
                        "https://github.com/"
                    )
                ) .
            }
            ''',
        )

        iris = map(operator.itemgetter('url'), rows)

        for iri in iris:
            url = URL(iri)

            try:
                _hostname, owner_name, repo_name, *etc = url.parts
            except ValueError:
                continue

            if etc:
                # This is not a repo name.
                continue

            owner_iri = URIRef(f'https://github.com/{owner_name}')
            repo_label = f'{owner_name}/{repo_name}'

            self.insert(
                Triple(iri, RDFS.label, Literal(repo_label)),
                Triple(iri, GH.owner, owner_iri),
                Triple(owner_iri, RDFS.label, Literal(owner_name)),
            )
