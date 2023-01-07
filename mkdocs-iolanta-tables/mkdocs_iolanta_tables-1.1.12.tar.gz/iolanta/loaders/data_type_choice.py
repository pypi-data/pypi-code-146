from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional

from rdflib import URIRef
from urlpath import URL

from iolanta.loaders.base import Loader
from iolanta.models import LDContext, LDDocument, Quad


@dataclass(frozen=True)
class DataTypeChoiceLoader(Loader[Any]):   # type: ignore
    """Try to load a file via several loaders."""

    loader_by_data_type: Dict[type, Loader[Any]]    # type: ignore

    def resolve_loader(self, source: Any):   # type: ignore
        """Find loader instance by URL."""
        try:
            return self.loader_by_data_type[source.scheme]
        except KeyError:
            raise ValueError(f'Cannot find a loader for URL: {source}')

    def as_jsonld_document(
        self,
        source: URL,
        iri: Optional[URIRef] = None,
    ) -> LDDocument:
        """Represent a file as a JSON-LD document."""
        return self.resolve_loader(
            source=source,
        ).as_jsonld_document(
            source=source,
            iri=iri,
        )

    def as_quad_stream(
        self,
        source: str,
        iri: Optional[URIRef],
        root_loader: Optional[Loader[URL]] = None,
        context: Optional[LDContext] = None,
    ) -> Iterable[Quad]:
        """Convert data into a stream of RDF quads."""
        return self.resolve_loader(
            source=source,
        ).as_quad_stream(
            source=source,
            iri=iri,
            root_loader=root_loader or self,
            context=context,
        )
