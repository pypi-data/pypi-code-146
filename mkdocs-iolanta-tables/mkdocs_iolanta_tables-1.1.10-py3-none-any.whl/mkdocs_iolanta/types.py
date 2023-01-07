from enum import Enum
from logging import config as logging_config
from typing import Any, Dict, NamedTuple, Optional, Union

import rdflib
from rdflib import Graph, term
from typing_extensions import Protocol

from ldflex.ldflex import SelectResult

MKDOCS = rdflib.Namespace('https://mkdocs.iolanta.tech/')
IOLANTA = rdflib.Namespace('https://iolanta.tech/')
LOCAL = rdflib.Namespace('local:')


class Triple(NamedTuple):
    """RDF triple."""

    subject: rdflib.URIRef
    predicate: rdflib.URIRef
    object: Union[rdflib.URIRef, rdflib.Literal]  # noqa: WPS125

    def as_quad(self, graph: rdflib.URIRef) -> 'Quad':
        """Add graph to this triple and hence get a quad."""
        return Quad(self.subject, self.predicate, self.object, graph)


class Quad(NamedTuple):
    """Triple assigned to a named graph."""

    subject: rdflib.URIRef
    predicate: rdflib.URIRef
    object: Union[rdflib.URIRef, rdflib.Literal]  # noqa: WPS125
    graph: rdflib.URIRef


# Should be Dict[str, 'Context'] but mypy crashes on a recursive type.
Context = Optional[   # type: ignore
    Union[str, int, float, Dict[str, Any]]
]


logging_config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
})
SelectRow = Dict[str, term.Node]


QueryResult = Union[
    SelectResult,   # SELECT
    Graph,          # CONSTRUCT
    bool,           # ASK
]


class Query(Protocol):
    """Query protocol."""

    def __call__(
        self,
        query_text: str,
        instance: rdflib.ConjunctiveGraph,
        **kwargs: str,
    ) -> QueryResult:
        """Query prototype."""


class QueryResultsFormat(str, Enum):
    """Format to print query results in CLI."""

    PRETTY = 'pretty'
    CSV = 'csv'
    JSON = 'json'


class ComputedQName(NamedTuple):
    """QName computed from an URIRef."""

    namespace_name: str
    namespace_url: str
    term: str
