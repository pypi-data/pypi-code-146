import json
from dataclasses import dataclass, field
from functools import reduce
from pathlib import Path
from typing import Iterable, List, Optional, TextIO, Type, Union

from documented import DocumentedError
from rdflib import Literal, URIRef
from urlpath import URL

from iolanta.context import merge
from iolanta.conversions import url_to_iri, url_to_path
from iolanta.loaders.base import Loader
from iolanta.loaders.errors import IsAContext, ParserNotFound
from iolanta.models import LDContext, LDDocument, Quad
from iolanta.parsers.base import Parser
from iolanta.parsers.json import JSON
from iolanta.parsers.markdown import Markdown
from iolanta.parsers.yaml import YAML
from mkdocs_iolanta.types import MKDOCS


def choose_parser_by_extension(url: URL) -> Type[Parser]:
    """
    Choose parser class based on file extension.

    FIXME this is currently hard coded; need to change to a more extensible
      mechanism.
    """
    try:
        return {
            '.yaml': YAML,
            '.json': JSON,
            '.md': Markdown,
        }[url.suffix]
    except KeyError:
        raise ParserNotFound(path=url)


@dataclass(frozen=True)
class LocalFile(Loader[URL]):
    """
    Retrieve Linked Data from a file on local disk.

    Requires URL with file:// scheme as input.
    """

    def find_context(self, source: str) -> LDContext:
        return {}

    def choose_parser_class(self, source: URL) -> Type[Parser]:
        return choose_parser_by_extension(source)

    def as_quad_stream(
        self,
        source: URL,
        root_loader: Loader[URL],
        iri: Optional[URIRef] = None,
        context: Optional[LDContext] = None,
    ) -> Iterable[Quad]:
        """Extract a sequence of quads from a local file."""
        path = url_to_path(source) if isinstance(source, URL) else source

        if path.stem == 'context':
            raise IsAContext(path=source)

        try:
            parser_class = self.choose_parser_class(source)
        except ParserNotFound:
            return []

        if iri is None:
            iri = url_to_iri(source)

        with path.open() as text_io:
            yield from parser_class().as_quad_stream(
                raw_data=text_io,
                iri=iri,
                context=context,
                root_loader=root_loader,
            )

            yield Quad(
                iri,
                MKDOCS.fileName,
                Literal(path.name),
                URIRef('https://iolanta.tech/loaders/local-file'),
            )

    def as_file(self, source: URL) -> TextIO:
        """Construct a file-like object."""
        path = url_to_path(source)
        with path.open() as text_io:
            return text_io

    def as_jsonld_document(
        self,
        source: URL,
        iri: Optional[URIRef] = None,
    ) -> LDDocument:
        """As JSON-LD document."""
        parser_class: Type[Parser] = self.choose_parser_class(source)
        with url_to_path(source).open() as text_io:
            document = parser_class().as_jsonld_document(text_io)

        if iri is not None and isinstance(document, dict):
            document.setdefault('@id', str(iri))

        return document
