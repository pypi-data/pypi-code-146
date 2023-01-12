from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel
class PropertyValue(BaseModel):
    property_id: int
    property_name: Optional[str]
    scale_id: Optional[int]
    scale_name: Optional[str]
    value_ids: List[int]
    values: List[str]