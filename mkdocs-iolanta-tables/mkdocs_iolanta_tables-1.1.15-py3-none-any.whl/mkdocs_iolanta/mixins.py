import json
import logging
import operator
import re
from functools import cached_property, partial
from pathlib import Path
from typing import Any, Callable, Dict, Optional, TypedDict, Union

from mkdocs.config import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page
from rdflib import SDO, ConjunctiveGraph, Namespace, URIRef

from iolanta.conversions import path_to_url
from iolanta.errors import FacetNotFound
from iolanta.iolanta import Iolanta
from iolanta.loaders.base import term_for_python_class
from iolanta.loaders.local_directory import merge_contexts
from iolanta.models import LDContext, Triple
from iolanta.namespaces import IOLANTA
from iolanta.parsers.yaml import YAML
from iolanta.renderer import Render, render
from iolanta.shortcuts import construct_root_loader
from mkdocs_iolanta.conversions import iri_by_page
from mkdocs_iolanta.storage import save_graph
from mkdocs_iolanta.types import MKDOCS

logger = logging.getLogger(__name__)


class TemplateContext(TypedDict):
    """Context for the native MkDocs page rendering engine."""

    graph: ConjunctiveGraph
    iri: URIRef
    this: URIRef
    local: Namespace
    render: Callable[[URIRef], str]

    # FIXME this is hardcode and should be removed
    rdfs: Namespace


def _construct_default_context(config: Config):
    context_paths = [
        Path(__file__).parent / 'yaml/context.yaml',
        *config['extra']['contexts'],
    ]

    context_contents = [
        YAML().as_jsonld_document(path.open('r'))
        for path in context_paths
    ]

    for context in context_contents:
        if isinstance(context, list):
            raise ValueError('Context cannot be a list: %s', context)

    return merge_contexts(*context_contents)   # type: ignore


