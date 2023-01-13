# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

from dataclasses import dataclass, field
from typing import List, Optional
from tgclients.databinding.textgrid_metadata_2010 import Object

__NAMESPACE__ = "http://www.textgrid.info/namespaces/middleware/tgsearch"


@dataclass
class FulltextType:
    kwic: List["FulltextType.Kwic"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.textgrid.info/namespaces/middleware/tgsearch",
        }
    )
    hits: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )

    @dataclass
    class Kwic:
        left: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.textgrid.info/namespaces/middleware/tgsearch",
                "required": True,
            }
        )
        match: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.textgrid.info/namespaces/middleware/tgsearch",
                "required": True,
            }
        )
        right: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.textgrid.info/namespaces/middleware/tgsearch",
                "required": True,
            }
        )
        xpath: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "http://www.textgrid.info/namespaces/middleware/tgsearch",
            }
        )
        ref_id: Optional[str] = field(
            default=None,
            metadata={
                "name": "refId",
                "type": "Attribute",
            }
        )
        ref_title: Optional[str] = field(
            default=None,
            metadata={
                "name": "refTitle",
                "type": "Attribute",
            }
        )


@dataclass
class EntryType:
    class Meta:
        name = "entryType"

    textgrid_uri: Optional[str] = field(
        default=None,
        metadata={
            "name": "textgridUri",
            "type": "Element",
            "namespace": "http://www.textgrid.info/namespaces/middleware/tgsearch",
            "required": True,
        }
    )
    format: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.textgrid.info/namespaces/middleware/tgsearch",
            "required": True,
        }
    )
    title: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.textgrid.info/namespaces/middleware/tgsearch",
            "required": True,
        }
    )


@dataclass
class FacetType:
    class Meta:
        name = "facetType"

    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )
    count: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class RelationType:
    class Meta:
        name = "relationType"

    s: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.textgrid.info/namespaces/middleware/tgsearch",
            "required": True,
        }
    )
    p: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.textgrid.info/namespaces/middleware/tgsearch",
            "required": True,
        }
    )
    o: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://www.textgrid.info/namespaces/middleware/tgsearch",
            "required": True,
        }
    )


@dataclass
class Revisions:
    class Meta:
        name = "revisions"
        namespace = "http://www.textgrid.info/namespaces/middleware/tgsearch"

    revision: List[int] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    textgrid_uri: Optional[str] = field(
        default=None,
        metadata={
            "name": "textgridUri",
            "type": "Attribute",
        }
    )


@dataclass
class TextgridUris:
    class Meta:
        name = "textgridUris"
        namespace = "http://www.textgrid.info/namespaces/middleware/tgsearch"

    textgrid_uri: List[str] = field(
        default_factory=list,
        metadata={
            "name": "textgridUri",
            "type": "Element",
        }
    )
    hits: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    start: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    limit: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class FacetGroupType:
    class Meta:
        name = "facetGroupType"

    facet: List[FacetType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.textgrid.info/namespaces/middleware/tgsearch",
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class PathType:
    class Meta:
        name = "pathType"

    entry: List[EntryType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.textgrid.info/namespaces/middleware/tgsearch",
            "min_occurs": 1,
        }
    )


@dataclass
class RelationResponseType:
    class Meta:
        name = "relationResponseType"

    relation: List[RelationType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.textgrid.info/namespaces/middleware/tgsearch",
        }
    )


@dataclass
class FacetResponse:
    class Meta:
        name = "facetResponse"
        namespace = "http://www.textgrid.info/namespaces/middleware/tgsearch"

    facet_group: List[FacetGroupType] = field(
        default_factory=list,
        metadata={
            "name": "facetGroup",
            "type": "Element",
        }
    )


@dataclass
class FacetResponseType:
    class Meta:
        name = "facetResponseType"

    facet_group: List[FacetGroupType] = field(
        default_factory=list,
        metadata={
            "name": "facetGroup",
            "type": "Element",
            "namespace": "http://www.textgrid.info/namespaces/middleware/tgsearch",
        }
    )


@dataclass
class PathGroupType:
    class Meta:
        name = "pathGroupType"

    path: List[PathType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.textgrid.info/namespaces/middleware/tgsearch",
        }
    )
    start_uri: Optional[str] = field(
        default=None,
        metadata={
            "name": "startUri",
            "type": "Attribute",
        }
    )


@dataclass
class PathResponse:
    class Meta:
        name = "pathResponse"
        namespace = "http://www.textgrid.info/namespaces/middleware/tgsearch"

    path_group: List[PathGroupType] = field(
        default_factory=list,
        metadata={
            "name": "pathGroup",
            "type": "Element",
        }
    )


@dataclass
class ResultType:
    class Meta:
        name = "resultType"

    object_value: Optional[Object] = field(
        default=None,
        metadata={
            "name": "object",
            "type": "Element",
            "namespace": "http://textgrid.info/namespaces/metadata/core/2010",
            "required": True,
        }
    )
    fulltext: List[FulltextType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://www.textgrid.info/namespaces/middleware/tgsearch",
        }
    )
    path_response: Optional[PathResponse] = field(
        default=None,
        metadata={
            "name": "pathResponse",
            "type": "Element",
            "namespace": "http://www.textgrid.info/namespaces/middleware/tgsearch",
        }
    )
    textgrid_uri: Optional[str] = field(
        default=None,
        metadata={
            "name": "textgridUri",
            "type": "Attribute",
        }
    )
    authorized: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    sandbox: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    author: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Response:
    class Meta:
        name = "response"
        namespace = "http://www.textgrid.info/namespaces/middleware/tgsearch"

    result: List[ResultType] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )
    relation_response: Optional[RelationResponseType] = field(
        default=None,
        metadata={
            "name": "relationResponse",
            "type": "Element",
        }
    )
    facet_response: Optional[FacetResponseType] = field(
        default=None,
        metadata={
            "name": "facetResponse",
            "type": "Element",
        }
    )
    hits: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    session: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    start: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    limit: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
