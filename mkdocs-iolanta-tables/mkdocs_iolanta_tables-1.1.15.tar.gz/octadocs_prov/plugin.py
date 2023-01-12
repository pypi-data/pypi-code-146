from pathlib import Path
from typing import Dict

from mkdocs.plugins import BasePlugin
from rdflib import PROV, URIRef
from urlpath import URL

from iolanta import as_document
from iolanta.models import LDContext
from mkdocs_iolanta.mixins import OctadocsMixin
from mkdocs_iolanta.types import MKDOCS


class ProvenancePlugin(OctadocsMixin, BasePlugin):
    """Render an HTML table from data presented in the graph."""

    plugin_data_dir = Path(__file__).parent / 'data'

    def named_contexts(self) -> Dict[str, LDContext]:
        """Reusable named contexts."""
        return {
            'prov': as_document(
                URL('file://', self.plugin_data_dir / 'named-context.json'),
            ),
        }

    def vocabularies(self) -> Dict[URIRef, Path]:
        """Load PROV-O ontology."""
        return {
            URIRef(PROV): self.plugin_data_dir / 'prov.json',
            URIRef(MKDOCS.term('prov')): (
                self.plugin_data_dir / 'inference.yaml'
            ),
        }
