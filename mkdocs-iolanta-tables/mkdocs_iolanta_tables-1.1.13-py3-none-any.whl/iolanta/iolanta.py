import functools
import logging
from dataclasses import dataclass, field
from functools import cached_property
from typing import Dict, Optional

import owlrl
from owlrl import OWLRL_Extension
from rdflib import ConjunctiveGraph, Namespace, URIRef
from urlpath import URL

from iolanta.conversions import url_to_path
from iolanta.loaders import Loader
from iolanta.loaders.base import SourceType
from iolanta.models import LDContext
from iolanta.namespaces import LOCAL
from iolanta.shortcuts import construct_root_loader
from ldflex import LDFlex


@dataclass
class Iolanta:
    """Iolanta is a Semantic web browser."""

    loader: Loader[SourceType]
    graph: ConjunctiveGraph = field(
        default_factory=functools.partial(
            ConjunctiveGraph,
            identifier=LOCAL.term('_inference'),
        ),
    )
    namespaces: Dict[str, Namespace] = field(default_factory=dict)

    logger: logging.Logger = field(
        default_factory=functools.partial(
            logging.getLogger,
            name='iolanta',
        ),
    )

    @cached_property
    def ldflex(self) -> LDFlex:
        """LDFlex is a wrapper to make SPARQL querying RDF graphs bearable."""
        return LDFlex(self.graph)

    def add(
        self,
        source: URL,
        context: Optional[LDContext] = None,
        graph_iri: Optional[URIRef] = None,
    ) -> 'Iolanta':
        """Parse & load information from given URL into the graph."""
        quads = list(
            self.loader.as_quad_stream(
                source=source,
                iri=graph_iri,
                context=context,
                root_loader=self.loader,
            ),
        )

        self.graph.addN(quads)

        return self

    def infer(self) -> 'Iolanta':
        self.logger.info('Inference: OWL RL started...')
        owlrl.DeductiveClosure(OWLRL_Extension).expand(self.graph)
        self.logger.info('Inference: OWL RL complete.')

        return self

    def bind_namespaces(self, **mappings: Namespace) -> 'Iolanta':
        """Bind namespaces."""
        for prefix, namespace in mappings.items():
            self.graph.bind(prefix=prefix, namespace=namespace)

        return self

    @property
    def query(self):
        return self.ldflex.query
