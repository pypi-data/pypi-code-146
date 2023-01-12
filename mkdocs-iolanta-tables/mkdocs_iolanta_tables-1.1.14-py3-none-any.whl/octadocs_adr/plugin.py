from pathlib import Path
from typing import Optional

from mkdocs.config import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page
from rdflib import URIRef

from iolanta.conversions import path_to_url
from mkdocs_iolanta.mixins import OctadocsMixin, TemplateContext
from octadocs_adr.models import ADR


class ADRPlugin(OctadocsMixin):
    """Decisions plugin automatically presents MkDocs pages as ADR documents."""

    namespaces = {'adr': ADR}

    @property
    def templates_path(self) -> Path:
        """Templates associated with the plugin."""
        return Path(__file__).parent / 'templates'

    def on_config(self, config, **kwargs):
        """Adjust configuration."""
        super().on_config(config, **kwargs)

        # Make plugin's templates available to MkDocs
        config['theme'].dirs.append(str(self.templates_path))

        # Load the triples
        self.iolanta.add(
            path_to_url(
                Path(__file__).parent / 'yaml/octadocs-adr.yaml',
            ),
        )

    def on_page_context(
        self,
        context: TemplateContext,
        page: Page,
        config: Config,
        nav: Page,
    ) -> TemplateContext:
        return {
            **super().on_page_context(
                context=context,
                page=page,
                config=config,
                nav=nav,
            ),

            'ADR': ADR,
        }
