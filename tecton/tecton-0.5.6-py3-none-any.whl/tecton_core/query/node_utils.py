from dataclasses import dataclass
from typing import Optional

from tecton_core.query.node_interface import NodeRef


@dataclass
class AsofJoinInputContainer:
    node: NodeRef
    timestamp_field: str  # spine or feature timestamp
    effective_timestamp_field: Optional[str] = None
    prefix: Optional[str] = None
