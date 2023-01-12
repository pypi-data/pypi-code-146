import shelve  # noqa: S403
from pathlib import Path

import rdflib

from iolanta.graph_providers.base import GraphProvider


class MkDocsIolantaGraphProvider(GraphProvider):
    """Graph from local MkDocs installation."""

    def retrieve_graph(self) -> rdflib.Dataset:
        """Graph from cache."""
        path = Path.cwd() / '.cache/octadocs'

        with shelve.open(str(path)) as db:   # noqa: S301
            return db['graph']
