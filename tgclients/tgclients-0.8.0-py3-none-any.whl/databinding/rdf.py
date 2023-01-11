# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

from dataclasses import dataclass, field
from typing import List

__NAMESPACE__ = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"


@dataclass
class RdfType:
    """
    Content may be in any namespace (namespace=##any, see
    http://www.w3.org/TR/xmlschema-1/#declare-openness) and the elements are
    only validated if a schema is available that uniquely determines the
    declaration (processContents="lax", see
    http://www.w3.org/TR/xmlschema-1/#declare-openness)
    """
    class Meta:
        name = "rdfType"

    any_element: List[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
        }
    )


@dataclass
class Rdf(RdfType):
    class Meta:
        name = "RDF"
        namespace = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
