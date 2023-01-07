from pathlib import Path
from typing import Dict, Iterable, Type

from rdflib import URIRef
from urlpath import URL

from iolanta.loaders.http import HTTP
from iolanta.loaders.local_directory import Loader, LocalDirectory
from iolanta.loaders.local_file import LocalFile
from iolanta.loaders.scheme_choice import SchemeChoiceLoader
from iolanta.models import LDContext, LDDocument, Quad


def choose_loader_by_url(url: URL) -> Type[Loader[URL]]:
    """Find loader by URL scheme."""
    return LocalDirectory


def as_document(url: URL) -> LDDocument:
    """Retrieve the document presented by the specified URL."""
    return LocalFile().as_jsonld_document(url)


def construct_root_loader() -> SchemeChoiceLoader:
    # FIXME This is hardcoded, and that not a very good thing. Need to make this
    #   extensible somehow.
    #     - endpoints,
    #     - or maybe something akin to `typecasts`,
    #     - or whatever.
    return SchemeChoiceLoader(
        loader_by_scheme={
            'file': LocalDirectory(),
            'http': HTTP(),
            'https': HTTP(),
        },
    )


def as_quad_stream(
    url: URL,
    iri: URIRef,
    default_context: LDContext,
    root_directory: Path,
    named_contexts: Dict[str, LDContext],
) -> Iterable[Quad]:
    """Retrieve the stream presented by the specified URL."""
    root_loader = construct_root_loader(
        default_context=default_context,
        root_directory=root_directory,
    )

    return root_loader.as_quad_stream(
        source=url,
        iri=iri,
        context=default_context,
    )
