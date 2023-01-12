from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel

class PropertyValue(BaseModel):
    value_id: Optional[int] = None
    name: str
    scale_id: Optional[int] = None
    equal_to: List[int]
    
class Scale(BaseModel):
    scale_id: int
    display_name: str
    description: str

class ProductProperty(BaseModel):
    """
    Taxonomy Product Properties
    """
    property_id: int
    name: str
    display_name: str
    scales: List[Scale]
    is_required: bool
    supports_attributes: bool
    supports_variations: bool
    is_multivalued: bool
    max_values_allowed: Optional[int]
    possible_values: List[PropertyValue]
    selected_values: List[PropertyValue]

class Taxonomy(BaseModel):
    id: int
    level: int
    name: str
    children: List[Taxonomy]
    full_path_taxonomy_ids: List[int]
    parent_id: Optional[int] = None