class OctadocsMixin(BasePlugin):   # type: ignore   # noqa: WPS338, WPS214
    """MkDocs plugin that aims to extend Octadocs functionality."""

    iolanta: Iolanta
    namespaces: Optional[Dict[str, Namespace]] = None
    plugin_data_dir: Path
    docs_dir: Path

    @property
    def graph(self) -> ConjunctiveGraph:
        """Shortcut to access RDFLib graph."""
        return self.iolanta.graph

    @cached_property
    def templates_path(self) -> Optional[Path]:
        """Templates associated with the plugin."""
        path = Path(__file__).parent / 'templates'
        if path.exists():
            return path

        return None

    @property
    def cache_directory(self) -> Path:
        """Disk path for mkdocs-iolanta pickled graph."""
        (directory := self.docs_dir.parent / '.cache').mkdir(exist_ok=True)
        return directory

    @property
    def cache_file(self) -> Path:
        """Disk path for mkdocs-iolanta pickled graph."""
        return self.cache_directory / 'octadocs'

    def on_config(self, config, **kwargs):
        """Adjust system configuration to suit this plugin."""
        # Make plugin's templates available to MkDocs
        if self.templates_path:
            config['theme'].dirs.append(str(self.templates_path))

        docs_dir = Path(config['docs_dir'])
        self.docs_dir = docs_dir

        config.setdefault('extra', {})
        extra = config['extra']

        try:
            self.iolanta = extra['iolanta']
        except KeyError:
            # FIXME we're not loading the graph from cache.
            #   That's because we do not have any kind of cache invalidation.
            self.iolanta = Iolanta(
                loader=construct_root_loader(),
            )

        extra['iolanta'] = self.iolanta

        self.bind_namespaces()

    @property
    def query(self):
        """
        Execute a SPARQL query.

        Convenience method for plugin writers.
        """
        return self.iolanta.query

    def insert(self, *triples: Triple):
        """Insert triples into graph."""
        graph = term_for_python_class(self.__class__)
        quads = map(
            operator.methodcaller('as_quad', graph),
            triples,
        )
        self.graph.addN(quads)

    def save_graph_to_cache(   # type: ignore
        self,
        config: Union[Dict[str, Any], MkDocsConfig],
    ):
        """Pickle the graph to reuse it in CLI and other tools."""
        extra = config['extra']
        if extra.get('save_graph_to_cache'):
            return

        try:
            graph = self.iolanta.graph
        except AttributeError:
            logger.error(
                'Cannot save Iolanta graph to disk because graph has not '
                'been initialized yet.',
            )
            return

        save_graph(
            graph=graph,
            path=self.cache_file,
        )
        logger.info('Saved graph to disk for CLI to use.')

        extra['save_graph_to_cache'] = True

    def bind_namespaces(self) -> None:
        """Configure default namespaces for mkdocs-iolanta."""
        namespaces = (
            self.namespaces or {}
        )

        # Default namespaces for mkdocs-iolanta.
        namespaces.update({
            'mkdocs': MKDOCS,
            'iolanta': IOLANTA,
            'schema': SDO,   # type: ignore

            'docs': Namespace('docs://'),
            'local': Namespace('local:'),
        })

        self.iolanta.bind_namespaces(**namespaces)

    def on_page_markdown(
        self,
        markdown: str,
        page: Page,
        config: Config,
        files: Files,
    ):
        """Inject page template path, if necessary."""
        page.iri = iri_by_page(page)   # type: ignore

        try:
            template_url = Render(
                ldflex=self.iolanta.ldflex,
            ).find_facet_iri(
                node=page.iri,   # type: ignore
                environments=[URIRef(MKDOCS)],
            )
        except FacetNotFound:
            return markdown

        page.meta['template'] = re.sub(
            '^templates:/*',
            '',
            template_url,
        )

        return markdown

    def on_shutdown(self) -> None:
        """Save the graph to disk when MkDocs is closing."""
        self.save_graph_to_cache(config={'extra': {}})

    def on_build_error(self, error):
        """Save the graph to a file on build error."""
        self.save_graph_to_cache(config={'extra': {}})

    def on_post_build(self, config: MkDocsConfig):
        """Save the graph to a file on disk."""
        self.save_graph_to_cache(config)

    def _inference_and_navigation(
        self,
        config: Config,
        nav: Navigation,
    ) -> Navigation:
        extra = config['extra']
        if extra.get('_inference_and_navigation'):
            return nav

        self._compute_urls(
            navigation=nav,
            context=config['extra']['default_context'],
        )

        # This must run after all on_files() handlers of all plugins, but before
        # any page rendering and facets. Nav calculation depends on inference,
        # that's why we call it here in on_nav().
        self.iolanta.infer()

        extra['_inference_and_navigation'] = True

        return nav

    def on_nav(
        self,
        nav: Navigation,
        config: Config,
        files: Files,
    ) -> Navigation:
        """Update the site's navigation from the knowledge graph."""
        return self._inference_and_navigation(
            config=config,
            nav=nav,
        )

    def on_page_context(  # type: ignore
        self,
        context: Dict[str, Any],
        *,
        page: Page,
        config: MkDocsConfig,
        nav: Navigation,
    ) -> Dict[str, Any]:
        """Attach the views to certain pages."""
        context['render'] = partial(
            render,
            iolanta=self.iolanta,
        )
        return context

    def _add_files(self, config: Config):
        extra = config['extra']
        if extra.get('_add_files'):
            return

        default_context = _construct_default_context(config)
        extra['default_context'] = default_context

        docs_dir_url = path_to_url(self.docs_dir)

        self.iolanta.add(
            docs_dir_url,
            graph_iri=URIRef('docs://'),
            context=default_context,
        )

        self.iolanta.add(
            path_to_url(
                Path(__file__).parent / 'yaml/octadocs.yaml',
            ),
            context=default_context,
        )

        self.iolanta.add(
            path_to_url(
                Path(__file__).parent / 'yaml/iolanta.yaml',
            ),
            context=default_context,
        )

        extra['_add_files'] = True

    def on_files(self, files: Files, config: Config):
        """Extract metadata from files and compose the site graph."""
        self._add_files(config)

    def _compute_urls(self, navigation: Navigation, context: LDContext):
        """Assign a URL to every MkDocs page."""
        mapping = [
            {
                '@id': f'docs://{page.file.src_path}',  # noqa: WPS237
                'mkdocs:url': page.abs_url,
            }
            for page in navigation.pages
            if page.is_page
        ]

        document = {
            '@context': {
                'mkdocs': str(MKDOCS),
            },
            '@included': mapping,
        }

        urls_file = self.cache_directory / 'urls.json'

        urls_file.write_text(
            json.dumps(
                document,
            ),
        )

        self.iolanta.add(
            source=path_to_url(urls_file),
            graph_iri=URIRef('https://mkdocs.iolanta.tech/urls/'),
            context=context,
        )
