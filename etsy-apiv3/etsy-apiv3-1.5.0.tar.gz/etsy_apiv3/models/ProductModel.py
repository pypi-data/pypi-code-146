from __future__ import annotations
from typing import List
from pydantic import BaseModel
from .OfferingModel import Offering
from .PropertyValueModel import PropertyValue

class Product(BaseModel):
    product_id: int
    sku: str
    is_deleted: bool
    offerings: List[Offering]
    property_values: List[PropertyValue]