import logging
from pathlib import Path
from typing import Any, Dict

from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page
from rdflib import URIRef
from urlpath import URL

from iolanta import as_document
from iolanta.models import LDContext
from mkdocs_iolanta.mixins import OctadocsMixin
from octadocs_telegram.models import TELEGRAM

logger = logging.getLogger(__name__)


class TelegramPlugin(OctadocsMixin, BasePlugin):
    """Telegram links plugins."""

    plugin_data_dir = Path(__file__).parent / 'data'
    sparql_query = '''
    PREFIX telegram: <%s>

    INSERT {
        ?url a telegram:TelegramLink .
    } WHERE {
        { ?url ?p ?o . } UNION { ?s ?p ?url }

        FILTER(
            STRSTARTS(
                str(?url),
                "https://t.me/"
            )
        ) .
    }
    ''' % TELEGRAM

    def named_contexts(self) -> Dict[str, LDContext]:
        """Reusable named contexts."""
        return {
            'telegram': as_document(
                URL('file://', self.plugin_data_dir / 'named-context.yaml'),
            ),
        }

    def vocabularies(self) -> Dict[URIRef, Path]:
        """Load IBIS ontology."""
        return {
            URIRef(TELEGRAM): self.plugin_data_dir / 'telegram.yaml',
        }

    @property
    def templates_path(self) -> Path:
        """Templates associated with the plugin."""
        return Path(__file__).parent / 'templates'

    def on_page_context(
        self,
        context: Dict[str, Any],
        page: Page,
        **kwargs,
    ):
        """Make custom functions available to the template."""
        return {
            **context,
            'telegram': TELEGRAM,
        }

    def inference(self):
        logger.info('Marking Telegram links as such...')
        self.octiron.ldflex.graph.update(self.sparql_query)
