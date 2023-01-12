from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CodesysAttributes:

    class Meta:
        name = 'attributes'

    xmlns: str = field(
        default="",
        metadata=dict(
            type="Attribute"
        )
    )

    attribute: List["CodesysAttribute"] = field(
        default_factory=list,
        metadata=dict(
            type="Element",
            namespace="http://www.plcopen.org/xml/tc6_0201",
            min_occurs=0,
            max_occurs=9223372036854775807
        )
    )


@dataclass
class CodesysAttribute:

    class Meta:
        name = 'attribute'

    guid: str = field(
        default="",
        metadata=dict(
            type="Attribute"
        )
    )

    content: Optional[object] = field(
        default=None,
        metadata=dict(
            type="Wildcard",
            namespace="##any"
        )
    )


@dataclass
class XHTML:

    value: Optional[str] = field(default=None)
