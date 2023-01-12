import itertools
from dataclasses import dataclass
from typing import Iterable, Optional, Set, Tuple, Type, Union

from boltons.iterutils import remap
from more_itertools import first, last
from rdflib import OWL, RDF, RDFS, BNode, Graph, Namespace, URIRef
from rdflib.namespace import DefinedNamespace

from autocontext.models import AUTO
from iolanta.models import LDContext


@dataclass
class AutoContextBuilder:
    """Build JSON-LD context for a graph."""

    graph: Graph
    namespace: Optional[Union[Type[DefinedNamespace], URIRef]] = None
    exclude: Optional[Set[URIRef]] = None

    def build(self) -> LDContext:
        """Construct context."""
        rules = dict(self.construct_rules())
        shortcut_rules = dict(self.construct_shortcut_rules(rules))
        return self.add_namespace_rules({
            **rules,
            **shortcut_rules,
        })

    def compact(self, iri: URIRef) -> Tuple[Optional[str], Optional[str], str]:
        """Create a compact form of an IRI."""
        qname = self.graph.compute_qname(iri)
        try:
            namespace_name, namespace_iri, term = qname
        except ValueError:
            return None, None, str(iri)

        return namespace_name, namespace_iri, f'{namespace_name}:{term}'

    def range_by_property(self) -> Iterable[Tuple[URIRef, URIRef]]:
        range_triples = self.graph.triples((None, RDFS.range, None))

        range_pairs = [
            (property_type, value_type)
            for property_type, _range, value_type
            in range_triples
        ]

        grouped_range_pairs = itertools.groupby(
            sorted(
                range_pairs,
                key=first,
            ),
            key=first,
        )

        range_types_by_property = {
            property_type: set(map(last, pairs))
            for property_type, pairs in grouped_range_pairs
        }

        node_types = {OWL.Thing, RDFS.Resource}
        for property_type, range_types in range_types_by_property.items():
            if self.namespace and not property_type.startswith(self.namespace):
                continue

            if self.exclude and property_type in self.exclude:
                continue

            if range_types & node_types:
                yield property_type, {
                    '@type': '@id',
                }

    def construct_rules(self):
        yield from self.range_by_property()

    def construct_shortcut_rules(self, rules: LDContext):
        for term, _has_shortcut, shortcut in self.graph.triples((None, AUTO.shortcut, None)):
            yield str(shortcut), {
                '@id': term,
                **rules.get(term, {}),
            }

    def add_namespace_rules(self, rules: LDContext) -> LDContext:
        """
        Compact all URIRef instances in the context, converting them to
        QName strings, and add declarations for namespaces which those
        strings are referencing.

        This function is quite dirty. I did not yet find a way
        to make it better.
        """
        namespaces = {}

        def context_post_processor(path, key, value):
            if isinstance(key, URIRef):
                key_ns_name, key_ns_iri, key = self.compact(key)

                if key_ns_name:
                    namespaces[key_ns_name] = key_ns_iri

            if isinstance(value, URIRef):
                value_ns_name, value_ns_iri, value = self.compact(value)

                if value_ns_name:
                    namespaces[value_ns_name] = value_ns_iri

            return key, value

        rules = remap(rules, context_post_processor)

        return {
            **namespaces,
            **rules,
        }
